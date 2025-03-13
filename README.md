# Medocker

**Clinic in a box by way of docker stack**

Medocker is a comprehensive Docker packaging of all the software a medical practice needs, including:

1. **OpenEMR** with all modules for electronic medical records
2. **Nextcloud** with all backends and relevant apps for file storage and collaboration
3. **Vaultwarden** for secure password management with Bitwarden compatibility
4. Many optional additional services for a complete medical practice IT infrastructure

## Key Features

- **All-in-one solution** for medical practice software needs
- **Configurable deployment** with only the components you need
- **Security focused** with proper network isolation and data protection
- **Easy setup** through interactive configuration or web GUI
- **Scalable architecture** supporting small practices to large clinics
- **Modern infrastructure** with Traefik reverse proxy and Keycloak identity management

## Components

Medocker includes a wide range of software components organized into categories:

### Core Components
- **OpenEMR** - Complete electronic medical record system
- **Nextcloud** - Secure file sharing and collaboration platform
- **Vaultwarden** - Lightweight Bitwarden-compatible password manager

### Infrastructure Components
- **Traefik** - Modern reverse proxy with automatic SSL and service discovery
- **Keycloak** - Enterprise-grade identity provider for single sign-on across all services

### Additional Services
- Medical Device Integration (Mirth Connect, OpenHIM)
- Security Infrastructure (Vault, Wazuh, OpenVAS)
- Backup and Disaster Recovery (Duplicati, MinIO, Barman)
- Analytics and Reporting (Metabase, HAPI FHIR Server)
- Communication Infrastructure (FreePBX, Mattermost)
- Monitoring and Management (Prometheus, Grafana, Portainer)
- Imaging Solutions (Orthanc DICOM server)
- Workflow Automation (n8n, Kong API Gateway)

## Getting Started

### Prerequisites

- Docker and Docker Compose installed on your system
- Sufficient disk space for the components you plan to enable
- A domain name (optional, but recommended for production use with Traefik)

### For Users

#### Installation

1. Download the latest Medocker release for your platform from the [Releases](https://github.com/yourusername/medocker/releases) page.

2. Extract the downloaded archive:
   ```bash
   # For Windows
   Extract the medocker-windows.zip file using Windows Explorer
   
   # For Linux
   tar -xzf medocker-linux.tar.gz
   
   # For macOS
   tar -xzf medocker-macos.tar.gz
   ```

3. Run the Medocker launcher:
   ```bash
   # For Windows
   Double-click on Medocker.bat
   
   # For Linux/macOS
   chmod +x medocker.sh (if needed)
   ./medocker.sh
   ```

4. Follow the on-screen instructions to configure and deploy your Medocker stack.

### For Developers

#### Setup Development Environment

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/medocker.git
   cd medocker
   ```

2. Install Poetry if you don't have it already:
   ```bash
   # On Linux, macOS, Windows (WSL)
   curl -sSL https://install.python-poetry.org | python3 -

   # On Windows (PowerShell)
   (Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | python -
   ```

3. Install dependencies using Poetry:
   ```bash
   poetry install
   ```

#### Development Workflow

```bash
# Activate the virtual environment
poetry shell

# Run the configuration tool
python configure.py --interactive

# Run the web interface
python run_web.py

# Use the unified CLI
python medocker.py --help
```

#### Building Standalone Executables

To build standalone executables for distribution:

```bash
# Install development dependencies
poetry install --with dev

# Run the build script
python build.py
```

This will create platform-specific packages in the project root directory:
- `medocker-windows.zip` for Windows
- `medocker-linux.tar.gz` for Linux
- `medocker-macos.tar.gz` for macOS

## Standalone Executables

Medocker is distributed as standalone executables for all major platforms, making it easy to use without installing Python or any dependencies. The executables include everything needed to run the application.

### For End Users

Simply download the appropriate package for your platform, extract it, and run the launcher:

- **Windows**: Run `Medocker.bat`
- **Linux/macOS**: Run `./medocker.sh`

The launcher provides a simple menu to configure, run the web interface, or deploy your Medocker stack.

### For Developers

Standalone executables are built using PyInstaller. To build the executables:

```bash
# Install development dependencies
poetry install --with dev

# Run the build script
python build.py
```

This will create platform-specific packages that can be distributed to end users.

## Configuration Options

You can customize your Medocker deployment using these options:

#### Unified CLI

```bash
# Get help for all commands
poetry run medocker --help

# Configure interactively
poetry run medocker configure --interactive

# Configure with a custom config file
poetry run medocker configure --config my-config.yml

# Save configuration to a specific file
poetry run medocker configure --interactive --save my-clinic-config.yml

# Start the web interface
poetry run medocker web

# Run web interface on a specific port
poetry run medocker web --port 8080

# Run web interface in debug mode
poetry run medocker web --debug

# Deploy the stack
poetry run medocker deploy

# Deploy with latest Docker images
poetry run medocker deploy --pull
```

#### Traditional Command-line Interface

```bash
# Using activated environment
python configure.py --interactive

# Using Poetry directly
poetry run python configure.py --interactive

# Use a custom configuration file
poetry run python configure.py --config my-config.yml

# Save configuration to a specific file
poetry run python configure.py --interactive --save my-clinic-config.yml

# Generate docker-compose with a custom output file
poetry run python configure.py --output production-compose.yml

# Generate secure passwords for all services
poetry run python configure.py --secure
```

#### Web Interface

```bash
# Using activated environment
python run_web.py

# Using Poetry directly
poetry run python run_web.py

# Run on a specific port
poetry run python run_web.py --port 8080

# Run in debug mode for development
poetry run python run_web.py --debug

# Run with a specific host binding
poetry run python run_web.py --host 127.0.0.1
```

The web interface provides a user-friendly way to:
- Configure all components and services
- View and manage running services
- Deploy and monitor your Medocker stack
- Generate secure passwords
- Download your configuration files

## Development

### Using Poetry for Development

```bash
# Install development dependencies
poetry install --with dev

# Run code formatting
poetry run black .
poetry run isort .

# Run linting
poetry run flake8

# Run tests (when implemented)
poetry run pytest
```

## Security Considerations

- Change all default passwords before using in production
- Configure proper firewall rules to limit access to services
- Enable SSL for all publicly accessible services
- Regularly backup your data
- Keep all components updated with security patches
- Use Keycloak for centralized authentication when possible
- Store all service credentials securely in Vaultwarden

## Documentation

- [Authentication and Reverse Proxy Guide](docs/authentication-and-proxy.md) - Details about Traefik and Keycloak setup

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Install development dependencies (`poetry install --with dev`)
4. Format your code (`poetry run black . && poetry run isort .`)
5. Commit your changes (`git commit -m 'Add some amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request
