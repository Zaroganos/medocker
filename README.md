# Medocker

**Clinic in a box by way of docker stack**

Medocker is a comprehensive Docker packaging of all the software a medical practice needs, including:

1. **OpenEMR** with all modules for electronic medical records
2. **Nextcloud** with all backends and relevant apps for file storage and collaboration
3. Many optional additional services for a complete medical practice IT infrastructure

## Key Features

- **All-in-one solution** for medical practice software needs
- **Configurable deployment** with only the components you need
- **Security focused** with proper network isolation and data protection
- **Easy setup** through interactive configuration
- **Scalable architecture** supporting small practices to large clinics

## Components

Medocker includes a wide range of software components organized into categories:

### Core Components
- **OpenEMR** - Complete electronic medical record system
- **Nextcloud** - Secure file sharing and collaboration platform

### Additional Services
- Medical Device Integration (Mirth Connect, OpenHIM)
- Security Infrastructure (Keycloak, Vault, Wazuh, OpenVAS)
- Backup and Disaster Recovery (Duplicati, MinIO, Barman)
- Analytics and Reporting (Metabase, HAPI FHIR Server)
- Communication Infrastructure (FreePBX, Mattermost)
- Monitoring and Management (Prometheus, Grafana, Portainer)
- Imaging Solutions (Orthanc DICOM server)
- Workflow Automation (n8n, Kong API Gateway)

## Getting Started

### Prerequisites

- Docker and Docker Compose installed on your system
- Python 3.6 or higher
- Sufficient disk space for the components you plan to enable

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/medocker.git
   cd medocker
   ```

2. Install required Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the configuration script in interactive mode:
   ```bash
   python configure.py --interactive
   ```

4. Launch the configured stack:
   ```bash
   docker-compose up -d
   ```

### Configuration Options

You can customize your Medocker deployment using these options:

```bash
# Run with interactive prompts
python configure.py --interactive

# Use a custom configuration file
python configure.py --config my-config.yml

# Save configuration to a specific file
python configure.py --interactive --save my-clinic-config.yml

# Generate docker-compose with a custom output file
python configure.py --output production-compose.yml
```

## Security Considerations

- Change all default passwords before using in production
- Configure proper firewall rules to limit access to services
- Enable SSL for all publicly accessible services
- Regularly backup your data
- Keep all components updated with security patches

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request
