#!/bin/bash
# Setup script to initialize data directory from templates

echo "Setting up Medocker data directory from templates..."

# Create data directory if it doesn't exist
mkdir -p data

# Copy template directories only if they don't exist
if [ ! -d "data/keycloak" ]; then cp -r data-templates/keycloak data/; fi
if [ ! -d "data/mariadb" ]; then cp -r data-templates/mariadb data/; fi
if [ ! -d "data/mattermost" ]; then cp -r data-templates/mattermost data/; fi
if [ ! -d "data/nextcloud" ]; then cp -r data-templates/nextcloud data/; fi
if [ ! -d "data/openemr" ]; then cp -r data-templates/openemr data/; fi
if [ ! -d "data/portainer" ]; then cp -r data-templates/portainer data/; fi
if [ ! -d "data/postgres" ]; then cp -r data-templates/postgres data/; fi
if [ ! -d "data/rustdesk" ]; then cp -r data-templates/rustdesk data/; fi
if [ ! -d "data/traefik" ]; then cp -r data-templates/traefik data/; fi
if [ ! -d "data/vaultwarden" ]; then cp -r data-templates/vaultwarden data/; fi

echo "Data directory setup complete!" 