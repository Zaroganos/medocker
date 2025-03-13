#!/usr/bin/env python3
"""
Medocker Web Configuration Tool

This script provides a web interface for configuring and managing the Medocker stack.
"""

import os
import sys
import yaml
import secrets
import string
from pathlib import Path
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, send_file
from flask_wtf import CSRFProtect
from waitress import serve

# Import functions from configure.py
from configure import (
    load_config, 
    save_config, 
    generate_password,
    resolve_variable_references,
    generate_docker_compose,
    create_directories
)

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', secrets.token_hex(16))
csrf = CSRFProtect(app)

# Ensure the template and static directories exist
os.makedirs('templates', exist_ok=True)
os.makedirs('static', exist_ok=True)

# Default configuration file
DEFAULT_CONFIG_FILE = 'config/default.yml'
CUSTOM_CONFIG_FILE = 'config/custom.yml'


@app.route('/')
def index():
    """Render the home page with overview information."""
    return render_template('index.html')


@app.route('/config', methods=['GET', 'POST'])
def config():
    """Render the configuration form and handle form submission."""
    # Load current configuration
    config_file = CUSTOM_CONFIG_FILE if os.path.exists(CUSTOM_CONFIG_FILE) else DEFAULT_CONFIG_FILE
    config_data = load_config(config_file)
    
    if request.method == 'POST':
        # Update configuration with form data
        update_config_from_form(config_data, request.form)
        
        # Save configuration
        save_config(config_data, CUSTOM_CONFIG_FILE)
        
        # Generate docker-compose file
        generate_docker_compose(config_data, 'docker-compose.yml')
        
        # Create directories
        create_directories(config_data)
        
        flash('Configuration saved successfully!', 'success')
        return redirect(url_for('config'))
    
    return render_template('config.html', config=config_data)


@app.route('/services')
def services():
    """Render the services page showing status of running containers."""
    return render_template('services.html')


@app.route('/generate_password', methods=['POST'])
def generate_password_route():
    """Generate and return a secure password."""
    length = int(request.form.get('length', 16))
    return jsonify({'password': generate_password(length)})


@app.route('/download_compose')
def download_compose():
    """Download the generated docker-compose.yml file."""
    return send_file('docker-compose.yml', as_attachment=True)


@app.route('/api/config', methods=['GET'])
def api_config():
    """Return the current configuration as JSON."""
    config_file = CUSTOM_CONFIG_FILE if os.path.exists(CUSTOM_CONFIG_FILE) else DEFAULT_CONFIG_FILE
    config_data = load_config(config_file)
    return jsonify(config_data)


