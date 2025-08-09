#!/bin/bash
# Quick fix for port conflicts on EC2
# Run this on your EC2 instance to resolve port conflicts

set -e

echo "🔧 Fixing port conflicts on EC2..."
echo "================================="

# Stop any conflicting services
echo "1. Stopping conflicting services..."
sudo systemctl stop redis-server 2>/dev/null || echo "Redis not running as service"
sudo systemctl stop postgresql 2>/dev/null || echo "PostgreSQL not running as service" 
sudo systemctl stop nginx 2>/dev/null || echo "Nginx not running as service"

# Kill any processes using our ports
echo "2. Freeing up ports..."
sudo fuser -k 6379/tcp 2>/dev/null || echo "Port 6379 already free"
sudo fuser -k 5432/tcp 2>/dev/null || echo "Port 5432 already free"
sudo fuser -k 80/tcp 2>/dev/null || echo "Port 80 already free"
sudo fuser -k 443/tcp 2>/dev/null || echo "Port 443 already free"

# Clean up any existing Docker containers
echo "3. Cleaning up Docker containers..."
cd /opt/alx-ecommerce 2>/dev/null || cd ~/alx-project-nexus
docker compose -f docker-compose.prod.yml down 2>/dev/null || echo "No containers to stop"
docker system prune -f

echo "4. Starting services..."
docker compose -f docker-compose.prod.yml up -d

echo "✅ Fix complete! Services should be running now."
echo ""
echo "Check status with:"
echo "docker compose -f docker-compose.prod.yml ps"
