#!/bin/bash
# Debug Nginx routing for EC2 deployment
# Usage: ./test-ec2-connection.sh

EC2_IP="3.80.35.89"

echo "🔍 Debugging Nginx Routing on EC2: $EC2_IP"  
echo "=========================================="

echo "1. Testing Django health endpoint paths..."
echo "=========================================="

# Test different health endpoint paths directly on Django
echo "Testing /health/ path on Django:"
docker exec ecommerce_web_prod curl -s -w "HTTP %{http_code}\n" http://localhost:8000/health/ || echo "Failed"

echo "Testing /api/health/ path on Django:"  
docker exec ecommerce_web_prod curl -s -w "HTTP %{http_code}\n" http://localhost:8000/api/health/ || echo "Failed"

echo ""
echo "2. Testing Nginx->Django connectivity..."
echo "========================================"

# Test if Nginx can reach Django at all
echo "Testing basic connection to Django upstream:"
docker exec ecommerce_nginx_prod curl -s -w "HTTP %{http_code}\n" http://web:8000/health/ || echo "Failed"

echo ""
echo "3. Testing Nginx configuration syntax..."
echo "========================================"
docker exec ecommerce_nginx_prod nginx -t

echo ""
echo "4. Checking Nginx error logs..."
echo "==============================="
docker exec ecommerce_nginx_prod cat /var/log/nginx/error.log | tail -10

echo ""
echo "5. Testing all paths through Nginx..."
echo "===================================="

# Test different paths through Nginx
echo "Testing / through Nginx:"
curl -s -w "HTTP %{http_code}\n" http://localhost/ | head -3

echo "Testing /health/ through Nginx:"
curl -s -w "HTTP %{http_code}\n" http://localhost/health/ | head -3

echo "Testing /api/health/ through Nginx:"
curl -s -w "HTTP %{http_code}\n" http://localhost/api/health/ | head -3

echo ""
echo "6. Network connectivity test..."
echo "==============================="
echo "Checking if services can communicate:"
docker exec ecommerce_nginx_prod nslookup web 2>/dev/null || echo "nslookup not available"

echo ""
echo "7. External access test..."
echo "=========================="

# Test external endpoint
echo "Testing external health endpoint..."
if curl -f -s "http://$EC2_IP/health/" > /dev/null; then
    echo "✅ External /health/: OK"
else
    echo "❌ External /health/: FAILED"
fi

# Test API endpoint  
echo "Testing external API endpoint..."
if curl -f -s "http://$EC2_IP/api/health/" > /dev/null; then
    echo "✅ API endpoint: OK"
else
    echo "❌ API endpoint: FAILED"
fi

# Test main page
echo "3. Testing main page (Swagger UI)..."
if curl -f -s "http://$EC2_IP/" > /dev/null; then
    echo "✅ Main page: OK"
else
    echo "❌ Main page: FAILED"
fi

echo ""
echo "📋 Access URLs:"
echo "• Main Page: http://$EC2_IP/"
echo "• Health: http://$EC2_IP/health/"
echo "• Admin: http://$EC2_IP/admin/"
echo "• API: http://$EC2_IP/api/v1/"
echo ""

# Show response times
echo "⏱️ Response times:"
echo "Health:" $(curl -o /dev/null -s -w '%{time_total}s\n' "http://$EC2_IP/health/")
echo "API:" $(curl -o /dev/null -s -w '%{time_total}s\n' "http://$EC2_IP/api/v1/products/")
echo ""

echo "🎉 Test complete!"
