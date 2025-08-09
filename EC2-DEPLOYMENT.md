# 🚀 ALX E-Commerce Backend - AWS EC2 Production Deployment

## 🎯 Overview
Production-ready deployment of ALX E-Commerce Backend on AWS EC2 instance **3.80.35.89**.

### ✅ What's Included
- **Docker containerized services** (Django + PostgreSQL + Redis + Nginx)
- **Production security configurations**
- **SSL-ready Nginx with rate limiting**
- **Automated deployment scripts**
- **Health monitoring and logging**
- **Firewall configuration (UFW)**

---

## 🏗️ Quick Deployment

### 1. Connect to Your EC2 Instance
```bash
ssh -i your-key.pem ubuntu@3.80.35.89
```

### 2. Deploy the Application
```bash
# Clone the repository
git clone https://github.com/messkely/alx-project-nexus.git
cd alx-project-nexus

# Run the automated deployment
sudo ./scripts/deploy-ec2-production.sh setup
```

### 3. Access Your Application
- **API Documentation**: http://3.80.35.89/
- **Admin Panel**: http://3.80.35.89/admin/
- **Health Check**: http://3.80.35.89/health/
- **API Endpoints**: http://3.80.35.89/api/v1/

---

## 📋 Management Commands

### Using Makefile (Recommended)
```bash
# Full deployment
make ec2-deploy

# Update application
make ec2-update

# Check status
make ec2-status

# View logs
make ec2-logs

# Restart services
make ec2-restart
```

### Using Script Directly
```bash
# Setup (initial deployment)
./scripts/deploy-ec2-production.sh setup

# Start services
./scripts/deploy-ec2-production.sh start

# Stop services
./scripts/deploy-ec2-production.sh stop

# Restart services
./scripts/deploy-ec2-production.sh restart

# Check status
./scripts/deploy-ec2-production.sh status

# View logs
./scripts/deploy-ec2-production.sh logs

# Update from git
./scripts/deploy-ec2-production.sh update
```

---

## 🔧 Service Management

### Docker Commands
```bash
# View all containers
docker ps

# View specific service logs
docker compose -f docker-compose.prod.yml logs web
docker compose -f docker-compose.prod.yml logs db
docker compose -f docker-compose.prod.yml logs redis
docker compose -f docker-compose.prod.yml logs nginx

# Execute commands in containers
docker compose -f docker-compose.prod.yml exec web python manage.py createsuperuser
docker compose -f docker-compose.prod.yml exec web python manage.py migrate
docker compose -f docker-compose.prod.yml exec db psql -U ecommerce_user -d ecommerce_db
```

### Django Management
```bash
# Create admin user
docker compose -f docker-compose.prod.yml exec web python manage.py createsuperuser

# Run migrations
docker compose -f docker-compose.prod.yml exec web python manage.py migrate

# Collect static files
docker compose -f docker-compose.prod.yml exec web python manage.py collectstatic --noinput

# Load sample data
docker compose -f docker-compose.prod.yml exec web python manage.py loaddata catalog/fixtures/sample_data.json
```

---

## 🔐 Security Features

### 🛡️ Implemented Security
- **Firewall (UFW)**: Only ports 22, 80, 443 open
- **Rate Limiting**: API and auth endpoints protected
- **Security Headers**: XSS, CSRF, Content-Type protection
- **Container Isolation**: Services run in separate containers
- **Non-root Users**: Containers run with limited privileges
- **Input Validation**: Django built-in protections

### 🔧 Security Configuration
```bash
# Check firewall status
sudo ufw status verbose

# View nginx rate limiting logs
docker compose -f docker-compose.prod.yml logs nginx | grep limit

# Monitor failed requests
docker compose -f docker-compose.prod.yml logs nginx | grep 40[0-9]
```

---

## 📊 Monitoring & Health Checks

### Health Endpoints
```bash
# Application health
curl http://3.80.35.89/health/

# API availability
curl http://3.80.35.89/api/v1/products/

# Database connectivity
docker compose -f docker-compose.prod.yml exec web python manage.py check --database default
```

### System Monitoring
```bash
# Container resource usage
docker stats

# System resources
htop

# Disk usage
df -h

# Network connections
sudo netstat -tlnp
```

---

## 🔧 Troubleshooting

### Common Issues & Solutions

#### 🚨 Service Won't Start
```bash
# Check container status
docker compose -f docker-compose.prod.yml ps

# View detailed logs
docker compose -f docker-compose.prod.yml logs

# Restart specific service
docker compose -f docker-compose.prod.yml restart web
```

#### 🚨 Database Connection Issues
```bash
# Check database container
docker compose -f docker-compose.prod.yml logs db

# Test database connectivity
docker compose -f docker-compose.prod.yml exec web python manage.py check --database default

# Reset database (⚠️ DATA LOSS)
docker compose -f docker-compose.prod.yml exec web python manage.py migrate --run-syncdb
```

#### 🚨 Nginx Configuration Issues
```bash
# Test nginx configuration
docker compose -f docker-compose.prod.yml exec nginx nginx -t

# Reload nginx
docker compose -f docker-compose.prod.yml exec nginx nginx -s reload

# Check nginx logs
docker compose -f docker-compose.prod.yml logs nginx
```

#### 🚨 Port Access Issues
```bash
# Check if ports are listening
sudo netstat -tlnp | grep :80
sudo netstat -tlnp | grep :443

# Check firewall rules
sudo ufw status numbered

# Test from another machine
curl -I http://3.80.35.89/health/
```

---

## 🔄 Updates & Maintenance

### Automated Updates
```bash
# Update application code and restart
./scripts/deploy-ec2-production.sh update
```

### Manual Updates
```bash
# Pull latest code
git pull origin main

# Rebuild containers
docker compose -f docker-compose.prod.yml build --no-cache

# Restart services
docker compose -f docker-compose.prod.yml up -d
```

### Database Backups
```bash
# Create backup
docker compose -f docker-compose.prod.yml exec db pg_dump -U ecommerce_user ecommerce_db > backup_$(date +%Y%m%d_%H%M%S).sql

# Restore backup
docker compose -f docker-compose.prod.yml exec db psql -U ecommerce_user ecommerce_db < backup_file.sql
```

---

## 📝 Configuration Files

### Key Files
- `docker-compose.prod.yml` - Production Docker Compose
- `nginx/ec2-production.conf` - Nginx production config
- `.env.production` - Environment variables
- `scripts/deploy-ec2-production.sh` - Deployment script

### Environment Variables
Located in `docker-compose.prod.yml`:
- **SECRET_KEY**: Django secret key
- **ALLOWED_HOSTS**: Includes `3.80.35.89`
- **Database**: PostgreSQL credentials
- **Redis**: Cache configuration

---

## 🆘 Support & Documentation

### Additional Resources
- **Main Documentation**: `docs/EC2_DEPLOYMENT.md`
- **API Documentation**: http://3.80.35.89/ (when deployed)
- **GitHub Repository**: https://github.com/messkely/alx-project-nexus

### Getting Help
1. Check the logs: `./scripts/deploy-ec2-production.sh logs`
2. Verify service status: `./scripts/deploy-ec2-production.sh status`
3. Review configuration files
4. Check GitHub issues

---

**🎉 Your ALX E-Commerce Backend is production-ready on AWS EC2!**
