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
    page_title="Small Business PO Percentage Target Dashboard",
    page_icon="🏢",  # Keep this as fallback for browser tab
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS with Bootstrap Icons and Cal Poly Colors
st.markdown("""
<link href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.0/font/bootstrap-icons.css" rel="stylesheet">
<style>
    :root {
        --poly-green: #154734;
        --poly-green-light: #1a5a3e;
        --poly-green-dark: #0f3426;
        --mustard-gold: #C69214;
        --mustard-gold-light: #D4A017;
        --mustard-gold-dark: #B8860B;
        --white: #FFFFFF;
        --light-gray: #F5F5F5;
        --medium-gray: #CCCCCC;
        --dark-gray: #333333;
    }

    .main {
        background: linear-gradient(135deg, var(--poly-green) 0%, var(--poly-green-light) 100%) !important;
        font-family: 'Inter', sans-serif;
    }
    
    .block-container {
        padding-top: 2rem !important;
        padding-bottom: 2rem !important;
        background: transparent !important;
    }
    
    .dashboard-card {
        background: var(--white);
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        border-left: 4px solid var(--mustard-gold);
    }
    
    .metric-card {
        background: var(--white);
        border-radius: 8px;
        padding: 1rem;
        text-align: center;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        border-top: 3px solid var(--mustard-gold);
    }
    
    .metric-value {
        font-size: 2rem;
        font-weight: bold;
        color: var(--poly-green);
        margin: 0.5rem 0;
    }
    
    .metric-label {
        font-size: 0.9rem;
        color: var(--dark-gray);
        font-weight: 500;
    }
    
    .metric-delta {
        font-size: 0.8rem;
        color: var(--mustard-gold-dark);
        font-weight: 500;
    }
    
    .section-header {
        color: var(--white);
        font-size: 1.8rem;
        font-weight: 600;
        margin: 2rem 0 1rem 0;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    .insight-box {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 8px;
        padding: 1rem;
        margin: 1rem 0;
        border-left: 4px solid var(--mustard-gold);
    }
    
    .quick-win-item {
        background: var(--white);
        border-radius: 6px;
        padding: 0.8rem;
        margin: 0.5rem 0;
        border-left: 3px solid var(--poly-green);
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
    }
    
    .supplier-item {
        background: var(--light-gray);
        border-radius: 6px;
        padding: 0.8rem;
        margin: 0.3rem 0;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    
    .progress-bar {
        background: var(--medium-gray);
        border-radius: 10px;
        height: 20px;
        overflow: hidden;
        margin: 0.5rem 0;
    }
    
    .progress-fill {
        background: linear-gradient(90deg, var(--poly-green) 0%, var(--mustard-gold) 100%);
        height: 100%;
        border-radius: 10px;
        transition: width 0.3s ease;
    }
    
    .phase-card {
        background: var(--white);
        border-radius: 8px;
        padding: 1rem;
        margin: 0.5rem 0;
        border-left: 4px solid var(--poly-green);
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
    }
    
    .cal-poly-header {
        background: linear-gradient(90deg, var(--poly-green) 0%, var(--mustard-gold) 100%);
        color: var(--white);
        padding: 1.5rem;
        border-radius: 12px;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
    }
    
    .stMetric {
        background: var(--white) !important;
        border-radius: 8px !important;
        padding: 1rem !important;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1) !important;
        border-top: 3px solid var(--mustard-gold) !important;
    }
    
    .stMetric > div {
        color: var(--poly-green) !important;
    }
    
    .stMetric [data-testid="metric-container"] {
        background: transparent !important;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Custom button styling */
    .stButton > button {
        background: var(--mustard-gold);
        color: var(--white);
        border: none;
        border-radius: 6px;
        padding: 0.5rem 1rem;
        font-weight: 500;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        background: var(--mustard-gold-dark);
        transform: translateY(-1px);
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
    }
</style>
""", unsafe_allow_html=True)

