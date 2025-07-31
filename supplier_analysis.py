import pandas as pd
import matplotlib.pyplot as plt

def categorize_supplier(vlookup2_value):
    """Categorizes a supplier as 'Small Business' or 'Big Business' based on vlookup2 column."""
    if pd.isna(vlookup2_value):
        return 'Big Business'
    
    vlookup2_str = str(vlookup2_value).upper()
    small_business_indicators = ['SB', 'MB', 'DVBE', 'DVB']
    
    for indicator in small_business_indicators:
        if indicator in vlookup2_str:
            return 'Small Business'
    
    return 'Big Business'

def analyze_supplier_diversity(file_path):
    """
    Analyzes supplier diversity from a CSV file to categorize suppliers.

    Args:
        file_path (str): The path to the CSV file.

    Returns:
        tuple: (small_business_count, big_business_count, total_suppliers)
    """
    try:
        df = pd.read_csv(file_path, encoding='utf-8')
    except UnicodeDecodeError:
        df = pd.read_csv(file_path, encoding='latin1')

    # Clean column names
    df.columns = df.columns.str.strip()

    # Add a 'Business Category' column based on Vlookup2
    df['Business Category'] = df['Vlookup2'].apply(categorize_supplier)

    # Get unique suppliers and their categories
    unique_suppliers = df[['Supplier Name', 'Vlookup2', 'Business Category']].drop_duplicates()
    
    small_business_count = len(unique_suppliers[unique_suppliers['Business Category'] == 'Small Business'])
    big_business_count = len(unique_suppliers[unique_suppliers['Business Category'] == 'Big Business'])
    total_suppliers = len(unique_suppliers)

    return small_business_count, big_business_count, total_suppliers, unique_suppliers

if __name__ == "__main__":
    file_path = "/Users/ngobrian/Downloads/csu fullerton/SLO AI Summer Camp/supplier-diversity/SLO CFS Spend Data 2024.csv"
    small_count, big_count, total, suppliers_df = analyze_supplier_diversity(file_path)

    print(f"Supplier Diversity Analysis:")
    print(f"Total Suppliers: {total}")
    print(f"Small Businesses: {small_count} ({small_count/total*100:.1f}%)")
    print(f"Big Businesses: {big_count} ({big_count/total*100:.1f}%)")
    
    print(f"\nSmall Business Suppliers:")
    small_businesses = suppliers_df[suppliers_df['Business Category'] == 'Small Business']
    for _, row in small_businesses.iterrows():
        print(f"  - {row['Supplier Name']} (Vlookup2: {row['Vlookup2']})")
        
    print(f"\nBig Business Suppliers:")
    big_businesses = suppliers_df[suppliers_df['Business Category'] == 'Big Business']
    for _, row in big_businesses.iterrows():
        print(f"  - {row['Supplier Name']} (Vlookup2: {row['Vlookup2']})")
    
    # Create figure with subplots
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8))
    
    # Pie chart
    labels = ['Small Business', 'Big Business']
    sizes = [small_count, big_count]
    colors = ['#4CAF50', '#FF5722']
    explode = (0.1, 0)  # explode small business slice
    
    ax1.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%',
            shadow=False, startangle=90)
    ax1.set_title('Supplier Diversity Distribution', fontsize=14, fontweight='bold')
    
    # Bar chart
    ax2.bar(labels, sizes, color=colors)
    ax2.set_title('Supplier Count Comparison', fontsize=14, fontweight='bold')
    ax2.set_ylabel('Number of Suppliers')
    ax2.set_ylim(0, max(sizes) * 1.1)
    
    # Add value labels on bars
    for i, v in enumerate(sizes):
        ax2.text(i, v + max(sizes) * 0.02, str(v), ha='center', va='bottom', fontweight='bold')
    
    # Overall title
    fig.suptitle('Supplier Diversity Analysis\nSmall Business vs Big Business', fontsize=16, fontweight='bold')
    
    # Save the plot
    plt.tight_layout()
    plt.savefig('supplier_diversity_analysis.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"\nVisualization saved as 'supplier_diversity_analysis.png'")