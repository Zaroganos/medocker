#!/usr/bin/env python3
# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) 2024-2025 Iliya Yaroshevskiy
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

def main(host=None, port=None, debug=None):
    """Main entry point for the Medocker web interface."""
    
    # If arguments are provided programmatically, use them directly
    if host is not None and port is not None and debug is not None:
        # Use provided arguments directly
        final_host = host
        final_port = port
        final_debug = debug
    else:
        # Parse arguments from command line
        parser = argparse.ArgumentParser(
            description="Medocker Web Interface - Medical Practice Software Stack Manager",
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog="""
Examples:
  medocker --web --help                    Show this help message
  medocker --web --port 8080              Launch on port 8080
  medocker --web --host 127.0.0.1        Launch on localhost only
        """
        )
        
        parser.add_argument(
            '--host',
            default=host or '0.0.0.0',
            help='Host to bind the web server to (default: 0.0.0.0)'
        )
        
        parser.add_argument(
            '--port',
            type=int,
            default=port or 9876,
            help='Port to bind the web server to (default: 9876)'
        )
        
        parser.add_argument(
            '--debug',
            action='store_true',
            default=debug or False,
            help='Run in debug mode'
        )
        
        parser.add_argument(
            '--version',
            action='version',
            version='%(prog)s 0.1.0'
        )
        
        args = parser.parse_args()
        
        # Use the parsed arguments
        final_host = args.host
        final_port = args.port
        final_debug = args.debug
    
    # Then import the web module
    try:
        # Try relative import first (within the same package)
        from .web import app, main as web_main
    except ImportError as e:
        # Try an alternative import path
        try:
            from .web import app, main as web_main
        except ImportError:
            # Try to patch the specific modules before importing again
            import sys
            import types
            
            # Create a mock module for src
            src_module = types.ModuleType('src')
            sys.modules['src'] = src_module
            
            # Now try importing again with both possible paths
            try:
                from .web import app, main as web_main
            except ImportError:
                from .web import app, main as web_main
            except ImportError as e2:
                print(f"Failed to import web module: {e2}")
                return 1
    
    # Launch the web interface
    print(f"Starting Medocker web interface on {final_host}:{final_port}")
    
    if not final_debug:
        # Open browser automatically
        def open_browser():
            time.sleep(1.5)  # Wait for server to start
            url = f"http://{final_host if final_host != '0.0.0.0' else 'localhost'}:{final_port}"
            webbrowser.open(url)
        
        threading.Thread(target=open_browser, daemon=True).start()
    
    # Run the web server
    web_main(host=final_host, port=final_port, debug=final_debug)
    
    return 0

if __name__ == "__main__":
    sys.exit(main()) 