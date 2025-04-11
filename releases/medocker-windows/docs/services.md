# Additional Services

This document describes optional additional services that can be enabled in your Medocker deployment.

## Rustdesk

Rustdesk is an open-source remote desktop software, similar to TeamViewer or AnyDesk, but completely self-hosted. It's perfect for providing IT support to your staff or allowing secure remote access to clinic systems.

### Features

- **Self-hosted**: All data stays within your network, enhancing security
- **Cross-platform**: Works on Windows, macOS, Linux, iOS, and Android
- **End-to-end encryption**: Secure communication between clients
- **No firewall configuration needed**: Works without opening ports when using the relay server
- **Web client**: Access via browser without installing software

### Configuration Options

```yaml
additional_services:
  rustdesk:
    enabled: true  # Set to true to enable Rustdesk
    version: latest  # Docker image version
    hbbs_port: 21115  # ID/Rendezvous server port
    hbbr_port: 21116  # Relay server port
    relay_port: 21117  # Direct TCP relay port
    web_port: 8080  # Web client port
    key_base: "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"  # Encryption key (recommended to change)
```

### Usage

1. Enable Rustdesk in your configuration
2. Deploy your Medocker stack
3. Access the web client at `https://rustdesk.yourdomain.com` (if Traefik is enabled) or via the configured port
4. Install Rustdesk clients on devices that need access or support
5. Configure clients to use your self-hosted server

### Security Considerations

- Change the default `key_base` to a secure random string
- Use HTTPS (enabled by default with Traefik) for the web client
- Limit access to the Rustdesk services using appropriate network controls

## Fasten Health

Fasten Health is a self-hosted application that allows patients and healthcare providers to aggregate and access health records from multiple sources. It helps consolidate medical data from different healthcare providers.

### Features

- **Unified view**: Aggregate medical records from multiple providers
- **Self-hosted**: Maintain full control over sensitive health data
- **FHIR compatible**: Works with modern health data standards
- **Patient-focused**: Designed for individuals to manage their own health information
- **Provider integration**: Connect to multiple healthcare systems

### Configuration Options

```yaml
additional_services:
  fasten-health:
    enabled: true  # Set to true to enable Fasten Health
    version: latest  # Docker image version
    port: 8090  # Application port
    host: 0.0.0.0  # Listening interface
```

### Usage

1. Enable Fasten Health in your configuration
2. Deploy your Medocker stack
3. Access the web interface at `https://fastenhealth.yourdomain.com` (if Traefik is enabled) or via the configured port
4. Create an account and start linking your healthcare providers
5. View and manage your aggregated health records

### Security Considerations

- Ensure your Medocker deployment uses HTTPS (enabled by default with Traefik)
- Regularly back up the Fasten Health data
- Consider implementing additional authentication methods

### Integration with Other Medocker Services

Fasten Health works well alongside other Medocker components:

- **OpenEMR**: Complementary to the clinical-focused EMR system
- **Nextcloud**: Store exported health records for long-term archiving
- **Vaultwarden**: Securely store credentials for multiple healthcare provider portals 