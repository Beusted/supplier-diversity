import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import sys
import os
from pathlib import Path

# Page configuration
st.set_page_config(
    page_title="Small Business PO Percentage Target Dashboard",
    page_icon="📋",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Enhanced Custom CSS for Cal Poly theme
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap');
    
    /* Root variables for consistent theming */
    :root {
        --poly-green: #154734;
        --poly-green-dark: #0d2e1f;
        --poly-green-light: #1a5a3e;
        --mustard-gold: #C49214;
        --mustard-gold-light: #D4A429;
        --white: #FFFFFF;
        --light-gray: #F8F9FA;
        --dark-gray: #2C3E50;
    }
    
    /* Main app styling */
    .stApp {
        background: linear-gradient(135deg, var(--poly-green) 0%, var(--poly-green-light) 100%) !important;
        font-family: 'Inter', sans-serif !important;
    }
    
    .main {
        background: transparent !important;
        color: var(--white) !important;
        font-family: 'Inter', sans-serif !important;
    }
    
    /* Header styling */
    h1 {
        color: var(--mustard-gold) !important;
        font-weight: 800 !important;
        font-size: 3rem !important;
        text-align: center !important;
        margin-bottom: 0.5rem !important;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3) !important;
    }
    
    h2, h3 {
        color: var(--mustard-gold-light) !important;
        font-weight: 700 !important;
    }
    
    /* Metric cards styling */
    .metric-card {
        background: rgba(255, 255, 255, 0.15) !important;
        padding: 1.5rem !important;
        border-radius: 15px !important;
        border: 2px solid rgba(196, 146, 20, 0.4) !important;
        margin: 0.5rem 0 !important;
        backdrop-filter: blur(10px) !important;
        box-shadow: 0 8px 32px rgba(0,0,0,0.2) !important;
        transition: transform 0.3s ease, box-shadow 0.3s ease !important;
    }
    
    .metric-card:hover {
        transform: translateY(-5px) !important;
        box-shadow: 0 12px 40px rgba(196, 146, 20, 0.3) !important;
    }
    
    /* Streamlit metric styling */
    [data-testid="metric-container"] {
        background: rgba(255, 255, 255, 0.15) !important;
        border: 2px solid rgba(196, 146, 20, 0.4) !important;
        padding: 1rem !important;
        border-radius: 15px !important;
        backdrop-filter: blur(10px) !important;
        box-shadow: 0 8px 32px rgba(0,0,0,0.2) !important;
    }
    
    [data-testid="metric-container"]:hover {
        transform: translateY(-3px) !important;
        box-shadow: 0 12px 40px rgba(196, 146, 20, 0.3) !important;
        transition: all 0.3s ease !important;
    }
    
    [data-testid="metric-container"] > div {
        color: var(--white) !important;
    }
    
    [data-testid="metric-container"] label {
        color: var(--mustard-gold-light) !important;
        font-weight: 600 !important;
    }
    
    /* Chart styling */
    .js-plotly-plot {
        border-radius: 15px !important;
        overflow: hidden !important;
        box-shadow: 0 8px 32px rgba(0,0,0,0.2) !important;
    }
    
    /* Text styling */
    .stMarkdown {
        color: var(--white) !important;
    }
    
    /* Success/Warning/Error styling */
    .stSuccess {
        background: rgba(40, 167, 69, 0.2) !important;
        border: 1px solid rgba(40, 167, 69, 0.5) !important;
        border-radius: 10px !important;
    }
    
    .stWarning {
        background: rgba(255, 193, 7, 0.2) !important;
        border: 1px solid rgba(255, 193, 7, 0.5) !important;
        border-radius: 10px !important;
    }
    
    .stError {
        background: rgba(220, 53, 69, 0.2) !important;
        border: 1px solid rgba(220, 53, 69, 0.5) !important;
        border-radius: 10px !important;
    }
    
    .stInfo {
        background: rgba(23, 162, 184, 0.2) !important;
        border: 1px solid rgba(23, 162, 184, 0.5) !important;
        border-radius: 10px !important;
    }
    
    /* Expander styling */
    .streamlit-expanderHeader {
        background: rgba(255, 255, 255, 0.1) !important;
        border-radius: 10px !important;
        color: var(--mustard-gold) !important;
    }
    
    .streamlit-expanderContent {
        background: rgba(255, 255, 255, 0.05) !important;
        border-radius: 0 0 10px 10px !important;
    }
    
    /* Custom bullet points */
    .stMarkdown ul li {
        color: var(--white) !important;
        margin-bottom: 0.5rem !important;
    }
    
    .stMarkdown strong {
        color: var(--mustard-gold-light) !important;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

def show_demo_dashboard():
    """Show a demo dashboard with sample data when real data isn't available"""
    
    # Demo data
    demo_stats = {
        'total_pos': 1274,
        'current_small_business_pos': 208,
        'current_percentage': 16.3,
        'target_percentage': 25.0,
        'target_pos_needed': 318,
        'gap_pos_needed': 110,
        'gap_percentage': 8.7,
        'current_non_small_business_pos': 1066
    }
    
    st.warning("⚠️ This is demo data. Connect your real data source for actual metrics.")
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Current PO %",
            f"{demo_stats['current_percentage']:.1f}%",
            delta=f"{demo_stats['current_percentage'] - demo_stats['target_percentage']:.1f}%"
        )
    
    with col2:
        st.metric(
            "Target PO %",
            f"{demo_stats['target_percentage']:.1f}%"
        )
    
    with col3:
        st.metric(
            "Current Small Business POs",
            f"{demo_stats['current_small_business_pos']:,}"
        )
    
    with col4:
        st.metric(
            "POs Needed to Reach Target",
            f"{demo_stats['gap_pos_needed']:,}",
            delta=f"+{demo_stats['gap_pos_needed']:,}"
        )
    
    # Progress visualization
    st.subheader("📊 Progress Toward 25% Target")
    
    # Create enhanced progress chart
    fig = go.Figure()
    
    # Current progress
    fig.add_trace(go.Bar(
        x=['Current', 'Target'],
        y=[demo_stats['current_percentage'], demo_stats['target_percentage']],
        marker_color=['#C49214', '#154734'],
        text=[f"{demo_stats['current_percentage']:.1f}%", f"{demo_stats['target_percentage']:.1f}%"],
        textposition='auto',
        textfont=dict(size=16, color='white', family='Inter'),
        hovertemplate='<b>%{x}</b><br>Percentage: %{y:.1f}%<extra></extra>'
    ))
    
    fig.update_layout(
        title={
            'text': "Small Business PO Percentage: Current vs Target (Demo Data)",
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 20, 'color': '#C49214', 'family': 'Inter'}
        },
        yaxis_title="Percentage of POs",
        showlegend=False,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white', family='Inter'),
        height=500,
        margin=dict(t=80, b=60, l=60, r=60)
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Gap analysis
    st.subheader("🎯 Gap Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Current Status")
        st.write(f"• **Total POs:** {demo_stats['total_pos']:,}")
        st.write(f"• **Small Business POs:** {demo_stats['current_small_business_pos']:,}")
        st.write(f"• **Current Percentage:** {demo_stats['current_percentage']:.1f}%")
    
    with col2:
        st.markdown("### To Reach Target")
        st.write(f"• **Target Percentage:** {demo_stats['target_percentage']:.1f}%")
        st.write(f"• **Target POs Needed:** {demo_stats['target_pos_needed']:,}")
        st.write(f"• **Additional POs Needed:** {demo_stats['gap_pos_needed']:,}")

