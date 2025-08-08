#!/bin/bash
# ALX E-Commerce Backend - EC2 Ubuntu Deployment Script
# Usage: ./scripts/deploy-ec2.sh [init|update|setup|status]

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Project configuration
PROJECT_NAME="alx-ecommerce"
PROJECT_DIR="/opt/alx-ecommerce"
NGINX_SITE="alx-ecommerce"
PYTHON_VERSION="3.11"
DB_NAME="ecommerce_db"
DB_USER="ecommerce_user"

# Helper functions
log_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

log_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

log_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

log_error() {
    echo -e "${RED}❌ $1${NC}"
}

# Check if running as root or with sudo
check_sudo() {
    if [[ $EUID -eq 0 ]]; then
        log_warning "Running as root. Consider using a non-root user with sudo privileges."
    elif ! sudo -n true 2>/dev/null; then
        log_error "This script requires sudo privileges. Please run with sudo or configure passwordless sudo."
        exit 1
    fi
}

# Update system packages
update_system() {
    log_info "Updating system packages..."
    sudo apt update
    sudo apt upgrade -y
    log_success "System packages updated"
}

# Install system dependencies
install_dependencies() {
    log_info "Installing system dependencies..."
    
    # Essential packages
    sudo apt install -y \
        python3.11 \
        python3.11-venv \
        python3.11-dev \
        python3-pip \
        postgresql \
        postgresql-contrib \
        redis-server \
        nginx \
        git \
        curl \
        wget \
        supervisor \
        ufw \
        fail2ban \
        certbot \
        python3-certbot-nginx
    
    # Install Node.js (for any frontend assets)
    curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
    sudo apt install -y nodejs
    
    log_success "System dependencies installed"
}

# Configure PostgreSQL
setup_database() {
    log_info "Setting up PostgreSQL database..."
    
    # Start PostgreSQL service
    sudo systemctl start postgresql
    sudo systemctl enable postgresql
    
    # Create database and user
    sudo -u postgres psql -c "CREATE DATABASE ${DB_NAME};" 2>/dev/null || log_warning "Database ${DB_NAME} may already exist"
    sudo -u postgres psql -c "CREATE USER ${DB_USER} WITH PASSWORD 'secure_password_change_me';" 2>/dev/null || log_warning "User ${DB_USER} may already exist"
    sudo -u postgres psql -c "ALTER USER ${DB_USER} CREATEDB;"
    sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE ${DB_NAME} TO ${DB_USER};"
    
    log_success "PostgreSQL database configured"
}

# Configure Redis
setup_redis() {
    log_info "Setting up Redis..."
    
    # Start Redis service
    sudo systemctl start redis-server
    sudo systemctl enable redis-server
    
    # Basic Redis configuration
    sudo sed -i 's/# maxmemory <bytes>/maxmemory 256mb/' /etc/redis/redis.conf
    sudo sed -i 's/# maxmemory-policy noeviction/maxmemory-policy allkeys-lru/' /etc/redis/redis.conf
    
    sudo systemctl restart redis-server
    log_success "Redis configured"
}

# Setup project directory and virtual environment
setup_project() {
    log_info "Setting up project environment..."
    
    # Create project directory
    sudo mkdir -p $PROJECT_DIR
    sudo chown $USER:$USER $PROJECT_DIR
    
    # Clone or update project
    if [ -d "$PROJECT_DIR/.git" ]; then
        log_info "Updating existing project..."
        cd $PROJECT_DIR
        git pull origin main
    else
        log_info "Cloning project..."
        git clone https://github.com/messkely/alx-project-nexus.git $PROJECT_DIR
        cd $PROJECT_DIR
    fi
    
    # Create virtual environment
    python3.11 -m venv venv
    source venv/bin/activate
    
    # Upgrade pip
    pip install --upgrade pip
    
    # Install Python dependencies
    pip install -r requirements.txt
    
    log_success "Project environment setup complete"
}

