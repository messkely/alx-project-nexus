# ALX E-Commerce Backend - Production Makefile
# Updated: August 8, 2025

.PHONY: help production logs status backup restore clean dev-install dev-migrate dev-seed dev-test

# Default target
help:
	@echo "🐳 ALX E-Commerce Backend - Production Commands"
	@echo "=============================================="
	@echo ""
	@echo "Production Deployment:"
	@echo "  make production   - Start production environment"
	@echo "  make logs         - View application logs"
	@echo "  make status       - Check service status"
	@echo "  make backup       - Create database backup"
	@echo "  make restore      - Restore from backup (use BACKUP_FILE=path)"
	@echo "  make clean        - Clean up Docker resources"
	@echo ""
	@echo "Development Helpers:"
	@echo "  make dev-install  - Install development dependencies"
	@echo "  make dev-migrate  - Run database migrations (local)"
	@echo "  make dev-seed     - Seed database (local)"
	@echo "  make dev-test     - Run tests (local)"
	@echo ""
	@echo "For full deployment automation:"
	@echo "  ./deploy.sh init  - Initialize production deployment"
	@echo "  ./deploy.sh ssl   - Setup SSL certificates"
# Production Commands
production:
	@echo "🚀 Starting production environment..."
	docker compose -f docker-compose.production.yml up -d --build

logs:
	@echo "📋 Viewing application logs..."
	docker compose -f docker-compose.production.yml logs -f

status:
	@echo "📊 Checking service status..."
	docker compose -f docker-compose.production.yml ps

backup:
	@echo "💾 Creating database backup..."
	./deploy.sh backup

restore:
	@echo "🔄 Restoring from backup..."
	@test -n "$(BACKUP_FILE)" || (echo "❌ Please specify BACKUP_FILE=path/to/backup" && exit 1)
	./deploy.sh restore $(BACKUP_FILE)

clean:
	@echo "🧹 Cleaning up Docker resources..."
	docker compose -f docker-compose.production.yml down -v
	docker system prune -f
	docker volume prune -f

# Development Helpers (for local development only)
dev-install:
	@echo "📦 Installing development dependencies..."
	pip install -r requirements.txt

dev-migrate:
	@echo "🗃️ Running migrations..."
	python manage.py migrate

dev-seed:
	@echo "🌱 Seeding database..."
	python seed_database.py

dev-test:
	@echo "🧪 Running tests..."
	python manage.py test


