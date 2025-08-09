# EC2 Production Troubleshooting Guide

## Quick Commands for Your EC2 Instance

### 1. Start All Services
```bash
sudo ./scripts/start-ec2-production.sh
```

### 2. Check Service Status
```bash
# Check all containers
docker compose -f docker-compose.prod.yml ps

# Check specific service
docker compose -f docker-compose.prod.yml ps web
docker compose -f docker-compose.prod.yml ps db
docker compose -f docker-compose.prod.yml ps redis
docker compose -f docker-compose.prod.yml ps nginx
```

### 3. View Logs (Correct Service Names)
```bash
# Django application logs
docker compose -f docker-compose.prod.yml logs web

# Database logs
docker compose -f docker-compose.prod.yml logs db

# Redis logs
docker compose -f docker-compose.prod.yml logs redis

# Nginx logs
docker compose -f docker-compose.prod.yml logs nginx

# All logs together
docker compose -f docker-compose.prod.yml logs -f
```

### 4. Test Endpoints
```bash
# Health check
curl http://3.80.35.89/api/health/

# API documentation
curl http://3.80.35.89/api/docs/

# Test internal networking
curl http://localhost/api/health/
```

### 5. Restart Individual Services
```bash
# Restart Django
docker compose -f docker-compose.prod.yml restart web

# Restart all services
docker compose -f docker-compose.prod.yml restart
```

### 6. Emergency Commands
```bash
# Stop everything
docker compose -f docker-compose.prod.yml down

# Force restart everything
docker compose -f docker-compose.prod.yml down
docker system prune -f
docker compose -f docker-compose.prod.yml up -d --build

# Check system resources
docker stats
df -h
free -h
```

### 7. Common Issues & Solutions

#### Issue: Services not starting
**Solution:**
```bash
# Check if ports are blocked
sudo netstat -tulpn | grep -E ':(80|443|5432|6379|8000)'

# Kill conflicting processes
sudo fuser -k 80/tcp
sudo fuser -k 443/tcp

# Restart services
sudo ./scripts/start-ec2-production.sh
```

#### Issue: Database connection failed
**Solution:**
```bash
# Check database health
docker compose -f docker-compose.prod.yml logs db

# Restart database
docker compose -f docker-compose.prod.yml restart db
```

#### Issue: Redis connection failed
**Solution:**
```bash
# Check Redis health
docker compose -f docker-compose.prod.yml logs redis

# Restart Redis
docker compose -f docker-compose.prod.yml restart redis
```

### 8. File Locations on EC2
```
Project Directory: ~/alx-project-nexus/
Logs: ~/alx-project-nexus/logs/
SSL Certificates: ~/alx-project-nexus/ssl/
Nginx Config: ~/alx-project-nexus/nginx/
Scripts: ~/alx-project-nexus/scripts/
```

### 9. Service Names Reference
- **Django App**: `web` (not `django`)
- **PostgreSQL**: `db`
- **Redis**: `redis`
- **Nginx**: `nginx`

### 10. URLs and Ports
- **Public URL**: http://3.80.35.89
- **Internal Django**: http://web:8000
- **Internal DB**: db:5432
- **Internal Redis**: redis:6379
- **Nginx**: ports 80 and 443
