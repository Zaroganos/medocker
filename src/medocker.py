#!/usr/bin/env python3
"""
Medocker CLI - the unified interface for Medocker commands.
Acts as the main entry point for all Medocker functionality.
"""

import os
import sys
import argparse
import subprocess
import logging

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger('medocker')

# Import Medocker modules
try:
    # Try direct imports first
    from src.configure import run_configuration
    from src.web import app
    from src.run_web import run_web_server
except ImportError:
    # Fall back to relative imports
    from .configure import run_configuration
    from .web import app
    from .run_web import run_web_server

__version__ = "0.1.0"

def print_banner():
    """Print a banner for the Medocker CLI"""
    print("""
  __  __          _            _             
 |  \/  | ___  __| | ___   ___| | _____ _ __ 
 | |\/| |/ _ \/ _` |/ _ \ / __| |/ / _ \ '__|
 | |  | |  __/ (_| | (_) | (__|   <  __/ |   
 |_|  |_|\___|\__,_|\___/ \___|_|\_\___|_|   
                                             
 The Docker-based Medical Office System
 Version: {version}
    """.format(version=__version__))

def main():
    """Main entry point for the Medocker CLI"""
    parser = argparse.ArgumentParser(description='Medocker: The Docker-based Medical Office System')
    parser.add_argument('--version', action='version', version=f'Medocker {__version__}')
    
    subparsers = parser.add_subparsers(dest='command', help='Command to run')
    
    # Configure command
    configure_parser = subparsers.add_parser('configure', help='Configure the Medocker stack')
    configure_parser.add_argument('--config', help='Path to the configuration file', default='config/medocker.yaml')
    configure_parser.add_argument('--output', help='Path to save the generated docker-compose file', default='docker-compose.yml')
    configure_parser.add_argument('--interactive', action='store_true', help='Run in interactive mode')
    configure_parser.add_argument('--secure', action='store_true', help='Generate secure random passwords')
    
    # Web interface command
    web_parser = subparsers.add_parser('web', help='Start the web interface')
    web_parser.add_argument('--host', help='Host to bind the web server to', default='0.0.0.0')
    web_parser.add_argument('--port', type=int, help='Port to bind the web server to', default=9876)
    web_parser.add_argument('--debug', action='store_true', help='Run in debug mode')
    
    # Deploy command
    deploy_parser = subparsers.add_parser('deploy', help='Deploy the Docker stack')
    deploy_parser.add_argument('--config', help='Path to the configuration file', default='docker-compose.yml')
    deploy_parser.add_argument('--force', action='store_true', help='Force deployment without confirmation')
    
    args = parser.parse_args()
    
    # Print banner
    print_banner()
    
    # If no command is specified, default to launching the web UI
    if args.command is None:
        print("No command specified. Launching web interface...")
        print("Use 'medocker --help' for other available commands.")
        return run_web_server(host='0.0.0.0', port=9876, debug=False)
    
    if args.command == 'configure':
        return run_configuration(args)
    
    if args.command == 'web':
        return run_web_server(host=args.host, port=args.port, debug=args.debug)
    
    if args.command == 'deploy':
        # Check if the config file exists
        if not os.path.exists(args.config):
            logger.error(f"Configuration file {args.config} not found. Run 'medocker configure' first.")
            return 1
        
        # Confirm deployment
        if not args.force:
            confirm = input("Are you sure you want to deploy the Docker stack? [y/N] ")
            if confirm.lower() not in ['y', 'yes']:
                logger.info("Deployment cancelled.")
                return 0
        
        # Run docker-compose command
        try:
            cmd = ['docker-compose', '-f', args.config, 'up', '-d']
            logger.info(f"Running command: {' '.join(cmd)}")
            subprocess.run(cmd, check=True)
            logger.info("Docker stack deployed successfully.")
            return 0
        except subprocess.CalledProcessError as e:
            logger.error(f"Error deploying Docker stack: {e}")
            return 1
    
    logger.error(f"Unknown command: {args.command}")
    return 1

if __name__ == '__main__':
    sys.exit(main()) 