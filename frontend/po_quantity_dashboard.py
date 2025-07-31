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
        background: transparent !important;
        border-radius: 12px;
        padding: 2rem;
        margin-bottom: 2rem;
        box-shadow: none !important;
    }
    
    .metric-card {
        background: linear-gradient(135deg, var(--mustard-gold) 0%, var(--mustard-gold-dark) 100%);
        border-radius: 8px;
        padding: 1.5rem;
        text-align: center;
        color: var(--white);
        font-weight: bold;
        margin-bottom: 1rem;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
    }
    
    .metric-card.current {
        background: linear-gradient(135deg, #DC143C 0%, #B22222 100%);
        color: var(--white);
    }
    
    .metric-card.target {
        background: linear-gradient(135deg, var(--poly-green) 0%, var(--poly-green-dark) 100%);
        color: var(--white);
    }
    
    .metric-card.gap {
        background: linear-gradient(135deg, var(--mustard-gold-light) 0%, var(--mustard-gold) 100%);
        color: var(--poly-green-dark);
        font-weight: 800;
    }
    
    .metric-value {
        font-size: 2.5rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
    }
    
    .metric-label {
        font-size: 1rem;
        opacity: 0.9;
    }
    
    .phase-card {
        background: rgba(255, 255, 255, 0.1);
        border-left: 4px solid var(--mustard-gold);
        padding: 1rem;
        margin: 0.5rem 0;
        border-radius: 0 8px 8px 0;
        backdrop-filter: blur(10px);
        color: var(--white);
    }
    
    .phase-card.achieved {
        background: rgba(196, 146, 20, 0.2);
        border-left-color: var(--mustard-gold-light);
    }
    
    h1, h2, h3 {
        color: var(--white) !important;
    }
    
    .big-number {
        font-size: 4rem;
        font-weight: 800;
        text-align: center;
        margin: 1rem 0;
    }
    
    .current-number { color: #DC143C; }
    .target-number { color: var(--mustard-gold-light); }
    .gap-number { color: var(--mustard-gold); }
    
    .po-stat {
        background: rgba(255, 255, 255, 0.1);
        padding: 1rem;
        border-radius: 8px;
        text-align: center;
        margin: 0.5rem 0;
        color: var(--mustard-gold-light);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(196, 146, 20, 0.3);
    }
    
    .po-stat strong {
        color: var(--white) !important;
        font-weight: 800;
    }
    
    .icon-header {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        margin-bottom: 1rem;
    }
    
    .icon-header i {
        font-size: 1.5rem;
        color: var(--mustard-gold-light);
    }
    
    .section-icon {
        font-size: 1.2rem;
        margin-right: 0.5rem;
        color: var(--mustard-gold);
    }
    
    /* Make text white throughout */
    p, div, span {
        color: var(--white) !important;
    }
    
    /* Specific text color overrides */
    .phase-card p {
        color: var(--mustard-gold-light) !important;
    }
    
    .phase-card strong {
        color: var(--white) !important;
    }
    
    .phase-card h4 {
        color: var(--white) !important;
        margin-bottom: 0.5rem;
    }
    
    /* Table and data styling */
    .stDataFrame {
        background: rgba(255, 255, 255, 0.1) !important;
        border-radius: 8px !important;
        backdrop-filter: blur(10px) !important;
        border: 1px solid rgba(196, 146, 20, 0.3) !important;
    }
    
    .stDataFrame td, .stDataFrame th {
        color: var(--white) !important;
        border-color: rgba(196, 146, 20, 0.2) !important;
    }
    
    .stDataFrame th {
        background-color: rgba(196, 146, 20, 0.2) !important;
        color: var(--white) !important;
        font-weight: bold;
    }
    
    /* Style plotly charts background */
    .js-plotly-plot {
        background: transparent !important;
    }
    
    /* Cal Poly accent colors for success/warning states */
    .success-text { color: var(--mustard-gold-light) !important; }
    .warning-text { color: #DC143C !important; }
    .info-text { color: var(--mustard-gold) !important; }
    
    /* Number emphasis */
    .highlight-number {
        color: var(--mustard-gold-light) !important;
        font-weight: 800 !important;
        font-size: 1.1em;
    }
    
    .emphasis-text {
        color: var(--mustard-gold) !important;
        font-weight: 600;
    }
    
    /* Subtitle and description text */
    .subtitle-text {
        color: rgba(255, 255, 255, 0.8) !important;
        font-size: 0.9em;
    }
    
    /* Footer styling */
    .footer-text {
        color: var(--mustard-gold-light) !important;
    }
    
    .footer-subtitle {
        color: rgba(255, 255, 255, 0.7) !important;
    }
</style>
""", unsafe_allow_html=True)

# Initialize analytics
@st.cache_data
def load_po_analytics():
    analytics = POQuantityAnalytics()
    return {
        'current_stats': analytics.calculate_current_po_percentage(),
        'optimization_plan': analytics.generate_po_optimization_plan(),
        'supplier_analysis': analytics.get_supplier_transition_analysis(),
        'category_impact': analytics.get_category_po_impact(),
        'quick_wins': analytics.get_quick_wins_by_po_impact(20)
    }

# Load all data
try:
    data = load_po_analytics()
    data_loaded = True
except Exception as e:
    st.error(f"Error loading data: {str(e)}")
    data_loaded = False
    data = {}

# Header
st.markdown("""
<div class="dashboard-card">
    <h1 style="margin: 0; text-align: center; color: var(--poly-green) !important;">Small Business PO Percentage Target</h1>
    <p class="subtitle-text" style="text-align: center; margin-top: 0.5rem; font-size: 1.2rem;">
        Current % of Purchase Orders vs. <span class="highlight-number">25% Target</span>
    </p>
</div>
""", unsafe_allow_html=True)

if data_loaded and 'error' not in data['current_stats']:
    current_stats = data['current_stats']
    
    # Big Numbers Section - PO Quantities
    st.markdown('<div class="dashboard-card">', unsafe_allow_html=True)
    st.markdown('<h2 style="margin: 0;">Purchase Order Percentage Analysis</h2>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
        <div class="big-number current-number">{current_stats['current_percentage']:.1f}%</div>
        <h3 style="text-align: center; color: #DC143C;">Current PO %</h3>
        <div class="po-stat">
            <span class="highlight-number">{current_stats['current_small_business_pos']:,}</span> small business POs<br>
            out of <span class="highlight-number">{current_stats['total_pos']:,}</span> total POs
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="big-number target-number">{current_stats['target_percentage']:.1f}%</div>
        <h3 style="text-align: center; color: var(--mustard-gold-light);">Target PO %</h3>
        <div class="po-stat">
            Need <span class="highlight-number">{current_stats['target_pos_needed']:,}</span> small business POs<br>
            out of <span class="highlight-number">{current_stats['total_pos']:,}</span> total POs
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="big-number gap-number">{current_stats['gap_pos_needed']:,}</div>
        <h3 style="text-align: center; color: var(--mustard-gold);">POs to Transition</h3>
        <div class="po-stat">
            Need to transition <span class="highlight-number">{current_stats['gap_pos_needed']:,}</span> more POs<br>
            from current suppliers to small businesses
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # PO Distribution Visualization
    st.markdown('<div class="dashboard-card">', unsafe_allow_html=True)
    st.markdown('<h2 style="margin: 0;">Current PO Distribution</h2>', unsafe_allow_html=True)
    
    # Current PO distribution pie chart (full width)
    current_data = {
        'Type': ['Small Business POs', 'Other POs'],
        'Count': [current_stats['current_small_business_pos'], 
                 current_stats['current_non_small_business_pos']],
        'Percentage': [current_stats['current_percentage'], 
                      100 - current_stats['current_percentage']]
    }
    
    fig_current = px.pie(
        values=current_data['Count'],
        names=current_data['Type'],
        title=f"Current PO Distribution ({current_stats['current_percentage']:.1f}% Small Business)",
        color_discrete_map={
            'Small Business POs': '#C69214',  # Mustard Gold
            'Other POs': '#CCCCCC'  # Light Gray
        }
    )
    fig_current.update_layout(
        font=dict(color='white'),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        title_font_color='white'
    )
    st.plotly_chart(fig_current, use_container_width=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Optimization Scenarios
    if 'error' not in data['optimization_plan']:
        opt_plan = data['optimization_plan']
        
        st.markdown('<div class="dashboard-card">', unsafe_allow_html=True)
        st.markdown('<h2 style="margin: 0;">PO Transition Scenarios to Reach 25%</h2>', unsafe_allow_html=True)
        
        scenarios = opt_plan['scenarios']
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            high_conf = scenarios['high_confidence']
            st.markdown(f"""
            <div class="phase-card {'achieved' if high_conf['target_achieved'] else ''}">
                <h4><i class="bi bi-bullseye section-icon"></i>High Confidence (≥0.4 similarity)</h4>
                <p><strong>POs to transition:</strong> <span class="highlight-number">{high_conf['pos_to_transition']:,}</span></p>
                <p><strong>Resulting %:</strong> <span class="highlight-number">{high_conf['resulting_percentage']:.1f}%</span></p>
                <p><strong>Total small business POs:</strong> <span class="highlight-number">{high_conf['resulting_small_business_pos']:,}</span></p>
                {'<p class="success-text"><strong><i class="bi bi-check-circle"></i> TARGET ACHIEVED!</strong></p>' if high_conf['target_achieved'] else '<p class="warning-text"><strong><i class="bi bi-x-circle"></i> Target not reached</strong></p>'}
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            med_conf = scenarios['medium_confidence']
            st.markdown(f"""
            <div class="phase-card achieved">
                <h4><i class="bi bi-graph-up section-icon"></i>Medium Confidence (≥0.2 similarity)</h4>
                <p><strong>POs to transition:</strong> <span class="highlight-number">{med_conf['pos_to_transition']:,}</span></p>
                <p><strong>Resulting %:</strong> <span class="highlight-number">{med_conf['resulting_percentage']:.1f}%</span></p>
                <p><strong>Total small business POs:</strong> <span class="highlight-number">{med_conf['resulting_small_business_pos']:,}</span></p>
                <p class="success-text"><strong><i class="bi bi-check-circle"></i> TARGET EXCEEDED!</strong></p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            all_matches = scenarios['all_matches']
            st.markdown(f"""
            <div class="phase-card achieved">
                <h4><i class="bi bi-arrow-repeat section-icon"></i>All Available Matches</h4>
                <p><strong>POs to transition:</strong> <span class="highlight-number">{all_matches['pos_to_transition']:,}</span></p>
                <p><strong>Resulting %:</strong> <span class="highlight-number">{all_matches['resulting_percentage']:.1f}%</span></p>
                <p><strong>Total small business POs:</strong> <span class="highlight-number">{all_matches['resulting_small_business_pos']:,}</span></p>
                <p class="success-text"><strong><i class="bi bi-check-circle"></i> MAXIMUM POTENTIAL!</strong></p>
            </div>
            """, unsafe_allow_html=True)
        
        # Optimal Path
        st.markdown('<h3 style="margin: 0;">Optimal Path to Exactly 25%</h3>', unsafe_allow_html=True)
        optimal = opt_plan['optimal_path']
        
        if optimal.get('target_achieved', False):
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown(f"""
                <div class="metric-card target">
                    <div class="metric-value">{optimal['pos_to_transition']:,}</div>
                    <div class="metric-label">POs Need to Transition</div>
                </div>
                """, unsafe_allow_html=True)
                
                st.markdown(f"""
                <div class="metric-card gap">
                    <div class="metric-value">{optimal.get('avg_similarity_score', 0):.3f}</div>
                    <div class="metric-label">Average Similarity Score</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown("**What this means:**")
                st.markdown(f"- Transition **<span class='highlight-number'>{optimal['pos_to_transition']:,} purchase orders</span>** from current suppliers to small businesses", unsafe_allow_html=True)
                st.markdown(f"- This will achieve exactly **<span class='highlight-number'>{optimal['resulting_percentage']:.1f}%</span>** small business POs", unsafe_allow_html=True)
                st.markdown(f"- Average match quality: **<span class='highlight-number'>{optimal.get('avg_similarity_score', 0):.1%}</span>** similarity", unsafe_allow_html=True)
                st.markdown("- <span class='emphasis-text'>Focus on highest similarity matches first</span> for best results", unsafe_allow_html=True)
        else:
            st.warning(f"⚠️ {optimal.get('message', 'Cannot reach 25% with available matches')}")
            if 'shortfall' in optimal:
                st.markdown(f"**Shortfall:** Need {optimal['shortfall']:,} more potential matches to reach 25%")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Implementation Phases
    if opt_plan.get('implementation_phases'):
        st.markdown('<div class="dashboard-card">', unsafe_allow_html=True)
        st.markdown('<h2 style="margin: 0;">Phased Implementation Plan</h2>', unsafe_allow_html=True)
        
        phases_df = pd.DataFrame(opt_plan['implementation_phases'])
        
        # Create phase visualization
        fig_phases = go.Figure()
        
        # Cal Poly color palette
        cal_poly_colors = ['#DC143C', '#C69214', '#D4A017', '#154734', '#1a5a3e']
        
        for i, phase in enumerate(phases_df.itertuples()):
            fig_phases.add_trace(go.Bar(
                name=phase.phase,
                x=[phase.phase],
                y=[phase.resulting_percentage],
                marker_color=cal_poly_colors[i % len(cal_poly_colors)],
                text=f"{phase.resulting_percentage:.1f}%<br>({phase.cumulative_pos} POs)",
                textposition='inside'
            ))
        
        fig_phases.add_hline(y=25, line_dash="dash", line_color="#C69214", 
                            annotation_text="25% Target")
        
        fig_phases.update_layout(
            title="Cumulative PO Percentage by Implementation Phase",
            yaxis_title="Small Business PO Percentage (%)",
            font=dict(color='white'),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            showlegend=False,
            title_font_color='white'
        )
        
        st.plotly_chart(fig_phases, use_container_width=True)
        
        # Phase details table
        st.markdown("### Phase Implementation Details")
        display_phases = phases_df.copy()
        display_phases['resulting_percentage'] = display_phases['resulting_percentage'].apply(lambda x: f"{x:.1f}%")
        
        st.dataframe(
            display_phases[['phase', 'similarity_threshold', 'pos_in_phase', 
                          'cumulative_pos', 'resulting_percentage', 'target_achieved']].rename(columns={
                'phase': 'Phase',
                'similarity_threshold': 'Similarity Threshold',
                'pos_in_phase': 'POs in Phase',
                'cumulative_pos': 'Cumulative POs',
                'resulting_percentage': 'Resulting %',
                'target_achieved': 'Target Achieved'
            }),
            use_container_width=True,
            hide_index=True
        )
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Quick Wins - PO Focused
    if data['quick_wins']:
        st.markdown('<div class="dashboard-card">', unsafe_allow_html=True)
        st.markdown('<h2 style="margin: 0;">Top PO Transition Opportunities</h2>', unsafe_allow_html=True)
        
        quick_wins_df = pd.DataFrame(data['quick_wins'])
        quick_wins_df['Purchase_Amount'] = quick_wins_df['Purchase_Amount'].apply(lambda x: f"${x:,.2f}")
        quick_wins_df['Similarity_Score'] = quick_wins_df['Similarity_Score'].apply(lambda x: f"{x:.3f}")
        quick_wins_df['PO_Impact_Score'] = quick_wins_df['PO_Impact_Score'].apply(lambda x: f"{x:.3f}")
        
        st.markdown("**Each row represents one PO that could be transitioned to a small business**")
        
        st.dataframe(
            quick_wins_df.rename(columns={
                'Current_Supplier': 'Current Supplier',
                'Small_Business': 'Recommended Small Business',
                'Purchase_Amount': 'PO Amount',
                'Similarity_Score': 'Similarity Score',
                'Business_Category': 'Category',
                'Supplier_PO_Count': 'Supplier Total POs',
                'PO_Impact_Score': 'Impact Score'
            }),
            use_container_width=True,
            hide_index=True,
            column_config={
                "Similarity Score": st.column_config.ProgressColumn(
                    "Similarity Score",
                    help="How similar the services are (0-1)",
                    min_value=0,
                    max_value=1,
                ),
                "Impact Score": st.column_config.ProgressColumn(
                    "Impact Score",
                    help="Combined similarity and strategic impact score",
                    min_value=0,
                    max_value=1,
                ),
            }
        )
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Supplier Transition Analysis
    if 'error' not in data['supplier_analysis']:
        st.markdown('<div class="dashboard-card">', unsafe_allow_html=True)
        st.markdown('<h2 style="margin: 0;">Current Suppliers with Most PO Transition Opportunities</h2>', unsafe_allow_html=True)
        
        supplier_data = data['supplier_analysis']['top_suppliers_by_po_count']
        
        if supplier_data:
            suppliers_df = pd.DataFrame(supplier_data)
            suppliers_df['Total_Amount'] = suppliers_df['Total_Amount'].apply(lambda x: f"${x:,.0f}")
            
            st.markdown("**These suppliers have the most POs that could potentially be transitioned:**")
            
            st.dataframe(
                suppliers_df.rename(columns={
                    'Current_Supplier': 'Current Supplier',
                    'PO_Count': 'Number of POs',
                    'Total_Amount': 'Total Amount',
                    'Avg_Similarity': 'Avg Similarity Score',
                    'Small_Business_Options': 'Small Business Options'
                }),
                use_container_width=True,
                hide_index=True
            )
        
        st.markdown('</div>', unsafe_allow_html=True)

else:
    st.markdown('<div class="dashboard-card">', unsafe_allow_html=True)
    st.markdown('<h2 style="margin: 0;">Data Not Available</h2>', unsafe_allow_html=True)
    st.markdown("""
    Unable to load PO quantity analysis data. Please ensure:
    
    1. Backend analysis has been completed
    2. CSV files are available in the backend directory
    3. Test results contain purchase order information
    """)
    st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("""
<div class="dashboard-card" style="text-align: center; margin-top: 3rem;">
    <p class="footer-text" style="margin: 0;">
        <i class="bi bi-mortarboard"></i> Cal Poly SLO AI Summer Camp - Small Business PO Percentage Analysis
    </p>
    <p class="footer-subtitle" style="margin: 0; font-size: 0.9rem;">
        Focus: <span class="emphasis-text">Percentage of Purchase Orders</span> (not dollar amounts) going to small businesses
    </p>
</div>
""", unsafe_allow_html=True)
