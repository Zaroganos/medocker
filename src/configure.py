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
import secrets
import string
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


def generate_password(length=20):
    """Generate a secure random password."""
    alphabet = string.ascii_letters + string.digits
    return ''.join(secrets.choice(alphabet) for _ in range(length))


def resolve_variable_references(config):
    """Resolve variable references in the configuration like ${system.admin_email}."""
    def _resolve_ref(value, config):
        if not isinstance(value, str):
            return value
        
        if value.startswith('${') and value.endswith('}'):
            ref_path = value[2:-1].split('.')
            ref_value = config
            for key in ref_path:
                if key in ref_value:
                    ref_value = ref_value[key]
                else:
                    # Reference not found, return original value
                    return value
            return ref_value
        return value
    
    # Process the entire config recursively
    def _process_dict(d, config):
        for key, value in d.items():
            if isinstance(value, dict):
                _process_dict(value, config)
            elif isinstance(value, list):
                for i, item in enumerate(value):
                    if isinstance(item, dict):
                        _process_dict(item, config)
                    else:
                        value[i] = _resolve_ref(item, config)
            else:
                d[key] = _resolve_ref(value, config)
        return d
    
    return _process_dict(config, config)


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
    
    # Infrastructure Services
    print("\nInfrastructure Services:")
    
    # Traefik
    traefik_enabled = input(f"Enable Traefik reverse proxy (true/false) [{config['infrastructure']['traefik']['enabled']}]: ") or str(config['infrastructure']['traefik']['enabled']).lower()
    config['infrastructure']['traefik']['enabled'] = traefik_enabled.lower() == 'true'
    
    if config['infrastructure']['traefik']['enabled']:
        config['infrastructure']['traefik']['http_port'] = input(f"Traefik HTTP port [{config['infrastructure']['traefik']['http_port']}]: ") or config['infrastructure']['traefik']['http_port']
        config['infrastructure']['traefik']['https_port'] = input(f"Traefik HTTPS port [{config['infrastructure']['traefik']['https_port']}]: ") or config['infrastructure']['traefik']['https_port']
        config['infrastructure']['traefik']['dashboard_port'] = input(f"Traefik dashboard port [{config['infrastructure']['traefik']['dashboard_port']}]: ") or config['infrastructure']['traefik']['dashboard_port']
    
    # Keycloak
    keycloak_enabled = input(f"Enable Keycloak identity provider (true/false) [{config['infrastructure']['keycloak']['enabled']}]: ") or str(config['infrastructure']['keycloak']['enabled']).lower()
    config['infrastructure']['keycloak']['enabled'] = keycloak_enabled.lower() == 'true'
    
    if config['infrastructure']['keycloak']['enabled']:
        # Generate secure default passwords if none are set
        if config['infrastructure']['keycloak']['admin_password'] == "change-me-please":
            admin_password = input("Keycloak admin password (leave blank to generate): ")
            if not admin_password:
                admin_password = generate_password(16)
                print(f"Generated Keycloak admin password: {admin_password}")
            config['infrastructure']['keycloak']['admin_password'] = admin_password
    
    # PostgreSQL (required for Keycloak and Vaultwarden)
    if config['infrastructure']['keycloak']['enabled'] or config['components']['vaultwarden']['enabled']:
        config['databases']['postgres']['enabled'] = True
        
        # Generate secure password for PostgreSQL if default is still used
        if config['databases']['postgres']['root_password'] == "postgres_password":
            config['databases']['postgres']['root_password'] = generate_password(16)
            print("Generated secure PostgreSQL root password")
        
        if config['databases']['postgres']['keycloak_password'] == "keycloak_password":
            config['databases']['postgres']['keycloak_password'] = generate_password(16)
            print("Generated secure PostgreSQL Keycloak user password")
            
        if config['databases']['postgres']['vaultwarden_password'] == "vaultwarden_password":
            config['databases']['postgres']['vaultwarden_password'] = generate_password(16)
            print("Generated secure PostgreSQL Vaultwarden user password")
    
    # Core Components
    print("\nCore Components:")
    
    # OpenEMR
    openemr_enabled = input(f"Enable OpenEMR (true/false) [{config['components']['openemr']['enabled']}]: ") or str(config['components']['openemr']['enabled']).lower()
    config['components']['openemr']['enabled'] = openemr_enabled.lower() == 'true'
    
    if config['components']['openemr']['enabled']:
        config['components']['openemr']['version'] = input(f"OpenEMR version [{config['components']['openemr']['version']}]: ") or config['components']['openemr']['version']
        
        # If Traefik is enabled, we use domain routing instead of port
        if not config['infrastructure']['traefik']['enabled']:
            config['components']['openemr']['port'] = input(f"OpenEMR port [{config['components']['openemr']['port']}]: ") or config['components']['openemr']['port']
    
    # Nextcloud
    nextcloud_enabled = input(f"Enable Nextcloud (true/false) [{config['components']['nextcloud']['enabled']}]: ") or str(config['components']['nextcloud']['enabled']).lower()
    config['components']['nextcloud']['enabled'] = nextcloud_enabled.lower() == 'true'
    
    if config['components']['nextcloud']['enabled']:
        config['components']['nextcloud']['version'] = input(f"Nextcloud version [{config['components']['nextcloud']['version']}]: ") or config['components']['nextcloud']['version']
        
        # If Traefik is enabled, we use domain routing instead of port
        if not config['infrastructure']['traefik']['enabled']:
            config['components']['nextcloud']['port'] = input(f"Nextcloud port [{config['components']['nextcloud']['port']}]: ") or config['components']['nextcloud']['port']
    
    # Vaultwarden (Password Manager)
    vaultwarden_enabled = input(f"Enable Vaultwarden password manager (true/false) [{config['components']['vaultwarden']['enabled']}]: ") or str(config['components']['vaultwarden']['enabled']).lower()
    config['components']['vaultwarden']['enabled'] = vaultwarden_enabled.lower() == 'true'
    
    if config['components']['vaultwarden']['enabled']:
        config['components']['vaultwarden']['version'] = input(f"Vaultwarden version [{config['components']['vaultwarden']['version']}]: ") or config['components']['vaultwarden']['version']
        
        # If Traefik is enabled, we use domain routing instead of port
        if not config['infrastructure']['traefik']['enabled']:
            config['components']['vaultwarden']['port'] = input(f"Vaultwarden port [{config['components']['vaultwarden']['port']}]: ") or config['components']['vaultwarden']['port']
        
        # Generate secure admin token if default is still used
        if config['components']['vaultwarden']['admin_token'] == "change-me-please":
            admin_token = input("Vaultwarden admin token (leave blank to generate): ")
            if not admin_token:
                admin_token = generate_password(40)
                print(f"Generated Vaultwarden admin token: {admin_token}")
            config['components']['vaultwarden']['admin_token'] = admin_token
            
        # Configure SSO with Keycloak if both are enabled
        if config['infrastructure']['keycloak']['enabled']:
            sso_enabled = input("Enable Keycloak SSO for Vaultwarden? (true/false) [true]: ") or "true"
            config['components']['vaultwarden']['sso_enabled'] = sso_enabled.lower() == 'true'
            if config['components']['vaultwarden']['sso_enabled']:
                print("Vaultwarden will be configured to use Keycloak for Single Sign-On")
    
    # Database
    mariadb_enabled = input(f"Enable MariaDB (true/false) [{config['databases']['mariadb']['enabled']}]: ") or str(config['databases']['mariadb']['enabled']).lower()
    config['databases']['mariadb']['enabled'] = mariadb_enabled.lower() == 'true'
    
    if config['databases']['mariadb']['enabled']:
        # Generate secure password for MariaDB if default is still used
        if config['databases']['mariadb']['root_password'] == "root_password":
            use_default = input("MariaDB is using the default root password. Generate a secure password? (yes/no): ").lower()
            if use_default == 'yes':
                config['databases']['mariadb']['root_password'] = generate_password(16)
                print(f"Generated secure MariaDB root password: {config['databases']['mariadb']['root_password']}")
                print("Make sure to save this password securely!")
    
    # Additional Services
    print("\nAdditional Services:")
    print("The following additional services are available. Type 'true' to enable, 'false' to disable.")
    
    for category, services in config['additional_services'].items():
        if isinstance(services, dict):
            service_enabled = input(f"Enable {category} (true/false) [{services['enabled']}]: ") or str(services['enabled']).lower()
            config['additional_services'][category]['enabled'] = service_enabled.lower() == 'true'
    
    # Resolve any variable references
    config = resolve_variable_references(config)
    
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
    
    # Add Traefik if enabled
    if config['infrastructure']['traefik']['enabled']:
        traefik_labels = [
            'traefik.enable=true',
            'traefik.http.routers.traefik.rule=Host(`traefik.' + config['system']['domain'] + '`)',
            'traefik.http.routers.traefik.service=api@internal',
            'traefik.http.routers.traefik.entrypoints=websecure',
            'traefik.http.routers.traefik.tls=true',
            'traefik.http.routers.traefik.middlewares=traefik-auth'
        ]
        
        # Add basic auth middleware if Keycloak is not enabled
        if not config['infrastructure']['keycloak']['enabled']:
            # Using a default admin/password for demo purposes - should be changed in production
            traefik_labels.extend([
                'traefik.http.middlewares.traefik-auth.basicauth.users=admin:$$apr1$$JY5M3OsG$$vKDvGPGAM8TO9el64HSVl1' # admin:password
            ])
        
        compose['services']['traefik'] = {
            'image': f"traefik:{config['infrastructure']['traefik']['version']}",
            'restart': 'unless-stopped',
            'ports': [
                f"{config['infrastructure']['traefik']['http_port']}:80",
                f"{config['infrastructure']['traefik']['https_port']}:443",
                f"{config['infrastructure']['traefik']['dashboard_port']}:8080"
            ],
            'volumes': [
                '/var/run/docker.sock:/var/run/docker.sock:ro',
                './data/traefik/acme.json:/acme.json',
                './data/traefik/config:/etc/traefik/config'
            ],
            'command': [
                '--api.dashboard=true',
                '--providers.docker=true',
                '--providers.docker.exposedByDefault=false',
                '--entrypoints.web.address=:80',
                '--entrypoints.websecure.address=:443',
                '--certificatesresolvers.myresolver.acme.email=' + config['system']['admin_email'],
                '--certificatesresolvers.myresolver.acme.storage=/acme.json',
                '--certificatesresolvers.myresolver.acme.tlschallenge=true',
                # Redirect HTTP to HTTPS if SSL is enabled
                '--entrypoints.web.http.redirections.entrypoint.to=websecure' if config['system']['ssl_enabled'] else ''
            ],
            'labels': traefik_labels,
            'networks': [
                'medocker_network'
            ]
        }
        compose['volumes']['traefik_data'] = {'driver': 'local'}
    
    # Add PostgreSQL if enabled (needed for Keycloak and Vaultwarden)
    if config['databases']['postgres']['enabled']:
        compose['services']['postgres'] = {
            'image': f"postgres:{config['databases']['postgres']['version']}",
            'restart': 'unless-stopped',
            'environment': {
                'POSTGRES_PASSWORD': config['databases']['postgres']['root_password'],
            },
            'volumes': [
                './data/postgres:/var/lib/postgresql/data'
            ],
            'networks': [
                'medocker_network'
            ]
        }
        compose['volumes']['postgres_data'] = {'driver': 'local'}
    
    # Add Keycloak if enabled
    if config['infrastructure']['keycloak']['enabled']:
        keycloak_service = {
            'image': f"quay.io/keycloak/keycloak:{config['infrastructure']['keycloak']['version']}",
            'restart': 'unless-stopped',
            'command': [
                'start-dev', 
                '--import-realm'
            ],
            'environment': {
                'KC_DB': 'postgres',
                'KC_DB_URL': f"jdbc:postgresql://{config['infrastructure']['keycloak']['db_host']}:5432/{config['infrastructure']['keycloak']['db_name']}",
                'KC_DB_USERNAME': config['infrastructure']['keycloak']['db_user'],
                'KC_DB_PASSWORD': config['infrastructure']['keycloak']['db_password'],
                'KEYCLOAK_ADMIN': config['infrastructure']['keycloak']['admin_user'],
                'KEYCLOAK_ADMIN_PASSWORD': config['infrastructure']['keycloak']['admin_password'],
                'KC_HOSTNAME': f"keycloak.{config['system']['domain']}",
                'KC_PROXY': 'edge'
            },
            'volumes': [
                './data/keycloak/realms:/opt/keycloak/data/import'
            ],
            'depends_on': [
                'postgres'
            ],
            'networks': [
                'medocker_network'
            ]
        }
        
        # If Traefik is enabled, add labels for Traefik routing
        if config['infrastructure']['traefik']['enabled']:
            keycloak_service['labels'] = [
                'traefik.enable=true',
                'traefik.http.routers.keycloak.rule=Host(`keycloak.' + config['system']['domain'] + '`)',
                'traefik.http.routers.keycloak.entrypoints=websecure',
                'traefik.http.routers.keycloak.tls=true',
                'traefik.http.services.keycloak.loadbalancer.server.port=8080'
            ]
        else:
            # If Traefik is not enabled, expose port directly
            keycloak_service['ports'] = [
                f"{config['infrastructure']['keycloak']['port']}:8080"
            ]
        
        compose['services']['keycloak'] = keycloak_service
        compose['volumes']['keycloak_data'] = {'driver': 'local'}
    
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
    
    # Add Vaultwarden if enabled
    if config['components']['vaultwarden']['enabled']:
        vaultwarden_service = {
            'image': f"vaultwarden/server:{config['components']['vaultwarden']['version']}",
            'restart': 'unless-stopped',
            'environment': {
                'DATABASE_URL': f"postgresql://{config['components']['vaultwarden']['db_user']}:{config['components']['vaultwarden']['db_pass']}@{config['components']['vaultwarden']['db_host']}:5432/{config['components']['vaultwarden']['db_name']}",
                'ADMIN_TOKEN': config['components']['vaultwarden']['admin_token'],
                'DOMAIN': f"https://{config['components']['vaultwarden']['domain']}",
                'WEBSOCKET_ENABLED': 'true',
                'SIGNUPS_ALLOWED': 'false',  # Disable public signups by default
                'WEB_VAULT_ENABLED': 'true',
            },
            'volumes': [
                './data/vaultwarden:/data'
            ],
            'networks': [
                'medocker_network'
            ],
            'depends_on': [
                'postgres'
            ]
        }
        
        # Configure SMTP if settings provided
        if config['components']['vaultwarden']['smtp_host']:
            vaultwarden_service['environment'].update({
                'SMTP_HOST': config['components']['vaultwarden']['smtp_host'],
                'SMTP_PORT': str(config['components']['vaultwarden']['smtp_port']),
                'SMTP_SSL': str(config['components']['vaultwarden']['smtp_ssl']).lower(),
                'SMTP_USERNAME': config['components']['vaultwarden']['smtp_username'],
                'SMTP_PASSWORD': config['components']['vaultwarden']['smtp_password'],
                'SMTP_FROM': config['system']['admin_email']
            })
            
        # Configure SSO with Keycloak if both are enabled
        if config['infrastructure']['keycloak']['enabled'] and config['components']['vaultwarden']['sso_enabled']:
            keycloak_url = f"https://keycloak.{config['system']['domain']}"
            vaultwarden_service['environment'].update({
                'OIDC_ENABLED': 'true',
                'OIDC_CLIENT_ID': 'vaultwarden',
                'OIDC_CLIENT_SECRET': 'vaultwarden-secret',  # This should be configured in Keycloak
                'OIDC_ISSUER_URL': f"{keycloak_url}/realms/{config['infrastructure']['keycloak']['realm_name']}",
                'OIDC_AUTHORIZATION_ENDPOINT': f"{keycloak_url}/realms/{config['infrastructure']['keycloak']['realm_name']}/protocol/openid-connect/auth",
                'OIDC_TOKEN_ENDPOINT': f"{keycloak_url}/realms/{config['infrastructure']['keycloak']['realm_name']}/protocol/openid-connect/token",
                'OIDC_USERINFO_ENDPOINT': f"{keycloak_url}/realms/{config['infrastructure']['keycloak']['realm_name']}/protocol/openid-connect/userinfo",
                'OIDC_DISPLAY_NAME': 'Keycloak',
                'OIDC_ALLOW_SIGNUP': 'true'
            })
        
        # If Traefik is enabled, add labels for Traefik routing
        if config['infrastructure']['traefik']['enabled']:
            vaultwarden_service['labels'] = [
                'traefik.enable=true',
                'traefik.http.routers.vaultwarden.rule=Host(`vaultwarden.' + config['system']['domain'] + '`)',
                'traefik.http.routers.vaultwarden.entrypoints=websecure',
                'traefik.http.routers.vaultwarden.tls=true',
                'traefik.http.services.vaultwarden.loadbalancer.server.port=80',
                # WebSocket support for real-time notifications
                'traefik.http.routers.vaultwarden-ws.rule=Host(`vaultwarden.' + config['system']['domain'] + '`) && Path(`/notifications/hub`)',
                'traefik.http.routers.vaultwarden-ws.entrypoints=websecure',
                'traefik.http.routers.vaultwarden-ws.tls=true',
                'traefik.http.services.vaultwarden-ws.loadbalancer.server.port=3012'
            ]
        else:
            # If Traefik is not enabled, expose port directly
            vaultwarden_service['ports'] = [
                f"{config['components']['vaultwarden']['port']}:80",
                '3012:3012'  # WebSocket port
            ]
        
        compose['services']['vaultwarden'] = vaultwarden_service
        compose['volumes']['vaultwarden_data'] = {'driver': 'local'}
    
    # Add OpenEMR if enabled
    if config['components']['openemr']['enabled']:
        openemr_service = {
            'image': f"openemr/openemr:{config['components']['openemr']['version']}",
            'restart': 'unless-stopped',
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
        
        # If Traefik is enabled, add labels for Traefik routing
        if config['infrastructure']['traefik']['enabled']:
            openemr_service['labels'] = [
                'traefik.enable=true',
                'traefik.http.routers.openemr.rule=Host(`openemr.' + config['system']['domain'] + '`)',
                'traefik.http.routers.openemr.entrypoints=websecure',
                'traefik.http.routers.openemr.tls=true',
                'traefik.http.services.openemr.loadbalancer.server.port=80'
            ]
            
            # Add OIDC configuration if Keycloak is enabled
            if config['infrastructure']['keycloak']['enabled']:
                # Note: OpenEMR OIDC configuration needs to be done through the admin interface
                print("OpenEMR and Keycloak detected. You'll need to configure OIDC in OpenEMR manually after startup.")
        else:
            # If Traefik is not enabled, expose port directly
            openemr_service['ports'] = [
                f"{config['components']['openemr']['port']}:80"
            ]
        
        compose['services']['openemr'] = openemr_service
        compose['volumes']['openemr_sites'] = {'driver': 'local'}
        compose['volumes']['openemr_logs'] = {'driver': 'local'}
    
    # Add Nextcloud if enabled
    if config['components']['nextcloud']['enabled']:
        nextcloud_service = {
            'image': f"nextcloud:{config['components']['nextcloud']['version']}",
            'restart': 'unless-stopped',
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
                'NEXTCLOUD_TRUSTED_DOMAINS': config['system']['domain'] + ' nextcloud.' + config['system']['domain']
            },
            'networks': [
                'medocker_network'
            ],
            'depends_on': [
                'mariadb'
            ]
        }
        
        # If Traefik is enabled, add labels for Traefik routing
        if config['infrastructure']['traefik']['enabled']:
            nextcloud_service['labels'] = [
                'traefik.enable=true',
                'traefik.http.routers.nextcloud.rule=Host(`nextcloud.' + config['system']['domain'] + '`)',
                'traefik.http.routers.nextcloud.entrypoints=websecure',
                'traefik.http.routers.nextcloud.tls=true',
                'traefik.http.services.nextcloud.loadbalancer.server.port=80'
            ]
            
            # Add OIDC configuration if Keycloak is enabled
            if config['infrastructure']['keycloak']['enabled']:
                # Note: Nextcloud OIDC configuration can be done through env vars or apps
                print("Nextcloud and Keycloak detected. You'll need to install the SSO & SAML app in Nextcloud.")
        else:
            # If Traefik is not enabled, expose port directly
            nextcloud_service['ports'] = [
                f"{config['components']['nextcloud']['port']}:80"
            ]
        
        compose['services']['nextcloud'] = nextcloud_service
        compose['volumes']['nextcloud_data'] = {'driver': 'local'}
    
    # Add Portainer if enabled
    if config['additional_services']['portainer']['enabled']:
        portainer_service = {
            'image': f"portainer/portainer-ce:{config['additional_services']['portainer']['version']}",
            'restart': 'unless-stopped',
            'volumes': [
                './data/portainer:/data',
                '/var/run/docker.sock:/var/run/docker.sock'
            ],
            'networks': [
                'medocker_network'
            ]
        }
        
        # If Traefik is enabled, add labels for Traefik routing
        if config['infrastructure']['traefik']['enabled']:
            portainer_service['labels'] = [
                'traefik.enable=true',
                'traefik.http.routers.portainer.rule=Host(`portainer.' + config['system']['domain'] + '`)',
                'traefik.http.routers.portainer.entrypoints=websecure',
                'traefik.http.routers.portainer.tls=true',
                'traefik.http.services.portainer.loadbalancer.server.port=9000'
            ]
        else:
            # If Traefik is not enabled, expose port directly
            portainer_service['ports'] = [
                f"{config['additional_services']['portainer']['port']}:9443"
            ]
        
        compose['services']['portainer'] = portainer_service
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
    
    # Create directories for Traefik if enabled
    if config['infrastructure']['traefik']['enabled']:
        os.makedirs(base_dir / 'traefik', exist_ok=True)
        # Create empty acme.json file with correct permissions
        acme_path = base_dir / 'traefik' / 'acme.json'
        if not acme_path.exists():
            with open(acme_path, 'w') as f:
                f.write('{}')
            try:
                # Set correct permissions (600) for acme.json
                acme_path.chmod(0o600)
            except Exception as e:
                print(f"Warning: Could not set permissions on acme.json: {e}")
        
        os.makedirs(base_dir / 'traefik' / 'config', exist_ok=True)
    
    # Create directories for Keycloak if enabled
    if config['infrastructure']['keycloak']['enabled']:
        os.makedirs(base_dir / 'keycloak' / 'realms', exist_ok=True)
        # Create a default realm configuration for medocker
        realm_file = base_dir / 'keycloak' / 'realms' / f"{config['infrastructure']['keycloak']['realm_name']}-realm.json"
        if not realm_file.exists():
            try:
                # Create a minimal realm configuration
                realm_config = {
                    "realm": config['infrastructure']['keycloak']['realm_name'],
                    "enabled": True,
                    "sslRequired": "external",
                    "registrationAllowed": False,
                    "clients": [
                        {
                            "clientId": "vaultwarden",
                            "enabled": True,
                            "clientAuthenticatorType": "client-secret",
                            "secret": "vaultwarden-secret",
                            "redirectUris": [
                                f"https://vaultwarden.{config['system']['domain']}/*"
                            ],
                            "webOrigins": [
                                f"https://vaultwarden.{config['system']['domain']}"
                            ],
                            "protocol": "openid-connect",
                            "publicClient": False,
                            "attributes": {
                                "pkce.code.challenge.method": "S256"
                            }
                        }
                    ]
                }
                with open(realm_file, 'w') as f:
                    yaml.dump(realm_config, f, default_flow_style=False)
                print(f"Created default Keycloak realm configuration: {realm_file}")
            except Exception as e:
                print(f"Warning: Could not create default realm configuration: {e}")
    
    # Create directories for Vaultwarden if enabled
    if config['components']['vaultwarden']['enabled']:
        os.makedirs(base_dir / 'vaultwarden', exist_ok=True)
    
    # Create directories for PostgreSQL if enabled
    if config['databases']['postgres']['enabled']:
        os.makedirs(base_dir / 'postgres', exist_ok=True)
    
    # Create directories for enabled core services
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


