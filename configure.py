#!/usr/bin/env python3
"""
Medocker Configuration Tool

This script generates docker-compose files and other configuration based on the
user's selections in the config directory.
"""

import os
import sys
import yaml
import shutil
import argparse
from pathlib import Path


def load_config(config_file='config/default.yml'):
    """Load the configuration from the specified YAML file."""
    try:
        with open(config_file, 'r') as f:
            return yaml.safe_load(f)
    except Exception as e:
        print(f"Error loading configuration file {config_file}: {e}")
        sys.exit(1)


def save_config(config, config_file='config/custom.yml'):
    """Save the configuration to a YAML file."""
    os.makedirs(os.path.dirname(config_file), exist_ok=True)
    try:
        with open(config_file, 'w') as f:
            yaml.dump(config, f, default_flow_style=False)
        print(f"Configuration saved to {config_file}")
    except Exception as e:
        print(f"Error saving configuration file {config_file}: {e}")
        sys.exit(1)


def interactive_configuration(config):
    """Allow the user to interactively configure the Medocker stack."""
    print("Medocker Interactive Configuration")
    print("=================================")
    
    # System Configuration
    print("\nSystem Configuration:")
    config['system']['domain'] = input(f"Domain name [{config['system']['domain']}]: ") or config['system']['domain']
    ssl_input = input(f"Enable SSL (true/false) [{config['system']['ssl_enabled']}]: ") or str(config['system']['ssl_enabled']).lower()
    config['system']['ssl_enabled'] = ssl_input.lower() == 'true'
    config['system']['admin_email'] = input(f"Admin email [{config['system']['admin_email']}]: ") or config['system']['admin_email']
    config['system']['timezone'] = input(f"Timezone [{config['system']['timezone']}]: ") or config['system']['timezone']
    config['system']['data_directory'] = input(f"Data directory [{config['system']['data_directory']}]: ") or config['system']['data_directory']
    
    # Core Components
    print("\nCore Components:")
    
    # OpenEMR
    openemr_enabled = input(f"Enable OpenEMR (true/false) [{config['components']['openemr']['enabled']}]: ") or str(config['components']['openemr']['enabled']).lower()
    config['components']['openemr']['enabled'] = openemr_enabled.lower() == 'true'
    
    if config['components']['openemr']['enabled']:
        config['components']['openemr']['version'] = input(f"OpenEMR version [{config['components']['openemr']['version']}]: ") or config['components']['openemr']['version']
        config['components']['openemr']['port'] = input(f"OpenEMR port [{config['components']['openemr']['port']}]: ") or config['components']['openemr']['port']
    
    # Nextcloud
    nextcloud_enabled = input(f"Enable Nextcloud (true/false) [{config['components']['nextcloud']['enabled']}]: ") or str(config['components']['nextcloud']['enabled']).lower()
    config['components']['nextcloud']['enabled'] = nextcloud_enabled.lower() == 'true'
    
    if config['components']['nextcloud']['enabled']:
        config['components']['nextcloud']['version'] = input(f"Nextcloud version [{config['components']['nextcloud']['version']}]: ") or config['components']['nextcloud']['version']
        config['components']['nextcloud']['port'] = input(f"Nextcloud port [{config['components']['nextcloud']['port']}]: ") or config['components']['nextcloud']['port']
    
    # Database
    mariadb_enabled = input(f"Enable MariaDB (true/false) [{config['databases']['mariadb']['enabled']}]: ") or str(config['databases']['mariadb']['enabled']).lower()
    config['databases']['mariadb']['enabled'] = mariadb_enabled.lower() == 'true'
    
    if config['databases']['mariadb']['enabled']:
        config['databases']['mariadb']['root_password'] = input(f"MariaDB root password (leave blank to keep current): ") or config['databases']['mariadb']['root_password']
    
    # Additional Services
    print("\nAdditional Services:")
    print("The following additional services are available. Type 'true' to enable, 'false' to disable.")
    
    for category, services in config['additional_services'].items():
        if isinstance(services, dict):
            service_enabled = input(f"Enable {category} (true/false) [{services['enabled']}]: ") or str(services['enabled']).lower()
            config['additional_services'][category]['enabled'] = service_enabled.lower() == 'true'
    
    return config


