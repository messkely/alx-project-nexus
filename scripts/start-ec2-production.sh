#!/bin/bash
# Start Production Services on EC2
# Run this on your EC2 instance: sudo ./scripts/start-ec2-production.sh

set -e

echo "🚀 Starting ALX E-commerce Production on EC2"
echo "============================================="

# Navigate to project directory
cd ~/alx-project-nexus 2>/dev/null || cd /opt/alx-ecommerce

# Stop conflicting services first
echo "1. Stopping conflicting services..."
sudo systemctl stop redis-server 2>/dev/null || echo "✓ Redis service not running"
sudo systemctl stop postgresql 2>/dev/null || echo "✓ PostgreSQL service not running" 
sudo systemctl stop nginx 2>/dev/null || echo "✓ Nginx service not running"

# Free up ports
echo "2. Freeing up ports..."
sudo fuser -k 6379/tcp 2>/dev/null || echo "✓ Port 6379 free"
sudo fuser -k 5432/tcp 2>/dev/null || echo "✓ Port 5432 free"
sudo fuser -k 80/tcp 2>/dev/null || echo "✓ Port 80 free"
sudo fuser -k 443/tcp 2>/dev/null || echo "✓ Port 443 free"

# Clean up existing containers
echo "3. Cleaning up existing containers..."
docker compose -f docker-compose.prod.yml down 2>/dev/null || echo "✓ No containers to stop"
docker system prune -f

# Build and start services
echo "4. Building and starting services..."
docker compose -f docker-compose.prod.yml build --no-cache
docker compose -f docker-compose.prod.yml up -d

echo "5. Waiting for services to be ready..."
sleep 30

echo "6. Checking service status..."
docker compose -f docker-compose.prod.yml ps

echo ""
echo "✅ Production deployment complete!"
echo ""
echo "🔍 Service Status:"
echo "=================="
docker compose -f docker-compose.prod.yml ps

echo ""
echo "🌐 Test URLs:"
echo "============="
echo "Health Check: curl http://3.80.35.89/api/health/"
echo "API Docs: http://3.80.35.89/api/docs/"
echo "Admin Panel: http://3.80.35.89/admin/"

echo ""
echo "📋 Useful Commands:"
echo "=================="
echo "View logs: docker compose -f docker-compose.prod.yml logs web"
echo "View all logs: docker compose -f docker-compose.prod.yml logs"
echo "Restart services: docker compose -f docker-compose.prod.yml restart"
echo "Stop services: docker compose -f docker-compose.prod.yml down"

# Test the health endpoint
echo ""
echo "🩺 Testing health endpoint..."
sleep 10
curl -f http://localhost/api/health/ 2>/dev/null && echo "✅ Health check passed!" || echo "❌ Health check failed - check logs"