# Cal Poly Header
st.markdown("""
<div class="cal-poly-header">
    <h1 style="margin: 0; font-size: 2.5rem;">
        <i class="bi bi-building"></i> Small Business PO Percentage Dashboard
    </h1>
    <p style="margin: 0.5rem 0 0 0; font-size: 1.1rem; opacity: 0.9;">
        Cal Poly SLO AI Summer Camp - Supplier Diversity Analysis Project
    </p>
</div>
""", unsafe_allow_html=True)

# Initialize analytics
@st.cache_data
def load_analytics():
    return POQuantityAnalytics()

analytics = load_analytics()

# Key Metrics Section
st.markdown('<h2 class="section-header"><i class="bi bi-graph-up"></i> Current Status vs Target</h2>', unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        label="Current Small Business PO %",
        value="16.3%",
        delta="-8.7% from target",
        delta_color="inverse"
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
        delta="To reach 25% target",
        delta_color="normal"
    )

with col4:
    st.metric(
        label="Target Achievement",
        value="65.2%",
        delta="34.8% remaining"
    )

# Progress Visualization
st.markdown('<h2 class="section-header"><i class="bi bi-bar-chart"></i> Progress Toward 25% Target</h2>', unsafe_allow_html=True)

# Create progress chart
fig_progress = go.Figure()

# Current progress
fig_progress.add_trace(go.Bar(
    x=['Current', 'Target'],
    y=[16.3, 25.0],
    marker_color=['#C69214', '#154734'],
    text=['16.3%', '25.0%'],
    textposition='auto',
    name='PO Percentage'
))

fig_progress.update_layout(
    title="Small Business PO Percentage: Current vs Target",
    xaxis_title="Status",
    yaxis_title="Percentage of POs",
    showlegend=False,
    height=400,
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)',
    font=dict(color='white')
)

st.plotly_chart(fig_progress, use_container_width=True)

