# Security Configuration for Production

This document outlines best practices for securing our Django DRF backend in production.

## Environment Variables

Sensitive information should be stored as environment variables, not in code:

1. Database credentials
2. Django secret key
3. API keys and tokens
4. SMTP credentials

Our deployment uses `.env` files for local development and environment variables in production.

## HTTPS Configuration

All production traffic should be served over HTTPS:

1. Use Let's Encrypt for free, automated SSL certificates
2. Configure Nginx to redirect all HTTP traffic to HTTPS
3. Use HTTP Strict Transport Security (HSTS)
4. Enable SSL/TLS with modern protocols (TLSv1.2 and TLSv1.3)

Sample Nginx HTTPS configuration:

```nginx
server {
    listen 80;
    server_name yourdomain.com;
    return 301 https://$host$request_uri;
}

server {
    listen 443 ssl http2;
    server_name yourdomain.com;

    ssl_certificate /etc/letsencrypt/live/yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/yourdomain.com/privkey.pem;
    ssl_trusted_certificate /etc/letsencrypt/live/yourdomain.com/chain.pem;

    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_prefer_server_ciphers on;
    ssl_ciphers ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384:ECDHE-ECDSA-CHACHA20-POLY1305:ECDHE-RSA-CHACHA20-POLY1305:DHE-RSA-AES128-GCM-SHA256:DHE-RSA-AES256-GCM-SHA384;
    
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
    add_header X-Content-Type-Options nosniff;
    add_header X-Frame-Options DENY;
    add_header X-XSS-Protection "1; mode=block";

    # Remaining configuration...
}
```

## Django Settings for Production

The following Django settings should be configured for production:

1. `DEBUG = False`
2. Limit `ALLOWED_HOSTS` to specific domains
3. Configure proper CORS settings
4. Set strong password validators
5. Use secure cookies

## JWT Authentication Security

For JWT token security:

1. Use short token lifetimes (access: 15 minutes, refresh: 7 days)
2. Implement token blacklisting for logout
3. Use HTTPS for all token transmission
4. Include proper audience and issuer claims

## Database Security

Secure the database with:

1. Strong, unique passwords
2. Network isolation (not exposed to the public internet)
3. Minimal privilege principle for database users
4. Regular security updates

## Firewall Configuration

Implement firewall rules to:

1. Only allow necessary ports (80, 443, and SSH)
2. Limit SSH access to specific IP addresses
3. Block all other incoming traffic

## Regular Security Updates

Keep all components updated:

1. Set up automated security updates for the OS
2. Regularly update Python dependencies
3. Keep Docker images updated
4. Monitor security advisories

## Secrets Management

For GitHub Actions, store secrets securely:

1. Use GitHub repository secrets for sensitive data
2. Never hardcode credentials in workflow files
3. Rotate secrets regularly

## Backup Security

Secure your backups:

1. Encrypt database backups
2. Use secure channels for backup transfer
3. Implement access controls for backup storage
4. Regularly test backup integrity
