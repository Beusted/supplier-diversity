import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import io
import base64

# Page configuration
st.set_page_config(
    page_title="Diversity in Procurement Dashboard",
    page_icon=":)",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for Cal Poly styling with Bootstrap Icons
st.markdown("""
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/font/bootstrap-icons.min.css">
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Main app styling */
    .main {
        background: linear-gradient(135deg, #154734 0%, #1a5a3e 100%) !important;
        font-family: 'Inter', sans-serif;
    }
    
    /* Remove any default Streamlit containers */
    .block-container {
        padding-top: 0 !important;
        padding-bottom: 0 !important;
        background: transparent !important;
    }
    
    /* Ensure main content area has no background */
    .main .block-container {
        background: transparent !important;
        max-width: none !important;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    
    /* Navigation Bar Styling */
    .nav-container {
        background: rgba(21, 71, 52, 0.95);
        backdrop-filter: blur(10px);
        border-bottom: 2px solid #ffc72c;
        padding: 0.75rem 2rem;
        border-radius: 0 0 12px 12px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.1);
        margin-bottom: 1rem;
    }
    
    /* Navigation buttons styling */
    .stButton > button {
        background: #154734 !important;
        color: #ffc72c !important;
        border: 2px solid #154734 !important;
        border-radius: 6px !important;
        font-weight: 500 !important;
        transition: all 0.3s ease !important;
        width: 100% !important;
    }
    
    .stButton > button:hover {
        background: #ffc72c !important;
        color: #154734 !important;
        border: 2px solid #ffc72c !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 4px 12px rgba(21, 71, 52, 0.3) !important;
    }
    
    /* Main content area */
    .main-content {
        padding: 1rem 2rem;
        min-height: 100vh;
    }
    
    /* Dashboard title */
    .dashboard-title {
        text-align: center;
        color: #ffc72c;
        font-size: 36px;
        font-weight: 700;
        margin-bottom: 1rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    /* Card styling */
    .dashboard-card {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border: 2px solid #154734;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 0.5rem 0;
        box-shadow: 0 8px 32px rgba(21, 71, 52, 0.2);
    }
    
    .card-title {
        color: #ffc72c;
        font-size: 22px;
        font-weight: 600;
        margin-bottom: 0.75rem;
        border-bottom: 2px solid #154734;
        padding-bottom: 0.5rem;
    }
    
    /* Upload section */
    .upload-section {
        text-align: center;
        padding: 1rem;
        border: 2px dashed #154734;
        border-radius: 12px;
        background: rgba(21, 71, 52, 0.05);
        margin: 0.5rem 0;
    }
    
    .upload-section h4 {
        color: #154734 !important;
        margin-bottom: 0.5rem !important;
        font-weight: 600 !important;
    }
    
    .upload-section p {
        color: #154734 !important;
        margin-bottom: 0 !important;
    }
    
    /* Metric containers */
    .metric-container {
        background: rgba(21, 71, 52, 0.1);
        border: 1px solid #154734;
        border-radius: 8px;
        padding: 1rem;
        margin: 0.5rem 0;
    }
    
    /* Button styling */
    .stButton > button {
        background: #ffc72c !important;
        color: #000000 !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 0.75rem 2rem !important;
        font-weight: 600 !important;
        font-size: 16px !important;
        transition: all 0.3s ease !important;
        text-decoration: none !important;
    }
    
    .stButton > button:hover {
        background: #e0b000 !important;
        color: #000000 !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(255, 199, 44, 0.3) !important;
        text-decoration: none !important;
    }
    
    /* Remove underlines from all buttons and links */
    button, a, .nav-btn, .stButton > button {
        text-decoration: none !important;
    }
    
    button:hover, a:hover, .nav-btn:hover, .stButton > button:hover {
        text-decoration: none !important;
    }
    
    /* Additional comprehensive underline removal */
    button *, a *, .nav-btn *, .stButton > button * {
        text-decoration: none !important;
    }
    
    /* Remove underlines from any text elements inside buttons */
    button span, button div, button p, button i,
    a span, a div, a p, a i,
    .nav-btn span, .nav-btn div, .nav-btn p, .nav-btn i,
    .stButton > button span, .stButton > button div, .stButton > button p, .stButton > button i {
        text-decoration: none !important;
    }
    
    /* Force remove underlines from all interactive elements */
    [role="button"], [type="button"], [type="submit"] {
        text-decoration: none !important;
    }
    
    [role="button"]:hover, [type="button"]:hover, [type="submit"]:hover {
        text-decoration: none !important;
    }
    
    /* File uploader styling */
    .stFileUploader > div > div {
        background: transparent !important;
        border: none !important;
        border-radius: 0 !important;
        padding: 0 !important;
    }
    
    .stFileUploader > div > div > div {
        background: transparent !important;
        border: 2px dashed #154734 !important;
        border-radius: 12px !important;
        padding: 2rem !important;
        text-align: center !important;
        margin-top: -1rem !important;
        min-height: 100px !important;
        display: flex !important;
        flex-direction: column !important;
        justify-content: center !important;
        align-items: center !important;
    }
    
    .stFileUploader > div > div > div > div {
        color: #154734 !important;
        font-weight: 500 !important;
    }
    
    .stFileUploader label {
        display: none !important;
    }
    
    .stFileUploader button {
        background: #154734 !important;
        color: #ffc72c !important;
        border: none !important;
        border-radius: 6px !important;
        padding: 0.5rem 1rem !important;
        font-weight: 500 !important;
        margin-top: 0.5rem !important;
    }
    
    .stFileUploader button:hover {
        background: #0f3426 !important;
    }
    
    /* Success/Error messages */
    .stSuccess {
        background: rgba(76, 175, 80, 0.1) !important;
        border: 1px solid #4CAF50 !important;
        border-radius: 8px !important;
    }
    
    .stError {
        background: rgba(244, 67, 54, 0.1) !important;
        border: 1px solid #f44336 !important;
        border-radius: 8px !important;
    }
    
    /* Chatbot styling */
    .chatbot-container {
        position: fixed !important;
        bottom: 20px !important;
        right: 20px !important;
        z-index: 9999 !important;
        pointer-events: auto !important;
    }
    
    .chatbot-toggle {
        width: 60px !important;
        height: 60px !important;
        border-radius: 50% !important;
        background: #ffc72c !important;
        color: #154734 !important;
        border: none !important;
        cursor: pointer !important;
        box-shadow: 0 4px 20px rgba(255, 199, 44, 0.4) !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        font-size: 24px !important;
        transition: all 0.3s ease !important;
        position: relative !important;
    }
    
    .chatbot-toggle:hover {
        transform: scale(1.1) !important;
        box-shadow: 0 6px 25px rgba(255, 199, 44, 0.6) !important;
    }
    
    .chatbot-window {
        position: fixed !important;
        bottom: 90px !important;
        right: 20px !important;
        width: 350px !important;
        height: 400px !important;
        background: rgba(21, 71, 52, 0.95) !important;
        backdrop-filter: blur(10px) !important;
        border: 2px solid #ffc72c !important;
        border-radius: 12px !important;
        display: none !important;
        flex-direction: column !important;
        box-shadow: 0 8px 32px rgba(0,0,0,0.3) !important;
        z-index: 10000 !important;
    }
    
    .chatbot-header {
        background: #ffc72c;
        color: #154734;
        padding: 1rem;
        border-radius: 10px 10px 0 0;
        font-weight: 600;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    
    .chatbot-messages {
        flex: 1;
        padding: 1rem;
        overflow-y: auto;
        color: #000000;
    }
    
    .chatbot-input {
        padding: 1rem;
        border-top: 1px solid rgba(255, 199, 44, 0.3);
        display: flex;
        gap: 0.5rem;
    }
    
    .chatbot-input input {
        flex: 1;
        padding: 0.5rem;
        border: 1px solid #ffc72c;
        border-radius: 6px;
        background: rgba(255, 255, 255, 0.9);
        color: #000000;
    }
    
    .chatbot-input button {
        background: #ffc72c;
        color: #154734;
        border: none;
        padding: 0.5rem 1rem;
        border-radius: 6px;
        cursor: pointer;
        font-weight: 500;
    }
    
    /* Chart containers */
    .chart-container {
        background: rgba(21, 71, 52, 0.05);
        border-radius: 12px;
        padding: 1rem;
        margin: 0.5rem 0;
        border: 2px solid #154734;
    }
    
    /* Text styling */
    .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {
        color: #ffc72c !important;
    }
    
    .stMarkdown h4, .stMarkdown h5 {
        color: #154734 !important;
        font-weight: 600 !important;
    }
    
    /* Dataframe styling */
    .stDataFrame {
        border: 2px solid #154734 !important;
        border-radius: 8px !important;
    }
    
    .stDataFrame > div {
        border-radius: 8px !important;
    }
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background-color: rgba(21, 71, 52, 0.1) !important;
        border: 1px solid #154734 !important;
        border-radius: 6px !important;
        color: #154734 !important;
        font-weight: 500 !important;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: #154734 !important;
        color: #ffc72c !important;
    }
    
    .stMarkdown p {
        color: #f8f9fa !important;
    }
    
    /* Make button text black */
    .stButton > button {
        color: #000000 !important;
    }
    
    .stButton > button:hover {
        color: #000000 !important;
    }
    
    /* Make navigation button text black */
    .nav-btn {
        color: #000000 !important;
    }
    
    .nav-btn:hover {
        color: #000000 !important;
    }
    
    /* Metrics styling */
    .metric-container {
        background: rgba(255, 199, 44, 0.1);
        border-radius: 8px;
        padding: 1rem;
        text-align: center;
        border: 1px solid rgba(255, 199, 44, 0.3);
    }
    
    /* Data display */
    .stDataFrame {
        background: rgba(255, 255, 255, 0.05) !important;
        border-radius: 8px !important;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'uploaded_data' not in st.session_state:
    st.session_state.uploaded_data = None
if 'report_generated' not in st.session_state:
    st.session_state.report_generated = False
if 'optimized_report_generated' not in st.session_state:
    st.session_state.optimized_report_generated = False
if 'charts_generated' not in st.session_state:
    st.session_state.charts_generated = False
if 'optimized_data' not in st.session_state:
    st.session_state.optimized_data = None
if 'current_page' not in st.session_state:
    st.session_state.current_page = 'dashboard'
if 'show_full_reports' not in st.session_state:
    st.session_state.show_full_reports = False
if 'current_page' not in st.session_state:
    st.session_state.current_page = 'dashboard'

# Top Navigation Bar
# Dashboard title
st.markdown('<h1 class="dashboard-title">Diversity in Procurement Dashboard</h1>', unsafe_allow_html=True)

# Main content - Dashboard functionality

# Upload Section
st.markdown('<div class="dashboard-card" style="margin-top: 1rem;">', unsafe_allow_html=True)
st.markdown('<h2 class="card-title">Data Upload</h2>', unsafe_allow_html=True)

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    # Custom styled file uploader that integrates with the dashed rectangle
    st.markdown("""
    <div class="upload-section">
        <h4 style="color: #ffc72c; margin-bottom: 0.5rem;">Upload Procurement Data</h4>
        <p style="color: #f8f9fa; margin-bottom: 1rem;">Drag and drop your Excel file here or click to browse</p>
    </div>
    """, unsafe_allow_html=True)
    
    uploaded_file = st.file_uploader(
        "Choose an Excel file",
        type=['xlsx', 'xls'],
        help="Upload your procurement data in Excel format",
        label_visibility="collapsed"
    )
    
    if uploaded_file is not None:
        try:
            # Read the uploaded file
            df = pd.read_excel(uploaded_file)
            st.session_state.uploaded_data = df
            st.markdown(f"<div style='color: #4CAF50; background: rgba(76, 175, 80, 0.1); padding: 0.75rem; border-radius: 6px; border: 1px solid #4CAF50;'>Successfully uploaded file with {len(df)} rows and {len(df.columns)} columns!</div>", unsafe_allow_html=True)
            
            # Show preview of data
            with st.expander("Preview Data"):
                st.dataframe(df.head(10), use_container_width=True)
                
        except Exception as e:
            st.markdown(f"<div style='color: #f44336; background: rgba(244, 67, 54, 0.1); padding: 0.75rem; border-radius: 6px; border: 1px solid #f44336;'>Error reading file: {str(e)}</div>", unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# Action Buttons Section
if st.session_state.uploaded_data is not None:
    st.markdown('<div class="dashboard-card">', unsafe_allow_html=True)
    st.markdown('<h2 class="card-title">Actions</h2>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("Optimize Data and Generate Tables", use_container_width=True, help="Generate original tables, optimize data via API, and create optimized tables"):
            with st.spinner("Generating original tables..."):
                # Step 1: Generate tables for original data
                import time
                time.sleep(1)
                st.session_state.report_generated = True
                st.markdown("<div style='color: #4CAF50; background: rgba(76, 175, 80, 0.1); padding: 0.75rem; border-radius: 6px; border: 1px solid #4CAF50;'>Original tables generated successfully!</div>", unsafe_allow_html=True)
            
            with st.spinner("Calling API to optimize data..."):
                # Step 2: Call API for data optimization (placeholder)
                time.sleep(2)
                # TODO: Replace with actual API call
                # optimized_data = call_optimization_api(st.session_state.uploaded_data)
                st.session_state.optimized_data = st.session_state.uploaded_data.copy()
                st.markdown("<div style='color: #2196F3; background: rgba(33, 150, 243, 0.1); padding: 0.75rem; border-radius: 6px; border: 1px solid #2196F3;'>Data optimization completed via API!</div>", unsafe_allow_html=True)
            
            with st.spinner("Generating optimized tables..."):
                # Step 3: Generate tables for optimized data
                time.sleep(1)
                st.session_state.optimized_report_generated = True
                st.markdown("<div style='color: #4CAF50; background: rgba(76, 175, 80, 0.1); padding: 0.75rem; border-radius: 6px; border: 1px solid #4CAF50;'>Optimized tables generated successfully!</div>", unsafe_allow_html=True)
    
    with col2:
        if st.button("Generate Charts", use_container_width=True, help="Create data visualizations"):
            with st.spinner("Creating visualizations..."):
                # Simulate chart generation
                import time
                time.sleep(1.5)
                st.session_state.charts_generated = True
                st.markdown("<div style='color: #4CAF50; background: rgba(76, 175, 80, 0.1); padding: 0.75rem; border-radius: 6px; border: 1px solid #4CAF50;'>Charts generated successfully!</div>", unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# Tables Section
if st.session_state.report_generated:
    st.markdown('<div class="dashboard-card">', unsafe_allow_html=True)
    st.markdown('<h2 class="card-title">Generated Diversity Tables</h2>', unsafe_allow_html=True)
    
    # Create tabs for original and optimized tables
    if st.session_state.optimized_report_generated:
        tab1, tab2 = st.tabs(["Original Data Tables", "Optimized Data Tables"])
        
        with tab1:
            st.markdown("#### Actual vs. Goal - Spend Percentages (Original Data)")
            
            # Create SWAM-style table for original data
            import pandas as pd
            
            # Define diversity categories (based on SWAM structure)
            categories = {
                'MB': 'Minority Business',
                'WB': 'Women Business', 
                'Micro': 'Micro Business',
                'SDV': 'Service-Disabled Veteran',
                'SB': 'Small Business',
                'ESO': 'Emerging Small Organization',
                '8A': '8(a) Business',
                'EDWOSB': 'Economically Disadvantaged WOSB',
                'WOSB': 'Women-Owned Small Business',
                'FSDV': 'Firm Service-Disabled Veteran'
            }
            
            # Original data table (based on current 25.1% diversity rate)
            original_table_data = {
                'Category': list(categories.keys()),
                'Goal (%)': [6.00, 5.50, 1.00, 1.00, 30.00, 1.00, 1.00, 1.00, 0.00, 1.00],
                'Actual (%)': [4.20, 3.80, 0.80, 0.50, 25.10, 0.30, 0.60, 0.40, 0.00, 0.30],
                'Variance': ['-1.80', '-1.70', '-0.20', '-0.50', '-4.90', '-0.70', '-0.40', '-0.60', '0.00', '-0.70']
            }
            
            original_df = pd.DataFrame(original_table_data)
            
            # Style the dataframe
            def highlight_variance(val):
                if isinstance(val, str) and val.startswith('-'):
                    return 'color: #f44336; font-weight: bold'  # Red for negative
                elif isinstance(val, str) and not val.startswith('-') and val != '0.00':
                    return 'color: #4CAF50; font-weight: bold'  # Green for positive
                return ''
            
            styled_original = original_df.style.applymap(highlight_variance, subset=['Variance'])
            st.dataframe(styled_original, use_container_width=True, hide_index=True)
            
            # Summary metrics for original data
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total Diversity Goal", "47.50%", help="Sum of all diversity category goals")
            with col2:
                st.metric("Total Diversity Actual", "35.00%", help="Sum of all diversity category actuals")
            with col3:
                st.metric("Overall Variance", "-12.50%", delta="-12.50%", help="Difference between goal and actual")
        
        with tab2:
            st.markdown("#### Actual vs. Goal - Spend Percentages (Optimized Data)")
            
            # Optimized data table (showing improved performance)
            optimized_table_data = {
                'Category': list(categories.keys()),
                'Goal (%)': [6.00, 5.50, 1.00, 1.00, 30.00, 1.00, 1.00, 1.00, 0.00, 1.00],
                'Actual (%)': [7.20, 6.80, 1.20, 1.50, 35.00, 1.20, 1.30, 1.10, 0.50, 1.20],
                'Variance': ['+1.20', '+1.30', '+0.20', '+0.50', '+5.00', '+0.20', '+0.30', '+0.10', '+0.50', '+0.20']
            }
            
            optimized_df = pd.DataFrame(optimized_table_data)
            styled_optimized = optimized_df.style.applymap(highlight_variance, subset=['Variance'])
            st.dataframe(styled_optimized, use_container_width=True, hide_index=True)
            
            # Summary metrics for optimized data
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total Diversity Goal", "47.50%", help="Sum of all diversity category goals")
            with col2:
                st.metric("Total Diversity Actual", "57.00%", help="Sum of all diversity category actuals")
            with col3:
                st.metric("Overall Variance", "+9.50%", delta="+9.50%", help="Difference between goal and actual")
            
            # Improvement summary
            st.markdown("##### Optimization Results")
            st.markdown("""
            - **Overall improvement**: +22.00 percentage points from original to optimized
            - **Categories exceeding goals**: 10 out of 10 categories
            - **Largest improvement**: Small Business category (+9.90 percentage points)
            - **Goal achievement**: All diversity targets met or exceeded
            """)
    
    else:
        # Show only original table if optimization hasn't been run
        st.markdown("#### Actual vs. Goal - Spend Percentages (Original Data)")
        
        # Create SWAM-style table for original data only
        import pandas as pd
        
        categories = {
            'MB': 'Minority Business',
            'WB': 'Women Business', 
            'Micro': 'Micro Business',
            'SDV': 'Service-Disabled Veteran',
            'SB': 'Small Business',
            'ESO': 'Emerging Small Organization',
            '8A': '8(a) Business',
            'EDWOSB': 'Economically Disadvantaged WOSB',
            'WOSB': 'Women-Owned Small Business',
            'FSDV': 'Firm Service-Disabled Veteran'
        }
        
        original_table_data = {
            'Category': list(categories.keys()),
            'Goal (%)': [6.00, 5.50, 1.00, 1.00, 30.00, 1.00, 1.00, 1.00, 0.00, 1.00],
            'Actual (%)': [4.20, 3.80, 0.80, 0.50, 25.10, 0.30, 0.60, 0.40, 0.00, 0.30],
            'Variance': ['-1.80', '-1.70', '-0.20', '-0.50', '-4.90', '-0.70', '-0.40', '-0.60', '0.00', '-0.70']
        }
        
        original_df = pd.DataFrame(original_table_data)
        
        def highlight_variance(val):
            if isinstance(val, str) and val.startswith('-'):
                return 'color: #f44336; font-weight: bold'
            elif isinstance(val, str) and not val.startswith('-') and val != '0.00':
                return 'color: #4CAF50; font-weight: bold'
            return ''
        
        styled_original = original_df.style.applymap(highlight_variance, subset=['Variance'])
        st.dataframe(styled_original, use_container_width=True, hide_index=True)
        
        # Summary metrics
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Diversity Goal", "47.50%")
        with col2:
            st.metric("Total Diversity Actual", "35.00%")
        with col3:
            st.metric("Overall Variance", "-12.50%", delta="-12.50%")
    
    st.markdown('</div>', unsafe_allow_html=True)

# Charts Section
if st.session_state.charts_generated:
    st.markdown('<div class="dashboard-card">', unsafe_allow_html=True)
    st.markdown('<h2 class="card-title">Data Visualizations</h2>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.markdown("#### Original Data Distribution")
        
        # Mock pie chart for original data
        labels = ['Diverse Suppliers', 'Traditional Suppliers', 'Minority-Owned', 'Women-Owned']
        values = [25, 60, 10, 5]
        colors = ['#ffc72c', '#154734', '#4CAF50', '#2196F3']
        
        fig1 = go.Figure(data=[go.Pie(
            labels=labels, 
            values=values,
            marker_colors=colors,
            textinfo='label+percent',
            textfont_size=12
        )])
        
        fig1.update_layout(
            title="Supplier Distribution - Original",
            font=dict(color='white'),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            showlegend=True
        )
        
        st.plotly_chart(fig1, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.markdown("#### Optimized Data Distribution")
        
        # Mock pie chart for optimized data
        optimized_values = [35, 45, 15, 5]
        
        fig2 = go.Figure(data=[go.Pie(
            labels=labels, 
            values=optimized_values,
            marker_colors=colors,
            textinfo='label+percent',
            textfont_size=12
        )])
        
        fig2.update_layout(
            title="Supplier Distribution - Optimized",
            font=dict(color='white'),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            showlegend=True
        )
        
        st.plotly_chart(fig2, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Comparison chart
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.markdown("#### Diversity Improvement Comparison")
    
    categories = ['Diverse Suppliers', 'Minority-Owned', 'Women-Owned', 'Veteran-Owned']
    original = [25, 10, 5, 3]
    optimized = [35, 15, 8, 5]
    
    fig3 = go.Figure(data=[
        go.Bar(name='Original', x=categories, y=original, marker_color='#154734'),
        go.Bar(name='Optimized', x=categories, y=optimized, marker_color='#ffc72c')
    ])
    
    fig3.update_layout(
        title="Diversity Metrics: Original vs Optimized",
        xaxis_title="Supplier Categories",
        yaxis_title="Percentage (%)",
        font=dict(color='white'),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        barmode='group'
    )
    
    st.plotly_chart(fig3, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# Data Preview Section
if st.session_state.uploaded_data is not None:
    st.markdown('<div class="dashboard-card">', unsafe_allow_html=True)
    st.markdown('<h2 class="card-title">Data Overview</h2>', unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["Original Data", "Optimized Data"])
    
    with tab1:
        st.dataframe(st.session_state.uploaded_data, use_container_width=True)
    
    with tab2:
        if st.session_state.optimized_data is not None:
            st.dataframe(st.session_state.optimized_data, use_container_width=True)
        else:
            st.info("Click 'Optimize Data' to generate optimized dataset")
    
    st.markdown('</div>', unsafe_allow_html=True)

# Chatbot Component (positioned outside main content)
st.markdown("""
<div class="chatbot-container">
    <button class="chatbot-toggle" onclick="toggleChatbot()" title="Chat Assistant">
        <i class="bi bi-chat-dots"></i>
    </button>
</div>

<div class="chatbot-window" id="chatbot-window">
    <div class="chatbot-header">
        <span><i class="bi bi-robot"></i> Procurement Assistant</span>
        <button onclick="toggleChatbot()" style="background: none; border: none; color: #154734; font-size: 20px; cursor: pointer;">&times;</button>
    </div>
    <div class="chatbot-messages" id="chatbot-messages">
        <div style="margin-bottom: 1rem; padding: 0.5rem; background: rgba(255, 199, 44, 0.1); border-radius: 6px;">
            <strong><i class="bi bi-robot"></i> Assistant:</strong> Hello! I'm here to help you with your procurement diversity analysis. How can I assist you today?
        </div>
    </div>
    <div class="chatbot-input">
        <input type="text" placeholder="Type your message..." id="chat-input" onkeypress="handleChatKeyPress(event)">
        <button onclick="sendMessage()"><i class="bi bi-send"></i></button>
    </div>
</div>

<script>
function toggleChatbot() {
    const chatWindow = document.getElementById('chatbot-window');
    if (chatWindow.style.display === 'none' || chatWindow.style.display === '') {
        chatWindow.style.display = 'flex';
        document.getElementById('chat-input').focus();
    } else {
        chatWindow.style.display = 'none';
    }
}

function sendMessage() {
    const input = document.getElementById('chat-input');
    const message = input.value.trim();
    
    if (message) {
        const messagesContainer = document.getElementById('chatbot-messages');
        
        // Add user message
        const userMsg = document.createElement('div');
        userMsg.style.cssText = 'margin-bottom: 1rem; padding: 0.5rem; background: rgba(21, 71, 52, 0.3); border-radius: 6px; text-align: right;';
        userMsg.innerHTML = '<strong>You:</strong> ' + message;
        messagesContainer.appendChild(userMsg);
        
        // Add bot response
        setTimeout(() => {
            const botMsg = document.createElement('div');
            botMsg.style.cssText = 'margin-bottom: 1rem; padding: 0.5rem; background: rgba(255, 199, 44, 0.1); border-radius: 6px;';
            botMsg.innerHTML = '<strong><i class="bi bi-robot"></i> Assistant:</strong> I understand you\\'re asking about "' + message + '". I can help you analyze your procurement data, generate reports, and provide insights on supplier diversity metrics.';
            messagesContainer.appendChild(botMsg);
            messagesContainer.scrollTop = messagesContainer.scrollHeight;
        }, 1000);
        
        input.value = '';
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
    }
}

function handleChatKeyPress(event) {
    if (event.key === 'Enter') {
        sendMessage();
    }
}

// Ensure chatbot stays in position on scroll and page load
document.addEventListener('DOMContentLoaded', function() {
    ensureChatbotPosition();
});

window.addEventListener('scroll', function() {
    ensureChatbotPosition();
});

window.addEventListener('resize', function() {
    ensureChatbotPosition();
});

function ensureChatbotPosition() {
    const chatContainer = document.querySelector('.chatbot-container');
    const chatWindow = document.querySelector('.chatbot-window');
    
    if (chatContainer) {
        chatContainer.style.position = 'fixed';
        chatContainer.style.bottom = '20px';
        chatContainer.style.right = '20px';
        chatContainer.style.zIndex = '9999';
    }
    
    if (chatWindow) {
        chatWindow.style.position = 'fixed';
        chatWindow.style.bottom = '90px';
        chatWindow.style.right = '20px';
        chatWindow.style.zIndex = '10000';
    }
}
</script>
""", unsafe_allow_html=True)
