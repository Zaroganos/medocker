# Authentication and Reverse Proxy in Medocker

Medocker now includes key infrastructure components that enhance your deployment's security, accessibility, and manageability:

1. **Traefik** - A modern reverse proxy and load balancer
2. **Keycloak** - A robust identity provider for centralized authentication
3. **Vaultwarden** - A lightweight Bitwarden-compatible password manager

## Traefik Reverse Proxy

Traefik serves as the main entry point for all your services, providing:

- **Automatic SSL/TLS certificate management** with Let's Encrypt
- **Domain-based routing** (e.g., openemr.yourdomain.com, nextcloud.yourdomain.com)
- **Traffic encryption** between clients and your services
- **Load balancing** for high availability setups
- **Middleware capabilities** for request modification, redirection, and authentication

When enabled, Traefik will automatically configure routes to your services based on subdomains, eliminating the need to expose multiple ports.

### Key Features

- **Automatic Service Discovery**: Traefik automatically detects services in Docker and configures routes
- **Dashboard**: A web UI for monitoring traffic and routes (available at traefik.yourdomain.com)
- **Dynamic Configuration**: Changes take effect without restarts
- **Performance**: High-performance Go-based proxy with minimal overhead

## Keycloak Identity Provider

Keycloak provides centralized authentication and authorization for all services:

- **Single Sign-On (SSO)** across your entire Medocker deployment
- **Multi-factor Authentication** for enhanced security
- **User self-service** including password reset, enrollment, etc.
- **Fine-grained access control** to your applications
- **Enterprise Support** options available through Red Hat

### Key Features

- **OIDC and SAML** support for broad compatibility
- **Identity Brokering** with external identity providers (Google, Facebook, etc.)
- **User Federation** with LDAP and Active Directory
- **Well-documented API** for integration with custom applications
- **Mature and widely-adopted** in enterprise and healthcare environments

## Vaultwarden Password Manager

Vaultwarden is an unofficial, lightweight Bitwarden-compatible password manager server:

- **Secure password management** for individuals and teams
- **Cross-platform clients** (mobile, desktop, browser extensions)
- **Self-hosted** for complete control of your data
- **Lightweight** requiring minimal resources
- **TOTP support** for two-factor authentication
- **Encrypted file attachments** for secure document storage

### Integration with Keycloak

Vaultwarden can be configured to use Keycloak for authentication through OpenID Connect (OIDC). This provides:

- Centralized user management
- Single sign-on experience
- Enhanced security policies
- Support for multi-factor authentication

## Integration Between Components

When all components are enabled, they work together to provide a seamless security experience:

1. All requests to your services first go through Traefik
2. User authentication is handled by Keycloak
3. Password management is handled by Vaultwarden, which can authenticate through Keycloak
4. Medical services (OpenEMR, Nextcloud) can also authenticate through Keycloak

This setup provides:

- Centralized authentication and authorization
- Consistent login experience
- Simplified user management
- Enhanced security through standardized protocols

## Alternative Options

### Authentication Alternatives

If Keycloak doesn't meet your needs, alternatives include:

- **Authentik**: More modern, Python-based alternative but less mature
- **Dex**: Lightweight OpenID Connect identity provider
- **Gluu**: Enterprise-focused open source IAM platform

### Reverse Proxy Alternatives

Alternative reverse proxy options include:

- **Nginx Proxy Manager**: User-friendly but less automated
- **Caddy**: Simpler configuration but fewer enterprise features
- **HAProxy**: Better for high-performance TCP routing
- **Kong**: More suited for API gateway patterns

### Password Manager Alternatives

Alternative password management options include:

- **Bitwarden (Official)**: More resource-intensive but comes with official support
- **Passbolt**: Open source password manager with a focus on team collaboration
- **Padloc**: Modern, open-source password manager

## Configuration Options

All components can be enabled and configured via the Medocker configuration script:

```bash
python configure.py --interactive
```

During the configuration, you'll be prompted to:

1. Enable/disable Traefik, Keycloak, and Vaultwarden
2. Set domain names for routing
3. Configure HTTPS settings
4. Set security credentials
5. Customize integration points

For advanced configuration, see `config/default.yml` for all available options.

## Setting Up Single Sign-On

To configure single sign-on between Keycloak and other services:

1. **For Vaultwarden**: SSO is configured automatically when both Keycloak and Vaultwarden are enabled
2. **For OpenEMR**: Log into the OpenEMR admin interface and configure the SSO settings manually 
3. **For Nextcloud**: Install the "Social Login" app from the Nextcloud app store and configure it to use Keycloak

## Security Best Practices

1. **Always change default passwords** provided in the configuration
2. **Enable multi-factor authentication** in Keycloak for administrative accounts
3. **Regularly update** all components to address security vulnerabilities
4. **Use a strong master password** for Vaultwarden
5. **Implement proper backup procedures** for all data, especially Keycloak and Vaultwarden databases 