def generate_docker_compose(config, output_file='docker-compose.yml'):
    """Generate a docker-compose.yml file based on the configuration."""
    compose = {
        'version': '3.8',
        'services': {},
        'networks': {
            'medocker_network': {
                'driver': 'bridge'
            }
        },
        'volumes': {}
    }
    
    # Add MariaDB if enabled
    if config['databases']['mariadb']['enabled']:
        compose['services']['mariadb'] = {
            'image': f"mariadb:{config['databases']['mariadb']['version']}",
            'restart': 'unless-stopped',
            'environment': {
                'MYSQL_ROOT_PASSWORD': config['databases']['mariadb']['root_password'],
            },
            'volumes': [
                './data/mariadb:/var/lib/mysql'
            ],
            'networks': [
                'medocker_network'
            ]
        }
        compose['volumes']['mariadb_data'] = {'driver': 'local'}
    
    # Add OpenEMR if enabled
    if config['components']['openemr']['enabled']:
        compose['services']['openemr'] = {
            'image': f"openemr/openemr:{config['components']['openemr']['version']}",
            'restart': 'unless-stopped',
            'ports': [
                f"{config['components']['openemr']['port']}:80"
            ],
            'volumes': [
                './data/openemr/sites:/var/www/localhost/htdocs/openemr/sites',
                './data/openemr/logs:/var/log/apache2'
            ],
            'environment': {
                'MYSQL_HOST': config['components']['openemr']['db_host'],
                'MYSQL_ROOT_PASS': config['databases']['mariadb']['root_password'],
                'MYSQL_USER': config['components']['openemr']['db_user'],
                'MYSQL_PASS': config['components']['openemr']['db_pass'],
                'MYSQL_DATABASE': config['components']['openemr']['db_name'],
                'OE_USER': 'admin',
                'OE_PASS': 'pass'
            },
            'networks': [
                'medocker_network'
            ],
            'depends_on': [
                'mariadb'
            ]
        }
        compose['volumes']['openemr_sites'] = {'driver': 'local'}
        compose['volumes']['openemr_logs'] = {'driver': 'local'}
    
    # Add Nextcloud if enabled
    if config['components']['nextcloud']['enabled']:
        compose['services']['nextcloud'] = {
            'image': f"nextcloud:{config['components']['nextcloud']['version']}",
            'restart': 'unless-stopped',
            'ports': [
                f"{config['components']['nextcloud']['port']}:80"
            ],
            'volumes': [
                './data/nextcloud:/var/www/html'
            ],
            'environment': {
                'MYSQL_HOST': config['components']['nextcloud']['db_host'],
                'MYSQL_DATABASE': config['components']['nextcloud']['db_name'],
                'MYSQL_USER': config['components']['nextcloud']['db_user'],
                'MYSQL_PASSWORD': config['components']['nextcloud']['db_pass'],
                'NEXTCLOUD_ADMIN_USER': 'admin',
                'NEXTCLOUD_ADMIN_PASSWORD': 'admin',
                'NEXTCLOUD_TRUSTED_DOMAINS': config['system']['domain']
            },
            'networks': [
                'medocker_network'
            ],
            'depends_on': [
                'mariadb'
            ]
        }
        compose['volumes']['nextcloud_data'] = {'driver': 'local'}
    
    # Add Portainer if enabled
    if config['additional_services']['portainer']['enabled']:
        compose['services']['portainer'] = {
            'image': f"portainer/portainer-ce:{config['additional_services']['portainer']['version']}",
            'restart': 'unless-stopped',
            'ports': [
                f"{config['additional_services']['portainer']['port']}:9443"
            ],
            'volumes': [
                './data/portainer:/data',
                '/var/run/docker.sock:/var/run/docker.sock'
            ],
            'networks': [
                'medocker_network'
            ]
        }
        compose['volumes']['portainer_data'] = {'driver': 'local'}
    
    # Add additional services as needed
    # This is just a starting point - you would add more service definitions
    # based on which are enabled in the configuration
    
    try:
        with open(output_file, 'w') as f:
            yaml.dump(compose, f, default_flow_style=False)
        print(f"Docker Compose file generated: {output_file}")
    except Exception as e:
        print(f"Error generating Docker Compose file: {e}")
        sys.exit(1)


def create_directories(config):
    """Create necessary directories based on the configuration."""
    base_dir = Path(config['system']['data_directory'])
    if not base_dir.is_absolute():
        base_dir = Path('./data')
    
    # Create base directory
    os.makedirs(base_dir, exist_ok=True)
    
    # Create directories for enabled services
    if config['components']['openemr']['enabled']:
        os.makedirs(base_dir / 'openemr' / 'sites', exist_ok=True)
        os.makedirs(base_dir / 'openemr' / 'logs', exist_ok=True)
    
    if config['components']['nextcloud']['enabled']:
        os.makedirs(base_dir / 'nextcloud', exist_ok=True)
    
    if config['databases']['mariadb']['enabled']:
        os.makedirs(base_dir / 'mariadb', exist_ok=True)
    
    if config['additional_services']['portainer']['enabled']:
        os.makedirs(base_dir / 'portainer', exist_ok=True)
    
    # Create directories for additional enabled services
    for service, settings in config['additional_services'].items():
        if isinstance(settings, dict) and settings.get('enabled', False):
            os.makedirs(base_dir / service, exist_ok=True)
    
    print(f"Created directories in {base_dir}")


def main():
    """Main entry point for the Medocker configuration tool."""
    parser = argparse.ArgumentParser(description='Medocker Configuration Tool')
    parser.add_argument('--config', '-c', help='Path to configuration file', default='config/default.yml')
    parser.add_argument('--output', '-o', help='Path to output docker-compose file', default='docker-compose.yml')
    parser.add_argument('--interactive', '-i', action='store_true', help='Run in interactive mode')
    parser.add_argument('--save', '-s', help='Save configuration to file', default='config/custom.yml')
    
    args = parser.parse_args()
    
    # Load configuration
    config = load_config(args.config)
    
    # Run interactive configuration if requested
    if args.interactive:
        config = interactive_configuration(config)
        save_config(config, args.save)
    
    # Generate docker-compose file
    generate_docker_compose(config, args.output)
    
    # Create directories
    create_directories(config)
    
    print("\nMedocker configuration completed!")
    print(f"Run 'docker-compose up -d' to start the stack.")


if __name__ == '__main__':
    main() 