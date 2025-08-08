# 🐳 Docker Deployment Guide

This guide explains how to deploy the Django E-commerce API using Docker and Docker Compose.

## 📋 Prerequisites

- Docker Engine 20.10+
- Docker Com   ```bash
   # Change ports in docker-compose.yml
   ports:
     - "8001:8000"  # Use different host port
   ```

2. **Database Connection Issues:**
   ```bash
   # Check database status
   docker compose exec db pg_isready -U ecommerce_user -d ecommerce
   
   # View database logs
   docker compose logs db
   ```B+ RAM available
- 10GB+ disk space

## 🚀 Quick Start

### Option 1: Automated Setup (Recommended)
```bash
./docker-setup.sh
```

### Option 2: Manual Setup

1. **Clone and navigate to the project:**
   ```bash
   git clone <repository-url>
   cd alx-project-nexus
   ```

2. **Create environment file:**
   ```bash
   cp .env.example .env
   # Edit .env file with your configuration
   ```

3. **Choose your environment:**

   **Development:**
   ```bash
   docker compose -f docker-compose.yml -f docker-compose.dev.yml up --build
   ```

   **Production:**
   ```bash
   docker compose -f docker-compose.yml -f docker-compose.prod.yml up --build
   ```

## 🏗️ Architecture

The Docker setup includes the following services:

- **web**: Django application (Python 3.11)
- **db**: PostgreSQL 15 database
- **redis**: Redis for caching and sessions
- **nginx**: Reverse proxy (production only)

## 🔧 Configuration

### Environment Variables (.env)

| Variable | Description | Default |
|----------|-------------|---------|
| `DEBUG` | Django debug mode | `False` |
| `SECRET_KEY` | Django secret key | Required |
| `DATABASE_URL` | PostgreSQL connection string | Auto-configured |
| `REDIS_URL` | Redis connection string | Auto-configured |
| `ALLOWED_HOSTS` | Comma-separated allowed hosts | `localhost,127.0.0.1` |

### Docker Compose Files

- `docker-compose.yml`: Base configuration
- `docker-compose.dev.yml`: Development overrides
- `docker-compose.prod.yml`: Production overrides

## 📊 Development Environment

The development setup includes:
- Hot code reloading
- Debug mode enabled
- Direct port access (8000)
- Volume mounting for live editing
- Django development server

**Access Points:**
- API: http://localhost:8000/api/v1/
- Admin: http://localhost:8000/admin/
- API Docs: http://localhost:8000/api/v1/docs/

## 🏭 Production Environment

The production setup includes:
- Nginx reverse proxy
- Static file serving
- SSL-ready configuration
- Health checks
- Automatic restarts
- Security hardening

**Access Points:**
- Application: http://localhost/
- Admin: http://localhost/admin/
- API Docs: http://localhost/api/v1/docs/

## 🛠️ Common Commands

### Container Management
```bash
# Start services
docker compose up -d

# Stop services
docker compose down

# Rebuild and start
docker compose up --build

# View logs
docker compose logs -f [service_name]

# Scale web service
docker compose up -d --scale web=3
```

### Django Management
```bash
# Run migrations
docker compose exec web python manage.py migrate

# Create superuser
docker compose exec web python manage.py createsuperuser

# Collect static files
docker compose exec web python manage.py collectstatic --noinput

# Django shell
docker compose exec web python manage.py shell

# Run tests
docker compose exec web python manage.py test

# Load seed data
docker compose exec web python manage.py loaddata fixture.json
```

### Database Operations
```bash
# Database shell
docker compose exec db psql -U ecommerce_user -d ecommerce

# Backup database
docker compose exec db pg_dump -U ecommerce_user ecommerce > backup.sql

# Restore database
docker compose exec -T db psql -U ecommerce_user ecommerce < backup.sql

# View database logs
docker compose logs db
```

## 🔒 Security Considerations

### Development
- Uses insecure secret keys
- Debug mode enabled
- Direct port access
- No SSL/HTTPS

### Production
- Strong secret keys required
- Debug mode disabled
- Access through Nginx only
- SSL/HTTPS ready
- Security headers configured
- Rate limiting enabled

## 🚨 Troubleshooting

### Common Issues

1. **Port Already in Use:**
   ```bash
   # Check what's using the port
   sudo netstat -tulpn | grep :8000
   
   # Change ports in docker-compose.yml
   ports:
     - "8001:8000"  # Use different host port
   ```

2. **Database Connection Issues:**
   ```bash
   # Check database status
   docker-compose exec db pg_isready -U ecommerce_user -d ecommerce
   
   # View database logs
   docker-compose logs db
   ```

3. **Permission Issues:**
   ```bash
   # Fix ownership issues
   sudo chown -R $USER:$USER .
   
   # Fix permissions
   chmod 644 .env
   chmod +x docker-setup.sh
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
