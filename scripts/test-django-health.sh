#!/bin/bash
# Simple Django Health Check Script
# Test if Django can start without Docker

echo "🩺 Django Health Check (No Docker)"
echo "=================================="

# Check if we can import Django
echo "1. Testing Python and Django import..."
python3 -c "
import django
print(f'✅ Django version: {django.get_version()}')
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce_backend.settings')
django.setup()
print('✅ Django settings loaded successfully')
" || echo "❌ Django import/setup failed"

echo ""
echo "2. Testing Django management commands..."
python3 manage.py check --deploy || echo "❌ Django check failed"

echo ""
echo "3. Testing database connection (if available)..."
python3 manage.py shell -c "
from django.db import connection
try:
    with connection.cursor() as cursor:
        cursor.execute('SELECT 1')
    print('✅ Database connection successful')
except Exception as e:
    print(f'❌ Database connection failed: {e}')
"

echo ""
echo "4. Testing static files collection..."
python3 manage.py collectstatic --noinput --dry-run | head -10

echo ""
echo "✅ Django health check complete"
