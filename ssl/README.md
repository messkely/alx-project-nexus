# SSL Certificates Directory

This directory is for SSL certificates when using HTTPS with Docker.

## For Development:
You can use self-signed certificates for local HTTPS testing.

## For Production:
Place your SSL certificates here:
- `cert.pem` - Your SSL certificate
- `key.pem` - Your private key
- `chain.pem` - Certificate chain (if applicable)

## Let's Encrypt with Docker:
You can use certbot with Docker volumes to automatically manage SSL certificates.

**Note**: This directory is excluded from Docker builds via .dockerignore for security.
