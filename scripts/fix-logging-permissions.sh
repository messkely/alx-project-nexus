#!/bin/bash
# Fix logging permission issue for HTTPS Django container

echo "🔧 Fixing Django Logging Permission Issue"
echo "========================================"

cd ~/alx-project-nexus

echo "1. Stopping HTTPS containers..."
docker compose -f docker-compose.https.yml down

echo "2. Fixing log file permissions..."
sudo chown -R $USER:$USER logs/
sudo chmod -R 755 logs/
sudo touch logs/security.log logs/django.log logs/nginx/access.log logs/nginx/error.log 2>/dev/null || true
sudo chown -R $USER:$USER logs/

echo "3. Creating logs directory with proper structure..."
mkdir -p logs/nginx
touch logs/security.log
touch logs/django.log
touch logs/nginx/access.log  
touch logs/nginx/error.log
chmod 666 logs/*.log
chmod 666 logs/nginx/*.log 2>/dev/null || true

echo "4. Updating docker-compose to fix volume permissions..."
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
      - ./logs:/app/logs:rw
    user: "root"
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
      - ./logs/nginx:/var/log/nginx:rw
      - /var/www/html:/var/www/html
    depends_on:
      - web

volumes:
  postgres_data:
  redis_data:
  static_volume:
  media_volume:
EOF

echo "5. Starting containers with corrected permissions..."
docker compose -f docker-compose.https.yml up -d --build

echo "6. Waiting for Django to start..."
echo "This may take a few minutes for the first startup..."
sleep 45

echo "7. Checking Django container status..."
docker compose -f docker-compose.https.yml ps web

echo "8. Testing Django health..."
echo "Checking internal Django health:"
for i in {1..10}; do
    if docker exec ecommerce_web_prod curl -f http://localhost:8000/health/ 2>/dev/null; then
        echo "✅ Django is running!"
        break
    else
        echo "⏳ Waiting for Django... ($i/10)"
        sleep 5
    fi
done

echo ""
echo "9. Testing HTTPS endpoints..."
echo "Testing HTTPS health endpoint:"
curl -k -s https://3.80.35.89/health/ | head -2 || echo "Still starting up..."

echo ""
echo "10. Final status check..."
docker compose -f docker-compose.https.yml ps

echo ""
echo "✅ Permission fix applied!"
echo ""
echo "If Django is still starting, wait 2-3 minutes and test:"
echo "curl -k https://3.80.35.89/health/"
echo ""
echo "🔒 Your HTTPS URLs:"
echo "• https://3.80.35.89/"
echo "• https://3.80.35.89/health/"
echo "• https://3.80.35.89/api/v1/docs/"
