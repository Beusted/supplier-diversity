import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import sys
from pathlib import Path

# Add the current directory to Python path for imports
sys.path.append(str(Path(__file__).parent))

from data_analytics import POQuantityAnalytics
from auth_ui import require_authentication, get_user_role, check_permission

# Page configuration
st.set_page_config(
    page_title="Small Business PO Percentage Target Dashboard",
    page_icon="📋",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #1f4e79 0%, #2e6da4 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: white;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #2e6da4;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .status-badge {
        display: inline-block;
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        font-size: 0.875rem;
        font-weight: bold;
    }
    .status-current { background-color: #ffeaa7; color: #2d3436; }
    .status-target { background-color: #00b894; color: white; }
    .auth-info {
        background-color: #f8f9fa;
        padding: 0.5rem 1rem;
        border-radius: 5px;
        border-left: 3px solid #28a745;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

def main():
    """Main dashboard application"""
    
    # Check authentication first
    if not require_authentication():
        return
    
    # Get current user info
    user_role = get_user_role()
    
    # Show authentication status
    st.markdown(f"""
    <div class="auth-info">
        🔐 <strong>Authenticated Access</strong> | Role: {user_role.title() if user_role else 'User'}
    </div>
    """, unsafe_allow_html=True)
    
    # Main header
    st.markdown("""
    <div class="main-header">
        <h1>🏢 Small Business PO Percentage Dashboard</h1>
        <p>Cal Poly SLO AI Summer Camp - Supplier Diversity Analysis</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Initialize analytics
    analytics = POQuantityAnalytics()
    
    # Load data
    with st.spinner("Loading procurement data..."):
        test_results = analytics.load_test_results()
        detailed_analysis = analytics.load_detailed_analysis()
    
    if test_results.empty:
        st.error("❌ No data available. Please ensure the backend analysis has been run.")
        return
    
    # Calculate key metrics
    metrics = analytics.calculate_key_metrics()
    
    # Key Metrics Section
    st.markdown("## 📊 Key Performance Indicators")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="metric-card">
            <h3 style="margin: 0; color: #2e6da4;">Current Status</h3>
            <h2 style="margin: 0.5rem 0; color: #e17055;">16.3%</h2>
            <span class="status-badge status-current">208 of 1,274 POs</span>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-card">
            <h3 style="margin: 0; color: #2e6da4;">Target Goal</h3>
            <h2 style="margin: 0.5rem 0; color: #00b894;">25.0%</h2>
            <span class="status-badge status-target">319 of 1,274 POs</span>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="metric-card">
            <h3 style="margin: 0; color: #2e6da4;">Gap to Close</h3>
            <h2 style="margin: 0.5rem 0; color: #d63031;">8.7%</h2>
            <span class="status-badge" style="background-color: #fab1a0; color: #2d3436;">110 POs needed</span>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="metric-card">
            <h3 style="margin: 0; color: #2e6da4;">Progress</h3>
            <h2 style="margin: 0.5rem 0; color: #6c5ce7;">65.2%</h2>
            <span class="status-badge" style="background-color: #a29bfe; color: white;">to target</span>
        </div>
        """, unsafe_allow_html=True)
    
    # Progress visualization
    st.markdown("## 🎯 Progress Toward 25% Target")
    
    # Create progress chart
    fig_progress = go.Figure()
    
    # Current progress bar
    fig_progress.add_trace(go.Bar(
        x=[16.3],
        y=['Current Status'],
        orientation='h',
        marker_color='#e17055',
        name='Current (16.3%)',
        text='16.3% (208 POs)',
        textposition='inside'
    ))
    
    # Target bar
    fig_progress.add_trace(go.Bar(
        x=[8.7],
        y=['Current Status'],
        orientation='h',
        marker_color='#00b894',
        name='Needed to reach target',
        text='8.7% (110 POs)',
        textposition='inside'
    ))
    
    fig_progress.update_layout(
        barmode='stack',
        xaxis_title="Percentage of POs to Small Businesses",
        yaxis_title="",
        height=200,
        showlegend=True,
        xaxis=dict(range=[0, 30])
    )
    
    st.plotly_chart(fig_progress, use_container_width=True)
    
    # Implementation Strategy (Admin/Manager only)
    if check_permission('manager'):
        st.markdown("## 🚀 Implementation Strategy")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### Phase 1: Quick Wins (30 POs)")
            st.markdown("""
            - **Target**: Low-risk, high-volume suppliers
            - **Timeline**: 30-60 days
            - **Impact**: +2.4% progress toward goal
            - **Focus**: Office supplies, maintenance services
            """)
            
            st.markdown("### Phase 2: Strategic Transitions (50 POs)")
            st.markdown("""
            - **Target**: Medium-complexity procurements
            - **Timeline**: 60-120 days
            - **Impact**: +3.9% progress toward goal
            - **Focus**: IT services, consulting
            """)
        
        with col2:
            st.markdown("### Phase 3: Major Contracts (30 POs)")
            st.markdown("""
            - **Target**: High-value, complex contracts
            - **Timeline**: 120-180 days
            - **Impact**: +2.4% progress toward goal
            - **Focus**: Construction, specialized services
            """)
            
            # Implementation timeline chart
            phases = ['Phase 1\n(Quick Wins)', 'Phase 2\n(Strategic)', 'Phase 3\n(Major Contracts)']
            pos_impact = [2.4, 3.9, 2.4]
            timeline = [45, 90, 150]  # days
            
            fig_timeline = go.Figure()
            fig_timeline.add_trace(go.Scatter(
                x=timeline,
                y=pos_impact,
                mode='markers+lines+text',
                marker=dict(size=15, color=['#00b894', '#0984e3', '#6c5ce7']),
                text=phases,
                textposition='top center',
                name='Implementation Phases'
            ))
            
            fig_timeline.update_layout(
                title="Implementation Timeline & Impact",
                xaxis_title="Days from Start",
                yaxis_title="Percentage Point Impact",
                height=400
            )
            
            st.plotly_chart(fig_timeline, use_container_width=True)
    
    # Detailed Analysis (All authenticated users)
    st.markdown("## 📈 Detailed Analysis")
    
    if not detailed_analysis.empty:
        # Top opportunities
        st.markdown("### 🎯 Top Transition Opportunities")
        
        # Sort by PO count and show top 10
        top_opportunities = detailed_analysis.nlargest(10, 'po_count')
        
        fig_opportunities = px.bar(
            top_opportunities,
            x='po_count',
            y='current_supplier',
            orientation='h',
            title="Suppliers with Most POs Available for Transition",
            labels={'po_count': 'Number of POs', 'current_supplier': 'Current Supplier'}
        )
        fig_opportunities.update_layout(height=500)
        st.plotly_chart(fig_opportunities, use_container_width=True)
        
        # Show detailed table
        st.markdown("### 📋 Detailed Transition Analysis")
        
        # Format the dataframe for display
        display_df = top_opportunities.copy()
        display_df.columns = ['Current Supplier', 'Small Business Match', 'PO Count', 'Similarity Score']
        display_df['Similarity Score'] = display_df['Similarity Score'].round(3)
        
        st.dataframe(
            display_df,
            use_container_width=True,
            hide_index=True
        )
    
    # Data Export (Admin only)
    if check_permission('admin'):
        st.markdown("## 📤 Data Export")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("📊 Export Analysis Results", use_container_width=True):
                csv = detailed_analysis.to_csv(index=False)
                st.download_button(
                    label="Download CSV",
                    data=csv,
                    file_name="supplier_diversity_analysis.csv",
                    mime="text/csv"
                )
        
        with col2:
            if st.button("📈 Export Summary Report", use_container_width=True):
                summary_data = {
                    'Metric': ['Current POs to Small Business', 'Target POs', 'Gap', 'Progress %'],
                    'Value': ['208 (16.3%)', '319 (25.0%)', '110 POs', '65.2%']
                }
                summary_df = pd.DataFrame(summary_data)
                csv = summary_df.to_csv(index=False)
                st.download_button(
                    label="Download Summary CSV",
                    data=csv,
                    file_name="supplier_diversity_summary.csv",
                    mime="text/csv"
                )
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666; padding: 1rem;">
        🎓 <strong>Cal Poly SLO AI Summer Camp Project</strong><br>
        Small Business Procurement Target Analysis | Secure Dashboard
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