# Configure environment variables
setup_environment() {
    log_info "Setting up environment variables..."
    
    cd $PROJECT_DIR
    
    # Create production environment file
    cat > .env << EOF
# ALX E-Commerce Backend - Production Environment

# Django Configuration
DEBUG=False
SECRET_KEY=your-very-secure-secret-key-change-this-in-production
ALLOWED_HOSTS=localhost,127.0.0.1,your-domain.com

# Database Configuration
DB_ENGINE=django.db.backends.postgresql
DB_NAME=${DB_NAME}
DB_USER=${DB_USER}
DB_PASSWORD=secure_password_change_me
DB_HOST=localhost
DB_PORT=5432

# Redis Configuration
REDIS_URL=redis://localhost:6379/0

# Security Settings
SECURE_SSL_REDIRECT=False
SECURE_PROXY_SSL_HEADER=None
CORS_ALLOWED_ORIGINS=http://localhost,http://127.0.0.1

# Media and Static Files
MEDIA_URL=/media/
STATIC_URL=/static/
STATIC_ROOT=${PROJECT_DIR}/staticfiles/
MEDIA_ROOT=${PROJECT_DIR}/media/

# Email Configuration (optional)
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
EOF

    log_success "Environment variables configured"
    log_warning "Remember to update the SECRET_KEY and database password in .env file!"
}

# Run Django setup
setup_django() {
    log_info "Setting up Django application..."
    
    cd $PROJECT_DIR
    source venv/bin/activate
    
    # Run migrations
    python manage.py migrate
    
    # Collect static files
    python manage.py collectstatic --noinput
    
    # Create superuser (automated)
    python manage.py shell -c "
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
    print('Superuser created: admin/admin123')
else:
    print('Superuser already exists')
"
    
    log_success "Django application configured"
}

# Configure Gunicorn
setup_gunicorn() {
    log_info "Setting up Gunicorn..."
    
    # Create Gunicorn configuration
    cat > $PROJECT_DIR/gunicorn.conf.py << EOF
# Gunicorn configuration file
bind = "127.0.0.1:8000"
workers = 3
worker_class = "sync"
worker_connections = 1000
max_requests = 1000
max_requests_jitter = 50
timeout = 30
keepalive = 2
preload_app = True
daemon = False
user = "$USER"
group = "$USER"
tmp_upload_dir = None
errorlog = "/var/log/gunicorn/error.log"
accesslog = "/var/log/gunicorn/access.log"
loglevel = "info"
EOF

    # Create log directory
    sudo mkdir -p /var/log/gunicorn
    sudo chown $USER:$USER /var/log/gunicorn
    
    log_success "Gunicorn configured"
}

# Configure Supervisor
setup_supervisor() {
    log_info "Setting up Supervisor..."
    
    # Create supervisor configuration
    sudo cat > /etc/supervisor/conf.d/${PROJECT_NAME}.conf << EOF
[program:${PROJECT_NAME}]
command=${PROJECT_DIR}/venv/bin/gunicorn ecommerce_backend.wsgi:application -c ${PROJECT_DIR}/gunicorn.conf.py
directory=${PROJECT_DIR}
user=${USER}
autostart=true
autorestart=true
stdout_logfile=/var/log/supervisor/${PROJECT_NAME}.log
stderr_logfile=/var/log/supervisor/${PROJECT_NAME}_error.log
environment=PATH="${PROJECT_DIR}/venv/bin"
EOF

    # Reload supervisor
    sudo supervisorctl reread
    sudo supervisorctl update
    sudo supervisorctl start ${PROJECT_NAME}
    
    log_success "Supervisor configured and application started"
}

# Configure Nginx
setup_nginx() {
    log_info "Setting up Nginx..."
    
    # Create Nginx site configuration
    sudo cat > /etc/nginx/sites-available/${NGINX_SITE} << EOF
server {
    listen 80;
    server_name your-domain.com www.your-domain.com;  # Change this to your domain
    
    client_max_body_size 100M;
    
    # Static files
    location /static/ {
        alias ${PROJECT_DIR}/staticfiles/;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
    
    # Media files
    location /media/ {
        alias ${PROJECT_DIR}/media/;
        expires 1y;
        add_header Cache-Control "public";
    }
    
    # Django application
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
        proxy_connect_timeout 300s;
        proxy_read_timeout 300s;
    }
}
EOF

    # Enable site
    sudo ln -sf /etc/nginx/sites-available/${NGINX_SITE} /etc/nginx/sites-enabled/
    
    # Remove default site if it exists
    sudo rm -f /etc/nginx/sites-enabled/default
    
    # Test Nginx configuration
    sudo nginx -t
    
    # Reload Nginx
    sudo systemctl reload nginx
    sudo systemctl enable nginx
    
    log_success "Nginx configured"
}

