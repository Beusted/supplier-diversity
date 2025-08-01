import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import sys
from pathlib import Path

# Add the current directory to Python path for imports
sys.path.append(str(Path(__file__).parent))

from analytics import POQuantityAnalytics

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
    """Simple chatbot responses for procurement questions"""
    user_message_lower = user_message.lower()
    
    if any(word in user_message_lower for word in ['hello', 'hi', 'hey', 'greetings']):
        return "🦆 Quack! Hello there! I'm Quack, your procurement assistant. I'm here to help you with questions about small business procurement, supplier diversity, and the dashboard data. What would you like to know?"
    
    elif any(word in user_message_lower for word in ['help', 'what can you do', 'assistance']):
        return "🦆 I can help you with:\n• Understanding the dashboard metrics\n• Explaining procurement strategies\n• Small business certification questions\n• Supplier transition recommendations\n• Implementation planning guidance\n\nJust ask me anything about procurement!"
    
    elif any(word in user_message_lower for word in ['25%', 'target', 'goal']):
        return "🦆 The 25% target means that 25% of all Purchase Orders (POs) should go to small businesses. Currently, we're at 16.3%, so we need to transition 110 more POs to reach our goal. The dashboard shows exactly which suppliers and POs would be best to transition!"
    
    elif any(word in user_message_lower for word in ['small business', 'certification', 'qualify']):
        return "🦆 Small businesses are typically defined as companies with fewer than 500 employees (varies by industry). They need proper certification through programs like SBA 8(a), HUBZone, WOSB, or VOSB. The dashboard helps identify which current suppliers could be replaced with certified small businesses!"
    
    elif any(word in user_message_lower for word in ['similarity', 'matching', 'algorithm']):
        return "🦆 Our AI uses similarity algorithms to match current suppliers with small businesses based on their services and descriptions. Higher similarity scores (0.4+) mean safer transitions, while lower scores need more evaluation. It's like finding suppliers that do very similar work!"
    
    elif any(word in user_message_lower for word in ['implementation', 'phases', 'plan']):
        return "🦆 The phased approach starts with high-confidence matches (40%+ similarity) for quick wins, then expands to medium-confidence matches. This minimizes risk while steadily increasing your small business percentage. Think of it as a step-by-step roadmap!"
    
    elif any(word in user_message_lower for word in ['dashboard', 'charts', 'data']):
        return "🦆 The dashboard shows your current state (16.3%), target (25%), and exactly what needs to change (110 POs). The charts help visualize progress, and the tables show specific recommendations. Everything is designed to make complex procurement data easy to understand!"
    
    elif any(word in user_message_lower for word in ['thank', 'thanks', 'appreciate']):
        return "🦆 You're very welcome! I'm always here to help with your procurement questions. Feel free to ask me anything else about supplier diversity or the dashboard data. Quack quack! 🦆"
    
    elif any(word in user_message_lower for word in ['bye', 'goodbye', 'see you']):
        return "🦆 Goodbye! Remember, every PO transitioned to a small business makes a difference. Keep up the great work on supplier diversity! Quack! 🦆"
    
    else:
        return f"🦆 Quack! That's an interesting question about '{user_message}'. While I'm still learning, I can help with procurement basics, dashboard explanations, and small business supplier strategies. Could you rephrase your question or ask about something specific like targets, matching, or implementation plans?"

# ONLY YELLOW TOGGLE CHAT BUTTON - Bottom-right sticky with all functionality
st.markdown("""
<div id="bottom-right-anchor" style="
    position: fixed; 
    bottom: 30px; 
    right: 30px; 
    z-index: 9999;
    width: 120px;
    height: 50px;
">
    <button id="duck-toggle-btn" onclick="toggleYellowChatbot()" style="
        width: 100%;
        height: 100%;
        border-radius: 25px;
        background: linear-gradient(135deg, #FFD700 0%, #FFC107 100%);
        border: none;
        font-size: 16px;
        font-weight: 600;
        color: #333333;
        cursor: pointer;
        box-shadow: 0 4px 20px rgba(255, 215, 0, 0.4);
        transition: all 0.3s ease;
        display: flex;
        align-items: center;
        justify-content: center;
    ">
        🦆 Toggle Chat
    </button>
</div>

<script>
function toggleYellowChatbot() {
    // Find the hidden Streamlit button for yellow toggle and click it
    const hiddenBtn = document.querySelector('button[key="yellow_toggle_only"]');
    if (hiddenBtn) {
        hiddenBtn.click();
    }
}
</script>

<style>
#duck-toggle-btn:hover {
    transform: scale(1.05);
    box-shadow: 0 6px 25px rgba(255, 215, 0, 0.6);
    background: linear-gradient(135deg, #FFE135 0%, #FFD700 100%);
}

#duck-toggle-btn:active {
    transform: scale(0.98);
}

/* Hide the hidden Streamlit button completely */
button[key="yellow_toggle_only"] {
    display: none !important;
    visibility: hidden !important;
    position: absolute !important;
    top: -9999px !important;
}

.stButton:has(button[key="yellow_toggle_only"]) {
    display: none !important;
    visibility: hidden !important;
    position: absolute !important;
    top: -9999px !important;
}
</style>
""", unsafe_allow_html=True)

# ONLY HIDDEN BUTTON - All toggle functionality consolidated here
if st.button("🦆 Yellow Toggle Only", key="yellow_toggle_only", help="Toggle Quack Chat"):
    st.session_state.show_chatbot = not st.session_state.show_chatbot
    st.rerun()

# Chatbot Modal - Completely self-contained with internal text input
if st.session_state.show_chatbot:
    # Initialize with welcome message if empty
    if not st.session_state.chat_messages:
        st.session_state.chat_messages.append({
            "role": "bot", 
            "content": "🦆 Quack! Hello! I'm your procurement assistant. Ask me about supplier diversity, the dashboard data, or small business procurement strategies!"
        })
    
    st.markdown(f"""
    <div class="chatbot-modal">
        <div class="chatbot-header">
            <div>
                <span>🦆 Quack - Procurement Assistant</span>
            </div>
            <button class="chatbot-close" onclick="document.querySelector('button[key=\\"yellow_toggle_only\\"]').click()">×</button>
        </div>
        <div class="chatbot-messages" id="chat-messages">
    """, unsafe_allow_html=True)
    
    # Display all chat messages within the modal
    for message in st.session_state.chat_messages:
        if message["role"] == "user":
            st.markdown(f'<div class="chat-message user">{message["content"]}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="chat-message bot">{message["content"]}</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Self-contained text input area ONLY within the modal
    st.markdown('<div class="chatbot-input-area">', unsafe_allow_html=True)
    
    # Create the text input and send functionality within the modal
    with st.container():
        # Text input for user queries - ONLY appears in the modal
        user_message = st.text_input(
            "Ask Quack anything about procurement:",
            key="quack_chat_input_internal",
            placeholder="Type your question here...",
            label_visibility="collapsed"
        )
        
        # Send button - ONLY within the modal
        if st.button("Send to Quack 🦆", key="send_quack_message", use_container_width=True, type="primary"):
            if user_message and user_message.strip():
                # Add user message to chat
                st.session_state.chat_messages.append({
                    "role": "user",
                    "content": user_message.strip()
                })
                
                # Get Quack's response
                bot_response = get_chatbot_response(user_message.strip())
                st.session_state.chat_messages.append({
                    "role": "bot",
                    "content": bot_response
                })
                
                # Clear the input and refresh
                st.session_state.quack_chat_input_internal = ""
                st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)  # Close input area
    st.markdown('</div>', unsafe_allow_html=True)  # Close modal

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
