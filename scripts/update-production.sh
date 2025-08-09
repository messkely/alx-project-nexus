#!/bin/bash
# Quick Update Script for EC2 Production
# Run this script on your EC2 instance to update the project

set -e

echo "🚀 Starting ALX E-Commerce Production Update"
echo "=============================================="

# Navigate to project directory
cd ~/alx-project-nexus

echo "1. 📥 Pulling latest changes from GitHub..."
git pull origin main

echo "2. 🛑 Stopping current containers..."
docker compose -f docker-compose.prod.yml down

echo "3. 🏗️ Rebuilding containers with latest code..."
docker compose -f docker-compose.prod.yml build --no-cache

echo "4. 🚀 Starting updated containers..."
docker compose -f docker-compose.prod.yml up -d

echo "5. ⏳ Waiting for services to start..."
sleep 30

echo "6. 🔍 Checking container health..."
docker compose -f docker-compose.prod.yml ps

echo "7. 🧪 Testing health endpoint..."
curl -f https://ecom-backend.store/health/ || echo "⚠️ Health check failed"

echo ""
echo "✅ Production update completed!"
echo "🌐 Site available at: https://ecom-backend.store"
echo "📊 Check status: docker compose -f docker-compose.prod.yml ps"
echo "📋 View logs: docker compose -f docker-compose.prod.yml logs -f"