@app.route('/api/deploy', methods=['POST'])
def api_deploy():
    """Deploy the Docker stack."""
    try:
        # This is where you would execute docker-compose commands
        # For now, we'll just return a success message
        return jsonify({'status': 'success', 'message': 'Deployment initiated'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500


@app.route('/api/service_status', methods=['GET'])
def service_status():
    """Get the status of all services."""
    try:
        # In a real implementation, you would check Docker service status
        # For now, return a simulated status
        services = {
            'traefik': {'status': 'running', 'version': 'v2.9.6'},
            'keycloak': {'status': 'running', 'version': '21.1.1'},
            'postgres': {'status': 'running', 'version': '14.5-alpine'},
            'mariadb': {'status': 'running', 'version': '10.6.12'},
            'openemr': {'status': 'running', 'version': '7.0.0'},
            'nextcloud': {'status': 'running', 'version': '25.0.3'},
            'vaultwarden': {'status': 'running', 'version': 'latest'},
            'portainer': {'status': 'running', 'version': '2.16.2'},
            'rustdesk': {'status': 'stopped', 'version': 'latest'},
            'fasten-health': {'status': 'stopped', 'version': 'latest'}
        }
        return jsonify({'status': 'success', 'services': services})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500


@app.route('/api/service_action', methods=['POST'])
def service_action():
    """Perform an action on a service."""
    try:
        service = request.json.get('service')
        action = request.json.get('action')
        
        if not service or not action:
            return jsonify({'status': 'error', 'message': 'Service and action are required'}), 400
            
        if action not in ['start', 'stop', 'restart']:
            return jsonify({'status': 'error', 'message': 'Invalid action'}), 400
            
        # In a real implementation, you would execute Docker commands
        # For now, just return success
        return jsonify({
            'status': 'success', 
            'message': f'{action.capitalize()} operation performed on {service}'
        })
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500


def update_config_from_form(config, form_data):
    """Update configuration dictionary with form data."""
    # System settings
    config['system']['domain'] = form_data.get('system_domain', config['system']['domain'])
    config['system']['ssl_enabled'] = form_data.get('system_ssl_enabled') == 'true'
    config['system']['admin_email'] = form_data.get('system_admin_email', config['system']['admin_email'])
    config['system']['timezone'] = form_data.get('system_timezone', config['system']['timezone'])
    config['system']['data_directory'] = form_data.get('system_data_directory', config['system']['data_directory'])
    
    # Infrastructure services
    
    # Traefik
    config['infrastructure']['traefik']['enabled'] = form_data.get('infrastructure_traefik_enabled') == 'true'
    if config['infrastructure']['traefik']['enabled']:
        config['infrastructure']['traefik']['http_port'] = form_data.get('infrastructure_traefik_http_port', config['infrastructure']['traefik']['http_port'])
        config['infrastructure']['traefik']['https_port'] = form_data.get('infrastructure_traefik_https_port', config['infrastructure']['traefik']['https_port'])
        config['infrastructure']['traefik']['dashboard_port'] = form_data.get('infrastructure_traefik_dashboard_port', config['infrastructure']['traefik']['dashboard_port'])
    
    # Keycloak
    config['infrastructure']['keycloak']['enabled'] = form_data.get('infrastructure_keycloak_enabled') == 'true'
    if config['infrastructure']['keycloak']['enabled']:
        config['infrastructure']['keycloak']['admin_password'] = form_data.get('infrastructure_keycloak_admin_password', config['infrastructure']['keycloak']['admin_password'])
        # If password is still default and generate checkbox is checked, generate a new one
        if config['infrastructure']['keycloak']['admin_password'] == "change-me-please" and form_data.get('generate_keycloak_password') == 'true':
            config['infrastructure']['keycloak']['admin_password'] = generate_password(16)
    
    # Databases
    
    # PostgreSQL (required for Keycloak and Vaultwarden)
    if config['infrastructure']['keycloak']['enabled'] or (
            'vaultwarden' in form_data and form_data.get('components_vaultwarden_enabled') == 'true'):
        config['databases']['postgres']['enabled'] = True
        
        # Generate secure passwords if requested
        if form_data.get('generate_postgres_passwords') == 'true':
            config['databases']['postgres']['root_password'] = generate_password(16)
            config['databases']['postgres']['keycloak_password'] = generate_password(16)
            config['databases']['postgres']['vaultwarden_password'] = generate_password(16)
    
    # MariaDB
    config['databases']['mariadb']['enabled'] = form_data.get('databases_mariadb_enabled') == 'true'
    if config['databases']['mariadb']['enabled']:
        if form_data.get('generate_mariadb_password') == 'true':
            config['databases']['mariadb']['root_password'] = generate_password(16)
        else:
            config['databases']['mariadb']['root_password'] = form_data.get('databases_mariadb_root_password', config['databases']['mariadb']['root_password'])
    
    # Components
    
    # OpenEMR
    config['components']['openemr']['enabled'] = form_data.get('components_openemr_enabled') == 'true'
    if config['components']['openemr']['enabled']:
        config['components']['openemr']['version'] = form_data.get('components_openemr_version', config['components']['openemr']['version'])
        if not config['infrastructure']['traefik']['enabled']:
            config['components']['openemr']['port'] = form_data.get('components_openemr_port', config['components']['openemr']['port'])
    
    # Nextcloud
    config['components']['nextcloud']['enabled'] = form_data.get('components_nextcloud_enabled') == 'true'
    if config['components']['nextcloud']['enabled']:
        config['components']['nextcloud']['version'] = form_data.get('components_nextcloud_version', config['components']['nextcloud']['version'])
        if not config['infrastructure']['traefik']['enabled']:
            config['components']['nextcloud']['port'] = form_data.get('components_nextcloud_port', config['components']['nextcloud']['port'])
    
    # Vaultwarden
    config['components']['vaultwarden']['enabled'] = form_data.get('components_vaultwarden_enabled') == 'true'
    if config['components']['vaultwarden']['enabled']:
        config['components']['vaultwarden']['version'] = form_data.get('components_vaultwarden_version', config['components']['vaultwarden']['version'])
        if not config['infrastructure']['traefik']['enabled']:
            config['components']['vaultwarden']['port'] = form_data.get('components_vaultwarden_port', config['components']['vaultwarden']['port'])
        
        # Generate secure admin token if requested
        if form_data.get('generate_vaultwarden_token') == 'true':
            config['components']['vaultwarden']['admin_token'] = generate_password(40)
        else:
            config['components']['vaultwarden']['admin_token'] = form_data.get('components_vaultwarden_admin_token', config['components']['vaultwarden']['admin_token'])
        
        # Configure SSO with Keycloak if both are enabled
        if config['infrastructure']['keycloak']['enabled']:
            config['components']['vaultwarden']['sso_enabled'] = form_data.get('components_vaultwarden_sso_enabled') == 'true'
    
    # Additional Services
    for service in config['additional_services']:
        if isinstance(config['additional_services'][service], dict):
            enabled_key = f'additional_services_{service}_enabled'
            config['additional_services'][service]['enabled'] = form_data.get(enabled_key) == 'true'
    
    # Resolve any variable references
    config = resolve_variable_references(config)
    
    return config


def main():
    """Main entry point for the Medocker web configuration tool."""
    # Create the templates directory if it does not exist
    host = os.environ.get('HOST', '0.0.0.0')
    port = int(os.environ.get('PORT', '5000'))
    
    print(f"Starting Medocker Web Configuration Tool at http://{host}:{port}")
    
    # Use waitress for production
    if os.environ.get('FLASK_ENV') == 'development':
        app.run(host=host, port=port, debug=True)
    else:
        serve(app, host=host, port=port)


if __name__ == '__main__':
    main() 