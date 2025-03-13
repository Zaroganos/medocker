#!/usr/bin/env python3
"""
Medocker Web UI Launcher

This script launches the Medocker web configuration interface.
"""

import os
import sys
import argparse
import webbrowser
import threading
import time
from web import app, main as web_main

def open_browser(url, delay=1.0):
    """Open a web browser after a short delay to allow the server to start."""
    def _open_browser():
        time.sleep(delay)
        webbrowser.open(url)
    
    browser_thread = threading.Thread(target=_open_browser)
    browser_thread.daemon = True
    browser_thread.start()

def run_web_server(host='0.0.0.0', port=5000, debug=False):
    """Run the web server with the specified options."""
    if debug:
        os.environ['FLASK_ENV'] = 'development'
    
    # Calculate the URL to open
    # Use localhost instead of 0.0.0.0 for the browser
    browser_host = 'localhost' if host == '0.0.0.0' else host
    url = f"http://{browser_host}:{port}"
    
    try:
        print(f"Starting Medocker Web UI at {url}")
        print("Opening web browser automatically...")
        
        # Open browser in a separate thread to not block server startup
        open_browser(url)
        
        if debug:
            app.run(host=host, port=port, debug=True)
        else:
            web_main()
    except KeyboardInterrupt:
        print("Server terminated by user")
        sys.exit(0)
    except Exception as e:
        print(f"Error starting server: {e}")
        sys.exit(1)

def main():
    """Main entry point for the Poetry script."""
    parser = argparse.ArgumentParser(description='Medocker Web UI')
    parser.add_argument('--host', help='Host to bind the server to', default='0.0.0.0')
    parser.add_argument('--port', '-p', type=int, help='Port to run the server on', default=5000)
    parser.add_argument('--debug', '-d', action='store_true', help='Run in debug mode')
    
    args = parser.parse_args()
    run_web_server(args.host, args.port, args.debug)

if __name__ == '__main__':
    main() 