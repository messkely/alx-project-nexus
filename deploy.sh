#!/bin/bash

# ALX E-Commerce Backend - Production Deployment Script
# Usage: ./deploy.sh [init|update|backup|restore]

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
PROJECT_NAME="alx-ecommerce"
BACKUP_DIR="./backups"
COMPOSE_FILE="docker-compose.production.yml"

# Functions
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if Docker and Docker Compose are installed
check_dependencies() {
    log_info "Checking dependencies..."
    
    if ! command -v docker &> /dev/null; then
        log_error "Docker is not installed. Please install Docker first."
        exit 1
    fi
    
    if ! command -v docker compose &> /dev/null; then
        log_error "Docker Compose is not installed. Please install Docker Compose first."
        exit 1
    fi
    
    log_success "Dependencies check passed"
}

# Initialize production environment
init_production() {
    log_info "Initializing production environment..."
    
    # Create necessary directories
    mkdir -p logs ssl backups
    
    # Check for environment file
    if [ ! -f ".env.prod" ]; then
        log_warning ".env.prod file not found"
        if [ -f ".env.prod.example" ]; then
            cp .env.prod.example .env.prod
            log_info "Created .env.prod from template"
            log_warning "Please edit .env.prod with your actual values before continuing"
            exit 1
        else
            log_error ".env.prod.example template not found"
            exit 1
        fi
    fi
    
    # Build images
    log_info "Building Docker images..."
    docker compose -f $COMPOSE_FILE build --no-cache
    
    # Start services
    log_info "Starting services..."
    docker compose -f $COMPOSE_FILE up -d
    
    # Wait for database to be ready
    log_info "Waiting for database to be ready..."
    sleep 30
    
    # Run migrations
    log_info "Running database migrations..."
    docker compose -f $COMPOSE_FILE exec -T web python manage.py migrate
    
    # Create superuser (interactive)
    log_info "Creating superuser (you will be prompted)..."
    docker compose -f $COMPOSE_FILE exec web python manage.py createsuperuser
    
    # Seed database (optional)
    read -p "Do you want to seed the database with sample data? (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        log_info "Seeding database..."
        docker compose -f $COMPOSE_FILE exec -T web python seed_database.py
    fi
    
    log_success "Production environment initialized successfully!"
    log_info "Your application is now running at https://your-domain.com"
}

# Update deployment
update_deployment() {
    log_info "Updating deployment..."
    
    # Create backup before update
    backup_database
    
    # Pull latest changes (if using git)
    if [ -d ".git" ]; then
        log_info "Pulling latest changes..."
        git pull origin main
    fi
    
    # Rebuild and restart services
    log_info "Rebuilding images..."
    docker compose -f $COMPOSE_FILE build --no-cache
    
    log_info "Restarting services..."
    docker compose -f $COMPOSE_FILE down
    docker compose -f $COMPOSE_FILE up -d
    
    # Wait for services to be ready
    sleep 30
    
    # Run migrations
    log_info "Running migrations..."
    docker compose -f $COMPOSE_FILE exec -T web python manage.py migrate
    
    # Collect static files
    log_info "Collecting static files..."
    docker compose -f $COMPOSE_FILE exec -T web python manage.py collectstatic --noinput
    
    log_success "Deployment updated successfully!"
}

# Backup database
backup_database() {
    log_info "Creating database backup..."
    
    mkdir -p $BACKUP_DIR
    TIMESTAMP=$(date +%Y%m%d_%H%M%S)
    BACKUP_FILE="$BACKUP_DIR/db_backup_$TIMESTAMP.sql"
    
    docker compose -f $COMPOSE_FILE exec -T db pg_dump -U ecommerce_user ecommerce > $BACKUP_FILE
    
    if [ -f $BACKUP_FILE ]; then
        log_success "Database backup created: $BACKUP_FILE"
    else
        log_error "Failed to create database backup"
        exit 1
    fi
}

# Restore database from backup
restore_database() {
    if [ -z "$1" ]; then
        log_error "Please provide backup file path"
        echo "Usage: $0 restore /path/to/backup.sql"
        exit 1
    fi
    
    BACKUP_FILE=$1
    
    if [ ! -f "$BACKUP_FILE" ]; then
        log_error "Backup file not found: $BACKUP_FILE"
        exit 1
    fi
    
    log_warning "This will replace the current database with the backup"
    read -p "Are you sure you want to continue? (y/N): " -n 1 -r
    echo
    
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        log_info "Restoring database from backup..."
        docker compose -f $COMPOSE_FILE exec -T db psql -U ecommerce_user -d ecommerce < $BACKUP_FILE
        log_success "Database restored successfully"
    else
        log_info "Restore cancelled"
    fi
}

# Show logs
show_logs() {
    SERVICE=${1:-}
    if [ -z "$SERVICE" ]; then
        docker compose -f $COMPOSE_FILE logs --tail=100 -f
    else
        docker compose -f $COMPOSE_FILE logs --tail=100 -f $SERVICE
    fi
}

# Show status
show_status() {
    log_info "Service Status:"
    docker compose -f $COMPOSE_FILE ps
    
    log_info "Resource Usage:"
    docker stats --no-stream --format "table {{.Container}}\t{{.CPUPerc}}\t{{.MemUsage}}"
}

# SSL certificate setup (Let's Encrypt)
setup_ssl() {
    log_info "Setting up SSL certificate with Let's Encrypt..."
    
    read -p "Enter your domain name: " DOMAIN
    read -p "Enter your email address: " EMAIL
    
    # Update nginx configuration with your domain
    sed -i "s/your-domain.com/$DOMAIN/g" nginx/conf.d/ecommerce.conf
    
    # Create temporary nginx config without SSL
    cp nginx/conf.d/ecommerce.conf nginx/conf.d/ecommerce.conf.bak
    
    log_info "Starting Certbot..."
    docker run --rm -it \
        -v "$(pwd)/ssl:/etc/letsencrypt" \
        -v "$(pwd)/nginx/html:/var/www/certbot" \
        certbot/certbot certonly \
        --webroot \
        --webroot-path=/var/www/certbot \
        --email $EMAIL \
        --agree-tos \
        --no-eff-email \
        -d $DOMAIN \
        -d www.$DOMAIN
    
    # Copy certificates to ssl directory
    cp ssl/live/$DOMAIN/fullchain.pem ssl/
    cp ssl/live/$DOMAIN/privkey.pem ssl/
    
    log_success "SSL certificate setup completed"
    log_info "Restarting nginx..."
    docker compose -f $COMPOSE_FILE restart nginx
}

# Main script
main() {
    check_dependencies
    
    case "${1:-init}" in
        "init")
            init_production
            ;;
        "update")
            update_deployment
            ;;
        "backup")
            backup_database
            ;;
        "restore")
            restore_database $2
            ;;
        "logs")
            show_logs $2
            ;;
        "status")
            show_status
            ;;
        "ssl")
            setup_ssl
            ;;
        *)
            echo "Usage: $0 {init|update|backup|restore|logs|status|ssl}"
            echo ""
            echo "Commands:"
            echo "  init     - Initialize production environment"
            echo "  update   - Update deployment with latest changes"
            echo "  backup   - Create database backup"
            echo "  restore  - Restore database from backup"
            echo "  logs     - Show application logs"
            echo "  status   - Show service status"
            echo "  ssl      - Setup SSL certificate"
            exit 1
            ;;
    esac
}

main $@
