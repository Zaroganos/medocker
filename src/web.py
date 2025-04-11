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
import tempfile
import json
from pathlib import Path
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, send_file, session
from flask_wtf import CSRFProtect
from flask_session import Session
from waitress import serve

# Import functions from configure.py
from configure import (
    load_config, 
    save_config, 
    generate_password,
    resolve_variable_references,
    generate_docker_compose,
    create_directories,
    deploy_docker_compose_ssh,
    generate_ansible_playbook,
    run_ansible_playbook
)

# Initialize Flask app
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(script_dir)
templates_dir = os.path.join(project_root, 'templates')
static_dir = os.path.join(project_root, 'static')

app = Flask(__name__, 
           template_folder=templates_dir,
           static_folder=static_dir)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', secrets.token_hex(16))
csrf = CSRFProtect(app)

# Configure Flask-Session
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_FILE_DIR'] = os.path.join(tempfile.gettempdir(), 'medocker_sessions')
os.makedirs(app.config['SESSION_FILE_DIR'], exist_ok=True)
Session(app)

# Ensure the template and static directories exist
os.makedirs(templates_dir, exist_ok=True)
os.makedirs(static_dir, exist_ok=True)

# Default configuration file
DEFAULT_CONFIG_FILE = os.path.join(project_root, 'config/default.yml')
CUSTOM_CONFIG_FILE = os.path.join(project_root, 'config/custom.yml')


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
    try:
        length = int(request.form.get('length', 16))
        return jsonify({'password': generate_password(length)})
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@app.route('/download_compose')
def download_compose():
    """Download the generated docker-compose.yml file."""
    # Get the absolute path to docker-compose.yml
    compose_file = os.path.abspath('docker-compose.yml')
    
    # Check if the file exists
    if not os.path.exists(compose_file):
        # Generate it if it doesn't exist
        config_file = CUSTOM_CONFIG_FILE if os.path.exists(CUSTOM_CONFIG_FILE) else DEFAULT_CONFIG_FILE
        config_data = load_config(config_file)
        generate_docker_compose(config_data, compose_file)
        
        # Check again after generation
        if not os.path.exists(compose_file):
            flash('Error: Could not generate docker-compose.yml file.', 'error')
            return redirect(url_for('deploy_page'))
    
    try:
        return send_file(compose_file, as_attachment=True)
    except Exception as e:
        flash(f'Error downloading file: {str(e)}', 'error')
        return redirect(url_for('deploy_page'))


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


@app.route('/deploy', methods=['GET', 'POST'])
def deploy_page():
    """Render the deployment page and handle deployment requests."""
    # Load current configuration
    config_file = CUSTOM_CONFIG_FILE if os.path.exists(CUSTOM_CONFIG_FILE) else DEFAULT_CONFIG_FILE
    config_data = load_config(config_file)
    
    # If this is a POST request, handle the deployment
    if request.method == 'POST':
        deployment_type = request.form.get('deployment_type')
        
        if deployment_type == 'ssh':
            # Get SSH parameters
            host = request.form.get('ssh_host')
            port = int(request.form.get('ssh_port', 22))
            username = request.form.get('ssh_username')
            password = request.form.get('ssh_password') if request.form.get('use_password') == 'true' else None
            key_path = request.form.get('ssh_key_path') if request.form.get('use_key') == 'true' else None
            
            # Validate required fields
            if not host or not username:
                flash('Host and username are required for SSH deployment', 'error')
                return redirect(url_for('deploy_page'))
            
            if not password and not key_path:
                flash('Either password or SSH key is required for SSH deployment', 'error')
                return redirect(url_for('deploy_page'))
            
            # Execute SSH deployment
            result = deploy_docker_compose_ssh(
                config_data, 
                host, 
                username, 
                password, 
                key_path, 
                port
            )
            
            if result['status'] == 'success':
                flash(result['message'], 'success')
            else:
                flash(result['message'], 'error')
                
        elif deployment_type == 'download':
            # Just generate docker-compose.yml for download
            # This is handled by the existing download_compose route
            return redirect(url_for('download_compose'))
            
        return redirect(url_for('deploy_page'))
    
    return render_template('deploy.html', config=config_data)


