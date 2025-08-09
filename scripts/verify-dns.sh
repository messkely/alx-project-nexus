#!/bin/bash
# Verify DNS setup for ecom-backend.store domain

DOMAIN="ecom-backend.store"

echo "🔍 DNS Verification for ${DOMAIN}"
echo "================================="

echo "1. Checking current DNS resolution..."
DOMAIN_IP=$(dig +short $DOMAIN | tail -1)
echo "Domain ${DOMAIN} resolves to: ${DOMAIN_IP}"

echo ""
echo "2. Checking server's public IP..."
SERVER_IP=$(curl -s ifconfig.me 2>/dev/null || curl -s icanhazip.com 2>/dev/null || echo "Could not determine")
echo "Server's public IP: ${SERVER_IP}"

echo ""
echo "3. DNS Status:"
if [ "$DOMAIN_IP" = "$SERVER_IP" ]; then
    echo "✅ DNS is correctly configured!"
    echo "   ${DOMAIN} → ${SERVER_IP}"
else
    echo "❌ DNS mismatch detected!"
    echo "   Domain points to: ${DOMAIN_IP}"
    echo "   Server IP is:    ${SERVER_IP}"
    echo ""
    echo "🔧 To fix this, update your DNS A record:"
    echo "   Record Type: A"
    echo "   Name: @"
    echo "   Value: ${SERVER_IP}"
    echo "   TTL: 300 (or your provider's minimum)"
fi

echo ""
echo "4. Testing domain accessibility..."
echo "HTTP test:"
curl -s -I http://${DOMAIN}/health/ | head -3 || echo "HTTP not accessible"

echo ""
echo "HTTPS test:"
curl -s -k -I https://${DOMAIN}/health/ | head -3 || echo "HTTPS not accessible"

echo ""
echo "5. Checking SSL certificate (if exists)..."
echo | openssl s_client -servername $DOMAIN -connect $DOMAIN:443 2>/dev/null | openssl x509 -noout -dates 2>/dev/null || echo "No SSL certificate found"

echo ""
if [ "$DOMAIN_IP" = "$SERVER_IP" ]; then
    echo "🚀 Ready to setup Let's Encrypt SSL!"
    echo "Run: sudo ./scripts/setup-domain-ssl.sh"
else
    echo "⚠️  Please fix DNS first, then run SSL setup."
fi
