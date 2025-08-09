#!/bin/bash
# Setup SSL/HTTPS for ALX E-Commerce on EC2
# This script will generate self-signed certificates and configure HTTPS

set -e

echo "🔒 Setting up HTTPS for ALX E-Commerce on EC2"
echo "============================================="

# Navigate to project directory
cd ~/alx-project-nexus

# Create SSL directory if it doesn't exist
echo "1. Creating SSL directory..."
mkdir -p ssl

# Generate self-signed SSL certificate (for development/testing)
echo "2. Generating self-signed SSL certificate..."
if [ ! -f "ssl/cert.pem" ] || [ ! -f "ssl/key.pem" ]; then
    sudo openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
        -keyout ssl/key.pem \
        -out ssl/cert.pem \
        -subj "/C=US/ST=State/L=City/O=ALX/OU=ECommerce/CN=3.80.35.89"
    
    echo "✅ SSL certificate generated"
else
    echo "✅ SSL certificate already exists"
fi

# Set proper permissions for SSL files
echo "3. Setting SSL file permissions..."
sudo chmod 600 ssl/key.pem
sudo chmod 644 ssl/cert.pem
sudo chown $USER:$USER ssl/*

# Stop services
echo "4. Stopping current services..."
docker compose -f docker-compose.prod.yml down

# Update nginx configuration to enable HTTPS
echo "5. Updating nginx configuration for HTTPS..."

# Backup original config
cp nginx/ec2-production.conf nginx/ec2-production.conf.backup

# Create HTTPS-enabled nginx config
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
    ssl_certificate /etc/nginx/ssl/cert.pem;
    ssl_certificate_key /etc/nginx/ssl/key.pem;
    
    # Modern SSL configuration
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers ECDHE-RSA-AES256-GCM-SHA512:DHE-RSA-AES256-GCM-SHA512:ECDHE-RSA-AES256-GCM-SHA384:DHE-RSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-SHA384;
    ssl_prefer_server_ciphers off;
    ssl_session_cache shared:SSL:10m;
    ssl_session_timeout 10m;
    
    # HSTS (HTTP Strict Transport Security)
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
    
    # Enhanced Security headers for HTTPS
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header Referrer-Policy "strict-origin-when-cross-origin" always;
    add_header Content-Security-Policy "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'; img-src 'self' data: https:;" always;
    
    # Client body size for file uploads
    client_max_body_size 100M;
    
    # Hide nginx version
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
        
        # Enable gzip for static files
        location ~* \.(css|js|png|jpg|jpeg|gif|ico|svg|woff|woff2|ttf|eot)$ {
            expires 1y;
            add_header Cache-Control "public, immutable";
            gzip_static on;
        }
    }
    
    # Media files
    location /media/ {
        alias /app/media/;
        expires 30d;
        add_header Cache-Control "public";
        
        # Prevent execution of scripts in media directory
        location ~* \.(php|py|pl|sh)$ {
            deny all;
        }
    }
    
    # API rate limiting
    location /api/ {
        limit_req zone=api burst=20 nodelay;
        
        proxy_pass http://django;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_redirect off;
        
        # Timeouts
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
        
        # Buffer settings
        proxy_buffering on;
        proxy_buffer_size 4k;
        proxy_buffers 8 4k;
    }

    # API health check (no rate limiting for health checks)
    location /api/v1/health/ {
        proxy_pass http://django;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_redirect off;
        access_log off;
    }
    
    # Authentication endpoints with stricter rate limiting
    location ~ ^/api/v1/auth/(login|register|password) {
        limit_req zone=auth burst=3 nodelay;
        
        proxy_pass http://django;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_Set_header X-Forwarded-Proto $scheme;
        proxy_redirect off;
    }
    
    # Health check endpoint 
    location /health/ {
        proxy_pass http://django/health/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_Set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_redirect off;
        access_log off;
    }
    
    # Admin interface (additional security)
    location /admin/ {
        # Optional: Restrict admin access to specific IPs
        # allow 1.2.3.4;  # Your admin IP
        # deny all;
        
        proxy_pass http://django;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_redirect off;
    }
    
    # Django application (main)
    location / {
        proxy_pass http://django;
        proxy_set_header Host $host;
        proxy_Set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_redirect off;
        
        # Timeouts
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
        
        # Buffer settings
        proxy_buffering on;
        proxy_buffer_size 4k;
        proxy_buffers 8 4k;
    }
    
    # Robots.txt
    location /robots.txt {
        add_header Content-Type text/plain;
        return 200 "User-agent: *\nDisallow: /admin/\nDisallow: /api/v1/auth/\n";
    }
    
    # Block access to sensitive files
    location ~ /\.(ht|git|env) {
        deny all;
    }
    
    # Error pages
    error_page 404 /404.html;
    error_page 500 502 503 504 /50x.html;
    location = /50x.html {
        root /usr/share/nginx/html;
    }
}
EOF

echo "6. Updating docker-compose for HTTPS..."

# Update docker-compose to use HTTPS nginx config
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
    # No external ports - internal access only
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
    # No external ports - internal access only
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

  # Nginx Reverse Proxy with HTTPS
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
    depends_on:
      - web

volumes:
  postgres_data:
  redis_data:
  static_volume:
  media_volume:
EOF

echo "7. Starting services with HTTPS..."
docker compose -f docker-compose.https.yml up -d --build

echo "8. Waiting for services to start..."
sleep 30

echo "9. Testing HTTPS endpoints..."
echo "================================"

echo "Testing HTTPS health endpoint:"
curl -k -s https://3.80.35.89/health/ | head -1 || echo "Failed"

echo "Testing HTTPS API health:"
curl -k -s https://3.80.35.89/api/v1/health/ | head -1 || echo "Failed"

echo "Testing HTTP redirect:"
curl -s -w "HTTP %{http_code}\n" http://3.80.35.89/health/ | tail -1

echo ""
echo "✅ HTTPS setup complete!"
echo ""
echo "🔒 HTTPS URLs:"
echo "• Main Page: https://3.80.35.89/"
echo "• Health Check: https://3.80.35.89/health/"
echo "• API Docs: https://3.80.35.89/api/v1/docs/"
echo "• Admin Panel: https://3.80.35.89/admin/"
echo ""
echo "⚠️  Note: Using self-signed certificate - browsers will show security warning"
echo "   For production, use Let's Encrypt or purchase an SSL certificate"
