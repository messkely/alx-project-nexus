#!/bin/bash
# Quick test script for EC2 deployment
# Usage: ./test-ec2-connection.sh

EC2_IP="3.80.35.89"

echo "🔍 Testing ALX E-Commerce Backend on EC2: $EC2_IP"
echo "=================================================="

# Test health endpoint
echo "1. Testing health endpoint..."
if curl -f -s "http://$EC2_IP/health/" > /dev/null; then
    echo "✅ Health check: OK"
else
    echo "❌ Health check: FAILED"
fi

# Test API endpoint
echo "2. Testing API endpoint..."
if curl -f -s "http://$EC2_IP/api/v1/products/" > /dev/null; then
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
