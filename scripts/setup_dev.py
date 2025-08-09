#!/usr/bin/env python
"""
Development setup script for ALX E-Commerce Backend
Creates a superuser and sets up initial data if needed
"""

import os
import sys
import django

# Add the project root to the Python path
sys.path.insert(0, '/app')

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce_backend.settings')
django.setup()

from django.contrib.auth import get_user_model

def create_superuser():
    """Create a superuser if one doesn't exist"""
    User = get_user_model()
    
    if not User.objects.filter(username='admin').exists():
        print("Creating admin superuser...")
        User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
        print("Admin superuser created successfully!")
    else:
        print("Admin user already exists, skipping creation.")

def main():
    """Main setup function"""
    print("Running development setup...")
    
    # Create superuser
    create_superuser()
    
    print("Development setup completed!")

if __name__ == '__main__':
    main()
