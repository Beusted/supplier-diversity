import pandas as pd

def categorize_supplier(supplier_type):
    """Categorizes a supplier as 'Small Business' or 'Big Business'."""
    small_business_types = ['OSB', 'SB', 'MB', 'DVB', 'DVBE']
    if supplier_type in small_business_types:
        return 'Small Business'
    else:
        return 'Big Business'

def analyze_supplier_diversity(file_path):
    """
    Analyzes supplier diversity from a CSV file to find products bought from
    both small and big businesses.

    Args:
        file_path (str): The path to the CSV file.

    Returns:
        dict: A dictionary where keys are product descriptions and values are
              lists of tuples, with each tuple containing the supplier name,
              original supplier type, and the business category.
    """
    try:
        df = pd.read_csv(file_path, encoding='utf-8')
    except UnicodeDecodeError:
        df = pd.read_csv(file_path, encoding='latin1')

    # Clean column names
    df.columns = df.columns.str.strip()

    # Handle NaN values in 'Supplier Type' by filling them with a placeholder
    df['Supplier Type'] = df['Supplier Type'].fillna('Unlabeled')


    # Add a 'Business Category' column
    df['Business Category'] = df['Supplier Type'].apply(categorize_supplier)

    # Group by product and find products with both 'Small Business' and 'Big Business'
    product_groups = df.groupby('Line Descr')['Business Category'].nunique()
    products_with_overlap = product_groups[product_groups > 1].index

    # Filter the DataFrame to get only the overlapping products
    result_df = df[df['Line Descr'].isin(products_with_overlap)]

    # Create a dictionary to store the results
    overlap_data = {}
    for product in products_with_overlap:
        # Get the suppliers for the current product
        product_suppliers_df = result_df[result_df['Line Descr'] == product]
        
        # Check if this product is sourced from both Small and Big businesses
        categories = product_suppliers_df['Business Category'].unique()
        if 'Small Business' in categories and 'Big Business' in categories:
            suppliers = product_suppliers_df[['Supplier Name', 'Supplier Type', 'Business Category']].drop_duplicates().to_records(index=False)
            overlap_data[product] = list(suppliers)

    return overlap_data

if __name__ == "__main__":
    file_path = "/Users/ngobrian/Downloads/csu fullerton/SLO AI Summer Camp/supplier-diversity/SLO CFS Spend Data 2024.csv"
    overlapped_products = analyze_supplier_diversity(file_path)

    if overlapped_products:
        print("Products bought from both Small and Big Businesses:")
        for product, suppliers in overlapped_products.items():
            print(f"\nProduct: {product}")
            for supplier_name, supplier_type, business_category in suppliers:
                print(f"  - Supplier: {supplier_name}, Type: {supplier_type} ({business_category})")
    else:
        print("No products found to be purchased from both Small and Big Businesses.")