# ALX E-Commerce Backend - EC2 Ubuntu Deployment Guide

This guide covers deploying the ALX E-Commerce Backend to AWS EC2 Ubuntu instances for production use.

## 🎯 Overview

This deployment setup provides:
- **Production-ready Django application** running on Ubuntu
- **Nginx reverse proxy** with SSL support
- **PostgreSQL database** for data persistence  
- **Redis caching** for improved performance
- **Supervisor process management** for reliability
- **Automated SSL certificates** with Let's Encrypt
- **Security hardening** with UFW firewall

---

## 📋 Prerequisites

### AWS EC2 Instance Requirements
- **OS**: Ubuntu 20.04 LTS or later
- **Instance Type**: t3.small minimum (t3.medium recommended)
- **Storage**: 20GB EBS volume minimum
- **RAM**: 2GB minimum (4GB recommended)
- **Security Group**: Ports 80, 443, and 22 open

### Local Requirements
- SSH key pair for EC2 access
- Domain name (optional, for SSL setup)

---

## 🚀 Quick Deployment

### Step 1: Connect to EC2 Instance
```bash
# Connect to your EC2 instance
ssh -i your-key-pair.pem ubuntu@your-ec2-ip-address
```

### Step 2: Run Automated Deployment
```bash
# Clone the repository
git clone https://github.com/messkely/alx-project-nexus.git
cd alx-project-nexus

# Make deployment script executable
chmod +x scripts/deploy-ec2.sh

# Run full deployment (requires sudo)
sudo ./scripts/deploy-ec2.sh init
```

### Step 3: Configure Environment
```bash
# Edit production environment variables
sudo nano /opt/alx-ecommerce/.env

# Update these critical values:
SECRET_KEY=your-very-secure-secret-key-here
DB_PASSWORD=your-secure-database-password
ALLOWED_HOSTS=your-domain.com,www.your-domain.com,your-ec2-ip
```

### Step 4: Restart Services
```bash
# Restart application services
sudo supervisorctl restart alx-ecommerce
sudo systemctl reload nginx
```

### Step 5: Setup SSL (Optional)
```bash
# Configure SSL with Let's Encrypt
sudo ./scripts/deploy-ec2.sh ssl yourdomain.com
```

---

## 🔧 Configuration Details

### Application Structure
```
/opt/alx-ecommerce/          # Main project directory
├── venv/                    # Python virtual environment
├── static/                  # Static files
├── media/                   # User uploaded files
├── .env                     # Environment variables
├── manage.py               # Django management
└── gunicorn.conf.py        # Gunicorn configuration
```

### Services Configuration

#### Nginx Configuration
- **Location**: `/etc/nginx/sites-available/alx-ecommerce`
- **Features**: Reverse proxy, static file serving, SSL ready
- **Port**: 80 (HTTP), 443 (HTTPS)

#### Gunicorn Configuration  
- **Location**: `/opt/alx-ecommerce/gunicorn.conf.py`
- **Workers**: 3 processes
- **Port**: 8000 (internal)
- **Logs**: `/var/log/gunicorn/`

#### Supervisor Configuration
- **Location**: `/etc/supervisor/conf.d/alx-ecommerce.conf`
- **Auto-restart**: Enabled
- **Logs**: `/var/log/supervisor/`

#### Database Configuration
- **PostgreSQL**: Local instance
- **Database**: `ecommerce_db`
- **User**: `ecommerce_user`
- **Port**: 5432

#### Redis Configuration
- **Port**: 6379
- **Memory Limit**: 256MB
- **Policy**: allkeys-lru

---

## 🛡️ Security Features

### Firewall Configuration (UFW)
```bash
# View current firewall status
sudo ufw status

# Allowed ports:
# - 22/tcp (SSH)
# - 80/tcp (HTTP)
# - 443/tcp (HTTPS)
```

### SSL/TLS Configuration
- **Provider**: Let's Encrypt
- **Auto-renewal**: Configured via certbot
- **HTTPS Redirect**: Automatic
- **Security Headers**: Included

### Application Security
- **Debug Mode**: Disabled in production
- **CSRF Protection**: Enabled
- **SQL Injection Protection**: Django ORM
- **XSS Protection**: Built-in Django middleware

---

## 📊 Management Commands

### Deployment Commands
```bash
# Full initial deployment
sudo ./scripts/deploy-ec2.sh init

# Update existing deployment
./scripts/deploy-ec2.sh update

# Check deployment status
./scripts/deploy-ec2.sh status

# Setup SSL certificate
sudo ./scripts/deploy-ec2.sh ssl yourdomain.com
```

### Service Management
```bash
# Restart application
sudo supervisorctl restart alx-ecommerce

# Check application status
sudo supervisorctl status alx-ecommerce

# View application logs
sudo tail -f /var/log/supervisor/alx-ecommerce.log

# Restart Nginx
sudo systemctl restart nginx

# Check Nginx status
sudo systemctl status nginx
```

### Database Management
```bash
# Connect to PostgreSQL
sudo -u postgres psql -d ecommerce_db

# Run Django migrations
cd /opt/alx-ecommerce
source venv/bin/activate
python manage.py migrate

# Create database backup
sudo -u postgres pg_dump ecommerce_db > backup_$(date +%Y%m%d_%H%M%S).sql
```

