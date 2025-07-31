#!/usr/bin/env python3
"""
Launch script for the Diversity in Procurement Dashboard
Run this file to start the Streamlit application
"""

import subprocess
import sys
import os

def install_requirements():
    """Install required packages if not already installed"""
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✓ Dependencies installed successfully!")
    except subprocess.CalledProcessError:
        print("✗ Error installing dependencies. Please install manually:")
        print("pip install -r requirements.txt")
        return False
    return True

def run_streamlit():
    """Launch the Streamlit application"""
    try:
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", "streamlit_app.py",
            "--server.port", "8501",
            "--server.address", "localhost",
            "--theme.base", "dark"
        ])
    except KeyboardInterrupt:
        print("\n👋 Application stopped by user")
    except Exception as e:
        print(f"✗ Error running application: {e}")

if __name__ == "__main__":
    print("🚀 Starting Diversity in Procurement Dashboard...")
    print("📦 Checking dependencies...")
    
    if install_requirements():
        print("🌐 Launching Streamlit application...")
        print("📍 The app will open in your browser at: http://localhost:8501")
        print("⏹️  Press Ctrl+C to stop the application")
        run_streamlit()
    else:
        print("✗ Failed to start application due to dependency issues")
