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


def main():
    """Main entry point for the Medocker CLI."""
    parser = argparse.ArgumentParser(
        description='Medocker - A comprehensive Docker stack for medical practices',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    # Create subparsers for different commands
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Configure command
    config_parser = subparsers.add_parser('configure', help='Configure the Medocker stack')
    config_parser.add_argument('--config', '-c', help='Path to configuration file', default='config/default.yml')
    config_parser.add_argument('--output', '-o', help='Path to output docker-compose file', default='docker-compose.yml')
    config_parser.add_argument('--interactive', '-i', action='store_true', help='Run in interactive mode')
    config_parser.add_argument('--save', '-s', help='Save configuration to file', default='config/custom.yml')
    config_parser.add_argument('--secure', '-S', action='store_true', help='Generate secure random passwords for all services')
    
    # Web command
    web_parser = subparsers.add_parser('web', help='Run the web interface')
    web_parser.add_argument('--host', help='Host to bind the server to', default='0.0.0.0')
    web_parser.add_argument('--port', '-p', type=int, help='Port to run the server on', default=5000)
    web_parser.add_argument('--debug', '-d', action='store_true', help='Run in debug mode')
    
    # Deploy command
    deploy_parser = subparsers.add_parser('deploy', help='Deploy the Medocker stack')
    deploy_parser.add_argument('--config', '-c', help='Path to configuration file', default='config/custom.yml')
    deploy_parser.add_argument('--pull', action='store_true', help='Pull latest images before deploying')
    
    # Parse arguments
    args = parser.parse_args()
    
    # Handle commands
    if args.command == 'configure':
        return run_configuration(args)
    elif args.command == 'web':
        run_web_server(args.host, args.port, args.debug)
        return 0
    elif args.command == 'deploy':
        # This would run docker-compose up commands, but for now just print the command
        import os
        if not os.path.exists(args.config):
            print(f"Error: Configuration file {args.config} not found.")
            return 1
            
        pull_command = "--pull always" if args.pull else ""
        print(f"Would run: docker-compose -f docker-compose.yml up -d {pull_command}")
        print("For now, please run this command manually:")
        print(f"  docker-compose -f docker-compose.yml up -d {pull_command}")
        return 0
    else:
        # If no command is specified, print help
        parser.print_help()
        return 1


if __name__ == '__main__':
    sys.exit(main()) 