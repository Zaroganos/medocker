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
import platform

# Add the parent directory to sys.path if needed
script_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(script_dir)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

# Add some platform-specific handling for Windows
is_windows = platform.system() == "Windows" or sys.platform == "win32"

# Then import the web module
try:
    from src.web import app, main as web_main
except ImportError as e:
    # Try an alternative import path
    try:
        from web import app, main as web_main
    except ImportError:
        if is_windows and "fcntl" in str(e):
            print("Notice: Some Unix-specific modules are not available on Windows.")
            print("We will use alternative implementations for Windows compatibility.")
            print("All core features should still work.")
            
            # Try to patch the specific modules before importing again
            try:
                # Create a mock fcntl module for Windows
                import types
                fcntl_mock = types.ModuleType('fcntl')
                fcntl_mock.LOCK_EX = 1
                fcntl_mock.LOCK_NB = 2
                fcntl_mock.LOCK_UN = 4
                
                def fcntl_mock_flock(fd, operation):
                    # This is a no-op on Windows
                    pass
                    
                fcntl_mock.flock = fcntl_mock_flock
                sys.modules['fcntl'] = fcntl_mock
                
                # Now try importing again with both possible paths
                try:
                    from src.web import app, main as web_main
                except ImportError:
                    from web import app, main as web_main
            except ImportError as e2:
                print(f"Error: Could not initialize the web interface: {e2}")
                sys.exit(1)
        else:
            print(f"Error: {e}")
            sys.exit(1)

def open_browser(url, delay=1.0):
    """Open a web browser after a short delay to allow the server to start."""
    def _open_browser():
        time.sleep(delay)
        webbrowser.open(url)
    
    browser_thread = threading.Thread(target=_open_browser)
    browser_thread.daemon = True
    browser_thread.start()

def run_web_server(host='0.0.0.0', port=9876, debug=False):
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
    parser.add_argument('--port', '-p', type=int, help='Port to run the server on', default=9876)
    parser.add_argument('--debug', '-d', action='store_true', help='Run in debug mode')
    
    args = parser.parse_args()
    run_web_server(args.host, args.port, args.debug)

if __name__ == '__main__':
    main() 