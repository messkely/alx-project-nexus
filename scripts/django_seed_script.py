#!/usr/bin/env python3
"""
Django Management Command Script for Database Operations
Run with: python manage.py shell < django_seed_script.py
"""

from decimal import Decimal
from datetime import datetime, timedelta
import random

from django.contrib.auth.hashers import make_password
from users.models import User, Address
from catalog.models import Category, Product
from cart.models import Cart, CartItem
from orders.models import Order, OrderItem
from reviews.models import Review


def create_sample_data():
    """Create comprehensive sample data for the e-commerce application."""
    
    print("Starting database seeding...")
    
    # Create superuser
    if not User.objects.filter(email="admin@ecommerce.com").exists():
        admin = User.objects.create_superuser(
            email="admin@ecommerce.com",
            username="admin",
            password="admin123",
            first_name="Admin",
            last_name="User"
        )
        print(f"Created superuser: {admin.email}")
    
    # Create regular users
    users_data = [
        {"email": "john.doe@email.com", "username": "johndoe", "first_name": "John", "last_name": "Doe"},
        {"email": "jane.smith@email.com", "username": "janesmith", "first_name": "Jane", "last_name": "Smith"},
        {"email": "bob.wilson@email.com", "username": "bobwilson", "first_name": "Bob", "last_name": "Wilson"},
        {"email": "alice.brown@email.com", "username": "alicebrown", "first_name": "Alice", "last_name": "Brown"},
        {"email": "charlie.davis@email.com", "username": "charliedavis", "first_name": "Charlie", "last_name": "Davis"}
    ]
    
    users = []
    for user_data in users_data:
        user, created = User.objects.get_or_create(
            email=user_data["email"],
            defaults={**user_data, "password": make_password("userpass123")}
        )
        users.append(user)
        if created:
            print(f"Created user: {user.email}")
    
    # Create addresses
    addresses_data = [
        {"first_name": "John", "last_name": "Doe", "address_line_1": "123 Main Street", "city": "New York", "postal_code": "10001", "country": "United States", "phone_number": "+1-555-0101"},
        {"first_name": "Jane", "last_name": "Smith", "address_line_1": "456 Oak Avenue", "city": "Los Angeles", "postal_code": "90210", "country": "United States", "phone_number": "+1-555-0102"},
        {"first_name": "Bob", "last_name": "Wilson", "address_line_1": "789 Pine Road", "city": "Chicago", "postal_code": "60601", "country": "United States", "phone_number": "+1-555-0103"},
        {"first_name": "Alice", "last_name": "Brown", "address_line_1": "321 Elm Street", "city": "Houston", "postal_code": "77001", "country": "United States", "phone_number": "+1-555-0104"},
        {"first_name": "Charlie", "last_name": "Davis", "address_line_1": "654 Maple Drive", "city": "Phoenix", "postal_code": "85001", "country": "United States", "phone_number": "+1-555-0105"}
    ]
    
    for i, user in enumerate(users):
        if not Address.objects.filter(user=user).exists() and i < len(addresses_data):
            address_data = addresses_data[i]
            Address.objects.create(user=user, is_default=True, **address_data)
            print(f"Created address for {user.email}")
    
    # Create categories
    categories_data = [
        "Electronics", "Clothing & Fashion", "Home & Garden", "Sports & Outdoors", 
        "Books & Media", "Health & Beauty", "Toys & Games", "Automotive"
    ]
    
    categories = []
    for cat_name in categories_data:
        category, created = Category.objects.get_or_create(name=cat_name)
        categories.append(category)
        if created:
            print(f"Created category: {category.name}")
    
    # Create products
    products_data = [
        {"title": "iPhone 15 Pro", "description": "Latest iPhone with advanced camera", "price": "999.99", "inventory": 50, "category": "Electronics"},
        {"title": "Samsung Galaxy S24", "description": "Flagship Android smartphone", "price": "899.99", "inventory": 45, "category": "Electronics"},
        {"title": "MacBook Air M3", "description": "Lightweight laptop", "price": "1199.99", "inventory": 30, "category": "Electronics"},
        {"title": "Sony Headphones", "description": "Noise-canceling headphones", "price": "399.99", "inventory": 75, "category": "Electronics"},
        {"title": "Men's Jeans", "description": "Comfortable denim jeans", "price": "79.99", "inventory": 100, "category": "Clothing & Fashion"},
        {"title": "Summer Dress", "description": "Floral print dress", "price": "59.99", "inventory": 85, "category": "Clothing & Fashion"},
        {"title": "Running Shoes", "description": "Athletic shoes", "price": "129.99", "inventory": 60, "category": "Clothing & Fashion"},
        {"title": "Coffee Maker", "description": "12-cup programmable", "price": "89.99", "inventory": 35, "category": "Home & Garden"},
        {"title": "Air Fryer", "description": "4-quart digital", "price": "149.99", "inventory": 42, "category": "Home & Garden"},
        {"title": "Yoga Mat", "description": "Non-slip exercise mat", "price": "29.99", "inventory": 80, "category": "Sports & Outdoors"},
        {"title": "Basketball", "description": "Official size", "price": "24.99", "inventory": 65, "category": "Sports & Outdoors"},
        {"title": "Python Programming", "description": "Learn Python", "price": "49.99", "inventory": 45, "category": "Books & Media"},
        {"title": "Fiction Novel", "description": "Bestselling book", "price": "19.99", "inventory": 90, "category": "Books & Media"}
    ]
    
    category_dict = {cat.name: cat for cat in categories}
    products = []
    
    for product_data in products_data:
        category = category_dict.get(product_data["category"])
        if category:
            product, created = Product.objects.get_or_create(
                title=product_data["title"],
                defaults={
                    "description": product_data["description"],
                    "price": Decimal(product_data["price"]),
                    "inventory": product_data["inventory"],
                    "category": category
                }
            )
            products.append(product)
            if created:
                print(f"Created product: {product.title}")
    
    # Create carts and cart items
    for user in users[:3]:
        cart, created = Cart.objects.get_or_create(user=user)
        if created:
            # Add random items
            selected_products = random.sample(products, min(3, len(products)))
            for product in selected_products:
                CartItem.objects.get_or_create(
                    cart=cart, 
                    product=product,
                    defaults={"quantity": random.randint(1, 3)}
                )
            print(f"Created cart for {user.email}")
    
    # Create orders
    for user in users[:4]:
        if not Order.objects.filter(user=user).exists():
            selected_products = random.sample(products, random.randint(1, 3))
            total_amount = Decimal('0.00')
            
            for product in selected_products:
                total_amount += product.price * random.randint(1, 2)
            
            order = Order.objects.create(
                user=user,
                status=random.choice(['pending', 'completed']),
                payment_status=random.choice(['paid', 'unpaid']),
                total_amount=total_amount
            )
            
            for product in selected_products:
                quantity = random.randint(1, 2)
                OrderItem.objects.create(
                    order=order,
                    product=product,
                    quantity=quantity,
                    unit_price=product.price,
                    subtotal=product.price * quantity
                )
            
            print(f"Created order for {user.email}")
    
    # Create reviews
    comments = [
        "Great product! Highly recommended.",
        "Good value for money.",
        "Excellent quality.",
        "Very satisfied with purchase.",
        "Fast delivery."
    ]
    
    for user in users:
        user_products = random.sample(products, min(3, len(products)))
        for product in user_products:
            Review.objects.get_or_create(
                user=user,
                product=product,
                defaults={
                    "rating": random.randint(4, 5),
                    "comment": random.choice(comments)
                }
            )
    
    print("Database seeding completed!")
    print(f"Users: {User.objects.count()}")
    print(f"Categories: {Category.objects.count()}")
    print(f"Products: {Product.objects.count()}")
    print(f"Orders: {Order.objects.count()}")
    print(f"Reviews: {Review.objects.count()}")

# Run the function
create_sample_data()