# Header with enhanced styling
st.title("🎯 Small Business PO Percentage Dashboard")
st.markdown("**Cal Poly SLO AI Summer Camp - Supplier Diversity Analysis**")

# Railway environment indicator
if os.environ.get('RAILWAY_ENVIRONMENT'):
    st.success("🚂 Running on Railway")

# Check if we can load the analytics module
try:
    # Add the frontend directory to Python path for imports
    frontend_dir = Path(__file__).parent / "frontend"
    sys.path.append(str(frontend_dir))
    
    from analytics import POQuantityAnalytics
    
    # Initialize analytics
    analytics = POQuantityAnalytics()
    
    # Get current statistics
    current_stats = analytics.calculate_current_po_percentage()
    
    if "error" not in current_stats:
        st.success("✅ Real data loaded successfully!")
        
        # Key metrics with enhanced styling
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                "Current PO %",
                f"{current_stats['current_percentage']:.1f}%",
                delta=f"{current_stats['current_percentage'] - current_stats['target_percentage']:.1f}%"
            )
        
        with col2:
            st.metric(
                "Target PO %",
                f"{current_stats['target_percentage']:.1f}%"
            )
        
        with col3:
            st.metric(
                "Current Small Business POs",
                f"{current_stats['current_small_business_pos']:,}"
            )
        
        with col4:
            st.metric(
                "POs Needed to Reach Target",
                f"{current_stats['gap_pos_needed']:,}",
                delta=f"+{current_stats['gap_pos_needed']:,}"
            )
        
        # Progress visualization
        st.subheader("📊 Progress Toward 25% Target")
        
        # Create enhanced progress chart
        fig = go.Figure()
        
        # Current progress
        fig.add_trace(go.Bar(
            x=['Current', 'Target'],
            y=[current_stats['current_percentage'], current_stats['target_percentage']],
            marker_color=['#C49214', '#154734'],
            text=[f"{current_stats['current_percentage']:.1f}%", f"{current_stats['target_percentage']:.1f}%"],
            textposition='auto',
            textfont=dict(size=16, color='white', family='Inter'),
            hovertemplate='<b>%{x}</b><br>Percentage: %{y:.1f}%<extra></extra>'
        ))
        
        fig.update_layout(
            title={
                'text': "Small Business PO Percentage: Current vs Target",
                'x': 0.5,
                'xanchor': 'center',
                'font': {'size': 20, 'color': '#C49214', 'family': 'Inter'}
            },
            yaxis_title="Percentage of POs",
            showlegend=False,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white', family='Inter'),
            height=500,
            margin=dict(t=80, b=60, l=60, r=60)
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Gap analysis
        st.subheader("🎯 Gap Analysis")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### Current Status")
            st.write(f"• **Total POs:** {current_stats['total_pos']:,}")
            st.write(f"• **Small Business POs:** {current_stats['current_small_business_pos']:,}")
            st.write(f"• **Current Percentage:** {current_stats['current_percentage']:.1f}%")
        
        with col2:
            st.markdown("### To Reach Target")
            st.write(f"• **Target Percentage:** {current_stats['target_percentage']:.1f}%")
            st.write(f"• **Target POs Needed:** {current_stats['target_pos_needed']:,}")
            st.write(f"• **Additional POs Needed:** {current_stats['gap_pos_needed']:,}")
        
        # Implementation recommendations
        st.subheader("💡 Implementation Strategy")
        
        st.markdown(f"""
        **Key Insight:** You need to transition **{current_stats['gap_pos_needed']:,} additional POs** 
        from current suppliers to small businesses to reach the 25% target.
        
        **Recommended Approach:**
        1. **Identify Transition Opportunities:** Focus on POs that can be easily moved to small businesses
        2. **Phased Implementation:** Gradually transition POs over time to minimize disruption
        3. **Supplier Development:** Work with small businesses to ensure they can handle the volume
        4. **Monitor Progress:** Track monthly progress toward the 25% goal
        """)
        
    else:
        st.error("❌ Unable to load real data. Using demo data instead.")
        show_demo_dashboard()

except Exception as e:
    st.error(f"❌ Unable to load analytics module: {str(e)}")
    st.info("📊 Showing demo dashboard with sample data")
    show_demo_dashboard()

# Debug information
with st.expander("🔍 Debug Information"):
    st.write(f"**Current directory:** {Path.cwd()}")
    st.write(f"**Environment:** {os.environ.get('RAILWAY_ENVIRONMENT', 'local')}")
    st.write(f"**Port:** {os.environ.get('PORT', 'not set')}")
    
    backend_dir = Path(__file__).parent / "backend"
    st.write(f"**Backend directory exists:** {backend_dir.exists()}")
    
    if backend_dir.exists():
        backend_files = list(backend_dir.glob("*"))
        st.write(f"**Backend files:** {[f.name for f in backend_files]}")
    
    frontend_dir = Path(__file__).parent / "frontend"
    st.write(f"**Frontend directory exists:** {frontend_dir.exists()}")
    
    if frontend_dir.exists():
        frontend_files = list(frontend_dir.glob("*"))
        st.write(f"**Frontend files:** {[f.name for f in frontend_files]}")

# Footer
st.markdown("---")
st.markdown("**🎓 Cal Poly SLO AI Summer Camp Project** | *Empowering Small Businesses Through Data-Driven Procurement Analytics*")
