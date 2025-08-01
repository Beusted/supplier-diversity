import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import sys
from pathlib import Path

# Add the current directory to Python path for imports
sys.path.append(str(Path(__file__).parent))
sys.path.append(str(Path(__file__).parent.parent))  # Add parent directory for backend imports

from analytics import POQuantityAnalytics

# Import chatbot backend modules
try:
    from backend.chatbot.chatbot_engine import SupplierDiversityChatbot
    from backend.chatbot.data_analyzer import ProcurementDataAnalyzer
    from backend.chatbot.response_generator import ResponseGenerator
    CHATBOT_AVAILABLE = True
except ImportError as e:
    # Try alternative import path
    try:
        import sys
        import os
        backend_path = os.path.join(os.path.dirname(__file__), '..', 'backend')
        sys.path.insert(0, backend_path)
        from chatbot.chatbot_engine import SupplierDiversityChatbot
        from chatbot.data_analyzer import ProcurementDataAnalyzer
        from chatbot.response_generator import ResponseGenerator
        CHATBOT_AVAILABLE = True
    except ImportError as e2:
        st.warning(f"⚠️ Advanced chatbot features unavailable. Install AI libraries for full functionality. Error: {e2}")
        CHATBOT_AVAILABLE = False

# Page configuration
st.set_page_config(
    page_title="Small Business PO Percentage Target Dashboard",
    page_icon="📋",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Initialize session state for page navigation and settings
if 'current_page' not in st.session_state:
    st.session_state.current_page = 'dashboard'
if 'dark_mode' not in st.session_state:
    st.session_state.dark_mode = True  # Default to dark mode
if 'notifications' not in st.session_state:
    st.session_state.notifications = True
if 'show_settings' not in st.session_state:
    st.session_state.show_settings = False
if 'show_chatbot' not in st.session_state:
    st.session_state.show_chatbot = False
if 'chat_messages' not in st.session_state:
    st.session_state.chat_messages = []

# Initialize chatbot components
if 'chatbot_engine' not in st.session_state and CHATBOT_AVAILABLE:
    st.session_state.chatbot_engine = SupplierDiversityChatbot()
if 'data_analyzer' not in st.session_state and CHATBOT_AVAILABLE:
    st.session_state.data_analyzer = ProcurementDataAnalyzer()
if 'response_generator' not in st.session_state and CHATBOT_AVAILABLE:
    st.session_state.response_generator = ResponseGenerator()

# Custom CSS with Bootstrap Icons and Cal Poly Colors
def get_theme_colors():
    if st.session_state.dark_mode:
        return {
            'bg_primary': 'linear-gradient(135deg, var(--poly-green) 0%, var(--poly-green-light) 100%)',
            'bg_card': 'transparent',
            'text_primary': '#FFFFFF',
            'text_secondary': 'rgba(255, 255, 255, 0.8)',
            'text_body': '#FFFFFF',
            'nav_bg': 'rgba(255, 255, 255, 0.1)',
            'modal_bg': 'rgba(21, 71, 52, 0.95)',
            'body_bg': '#154734'
        }
    else:
        return {
            'bg_primary': 'linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%)',
            'bg_card': 'rgba(255, 255, 255, 0.9)',
            'text_primary': '#333333',
            'text_secondary': 'rgba(51, 51, 51, 0.8)',
            'text_body': '#333333',
            'nav_bg': 'rgba(255, 255, 255, 0.9)',
            'modal_bg': 'rgba(248, 249, 250, 0.95)',
            'body_bg': '#f8f9fa'
        }

theme = get_theme_colors()

# CSS with properly escaped braces
st.markdown("""
<style>
    :root {
        --poly-green: #154734;
        --poly-green-dark: #0f3325;
        --poly-green-light: #1a5a3f;
        --mustard-gold: #ffc72c;
        --mustard-gold-light: #ffd54f;
        --white: #ffffff;
        --dark-gray: #333333;
    }
    
    .main {
        background: """ + theme['bg_primary'] + """ !important;
        font-family: 'Inter', sans-serif;
    }
    
    /* Force background color change on the entire page */
    .stApp {
        background: """ + theme['body_bg'] + """ !important;
    }
    
    /* Also target the main content area */
    .main .block-container {
        background: """ + theme['bg_primary'] + """ !important;
    }
    
    /* Ensure sidebar also changes if visible */
    .css-1d391kg {
        background: """ + theme['body_bg'] + """ !important;
    }
    
    /* Topbar styling */
    .topbar {
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        z-index: 999999;
        background: """ + theme['nav_bg'] + """;
        backdrop-filter: blur(15px);
        border-bottom: 3px solid var(--mustard-gold);
        height: 70px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 0 2rem;
        box-shadow: 0 4px 20px rgba(0,0,0,0.15);
    }
    
    .topbar-title {
        font-size: 1.8rem;
        font-weight: 700;
        color: var(--mustard-gold);
        display: flex;
        align-items: center;
        gap: 0.5rem;
        text-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    .topbar-buttons {
        display: flex;
        gap: 1rem;
        align-items: center;
    }
    
    .topbar-btn {
        background: var(--mustard-gold);
        color: var(--poly-green-dark);
        border: 2px solid var(--mustard-gold);
        padding: 0.6rem 1.2rem;
        border-radius: 8px;
        font-weight: 700;
        font-size: 0.9rem;
        cursor: pointer;
        transition: all 0.3s ease;
        box-shadow: 0 3px 8px rgba(0,0,0,0.15);
        font-family: 'Inter', sans-serif;
        height: 45px;
        white-space: nowrap;
        text-decoration: none;
        display: inline-block;
    }
    
    .topbar-btn:hover {
        background: var(--poly-green);
        color: var(--mustard-gold);
        border-color: var(--poly-green);
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(21, 71, 52, 0.4);
    }
    
    /* Position navigation buttons in topbar */
    .topbar-nav-buttons {
        position: fixed;
        top: 12px;
        right: 2rem;
        z-index: 1000000;
        display: flex;
        gap: 1rem;
        width: auto;
    }
    
    .topbar-nav-buttons .stColumns {
        width: auto !important;
        gap: 1rem !important;
    }
    
    .topbar-nav-buttons button {
        background: var(--mustard-gold) !important;
        color: var(--poly-green-dark) !important;
        border: 2px solid var(--mustard-gold) !important;
        padding: 0.6rem 1.2rem !important;
        border-radius: 8px !important;
        font-weight: 700 !important;
        font-size: 0.9rem !important;
        cursor: pointer !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 3px 8px rgba(0,0,0,0.15) !important;
        font-family: 'Inter', sans-serif !important;
        height: 45px !important;
        white-space: nowrap !important;
        min-width: 120px !important;
    }
    
    .topbar-nav-buttons button:hover {
        background: var(--poly-green) !important;
        color: var(--mustard-gold) !important;
        border-color: var(--poly-green) !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(21, 71, 52, 0.4) !important;
    }
    
    .block-container {
        padding-top: 90px !important;
        padding-bottom: 2rem !important;
        background: transparent !important;
        margin-top: 0 !important;
    }
    
    .dashboard-card {
        background: """ + theme['bg_card'] + """ !important;
        border-radius: 12px;
        padding: 2rem;
        margin-bottom: 2rem;
        box-shadow: none !important;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(196, 146, 20, 0.2);
    }
    
    .metric-card {
        background: linear-gradient(135deg, #ffc72c 0%, #ffb000 100%);
        border-radius: 8px;
        padding: 1.5rem;
        text-align: center;
        color: #154734;
        font-weight: bold;
        margin-bottom: 1rem;
    }
    
    .metric-card.current {
        background: linear-gradient(135deg, #ff6b6b 0%, #ee5a52 100%);
        color: white;
    }
    
    .metric-card.target {
        background: linear-gradient(135deg, #51cf66 0%, #40c057 100%);
        color: white;
    }
    
    .metric-card.gap {
        background: linear-gradient(135deg, #339af0 0%, #228be6 100%);
        color: white;
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
        background: rgba(21, 71, 52, 0.05);
        border-left: 4px solid #154734;
        padding: 1rem;
        margin: 0.5rem 0;
        border-radius: 0 8px 8px 0;
    }
    
    .phase-card.achieved {
        background: rgba(81, 207, 102, 0.1);
        border-left-color: #51cf66;
    }
    
    h1, h2, h3 {
        color: """ + theme['text_primary'] + """ !important;
    }
    
    .big-number {
        font-size: 4rem;
        font-weight: 800;
        text-align: center;
        margin: 1rem 0;
    }
    
    .current-number { color: #ff6b6b; }
    .target-number { color: #51cf66; }
    .gap-number { color: #339af0; }
    
    /* Comprehensive text color coverage for light/dark mode - EXCEPT navigation buttons */
    p:not(.topbar-nav-buttons p), 
    div:not(.topbar-nav-buttons div), 
    span:not(.topbar-nav-buttons span), 
    li, ul, ol, strong, em, b, i {
        color: """ + theme['text_body'] + """ !important;
    }
    
    /* Streamlit specific text elements - EXCEPT navigation buttons */
    .stMarkdown:not(.topbar-nav-buttons .stMarkdown), 
    .stMarkdown p:not(.topbar-nav-buttons p), 
    .stMarkdown div:not(.topbar-nav-buttons div), 
    .stMarkdown span:not(.topbar-nav-buttons span) {
        color: """ + theme['text_body'] + """ !important;
    }
    
    /* ULTRA-SPECIFIC RULES FOR NAVIGATION BUTTON TEXT - MUST STAY WHITE */
    .topbar-nav-buttons .stButton > button,
    .topbar-nav-buttons .stButton > button *,
    .topbar-nav-buttons .stButton > button span,
    .topbar-nav-buttons .stButton > button p,
    .topbar-nav-buttons .stButton > button div {
        color: #FFFFFF !important;
    }
    
    .topbar-nav-buttons .stButton > button:hover,
    .topbar-nav-buttons .stButton > button:hover *,
    .topbar-nav-buttons .stButton > button:hover span,
    .topbar-nav-buttons .stButton > button:hover p,
    .topbar-nav-buttons .stButton > button:hover div {
        color: #FFFFFF !important;
    }
    
    .topbar-nav-buttons .stButton > button:active,
    .topbar-nav-buttons .stButton > button:active *,
    .topbar-nav-buttons .stButton > button:active span,
    .topbar-nav-buttons .stButton > button:active p,
    .topbar-nav-buttons .stButton > button:active div,
    .topbar-nav-buttons .stButton > button:focus,
    .topbar-nav-buttons .stButton > button:focus *,
    .topbar-nav-buttons .stButton > button:focus span,
    .topbar-nav-buttons .stButton > button:focus p,
    .topbar-nav-buttons .stButton > button:focus div {
        color: #FFFFFF !important;
    }
    
    /* OVERRIDE ANY STREAMLIT DEFAULT BUTTON TEXT COLORS */
    .stButton > button {
        color: #FFFFFF !important;
    }
    
    .stButton > button:hover {
        color: #FFFFFF !important;
    }
    
    .stButton > button:active,
    .stButton > button:focus {
        color: #FFFFFF !important;
    }
    
    /* FORCE WHITE TEXT ON ALL BUTTON CHILDREN */
    .stButton > button * {
        color: #FFFFFF !important;
    }
    
    .stButton > button:hover * {
        color: #FFFFFF !important;
    }
    
    .stButton > button:active *,
    .stButton > button:focus * {
        color: #FFFFFF !important;
    }
    
    .po-stat {
        background: rgba(21, 71, 52, 0.1);
        padding: 1rem;
        border-radius: 8px;
        text-align: center;
        margin: 0.5rem 0;
        color: """ + theme['text_body'] + """;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(196, 146, 20, 0.3);
    }
    
    .po-stat strong {
        color: """ + theme['text_primary'] + """ !important;
        font-weight: 800;
    }
    
    .highlight-number {
        color: var(--mustard-gold) !important;
        font-weight: 800 !important;
        font-size: 1.1em;
    }
    
    .subtitle-text {
        color: """ + theme['text_secondary'] + """ !important;
    }
    
    /* Phase card text styling */
    .phase-card, .phase-card p, .phase-card strong {
        color: """ + theme['text_body'] + """ !important;
    }
    
    /* Success/warning/info text colors adapted for theme */
    .success-text { 
        color: """ + ('#51cf66' if st.session_state.dark_mode else '#2d8f47') + """ !important; 
    }
    .warning-text { 
        color: """ + ('#DC143C' if st.session_state.dark_mode else '#c92a2a') + """ !important; 
    }
    .info-text { 
        color: var(--mustard-gold) !important; 
    }
    
    /* Metric cards should always have white text regardless of theme */
    .metric-card, .metric-card *, .metric-card p, .metric-card div, .metric-card span {
        color: white !important;
    }
    
    .metric-value, .metric-label {
        color: white !important;
    }
    
    /* Navigation buttons should ALWAYS have white text regardless of theme */
    .stButton > button {
        color: #FFFFFF !important;
        background-color: var(--mustard-gold) !important;
        border: none !important;
        font-weight: 500 !important;
    }
    
    .stButton > button:hover {
        background-color: var(--mustard-gold-light) !important;
        color: #FFFFFF !important;
    }
    
    .stButton > button:active, .stButton > button:focus {
        background-color: var(--poly-green) !important;
        color: #FFFFFF !important;
        outline: none !important;
    }
    
    /* Target all navigation and settings buttons specifically with static white text */
    .topbar-nav-buttons .stButton > button {
        background-color: var(--mustard-gold) !important;
        color: #FFFFFF !important;
        border: none !important;
        font-weight: 500 !important;
        padding: 0.5rem 1rem !important;
        border-radius: 6px !important;
    }
    
    .topbar-nav-buttons .stButton > button:hover {
        background-color: var(--mustard-gold-light) !important;
        color: #FFFFFF !important;
        transform: translateY(-1px) !important;
        box-shadow: 0 2px 8px rgba(196, 146, 20, 0.3) !important;
    }
    
    .topbar-nav-buttons .stButton > button:active,
    .topbar-nav-buttons .stButton > button:focus {
        background-color: var(--poly-green) !important;
        color: #FFFFFF !important;
        outline: none !important;
    }
    
    /* Override any theme-based text color changes for navigation buttons */
    .topbar-nav-buttons .stButton > button,
    .topbar-nav-buttons .stButton > button *,
    .topbar-nav-buttons .stButton > button span,
    .topbar-nav-buttons .stButton > button p {
        color: #FFFFFF !important;
    }
    
    /* Settings panel buttons with static white text - NO YELLOW HIGHLIGHTS */
    .stButton > button[kind="secondary"] {
        background-color: #333333 !important;
        color: #FFFFFF !important;
        border: 1px solid #555555 !important;
    }
    
    .stButton > button[kind="secondary"]:hover {
        background-color: #555555 !important;
        color: #FFFFFF !important;
    }
    
    /* Specific styling for close settings button with static white text - NO YELLOW HIGHLIGHTS */
    button[key="close_settings"] {
        background-color: #333333 !important;
        color: #FFFFFF !important;
        border: 1px solid #555555 !important;
    }
    
    button[key="close_settings"]:hover {
        background-color: #555555 !important;
        color: #FFFFFF !important;
    }
    
    /* Override any theme changes for close settings button - WHITE TEXT ONLY */
    button[key="close_settings"],
    button[key="close_settings"] *,
    button[key="close_settings"] span,
    button[key="close_settings"] p {
        color: #FFFFFF !important;
    }

/* FINAL OVERRIDE - NAVIGATION BUTTONS MUST BE WHITE - MAXIMUM PRIORITY */
.stButton > button,
.stButton > button *,
.stButton > button span,
.stButton > button p,
.stButton > button div,
.stButton > button strong,
.stButton > button em {
    color: #FFFFFF !important;
}

.stButton > button:hover,
.stButton > button:hover *,
.stButton > button:hover span,
.stButton > button:hover p,
.stButton > button:hover div,
.stButton > button:hover strong,
.stButton > button:hover em {
    color: #FFFFFF !important;
}

.stButton > button:active,
.stButton > button:active *,
.stButton > button:active span,
.stButton > button:active p,
.stButton > button:active div,
.stButton > button:active strong,
.stButton > button:active em,
.stButton > button:focus,
.stButton > button:focus *,
.stButton > button:focus span,
.stButton > button:focus p,
.stButton > button:focus div,
.stButton > button:focus strong,
.stButton > button:focus em {
    color: #FFFFFF !important;
}

/* TOPBAR NAVIGATION SPECIFIC - ABSOLUTE PRIORITY */
.topbar-nav-buttons .stButton > button,
.topbar-nav-buttons .stButton > button *,
.topbar-nav-buttons .stButton > button span,
.topbar-nav-buttons .stButton > button p,
.topbar-nav-buttons .stButton > button div,
.topbar-nav-buttons .stButton > button strong,
.topbar-nav-buttons .stButton > button em {
    color: #FFFFFF !important;
}

.topbar-nav-buttons .stButton > button:hover,
.topbar-nav-buttons .stButton > button:hover *,
.topbar-nav-buttons .stButton > button:hover span,
.topbar-nav-buttons .stButton > button:hover p,
.topbar-nav-buttons .stButton > button:hover div,
.topbar-nav-buttons .stButton > button:hover strong,
.topbar-nav-buttons .stButton > button:hover em {
    color: #FFFFFF !important;
}

.topbar-nav-buttons .stButton > button:active,
.topbar-nav-buttons .stButton > button:active *,
.topbar-nav-buttons .stButton > button:active span,
.topbar-nav-buttons .stButton > button:active p,
.topbar-nav-buttons .stButton > button:active div,
.topbar-nav-buttons .stButton > button:active strong,
.topbar-nav-buttons .stButton > button:active em,
.topbar-nav-buttons .stButton > button:focus,
.topbar-nav-buttons .stButton > button:focus *,
.topbar-nav-buttons .stButton > button:focus span,
.topbar-nav-buttons .stButton > button:focus p,
.topbar-nav-buttons .stButton > button:focus div,
.topbar-nav-buttons .stButton > button:focus strong,
.topbar-nav-buttons .stButton > button:focus em {
    color: #FFFFFF !important;
}

/* CHATBOT BUTTON - YELLOW CIRCLE WITH GREEN DUCK */
.chatbot-button {
    position: fixed;
    bottom: 30px;
    right: 30px;
    width: 60px;
    height: 60px;
    background: linear-gradient(135deg, #FFD700 0%, #FFC107 100%);
    border-radius: 50%;
    border: none;
    cursor: pointer;
    box-shadow: 0 4px 20px rgba(255, 215, 0, 0.4);
    z-index: 1000;
    display: flex;
    align-items: center;
    justify-content: center;
    transition: all 0.3s ease;
}

.chatbot-button:hover {
    transform: scale(1.1);
    box-shadow: 0 6px 25px rgba(255, 215, 0, 0.6);
}

.chatbot-button:active {
    transform: scale(0.95);
}

/* GREEN DUCK EMOJI */
.duck-emoji {
    font-size: 28px;
    line-height: 1;
}

/* CHATBOT MODAL */
.chatbot-modal {
    position: fixed;
    bottom: 100px;
    right: 30px;
    width: 350px;
    height: 500px;
    background: """ + theme['bg_card'] + """;
    border-radius: 15px;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
    z-index: 1001;
    display: flex;
    flex-direction: column;
    border: 2px solid var(--mustard-gold);
    backdrop-filter: blur(10px);
}

.chatbot-header {
    background: linear-gradient(135deg, var(--mustard-gold) 0%, var(--mustard-gold-light) 100%);
    color: white;
    padding: 15px 20px;
    border-radius: 13px 13px 0 0;
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-weight: 600;
}

.chatbot-close {
    background: none;
    border: none;
    color: white;
    font-size: 18px;
    cursor: pointer;
    padding: 5px;
    border-radius: 50%;
    transition: background 0.3s ease;
}

.chatbot-close:hover {
    background: rgba(255, 255, 255, 0.2);
}

.chatbot-messages {
    flex: 1;
    padding: 15px;
    overflow-y: auto;
    display: flex;
    flex-direction: column;
    gap: 10px;
}

.chat-message {
    max-width: 80%;
    padding: 10px 15px;
    border-radius: 15px;
    word-wrap: break-word;
}

.chat-message.user {
    background: var(--mustard-gold);
    color: white;
    align-self: flex-end;
    border-bottom-right-radius: 5px;
}

.chat-message.bot {
    background: """ + theme['text_secondary'] + """;
    color: """ + theme['text_primary'] + """;
    align-self: flex-start;
    border-bottom-left-radius: 5px;
}

.chatbot-input {
    padding: 15px;
    border-top: 1px solid rgba(196, 146, 20, 0.3);
    display: flex;
    gap: 10px;
}

.chatbot-input input {
    flex: 1;
    padding: 10px 15px;
    border: 1px solid rgba(196, 146, 20, 0.3);
    border-radius: 20px;
    background: """ + theme['bg_card'] + """;
    color: """ + theme['text_primary'] + """;
    outline: none;
}

.chatbot-input input:focus {
    border-color: var(--mustard-gold);
}

.chatbot-send {
    background: var(--mustard-gold);
    color: white;
    border: none;
    padding: 10px 15px;
    border-radius: 20px;
    cursor: pointer;
    font-weight: 500;
    transition: background 0.3s ease;
}

.chatbot-send:hover {
    background: var(--mustard-gold-light);
}
    
    .section-icon {
        font-size: 1.2rem;
        margin-right: 0.5rem;
        color: var(--mustard-gold);
    }
    
    /* Table styling */
    .stDataFrame {
        background: rgba(255, 255, 255, 0.1) !important;
        border-radius: 8px !important;
        backdrop-filter: blur(10px) !important;
        border: 1px solid rgba(196, 146, 20, 0.3) !important;
    }
    
    .stDataFrame td, .stDataFrame th {
        color: """ + theme['text_primary'] + """ !important;
        border-color: rgba(196, 146, 20, 0.2) !important;
    }
    
    .stDataFrame th {
        background-color: rgba(196, 146, 20, 0.2) !important;
        color: """ + theme['text_primary'] + """ !important;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)


# Create topbar with title
st.markdown(f"""
<div class="topbar">
    <div class="topbar-title">
        <i class="bi bi-building"></i>
        PO Diversity Dashboard
    </div>
</div>
""", unsafe_allow_html=True)

# Navigation buttons positioned in topbar using CSS
st.markdown("""
<div class="topbar-nav-buttons">
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns([1, 1, 1])
with col1:
    if st.button("📊 Dashboard", key="nav-dashboard", use_container_width=True):
        st.session_state.current_page = 'dashboard'
        st.session_state.show_settings = False
        st.rerun()
with col2:
    if st.button("⚙️ Settings", key="nav-settings", use_container_width=True):
        st.session_state.show_settings = not st.session_state.show_settings
        st.rerun()
with col3:
    if st.button("ℹ️ About", key="nav-about", use_container_width=True):
        st.session_state.current_page = 'about'
        st.session_state.show_settings = False
        st.rerun()

st.markdown("</div>", unsafe_allow_html=True)

# Custom CSS for overall styling
st.markdown(f"""
<style>
    /* General app styling improvements */
    .stApp {{
        background: {theme['body_bg']} !important;
    }}
</style>
""", unsafe_allow_html=True)

# Settings toggles (when settings modal is open)
if st.session_state.show_settings:
    st.markdown("### Settings Panel")
    
    col1, col2 = st.columns(2)
    with col1:
        dark_mode = st.toggle("Dark Mode", value=st.session_state.dark_mode, key="dark_mode_toggle")
        if dark_mode != st.session_state.dark_mode:
            st.session_state.dark_mode = dark_mode
            st.rerun()
    
    with col2:
        notifications = st.toggle("Notifications", value=st.session_state.notifications, key="notifications_toggle")
        if notifications != st.session_state.notifications:
            st.session_state.notifications = notifications
            st.rerun()
    
    if st.button("Close Settings", key="close_settings", type="secondary"):
        st.session_state.show_settings = False
        st.rerun()

# Chatbot Interface
def get_chatbot_response(user_message):
    """AI-powered chatbot responses for procurement questions"""
    if not CHATBOT_AVAILABLE:
        return "🦆 I apologize, but the advanced AI chatbot features are currently unavailable. Please ensure all required packages are installed. I can still provide basic assistance with procurement questions!"
    
    try:
        # Get current dashboard data for context
        context_data = get_current_dashboard_context()
        
        # Load current data into analyzer if available
        if hasattr(st.session_state, 'analytics') and st.session_state.analytics is not None:
            # POQuantityAnalytics doesn't have .data, so we'll skip this for now
            pass
            
            # Get comprehensive analysis
            analysis_data = st.session_state.data_analyzer.get_comprehensive_analysis()
            
            # Use AI-powered response generation
            if st.session_state.chatbot_engine.is_ai_enabled:
                response = st.session_state.chatbot_engine.get_response(user_message, context_data)
            else:
                # Use intelligent rule-based responses
                response = st.session_state.response_generator.generate_response(user_message, analysis_data)
        else:
            # Fallback to chatbot engine without specific data
            response = st.session_state.chatbot_engine.get_response(user_message, context_data)
        
        return f"🤖 {response}"
        
    except Exception as e:
        # Fallback to simple responses if there's an error
        return get_fallback_chatbot_response(user_message)

def get_current_dashboard_context():
    """Get current dashboard context data for chatbot"""
    context = {
        'timestamp': pd.Timestamp.now().isoformat(),
        'current_page': st.session_state.get('current_page', 'dashboard'),
        'dark_mode': st.session_state.get('dark_mode', True)
    }
    
    # Add analytics data if available
    if hasattr(st.session_state, 'analytics') and st.session_state.analytics is not None:
        try:
            # Get current stats from analytics
            stats = st.session_state.analytics.calculate_current_po_percentage()
            context.update({
                'total_pos': stats.get('total_pos', 0),
                'current_po_percentage': stats.get('current_percentage', 'N/A'),
                'target_percentage': st.session_state.analytics.target_percentage,
                'small_business_pos': stats.get('small_business_pos', 0)
            })
        except Exception:
            pass  # Continue without analytics data
    
    return context

def get_fallback_chatbot_response(user_message):
    """Fallback chatbot responses when AI is not available"""
    user_message_lower = user_message.lower()
    
    if any(word in user_message_lower for word in ['hello', 'hi', 'hey', 'greetings']):
        return "🤖 Hello! I'm your AI-powered supplier diversity assistant. I can help analyze your procurement data, track progress toward diversity targets, and provide recommendations. What would you like to know?"
    
    elif any(word in user_message_lower for word in ['help', 'what can you do', 'capabilities']):
        return """🤖 I can help you with:

• **PO Analysis**: Track small business percentage and progress toward targets
• **Gap Analysis**: Calculate how many more POs you need to meet goals  
• **Supplier Insights**: Recommend transitions and identify opportunities
• **Data Trends**: Analyze spending patterns and performance metrics
• **Compliance**: Monitor diversity requirements and reporting

What would you like to explore?"""
    
    elif any(word in user_message_lower for word in ['target', 'goal', '25%', 'percentage']):
        return "🤖 I can help you track progress toward your supplier diversity targets! The typical goal is 25% of POs going to small businesses. I can analyze your current performance, calculate gaps, and suggest strategies to reach your targets."
    
    elif any(word in user_message_lower for word in ['small business', 'supplier', 'diversity']):
        return "🤖 Small business supplier diversity is crucial for economic growth and compliance. I can help identify opportunities to transition to small business suppliers, analyze your current participation rates, and recommend strategies for improvement."
    
    elif any(word in user_message_lower for word in ['data', 'analyze', 'analysis', 'insights']):
        return "🤖 I can provide comprehensive analysis of your procurement data! This includes trend analysis, category breakdowns, supplier performance metrics, and actionable insights to improve your supplier diversity program."
    
    else:
        return "🤖 I'm here to help with supplier diversity and procurement analysis! Ask me about PO percentages, target gaps, supplier recommendations, or data insights. How can I assist you today?"


# Tiny Floating Chat Integration
try:
    from frontend.floating_chat import render_floating_chat
    
    # Get current dashboard data for context
    dashboard_context = {
        'current_po_percentage': 'N/A',
        'target_percentage': 25.0,
        'total_pos': 0,
        'small_business_pos': 0,
        'last_updated': pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S"),
        'page': 'Main Dashboard'
    }
    
    # Add analytics data if available
    if hasattr(st.session_state, 'analytics') and st.session_state.analytics is not None:
        try:
            # Get current stats from the analytics object
            stats = st.session_state.analytics.calculate_current_po_percentage()
            dashboard_context.update({
                'current_po_percentage': stats.get('current_percentage', 'N/A'),
                'target_percentage': st.session_state.analytics.target_percentage,
                'total_pos': stats.get('total_pos', 0),
                'small_business_pos': stats.get('small_business_pos', 0)
            })
        except Exception:
            pass  # Continue without analytics data
    
    # Fallback to loaded data if analytics object isn't working
    if dashboard_context['current_po_percentage'] == 'N/A':
        try:
            # Try to load analytics data directly
            analytics = POQuantityAnalytics()
            stats = analytics.calculate_current_po_percentage()
            dashboard_context.update({
                'current_po_percentage': stats.get('current_percentage', 'N/A'),
                'total_pos': stats.get('total_pos', 0),
                'small_business_pos': stats.get('small_business_pos', 0)
            })
        except Exception:
            pass
    
    # Add floating chat interface
    render_floating_chat(dashboard_context)
    
except ImportError:
    # Fallback to original chatbot button
    if st.button("🦆 Toggle Chat", key="chatbot_toggle_main", help="Toggle Quack Chat"):
        st.session_state.show_chatbot = not st.session_state.show_chatbot
        st.rerun()

# Simple HTML button that works
st.markdown("""
<button id="simple-chat-button" style="
    position: fixed !important;
    bottom: 90px !important;
    right: 30px !important;
    z-index: 2147483646 !important;
    width: 280px !important;
    height: 45px !important;
    background: rgba(255, 255, 255, 0.95) !important;
    border: 2px solid #FFD700 !important;
    border-radius: 25px !important;
    cursor: pointer !important;
    font-size: 14px !important;
    font-weight: 500 !important;
    color: #666 !important;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1) !important;
    transition: all 0.3s ease !important;
    backdrop-filter: blur(10px) !important;
    pointer-events: auto !important;
" onclick="
    console.log('Simple button clicked!');
    const toggleBtn = document.querySelector('button[title=\\'Toggle Quack Chat\\']') || 
                     Array.from(document.querySelectorAll('button')).find(b => b.textContent.includes('🦆 Toggle Chat'));
    if (toggleBtn) {
        console.log('Found toggle button, clicking...');
        toggleBtn.click();
    } else {
        console.log('Toggle button not found, trying page refresh...');
        window.location.reload();
    }
">
💬 Ask me about supplier diversity...
</button>

<style>
#simple-chat-button:hover {
    background: rgba(255, 255, 255, 1) !important;
    border-color: #FFC107 !important;
    box-shadow: 0 6px 25px rgba(255, 215, 0, 0.3) !important;
    transform: translateY(-2px) !important;
    color: #333 !important;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<style>
/* STICKY TOGGLE CHAT BUTTON - MAXIMUM SPECIFICITY FOR FIXED POSITIONING */
html body .stApp .main div[data-testid="stButton"]:has(button[title="Toggle Quack Chat"]),
html body .stApp .main div[data-testid="stButton"]:has(button:contains("🦆 Toggle Chat")),
html body .stApp .main .stButton:has(button[title="Toggle Quack Chat"]),
html body .stApp .main .stButton:has(button:contains("🦆 Toggle Chat")),
div[data-testid="stButton"]:has(button[title="Toggle Quack Chat"]),
div[data-testid="stButton"]:has(button:contains("🦆 Toggle Chat")),
.stButton:has(button[title="Toggle Quack Chat"]),
.stButton:has(button:contains("🦆 Toggle Chat")) {
    position: fixed !important;
    bottom: 30px !important;
    right: 30px !important;
    z-index: 2147483647 !important;
    width: 120px !important;
    height: 50px !important;
    top: auto !important;
    left: auto !important;
    transform: none !important;
    margin: 0 !important;
    padding: 0 !important;
    pointer-events: auto !important;
}

/* STICKY TOGGLE CHAT BUTTON STYLING - ULTRA HIGH SPECIFICITY */
html body .stApp .main button[title="Toggle Quack Chat"],
html body .stApp .main button:contains("🦆 Toggle Chat"),
html body .stApp .main div[data-testid="stButton"] button:contains("🦆 Toggle Chat"),
button[title="Toggle Quack Chat"],
button:contains("🦆 Toggle Chat"),
div[data-testid="stButton"] button:contains("🦆 Toggle Chat") {
    position: fixed !important;
    bottom: 30px !important;
    right: 30px !important;
    z-index: 2147483647 !important;
    width: 120px !important;
    height: 50px !important;
    border-radius: 25px !important;
    background: linear-gradient(135deg, #FFD700 0%, #FFC107 100%) !important;
    border: none !important;
    font-size: 16px !important;
    font-weight: 600 !important;
    color: #333333 !important;
    cursor: pointer !important;
    box-shadow: 0 4px 20px rgba(255, 215, 0, 0.4) !important;
    transition: all 0.3s ease !important;
    top: auto !important;
    left: auto !important;
    transform: none !important;
    margin: 0 !important;
    padding: 0 !important;
    pointer-events: auto !important;
}

/* Hover effects for sticky button */
button[title="Toggle Quack Chat"]:hover,
button:contains("🦆 Toggle Chat"):hover {
    transform: scale(1.05) !important;
    box-shadow: 0 6px 25px rgba(255, 215, 0, 0.6) !important;
    background: linear-gradient(135deg, #FFE135 0%, #FFD700 100%) !important;
    color: #333333 !important;
    position: fixed !important;
    bottom: 30px !important;
    right: 30px !important;
    z-index: 2147483647 !important;
}

/* Active effects for sticky button */
button[title="Toggle Quack Chat"]:active,
button:contains("🦆 Toggle Chat"):active {
    transform: scale(0.98) !important;
    position: fixed !important;
    bottom: 30px !important;
    right: 30px !important;
    z-index: 2147483647 !important;
}

/* Ensure button stays sticky during scroll events */
.stApp .main .block-container button:contains("🦆 Toggle Chat"),
.stApp button:contains("🦆 Toggle Chat") {
    position: fixed !important;
    bottom: 30px !important;
    right: 30px !important;
    z-index: 2147483647 !important;
    pointer-events: auto !important;
}

/* Override any potential interference from Streamlit's default styles */
[data-testid="stButton"]:has(button:contains("🦆 Toggle Chat")) {
    position: fixed !important;
    bottom: 30px !important;
    right: 30px !important;
    z-index: 2147483647 !important;
    width: 120px !important;
    height: 50px !important;
}

/* Final fallback - catch any button with duck emoji anywhere in the DOM */
* button:contains("🦆") {
    position: fixed !important;
    bottom: 30px !important;
    right: 30px !important;
    z-index: 2147483647 !important;
    width: 120px !important;
    height: 50px !important;
    border-radius: 25px !important;
    background: linear-gradient(135deg, #FFD700 0%, #FFC107 100%) !important;
    border: none !important;
    font-size: 16px !important;
    font-weight: 600 !important;
    color: #333333 !important;
    cursor: pointer !important;
    box-shadow: 0 4px 20px rgba(255, 215, 0, 0.4) !important;
    pointer-events: auto !important;
}

/* STICKY CLICKABLE TEXT BOX FOR CHAT */
#sticky-chat-textbox {
    position: fixed !important;
    bottom: 90px !important;
    right: 30px !important;
    z-index: 2147483646 !important;
    width: 280px !important;
    height: 45px !important;
    background: rgba(255, 255, 255, 0.95) !important;
    border: 2px solid #FFD700 !important;
    border-radius: 25px !important;
    cursor: pointer !important;
    display: flex !important;
    align-items: center !important;
    justify-content: flex-start !important;
    padding: 0 20px !important;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1) !important;
    transition: all 0.3s ease !important;
    backdrop-filter: blur(10px) !important;
    pointer-events: auto !important;
}

#sticky-chat-textbox:hover {
    background: rgba(255, 255, 255, 1) !important;
    border-color: #FFC107 !important;
    box-shadow: 0 6px 25px rgba(255, 215, 0, 0.3) !important;
    transform: translateY(-2px) !important;
}

#sticky-chat-textbox .chat-prompt {
    color: #666 !important;
    font-size: 14px !important;
    font-weight: 500 !important;
    user-select: none !important;
    pointer-events: none !important;
}

#sticky-chat-textbox:hover .chat-prompt {
    color: #333 !important;
}

/* Dark mode styles for the text box */
.dark-mode #sticky-chat-textbox {
    background: rgba(45, 45, 45, 0.95) !important;
    border-color: #FFD700 !important;
}

.dark-mode #sticky-chat-textbox:hover {
    background: rgba(55, 55, 55, 1) !important;
}

.dark-mode #sticky-chat-textbox .chat-prompt {
    color: #ccc !important;
}

.dark-mode #sticky-chat-textbox:hover .chat-prompt {
    color: #fff !important;
}

/* Hide the hidden trigger button */
button[title="Hidden button for text box"],
[data-testid="stButton"]:has(button[title="Hidden button for text box"]) {
    display: none !important;
    visibility: hidden !important;
    position: absolute !important;
    left: -9999px !important;
}

/* Alternative approach - target by text content with JavaScript injection */
div[data-testid="stButton"] {
    position: relative;
}

/* Try to catch any button with duck emoji */
button:contains("🦆") {
    position: fixed !important;
    bottom: 30px !important;
    right: 30px !important;
    z-index: 9999 !important;
}

/* CHAT BUTTON STYLING - positioned above the duck button - MAXIMUM SPECIFICITY */
html body .stApp .main div[data-testid="stButton"]:has(button[title="Open Chat"]),
html body .stApp .main div[data-testid="stButton"]:has(button:contains("Chat")),
html body .stApp .main .stButton:has(button[title="Open Chat"]),
html body .stApp .main .stButton:has(button:contains("Chat")),
div[data-testid="stButton"]:has(button[title="Open Chat"]),
div[data-testid="stButton"]:has(button:contains("Chat")),
.stButton:has(button[title="Open Chat"]),
.stButton:has(button:contains("Chat")) {
    position: fixed !important;
    bottom: 90px !important;
    right: 30px !important;
    z-index: 999999 !important;
    width: 80px !important;
    height: 40px !important;
    top: auto !important;
    left: auto !important;
    transform: none !important;
    margin: 0 !important;
    padding: 0 !important;
}

/* Style the actual chat button - ULTRA HIGH SPECIFICITY */
html body .stApp .main button[title="Open Chat"],
html body .stApp .main button:contains("Chat"):not(:contains("🦆")),
html body .stApp .main div[data-testid="stButton"] button:contains("Chat"):not(:contains("🦆")),
button[title="Open Chat"],
button:contains("Chat"):not(:contains("🦆")),
div[data-testid="stButton"] button:contains("Chat"):not(:contains("🦆")) {
    position: fixed !important;
    bottom: 90px !important;
    right: 30px !important;
    z-index: 999999 !important;
    width: 80px !important;
    height: 40px !important;
    border-radius: 20px !important;
    background: linear-gradient(135deg, var(--mustard-gold) 0%, var(--mustard-gold-light) 100%) !important;
    border: none !important;
    font-size: 14px !important;
    font-weight: 600 !important;
    color: #FFFFFF !important;
    cursor: pointer !important;
    box-shadow: 0 4px 15px rgba(255, 199, 44, 0.4) !important;
    transition: all 0.3s ease !important;
    top: auto !important;
    left: auto !important;
    transform: none !important;
    margin: 0 !important;
    padding: 0 !important;
}

/* Chat button hover effects */
button[title="Open Chat"]:hover,
button:contains("Chat"):not(:contains("🦆")):hover {
    transform: scale(1.05) !important;
    box-shadow: 0 6px 20px rgba(255, 199, 44, 0.6) !important;
    background: linear-gradient(135deg, var(--mustard-gold-light) 0%, var(--mustard-gold) 100%) !important;
    color: #FFFFFF !important;
}

/* Chat button active effects */
button[title="Open Chat"]:active,
button:contains("Chat"):not(:contains("🦆")):active {
    transform: scale(0.98) !important;
}

/* ADDITIONAL STICKY POSITIONING - Force the chatbot button to stay fixed */
#chatbot-button-container {
    position: fixed !important;
    bottom: 30px !important;
    right: 30px !important;
    z-index: 99999 !important;
    width: 120px !important;
    height: 50px !important;
    pointer-events: auto !important;
    display: block !important;
    visibility: visible !important;
}

/* CHAT BUTTON CONTAINER */
#chat-button-container {
    position: fixed !important;
    bottom: 90px !important;
    right: 30px !important;
    z-index: 99999 !important;
    width: 80px !important;
    height: 40px !important;
    pointer-events: auto !important;
    display: block !important;
    visibility: visible !important;
}

/* Force any button inside the container to be properly styled */
#chatbot-button-container button,
#chatbot-button-container .stButton,
#chatbot-button-container .stButton > button {
    position: relative !important;
    width: 100% !important;
    height: 100% !important;
    border-radius: 25px !important;
    background: linear-gradient(135deg, #FFD700 0%, #FFC107 100%) !important;
    border: none !important;
    font-size: 16px !important;
    font-weight: 600 !important;
    color: #333333 !important;
    cursor: pointer !important;
    box-shadow: 0 4px 20px rgba(255, 215, 0, 0.4) !important;
    transition: all 0.3s ease !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
}

#chatbot-button-container button:hover {
    transform: scale(1.05) !important;
    box-shadow: 0 6px 25px rgba(255, 215, 0, 0.6) !important;
    background: linear-gradient(135deg, #FFE135 0%, #FFD700 100%) !important;
}

/* Force any button inside the chat container to be properly styled */
#chat-button-container button,
#chat-button-container .stButton,
#chat-button-container .stButton > button {
    position: relative !important;
    width: 100% !important;
    height: 100% !important;
    border-radius: 20px !important;
    background: linear-gradient(135deg, var(--mustard-gold) 0%, var(--mustard-gold-light) 100%) !important;
    border: none !important;
    font-size: 14px !important;
    font-weight: 600 !important;
    color: #FFFFFF !important;
    cursor: pointer !important;
    box-shadow: 0 4px 15px rgba(255, 199, 44, 0.4) !important;
    transition: all 0.3s ease !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
}

#chat-button-container button:hover {
    transform: scale(1.05) !important;
    box-shadow: 0 6px 20px rgba(255, 199, 44, 0.6) !important;
    background: linear-gradient(135deg, var(--mustard-gold-light) 0%, var(--mustard-gold) 100%) !important;
}

</style>

<script>
// Find and position both buttons after page loads
document.addEventListener('DOMContentLoaded', function() {
    setTimeout(function() {
        // Find the buttons by text content
        const buttons = document.querySelectorAll('button');
        let chatbotButton = null;
        let chatbotContainer = null;
        let chatButton = null;
        let chatContainer = null;
        
        buttons.forEach(function(btn) {
            if (btn.textContent.includes('🦆 Toggle Chat')) {
                console.log('Found chatbot button:', btn);
                chatbotButton = btn;
                chatbotContainer = btn.closest('[data-testid="stButton"]') || btn.closest('.stButton');
            } else if (btn.textContent.trim() === 'Chat') {
                console.log('Found chat button:', btn);
                chatButton = btn;
                chatContainer = btn.closest('[data-testid="stButton"]') || btn.closest('.stButton');
            }
        });
        
        // Handle chatbot button
        if (chatbotButton && chatbotContainer) {
            console.log('Moving chatbot button to fixed container');
            
            // Find the fixed container we created
            const fixedContainer = document.getElementById('chatbot-button-container');
            if (fixedContainer) {
                // Move the entire button container into our fixed container
                fixedContainer.appendChild(chatbotContainer);
                
                // Style the moved container
                chatbotContainer.style.width = '100%';
                chatbotContainer.style.height = '100%';
                chatbotContainer.style.position = 'relative';
                
                // Style the button
                chatbotButton.style.width = '100%';
                chatbotButton.style.height = '100%';
                chatbotButton.style.borderRadius = '25px';
                chatbotButton.style.background = 'linear-gradient(135deg, #FFD700 0%, #FFC107 100%)';
                chatbotButton.style.border = 'none';
                chatbotButton.style.fontSize = '16px';
                chatbotButton.style.fontWeight = '600';
                chatbotButton.style.color = '#333333';
                chatbotButton.style.cursor = 'pointer';
                chatbotButton.style.boxShadow = '0 4px 20px rgba(255, 215, 0, 0.4)';
                chatbotButton.style.transition = 'all 0.3s ease';
                chatbotButton.style.display = 'flex';
                chatbotButton.style.alignItems = 'center';
                chatbotButton.style.justifyContent = 'center';
                
                console.log('Chatbot button moved to fixed container successfully');
            } else {
                console.log('Chatbot fixed container not found');
            }
        }
        
        // Handle chat button
        if (chatButton && chatContainer) {
            console.log('Moving chat button to fixed container');
            
            // Find the fixed container we created
            const chatFixedContainer = document.getElementById('chat-button-container');
            if (chatFixedContainer) {
                // Move the entire button container into our fixed container
                chatFixedContainer.appendChild(chatContainer);
                
                // Style the moved container
                chatContainer.style.width = '100%';
                chatContainer.style.height = '100%';
                chatContainer.style.position = 'relative';
                
                // Style the button
                chatButton.style.width = '100%';
                chatButton.style.height = '100%';
                chatButton.style.borderRadius = '20px';
                chatButton.style.background = 'linear-gradient(135deg, #ffc72c 0%, #ffd54f 100%)';
                chatButton.style.border = 'none';
                chatButton.style.fontSize = '14px';
                chatButton.style.fontWeight = '600';
                chatButton.style.color = '#FFFFFF';
                chatButton.style.cursor = 'pointer';
                chatButton.style.boxShadow = '0 4px 15px rgba(255, 199, 44, 0.4)';
                chatButton.style.transition = 'all 0.3s ease';
                chatButton.style.display = 'flex';
                chatButton.style.alignItems = 'center';
                chatButton.style.justifyContent = 'center';
                
                console.log('Chat button moved to fixed container successfully');
            } else {
                console.log('Chat fixed container not found');
            }
        }
        
        if (!chatbotButton && !chatButton) {
            console.log('No buttons found - available buttons:');
            buttons.forEach((btn, i) => {
                console.log(`Button ${i}:`, btn.textContent);
            });
        }
        
        // Keep trying to find and move both buttons with a more persistent approach
        let attempts = 0;
        const maxAttempts = 10;
        
        function findAndMoveButtons() {
            attempts++;
            console.log(`Attempt ${attempts} to find buttons`);
            
            const buttons = document.querySelectorAll('button');
            let chatbotFound = false;
            let chatFound = false;
            
            buttons.forEach(function(btn) {
                // Handle ducK button
                if (btn.textContent.includes('🦆 Toggle Chat')) {
                    const container = btn.closest('[data-testid="stButton"]') || btn.closest('.stButton');
                    const fixedContainer = document.getElementById('chatbot-button-container');
                    
                    if (container && fixedContainer && !fixedContainer.contains(container)) {
                        console.log(`Found and moving chatbot button on attempt ${attempts}`);
                        
                        // Move to fixed container
                        fixedContainer.appendChild(container);
                        
                        // Style the container and button
                        container.style.width = '100%';
                        container.style.height = '100%';
                        container.style.position = 'relative';
                        
                        btn.style.width = '100%';
                        btn.style.height = '100%';
                        btn.style.borderRadius = '25px';
                        btn.style.background = 'linear-gradient(135deg, #FFD700 0%, #FFC107 100%)';
                        btn.style.border = 'none';
                        btn.style.fontSize = '16px';
                        btn.style.fontWeight = '600';
                        btn.style.color = '#333333';
                        btn.style.cursor = 'pointer';
                        btn.style.boxShadow = '0 4px 20px rgba(255, 215, 0, 0.4)';
                        btn.style.transition = 'all 0.3s ease';
                        btn.style.display = 'flex';
                        btn.style.alignItems = 'center';
                        btn.style.justifyContent = 'center';
                        
                        chatbotFound = true;
                        console.log('Chatbot button successfully moved and styled');
                    }
                }
                
                // Handle Chat button
                if (btn.textContent.trim() === 'Chat') {
                    const container = btn.closest('[data-testid="stButton"]') || btn.closest('.stButton');
                    const chatFixedContainer = document.getElementById('chat-button-container');
                    
                    if (container && chatFixedContainer && !chatFixedContainer.contains(container)) {
                        console.log(`Found and moving chat button on attempt ${attempts}`);
                        
                        // Move to fixed container
                        chatFixedContainer.appendChild(container);
                        
                        // Style the container and button
                        container.style.width = '100%';
                        container.style.height = '100%';
                        container.style.position = 'relative';
                        
                        btn.style.width = '100%';
                        btn.style.height = '100%';
                        btn.style.borderRadius = '20px';
                        btn.style.background = 'linear-gradient(135deg, #ffc72c 0%, #ffd54f 100%)';
                        btn.style.border = 'none';
                        btn.style.fontSize = '14px';
                        btn.style.fontWeight = '600';
                        btn.style.color = '#FFFFFF';
                        btn.style.cursor = 'pointer';
                        btn.style.boxShadow = '0 4px 15px rgba(255, 199, 44, 0.4)';
                        btn.style.transition = 'all 0.3s ease';
                        btn.style.display = 'flex';
                        btn.style.alignItems = 'center';
                        btn.style.justifyContent = 'center';
                        
                        chatFound = true;
                        console.log('Chat button successfully moved and styled');
                    }
                }
            });
            
            if ((!chatbotFound || !chatFound) && attempts < maxAttempts) {
                setTimeout(findAndMoveButtons, 1000);
            } else if (!chatbotFound && !chatFound) {
                console.log('Failed to find buttons after all attempts');
            }
        }
        
        // Start the persistent search
        findAndMoveButtons();
        
    }, 1000);
    
    // Enhanced function to ensure buttons stay sticky
    function ensureButtonsSticky() {
        // Force position both containers
        const chatbotContainer = document.getElementById('chatbot-button-container');
        const chatContainer = document.getElementById('chat-button-container');
        const stickyTextbox = document.getElementById('sticky-chat-textbox');
        
        if (chatbotContainer) {
            chatbotContainer.style.position = 'fixed';
            chatbotContainer.style.bottom = '30px';
            chatbotContainer.style.right = '30px';
            chatbotContainer.style.zIndex = '2147483647';
            chatbotContainer.style.width = '120px';
            chatbotContainer.style.height = '50px';
            chatbotContainer.style.pointerEvents = 'auto';
            chatbotContainer.style.display = 'block';
            chatbotContainer.style.visibility = 'visible';
        }
        
        // Ensure sticky text box stays positioned
        if (stickyTextbox) {
            stickyTextbox.style.position = 'fixed';
            stickyTextbox.style.bottom = '90px';
            stickyTextbox.style.right = '30px';
            stickyTextbox.style.zIndex = '2147483646';
            stickyTextbox.style.width = '280px';
            stickyTextbox.style.height = '45px';
            stickyTextbox.style.pointerEvents = 'auto';
            stickyTextbox.style.display = 'flex';
            stickyTextbox.style.visibility = 'visible';
        }
        
        // Also directly style any toggle chat buttons found
        const allButtons = document.querySelectorAll('button');
        allButtons.forEach(function(btn) {
            if (btn.textContent.includes('🦆 Toggle Chat')) {
                btn.style.position = 'fixed';
                btn.style.bottom = '30px';
                btn.style.right = '30px';
                btn.style.zIndex = '2147483647';
                btn.style.width = '120px';
                btn.style.height = '50px';
                btn.style.pointerEvents = 'auto';
                
                // Also style the parent container
                const parentContainer = btn.closest('[data-testid="stButton"]') || btn.closest('.stButton');
                if (parentContainer) {
                    parentContainer.style.position = 'fixed';
                    parentContainer.style.bottom = '30px';
                    parentContainer.style.right = '30px';
                    parentContainer.style.zIndex = '2147483647';
                    parentContainer.style.width = '120px';
                    parentContainer.style.height = '50px';
                    parentContainer.style.pointerEvents = 'auto';
                }
            }
        });
    }
        
        if (chatContainer) {
            chatContainer.style.position = 'fixed';
            chatContainer.style.bottom = '90px';
            chatContainer.style.right = '30px';
            chatContainer.style.zIndex = '999999';
            chatContainer.style.width = '80px';
            chatContainer.style.height = '40px';
            chatContainer.style.pointerEvents = 'auto';
            chatContainer.style.display = 'block';
            chatContainer.style.visibility = 'visible';
        }
    }
    
    // Add event listeners to maintain sticky positioning during scroll and resize
    window.addEventListener('scroll', ensureButtonsSticky, { passive: true });
    window.addEventListener('resize', ensureButtonsSticky, { passive: true });
    
    // Also run on DOM mutations to catch dynamic content changes
    const observer = new MutationObserver(function(mutations) {
        let shouldUpdate = false;
        mutations.forEach(function(mutation) {
            if (mutation.type === 'childList' || mutation.type === 'attributes') {
                shouldUpdate = true;
            }
        });
        if (shouldUpdate) {
            setTimeout(ensureButtonsSticky, 100);
        }
    });
    
    observer.observe(document.body, {
        childList: true,
        subtree: true,
        attributes: true,
        attributeFilter: ['style', 'class']
    });
    
    // Run initial positioning
    ensureButtonsSticky();
    
    // Run periodically to catch any missed updates
    setInterval(ensureButtonsSticky, 2000);
    
    // Simplified global function to open chat from text box
    window.openChatFromTextbox = function() {
        console.log('Opening chat from text box...');
        
        // Look for the hidden button first
        const hiddenButton = document.querySelector('button[title="Hidden button for text box"]');
        if (hiddenButton) {
            console.log('Found hidden button, clicking...');
            hiddenButton.click();
            return;
        }
        
        // Fallback to main toggle button
        const buttons = document.querySelectorAll('button');
        for (let btn of buttons) {
            if (btn.textContent.includes('🦆 Toggle Chat')) {
                console.log('Clicking main toggle button...');
                btn.click();
                return;
            }
        }
        
        console.error('No chat buttons found!');
    };
    
    // Also make triggerChatOpen available globally
    window.triggerChatOpen = function() {
        if (window.openChatFromTextbox) {
            window.openChatFromTextbox();
        }
    };
    
    // Also ensure the text box is always positioned correctly
    function ensureTextboxSticky() {
        const stickyTextbox = document.getElementById('sticky-chat-textbox');
        if (stickyTextbox) {
            stickyTextbox.style.position = 'fixed';
            stickyTextbox.style.bottom = '90px';
            stickyTextbox.style.right = '30px';
            stickyTextbox.style.zIndex = '2147483646';
            stickyTextbox.style.pointerEvents = 'auto';
        }
    }
    
    // Enhanced function to find the toggle chat button
    function findToggleChatButton() {
        // Method 1: Look for button with specific text content
        let buttons = document.querySelectorAll('button');
        for (let btn of buttons) {
            if (btn.textContent.includes('🦆 Toggle Chat')) {
                return btn;
            }
        }
        
        // Method 2: Look in Streamlit button containers
        let buttonContainers = document.querySelectorAll('[data-testid="stButton"]');
        for (let container of buttonContainers) {
            let btn = container.querySelector('button');
            if (btn && btn.textContent.includes('🦆')) {
                return btn;
            }
        }
        
        // Method 3: Look for buttons with duck emoji anywhere
        for (let btn of buttons) {
            if (btn.textContent.includes('🦆')) {
                return btn;
            }
        }
        
        // Method 4: Look for buttons with "Toggle" and "Chat" in text
        for (let btn of buttons) {
            if (btn.textContent.includes('Toggle') && btn.textContent.includes('Chat')) {
                return btn;
            }
        }
        
        return null;
    }
    
    // Test function to verify button detection
    function testButtonDetection() {
        const btn = findToggleChatButton();
        if (btn) {
            console.log('Toggle chat button found:', btn);
            console.log('Button text:', btn.textContent);
            console.log('Button parent:', btn.parentElement);
        } else {
            console.log('Toggle chat button NOT found');
            console.log('Available buttons:', document.querySelectorAll('button'));
        }
    }
    
    // Run test periodically
    setInterval(testButtonDetection, 5000);
    
    // Run textbox positioning checks
    setInterval(ensureTextboxSticky, 1000);
        
        // Force position any buttons that might have moved
        const allButtons = document.querySelectorAll('button');
        allButtons.forEach(function(btn) {
            if (btn.textContent.includes('🦆 Toggle Chat')) {
                btn.style.position = 'fixed';
                btn.style.bottom = '30px';
                btn.style.right = '30px';
                btn.style.zIndex = '999999';
            } else if (btn.textContent.trim() === 'Chat') {
                btn.style.position = 'fixed';
                btn.style.bottom = '90px';
                btn.style.right = '30px';
                btn.style.zIndex = '999999';
            }
        });
    }
    
    // Run on scroll, resize, and periodically
    window.addEventListener('scroll', ensureButtonsSticky);
    window.addEventListener('resize', ensureButtonsSticky);
    setInterval(ensureButtonsSticky, 2000); // Check every 2 seconds
    
    // Initial call
    setTimeout(ensureButtonsSticky, 500);
});
</script>

<!-- Fixed containers for sticky buttons with inline styles for maximum priority -->
<div id="chatbot-button-container" style="position: fixed !important; bottom: 30px !important; right: 30px !important; z-index: 999999 !important; width: 120px !important; height: 50px !important; pointer-events: auto !important; display: block !important; visibility: visible !important;"></div>
<div id="chat-button-container" style="position: fixed !important; bottom: 90px !important; right: 30px !important; z-index: 999999 !important; width: 80px !important; height: 40px !important; pointer-events: auto !important; display: block !important; visibility: visible !important;"></div>
""", unsafe_allow_html=True)

# Chatbot Modal - Pure HTML/CSS popup (no Streamlit widgets inside)
if st.session_state.show_chatbot:
    # Initialize with welcome message if empty
    if not st.session_state.chat_messages:
        st.session_state.chat_messages.append({
            "role": "bot", 
            "content": "🦆 Quack! Hello! I'm your procurement assistant. Ask me about supplier diversity, the dashboard data, or small business procurement strategies!"
        })
    
    # Build chat messages HTML
    messages_html = ""
    for message in st.session_state.chat_messages:
        if message["role"] == "user":
            messages_html += f'<div class="chat-message user">{message["content"]}</div>'
        else:
            messages_html += f'<div class="chat-message bot">{message["content"]}</div>'
    
    # Create the complete modal as pure HTML
    st.markdown(f"""
    <div class="chatbot-modal">
        <div class="chatbot-header">
            <div>
                <span>🦆 Quack - Procurement Assistant</span>
            </div>
            <button class="chatbot-close" onclick="document.querySelector('button[key=\\"chatbot_toggle_main\\"]').click()">×</button>
        </div>
        <div class="chatbot-messages" id="chat-messages">
            {messages_html}
        </div>
        <div class="chatbot-input">
            <input type="text" id="chat-input" placeholder="Type your question here..." />
            <button id="chat-send" onclick="sendMessage()">Send 🦆</button>
        </div>
    </div>
    
    <script>
    // Function to open chat from the sticky text box
    function openChatFromTextbox() {{
        console.log('Opening chat from text box (modal version)...');
        
        // Use the same logic as the global function
        let toggleButton = document.querySelector('button[data-testid="baseButton-secondary"][title="Toggle Quack Chat"]');
        
        if (!toggleButton) {{
            const buttons = document.querySelectorAll('button');
            buttons.forEach(function(btn) {{
                if (btn.textContent.includes('🦆 Toggle Chat')) {{
                    toggleButton = btn;
                }}
            }});
        }}
        
        if (!toggleButton) {{
            const buttonContainers = document.querySelectorAll('[data-testid="stButton"]');
            buttonContainers.forEach(function(container) {{
                const btn = container.querySelector('button');
                if (btn && btn.textContent.includes('🦆 Toggle Chat')) {{
                    toggleButton = btn;
                }}
            }});
        }}
        
        if (toggleButton) {{
            toggleButton.click();
            setTimeout(function() {{
                const chatInput = document.getElementById('chat-input');
                if (chatInput) {{
                    chatInput.focus();
                }}
            }}, 500);
        }}
    }}
    
    function sendMessage() {{
        const input = document.getElementById('chat-input');
        const message = input.value.trim();
        if (message) {{
            // For now, just show an alert - we'd need a more complex setup to actually process messages
            alert('Message sent: ' + message);
            input.value = '';
        }}
    }}
    
    // Allow Enter key to send message
    document.getElementById('chat-input').addEventListener('keypress', function(e) {{
        if (e.key === 'Enter') {{
            sendMessage();
        }}
    }});
    </script>
    """, unsafe_allow_html=True)

# ULTIMATE CSS OVERRIDE - MAXIMUM SPECIFICITY FOR STICKY BUTTONS
st.markdown(f"""
<style>
/* ULTIMATE OVERRIDE - FORCE STICKY POSITIONING WITH HIGHEST POSSIBLE SPECIFICITY */
html body .stApp .main .block-container #chatbot-button-container,
html body .stApp .main #chatbot-button-container,
html body .stApp #chatbot-button-container,
html body #chatbot-button-container,
#chatbot-button-container {{
    position: fixed !important;
    bottom: 30px !important;
    right: 30px !important;
    z-index: 2147483647 !important;
    width: 120px !important;
    height: 50px !important;
    pointer-events: auto !important;
    display: block !important;
    visibility: visible !important;
    top: auto !important;
    left: auto !important;
    transform: none !important;
    margin: 0 !important;
    padding: 0 !important;
}}

html body .stApp .main .block-container #chat-button-container,
html body .stApp .main #chat-button-container,
html body .stApp #chat-button-container,
html body #chat-button-container,
#chat-button-container {{
    position: fixed !important;
    bottom: 90px !important;
    right: 30px !important;
    z-index: 2147483647 !important;
    width: 80px !important;
    height: 40px !important;
    pointer-events: auto !important;
    display: block !important;
    visibility: visible !important;
    top: auto !important;
    left: auto !important;
    transform: none !important;
    margin: 0 !important;
    padding: 0 !important;
}}

/* FORCE BUTTON POSITIONING WITH ABSOLUTE MAXIMUM SPECIFICITY */
html body .stApp .main .block-container button[title="Toggle Quack Chat"],
html body .stApp .main .block-container button:contains("🦆 Toggle Chat"),
html body .stApp .main button[title="Toggle Quack Chat"],
html body .stApp .main button:contains("🦆 Toggle Chat"),
html body .stApp button[title="Toggle Quack Chat"],
html body .stApp button:contains("🦆 Toggle Chat"),
html body button[title="Toggle Quack Chat"],
html body button:contains("🦆 Toggle Chat"),
button[title="Toggle Quack Chat"],
button:contains("🦆 Toggle Chat") {{
    position: fixed !important;
    bottom: 30px !important;
    right: 30px !important;
    z-index: 2147483647 !important;
    width: 120px !important;
    height: 50px !important;
    top: auto !important;
    left: auto !important;
    transform: none !important;
    margin: 0 !important;
    padding: 0 !important;
}}

html body .stApp .main .block-container button[title="Open Chat"],
html body .stApp .main .block-container button:contains("Chat"):not(:contains("🦆")),
html body .stApp .main button[title="Open Chat"],
html body .stApp .main button:contains("Chat"):not(:contains("🦆")),
html body .stApp button[title="Open Chat"],
html body .stApp button:contains("Chat"):not(:contains("🦆")),
html body button[title="Open Chat"],
html body button:contains("Chat"):not(:contains("🦆")),
button[title="Open Chat"],
button:contains("Chat"):not(:contains("🦆")) {{
    position: fixed !important;
    bottom: 90px !important;
    right: 30px !important;
    z-index: 2147483647 !important;
    width: 80px !important;
    height: 40px !important;
    top: auto !important;
    left: auto !important;
    transform: none !important;
    margin: 0 !important;
    padding: 0 !important;
}}
</style>
""", unsafe_allow_html=True)

# FINAL OVERRIDE - CLEAN UP - No longer needed since we only have yellow button
st.markdown(f"""
<style>
    /* CHATBOT MODAL POSITIONING */
    .chatbot-modal {{
        position: fixed !important;
        bottom: 90px !important;
        right: 30px !important;
        width: 350px !important;
        height: 500px !important;
        background: {theme['bg_card']} !important;
        border-radius: 15px !important;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3) !important;
        z-index: 10000 !important;
        display: flex !important;
        flex-direction: column !important;
        border: 2px solid var(--mustard-gold) !important;
        backdrop-filter: blur(10px) !important;
    }}
</style>
""", unsafe_allow_html=True)

# About Page Content
def render_about_page():
    st.markdown(f"""
    <div class="dashboard-card">
        <h1 style="margin: 0; text-align: center; font-size: 4rem; font-weight: 800; line-height: 1.1; letter-spacing: -0.02em;">About Our Mission</h1>
        <p class="subtitle-text" style="text-align: center; margin-top: 1rem; font-size: 1.3rem;">
            Empowering Small Businesses Through <span style="color: var(--mustard-gold); font-weight: 600;">Data-Driven Procurement</span>
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Mission Statement
    st.markdown(f"""
    <div class="dashboard-card">
        <h2 style="color: var(--mustard-gold); margin-bottom: 1rem;">🎯 Our Mission</h2>
        <p style="font-size: 1.1rem; line-height: 1.6;">
            We are dedicated to creating equitable opportunities for small businesses by providing data-driven insights 
            that help organizations achieve their diversity procurement goals. Our platform bridges the gap between 
            large institutions and small business suppliers, fostering economic growth and community development.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Why We Do This
    st.markdown(f"""
    <div class="dashboard-card">
        <h2 style="color: var(--mustard-gold); margin-bottom: 1rem;">💡 Why We Do This</h2>
        <p style="font-size: 1.1rem; line-height: 1.6;">
            Small businesses are the backbone of our economy, representing 99.9% of all U.S. businesses and employing 
            nearly half of the private workforce. However, they often face barriers in accessing procurement opportunities 
            with large organizations. Our solution uses advanced analytics to identify optimal matches between current 
            suppliers and qualified small businesses, making the transition seamless and data-driven.
        </p>
    </div>
    """, unsafe_allow_html=True)

# Page Routing Logic
if st.session_state.current_page == 'about':
    render_about_page()
    st.stop()  # Stop execution here for About page

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
    
    # Initialize analytics object for chatbot
    if 'analytics' not in st.session_state:
        st.session_state.analytics = POQuantityAnalytics()
        
except Exception as e:
    st.error(f"Error loading data: {str(e)}")
    data_loaded = False
    data = {}

# Header
st.markdown("""
<div class="dashboard-card">
    <h1 style="margin: 0; text-align: center; font-size: 4rem; font-weight: 800; line-height: 1.1; letter-spacing: -0.02em;">Small Business PO Percentage Target</h1>
    <p class="subtitle-text" style="text-align: center; margin-top: 1rem; font-size: 1.3rem;">
        Current % of Purchase Orders vs. <span class="highlight-number">25% Target</span>
    </p>
</div>
""", unsafe_allow_html=True)

if data_loaded and 'error' not in data['current_stats']:
    current_stats = data['current_stats']
    
    # Big Numbers Section - PO Quantities
    st.markdown('<div class="dashboard-card">', unsafe_allow_html=True)
    st.markdown("## 📊 Purchase Order Percentage Analysis")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
        <div class="big-number current-number">{current_stats['current_percentage']:.1f}%</div>
        <h3 style="text-align: center; color: #ff6b6b;">Current PO %</h3>
        <div class="po-stat">
            <strong>{current_stats['current_small_business_pos']:,}</strong> small business POs<br>
            out of <strong>{current_stats['total_pos']:,}</strong> total POs
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="big-number target-number">{current_stats['target_percentage']:.1f}%</div>
        <h3 style="text-align: center; color: #51cf66;">Target PO %</h3>
        <div class="po-stat">
            Need <strong>{current_stats['target_pos_needed']:,}</strong> small business POs<br>
            out of <strong>{current_stats['total_pos']:,}</strong> total POs
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="big-number gap-number">{current_stats['gap_pos_needed']:,}</div>
        <h3 style="text-align: center; color: #339af0;">POs to Transition</h3>
        <div class="po-stat">
            Need to transition <strong>{current_stats['gap_pos_needed']:,}</strong> more POs<br>
            from current suppliers to small businesses
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # PO Distribution Visualization
    st.markdown('<div class="dashboard-card">', unsafe_allow_html=True)
    st.markdown('<h2 style="margin: 0;">PO Distribution: Current vs Target</h2>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Current PO distribution pie chart
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
                'Small Business POs': '#ff6b6b',
                'Other POs': '#cccccc'
            }
        )
        fig_current.update_layout(
            font=dict(color=theme['text_primary']),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            title_font_color=theme['text_primary']
        )
        st.plotly_chart(fig_current, use_container_width=True)
    
    with col2:
        # Optimal Path to Exactly 25% (moved from scenarios section)
        st.markdown("### 🎯 Optimal Path to Exactly 25%")
        
        if 'error' not in data['optimization_plan']:
            opt_plan = data['optimization_plan']
            optimal = opt_plan['optimal_path']
            
            if optimal.get('target_achieved', False):
                st.markdown(f"""
                <div class="metric-card target" style="margin-bottom: 1rem;">
                    <div class="metric-value">{optimal['pos_to_transition']:,}</div>
                    <div class="metric-label">POs Need to Transition</div>
                </div>
                """, unsafe_allow_html=True)
                
                st.markdown(f"""
                <div class="metric-card gap" style="margin-bottom: 1rem;">
                    <div class="metric-value">{optimal.get('avg_similarity_score', 0):.3f}</div>
                    <div class="metric-label">Average Similarity Score</div>
                </div>
                """, unsafe_allow_html=True)
                
                st.markdown("**Strategic Approach:**")
                st.markdown(f"• Transition **{optimal['pos_to_transition']:,} purchase orders** from current suppliers")
                st.markdown(f"• Achieve exactly **{optimal['resulting_percentage']:.1f}%** small business POs")
                st.markdown(f"• Average match quality: **{optimal.get('avg_similarity_score', 0):.1%}** similarity")
                st.markdown("• Focus on highest similarity matches first")
            else:
                st.warning(f"⚠️ {optimal.get('message', 'Cannot reach 25% with available matches')}")
                if 'shortfall' in optimal:
                    st.markdown(f"**Gap:** Need {optimal['shortfall']:,} more potential matches to reach 25%")
        else:
            st.info("📊 Optimal path analysis requires scenario data to be available")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Optimization Scenarios
    if 'error' not in data['optimization_plan']:
        opt_plan = data['optimization_plan']
        
        st.markdown('<div class="dashboard-card">', unsafe_allow_html=True)
        st.markdown("## 🚀 PO Transition Scenarios to Reach 25%")
        
        scenarios = opt_plan['scenarios']
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            high_conf = scenarios['high_confidence']
            st.markdown(f"""
            <div class="phase-card {'achieved' if high_conf['target_achieved'] else ''}">
                <h4>🎯 High Confidence (≥0.4 similarity)</h4>
                <p><strong>POs to transition:</strong> {high_conf['pos_to_transition']:,}</p>
                <p><strong>Resulting %:</strong> {high_conf['resulting_percentage']:.1f}%</p>
                <p><strong>Total small business POs:</strong> {high_conf['resulting_small_business_pos']:,}</p>
                {'<p style="color: #51cf66;"><strong>✅ TARGET ACHIEVED!</strong></p>' if high_conf['target_achieved'] else '<p style="color: #ff6b6b;"><strong>❌ Target not reached</strong></p>'}
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            med_conf = scenarios['medium_confidence']
            st.markdown(f"""
            <div class="phase-card achieved">
                <h4>📈 Medium Confidence (≥0.2 similarity)</h4>
                <p><strong>POs to transition:</strong> {med_conf['pos_to_transition']:,}</p>
                <p><strong>Resulting %:</strong> {med_conf['resulting_percentage']:.1f}%</p>
                <p><strong>Total small business POs:</strong> {med_conf['resulting_small_business_pos']:,}</p>
                <p style="color: #51cf66;"><strong>✅ TARGET EXCEEDED!</strong></p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            all_matches = scenarios['all_matches']
            st.markdown(f"""
            <div class="phase-card achieved">
                <h4>🔄 All Available Matches</h4>
                <p><strong>POs to transition:</strong> {all_matches['pos_to_transition']:,}</p>
                <p><strong>Resulting %:</strong> {all_matches['resulting_percentage']:.1f}%</p>
                <p><strong>Total small business POs:</strong> {all_matches['resulting_small_business_pos']:,}</p>
                <p style="color: #51cf66;"><strong>✅ MAXIMUM POTENTIAL!</strong></p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Implementation Phases
    if opt_plan.get('implementation_phases'):
        st.markdown('<div class="dashboard-card">', unsafe_allow_html=True)
        st.markdown("## 📅 Phased Implementation Plan")
        
        phases_df = pd.DataFrame(opt_plan['implementation_phases'])
        
        # Create phase visualization
        fig_phases = go.Figure()
        
        colors = ['#ff6b6b', '#ffc72c', '#339af0', '#51cf66', '#9775fa']
        
        for i, phase in enumerate(phases_df.itertuples()):
            fig_phases.add_trace(go.Bar(
                name=phase.phase,
                x=[phase.phase],
                y=[phase.resulting_percentage],
                marker_color=colors[i % len(colors)],
                text=f"{phase.resulting_percentage:.1f}%<br>({phase.cumulative_pos} POs)",
                textposition='inside'
            ))
        
        fig_phases.add_hline(y=25, line_dash="dash", line_color="#51cf66", 
                            annotation_text="25% Target")
        
        fig_phases.update_layout(
            title="Cumulative PO Percentage by Implementation Phase",
            yaxis_title="Small Business PO Percentage (%)",
            font=dict(color=theme['text_primary']),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            showlegend=False,
            title_font_color=theme['text_primary']
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
        st.markdown("## ⚡ Top PO Transition Opportunities")
        
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
        st.markdown("## 🔄 Current Suppliers with Most PO Transition Opportunities")
        
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
    
    # Footer
    st.markdown(f"""
    <div class="dashboard-card" style="text-align: center;">
        <p style="margin: 0; color: var(--mustard-gold-light);">
            <i class="bi bi-mortarboard"></i> Cal Poly SLO AI Summer Camp - Small Business PO Percentage Analysis
        </p>
        <p style="margin: 0; font-size: 0.9rem; color: {theme['text_secondary']};">
            Focus: <span style="color: var(--mustard-gold); font-weight: 600;">Percentage of Purchase Orders</span> (not dollar amounts) going to small businesses
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.success("✅ Navigation system implemented successfully! Use the buttons above to navigate between Dashboard and About pages, or access Settings.")

else:
    st.markdown('<div class="dashboard-card">', unsafe_allow_html=True)
    st.markdown("## ⚠️ Data Not Available")
    st.markdown("""
    Unable to load PO quantity analysis data. Please ensure:
    
    1. Backend analysis has been completed
    2. CSV files are available in the backend directory
    3. Test results contain purchase order information
    """)
    st.markdown('</div>', unsafe_allow_html=True)
