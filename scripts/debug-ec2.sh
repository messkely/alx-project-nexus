#!/bin/bash
# Debug and Fix EC2 Production Deployment
# Run this to diagnose and fix the deployment issues

set -e

echo "🔍 ALX E-commerce Production Debug & Fix"
echo "========================================"

# Navigate to project directory
cd ~/alx-project-nexus 2>/dev/null || cd /opt/alx-ecommerce

echo "1. Checking current Docker status..."
echo "==================================="
docker --version
docker compose version
docker ps -a
echo ""

echo "2. Stopping all containers and cleaning up..."
echo "=============================================="
docker compose -f docker-compose.prod.yml down 2>/dev/null || echo "No containers to stop"
docker system prune -f
docker volume prune -f
echo ""

echo "3. Checking system ports..."
echo "==========================="
sudo netstat -tulpn | grep -E ':(80|443|5432|6379|8000)' || echo "Ports appear to be free"
echo ""

echo "4. Stopping conflicting services..."
echo "===================================="
sudo systemctl stop redis-server 2>/dev/null || echo "✓ Redis not running as service"
sudo systemctl stop postgresql 2>/dev/null || echo "✓ PostgreSQL not running as service"
sudo systemctl stop nginx 2>/dev/null || echo "✓ Nginx not running as service"
sudo systemctl stop apache2 2>/dev/null || echo "✓ Apache not running"

# Kill any remaining processes on our ports
sudo fuser -k 80/tcp 2>/dev/null || echo "✓ Port 80 free"
sudo fuser -k 443/tcp 2>/dev/null || echo "✓ Port 443 free"
sudo fuser -k 5432/tcp 2>/dev/null || echo "✓ Port 5432 free"
sudo fuser -k 6379/tcp 2>/dev/null || echo "✓ Port 6379 free"
sudo fuser -k 8000/tcp 2>/dev/null || echo "✓ Port 8000 free"
echo ""

echo "5. Checking Docker Compose file..."
echo "=================================="
if [ -f "docker-compose.prod.yml" ]; then
    echo "✓ docker-compose.prod.yml exists"
    echo "Services defined:"
    grep -E "^\s+\w+:" docker-compose.prod.yml || echo "Could not parse services"
else
    echo "❌ docker-compose.prod.yml not found!"
    exit 1
fi
echo ""

echo "6. Checking required files..."
echo "============================="
[ -f "Dockerfile" ] && echo "✓ Dockerfile exists" || echo "❌ Dockerfile missing"
[ -f "requirements.txt" ] && echo "✓ requirements.txt exists" || echo "❌ requirements.txt missing"
[ -f "manage.py" ] && echo "✓ manage.py exists" || echo "❌ manage.py missing"
[ -d "nginx" ] && echo "✓ nginx directory exists" || echo "❌ nginx directory missing"
[ -f "nginx/ec2-production.conf" ] && echo "✓ nginx config exists" || echo "❌ nginx config missing"
echo ""

echo "7. Building images with verbose output..."
echo "========================================="
docker compose -f docker-compose.prod.yml build --no-cache --progress=plain

echo ""
echo "8. Starting services one by one..."
echo "=================================="

# Start database first
echo "Starting database..."
docker compose -f docker-compose.prod.yml up -d db
sleep 10

echo "Database status:"
docker compose -f docker-compose.prod.yml ps db
docker compose -f docker-compose.prod.yml logs --tail=20 db

# Start Redis
echo ""
echo "Starting Redis..."
docker compose -f docker-compose.prod.yml up -d redis
sleep 5

echo "Redis status:"
docker compose -f docker-compose.prod.yml ps redis
docker compose -f docker-compose.prod.yml logs --tail=20 redis

# Start Django app
echo ""
echo "Starting Django web application..."
docker compose -f docker-compose.prod.yml up -d web
sleep 20

echo "Django status:"
docker compose -f docker-compose.prod.yml ps web
docker compose -f docker-compose.prod.yml logs --tail=30 web

# Start Nginx
echo ""
echo "Starting Nginx..."
docker compose -f docker-compose.prod.yml up -d nginx
sleep 5

echo "Nginx status:"
docker compose -f docker-compose.prod.yml ps nginx
docker compose -f docker-compose.prod.yml logs --tail=20 nginx

echo ""
echo "9. Final status check..."
echo "========================"
docker compose -f docker-compose.prod.yml ps

echo ""
echo "10. Testing connections..."
echo "=========================="

# Test internal Django
echo "Testing internal Django connection..."
docker exec ecommerce_web_prod curl -f http://localhost:8000/health/ 2>/dev/null && echo "✅ Internal Django OK" || echo "❌ Internal Django failed"

# Test through Nginx
echo "Testing through Nginx..."
curl -f http://localhost/api/health/ 2>/dev/null && echo "✅ Nginx->Django OK" || echo "❌ Nginx->Django failed"

# Test external access
echo "Testing external access..."
curl -f http://3.80.35.89/api/health/ 2>/dev/null && echo "✅ External access OK" || echo "❌ External access failed"

echo ""
echo "11. Summary and Next Steps..."
echo "============================="
echo "If any service failed, check the logs above."
echo "Key commands:"
echo "  View all logs: docker compose -f docker-compose.prod.yml logs -f"
echo "  Restart all: docker compose -f docker-compose.prod.yml restart"
echo "  Check status: docker compose -f docker-compose.prod.yml ps"
echo ""