### Application Management
```bash
# Access Django shell
cd /opt/alx-ecommerce
source venv/bin/activate
python manage.py shell

# Create superuser
python manage.py createsuperuser

# Collect static files
python manage.py collectstatic --noinput

# Run tests
python manage.py test
```

---

## 🔍 Monitoring & Troubleshooting

### Log Files
```bash
# Application logs
sudo tail -f /var/log/supervisor/alx-ecommerce.log
sudo tail -f /var/log/supervisor/alx-ecommerce_error.log

# Gunicorn logs  
sudo tail -f /var/log/gunicorn/access.log
sudo tail -f /var/log/gunicorn/error.log

# Nginx logs
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log

# System logs
sudo journalctl -u nginx -f
sudo journalctl -u supervisor -f
```

### Health Checks
```bash
# Check application response
curl -I http://your-server-ip/health/

# Check database connection
cd /opt/alx-ecommerce
source venv/bin/activate
python manage.py check --database default

# Check all services
./scripts/deploy-ec2.sh status
```

### Common Issues

#### Application Not Starting
```bash
# Check supervisor status
sudo supervisorctl status

# Check gunicorn configuration
sudo supervisorctl tail alx-ecommerce

# Restart services
sudo supervisorctl restart alx-ecommerce
```

#### Database Connection Issues
```bash
# Check PostgreSQL status
sudo systemctl status postgresql

# Test database connection
sudo -u postgres psql -d ecommerce_db -c "SELECT 1;"

# Check database user permissions
sudo -u postgres psql -c "\du"
```

#### SSL Issues
```bash
# Test SSL certificate
sudo certbot certificates

# Renew SSL certificate
sudo certbot renew --dry-run

# Check Nginx SSL configuration
sudo nginx -t
```

---

## 🔄 Updates & Maintenance

### Regular Updates
```bash
# Update application code
./scripts/deploy-ec2.sh update

# Update system packages
sudo apt update && sudo apt upgrade -y

# Update Python dependencies
cd /opt/alx-ecommerce
source venv/bin/activate
pip install -r requirements.txt --upgrade
```

### Backup Strategy
```bash
# Database backup
sudo -u postgres pg_dump ecommerce_db > /opt/backups/db_$(date +%Y%m%d_%H%M%S).sql

# Media files backup
tar -czf /opt/backups/media_$(date +%Y%m%d_%H%M%S).tar.gz /opt/alx-ecommerce/media/

# Configuration backup
tar -czf /opt/backups/config_$(date +%Y%m%d_%H%M%S).tar.gz /etc/nginx/sites-available/alx-ecommerce /etc/supervisor/conf.d/alx-ecommerce.conf /opt/alx-ecommerce/.env
```

### Performance Monitoring
```bash
# Check system resources
htop
df -h
free -h

# Check application performance
curl -w "@curl-format.txt" -o /dev/null -s "http://your-server-ip/api/v1/"

# Database performance
sudo -u postgres psql -d ecommerce_db -c "SELECT * FROM pg_stat_activity;"
```

---

## 🌐 DNS & Domain Setup

### Domain Configuration
1. **Point your domain to EC2 IP**:
   - Create A record: `yourdomain.com` → `your-ec2-ip`
   - Create A record: `www.yourdomain.com` → `your-ec2-ip`

2. **Update application configuration**:
   ```bash
   sudo nano /opt/alx-ecommerce/.env
   # Update ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
   ```

3. **Setup SSL**:
   ```bash
   sudo ./scripts/deploy-ec2.sh ssl yourdomain.com
   ```

---

## 📈 Scaling Considerations

### Vertical Scaling
- Upgrade EC2 instance type (t3.small → t3.medium → t3.large)
- Increase EBS volume size
- Adjust Gunicorn worker count based on CPU cores

### Performance Optimization
```bash
# Optimize Gunicorn workers (CPU cores * 2 + 1)
sudo nano /opt/alx-ecommerce/gunicorn.conf.py

# Configure Redis memory limit
sudo nano /etc/redis/redis.conf

# Optimize PostgreSQL configuration
sudo nano /etc/postgresql/*/main/postgresql.conf
```

### Monitoring Setup
- Install monitoring tools (htop, iotop, nethogs)
- Setup log rotation
- Configure alerts for disk space and memory

---

## ⚡ Quick Reference

### Important Paths
- **Application**: `/opt/alx-ecommerce/`
- **Virtual Environment**: `/opt/alx-ecommerce/venv/`
- **Logs**: `/var/log/supervisor/`, `/var/log/nginx/`, `/var/log/gunicorn/`
- **Configuration**: `/etc/nginx/sites-available/alx-ecommerce`

### Key Commands
```bash
# Application status
sudo supervisorctl status alx-ecommerce

# Restart application
sudo supervisorctl restart alx-ecommerce

# Update deployment
./scripts/deploy-ec2.sh update

# Check logs
sudo tail -f /var/log/supervisor/alx-ecommerce.log

# SSL setup
sudo ./scripts/deploy-ec2.sh ssl yourdomain.com
```

### Access Points
- **Application**: `http://your-server-ip/` or `https://yourdomain.com/`
- **Admin Panel**: `http://your-server-ip/admin/` (admin/admin123)
- **API Documentation**: `http://your-server-ip/api/v1/docs/`
- **Health Check**: `http://your-server-ip/health/`

---

**Need help?** Check the troubleshooting section above or review the application logs for detailed error information.
