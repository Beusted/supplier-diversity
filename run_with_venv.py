#!/usr/bin/env python3
"""
Run the Streamlit app using the virtual environment
"""

import subprocess
import sys
import os

def run_app():
    """Run the Streamlit app with virtual environment"""
    try:
        # Change to the project directory
        project_dir = "/Users/jorgeguzman/Documents/GitHub/supplier-diversity"
        os.chdir(project_dir)
        
        # Run streamlit with virtual environment
        cmd = [
            "bash", "-c", 
            "source streamlit_env/bin/activate && streamlit run streamlit_app.py --server.port 8501 --server.address localhost"
        ]
        
        print("🚀 Starting Diversity in Procurement Dashboard...")
        print("📍 The app will open in your browser at: http://localhost:8501")
        print("⏹️  Press Ctrl+C to stop the application")
        print("✅ Using virtual environment with compatible Streamlit version")
        
        subprocess.run(cmd, cwd=project_dir)
        
    except KeyboardInterrupt:
        print("\n👋 Application stopped by user")
    except Exception as e:
        print(f"❌ Error running application: {e}")

if __name__ == "__main__":
    run_app()
