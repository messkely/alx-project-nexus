#!/bin/bash
# ALX E-Commerce Backend - AWS EC2 Deployment Script
# For IP: 3.80.35.89
# Usage: ./scripts/deploy-ec2-production.sh [setup|start|stop|restart|status|logs]

set -e

# Configuration
EC2_IP="3.80.35.89"
PROJECT_NAME="alx-ecommerce-backend"
PROJECT_DIR="/opt/alx-ecommerce"
GIT_REPO="https://github.com/messkely/alx-project-nexus.git"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log_info() { echo -e "${BLUE}ℹ️  $1${NC}"; }
log_success() { echo -e "${GREEN}✅ $1${NC}"; }
log_warning() { echo -e "${YELLOW}⚠️  $1${NC}"; }
log_error() { echo -e "${RED}❌ $1${NC}"; }

# Check if running as root or with sudo
check_sudo() {
    if [[ $EUID -eq 0 ]]; then
        log_warning "Running as root"
    elif ! sudo -n true 2>/dev/null; then
        log_error "This script requires sudo privileges"
        exit 1
    fi
}

# Install Docker and Docker Compose
install_docker() {
    log_info "Installing Docker..."
    
    # Remove old versions
    sudo apt-get remove -y docker docker-engine docker.io containerd runc 2>/dev/null || true
    
    # Update package index
    sudo apt-get update
    
    # Install packages to allow apt to use a repository over HTTPS
    sudo apt-get install -y \
        apt-transport-https \
        ca-certificates \
        curl \
        gnupg \
        lsb-release \
        git \
        ufw \
        htop \
        nano
    
    # Add Docker's official GPG key
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
    
    # Add Docker repository
    echo "deb [arch=amd64 signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
    
    # Update package index again
    sudo apt-get update
    
    # Install Docker Engine
    sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin
    
    # Add current user to docker group
    sudo usermod -aG docker $USER
    
    # Start and enable Docker
    sudo systemctl start docker
    sudo systemctl enable docker
    
    log_success "Docker installed successfully"
}

# Setup firewall
setup_firewall() {
    log_info "Setting up UFW firewall..."
    
    # Reset UFW to defaults
    sudo ufw --force reset
    
    # Default policies
    sudo ufw default deny incoming
    sudo ufw default allow outgoing
    
    # Allow SSH (adjust port if needed)
    sudo ufw allow ssh
    sudo ufw allow 22/tcp
    
    # Allow HTTP and HTTPS
    sudo ufw allow 80/tcp
    sudo ufw allow 443/tcp
    
    # Allow Docker daemon (if needed)
    sudo ufw allow 2376/tcp
    
    # Enable UFW
    sudo ufw --force enable
    
    log_success "Firewall configured"
}

# Setup project directory and clone repository
setup_project() {
    log_info "Setting up project directory..."
    
    # Create project directory
    sudo mkdir -p $PROJECT_DIR
    sudo chown $USER:$USER $PROJECT_DIR
    
    # Clone or update repository
    if [ -d "$PROJECT_DIR/.git" ]; then
        log_info "Updating existing repository..."
        cd $PROJECT_DIR
        git pull origin main
    else
        log_info "Cloning repository..."
        git clone $GIT_REPO $PROJECT_DIR
        cd $PROJECT_DIR
    fi
    
    # Create necessary directories
    mkdir -p logs/nginx
    mkdir -p ssl
    mkdir -p backups
    
    # Set permissions
    chmod +x scripts/*.sh
    
    log_success "Project setup complete"
}

# Build and start services
start_services() {
    log_info "Starting production services..."
    
    cd $PROJECT_DIR
    
    # Build images
    docker compose -f docker-compose.prod.yml build --no-cache
    
    # Start services
    docker compose -f docker-compose.prod.yml up -d
    
    log_success "Services started successfully"
    
    # Show status
    sleep 10
    show_status
}

# Stop services
stop_services() {
    log_info "Stopping services..."
    
    cd $PROJECT_DIR
    docker compose -f docker-compose.prod.yml down
    
    log_success "Services stopped"
}

# Restart services
restart_services() {
    log_info "Restarting services..."
    
    stop_services
    sleep 5
    start_services
}

# Show service status
show_status() {
    log_info "Service Status:"
    
    cd $PROJECT_DIR
    docker compose -f docker-compose.prod.yml ps
    
    echo
    log_info "Health Checks:"
    
    # Test health endpoint
    if curl -f -s http://localhost/health/ > /dev/null; then
        log_success "Health endpoint: OK"
    else
        log_error "Health endpoint: FAILED"
    fi
    
    # Test API endpoint
    if curl -f -s http://localhost/api/v1/products/ > /dev/null; then
        log_success "API endpoint: OK"
    else
        log_error "API endpoint: FAILED"
    fi
    
    echo
    log_info "Access URLs:"
    echo "• API Documentation: http://$EC2_IP/"
    echo "• Health Check: http://$EC2_IP/health/"
    echo "• Admin Panel: http://$EC2_IP/admin/"
    echo "• API Base: http://$EC2_IP/api/v1/"
}

# Show logs
show_logs() {
    cd $PROJECT_DIR
    
    if [ -n "$1" ]; then
        docker compose -f docker-compose.prod.yml logs -f $1
    else
        docker compose -f docker-compose.prod.yml logs -f
    fi
}

# Main execution
case "${1:-setup}" in
    "setup")
        log_info "Setting up ALX E-Commerce Backend on EC2 ($EC2_IP)..."
        check_sudo
        install_docker
        setup_firewall
        setup_project
        start_services
        log_success "Deployment complete!"
        echo
        echo "Next steps:"
        echo "1. Test the application: http://$EC2_IP/"
        echo "2. Create admin user: docker compose -f docker-compose.prod.yml exec web python manage.py createsuperuser"
        echo "3. Load sample data: docker compose -f docker-compose.prod.yml exec web python manage.py loaddata catalog/fixtures/sample_data.json"
        ;;
    "start")
        start_services
        ;;
    "stop")
        stop_services
        ;;
    "restart")
        restart_services
        ;;
    "status")
        show_status
        ;;
    "logs")
        show_logs $2
        ;;
    "update")
        log_info "Updating application..."
        cd $PROJECT_DIR
        git pull origin main
        docker compose -f docker-compose.prod.yml build --no-cache web
        docker compose -f docker-compose.prod.yml up -d
        log_success "Update complete"
        ;;
    *)
        echo "Usage: $0 [setup|start|stop|restart|status|logs|update]"
        echo
        echo "Commands:"
        echo "  setup   - Full initial setup (Docker, firewall, project)"
        echo "  start   - Start all services"
        echo "  stop    - Stop all services"
        echo "  restart - Restart all services"
        echo "  status  - Show service status and health"
        echo "  logs    - Show logs (optionally specify service name)"
        echo "  update  - Update application from git and restart"
        exit 1
        ;;
esac
