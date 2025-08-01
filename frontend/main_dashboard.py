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
    from backend.chatbot.claude_chatbot_engine import ClaudeSupplierDiversityChatbot
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
        from chatbot.claude_chatbot_engine import ClaudeSupplierDiversityChatbot
        from chatbot.data_analyzer import ProcurementDataAnalyzer
        from chatbot.response_generator import ResponseGenerator
        CHATBOT_AVAILABLE = True
    except ImportError as e2:
        st.warning(f"⚠️ Advanced chatbot features unavailable. Install AI libraries for full functionality. Error: {e2}")
        CHATBOT_AVAILABLE = False

# Page configuration
st.set_page_config(
    page_title="Duckling Dashboard",
    page_icon="🦆",
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
    st.session_state.chatbot_engine = ClaudeSupplierDiversityChatbot()
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

/* CONTAINED CHATBOT INTERFACE */
.chat-container {
    background: """ + theme['bg_card'] + """;
    border-radius: 15px;
    border: 2px solid var(--mustard-gold);
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
    backdrop-filter: blur(10px);
    margin: 1rem 0;
    overflow: hidden;
    max-height: 500px;
    height: 500px;
    display: flex;
    flex-direction: column;
}

.chat-header {
    background: linear-gradient(135deg, var(--mustard-gold) 0%, var(--mustard-gold-light) 100%);
    color: white;
    padding: 15px 20px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-weight: 600;
    font-size: 1.1rem;
    flex-shrink: 0;
}

.chat-messages-container {
    flex: 1;
    height: 350px;
    max-height: 350px;
    overflow-y: auto;
    padding: 15px;
    display: flex;
    flex-direction: column;
    gap: 10px;
    background: """ + theme['bg_card'] + """;
}

.chat-message {
    max-width: 80%;
    padding: 12px 16px;
    border-radius: 15px;
    word-wrap: break-word;
    line-height: 1.4;
}

.chat-message.user {
    background: var(--mustard-gold);
    color: white;
    align-self: flex-end;
    border-bottom-right-radius: 5px;
    font-weight: 500;
}

.chat-message.bot {
    background: rgba(196, 146, 20, 0.1);
    color: """ + theme['text_primary'] + """;
    align-self: flex-start;
    border-bottom-left-radius: 5px;
    border: 1px solid rgba(196, 146, 20, 0.2);
}

.chat-input-container {
    padding: 15px;
    border-top: 1px solid rgba(196, 146, 20, 0.3);
    background: """ + theme['bg_card'] + """;
    flex-shrink: 0;
    display: flex;
    align-items: center;
    justify-content: center;
}

.chat-input-form {
    display: flex;
    gap: 10px;
    align-items: center;
}

/* Custom scrollbar for chat messages */
.chat-messages-container::-webkit-scrollbar {
    width: 6px;
}

.chat-messages-container::-webkit-scrollbar-track {
    background: rgba(196, 146, 20, 0.1);
    border-radius: 3px;
}

.chat-messages-container::-webkit-scrollbar-thumb {
    background: var(--mustard-gold);
    border-radius: 3px;
}

.chat-messages-container::-webkit-scrollbar-thumb:hover {
    background: var(--mustard-gold-light);
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
        Duckling Dashboard
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
            
            # Use Claude AI-powered response generation
            response = st.session_state.chatbot_engine.get_response(user_message, context_data)
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
    pass

# Simple Chatbot Toggle Button
if st.button("🦆 Toggle Chat", key="chatbot_toggle_main", help="Toggle Chat"):
    st.session_state.show_chatbot = not st.session_state.show_chatbot
    st.rerun()

# Simple Chatbot Interface with Fixed Height Container
if st.session_state.show_chatbot:
    st.markdown("---")
    st.markdown("### 🦆 Quack - Procurement Assistant")
    
    # Initialize chat messages if empty
    if not st.session_state.chat_messages:
        st.session_state.chat_messages = [{
            "role": "assistant",
            "content": "🦆 Quack! Hello! I'm Quack, your procurement assistant powered by Claude AI. I specialize in supplier diversity and can help you with:\n\n• **Supplier matching** - Find diverse suppliers for your needs\n• **25% small business targets** - Track and achieve your goals\n• **Procurement strategies** - Optimize your sourcing approach\n• **Dashboard insights** - Understand your diversity metrics\n\nWhat can I help you with today?"
        }]
    
    # Create a container with fixed height for chat messages
    with st.container():
        # Add a unique ID to make scrolling more reliable
        chat_container_id = "chat-messages-container"
        
        # Display chat messages in a simple scrollable area with unique ID
        chat_html = f'<div id="{chat_container_id}" style="height: 300px; overflow-y: auto; border: 2px solid #ffc72c; border-radius: 10px; padding: 15px; background: rgba(255, 255, 255, 0.1); margin-bottom: 20px;">'
        
        for i, message in enumerate(st.session_state.chat_messages):
            if message["role"] == "user":
                chat_html += f'<div style="text-align: right; margin: 10px 0;"><div style="display: inline-block; background: #ffc72c; color: white; padding: 10px 15px; border-radius: 15px; max-width: 80%;"><strong>You:</strong> {message["content"]}</div></div>'
            else:
                chat_html += f'<div style="text-align: left; margin: 10px 0;"><div style="display: inline-block; background: rgba(255, 255, 255, 0.2); color: white; padding: 10px 15px; border-radius: 15px; max-width: 80%;"><strong>Quack:</strong> {message["content"]}</div></div>'
        
        # Add an invisible anchor at the bottom
        chat_html += '<div id="chat-bottom-anchor"></div>'
        chat_html += '</div>'
        
        st.markdown(chat_html, unsafe_allow_html=True)
        
        # More aggressive auto-scroll approach
        st.markdown(f"""
        <script>
        function scrollChatToBottom() {{
            try {{
                // Try multiple methods to find and scroll the container
                var container = document.getElementById('{chat_container_id}');
                if (container) {{
                    container.scrollTop = container.scrollHeight;
                    return;
                }}
                
                // Fallback: find by style attribute
                var containers = document.querySelectorAll('div[style*="height: 300px"]');
                for (var i = 0; i < containers.length; i++) {{
                    if (containers[i].style.overflowY === 'auto') {{
                        containers[i].scrollTop = containers[i].scrollHeight;
                        break;
                    }}
                }}
                
                // Another fallback: scroll to bottom anchor
                var anchor = document.getElementById('chat-bottom-anchor');
                if (anchor) {{
                    anchor.scrollIntoView({{ behavior: 'smooth', block: 'end' }});
                }}
            }} catch (e) {{
                console.log('Scroll error:', e);
            }}
        }}
        
        // Multiple attempts to ensure scrolling works
        setTimeout(scrollChatToBottom, 50);
        setTimeout(scrollChatToBottom, 200);
        setTimeout(scrollChatToBottom, 500);
        
        // Also try when DOM content changes
        if (window.MutationObserver) {{
            var observer = new MutationObserver(function(mutations) {{
                setTimeout(scrollChatToBottom, 100);
            }});
            observer.observe(document.body, {{ childList: true, subtree: true }});
        }}
        </script>
        """, unsafe_allow_html=True)
    
    # Use a form to handle Enter key functionality properly
    with st.form(key="chat_form", clear_on_submit=True):
        col1, col2, col3 = st.columns([4, 1, 1])
        
        with col1:
            user_input = st.text_input("Ask me anything:", placeholder="E.g., How can I improve my supplier diversity?", label_visibility="collapsed")
        
        with col2:
            send_clicked = st.form_submit_button("Send 🦆")
        
        with col3:
            clear_clicked = st.form_submit_button("Clear")
    
    # Process the message if form was submitted
    if send_clicked and user_input:
        # Add user message
        st.session_state.chat_messages.append({
            "role": "user",
            "content": user_input
        })
        
        # Get AI response
        try:
            if CHATBOT_AVAILABLE:
                # Check if the question is relevant to procurement/supplier diversity
                relevance_check = f"Is this question related to procurement, supplier diversity, small business, contracting, sourcing, or business operations? Question: '{user_input}'. Answer only 'YES' or 'NO'."
                relevance_response = get_chatbot_response(relevance_check)
                
                if "NO" in relevance_response.upper():
                    bot_response = f"🦆 Quack! I'm specifically designed to help with procurement and supplier diversity topics. I cannot help you with '{user_input}'. \n\nI'd be happy to assist you with:\n• Supplier diversity strategies\n• Small business procurement goals\n• Dashboard insights and metrics\n• Procurement best practices\n\nWhat procurement-related question can I help you with today?"
                else:
                    # Enhanced context for better responses
                    context = f"You are Quack, a helpful procurement assistant specializing in supplier diversity. The user asked: '{user_input}'. Provide a helpful, specific response about supplier diversity, procurement strategies, or dashboard insights. Keep responses conversational but informative. Stay focused on procurement topics only."
                    response = get_chatbot_response(context + " User question: " + user_input)
                    # Clean up response and add Quack personality
                    bot_response = response.replace("🤖 ", "").replace("Claude", "Quack")
                    if not bot_response.startswith("🦆"):
                        bot_response = f"🦆 {bot_response}"
            else:
                bot_response = "🦆 Quack! I'm currently having trouble connecting to my AI brain. Please make sure the chatbot service is properly configured, and I'll be right back to help with your procurement needs!"
            
            st.session_state.chat_messages.append({
                "role": "assistant", 
                "content": bot_response
            })
        except Exception as e:
            st.session_state.chat_messages.append({
                "role": "assistant",
                "content": f"🦆 Oops! I encountered a technical issue: {str(e)}. Please check the AWS configuration or try again in a moment."
            })
        
        st.rerun()
    
    # Handle clear button
    if clear_clicked:
        st.session_state.chat_messages = []
        st.rerun()

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
    st.markdown("## Purchase Order Percentage Analysis")
    
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
        st.markdown("### Optimal Path to Exactly 25%")
        
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
        st.markdown("## PO Transition Scenarios to Reach 25%")
        
        scenarios = opt_plan['scenarios']
        
        col1, col2 = st.columns(2)
        
        with col1:
            high_conf = scenarios['high_confidence']
            st.markdown(f"""
            <div class="phase-card {'achieved' if high_conf['target_achieved'] else ''}">
                <h4>🎯 High Confidence (≥0.4 similarity)</h4>
                <p><strong>POs to transition:</strong> {high_conf['pos_to_transition']:,}</p>
                <p><strong>Resulting %:</strong> {high_conf['resulting_percentage']:.1f}%</p>
                <p><strong>Total small business POs:</strong> {high_conf['resulting_small_business_pos']:,}</p>
                {'<p style="color: #51cf66;"><strong>TARGET ACHIEVED!</strong></p>' if high_conf['target_achieved'] else '<p style="color: #ff6b6b;"><strong>Target not reached</strong></p>'}
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
                <p style="color: #51cf66;"><strong>TARGET EXCEEDED!</strong></p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Implementation Phases
    if opt_plan.get('implementation_phases'):
        st.markdown('<div class="dashboard-card">', unsafe_allow_html=True)
        st.markdown("## Phased Implementation Plan")
        
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
        st.markdown("## Top PO Transition Opportunities")
        
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
                'PO_Impact_Score': 'Impact Score',
                'Contact_Info': 'Contact Information',
                'contact_person': 'Contact Person'
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
                "Contact Information": st.column_config.TextColumn(
                    "Contact Information",
                    help="Email and phone number for the small business",
                    width="medium",
                ),
                "Contact Person": st.column_config.TextColumn(
                    "Contact Person",
                    help="Primary contact person at the small business",
                    width="small",
                ),
            }
        )
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Supplier Transition Analysis
    if 'error' not in data['supplier_analysis']:
        st.markdown('<div class="dashboard-card">', unsafe_allow_html=True)
        st.markdown("## Current Suppliers with Most PO Transition Opportunities")
        
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