# Configure firewall
setup_firewall() {
    log_info "Setting up firewall..."
    
    # Reset UFW to defaults
    sudo ufw --force reset
    
    # Default policies
    sudo ufw default deny incoming
    sudo ufw default allow outgoing
    
    # Allow SSH (be careful with this)
    sudo ufw allow ssh
    
    # Allow HTTP and HTTPS
    sudo ufw allow 'Nginx Full'
    
    # Enable firewall
    sudo ufw --force enable
    
    log_success "Firewall configured"
}

# Configure SSL with Let's Encrypt
setup_ssl() {
    if [ -z "$1" ]; then
        log_warning "No domain provided for SSL setup. Skipping SSL configuration."
        log_info "To setup SSL later, run: sudo certbot --nginx -d your-domain.com"
        return
    fi
    
    local domain=$1
    log_info "Setting up SSL certificate for ${domain}..."
    
    # Update Nginx config with the domain
    sudo sed -i "s/your-domain.com/${domain}/g" /etc/nginx/sites-available/${NGINX_SITE}
    sudo nginx -t && sudo systemctl reload nginx
    
    # Get SSL certificate
    sudo certbot --nginx -d ${domain} --non-interactive --agree-tos --email admin@${domain}
    
    log_success "SSL certificate configured for ${domain}"
}

# Display status
show_status() {
    log_info "Application Status:"
    echo ""
    
    # Check services
    echo "🔍 Service Status:"
    systemctl is-active postgresql && echo "✅ PostgreSQL: Running" || echo "❌ PostgreSQL: Stopped"
    systemctl is-active redis-server && echo "✅ Redis: Running" || echo "❌ Redis: Stopped"
    systemctl is-active nginx && echo "✅ Nginx: Running" || echo "❌ Nginx: Stopped"
    systemctl is-active supervisor && echo "✅ Supervisor: Running" || echo "❌ Supervisor: Stopped"
    
    # Check application
    echo ""
    echo "🔍 Application Status:"
    sudo supervisorctl status ${PROJECT_NAME}
    
    # Check ports
    echo ""
    echo "🔍 Port Status:"
    sudo netstat -tlnp | grep -E ":80|:443|:8000|:5432|:6379" || echo "No services listening on expected ports"
    
    echo ""
    echo "🌐 Access your application:"
    echo "   HTTP:  http://your-server-ip/"
    echo "   Admin: http://your-server-ip/admin/ (admin/admin123)"
    echo "   API:   http://your-server-ip/api/v1/"
}

# Main deployment function
deploy_init() {
    log_info "Starting ALX E-Commerce Backend EC2 deployment..."
    
    check_sudo
    update_system
    install_dependencies
    setup_database
    setup_redis
    setup_project
    setup_environment
    setup_django
    setup_gunicorn
    setup_supervisor
    setup_nginx
    setup_firewall
    
    log_success "Deployment completed successfully!"
    echo ""
    show_status
    
    echo ""
    log_warning "Next steps:"
    echo "1. Update .env file with your actual SECRET_KEY and database password"
    echo "2. Update Nginx configuration with your actual domain name"
    echo "3. Run: sudo systemctl restart supervisor nginx"
    echo "4. For SSL: ./scripts/deploy-ec2.sh ssl your-domain.com"
}

# Update existing deployment
deploy_update() {
    log_info "Updating ALX E-Commerce Backend deployment..."
    
    cd $PROJECT_DIR
    
    # Pull latest code
    git pull origin main
    
    # Activate virtual environment
    source venv/bin/activate
    
    # Update dependencies
    pip install -r requirements.txt
    
    # Run migrations
    python manage.py migrate
    
    # Collect static files
    python manage.py collectstatic --noinput
    
    # Restart application
    sudo supervisorctl restart ${PROJECT_NAME}
    sudo systemctl reload nginx
    
    log_success "Application updated successfully!"
}

# Main script logic
case "$1" in
    "init")
        deploy_init
        ;;
    "update")
        deploy_update
        ;;
    "setup")
        setup_django
        ;;
    "status")
        show_status
        ;;
    "ssl")
        setup_ssl "$2"
        ;;
    *)
        echo "ALX E-Commerce Backend - EC2 Ubuntu Deployment"
        echo ""
        echo "Usage: $0 {init|update|setup|status|ssl}"
        echo ""
        echo "Commands:"
        echo "  init   - Full deployment setup (first time)"
        echo "  update - Update existing deployment"
        echo "  setup  - Setup Django (migrations, static files)"
        echo "  status - Show application status"
        echo "  ssl    - Setup SSL certificate (ssl domain.com)"
        echo ""
        exit 1
        ;;
esac
