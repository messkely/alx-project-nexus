# scripts/seed_users.py
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce_backend.settings')
django.setup()

from users.models import User

def create_users():
    users = [
        {"email": "user1@example.com", "username": "user1", "password": "testpass123"},
        {"email": "user2@example.com", "username": "user2", "password": "testpass123"},
    ]

    for u in users:
        if not User.objects.filter(email=u["email"]).exists():
            User.objects.create_user(email=u["email"], username=u["username"], password=u["password"])
            print(f"Created user: {u['email']}")
        else:
            print(f"User already exists: {u['email']}")

    if not User.objects.filter(email="admin@example.com").exists():
        User.objects.create_superuser(email="admin@example.com", username="admin", password="admin123")
        print("Created superuser")
    else:
        print("Superuser already exists")

if __name__ == "__main__":
    create_users()
