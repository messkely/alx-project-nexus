# HTTPS Setup Guide for ALX E-Commerce Backend

## 🔒 Setup HTTPS for Your EC2 Production Environment

### Option 1: Quick Setup with Self-Signed Certificate (Immediate)

**On your EC2 instance:**

```bash
# Get the latest scripts
cd ~/alx-project-nexus
git pull origin main

# Run the HTTPS setup script
sudo ./scripts/setup-https.sh
```

**What this does:**
- ✅ Generates self-signed SSL certificates
- ✅ Creates HTTPS-enabled Nginx configuration
- ✅ Sets up automatic HTTP→HTTPS redirects
- ✅ Configures modern SSL/TLS security
- ✅ Adds security headers (HSTS, CSP, etc.)
- ✅ Enables HTTP/2 for better performance

### Option 2: Production SSL with Let's Encrypt (Requires Domain)

**If you have a domain name:**

```bash
# Setup Let's Encrypt SSL (FREE and trusted by browsers)
sudo ./scripts/setup-letsencrypt.sh yourdomain.com
```

### Testing Your HTTPS Setup

```bash
# Test HTTPS functionality
./scripts/test-https.sh
```

## 🌐 Your New HTTPS URLs

After setup, your application will be available at:

- **🔒 Main App:** https://3.80.35.89/
- **🔒 Health Check:** https://3.80.35.89/health/
- **🔒 API Docs:** https://3.80.35.89/api/v1/docs/
- **🔒 Admin Panel:** https://3.80.35.89/admin/
- **🔒 API Endpoints:** https://3.80.35.89/api/v1/

## 🔧 HTTPS Configuration Features

### Security Enhancements:
- ✅ **TLS 1.2 & 1.3** - Modern encryption protocols
- ✅ **HSTS Headers** - Prevents downgrade attacks  
- ✅ **CSP Headers** - Content Security Policy
- ✅ **X-Frame-Options** - Prevents clickjacking
- ✅ **HTTP/2 Support** - Improved performance
- ✅ **Automatic Redirects** - HTTP traffic redirects to HTTPS

### Performance Features:
- ✅ **Gzip Compression** - Faster page loads
- ✅ **Static File Caching** - 1-year cache for assets
- ✅ **SSL Session Caching** - Faster SSL handshakes

## 📊 Expected Results

### Successful HTTPS Setup:
```bash
# Health check should return:
curl -k https://3.80.35.89/health/
{"status": "healthy", "service": "alx-ecommerce-backend", ...}

# HTTP should redirect to HTTPS:
curl -I http://3.80.35.89/health/
HTTP/1.1 301 Moved Permanently
Location: https://3.80.35.89/health/
```

## ⚠️ Important Notes

### Self-Signed Certificates:
- Browsers will show "Not Secure" or certificate warnings
- Safe for testing and development
- Users must manually accept the certificate
- Not recommended for public production use

### Let's Encrypt Certificates:
- Trusted by all browsers (no warnings)
- FREE and auto-renewable
- Requires a registered domain name
- Recommended for production use

## 🔧 Management Commands

### Service Management:
```bash
# Check HTTPS services status
docker compose -f docker-compose.https.yml ps

# View Nginx logs
docker compose -f docker-compose.https.yml logs nginx

# Restart HTTPS services
docker compose -f docker-compose.https.yml restart

# Stop HTTPS and return to HTTP
docker compose -f docker-compose.https.yml down
docker compose -f docker-compose.prod.yml up -d
```

### SSL Certificate Management:
```bash
# Check certificate expiration
openssl x509 -in ssl/cert.crt -noout -dates

# Renew Let's Encrypt certificate (if using domain)
sudo certbot renew
```

## 🚀 Next Steps After HTTPS Setup

1. **Update API clients** to use HTTPS URLs
2. **Test all endpoints** with HTTPS
3. **Configure domain** (if you have one) for Let's Encrypt
4. **Update DNS records** to point to your EC2 instance
5. **Set up certificate auto-renewal** for Let's Encrypt

## 🔍 Troubleshooting

### If HTTPS doesn't work:
```bash
# Check Nginx configuration
docker exec ecommerce_nginx_prod nginx -t

# Check SSL files
ls -la ssl/

# View detailed logs
docker compose -f docker-compose.https.yml logs nginx --tail=50
```

### Common Issues:
- **Port 443 blocked**: Check EC2 security groups
- **Certificate not found**: Re-run setup script
- **Permission denied**: Use sudo for setup scripts

## 🎉 Benefits of HTTPS

- 🔒 **Encrypted traffic** between users and your API
- 🚀 **Better SEO** ranking (Google favors HTTPS)
- 🛡️ **Security headers** protect against attacks
- ⚡ **HTTP/2 support** for faster loading
- 🌐 **Browser compatibility** (modern browsers require HTTPS for many features)
- 📱 **Mobile app support** (iOS/Android require HTTPS for production APIs)