@app.route('/api/ssh_deploy', methods=['POST'])
def api_ssh_deploy():
    """API endpoint for SSH deployment."""
    try:
        # Get JSON data
        data = request.json
        
        # Load configuration
        config_file = CUSTOM_CONFIG_FILE if os.path.exists(CUSTOM_CONFIG_FILE) else DEFAULT_CONFIG_FILE
        config_data = load_config(config_file)
        
        # Execute SSH deployment
        result = deploy_docker_compose_ssh(
            config_data,
            data.get('host'),
            data.get('username'),
            data.get('password'),
            data.get('key_path'),
            data.get('port', 22)
        )
        
        return jsonify(result)
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500


@app.route('/ansible', methods=['GET', 'POST'])
def ansible_page():
    """Render the Ansible playbook page and handle playbook generation."""
    # Load current configuration
    config_file = CUSTOM_CONFIG_FILE if os.path.exists(CUSTOM_CONFIG_FILE) else DEFAULT_CONFIG_FILE
    config_data = load_config(config_file)
    
    # Initialize user_setup if not present
    if 'user_setup' not in config_data:
        config_data['user_setup'] = {
            'client_apps': {},
            'configure_browser': False
        }
    
    # Handle form submission
    if request.method == 'POST':
        action = request.form.get('action')
        
        if action == 'generate':
            # Update configuration with form data
            config_data['user_setup']['configure_browser'] = request.form.get('configure_browser') == 'true'
            
            # Update client app settings
            for component in ['nextcloud', 'vaultwarden', 'rustdesk']:
                if component in config_data.get('components', {}):
                    config_data['components'][component]['client_enabled'] = request.form.get(f'{component}_client') == 'true'
            
            # Save configuration
            save_config(config_data, CUSTOM_CONFIG_FILE)
            
            # Generate Ansible playbook
            playbook_path = generate_ansible_playbook(config_data)
            
            flash(f'Ansible playbook generated successfully at {playbook_path}', 'success')
            
            # Prepare download link
            playbook_dir = os.path.dirname(playbook_path)
            session['playbook_dir'] = playbook_dir
            
            return redirect(url_for('ansible_page'))
            
        elif action == 'run':
            # Run the playbook on localhost
            inventory_path = os.path.join('playbooks', 'inventory.yml')
            playbook_path = os.path.join('playbooks', 'medocker-user-setup.yml')
            
            result = run_ansible_playbook(playbook_path, inventory_path)
            
            if result['status'] == 'success':
                flash('Ansible playbook executed successfully!', 'success')
            else:
                flash(f'Ansible playbook execution failed: {result["message"]}', 'error')
                
            return redirect(url_for('ansible_page'))
    
    # Check if playbook exists
    playbook_exists = os.path.exists(os.path.join('playbooks', 'medocker-user-setup.yml'))
    
    return render_template('ansible.html', config=config_data, playbook_exists=playbook_exists)


@app.route('/download_ansible')
def download_ansible():
    """Download the generated Ansible playbook as a zip file."""
    try:
        import zipfile
        from io import BytesIO
        
        # Check if playbook directory exists
        playbook_dir = 'playbooks'
        if not os.path.exists(playbook_dir) or not os.path.isdir(playbook_dir):
            flash('Ansible playbook directory not found. Please generate the playbook first.', 'error')
            return redirect(url_for('ansible_page'))
            
        # Check if there are files in the directory
        files_exist = False
        for _, _, files in os.walk(playbook_dir):
            if files:
                files_exist = True
                break
                
        if not files_exist:
            flash('No Ansible playbook files found. Please generate the playbook first.', 'error')
            return redirect(url_for('ansible_page'))
        
        # Create a zip file in memory
        memory_file = BytesIO()
        
        with zipfile.ZipFile(memory_file, 'w', zipfile.ZIP_DEFLATED) as zipf:
            # Add all files from the playbook directory
            for root, dirs, files in os.walk(playbook_dir):
                for file in files:
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, playbook_dir)
                    zipf.write(file_path, arcname)
        
        # Seek to the beginning of the BytesIO object
        memory_file.seek(0)
        
        return send_file(
            memory_file,
            mimetype='application/zip',
            as_attachment=True,
            download_name='medocker-ansible-playbook.zip'
        )
    except Exception as e:
        flash(f'Error creating Ansible playbook zip: {str(e)}', 'error')
        return redirect(url_for('ansible_page'))


