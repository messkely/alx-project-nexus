#!/bin/sh
set -e

echo "Running migrations..."
python manage.py migrate

echo "Creating superuser..."
python manage.py shell << EOF
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
    print('Admin user created')
else:
    print('Admin user already exists')
EOF

echo "Starting Gunicorn..."
exec gunicorn ecommerce_backend.wsgi:application --bind 0.0.0.0:8000 --workers 3
