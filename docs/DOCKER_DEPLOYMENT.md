# ALX E-Commerce Backend - Docker Deployment Guide

This guide covers deploying the ALX E-Commerce Backend using Docker and Docker Compose for both development and production environments.

## 🎯 Overview

The Docker setup provides:
- **Multi-container application** with Django, PostgreSQL, Redis, and Nginx
- **Development environment** with hot reload and debugging
- **Production environment** with optimized settings and reverse proxy
- **Scalable architecture** ready for deployment anywhere
- **Consistent environments** across development, staging, and production

---

## 📋 Prerequisites

- **Docker**: Version 20.0+ 
- **Docker Compose**: Version 2.0+
- **Git**: For cloning the repository

### Installation

#### Ubuntu/Debian:
```bash
# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Install Docker Compose
sudo apt install docker-compose-plugin

# Add user to docker group
sudo usermod -aG docker $USER
newgrp docker
```

#### macOS:
```bash
# Install Docker Desktop
brew install --cask docker
```

#### Windows:
Download and install Docker Desktop from [docker.com](https://www.docker.com/products/docker-desktop)

---

## 🚀 Quick Start

### Development Environment
```bash
# Clone the repository
git clone https://github.com/messkely/alx-project-nexus.git
cd alx-project-nexus

# Start development environment
make docker-dev
```

### Production Environment
```bash
# Start production environment
make docker-prod
```

---

## 🔧 Docker Architecture

### Services Overview

```yaml
┌─────────────────────────────────────────────────┐
│                    nginx                        │
│           (Reverse Proxy & Static Files)       │
│                   Port: 80, 443                │
└─────────────────────┬───────────────────────────┘
                      │
┌─────────────────────▼───────────────────────────┐
│                    web                          │
│              (Django Application)               │
│                   Port: 8000                    │
└─────────────┬───────────────────┬───────────────┘
              │                   │
┌─────────────▼─────────┐ ┌───────▼─────────┐
│         db            │ │      redis      │
│   (PostgreSQL)        │ │    (Cache)      │
│    Port: 5432         │ │   Port: 6379    │
└───────────────────────┘ └─────────────────┘
```

### Container Details

| Service | Image | Purpose | Ports |
|---------|-------|---------|-------|
| **web** | Custom (Django) | Main application | 8000 |
| **db** | postgres:15-alpine | Database | 5432 |
| **redis** | redis:7-alpine | Caching | 6379 |
| **nginx** | nginx:alpine | Reverse proxy | 80, 443 |

---

## 💻 Development Environment

### Starting Development
```bash
# Start all services
make docker-dev

# Or manually
docker-compose -f docker-compose.dev.yml up --build
```

### Development Features
- **Hot Reload**: Code changes reflect immediately
- **Debug Mode**: Django debug mode enabled
- **Volume Mounting**: Local code mounted in container
- **Separate Database**: `ecommerce_dev` database
- **Development Server**: Django runserver

### Development Access
- **Application**: http://localhost:8000/
- **Admin Panel**: http://localhost:8000/admin/ (admin/admin123)
- **API Docs**: http://localhost:8000/api/v1/docs/
- **Database**: localhost:5433 (external access)
- **Redis**: localhost:6380 (external access)

---

## 🏭 Production Environment

### Starting Production
```bash
# Start all services
make docker-prod

# Or manually
docker-compose up --build -d
```

### Production Features
- **Gunicorn Server**: Production WSGI server
- **Nginx Reverse Proxy**: Static files and load balancing
- **Health Checks**: Container health monitoring
- **Security Headers**: Enhanced security configuration
- **SSL Ready**: HTTPS configuration available
- **Optimized Images**: Multi-stage builds and slim images

### Production Access
- **Application**: http://localhost/
- **Admin Panel**: http://localhost/admin/ (admin/admin123)
- **API Docs**: http://localhost/api/v1/docs/
- **Static Files**: Served by Nginx
- **SSL**: Ready for certificates

---

## 📊 Management Commands

### Container Management
```bash
# View running containers
make docker-status
docker-compose ps

# View logs
make docker-logs
docker-compose logs -f web

# Stop services
make docker-down
docker-compose down

# Restart specific service
docker-compose restart web
```

### Application Management
```bash
# Access Django shell
make docker-shell
docker-compose exec web python manage.py shell

# Run migrations
docker-compose exec web python manage.py migrate

# Create superuser
docker-compose exec web python manage.py createsuperuser

# Collect static files
docker-compose exec web python manage.py collectstatic --noinput

# Run tests
docker-compose exec web python manage.py test
```

### Database Management
```bash
# Access PostgreSQL
docker-compose exec db psql -U ecommerce_user -d ecommerce_db

# Database backup
docker-compose exec db pg_dump -U ecommerce_user ecommerce_db > backup.sql

# Database restore
docker-compose exec -T db psql -U ecommerce_user -d ecommerce_db < backup.sql

# Reset database
docker-compose down -v
docker-compose up -d db
docker-compose exec web python manage.py migrate
```

---

## 🔒 Production Configuration

### Environment Variables
Update `docker-compose.yml` environment section:

```yaml
environment:
  - DEBUG=False
  - SECRET_KEY=your-very-secure-secret-key-here
  - ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
  - DB_PASSWORD=your-secure-database-password
```

### SSL Configuration

#### 1. Add SSL Certificates
```bash
# Copy your certificates to ssl/ directory
cp your-cert.pem ssl/cert.pem
cp your-key.pem ssl/key.pem
```

#### 2. Update Nginx Configuration
Edit `nginx/default.conf` and uncomment HTTPS section:
```nginx
server {
    listen 443 ssl http2;
    server_name yourdomain.com;
    
    ssl_certificate /etc/nginx/ssl/cert.pem;
    ssl_certificate_key /etc/nginx/ssl/key.pem;
    # ... rest of configuration
}
```

#### 3. Restart Services
```bash
docker-compose restart nginx
```

### Let's Encrypt SSL (Automatic)
```bash
# Add certbot service to docker-compose.yml
# This will automatically get and renew certificates
```

---

## 📈 Scaling and Performance

### Horizontal Scaling
```yaml
# Scale web service
docker-compose up --scale web=3 -d

# Load balancer configuration in nginx
upstream django {
    server web_1:8000;
    server web_2:8000;
    server web_3:8000;
}
```

### Performance Optimization

#### Gunicorn Configuration
Edit Dockerfile to customize Gunicorn:
```dockerfile
CMD ["gunicorn", "ecommerce_backend.wsgi:application", 
     "--bind", "0.0.0.0:8000", 
     "--workers", "4", 
     "--worker-class", "sync",
     "--max-requests", "1000"]
```

#### Database Optimization
```yaml
# PostgreSQL optimizations in docker-compose.yml
environment:
  - POSTGRES_SHARED_PRELOAD_LIBRARIES=pg_stat_statements
  - POSTGRES_MAX_CONNECTIONS=200
  - POSTGRES_SHARED_BUFFERS=256MB
```

#### Redis Configuration
```yaml
# Redis optimizations
command: redis-server 
  --maxmemory 512mb 
  --maxmemory-policy allkeys-lru
  --save 900 1
```

---

## 🔍 Monitoring and Logging

### Container Health
```bash
# Check container health
docker-compose ps
docker inspect --format='{{.State.Health.Status}}' container_name

# Health check logs
docker inspect --format='{{.State.Health.Log}}' container_name
```

### Application Logs
```bash
# All services
make docker-logs

# Specific service
docker-compose logs -f web
docker-compose logs -f nginx
docker-compose logs -f db

# Django logs
docker-compose exec web tail -f /var/log/gunicorn/error.log
```

### Performance Monitoring
```bash
# Container resource usage
docker stats

# PostgreSQL performance
docker-compose exec db psql -U ecommerce_user -d ecommerce_db \
  -c "SELECT * FROM pg_stat_activity;"

# Redis info
docker-compose exec redis redis-cli info
```

---

## 🐛 Troubleshooting

### Common Issues

#### Container Won't Start
```bash
# Check logs
docker-compose logs service_name

# Check container status
docker-compose ps

# Rebuild image
docker-compose build --no-cache service_name
```

#### Database Connection Issues
```bash
# Check database health
docker-compose exec db pg_isready -U ecommerce_user

# Check network connectivity
docker-compose exec web ping db

# Reset database
docker-compose down -v db
docker-compose up -d db
```

#### Permission Issues
```bash
# Fix file permissions
sudo chown -R $USER:$USER .
sudo chmod -R 755 .

# Fix volume permissions
docker-compose exec web chown -R appuser:appuser /app
```

#### SSL Issues
```bash
# Check certificate validity
openssl x509 -in ssl/cert.pem -text -noout

# Test SSL configuration
docker-compose exec nginx nginx -t

# Check SSL logs
docker-compose logs nginx | grep ssl
```

---

## 🔄 Backup and Restore

### Full Backup
```bash
#!/bin/bash
# backup.sh
DATE=$(date +%Y%m%d_%H%M%S)

# Database backup
docker-compose exec -T db pg_dump -U ecommerce_user ecommerce_db > "backup_db_${DATE}.sql"

# Media files backup
docker cp $(docker-compose ps -q web):/app/media "./backup_media_${DATE}"

# Configuration backup
tar -czf "backup_config_${DATE}.tar.gz" docker-compose.yml nginx/ ssl/
```

### Full Restore
```bash
#!/bin/bash
# restore.sh
BACKUP_DATE=$1

# Restore database
docker-compose exec -T db psql -U ecommerce_user -d ecommerce_db < "backup_db_${BACKUP_DATE}.sql"

# Restore media files
docker cp "./backup_media_${BACKUP_DATE}" $(docker-compose ps -q web):/app/media

# Restart services
docker-compose restart web
```

---

## 🌐 Cloud Deployment

### AWS EC2 with Docker
```bash
# Install Docker on EC2
sudo yum update -y
sudo yum install -y docker
sudo service docker start
sudo usermod -a -G docker ec2-user

# Clone and run
git clone https://github.com/messkely/alx-project-nexus.git
cd alx-project-nexus
make docker-prod
```

### Digital Ocean Droplet
```bash
# Use Docker Droplet or install Docker
git clone https://github.com/messkely/alx-project-nexus.git
cd alx-project-nexus
make docker-prod
```

### Google Cloud Run
```bash
# Build and push to Google Container Registry
docker build -t gcr.io/PROJECT_ID/alx-ecommerce .
docker push gcr.io/PROJECT_ID/alx-ecommerce
gcloud run deploy --image gcr.io/PROJECT_ID/alx-ecommerce
```

---

## ⚡ Quick Reference

### Essential Commands
```bash
# Development
make docker-dev          # Start development
make docker-shell        # Access Django shell
make docker-logs         # View logs

# Production  
make docker-prod         # Start production
make docker-status       # Check status
make docker-down         # Stop all

# Maintenance
make docker-clean        # Clean up resources
docker-compose restart   # Restart services
docker-compose build     # Rebuild images
```

### Access Points

**Development:**
- App: http://localhost:8000/
- Admin: http://localhost:8000/admin/
- DB: localhost:5433

**Production:**
- App: http://localhost/
- Admin: http://localhost/admin/
- SSL: https://yourdomain.com/

### Important Paths
```
├── Dockerfile              # Production image
├── Dockerfile.dev          # Development image  
├── docker-compose.yml      # Production services
├── docker-compose.dev.yml  # Development services
├── .dockerignore          # Docker ignore patterns
├── nginx/                 # Nginx configuration
└── ssl/                   # SSL certificates
```

---

**Need help?** Check the troubleshooting section above or review container logs for detailed error information.