def run_configuration(args):
    """Run the configuration tool with the specified arguments."""
    # Load configuration
    config = load_config(args.config)
    
    # Generate secure passwords if requested
    if args.secure:
        print("Generating secure passwords for all services...")
        # MariaDB
        config['databases']['mariadb']['root_password'] = generate_password(16)
        # PostgreSQL
        if 'postgres' in config['databases']:
            config['databases']['postgres']['root_password'] = generate_password(16)
            config['databases']['postgres']['keycloak_password'] = generate_password(16)
            config['databases']['postgres']['vaultwarden_password'] = generate_password(16)
        # Keycloak
        if 'keycloak' in config['infrastructure']:
            config['infrastructure']['keycloak']['admin_password'] = generate_password(16)
        # Vaultwarden
        if 'vaultwarden' in config['components']:
            config['components']['vaultwarden']['admin_token'] = generate_password(40)
        print("Secure passwords generated!")
    
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
    
    return 0


def main():
    """Main entry point for the Medocker configuration tool."""
    parser = argparse.ArgumentParser(description='Medocker Configuration Tool')
    parser.add_argument('--config', '-c', help='Path to configuration file', default='config/default.yml')
    parser.add_argument('--output', '-o', help='Path to output docker-compose file', default='docker-compose.yml')
    parser.add_argument('--interactive', '-i', action='store_true', help='Run in interactive mode')
    parser.add_argument('--save', '-s', help='Save configuration to file', default='config/custom.yml')
    parser.add_argument('--secure', '-S', action='store_true', help='Generate secure random passwords for all services')
    
    args = parser.parse_args()
    
    return run_configuration(args)


if __name__ == '__main__':
    sys.exit(main()) 