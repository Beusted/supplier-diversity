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
    
    # Streamlit command with Railway-specific settings
    cmd = [
        'streamlit', 'run', 'streamlit_app.py',
        '--server.port', port,
        '--server.address', '0.0.0.0',
        '--server.headless', 'true',
        '--server.enableCORS', 'false',
        '--server.enableXsrfProtection', 'false',
        '--server.fileWatcherType', 'none',  # Disable file watcher for production
        '--browser.gatherUsageStats', 'false'  # Disable usage stats
    ]
    
    print(f"Starting Streamlit on port {port}")
    print(f"Command: {' '.join(cmd)}")
    
    # Start Streamlit
    try:
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error starting Streamlit: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
