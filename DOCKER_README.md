# 🐳 Docker Production Deployment Guide

This guide explains how to deploy the ALX E-Commerce Backend using Docker in production environments.

## 📋 Prerequisites

- Docker Engine 24.0+
- Docker Compose V2
- 4GB+ RAM available
- 20GB+ disk space
- Domain name (for SSL)
- VPS or cloud server

## 🚀 Quick Start

### Production Deployment (Recommended)
```bash
# Clone repository
git clone https://github.com/messkely/alx-project-nexus.git
cd alx-project-nexus

# Configure production environment
cp .env.prod.example .env.prod
# Edit .env.prod with your settings

# Run automated deployment
chmod +x deploy.sh
./deploy.sh init
```

### Development Setup (Local Only)
```bash
# For local development only
cp .env.example .env
# Edit .env for development settings

# Use local development server (not containerized)
python manage.py runserver
```

## 🏗️ Production Architecture

The Docker production setup includes:

- **web**: Django application (Gunicorn + Python 3.11)
- **db**: PostgreSQL 15 database with health checks
- **redis**: Redis 7 for caching and sessions
- **nginx**: Nginx reverse proxy with SSL termination

## 🔧 Production Configuration

### Environment Variables (.env.prod)

**Critical settings to configure:**

| Variable | Description | Example |
|----------|-------------|---------|
| `DEBUG` | Django debug mode | `False` |
| `DJANGO_SECRET_KEY` | Django secret key (50+ chars) | `your-super-secure-key...` |
| `DJANGO_ALLOWED_HOSTS` | Allowed hostnames | `yourdomain.com,www.yourdomain.com` |
| `DB_NAME` | Database name | `ecommerce_prod` |
| `DB_USER` | Database user | `ecommerce_user` |
| `DB_PASSWORD` | Database password | `secure-db-password` |
| `REDIS_URL` | Redis connection | `redis://redis:6379/0` |

### Docker Compose Configuration

The production setup uses `docker-compose.production.yml` which includes:
- Multi-stage production Docker builds
- Network isolation and security
- Health checks for all services
- Volume management for persistence
- SSL certificate handling
- Automated backups

## 📊 Production Features

### Security
- ✅ Non-root container execution
- ✅ Network isolation between services
- ✅ SSL/TLS encryption with Let's Encrypt
- ✅ Security headers via Nginx
- ✅ Rate limiting protection
- ✅ Database connection security

### Performance
- ✅ Gunicorn multi-worker setup
- ✅ Redis caching layer
- ✅ Nginx static file serving
- ✅ Database connection pooling
- ✅ Optimized Docker image layers

### Monitoring
- ✅ Container health checks
- ✅ Application logging
- ✅ Database monitoring
- ✅ SSL certificate monitoring

## 🛠️ Deployment Commands

### Initial Setup
```bash
# Initialize production environment
./deploy.sh init

# Setup SSL certificates
./deploy.sh ssl yourdomain.com
```

### Management
```bash
# Check service status
./deploy.sh status

# View application logs
./deploy.sh logs

# Create database backup
./deploy.sh backup

# Update deployment
./deploy.sh update
```

### Manual Operations
```bash
# Access Django shell
docker compose -f docker-compose.production.yml exec web python manage.py shell

# Run migrations
docker compose -f docker-compose.production.yml exec web python manage.py migrate

# Create superuser
docker compose -f docker-compose.production.yml exec web python manage.py createsuperuser
```

## 🔍 Troubleshooting

### Common Issues

1. **Port Conflicts:**
   ```bash
   # Check if ports are in use
   sudo netstat -tulpn | grep :80
   sudo netstat -tulpn | grep :443
   ```

2. **Database Connection Issues:**
   ```bash
   # Check database status
   docker compose -f docker-compose.production.yml exec db pg_isready -U ecommerce_user -d ecommerce
   
   # View database logs
   docker compose -f docker-compose.production.yml logs db
   ```

3. **SSL Certificate Issues:**
   ```bash
   # Check certificate status
   ./deploy.sh ssl-status yourdomain.com
   
   # Renew certificates
   ./deploy.sh ssl-renew yourdomain.com
   ```

## 📈 Performance Optimization

### Container Optimization
```bash
# Remove unused Docker objects
docker system prune -f

# Optimize image sizes
docker images --format "table {{.Repository}}\t{{.Tag}}\t{{.Size}}"
```

## � Backup and Recovery

### Automated Backups
```bash
# Manual backup
./deploy.sh backup

# Schedule automatic backups (add to crontab)
0 2 * * * /path/to/deploy.sh backup
```

### Recovery Process
```bash
# Restore from backup
./deploy.sh restore /path/to/backup/file
```

---

**Built for production deployment with enterprise-grade security and performance.**

   ```

4. **Memory Issues:**
   ```bash
   # Check Docker resource usage
   docker stats
   
   # Increase Docker memory limits in Docker Desktop
   ```

### Health Checks

The application includes health checks:
- Web service: `http://localhost:8000/api/v1/health/`
- Database: `pg_isready` command
- Redis: `redis-cli ping` command

## 📈 Monitoring

### Application Metrics
```bash
# View resource usage
docker stats

# Service health
docker compose ps

# Application logs
docker compose logs web

# Database performance
docker compose exec db pg_stat_activity
```

### Log Locations
- Application logs: `./logs/`
- Nginx logs: Inside nginx container at `/var/log/nginx/`
- PostgreSQL logs: Docker logs via `docker compose logs db`

## 🔄 Updates and Maintenance

### Updating the Application
```bash
# Pull latest changes
git pull origin main

# Rebuild containers
docker compose up --build -d

# Run migrations
docker compose exec web python manage.py migrate

# Collect static files
docker compose exec web python manage.py collectstatic --noinput
```

### Database Migrations
```bash
# Create migration
docker compose exec web python manage.py makemigrations

# Apply migrations
docker compose exec web python manage.py migrate

# View migration status
docker compose exec web python manage.py showmigrations
```

## 🌍 Production Deployment

For production deployment:

1. **Set up SSL certificates** in `./ssl/` directory
2. **Configure domain** in Nginx configuration
3. **Set strong passwords** in `.env` file
4. **Enable SSL redirect** in Nginx config
5. **Set up monitoring** and log aggregation
6. **Configure backup** strategies
7. **Set up CI/CD** pipeline

## 📚 Additional Resources

- [Django Documentation](https://docs.djangoproject.com/)
- [Docker Documentation](https://docs.docker.com/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [Nginx Documentation](https://nginx.org/en/docs/)
- [Redis Documentation](https://redis.io/documentation)

## 🐛 Support

If you encounter issues:
1. Check the troubleshooting section above
2. Review Docker and application logs
3. Verify your environment configuration
4. Check GitHub issues for similar problems
