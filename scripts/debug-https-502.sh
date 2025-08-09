#!/bin/bash
# Debug and fix HTTPS 502 Bad Gateway error

echo "🔍 Debugging HTTPS 502 Bad Gateway Error"
echo "========================================"

cd ~/alx-project-nexus

echo "1. Checking container status..."
echo "=============================="
docker compose -f docker-compose.https.yml ps

echo ""
echo "2. Checking Django container health..."
echo "====================================="
echo "Django container logs (last 20 lines):"
docker compose -f docker-compose.https.yml logs --tail=20 web

echo ""
echo "3. Testing Django directly..."
echo "============================"
echo "Testing Django health endpoint internally:"
docker exec ecommerce_web_prod curl -f http://localhost:8000/health/ 2>/dev/null || echo "❌ Django internal health check failed"

echo ""
echo "4. Testing network connectivity..."
echo "================================="
echo "Testing if Nginx can reach Django:"
docker exec ecommerce_nginx_prod curl -f http://web:8000/health/ 2>/dev/null || echo "❌ Nginx->Django connection failed"

echo ""
echo "5. Checking Nginx configuration..."
echo "================================="
echo "Testing Nginx config syntax:"
docker exec ecommerce_nginx_prod nginx -t

echo ""
echo "6. Checking Nginx error logs..."
echo "=============================="
docker exec ecommerce_nginx_prod cat /var/log/nginx/error.log | tail -15

echo ""
echo "7. Network inspection..."
echo "======================="
echo "Docker network information:"
docker network ls | grep alx
docker inspect $(docker compose -f docker-compose.https.yml ps -q) | grep -A 5 -B 5 NetworkMode || echo "Network inspection failed"

echo ""
echo "8. Attempting to fix common issues..."
echo "===================================="

# Check if web service is actually running
WEB_STATUS=$(docker compose -f docker-compose.https.yml ps web --format "table {{.Status}}" | tail -1)
echo "Web service status: $WEB_STATUS"

if [[ "$WEB_STATUS" == *"Up"* ]]; then
    echo "✅ Web service is running"
else
    echo "❌ Web service is not running properly - restarting..."
    docker compose -f docker-compose.https.yml restart web
    sleep 15
fi

# Test Django startup
echo ""
echo "9. Testing Django startup..."
echo "============================"
docker exec ecommerce_web_prod ps aux | grep gunicorn || echo "Gunicorn not running"
docker exec ecommerce_web_prod netstat -tlnp | grep :8000 || echo "Port 8000 not listening"

echo ""
echo "10. Attempting to restart services..."
echo "===================================="
echo "Restarting Nginx..."
docker compose -f docker-compose.https.yml restart nginx
sleep 5

echo "Testing after restart..."
curl -k -s -w "Status: %{http_code}\n" https://3.80.35.89/health/ | head -3

echo ""
echo "11. Final diagnosis..."
echo "===================="
docker compose -f docker-compose.https.yml ps
echo ""
echo "If still not working, try:"
echo "1. docker compose -f docker-compose.https.yml logs web"
echo "2. docker compose -f docker-compose.https.yml restart"
echo "3. sudo ./scripts/fix-https-conflicts.sh (full restart)"
