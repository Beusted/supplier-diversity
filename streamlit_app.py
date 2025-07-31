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
    page_icon="📊",
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
        background: linear-gradient(135deg, #154734 0%, #1a5a3e 100%);
        font-family: 'Inter', sans-serif;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Top Navigation Bar */
    .top-nav {
        background: rgba(21, 71, 52, 0.95);
        backdrop-filter: blur(10px);
        border-bottom: 2px solid #ffc72c;
        padding: 1rem 2rem;
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        z-index: 1000;
        display: flex;
        justify-content: space-between;
        align-items: center;
        box-shadow: 0 4px 20px rgba(0,0,0,0.1);
    }
    
    .nav-logo {
        color: #ffc72c;
        font-size: 24px;
        font-weight: 700;
        text-decoration: none;
    }
    
    .nav-buttons {
        display: flex;
        gap: 1rem;
        align-items: center;
    }
    
    .nav-btn {
        background: #ffc72c;
        color: #000000;
        border: none;
        padding: 0.5rem 1rem;
        border-radius: 6px;
        font-weight: 500;
        cursor: pointer;
        transition: all 0.3s ease;
        text-decoration: none;
        display: inline-block;
    }
    
    .nav-btn:hover {
        background: #e0b000;
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(255, 199, 44, 0.3);
        text-decoration: none;
    }
    
    /* Main content area */
    .main-content {
        margin-top: 100px;
        padding: 2rem;
        min-height: calc(100vh - 100px);
    }
    
    /* Dashboard title */
    .dashboard-title {
        text-align: center;
        color: #ffc72c;
        font-size: 48px;
        font-weight: 700;
        margin-bottom: 2rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    /* Card styling */
    .dashboard-card {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 199, 44, 0.2);
        border-radius: 12px;
        padding: 2rem;
        margin: 1rem 0;
        box-shadow: 0 8px 32px rgba(0,0,0,0.1);
    }
    
    .card-title {
        color: #ffc72c;
        font-size: 24px;
        font-weight: 600;
        margin-bottom: 1rem;
    }
    
    /* Upload section */
    .upload-section {
        text-align: center;
        padding: 3rem;
        border: 2px dashed #ffc72c;
        border-radius: 12px;
        background: rgba(255, 199, 44, 0.05);
        margin: 2rem 0;
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
        background: rgba(255, 255, 255, 0.1) !important;
        border: 2px dashed #ffc72c !important;
        border-radius: 12px !important;
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
        background: rgba(255, 255, 255, 0.05);
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        border: 1px solid rgba(255, 199, 44, 0.2);
    }
    
    /* Text styling */
    .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {
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
if 'charts_generated' not in st.session_state:
    st.session_state.charts_generated = False
if 'optimized_data' not in st.session_state:
    st.session_state.optimized_data = None

# Top Navigation Bar
st.markdown("""
<div class="top-nav">
    <div class="nav-logo"><i class="bi bi-building"></i> Diversity in Procurement</div>
    <div class="nav-buttons">
        <a href="#home" class="nav-btn"><i class="bi bi-house"></i> Home</a>
        <a href="#dashboard" class="nav-btn"><i class="bi bi-graph-up"></i> Dashboard</a>
        <a href="#reports" class="nav-btn"><i class="bi bi-file-earmark-text"></i> Reports</a>
    </div>
</div>
""", unsafe_allow_html=True)

# Main content area
st.markdown('<div class="main-content">', unsafe_allow_html=True)

# Dashboard title
st.markdown('<h1 class="dashboard-title">Diversity in Procurement Dashboard</h1>', unsafe_allow_html=True)

# Upload Section
st.markdown('<div class="dashboard-card">', unsafe_allow_html=True)
st.markdown('<h2 class="card-title"><i class="bi bi-folder"></i> Data Upload</h2>', unsafe_allow_html=True)

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.markdown('<div class="upload-section">', unsafe_allow_html=True)
    st.markdown("### Upload Procurement Data")
    st.markdown("Upload your Excel spreadsheet containing procurement data to get started.")
    
    uploaded_file = st.file_uploader(
        "Choose an Excel file",
        type=['xlsx', 'xls'],
        help="Upload your procurement data in Excel format"
    )
    
    if uploaded_file is not None:
        try:
            # Read the uploaded file
            df = pd.read_excel(uploaded_file)
            st.session_state.uploaded_data = df
            st.success(f"<i class='bi bi-check-circle'></i> Successfully uploaded file with {len(df)} rows and {len(df.columns)} columns!", unsafe_allow_html=True)
            
            # Show preview of data
            with st.expander("<i class='bi bi-table'></i> Preview Data"):
                st.dataframe(df.head(10), use_container_width=True)
                
        except Exception as e:
            st.error(f"<i class='bi bi-x-circle'></i> Error reading file: {str(e)}", unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# Action Buttons Section
if st.session_state.uploaded_data is not None:
    st.markdown('<div class="dashboard-card">', unsafe_allow_html=True)
    st.markdown('<h2 class="card-title"><i class="bi bi-rocket"></i> Actions</h2>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("<i class='bi bi-graph-up'></i> Generate Report", use_container_width=True, help="Generate comprehensive diversity report"):
            with st.spinner("Generating report..."):
                # Simulate report generation
                import time
                time.sleep(2)
                st.session_state.report_generated = True
                st.success("<i class='bi bi-check-circle'></i> Report generated successfully!", unsafe_allow_html=True)
    
    with col2:
        if st.button("<i class='bi bi-bar-chart'></i> Generate Charts", use_container_width=True, help="Create data visualizations"):
            with st.spinner("Creating visualizations..."):
                # Simulate chart generation
                import time
                time.sleep(1.5)
                st.session_state.charts_generated = True
                st.success("<i class='bi bi-check-circle'></i> Charts generated successfully!", unsafe_allow_html=True)
    
    with col3:
        if st.button("<i class='bi bi-arrow-clockwise'></i> Optimize Data", use_container_width=True, help="Optimize and clean data"):
            with st.spinner("Optimizing data..."):
                # Simulate data optimization
                import time
                time.sleep(2)
                # Create mock optimized data
                st.session_state.optimized_data = st.session_state.uploaded_data.copy()
                st.success("<i class='bi bi-check-circle'></i> Data optimized successfully!", unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# Report Section
if st.session_state.report_generated:
    st.markdown('<div class="dashboard-card">', unsafe_allow_html=True)
    st.markdown('<h2 class="card-title"><i class="bi bi-file-earmark-text"></i> Generated Report</h2>', unsafe_allow_html=True)
    
    # Mock report content
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown('<div class="metric-container">', unsafe_allow_html=True)
        st.metric("Total Suppliers", "1,247", "12%")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="metric-container">', unsafe_allow_html=True)
        st.metric("Diverse Suppliers", "312", "8%")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col3:
        st.markdown('<div class="metric-container">', unsafe_allow_html=True)
        st.metric("Diversity %", "25.1%", "2.3%")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col4:
        st.markdown('<div class="metric-container">', unsafe_allow_html=True)
        st.metric("Total Spend", "$2.4M", "15%")
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("### <i class='bi bi-graph-up'></i> Key Insights")
    st.markdown("""
    - **Supplier Diversity**: Current diversity rate is 25.1%, showing improvement from last quarter
    - **Spending Analysis**: Diverse suppliers account for 18% of total procurement spend
    - **Growth Opportunities**: Identified 45 potential diverse suppliers for future partnerships
    - **Compliance Status**: Meeting federal diversity requirements with room for improvement
    """)
    
    st.markdown('</div>', unsafe_allow_html=True)

# Charts Section
if st.session_state.charts_generated:
    st.markdown('<div class="dashboard-card">', unsafe_allow_html=True)
    st.markdown('<h2 class="card-title"><i class="bi bi-bar-chart"></i> Data Visualizations</h2>', unsafe_allow_html=True)
    
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
    st.markdown('<h2 class="card-title"><i class="bi bi-search"></i> Data Overview</h2>', unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["<i class='bi bi-graph-up'></i> Original Data", "<i class='bi bi-arrow-clockwise'></i> Optimized Data"])
    
    with tab1:
        st.dataframe(st.session_state.uploaded_data, use_container_width=True)
    
    with tab2:
        if st.session_state.optimized_data is not None:
            st.dataframe(st.session_state.optimized_data, use_container_width=True)
        else:
            st.info("Click 'Optimize Data' to generate optimized dataset")
    
    st.markdown('</div>', unsafe_allow_html=True)

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
