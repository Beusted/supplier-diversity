import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re
import json
from typing import Dict, List, Tuple
import logging

class SupplierSimilarityMatcher:
    def __init__(self, similarity_threshold: float = 0.1):
        self.similarity_threshold = similarity_threshold
        self.vectorizer = TfidfVectorizer(
            lowercase=True,
            stop_words='english',
            ngram_range=(1, 3),
            max_features=10000,
            min_df=1,
            max_df=0.95
        )
        
    def preprocess_text(self, text: str) -> str:
        """Clean and preprocess text for better matching"""
        if pd.isna(text) or text is None:
            return ""
        
        text = str(text).lower()
        # Remove special characters but keep spaces
        text = re.sub(r'[^\w\s]', ' ', text)
        # Remove extra whitespace
        text = ' '.join(text.split())
        return text
    
    def load_purchase_data(self, csv_path: str) -> pd.DataFrame:
        """Load and preprocess purchase data"""
        df = pd.read_csv(csv_path)
        
        # Clean column names
        df.columns = df.columns.str.strip()
        
        # Extract relevant columns
        required_cols = ['Supplier Type', 'Supplier Name', 'Line Descr']
        for col in required_cols:
            if col not in df.columns:
                raise ValueError(f"Missing required column: {col}")
        
        # Add amount columns if they exist
        amount_cols = ['Goods (Amt)', 'Services (Amt)', 'Construction (Amt)', 'IT (Amt)']
        for col in amount_cols:
            if col in df.columns:
                # Clean currency formatting
                df[col] = df[col].astype(str).str.replace(r'[\$,"]', '', regex=True)
                df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
        
        # Preprocess text fields
        df['processed_description'] = df['Line Descr'].apply(self.preprocess_text)
        df['processed_supplier'] = df['Supplier Name'].apply(self.preprocess_text)
        
        return df
    
    def create_small_business_data(self) -> pd.DataFrame:
        """Create sample small business data (you'll replace with real data)"""
        sample_businesses = [
            {"name": "Green Tech Solutions", "keywords": "solar panels renewable energy installation maintenance"},
            {"name": "Local Office Supply Co", "keywords": "office supplies paper pens furniture desk chairs"},
            {"name": "Community Catering Services", "keywords": "food catering meals breakfast lunch dinner events"},
            {"name": "Eco-Friendly Cleaning", "keywords": "cleaning supplies janitorial maintenance eco friendly"},
            {"name": "Tech Repair Specialists", "keywords": "computer repair IT services laptop desktop maintenance"},
            {"name": "Local Transportation LLC", "keywords": "vehicle transportation fleet management logistics"},
            {"name": "Small Biz Consulting", "keywords": "consulting services business advice management strategy"},
            {"name": "Artisan Uniform Company", "keywords": "uniforms clothing workwear custom embroidery apparel"},
            {"name": "Regional Lab Supplies", "keywords": "laboratory equipment chemicals testing supplies scientific"},
            {"name": "Community Print Shop", "keywords": "printing services marketing materials brochures business cards"}
        ]
        
        df = pd.DataFrame(sample_businesses)
        df['processed_keywords'] = df['keywords'].apply(self.preprocess_text)
        return df
    
    def find_matches(self, purchase_df: pd.DataFrame, small_biz_df: pd.DataFrame) -> List[Dict]:
        """Find similarity matches between purchases and small businesses"""
        
        # Combine all text for vectorization
        purchase_texts = purchase_df['processed_description'].tolist()
        small_biz_texts = small_biz_df['processed_keywords'].tolist()
        
        all_texts = purchase_texts + small_biz_texts
        
        # Create TF-IDF vectors
        tfidf_matrix = self.vectorizer.fit_transform(all_texts)
        
        # Split matrices
        purchase_vectors = tfidf_matrix[:len(purchase_texts)]
        small_biz_vectors = tfidf_matrix[len(purchase_texts):]
        
        # Calculate similarity matrix
        similarity_matrix = cosine_similarity(purchase_vectors, small_biz_vectors)
        
        matches = []
        
        for i, purchase_row in purchase_df.iterrows():
            for j, small_biz_row in small_biz_df.iterrows():
                similarity_score = similarity_matrix[i, j]
                
                if similarity_score >= self.similarity_threshold:
                    # Calculate total amount for this purchase
                    amount_cols = ['Goods (Amt)', 'Services (Amt)', 'Construction (Amt)', 'IT (Amt)']
                    total_amount = 0
                    for col in amount_cols:
                        if col in purchase_df.columns:
                            total_amount += abs(purchase_row.get(col, 0))
                    
                    # Determine recommendation level
                    if similarity_score >= 0.3:
                        recommendation = "High"
                    elif similarity_score >= 0.2:
                        recommendation = "Medium"
                    else:
                        recommendation = "Low"
                    
                    match = {
                        'MatchID': f"match_{i}_{j}",
                        'CurrentSupplier': purchase_row['Supplier Name'],
                        'CurrentSupplierType': purchase_row['Supplier Type'],
                        'LineDescription': purchase_row['Line Descr'],
                        'PurchaseAmount': total_amount,
                        'SmallBusinessName': small_biz_row['name'],
                        'SmallBusinessKeywords': small_biz_row['keywords'],
                        'SimilarityScore': round(similarity_score, 4),
                        'Recommendation': recommendation,
                        'Timestamp': pd.Timestamp.now().isoformat()
                    }
                    matches.append(match)
        
        # Sort by similarity score descending
        matches.sort(key=lambda x: x['SimilarityScore'], reverse=True)
        return matches
    
    def export_results(self, matches: List[Dict], output_path: str):
        """Export matches to CSV"""
        df = pd.DataFrame(matches)
        df.to_csv(output_path, index=False)
        print(f"Exported {len(matches)} matches to {output_path}")
        
        # Print summary
        high_matches = len([m for m in matches if m['Recommendation'] == 'High'])
        medium_matches = len([m for m in matches if m['Recommendation'] == 'Medium'])
        low_matches = len([m for m in matches if m['Recommendation'] == 'Low'])
        
        print(f"\nMatch Summary:")
        print(f"High confidence: {high_matches}")
        print(f"Medium confidence: {medium_matches}")
        print(f"Low confidence: {low_matches}")
        print(f"Total matches: {len(matches)}")

def main():
    """Main execution function"""
    matcher = SupplierSimilarityMatcher(similarity_threshold=0.1)
    
    # Load purchase data
    print("Loading purchase data...")
    purchase_df = matcher.load_purchase_data("slo purchases data.csv")
    print(f"Loaded {len(purchase_df)} purchase records")
    
    # Create small business data (replace with real data later)
    print("Loading small business data...")
    small_biz_df = matcher.create_small_business_data()
    print(f"Loaded {len(small_biz_df)} small businesses")
    
    # Find matches
    print("Finding similarity matches...")
    matches = matcher.find_matches(purchase_df, small_biz_df)
    
    # Export results
    matcher.export_results(matches, "supplier_matches.csv")
    
    # Show top 10 matches
    print(f"\nTop 10 matches:")
    for i, match in enumerate(matches[:10]):
        print(f"{i+1}. {match['SmallBusinessName']} -> {match['CurrentSupplier']}")
        print(f"   Score: {match['SimilarityScore']}, Amount: ${match['PurchaseAmount']:,.2f}")
        print(f"   Description: {match['LineDescription'][:100]}...")
        print()

if __name__ == "__main__":
    main()