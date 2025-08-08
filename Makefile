# Django E-commerce Docker Management

.PHONY: help build dev prod up down logs clean test shell migrate superuser

# Default target
help:
	@echo "🐳 Django E-commerce Docker Commands"
	@echo "=================================="
	@echo "Development:"
	@echo "  make dev          - Start development environment"
	@echo "  make dev-up       - Start dev services in background"
	@echo "  make dev-build    - Build and start dev environment"
	@echo ""
	@echo "Production:"
	@echo "  make prod         - Start production environment"
	@echo "  make prod-up      - Start prod services in background"
	@echo "  make prod-build   - Build and start prod environment"
	@echo ""
	@echo "General:"
	@echo "  make build        - Build Docker images"
	@echo "  make up           - Start all services"
	@echo "  make down         - Stop all services"
	@echo "  make logs         - View logs"
	@echo "  make ps           - Show running containers"
	@echo ""
	@echo "Django Management:"
	@echo "  make shell        - Django shell"
	@echo "  make migrate      - Run database migrations"
	@echo "  make superuser    - Create superuser"
	@echo "  make collectstatic - Collect static files"
	@echo "  make test         - Run tests"
	@echo ""
	@echo "Maintenance:"
	@echo "  make clean        - Remove containers and volumes"
	@echo "  make clean-all    - Remove everything including images"
	@echo "  make backup-db    - Backup database"

# Build Docker images
build:
	docker compose build

# Development environment
dev:
	docker compose -f docker-compose.yml -f docker-compose.dev.yml up

dev-up:
	docker compose -f docker-compose.yml -f docker-compose.dev.yml up -d

dev-build:
	docker compose -f docker-compose.yml -f docker-compose.dev.yml up --build -d

# Production environment
prod:
	docker compose -f docker-compose.yml -f docker-compose.prod.yml up

prod-up:
	docker compose -f docker-compose.yml -f docker-compose.prod.yml up -d

prod-build:
	docker compose -f docker-compose.yml -f docker-compose.prod.yml up --build -d

# Basic Docker Compose commands
up:
	docker compose up -d

down:
	docker compose down

logs:
	docker compose logs -f

ps:
	docker compose ps

# Django management commands
shell:
	docker compose exec web python manage.py shell

migrate:
	docker compose exec web python manage.py migrate

makemigrations:
	docker compose exec web python manage.py makemigrations

superuser:
	docker compose exec web python manage.py createsuperuser

collectstatic:
	docker compose exec web python manage.py collectstatic --noinput

test:
	docker compose exec web python manage.py test

test-coverage:
	docker compose exec web coverage run --source='.' manage.py test
	docker compose exec web coverage report

# Database operations
dbshell:
	docker compose exec db psql -U ecommerce_user -d ecommerce

backup-db:
	docker compose exec db pg_dump -U ecommerce_user ecommerce > backup_$$(date +%Y%m%d_%H%M%S).sql

restore-db:
	@read -p "Enter backup file path: " backup_file; \
	docker compose exec -T db psql -U ecommerce_user ecommerce < $$backup_file

# Maintenance
clean:
	docker compose down -v
	docker system prune -f

clean-all:
	docker compose down -v --rmi all
	docker system prune -af

# Monitoring
stats:
	docker stats

inspect-web:
	docker compose exec web bash

inspect-db:
	docker compose exec db bash

# Setup commands
setup-env:
	cp .env.example .env
	@echo "⚠️  Edit .env file with your configuration!"

init-dev: setup-env dev-build migrate superuser
	@echo "✅ Development environment initialized!"

init-prod: setup-env prod-build migrate
	@echo "✅ Production environment initialized!"
