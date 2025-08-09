#!/bin/bash
# Test HTTPS functionality for ALX E-Commerce

echo "🔒 Testing HTTPS Configuration"
echo "=============================="

# Test variables
DOMAIN="3.80.35.89"

echo "1. Testing SSL certificate..."
echo "============================"
openssl s_client -connect $DOMAIN:443 -servername $DOMAIN < /dev/null 2>/dev/null | openssl x509 -noout -dates
echo ""

echo "2. Testing HTTPS endpoints..."
echo "============================"

echo "HTTPS Health Check:"
curl -k -w "Status: %{http_code} | Time: %{time_total}s\n" -s https://$DOMAIN/health/ | head -2

echo ""
echo "HTTPS API Health:"
curl -k -w "Status: %{http_code} | Time: %{time_total}s\n" -s https://$DOMAIN/api/v1/health/ | head -2

echo ""
echo "HTTPS Main Page:"
curl -k -w "Status: %{http_code} | Time: %{time_total}s\n" -s https://$DOMAIN/ | head -5

echo ""
echo "3. Testing HTTP to HTTPS redirect..."
echo "===================================="
echo "HTTP Health Check (should redirect):"
curl -s -I http://$DOMAIN/health/ | head -5

echo ""
echo "4. Testing SSL security..."
echo "=========================="
echo "SSL Grade Test:"
curl -s "https://api.ssllabs.com/api/v3/analyze?host=$DOMAIN" | grep -o '"grade":"[A-F][+-]*"' || echo "SSL Labs test not available"

echo ""
echo "5. Security headers check..."
echo "============================"
echo "HTTPS Security Headers:"
curl -k -s -I https://$DOMAIN/health/ | grep -E "(Strict-Transport-Security|X-Frame-Options|X-Content-Type-Options)"

echo ""
echo "✅ HTTPS test complete!"
echo ""
echo "🌐 Your secure URLs:"
echo "• https://$DOMAIN/"
echo "• https://$DOMAIN/health/"
echo "• https://$DOMAIN/api/v1/docs/"
echo "• https://$DOMAIN/admin/"
