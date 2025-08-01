import streamlit as st
from auth_manager import auth_manager
from typing import Optional

def show_login_form():
    """Display login form"""
    st.markdown("### 🔐 Login to Supplier Diversity Dashboard")
    
    with st.form("login_form"):
        username = st.text_input("Username", placeholder="Enter your username")
        password = st.text_input("Password", type="password", placeholder="Enter your password")
        
        col1, col2 = st.columns(2)
        with col1:
            login_button = st.form_submit_button("Login", use_container_width=True)
        with col2:
            register_button = st.form_submit_button("Register", use_container_width=True)
        
        if login_button:
            if username and password:
                with st.spinner("Authenticating..."):
                    success, message, user_data = auth_manager.authenticate_user(username, password)
                
                if success:
                    st.success(message)
                    st.rerun()
                else:
                    st.error(message)
            else:
                st.error("Please enter both username and password")
        
        if register_button:
            st.session_state.show_register = True
            st.rerun()

def show_register_form():
    """Display registration form"""
    st.markdown("### 📝 Register for Supplier Diversity Dashboard")
    
    with st.form("register_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            username = st.text_input("Username*", placeholder="Choose a username")
            email = st.text_input("Email*", placeholder="your.email@company.com")
        
        with col2:
            full_name = st.text_input("Full Name", placeholder="Your full name")
            password = st.text_input("Password*", type="password", placeholder="Choose a strong password")
        
        st.markdown("**Password Requirements:**")
        st.markdown("- At least 8 characters long")
        st.markdown("- Contains uppercase and lowercase letters")
        st.markdown("- Contains at least one number")
        st.markdown("- Contains at least one special character")
        
        col1, col2 = st.columns(2)
        with col1:
            register_button = st.form_submit_button("Register", use_container_width=True)
        with col2:
            back_button = st.form_submit_button("Back to Login", use_container_width=True)
        
        if register_button:
            if username and password and email:
                with st.spinner("Creating account..."):
                    success, message = auth_manager.register_user(username, password, email, full_name)
                
                if success:
                    st.success(message)
                    st.info("Please check your email for verification instructions, then return to login.")
                    if st.button("Go to Login"):
                        st.session_state.show_register = False
                        st.rerun()
                else:
                    st.error(message)
            else:
                st.error("Please fill in all required fields (marked with *)")
        
        if back_button:
            st.session_state.show_register = False
            st.rerun()

def show_user_menu():
    """Display user menu in sidebar"""
    if not auth_manager.is_authenticated():
        return
    
    user_data = auth_manager.get_current_user()
    if not user_data:
        return
    
    with st.sidebar:
        st.markdown("---")
        st.markdown("### 👤 User Account")
        
        # Display user info
        username = user_data['username']
        email = user_data['attributes'].get('email', 'N/A')
        name = user_data['attributes'].get('name', username)
        
        st.markdown(f"**Welcome, {name}!**")
        st.markdown(f"📧 {email}")
        st.markdown(f"👤 @{username}")
        
        # User actions
        if st.button("🔑 Change Password", use_container_width=True):
            st.session_state.show_change_password = True
        
        if st.button("🚪 Logout", use_container_width=True):
            auth_manager.logout()
            st.success("Logged out successfully!")
            st.rerun()

def show_change_password_form():
    """Display change password form"""
    st.markdown("### 🔑 Change Password")
    
    with st.form("change_password_form"):
        old_password = st.text_input("Current Password", type="password")
        new_password = st.text_input("New Password", type="password")
        confirm_password = st.text_input("Confirm New Password", type="password")
        
        col1, col2 = st.columns(2)
        with col1:
            change_button = st.form_submit_button("Change Password", use_container_width=True)
        with col2:
            cancel_button = st.form_submit_button("Cancel", use_container_width=True)
        
        if change_button:
            if not all([old_password, new_password, confirm_password]):
                st.error("Please fill in all fields")
            elif new_password != confirm_password:
                st.error("New passwords do not match")
            elif len(new_password) < 8:
                st.error("New password must be at least 8 characters long")
            else:
                with st.spinner("Changing password..."):
                    success, message = auth_manager.change_password(old_password, new_password)
                
                if success:
                    st.success(message)
                    st.session_state.show_change_password = False
                    st.rerun()
                else:
                    st.error(message)
        
        if cancel_button:
            st.session_state.show_change_password = False
            st.rerun()

def require_authentication():
    """
    Main authentication wrapper function
    Returns True if user is authenticated, False otherwise
    """
    # Check if user is authenticated
    if auth_manager.is_authenticated():
        # Show user menu in sidebar
        show_user_menu()
        
        # Handle change password form
        if st.session_state.get('show_change_password', False):
            show_change_password_form()
            return False  # Don't show main content while changing password
        
        return True
    
    # User not authenticated - show login/register forms
    st.markdown("""
    <div style="text-align: center; padding: 2rem;">
        <h1>🏢 Supplier Diversity Dashboard</h1>
        <p style="font-size: 1.2rem; color: #666;">
            Secure access to procurement analytics and small business targets
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Show appropriate form based on state
    if st.session_state.get('show_register', False):
        show_register_form()
    else:
        show_login_form()
    
    # Add some information about the dashboard
    st.markdown("---")
    st.markdown("### 📊 Dashboard Features")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        **📈 Analytics**
        - PO percentage tracking
        - Target progress monitoring
        - Supplier analysis
        """)
    
    with col2:
        st.markdown("""
        **🎯 Insights**
        - Gap analysis
        - Quick wins identification
        - Implementation roadmap
        """)
    
    with col3:
        st.markdown("""
        **🔒 Security**
        - AWS Cognito authentication
        - Secure data access
        - Role-based permissions
        """)
    
    return False

def get_user_role() -> Optional[str]:
    """Get the current user's role (if implemented)"""
    if not auth_manager.is_authenticated():
        return None
    
    user_data = auth_manager.get_current_user()
    if not user_data:
        return None
    
    # You can extend this to check for custom attributes like 'custom:role'
    return user_data['attributes'].get('custom:role', 'user')

def check_permission(required_role: str = 'user') -> bool:
    """Check if current user has required permission level"""
    if not auth_manager.is_authenticated():
        return False
    
    user_role = get_user_role()
    if not user_role:
        return False
    
    # Simple role hierarchy: admin > manager > user
    role_hierarchy = {
        'user': 1,
        'manager': 2,
        'admin': 3
    }
    
    user_level = role_hierarchy.get(user_role, 0)
    required_level = role_hierarchy.get(required_role, 1)
    
    return user_level >= required_level
