# Medocker

![Screenshot 2025-05-02 005811](https://github.com/user-attachments/assets/5b5454c1-3283-4405-8acf-e562ceefe3f8)

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
- **Remote Access**
  - **Rustdesk** - Open-source remote desktop software for secure remote support and access
- **Health Records**
  - **Fasten Health** - Self-hosted health record aggregation platform to manage medical data
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

### For End Users

#### Installation

0. **Prerelease**: If there is no release, or new recent release, skip to "For Developers" below.

1. Download the latest Medocker release for your platform from the [Releases](https://github.com/Zaroganos/medocker/releases) page.

2. Extract the downloaded archive:
   ```bash
   # For Windows
   Extract the medocker-windows.zip file using Windows Explorer
   
   # For Linux/macOS
   tar -xzf medocker-linux.tar.gz  # or medocker-macos.tar.gz
   ```

3. Run the Medocker launcher:
   ```bash
   # For Windows
   Double-click on launcher.bat
   
   # For Linux/macOS
   chmod +x launcher.sh (if needed)
   ./launcher.sh
   ```

4. Follow the on-screen instructions to configure and deploy your Medocker stack.

#### Using Medocker

The executable automatically launches the web interface, which is the primary way to interact with Medocker. You can also use specific commands:

```bash
# Show help for all available commands
medocker.exe --help  # or ./medocker --help on Linux/macOS

# Run the configuration tool in interactive mode
medocker.exe configure --interactive

# Deploy the Docker stack
medocker.exe deploy
```

### For Developers

#### Setup Development Environment

1. Clone the repository:
   ```bash
   git clone https://github.com/Zaroganos/medocker.git
   cd medocker
   ```

2. Install uv if you don't have it already:
   ```bash
   # On Linux, macOS, Windows (WSL)
   curl -LsSf https://astral.sh/uv/install.sh | sh

   # On Windows (PowerShell)
   powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

   # Or via pip
   pip install uv
   ```
3. Install dependencies:
   ```bash
   uv sync --all-extras
   ```

#### Development Workflow

```bash
# Use the unified CLI tool (recommended)
uv run medocker --help
uv run medocker --web --help
uv run medocker --configure --help

# Launch the web interface
uv run medocker --web

# Run configuration tool
uv run medocker --configure

# Or run modules directly
uv run python -m medocker.medocker --help
uv run python -m medocker.configure --interactive
uv run python -m medocker.run_web
```

#### Building Executables

```bash
# Using the build script (recommended)
uv run python scripts/build/build_auto.py

# Or manually with PyInstaller
uv run python -m PyInstaller medocker.spec --clean

# Or use platform-specific scripts
build.bat  # Windows
./build.sh # Linux/macOS
```

This creates platform-specific packages in the `releases` directory.

## Architecture & Structure

### How It Works

Medocker uses Docker Compose in two ways:
1. **Tool Deployment**: The Medocker configuration tool itself can be run via Docker Compose
2. **Service Generation**: The tool generates Docker Compose files for medical practice services

### Project Structure

Medocker follows modern Python packaging standards:

```
medocker/
├── src/
│   └── medocker/           # Main Python package
│       ├── __init__.py     # Package initialization and exports
│       ├── medocker.py     # Main CLI entry point
│       ├── configure.py    # Configuration and deployment logic
│       ├── run_web.py      # Web interface launcher
│       ├── web.py          # Flask web application
│       ├── config.py       # Configuration management
│       └── playbooks/      # Ansible playbooks for user setup
├── templates/               # HTML templates for web interface
├── static/                  # Static assets (CSS, JS, images)
├── config/                  # Configuration files
├── docker-compose.yml       # Development environment setup
├── Dockerfile               # Container configuration
└── pyproject.toml          # Project configuration and dependencies
```

### Docker Development

```bash
# Build and run the development container
docker build -t medocker .
docker run --rm -p 9876:9876 medocker

# Or use docker-compose for the full development stack
docker compose up -d
```

The Docker setup automatically handles:
- Python 3.12 runtime environment
- uv package management
- Proper template and static file paths
- Consistent behavior between development and production

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests: `uv run pytest`
5. Format code: `uv run black .` and `uv run isort .`
6. Verify the package structure: `uv build`
7. Test the CLI tools: `uv run medocker --help`
8. Submit a pull request

### Development Guidelines

- Follow the established `src/medocker/` package structure
- Use relative imports within the package
- Test both the CLI tools and web interface
- Ensure Docker builds work correctly
- Update documentation for any new features

## Support

This program is in active development and support may not be offered at this time.
Documentation and Discussions may not be enabled at this time.
As the project approaches viability and release, documentation and discussions will be enabled.

- **Documentation**: [docs/](docs/)
- **Issues**: [GitHub Issues](https://github.com/Zaroganos/medocker/issues)
- **Discussions**: [GitHub Discussions](https://github.com/Zaroganos/medocker/discussions)

## Roadmap

- [ ] Expanded software library
- [ ] Curated specialty stacks
- [ ] Addition of medical device integrations
- [ ] Security feature configuration
- [ ] Sharding deployment support
- [ ] Backup and disaster recovery automation
- [ ] Performance monitoring and alerting
- [ ] Mobile device support
- [ ] Basic multimedia tutorials for end users
- [ ] Dedicated documentation page

## License

This project is licensed under the GNU Affero General Public License v3.0 -- see the [LICENSE](LICENSE) file for details.

Copyright (C) 2024-2025 Iliya Yaroshevskiy