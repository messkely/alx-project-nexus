#!/bin/bash
# Quick fix for container conflicts when switching to HTTPS
# This will clean up existing containers and restart with HTTPS

echo "🔧 Fixing Container Conflicts for HTTPS Setup"
echo "============================================="

cd ~/alx-project-nexus

echo "1. Stopping all existing containers..."
docker compose -f docker-compose.prod.yml down 2>/dev/null || echo "No prod containers to stop"
docker compose -f docker-compose.https.yml down 2>/dev/null || echo "No https containers to stop"
docker compose -f docker-compose.yml down 2>/dev/null || echo "No default containers to stop"

echo "2. Removing conflicting containers..."
docker rm -f ecommerce_db_prod ecommerce_redis_prod ecommerce_web_prod ecommerce_nginx_prod 2>/dev/null || echo "Some containers already removed"

echo "3. Cleaning up Docker system..."
docker system prune -f
docker volume prune -f << EOF
y
EOF

echo "4. Checking if HTTPS configuration exists..."
if [ ! -f "docker-compose.https.yml" ]; then
    echo "Creating HTTPS docker-compose configuration..."
    
    cat > docker-compose.https.yml << 'EOF'
services:
  # PostgreSQL Database
  db:
    image: postgres:15-alpine
    container_name: ecommerce_db_prod
    restart: always
    environment:
      - POSTGRES_DB=ecommerce_db
      - POSTGRES_USER=ecommerce_user
      - POSTGRES_PASSWORD=EcommerceProd2025!SecurePass
      - POSTGRES_HOST_AUTH_METHOD=md5
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./backups:/backups
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U ecommerce_user -d ecommerce_db"]
      interval: 10s
      timeout: 5s
      retries: 5

  # Redis Cache
  redis:
    image: redis:7-alpine
    container_name: ecommerce_redis_prod
    restart: always
    command: redis-server --appendonly yes --requirepass RedisSecure2025Pass
    volumes:
      - redis_data:/data
    healthcheck:
      test: ["CMD", "redis-cli", "-a", "RedisSecure2025Pass", "ping"]
      interval: 10s
      timeout: 5s
      retries: 3

  # Django Web Application
  web:
    build:
      context: .
      dockerfile: Dockerfile
    container_name: ecommerce_web_prod
    restart: always
    ports:
      - "127.0.0.1:8000:8000"
    environment:
      - DEBUG=False
      - SECRET_KEY=EcommerceSecretKey2025!ProductionAWSEC2VerySecure
      - ALLOWED_HOSTS=3.80.35.89,localhost,127.0.0.1,0.0.0.0,web,django
      - DB_ENGINE=django.db.backends.postgresql
      - DB_NAME=ecommerce_db
      - DB_USER=ecommerce_user
      - DB_PASSWORD=EcommerceProd2025!SecurePass
      - DB_HOST=db
      - DB_PORT=5432
      - REDIS_URL=redis://:RedisSecure2025Pass@redis:6379/0
      - DJANGO_SETTINGS_MODULE=ecommerce_backend.settings
      - PYTHONPATH=/app
    volumes:
      - static_volume:/app/staticfiles
      - media_volume:/app/media
      - ./logs:/app/logs
    depends_on:
      db:
        condition: service_healthy
      redis:
        condition: service_healthy
    command: ["sh", "/app/scripts/start_production.sh"]
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health/"]
      interval: 30s
      timeout: 10s
      retries: 3

  # Nginx with HTTPS
  nginx:
    image: nginx:alpine
    container_name: ecommerce_nginx_prod
    restart: always
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx/nginx.conf:/etc/nginx/nginx.conf:ro
      - ./nginx/ec2-production-https.conf:/etc/nginx/conf.d/default.conf:ro
      - static_volume:/app/staticfiles:ro
      - media_volume:/app/media:ro
      - ./ssl:/etc/nginx/ssl:ro
      - ./logs/nginx:/var/log/nginx
      - /var/www/html:/var/www/html
    depends_on:
      - web

volumes:
  postgres_data:
  redis_data:
  static_volume:
  media_volume:
EOF
fi

echo "5. Generating SSL certificates..."
mkdir -p ssl