# Gap Analysis
st.markdown('<h2 class="section-header"><i class="bi bi-clipboard-data"></i> Gap Analysis</h2>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div class="dashboard-card">
        <h3><i class="bi bi-calculator"></i> The Math</h3>
        <ul>
            <li><strong>Current:</strong> 208 POs to small businesses (16.3%)</li>
            <li><strong>Target:</strong> 318 POs to small businesses (25%)</li>
            <li><strong>Gap:</strong> 110 additional POs needed</li>
            <li><strong>Strategy:</strong> Transition existing POs to small businesses</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

with col2:
    # Create a donut chart for current distribution
    fig_donut = go.Figure(data=[go.Pie(
        labels=['Small Business POs', 'Other POs'],
        values=[208, 1066],
        hole=.6,
        marker_colors=['#154734', '#C69214']
    )])
    
    fig_donut.update_layout(
        title="Current PO Distribution",
        annotations=[dict(text='1,274<br>Total POs', x=0.5, y=0.5, font_size=16, showarrow=False)],
        height=300,
        showlegend=True,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white')
    )
    
    st.plotly_chart(fig_donut, use_container_width=True)

# Implementation Roadmap
st.markdown('<h2 class="section-header"><i class="bi bi-map"></i> Implementation Roadmap</h2>', unsafe_allow_html=True)

phases = [
    {
        "phase": "Phase 1: Quick Wins",
        "target": "30 POs",
        "timeline": "Month 1-2",
        "description": "Target suppliers with highest similarity scores and easiest transitions"
    },
    {
        "phase": "Phase 2: Strategic Partnerships",
        "target": "50 POs", 
        "timeline": "Month 3-4",
        "description": "Develop relationships with small businesses in key categories"
    },
    {
        "phase": "Phase 3: Full Implementation",
        "target": "30 POs",
        "timeline": "Month 5-6", 
        "description": "Complete remaining transitions and establish monitoring systems"
    }
]

for i, phase in enumerate(phases):
    col1, col2, col3 = st.columns([2, 1, 2])
    
    with col1:
        st.markdown(f"""
        <div class="phase-card">
            <h4><i class="bi bi-check-circle"></i> {phase['phase']}</h4>
            <p>{phase['description']}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{phase['target']}</div>
            <div class="metric-label">POs to Transition</div>
            <div class="metric-delta">{phase['timeline']}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        # Progress bar for each phase
        progress = min(100, (i + 1) * 33.33)  # Simulate progress
        st.markdown(f"""
        <div class="progress-bar">
            <div class="progress-fill" style="width: {progress}%"></div>
        </div>
        <small>Phase Progress: {progress:.0f}%</small>
        """, unsafe_allow_html=True)

# Quick Wins Section
st.markdown('<h2 class="section-header"><i class="bi bi-lightning"></i> Top Quick Win Opportunities</h2>', unsafe_allow_html=True)

quick_wins = [
    {"supplier": "Office Supplies Plus", "pos": 15, "category": "Office Supplies", "similarity": "92%"},
    {"supplier": "Tech Solutions Inc", "pos": 12, "category": "IT Equipment", "similarity": "89%"},
    {"supplier": "Facility Services Co", "pos": 10, "category": "Maintenance", "similarity": "87%"},
    {"supplier": "Print & Copy Center", "pos": 8, "category": "Printing", "similarity": "85%"},
    {"supplier": "Catering Express", "pos": 7, "category": "Food Services", "similarity": "83%"}
]

col1, col2 = st.columns(2)

with col1:
    st.markdown("### <i class='bi bi-target'></i> High-Impact Transitions", unsafe_allow_html=True)
    for win in quick_wins[:3]:
        st.markdown(f"""
        <div class="quick-win-item">
            <strong>{win['supplier']}</strong><br>
            <small><i class="bi bi-box"></i> {win['pos']} POs | <i class="bi bi-tag"></i> {win['category']} | <i class="bi bi-percent"></i> {win['similarity']} match</small>
        </div>
        """, unsafe_allow_html=True)

with col2:
    st.markdown("### <i class='bi bi-graph-up-arrow'></i> Medium-Impact Transitions", unsafe_allow_html=True)
    for win in quick_wins[3:]:
        st.markdown(f"""
        <div class="quick-win-item">
            <strong>{win['supplier']}</strong><br>
            <small><i class="bi bi-box"></i> {win['pos']} POs | <i class="bi bi-tag"></i> {win['category']} | <i class="bi bi-percent"></i> {win['similarity']} match</small>
        </div>
        """, unsafe_allow_html=True)

# Supplier Analysis
st.markdown('<h2 class="section-header"><i class="bi bi-people"></i> Current Supplier Analysis</h2>', unsafe_allow_html=True)

# Create supplier distribution chart
supplier_data = {
    'Supplier Type': ['Large Corporations', 'Medium Businesses', 'Small Businesses', 'Micro Enterprises'],
    'PO Count': [650, 416, 158, 50],
    'Percentage': [51.0, 32.7, 12.4, 3.9]
}

fig_suppliers = px.bar(
    x=supplier_data['Supplier Type'],
    y=supplier_data['PO Count'],
    color=supplier_data['Percentage'],
    color_continuous_scale=['#C69214', '#154734'],
    title="Current PO Distribution by Supplier Type"
)

fig_suppliers.update_layout(
    height=400,
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)',
    font=dict(color='white')
)

st.plotly_chart(fig_suppliers, use_container_width=True)

# Key Insights
st.markdown('<h2 class="section-header"><i class="bi bi-lightbulb"></i> Key Insights</h2>', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="insight-box">
        <h4><i class="bi bi-bullseye"></i> Focus Area</h4>
        <p>Target the <strong>416 POs</strong> currently with medium businesses - these have the highest transition potential to small businesses.</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="insight-box">
        <h4><i class="bi bi-clock"></i> Timeline</h4>
        <p>Achieving 25% target requires transitioning <strong>110 POs</strong> over 6 months - approximately 18 POs per month.</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="insight-box">
        <h4><i class="bi bi-award"></i> Impact</h4>
        <p>Reaching 25% will increase small business POs by <strong>52.9%</strong> (from 208 to 318 POs).</p>
    </div>
    """, unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: white; padding: 1rem;">
    <p><i class="bi bi-mortarboard"></i> <strong>Cal Poly SLO AI Summer Camp Project</strong></p>
    <p><i class="bi bi-target"></i> Small Business Procurement Target Analysis | <i class="bi bi-graph-up"></i> 16.3% → 25% Goal</p>
</div>
""", unsafe_allow_html=True)
