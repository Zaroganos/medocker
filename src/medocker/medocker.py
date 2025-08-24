#!/usr/bin/env python3
# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) 2024-2025 Iliya Yaroshevskiy
"""
Medocker - A comprehensive Docker packaging system for medical practice software.
"""

import os
import sys
import argparse
import subprocess
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Import Medocker modules
try:
    # Try relative imports first
    from .configure import run_configuration
    from .web import app
    from .run_web import main as run_web_main
except ImportError:
    # Fall back to relative imports
    from .configure import run_configuration
    from .web import app
    from .run_web import main as run_web_main

def main():
    """Main entry point for the Medocker CLI."""
    parser = argparse.ArgumentParser(
        description="Medocker - Medical Practice Software Stack Manager",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  medocker --help                    Show this help message
  medocker --web                     Launch the web interface
  medocker --web --port 8080        Launch web interface on port 8080
  medocker --web --host 127.0.0.1   Launch web interface on localhost only
  medocker --web --debug             Launch web interface in debug mode
  medocker --configure               Run configuration tool
        """
    )
    
    # Web interface arguments
    parser.add_argument(
        '--web', 
        action='store_true',
        help='Launch the web interface'
    )
    
    parser.add_argument(
        '--host',
        default='0.0.0.0',
        help='Host to bind the web server to (default: 0.0.0.0)'
    )
    
    parser.add_argument(
        '--port',
        type=int,
        default=9876,
        help='Port to bind the web server to (default: 9876)'
    )
    
    parser.add_argument(
        '--debug',
        action='store_true',
        help='Run in debug mode'
    )
    
    # Configuration tool argument
    parser.add_argument(
        '--configure', 
        action='store_true',
        help='Run the configuration tool'
    )
    
    parser.add_argument(
        '--version',
        action='version',
        version='%(prog)s 0.1.0'
    )
    
    args = parser.parse_args()
    
    if args.web:
        logger.info(f"Launching Medocker web interface on {args.host}:{args.port}")
        # Pass the arguments to the web interface
        run_web_main(host=args.host, port=args.port, debug=args.debug)
    elif args.configure:
        logger.info("Running Medocker configuration tool...")
        run_configuration(args)
    else:
        parser.print_help()

if __name__ == "__main__":
    main() 