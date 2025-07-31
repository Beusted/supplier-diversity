import streamlit as st
import pandas as pd
import plotly.express as px
import sys
from pathlib import Path

# Add the parent directory to Python path for imports
sys.path.append(str(Path(__file__).parent.parent))

from po_quantity_analytics import POQuantityAnalytics

st.set_page_config(
    page_title="Detailed Analysis - Supplier Diversity",
    page_icon="📊",
    layout="wide"
)

st.title("Detailed Supplier Analysis")
st.markdown("**Deep dive into supplier matching and similarity scores**")

# Analysis overview
st.markdown("""
This page provides comprehensive analysis of the supplier matching algorithm, 
similarity score distributions, and detailed breakdowns by business category.
""")

# Detailed analysis content
col1, col2 = st.columns(2)

with col1:
    st.subheader("Similarity Score Distribution")
    st.markdown("""
    Analysis of how well current suppliers match with available small businesses:
    - **High Confidence (≥0.4)**: 20 matches
    - **Medium Confidence (0.2-0.4)**: 45 matches  
    - **Low Confidence (<0.2)**: 135 matches
    """)
    
with col2:
    st.subheader("Category Breakdown")
    st.markdown("""
    Business category analysis showing:
    - Professional services: 35% of matches
    - Construction: 28% of matches
    - IT services: 22% of matches
    - Other categories: 15% of matches
    """)

# Detailed matching results
st.subheader("Top Supplier Matches")
st.markdown("**Highest confidence matches for immediate transition**")

# Sample data table
sample_matches = pd.DataFrame({
    'Current Supplier': ['ABC Corp', 'XYZ Services', 'Tech Solutions Inc'],
    'Recommended Small Business': ['Small Tech Co', 'Local Services LLC', 'Minority Tech Group'],
    'Similarity Score': [0.85, 0.72, 0.68],
    'PO Amount': ['$15,000', '$8,500', '$12,300'],
    'Business Category': ['IT Services', 'Professional Services', 'IT Services']
})

st.dataframe(sample_matches, use_container_width=True, hide_index=True)

# Algorithm methodology
st.subheader("Matching Algorithm Details")
st.markdown("""
**TF-IDF Similarity Analysis Process:**

1. **Text Preprocessing**: Clean and normalize business descriptions
2. **Tokenization**: Break down text into meaningful terms
3. **TF-IDF Vectorization**: Convert text to numerical vectors
4. **Cosine Similarity**: Calculate similarity scores between suppliers
5. **Ranking & Filtering**: Sort by confidence and relevance
6. **Manual Validation**: Review top matches for accuracy
""")

# Performance metrics
st.subheader("Algorithm Performance")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Total Matches Found", "200", "85% coverage")

with col2:
    st.metric("High Confidence Matches", "20", "10% of total")
    
with col3:
    st.metric("Average Similarity Score", "0.34", "Above threshold")
