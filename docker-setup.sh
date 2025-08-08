#!/bin/bash

# Django E-commerce Docker Setup Script

set -e

echo "🐳 Setting up Django E-commerce with Docker..."

# Check if Docker Compose is available
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    exit 1
fi

# Check if Docker Compose (V2) is available
if ! docker compose version &> /dev/null; then
    echo "❌ Docker Compose is not available. Please install Docker Compose or enable the Docker Compose plugin."
    exit 1
fi

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "📝 Creating .env file from template..."
    cp .env.example .env
    echo "⚠️  Please edit .env file with your configuration before proceeding!"
    echo "   At minimum, change the SECRET_KEY value."
    read -p "Press Enter to continue after editing .env file..."
fi

# Choose environment
echo "🔧 Select environment:"
echo "1) Development (with hot reload)"
echo "2) Production (with Nginx)"
read -p "Enter your choice (1 or 2): " env_choice

# Build and start containers
if [ "$env_choice" = "1" ]; then
    echo "🚀 Starting development environment..."
    docker compose -f docker-compose.yml -f docker-compose.dev.yml up --build -d
    
    echo "⏳ Waiting for services to be ready..."
    sleep 10
    
    echo "📊 Creating superuser..."
    docker compose exec web python manage.py createsuperuser --noinput --email admin@example.com || true
    
    echo "🌱 Loading seed data..."
    docker compose exec web python manage.py loaddata seed_data.sql || true
    
    echo "✅ Development environment ready!"
    echo "🌐 Django API: http://localhost:8000/api/v1/"
    echo "📚 API Docs: http://localhost:8000/api/v1/docs/"
    echo "🔧 Admin Panel: http://localhost:8000/admin/"
    
elif [ "$env_choice" = "2" ]; then
    echo "🚀 Starting production environment..."
    docker compose -f docker-compose.yml -f docker-compose.prod.yml up --build -d
    
    echo "⏳ Waiting for services to be ready..."
    sleep 15
    
    echo "📊 Creating superuser..."
    docker compose exec web python manage.py createsuperuser --noinput --email admin@example.com || true
    
    echo "✅ Production environment ready!"
    echo "🌐 Application: http://localhost/"
    echo "📚 API Docs: http://localhost/api/v1/docs/"
    echo "🔧 Admin Panel: http://localhost/admin/"
    
else
    echo "❌ Invalid choice. Exiting."
    exit 1
fi

echo ""
echo "📋 Useful commands:"
echo "  View logs: docker compose logs -f"
echo "  Stop services: docker compose down"
echo "  Run tests: docker compose exec web python manage.py test"
echo "  Django shell: docker compose exec web python manage.py shell"
echo "  Database shell: docker compose exec db psql -U ecommerce_user -d ecommerce"

echo ""
echo "🎉 Setup complete! Your Django e-commerce API is running."
