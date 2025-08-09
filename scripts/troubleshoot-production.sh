#!/bin/bash
# Troubleshooting script for production update issues
# Run this on EC2 when update script shows health check failures

set -e

echo "🔍 ALX E-Commerce Production Troubleshooting"
echo "=============================================="

cd ~/alx-project-nexus

echo ""
echo "1. 📊 Container Status:"
echo "----------------------"
docker compose -f docker-compose.prod.yml ps

echo ""
echo "2. 🔍 Container Health Details:"
echo "-------------------------------"
docker inspect ecommerce_web_prod --format='{{.State.Health.Status}}'
echo "Web container health: $(docker inspect ecommerce_web_prod --format='{{.State.Health.Status}}')"

echo ""
echo "3. 📋 Recent Web Container Logs:"
echo "--------------------------------"
docker compose -f docker-compose.prod.yml logs --tail=30 web

echo ""
echo "4. 📋 Recent Nginx Logs:"
echo "------------------------"
docker compose -f docker-compose.prod.yml logs --tail=10 nginx

echo ""
echo "5. 🌐 Network Connectivity:"
echo "---------------------------"
echo "Testing internal connectivity..."
docker compose -f docker-compose.prod.yml exec web curl -f http://localhost:8000/health/ 2>/dev/null && echo "✅ Internal health check OK" || echo "❌ Internal health check failed"

echo ""
echo "6. 🔧 Port Status:"
echo "------------------"
echo "Checking if ports are bound:"
sudo netstat -tlnp | grep ':80\|:443\|:8000' || echo "No ports found"

echo ""
echo "7. 🧪 DNS Resolution:"
echo "--------------------"
nslookup ecom-backend.store || echo "DNS resolution issue"

echo ""
echo "8. 🚀 Quick Fixes to Try:"
echo "-------------------------"
echo "If web container is unhealthy:"
echo "  docker compose -f docker-compose.prod.yml restart web"
echo ""
echo "If nginx is not working:"
echo "  docker compose -f docker-compose.prod.yml restart nginx"
echo ""
echo "If SSL certificate issues:"
echo "  sudo certbot certificates"
echo "  docker compose -f docker-compose.prod.yml restart nginx"
echo ""
echo "Full restart:"
echo "  docker compose -f docker-compose.prod.yml down"
echo "  docker compose -f docker-compose.prod.yml up -d"

echo ""
echo "9. 🔄 Testing External Access:"
echo "------------------------------"
sleep 5  # Give services more time
echo "Testing external HTTPS..."
curl -I --connect-timeout 10 https://ecom-backend.store/ 2>&1 || echo "External HTTPS test failed"

echo ""
echo "Testing external HTTP..."
curl -I --connect-timeout 10 http://ecom-backend.store/ 2>&1 || echo "External HTTP test failed"

echo ""
echo "🎯 Troubleshooting completed!"
echo "Check the logs above for specific error messages."
