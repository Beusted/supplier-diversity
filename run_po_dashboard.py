#!/usr/bin/env python3
"""
Run script for the Multi-Page Supplier Diversity Dashboard
"""

import subprocess
import sys
import os
from pathlib import Path

def main():
    # Get the project root directory
    project_root = Path(__file__).parent
    frontend_dir = project_root / "frontend"
    
    # Change to frontend directory
    os.chdir(frontend_dir)
    
    # Run the main dashboard (multi-page app)
    app_path = frontend_dir / "main_dashboard.py"
    
    print("📊 Starting Multi-Page Supplier Diversity Dashboard...")
    print(f"📁 Frontend directory: {frontend_dir}")
    print(f"📄 Main app file: {app_path}")
    print("🌐 The dashboard will open in your browser automatically")
    print("📋 Available pages:")
    print("   • Main Dashboard - Project overview and key metrics")
    print("   • Detailed Analysis - Deep dive into supplier matching")
    print("   • Implementation Guide - Step-by-step action plan")
    print("   • Data Sources - Technical methodology and architecture")
    print("🎯 Target: 25% of POs should go to small businesses")
    print("⏹️  Press Ctrl+C to stop the server")
    print("-" * 60)
    
    try:
        # Run streamlit with the main page
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", 
            str(app_path),
            "--server.port", "8503",
            "--server.address", "localhost"
        ], check=True)
    except KeyboardInterrupt:
        print("\n👋 Dashboard stopped by user")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error running dashboard: {e}")
        return 1
    except FileNotFoundError:
        print("❌ Streamlit not found. Please install it with: pip install streamlit")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
