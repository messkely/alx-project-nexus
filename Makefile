# ALX E-Commerce Backend - EC2 Ubuntu Makefile
# Updated: August 8, 2025

.PHONY: help ec2-deploy ec2-update ec2-status local-dev local-test local-migrate local-seed check-env setup-dev

# Default target
help:
	@echo "🚀 ALX E-Commerce Backend - EC2 Ubuntu & Local Development"
	@echo "=========================================================="
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