@app.route('/api/generate_ansible', methods=['POST'])
def api_generate_ansible():
    """API endpoint for Ansible playbook generation."""
    try:
        # Get JSON data
        data = request.json
        
        # Load configuration
        config_file = CUSTOM_CONFIG_FILE if os.path.exists(CUSTOM_CONFIG_FILE) else DEFAULT_CONFIG_FILE
        config_data = load_config(config_file)
        
        # Update configuration with API data
        if 'user_setup' in data:
            config_data['user_setup'] = data['user_setup']
        
        # Update client app settings if provided
        if 'components' in data:
            for component, settings in data['components'].items():
                if component in config_data.get('components', {}):
                    if 'client_enabled' in settings:
                        config_data['components'][component]['client_enabled'] = settings['client_enabled']
        
        # Save configuration
        save_config(config_data, CUSTOM_CONFIG_FILE)
        
        # Generate Ansible playbook
        playbook_path = generate_ansible_playbook(config_data)
        
        return jsonify({
            'status': 'success',
            'message': 'Ansible playbook generated successfully',
            'playbook_path': playbook_path
        })
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500


@app.route('/cart')
def cart_page():
    """Render the service cart page."""
    return render_template('cart.html')


@app.route('/api/service_catalog', methods=['GET'])
def api_service_catalog():
    """Return the service catalog data."""
    try:
        catalog_file = os.path.join(project_root, 'data/service_catalog.json')
        if os.path.exists(catalog_file):
            with open(catalog_file, 'r') as f:
                catalog = json.load(f)
            return jsonify(catalog)
        else:
            return jsonify({
                'status': 'error',
                'message': 'Service catalog file not found'
            }), 404
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500


@app.route('/api/generate_from_cart', methods=['POST'])
def api_generate_from_cart():
    """Generate docker-compose configuration from cart contents."""
    try:
        # Get cart items from request
        data = request.json
        cart_items = data.get('cart', [])
        
        if not cart_items:
            return jsonify({
                'status': 'error',
                'message': 'Cart is empty'
            }), 400
        
        # Load current configuration
        config_file = CUSTOM_CONFIG_FILE if os.path.exists(CUSTOM_CONFIG_FILE) else DEFAULT_CONFIG_FILE
        config_data = load_config(config_file)
        
        # Load service catalog
        catalog_file = os.path.join(project_root, 'data/service_catalog.json')
        with open(catalog_file, 'r') as f:
            catalog = json.load(f)
        
        # Update configuration based on cart items
        for item in cart_items:
            service_id = item.get('id')
            service_type = item.get('type')
            
            if service_type == 'docker':
                # Find service in catalog
                service = next((s for s in catalog['docker_services'] if s['id'] == service_id), None)
                if service:
                    # Enable the service in configuration
                    if service_id in config_data.get('components', {}):
                        config_data['components'][service_id]['enabled'] = True
                    elif service_id in config_data.get('infrastructure', {}):
                        config_data['infrastructure'][service_id]['enabled'] = True
                    elif service_id in config_data.get('databases', {}):
                        config_data['databases'][service_id]['enabled'] = True
                    elif service_id in config_data.get('additional_services', {}):
                        config_data['additional_services'][service_id]['enabled'] = True
            elif service_type == 'ai':
                # Handle AI services
                # For now, just keep track of them in the cart
                if 'ai_services' not in config_data:
                    config_data['ai_services'] = {}
                config_data['ai_services'][service_id] = {
                    'enabled': True,
                    'api_key': '',  # Will be filled by user later
                    'local': True if 'local' in item.get('tags', []) else False
                }
        
        # Save updated configuration
        save_config(config_data, CUSTOM_CONFIG_FILE)
        
        # Generate docker-compose file
        generate_docker_compose(config_data, 'docker-compose.yml')
        
        return jsonify({
            'status': 'success',
            'message': 'Configuration generated successfully'
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500


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