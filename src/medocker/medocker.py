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
  medocker --configure               Run configuration tool
        """
    )
    
    parser.add_argument(
        '--web', 
        action='store_true',
        help='Launch the web interface'
    )
    
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
        logger.info("Launching Medocker web interface...")
        run_web_main()
    elif args.configure:
        logger.info("Running Medocker configuration tool...")
        run_configuration(args)
    else:
        parser.print_help()

if __name__ == "__main__":
    main() 