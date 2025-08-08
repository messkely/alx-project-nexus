# ALX E-Commerce Backend - Production Deployment Guide
**Updated:** August 8, 2025

This comprehensive guide will help you deploy the ALX E-Commerce Backend to a production VPS server with enterprise-grade security, performance, and monitoring.

## 🚀 Quick Start

1. **Clone the repository on your VPS:**
   ```bash
   git clone https://github.com/messkely/alx-project-nexus.git
   cd alx-project-nexus
   ```

2. **Run the deployment script:**
   ```bash
   ./deploy.sh init
   ```

3. **Follow the interactive prompts** to complete the setup.

## 📋 Prerequisites

### System Requirements
- **OS:** Ubuntu 20.04 LTS or later / CentOS 8 or later
- **RAM:** Minimum 2GB (4GB recommended)
- **Storage:** Minimum 20GB SSD
- **CPU:** 2 cores minimum

### Software Requirements
- Docker 24.0 or later
- Docker Compose V2
- Git
- Nginx (if not using containerized version)

### Domain Requirements
- Registered domain name
- DNS configured to point to your VPS IP

## 🛠️ Installation Steps

### 1. Server Preparation

Update your system:
```bash
sudo apt update && sudo apt upgrade -y
```

Install Docker:
```bash
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER
newgrp docker
```

### 2. Project Setup

```bash
# Clone repository
git clone https://github.com/messkely/alx-project-nexus.git
cd alx-project-nexus

# Make deployment script executable
chmod +x deploy.sh

# Copy environment template
cp .env.prod.example .env.prod
```

### 3. Environment Configuration

Edit `.env.prod` with your actual values:
```bash
nano .env.prod
```

**Critical settings to update:**
- `DJANGO_SECRET_KEY`: Generate a strong secret key
- `DJANGO_ALLOWED_HOSTS`: Your domain name
- `DB_PASSWORD`: Secure database password
- Email settings for notifications
- SSL and security settings

### 4. Domain Configuration

Update the Nginx configuration:
```bash
# Edit nginx config with your domain
sed -i 's/your-domain.com/YOUR_ACTUAL_DOMAIN/g' nginx/conf.d/ecommerce.conf
```

### 5. Initialize Production Environment

```bash
./deploy.sh init
```

This will:
- Build Docker images
- Start all services
- Run database migrations
- Create superuser account
- Optionally seed database

### 6. SSL Certificate Setup

```bash
./deploy.sh ssl
```

Follow the prompts to set up Let's Encrypt SSL certificate.

## 🔧 Management Commands

### Deployment Management
```bash
# Update deployment
./deploy.sh update

# View logs
./deploy.sh logs [service]

# Check status
./deploy.sh status

# Create backup
./deploy.sh backup

# Restore from backup
./deploy.sh restore /path/to/backup.sql
```

### Direct Docker Commands
```bash
# Start services
docker compose -f docker-compose.production.yml up -d

# Stop services
docker compose -f docker-compose.production.yml down

# View logs
docker compose -f docker-compose.production.yml logs -f

# Execute commands in web container
docker compose -f docker-compose.production.yml exec web python manage.py [command]
```

## 🔒 Security Considerations

### Firewall Configuration
```bash
# Basic firewall setup
sudo ufw enable
sudo ufw allow ssh
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw deny 5432/tcp  # Block direct database access
sudo ufw deny 6379/tcp  # Block direct Redis access
```

### SSL/HTTPS
- SSL certificates are automatically managed via Let's Encrypt
- HTTP traffic is redirected to HTTPS
- Strong SSL ciphers and security headers are configured

### Database Security
- PostgreSQL is configured to only accept connections from application containers
- Database passwords should be strong and unique
- Regular backups are automated

### Application Security
- Django runs as non-root user
- Security middleware enabled with CSP headers
- Rate limiting configured for API endpoints
- Admin interface can be IP-restricted

## 📊 Monitoring & Maintenance

### Health Checks
All services have built-in health checks:
- **Web:** `http://your-domain.com/api/v1/health/`
- **Database:** PostgreSQL health check
- **Redis:** Redis ping check

### Log Management
```bash
# Application logs
docker compose -f docker-compose.production.yml logs web

# Nginx logs
docker compose -f docker-compose.production.yml logs nginx

# Database logs
docker compose -f docker-compose.production.yml logs db
```

### Backup Strategy
```bash
# Automated daily backups (add to crontab)
0 2 * * * cd /path/to/project && ./deploy.sh backup

# Manual backup
./deploy.sh backup
```

### Updates
```bash
# Pull latest changes and update
git pull origin main
./deploy.sh update
```

## 🐛 Troubleshooting

### Common Issues

**Service won't start:**
```bash
# Check logs
./deploy.sh logs

# Check service status
./deploy.sh status

# Restart services
docker compose -f docker-compose.production.yml restart
```

**Database connection issues:**
```bash
# Check database health
docker compose -f docker-compose.production.yml exec db pg_isready

# Check environment variables
docker compose -f docker-compose.production.yml exec web env | grep DB_
```

**SSL issues:**
```bash
# Renew SSL certificate
docker run --rm -v "$(pwd)/ssl:/etc/letsencrypt" certbot/certbot renew

# Check certificate expiry
openssl x509 -in ssl/fullchain.pem -text -noout | grep "Not After"
```

### Performance Tuning

**Increase Gunicorn workers:**
Edit `Dockerfile.prod` and adjust `--workers` parameter based on your CPU cores.

**Database optimization:**
- Monitor slow queries
- Add indexes for frequently queried fields
- Configure PostgreSQL memory settings

**Redis optimization:**
- Monitor memory usage
- Configure maxmemory policy
- Use Redis persistence if needed

## 📈 Scaling

### Horizontal Scaling
- Use Docker Swarm or Kubernetes for multi-node deployment
- Configure load balancer (nginx, HAProxy)
- Separate database and Redis to dedicated servers

### Vertical Scaling
- Increase server resources (CPU, RAM)
- Optimize Gunicorn worker count
- Tune database connection pool

## 🆘 Support

For issues and support:
1. Check the troubleshooting section above
2. Review application logs
3. Consult Django and Docker documentation
4. Create an issue in the project repository

## 📝 License

This project is part of the ALX ProDev Backend Development Program.

---

**Production Checklist:**
- [ ] Environment variables configured
- [ ] Domain DNS configured
- [ ] SSL certificate installed
- [ ] Firewall configured
- [ ] Backup strategy implemented
- [ ] Monitoring setup
- [ ] Security headers verified
- [ ] Performance testing completed
