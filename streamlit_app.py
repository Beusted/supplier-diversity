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
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric(
            "Current PO %",
            f"{demo_stats['current_percentage']:.1f}%",
            delta=f"{demo_stats['current_percentage'] - demo_stats['target_percentage']:.1f}%"
        )
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric(
            "Target PO %",
            f"{demo_stats['target_percentage']:.1f}%"
        )
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col3:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric(
            "Current Small Business POs",
            f"{demo_stats['current_small_business_pos']:,}"
        )
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col4:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric(
            "POs Needed to Reach Target",
            f"{demo_stats['gap_pos_needed']:,}",
            delta=f"+{demo_stats['gap_pos_needed']:,}"
        )
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Progress visualization
    st.subheader("📊 Progress Toward 25% Target")
    
    # Create progress chart
    fig = go.Figure()
    
    # Current progress
    fig.add_trace(go.Bar(
        x=['Current', 'Target'],
        y=[demo_stats['current_percentage'], demo_stats['target_percentage']],
        marker_color=['#C49214', '#154734'],
        text=[f"{demo_stats['current_percentage']:.1f}%", f"{demo_stats['target_percentage']:.1f}%"],
        textposition='auto',
    ))
    
    fig.update_layout(
        title="Small Business PO Percentage: Current vs Target (Demo Data)",
        yaxis_title="Percentage of POs",
        showlegend=False,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font_color='white'
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

# Custom CSS for Cal Poly theme
st.markdown("""
<style>
.main {
    background: linear-gradient(135deg, #154734 0%, #1a5a3e 100%);
    color: white;
}
.stApp {
    background: linear-gradient(135deg, #154734 0%, #1a5a3e 100%);
}
h1, h2, h3 {
    color: #C49214 !important;
}
.metric-card {
    background: rgba(255, 255, 255, 0.1);
    padding: 1rem;
    border-radius: 10px;
    border: 1px solid rgba(196, 146, 20, 0.3);
    margin: 0.5rem 0;
}
</style>
""", unsafe_allow_html=True)

# Header
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
        # Key metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.metric(
                "Current PO %",
                f"{current_stats['current_percentage']:.1f}%",
                delta=f"{current_stats['current_percentage'] - current_stats['target_percentage']:.1f}%"
            )
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.metric(
                "Target PO %",
                f"{current_stats['target_percentage']:.1f}%"
            )
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col3:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.metric(
                "Current Small Business POs",
                f"{current_stats['current_small_business_pos']:,}"
            )
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col4:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.metric(
                "POs Needed to Reach Target",
                f"{current_stats['gap_pos_needed']:,}",
                delta=f"+{current_stats['gap_pos_needed']:,}"
            )
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Progress visualization
        st.subheader("📊 Progress Toward 25% Target")
        
        # Create progress chart
        fig = go.Figure()
        
        # Current progress
        fig.add_trace(go.Bar(
            x=['Current', 'Target'],
            y=[current_stats['current_percentage'], current_stats['target_percentage']],
            marker_color=['#C49214', '#154734'],
            text=[f"{current_stats['current_percentage']:.1f}%", f"{current_stats['target_percentage']:.1f}%"],
            textposition='auto',
        ))
        
        fig.update_layout(
            title="Small Business PO Percentage: Current vs Target",
            yaxis_title="Percentage of POs",
            showlegend=False,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='white'
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
        st.error("❌ Unable to load data. Using demo data instead.")
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
