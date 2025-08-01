#!/usr/bin/env python3
"""
Railway startup script for the Small Business Supplier Diversity Dashboard
This script replicates the behavior of run_po_dashboard.py for Railway deployment
"""

import subprocess
import sys
import os
from pathlib import Path

def main():
    # Get the project root directory
    project_root = Path(__file__).parent
    frontend_dir = project_root / "frontend"
    
    # Change to frontend directory (important for relative imports)
    os.chdir(frontend_dir)
    
    # Get port from environment variable (Railway sets this)
    port = os.environ.get('PORT', '8501')
    
    # Run the main dashboard from frontend directory
    app_path = "main_dashboard.py"  # Relative path since we're in frontend dir
    
    print("🚀 Starting Small Business Supplier Diversity Dashboard on Railway...")
    print(f"📁 Working directory: {os.getcwd()}")
    print(f"📄 Main app file: {app_path}")
    print(f"🌐 Port: {port}")
    
    try:
        # Run streamlit with Railway-compatible settings
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", 
            app_path,
            "--server.port", port,
            "--server.address", "0.0.0.0",
            "--server.headless", "true",
            "--server.enableCORS", "false",
            "--server.enableXsrfProtection", "false"
        ], check=True)
    except Exception as e:
        print(f"❌ Error running dashboard: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