if [ ! -f "ssl/cert.crt" ] || [ ! -f "ssl/cert.key" ]; then
    echo "Creating self-signed SSL certificate..."
    sudo openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
        -keyout ssl/cert.key \
        -out ssl/cert.crt \
        -subj "/C=US/ST=State/L=City/O=ALX/OU=ECommerce/CN=3.80.35.89"
    
    # Set permissions
    sudo chmod 600 ssl/cert.key
    sudo chmod 644 ssl/cert.crt
    sudo chown $USER:$USER ssl/*
    
    echo "✅ SSL certificate created"
else
    echo "✅ SSL certificate already exists"
fi

echo "6. Creating HTTPS Nginx configuration..."
cat > nginx/ec2-production-https.conf << 'EOF'
upstream django {
    server web:8000;
}

# Rate limiting
limit_req_zone $binary_remote_addr zone=api:10m rate=10r/s;
limit_req_zone $binary_remote_addr zone=auth:10m rate=5r/m;

# Redirect HTTP to HTTPS
server {
    listen 80;
    server_name 3.80.35.89;
    
    # Redirect all HTTP traffic to HTTPS
    return 301 https://$server_name$request_uri;
}

# HTTPS Server Configuration
server {
    listen 443 ssl http2;
    server_name 3.80.35.89;
    
    # SSL Configuration
    ssl_certificate /etc/nginx/ssl/cert.crt;
    ssl_certificate_key /etc/nginx/ssl/cert.key;
    
    # Modern SSL configuration
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers ECDHE-RSA-AES256-GCM-SHA512:DHE-RSA-AES256-GCM-SHA512:ECDHE-RSA-AES256-GCM-SHA384:DHE-RSA-AES256-GCM-SHA384;
    ssl_prefer_server_ciphers off;
    ssl_session_cache shared:SSL:10m;
    ssl_session_timeout 10m;
    
    # HSTS (HTTP Strict Transport Security)
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
    
    # Enhanced Security headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header Referrer-Policy "strict-origin-when-cross-origin" always;
    add_header Content-Security-Policy "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'; img-src 'self' data: https:;" always;
    
    client_max_body_size 100M;
    server_tokens off;
    
    # Gzip compression
    gzip on;
    gzip_vary on;
    gzip_min_length 1024;
    gzip_proxied any;
    gzip_comp_level 6;
    gzip_types
        application/javascript
        application/json
        application/xml
        text/css
        text/javascript
        text/plain
        text/xml;
    
    # Static files
    location /static/ {
        alias /app/staticfiles/;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
    
    # Media files
    location /media/ {
        alias /app/media/;
        expires 30d;
        add_header Cache-Control "public";
    }
    
    # API endpoints
    location /api/ {
        limit_req zone=api burst=20 nodelay;
        
        proxy_pass http://django;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_redirect off;
        
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
    }
    
    # Health check
    location /health/ {
        proxy_pass http://django/health/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_redirect off;
        access_log off;
    }
    
    # Admin interface
    location /admin/ {
        proxy_pass http://django;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_redirect off;
    }
    
    # Main application
    location / {
        proxy_pass http://django;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_redirect off;
    }
    
    # Security
    location ~ /\.(ht|git|env) {
        deny all;
    }
}
EOF

echo "7. Starting HTTPS services..."
docker compose -f docker-compose.https.yml up -d --build

echo "8. Waiting for services to start..."
sleep 30

echo "9. Testing HTTPS setup..."
echo "========================="

echo "Service status:"
docker compose -f docker-compose.https.yml ps

echo ""
echo "Testing HTTPS health endpoint:"
curl -k -s https://3.80.35.89/health/ | head -1 || echo "Health check failed"

echo ""
echo "Testing HTTP to HTTPS redirect:"
curl -s -I http://3.80.35.89/health/ | grep -i location || echo "Redirect not working"

echo ""
echo "✅ HTTPS setup complete!"
echo ""
echo "🔒 Your HTTPS URLs:"
echo "• Main Page: https://3.80.35.89/"
echo "• Health Check: https://3.80.35.89/health/"
echo "• API Docs: https://3.80.35.89/api/v1/docs/"
echo "• Admin Panel: https://3.80.35.89/admin/"
echo ""
echo "⚠️  Note: Using self-signed certificate - browsers will show security warning"
