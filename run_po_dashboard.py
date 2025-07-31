#!/usr/bin/env python3
"""
Run script for the PO Quantity Small Business Dashboard
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
    
    # Run the PO quantity focused dashboard
    app_path = "po_quantity_dashboard.py"
    
    print("📋 Starting Small Business PO Percentage Dashboard...")
    print(f"📁 Frontend directory: {frontend_dir}")
    print(f"📄 App file: {app_path}")
    print("🌐 The dashboard will open in your browser automatically")
    print("📊 Focus: Percentage of Purchase Orders (POs) going to small businesses")
    print("🎯 Target: 25% of POs should go to small businesses")
    print("⏹️  Press Ctrl+C to stop the server")
    print("-" * 60)
    
    try:
        # Run streamlit
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", 
            str(app_path),
            "--server.port", "8503",  # Different port to avoid conflicts
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
