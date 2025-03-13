#!/usr/bin/env python3
"""
Medocker - Main CLI Entry Point

This script provides a unified interface for all Medocker commands.
"""

import sys
import argparse
from configure import run_configuration
from web import app
from run_web import run_web_server

__version__ = "0.1.0"

def print_banner():
    """Print the Medocker banner."""
    print(r"""
  __  __          _            _             
 |  \/  | ___  __| | ___   ___| | _____ _ __ 
 | |\/| |/ _ \/ _` |/ _ \ / __| |/ / _ \ '__|
 | |  | |  __/ (_| | (_) | (__|   <  __/ |   
 |_|  |_|\___|\__,_|\___/ \___|_|\_\___|_|   
                                             
 Clinic in a box by way of docker stack
 Version: {version}
""".format(version=__version__))


def main():
    """Main entry point for the Medocker CLI."""
    print_banner()
    
    parser = argparse.ArgumentParser(
        description='Medocker - A comprehensive Docker stack for medical practices',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    # Add version argument
    parser.add_argument('--version', action='version', version=f'Medocker {__version__}')
    
    # Create subparsers for different commands
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Configure command
    config_parser = subparsers.add_parser(
        'configure', 
        help='Configure the Medocker stack',
        description='Interactive configuration tool for Medocker'
    )
    config_parser.add_argument('--config', '-c', help='Path to configuration file', default='config/default.yml')
    config_parser.add_argument('--output', '-o', help='Path to output docker-compose file', default='docker-compose.yml')
    config_parser.add_argument('--interactive', '-i', action='store_true', help='Run in interactive mode')
    config_parser.add_argument('--save', '-s', help='Save configuration to file', default='config/custom.yml')
    config_parser.add_argument('--secure', '-S', action='store_true', help='Generate secure random passwords for all services')
    
    # Web command
    web_parser = subparsers.add_parser(
        'web', 
        help='Run the web interface',
        description='Web-based configuration interface for Medocker'
    )
    web_parser.add_argument('--host', help='Host to bind the server to', default='0.0.0.0')
    web_parser.add_argument('--port', '-p', type=int, help='Port to run the server on', default=5000)
    web_parser.add_argument('--debug', '-d', action='store_true', help='Run in debug mode')
    
    # Deploy command
    deploy_parser = subparsers.add_parser(
        'deploy', 
        help='Deploy the Medocker stack',
        description='Deploy the Docker stack with the configured services'
    )
    deploy_parser.add_argument('--config', '-c', help='Path to configuration file', default='config/custom.yml')
    deploy_parser.add_argument('--pull', action='store_true', help='Pull latest images before deploying')
    
    # Parse arguments
    args = parser.parse_args()
    
    # If no command is specified, print help
    if not args.command:
        parser.print_help()
        print("\nTry one of these commands to get started:")
        print("  configure  - Set up your Medocker stack")
        print("  web        - Launch the web interface (easier for beginners)")
        print("  deploy     - Deploy your configured Docker stack")
        print("\nExample: medocker configure --interactive")
        return 1
    
    # Handle commands
    if args.command == 'configure':
        return run_configuration(args)
    elif args.command == 'web':
        print(f"Starting web interface at http://{args.host}:{args.port}")
        print("Press Ctrl+C to stop the server")
        run_web_server(args.host, args.port, args.debug)
        return 0
    elif args.command == 'deploy':
        # This would run docker-compose up commands, but for now just print the command
        import os
        if not os.path.exists(args.config):
            print(f"Error: Configuration file {args.config} not found.")
            print("Run 'medocker configure --interactive' first to create a configuration.")
            return 1
            
        pull_command = "--pull always" if args.pull else ""
        print(f"Deploying Medocker stack using configuration from {args.config}")
        print(f"Command: docker-compose -f docker-compose.yml up -d {pull_command}")
        
        # Ask for confirmation
        confirm = input("Proceed with deployment? (y/n): ")
        if confirm.lower() != 'y':
            print("Deployment cancelled.")
            return 0
            
        print("\nFor now, please run this command manually:")
        print(f"  docker-compose -f docker-compose.yml up -d {pull_command}")
        return 0


if __name__ == '__main__':
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\nOperation cancelled by user")
        sys.exit(1) 