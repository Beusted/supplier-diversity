import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import sys
from pathlib import Path

# Add the current directory to Python path for imports
sys.path.append(str(Path(__file__).parent))

from po_quantity_analytics import POQuantityAnalytics

# Page configuration
st.set_page_config(
    page_title="Supplier Diversity Dashboard",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Page title
st.title("Small Business PO Percentage Dashboard")
st.markdown("**Cal Poly SLO AI Summer Camp - Supplier Diversity Analysis**")

# Main dashboard overview
st.markdown("""
This dashboard analyzes the percentage of Purchase Orders (POs) going to small businesses 
and provides actionable insights to reach the 25% target.
""")

# Key metrics overview
col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        label="Current Small Business PO %",
        value="16.3%",
        delta="-8.7% from target"
    )

with col2:
    st.metric(
        label="Total Purchase Orders",
        value="1,274",
        delta="208 to small businesses"
    )

with col3:
    st.metric(
        label="POs to Transition",
        value="110",
        delta="To reach 25% target"
    )

# Navigation guidance
st.markdown("---")
st.markdown("### 📋 Navigate to Other Pages:")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    **📊 Detailed Analysis**
    - Deep dive into supplier matching
    - Similarity score distributions
    - Algorithm methodology
    """)
    
    st.markdown("""
    **📋 Implementation Guide**
    - Step-by-step action plan
    - Phase-based approach
    - Progress tracking tools
    """)

with col2:
    st.markdown("""
    **📁 Data Sources**
    - Technical methodology
    - AWS architecture details
    - Data quality metrics
    """)

# Quick summary
st.markdown("---")
st.info("""
**Quick Summary**: Currently 16.3% of POs go to small businesses. 
To reach the 25% target, we need to transition 110 more POs from current suppliers to small businesses.
Use the sidebar to navigate to detailed analysis and implementation guidance.
""")
