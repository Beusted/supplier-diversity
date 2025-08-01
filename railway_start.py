#!/usr/bin/env python3
"""
Railway-specific startup script for Streamlit app
"""
import os
import subprocess
import sys

def main():
    # Get port from environment or default to 8080
    port = os.environ.get('PORT', '8080')
    
    print(f"🚂 Railway Startup Script")
    print(f"📍 Port from environment: {port}")
    print(f"🌍 All environment variables: {dict(os.environ)}")
    
    # Validate port is a number
    try:
        port_int = int(port)
        print(f"✅ Port validated: {port_int}")
    except ValueError:
        print(f"❌ Invalid port '{port}', using default 8080")
        port = '8080'
    
    # Streamlit command with Railway-specific settings - using original dashboard
    cmd = [
        'streamlit', 'run', 'frontend/main_dashboard.py',
        '--server.port', str(port),  # Ensure port is string
        '--server.address', '0.0.0.0',
        '--server.headless', 'true',
        '--server.enableCORS', 'false',
        '--server.enableXsrfProtection', 'false',
        '--server.fileWatcherType', 'none',  # Disable file watcher for production
        '--browser.gatherUsageStats', 'false'  # Disable usage stats
    ]
    
    print(f"🚀 Starting Streamlit on port {port}")
    print(f"📄 Using dashboard: frontend/main_dashboard.py")
    print(f"💻 Command: {' '.join(cmd)}")
    
    # Start Streamlit
    try:
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ Error starting Streamlit: {e}")
        sys.exit(1)
    except FileNotFoundError as e:
        print(f"❌ Streamlit not found: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
