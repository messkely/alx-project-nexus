# ALX E-Commerce Backend - Docker & EC2 Ubuntu Makefile
# Updated: August 8, 2025

.PHONY: help docker-build docker-up docker-down docker-dev docker-prod docker-logs docker-shell docker-clean ec2-deploy ec2-update ec2-status local-dev local-test local-migrate local-seed check-env setup-dev

# Default target
help:
	@echo "🚀 ALX E-Commerce Backend - Docker, EC2 & Local Development"
	@echo "============================================================"
	@echo ""
	@echo "🐳 Docker Commands:"
	@echo "  make docker-build  - Build Docker images"
	@echo "  make docker-dev    - Run development environment with Docker"
	@echo "  make docker-prod   - Run production environment with Docker"
	@echo "  make docker-down   - Stop all Docker containers"
	@echo "  make docker-logs   - View Docker container logs"
	@echo "  make docker-shell  - Access Django shell in Docker"
	@echo "  make docker-clean  - Clean up Docker resources"
	@echo ""
	@echo "☁️ EC2 Ubuntu Deployment:"
	@echo "  make ec2-deploy   - Deploy to EC2 Ubuntu (full setup)"
	@echo "  make ec2-update   - Update existing EC2 deployment"
	@echo "  make ec2-status   - Check EC2 deployment status"
	@echo ""
	@echo "💻 Local Development:"
	@echo "  make local-dev    - Setup and run local development"
	@echo "  make local-test   - Run test suite"
	@echo "  make local-migrate- Run database migrations"
	@echo "  make local-seed   - Create local admin user"
	@echo "  make setup-dev    - Install development dependencies"
	@echo ""
	@echo "🔧 Utilities:"
	@echo "  make check-env    - Verify environment configuration"
	@echo ""
	@echo "📚 Documentation:"
	@echo "  EC2 Guide: docs/EC2_DEPLOYMENT.md"
	@echo "  Local Setup: docs/LOCAL_DEVELOPMENT_STATUS.md"

# Docker Commands
docker-build:
	@echo "🔨 Building Docker images..."
	docker compose build

docker-dev:
	@echo "🚀 Starting development environment with Docker..."
	@echo "📚 API Documentation: http://localhost:8000/"
	@echo "🔧 Admin Panel: http://localhost:8000/admin/ (admin/admin123)"
	@echo "❤️ Health Check: http://localhost:8000/health/"
	docker compose -f docker-compose.dev.yml up --build

docker-prod:
	@echo "🚀 Starting production environment with Docker..."
	@echo "🌐 Application: http://localhost/"
	@echo "🔧 Admin Panel: http://localhost/admin/ (admin/admin123)"
	@echo "📚 API Documentation: http://localhost/api/v1/docs/"
	docker compose up --build -d
	@echo "✅ Production environment started!"
	@make docker-status

docker-down:
	@echo "🛑 Stopping Docker containers..."
	docker compose down
	docker compose -f docker-compose.dev.yml down

docker-logs:
	@echo "📋 Viewing Docker logs..."
	docker compose logs -f

docker-shell:
	@echo "🐚 Accessing Django shell in Docker..."
	docker compose exec web python manage.py shell

docker-clean:
	@echo "🧹 Cleaning Docker resources..."
	docker compose down -v
	docker compose -f docker-compose.dev.yml down -v
	docker system prune -f
	docker volume prune -f

docker-status:
	@echo "📊 Docker Status:"
	@docker compose ps

docker-migrate:
	@echo "🗃️ Running database migrations in Docker..."
	docker compose exec web python manage.py migrate

docker-superuser:
	@echo "👤 Creating superuser in Docker..."
	docker compose exec web python manage.py createsuperuser

docker-test:
	@echo "🧪 Running tests in Docker..."
	docker compose exec web python manage.py test

docker-restart:
	@echo "🔄 Restarting Docker services..."
	docker compose restart

docker-stop:
	@echo "⏹️  Stopping Docker services..."
	docker compose stop

# EC2 Ubuntu Deployment Commands
ec2-deploy:
	@echo "☁️ Deploying to EC2 Ubuntu..."
	@./scripts/deploy-ec2.sh init

ec2-update:
	@echo "🔄 Updating EC2 deployment..."
	@./scripts/deploy-ec2.sh update

ec2-status:
	@echo "📊 Checking EC2 deployment status..."
	@./scripts/deploy-ec2.sh status

# Local Development Commands
local-dev: setup-dev local-migrate
	@echo "🚀 Starting local development server..."
	@echo "📚 API Documentation: http://127.0.0.1:8000/"
	@echo "🔧 Admin Panel: http://127.0.0.1:8000/admin/ (admin/admin123)"
	@echo "❤️ Health Check: http://127.0.0.1:8000/health/"
	@echo ""
	python manage.py runserver

setup-dev:
	@echo "📦 Installing development dependencies..."
	pip install -r requirements.txt
	@echo "✅ Dependencies installed"

local-migrate:
	@echo "🗃️ Running local database migrations..."
	python manage.py migrate
	@echo "✅ Migrations completed"

local-seed:
	@echo "🌱 Creating local admin user..."
	@python manage.py shell -c "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('admin', 'admin@example.com', 'admin123') if not User.objects.filter(username='admin').exists() else print('✅ Admin user already exists (admin/admin123)')"
	@echo "✅ Local admin user ready"

local-test:
	@echo "🧪 Running test suite..."
	python manage.py test

# Environment and Setup
check-env:
	@echo "🔍 Checking environment configuration..."
	@test -f .env || (echo "❌ .env not found for local development" && exit 1)
	@echo "✅ Environment files found"
	@echo ""
	@echo "📋 Environment Status:"
	@echo "  Local Development: .env ✅"
