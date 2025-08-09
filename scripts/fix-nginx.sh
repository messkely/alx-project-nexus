#!/bin/bash
# Quick fix for Nginx routing issue

echo "🔧 Fixing Nginx Configuration"
echo "============================="

cd ~/alx-project-nexus

echo "1. Reloading Nginx configuration..."
docker compose -f docker-compose.prod.yml restart nginx

echo "2. Waiting for Nginx to restart..."
sleep 5

echo "3. Testing Nginx configuration..."
docker exec ecommerce_nginx_prod nginx -t

echo "4. Testing health endpoints..."
echo ""
echo "Testing /health/ through Nginx:"
curl -s -w "HTTP %{http_code}\n" http://localhost/health/

echo "Testing /api/v1/health/ through Nginx:"
curl -s -w "HTTP %{http_code}\n" http://localhost/api/v1/health/

echo ""
echo "5. Testing external access..."
echo "External /health/:"
curl -s -w "HTTP %{http_code}\n" http://3.80.35.89/health/

echo "External /api/v1/health/:"
curl -s -w "HTTP %{http_code}\n" http://3.80.35.89/api/v1/health/

echo ""
echo "✅ Nginx fix complete!"
echo ""
echo "Test URLs:"
echo "http://3.80.35.89/health/"
echo "http://3.80.35.89/api/v1/health/"
echo "http://3.80.35.89/"
