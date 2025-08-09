# 🚀 Production Deployment Guide

## 📋 Overview

This guide covers the complete production deployment of the ALX E-Commerce Backend on AWS EC2 with HTTPS using Let's Encrypt SSL certificates.

**Current Production Environment:**
- **Domain:** https://ecom-backend.store/
- **Server:** AWS EC2 Ubuntu (3.80.35.89)
- **SSL:** Let's Encrypt (Auto-renewal enabled)
- **Containers:** Django, PostgreSQL, Redis, Nginx

---

## ✅ Production Deployment Status

### 🌐 Live Services
- ✅ **API Endpoint:** https://ecom-backend.store/
- ✅ **Health Check:** https://ecom-backend.store/health/
- ✅ **Admin Panel:** https://ecom-backend.store/admin/
- ✅ **API Documentation:** https://ecom-backend.store/api/v1/docs/

### 🔒 Security Features
- ✅ **Let's Encrypt SSL** - Valid until November 7, 2025
- ✅ **Auto-renewal** - Configured via cron job
- ✅ **HTTP → HTTPS Redirects** - Automatic secure redirects
- ✅ **Security Headers** - HSTS, CSP, X-Frame-Options
- ✅ **Rate Limiting** - API protection enabled

### 🐳 Container Status
- ✅ **Django Web App** - Healthy and responding
- ✅ **PostgreSQL Database** - Healthy with data persistence
- ✅ **Redis Cache** - Healthy with authentication
- ✅ **Nginx Proxy** - SSL termination and routing

---

## 🛠️ Deployment Architecture

```
Internet → Cloudflare DNS → AWS EC2 → Nginx → Django App
                                   ↓
                              PostgreSQL + Redis
```

### Network Flow:
1. **DNS Resolution:** ecom-backend.store → 3.80.35.89
2. **SSL Termination:** Nginx handles HTTPS with Let's Encrypt
3. **Reverse Proxy:** Nginx routes to Django (port 8000)
4. **Application:** Django serves API with PostgreSQL/Redis backend

---

## 📚 Key Configuration Files

### Docker Compose
```yaml
# docker-compose.prod.yml - Production container setup
version: '3.8'
services:
  web: # Django application
  db: # PostgreSQL database  
  redis: # Redis cache
  nginx: # Reverse proxy with SSL
```

### Nginx Configuration
```nginx
# nginx/ec2-production.conf
server {
    listen 443 ssl http2;
    server_name ecom-backend.store;
    
    ssl_certificate /etc/letsencrypt/live/ecom-backend.store/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/ecom-backend.store/privkey.pem;
    
    location / {
        proxy_pass http://web:8000;
        # Security headers and proxy settings
    }
}
```

### SSL Certificate Management
```bash
# Auto-renewal via cron (runs twice daily)
0 12 * * * /usr/bin/certbot renew --quiet --deploy-hook "docker compose -f /home/ubuntu/alx-project-nexus/docker-compose.prod.yml restart nginx"
```

---

## 🔧 Maintenance Commands

### Check SSL Certificate Status
```bash
sudo certbot certificates
```

### Monitor Container Health
```bash
docker compose -f docker-compose.prod.yml ps
docker compose -f docker-compose.prod.yml logs
```

### Update Application
```bash
git pull origin main
docker compose -f docker-compose.prod.yml down
docker compose -f docker-compose.prod.yml up -d --build
```

### Database Backup
```bash
docker compose -f docker-compose.prod.yml exec db pg_dump -U postgres ecommerce_db > backup_$(date +%Y%m%d).sql
```

---

## 🚨 Troubleshooting

### Common Issues

#### SSL Certificate Problems
```bash
# Check certificate expiry
sudo certbot certificates

# Manual renewal
sudo certbot renew --force-renewal
```

#### Container Issues
```bash
# Check container logs
docker compose -f docker-compose.prod.yml logs nginx
docker compose -f docker-compose.prod.yml logs web

# Restart specific service
docker compose -f docker-compose.prod.yml restart nginx
```

#### Database Connection Issues
```bash
# Check database health
docker compose -f docker-compose.prod.yml exec db pg_isready -U postgres

# Access database shell
docker compose -f docker-compose.prod.yml exec db psql -U postgres -d ecommerce_db
```

### Health Check Endpoints
- **Application:** https://ecom-backend.store/health/
- **Database:** https://ecom-backend.store/health/db/
- **Cache:** https://ecom-backend.store/health/cache/

---

## 📊 Performance Monitoring

### Key Metrics to Monitor
- **SSL Certificate Expiry:** 89 days remaining (as of deployment)
- **Container Memory Usage:** Monitor via `docker stats`
- **Database Performance:** Query response times
- **API Response Times:** Health endpoint latency
- **Error Rates:** Application logs for 4xx/5xx errors

### Logging Locations
- **Application Logs:** `logs/security.log`
- **Nginx Logs:** Container logs via docker compose
- **SSL Logs:** `/var/log/letsencrypt/letsencrypt.log`

---

## 🔐 Security Considerations

### Current Security Measures
- ✅ **HTTPS Only** - All traffic encrypted
- ✅ **Strong SSL Configuration** - A+ SSL Labs rating
- ✅ **Security Headers** - Comprehensive header protection
- ✅ **Rate Limiting** - API abuse protection
- ✅ **Database Security** - Encrypted connections
- ✅ **Container Isolation** - Docker network security

### Regular Security Tasks
- [ ] Monitor SSL certificate renewal (automated)
- [ ] Review application logs for suspicious activity
- [ ] Update Docker images for security patches
- [ ] Monitor for new Django security releases
- [ ] Backup database regularly

---

## 📞 Support and Resources

### Documentation Links
- [HTTPS Setup Guide](HTTPS_SETUP_GUIDE.md)
- [EC2 Deployment Details](EC2-DEPLOYMENT.md)
- [Docker Configuration](docs/DOCKER_DEPLOYMENT.md)

### Quick Commands Reference
```bash
# Check production status
curl -I https://ecom-backend.store/health/

# View container status  
docker compose -f docker-compose.prod.yml ps

# Check SSL certificate
sudo certbot certificates

# View application logs
docker compose -f docker-compose.prod.yml logs -f web
```

---

**🎉 Production deployment complete and operational!**  
**Domain:** https://ecom-backend.store/  
**Status:** ✅ All systems healthy and secure
