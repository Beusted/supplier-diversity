#!/usr/bin/env python3
"""
Run script for the Small Business PO Percentage Dashboard
Updated to use the FrontEnd-Overhaul-1.1 version
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
    
    # Run the main dashboard (cleaned up frontend)
    app_path = frontend_dir / "main_dashboard.py"
    
    print("📊 Starting Small Business PO Percentage Dashboard...")
    print(f"📁 Frontend directory: {frontend_dir}")
    print(f"📄 Main app file: {app_path}")
    print("🌐 The dashboard will open in your browser automatically")
    print("📋 Features:")
    print("   • Interactive PO percentage analysis")
    print("   • Real-time progress tracking toward 25% target")
    print("   • Supplier transition recommendations")
    print("   • Implementation roadmap and quick wins")
    print("🎯 Current: 16.3% → Target: 25% of POs to small businesses")
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
