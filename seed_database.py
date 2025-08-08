#!/usr/bin/env python3
"""
ALX E-Commerce Backend - Database Seeding Script
This script populates the database with comprehensive sample data for all models.

Features:
- Creates admin and regular users with proper authentication
- Seeds product catalog with categories and stock levels
- Generates sample orders, carts, and reviews
- Maintains data consistency with production-ready structure

Usage:
    python seed_database.py

Requirements:
- Django environment properly configured
- Database migrations completed
- All app models available

Last Updated: August 7, 2025
"""

import os
import sys
import django
from decimal import Decimal
from datetime import datetime, timedelta
import random

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce_backend.settings')
django.setup()

from django.contrib.auth.hashers import make_password
from users.models import User, Address
from catalog.models import Category, Product
from cart.models import Cart, CartItem
from orders.models import Order, OrderItem
from reviews.models import Review


def create_users():
    """Create sample users including admin with consistent email domains."""
    print("Creating users...")
    
    # Create superuser
    if not User.objects.filter(email="admin@alxecommerce.com").exists():
        admin = User.objects.create_user(
            email="admin@alxecommerce.com",
            username="admin",
            password="admin123",
            first_name="Admin",
            last_name="User",
            is_staff=True,
            is_superuser=True
        )
        print(f"✓ Created superuser: {admin.email}")
    
    # Create regular users (matching seed_data.sql)
    users_data = [
        {
            "email": "john.doe@example.com",
            "username": "johndoe",
            "password": "userpass123",
            "first_name": "John",
            "last_name": "Doe"
        },
        {
            "email": "jane.smith@example.com",
            "username": "janesmith",
            "password": "userpass123",
            "first_name": "Jane",
            "last_name": "Smith"
        },
        {
            "email": "bob.wilson@example.com",
            "username": "bobwilson",
            "password": "userpass123",
            "first_name": "Bob",
            "last_name": "Wilson"
        },
        {
            "email": "alice.brown@example.com",
            "username": "alicebrown",
            "password": "userpass123",
            "first_name": "Alice",
            "last_name": "Brown"
        },
        {
            "email": "charlie.davis@example.com",
            "username": "charliedavis",
            "password": "userpass123",
            "first_name": "Charlie",
            "last_name": "Davis"
        },
        {
            "email": "sarah.jones@example.com",
            "username": "sarahjones",
            "password": "userpass123",
            "first_name": "Sarah",
            "last_name": "Jones"
        },
        {
            "email": "mike.thompson@example.com",
            "username": "mikethompson",
            "password": "userpass123",
            "first_name": "Mike",
            "last_name": "Thompson"
        }
    ]
    
    created_users = []
    for user_data in users_data:
        if not User.objects.filter(email=user_data["email"]).exists():
            user = User.objects.create_user(**user_data)
            created_users.append(user)
            print(f"✓ Created user: {user.email}")
        else:
            user = User.objects.get(email=user_data["email"])
            created_users.append(user)
            print(f"→ User already exists: {user.email}")
    
    return created_users


def create_addresses(users):
    """Create sample addresses for users."""
    print("\nCreating addresses...")
    
    addresses_data = [
        {
            "first_name": "John",
            "last_name": "Doe",
            "address_line_1": "123 Main Street",
            "address_line_2": "Apt 4B",
            "city": "New York",
            "postal_code": "10001",
            "country": "United States",
            "phone_number": "+1-555-0101",
            "is_default": True
        },
        {
            "first_name": "Jane",
            "last_name": "Smith",
            "address_line_1": "456 Oak Avenue",
            "address_line_2": "",
            "city": "Los Angeles",
            "postal_code": "90210",
            "country": "United States",
            "phone_number": "+1-555-0102",
            "is_default": True
        },
        {
            "first_name": "Bob",
            "last_name": "Wilson",
            "address_line_1": "789 Pine Road",
            "address_line_2": "Suite 300",
            "city": "Chicago",
            "postal_code": "60601",
            "country": "United States",
            "phone_number": "+1-555-0103",
            "is_default": True
        },
        {
            "first_name": "Alice",
            "last_name": "Brown",
            "address_line_1": "321 Elm Street",
            "address_line_2": "",
            "city": "Houston",
            "postal_code": "77001",
            "country": "United States",
            "phone_number": "+1-555-0104",
            "is_default": True
        },
        {
            "first_name": "Charlie",
            "last_name": "Davis",
            "address_line_1": "654 Maple Drive",
            "address_line_2": "Unit 12",
            "city": "Phoenix",
            "postal_code": "85001",
            "country": "United States",
            "phone_number": "+1-555-0105",
            "is_default": True
        },
        {
            "first_name": "Sarah",
            "last_name": "Jones",
            "address_line_1": "987 Cedar Lane",
            "address_line_2": "",
            "city": "Miami",
            "postal_code": "33101",
            "country": "United States",
            "phone_number": "+1-555-0106",
            "is_default": True
        },
        {
            "first_name": "Mike",
            "last_name": "Thompson",
            "address_line_1": "147 Birch Avenue",
            "address_line_2": "Floor 2",
            "city": "Seattle",
            "postal_code": "98101",
            "country": "United States",
            "phone_number": "+1-555-0107",
            "is_default": True
        }
    ]
    
    for i, user in enumerate(users[:len(addresses_data)]):
        if not Address.objects.filter(user=user).exists():
            address_data = addresses_data[i]
            address_data["user"] = user
            address = Address.objects.create(**address_data)
            print(f"✓ Created address for {user.email}")
        else:
            print(f"→ Address already exists for {user.email}")


def create_categories():
    """Create product categories with descriptions."""
    print("\nCreating categories...")
    
    categories_data = [
        {"name": "Electronics", "description": "Electronic devices, gadgets, and technology products"},
        {"name": "Clothing", "description": "Fashion, apparel, and accessories for all ages"},
        {"name": "Books", "description": "Books, magazines, and educational materials"},
        {"name": "Sports", "description": "Sports equipment, fitness gear, and outdoor activities"},
        {"name": "Home & Garden", "description": "Home improvement, furniture, and gardening supplies"},
        {"name": "Health & Beauty", "description": "Personal care, cosmetics, and wellness products"},
        {"name": "Toys & Games", "description": "Children's toys, board games, and entertainment"},
        {"name": "Automotive", "description": "Car parts, accessories, and automotive supplies"}
    ]
    
    created_categories = []
    for category_data in categories_data:
        category, created = Category.objects.get_or_create(
            name=category_data["name"],
            defaults={"description": category_data["description"]}
        )
        created_categories.append(category)
        if created:
            print(f"✓ Created category: {category.name}")
        else:
            print(f"→ Category already exists: {category.name}")
    
    return created_categories


def create_products(categories):
    """Create sample products with stock_quantity field."""
    print("\nCreating products...")
    
    products_data = [
        # Electronics
        {"title": "Wireless Bluetooth Headphones", "description": "Premium noise-canceling wireless headphones with 30-hour battery life", "price": "149.99", "stock_quantity": 50, "category": "Electronics"},
        {"title": "Gaming Mechanical Keyboard", "description": "RGB backlit mechanical gaming keyboard with Cherry MX switches", "price": "89.99", "stock_quantity": 75, "category": "Electronics"},
        {"title": "Smartphone Case", "description": "Durable protective case for smartphones with shock absorption", "price": "19.99", "stock_quantity": 200, "category": "Electronics"},
        {"title": "Smart Watch", "description": "Advanced fitness tracking smartwatch with heart rate monitor", "price": "299.99", "stock_quantity": 40, "category": "Electronics"},
        {"title": "Bluetooth Speaker", "description": "Portable wireless speaker with rich bass and 12-hour battery", "price": "79.99", "stock_quantity": 85, "category": "Electronics"},
        
        # Clothing
        {"title": "Leather Jacket", "description": "Premium genuine leather jacket in classic black", "price": "199.99", "stock_quantity": 25, "category": "Clothing"},
        {"title": "Cotton T-Shirt", "description": "Comfortable 100% cotton t-shirt available in multiple colors", "price": "24.99", "stock_quantity": 150, "category": "Clothing"},
        {"title": "Running Sneakers", "description": "Lightweight running shoes with advanced cushioning technology", "price": "129.99", "stock_quantity": 100, "category": "Clothing"},
        {"title": "Designer Jeans", "description": "Premium denim jeans with modern fit and styling", "price": "89.99", "stock_quantity": 70, "category": "Clothing"},
        {"title": "Winter Jacket", "description": "Insulated winter jacket for extreme cold weather", "price": "179.99", "stock_quantity": 45, "category": "Clothing"},
        
        # Books
        {"title": "Bestselling Novel", "description": "Award-winning fiction novel by renowned author", "price": "14.99", "stock_quantity": 300, "category": "Books"},
        {"title": "Programming Guide", "description": "Comprehensive guide to modern web development", "price": "39.99", "stock_quantity": 80, "category": "Books"},
        {"title": "Cook Book Collection", "description": "Professional chef recipes and cooking techniques", "price": "29.99", "stock_quantity": 120, "category": "Books"},
        {"title": "Science Fiction Novel", "description": "Thrilling space adventure story with compelling characters", "price": "16.99", "stock_quantity": 180, "category": "Books"},
        {"title": "History Biography", "description": "Detailed biography of influential historical figure", "price": "22.99", "stock_quantity": 95, "category": "Books"},
        
        # Sports
        {"title": "Yoga Mat", "description": "Non-slip exercise yoga mat with carrying strap", "price": "34.99", "stock_quantity": 90, "category": "Sports"},
        {"title": "Dumbbell Set", "description": "Adjustable dumbbell set for home gym workouts", "price": "249.99", "stock_quantity": 35, "category": "Sports"},
        {"title": "Tennis Racket", "description": "Professional grade tennis racket for competitive play", "price": "159.99", "stock_quantity": 60, "category": "Sports"},
        {"title": "Basketball", "description": "Official size and weight basketball for indoor/outdoor play", "price": "49.99", "stock_quantity": 110, "category": "Sports"},
        {"title": "Fitness Tracker", "description": "Waterproof fitness band with sleep and activity monitoring", "price": "99.99", "stock_quantity": 120, "category": "Sports"},
    ]
    
    created_products = []
    category_dict = {cat.name: cat for cat in categories}
    
    for product_data in products_data:
        category = category_dict.get(product_data["category"])
        if category and not Product.objects.filter(title=product_data["title"]).exists():
            product = Product.objects.create(
                title=product_data["title"],
                description=product_data["description"],
                price=Decimal(product_data["price"]),
                stock_quantity=product_data["stock_quantity"],
                category=category
            )
            created_products.append(product)
            print(f"✓ Created product: {product.title}")
        elif Product.objects.filter(title=product_data["title"]).exists():
            product = Product.objects.get(title=product_data["title"])
            created_products.append(product)
            print(f"→ Product already exists: {product.title}")
    
    return created_products


def create_carts_and_items(users, products):
    """Create sample shopping carts with items."""
    print("\nCreating shopping carts...")
    
    for user in users[:3]:  # Create carts for first 3 users
        cart, created = Cart.objects.get_or_create(user=user)
        if created:
            print(f"✓ Created cart for {user.email}")
            
            # Add random items to cart
            selected_products = random.sample(products, min(3, len(products)))
            for product in selected_products:
                if not CartItem.objects.filter(cart=cart, product=product).exists():
                    CartItem.objects.create(
                        cart=cart,
                        product=product,
                        quantity=random.randint(1, 3)
                    )
                    print(f"  → Added {product.title} to cart")
        else:
            print(f"→ Cart already exists for {user.email}")


def create_orders_and_items(users, products):
    """Create sample orders with items."""
    print("\nCreating orders...")
    
    statuses = ['pending', 'completed', 'failed']
    payment_statuses = ['paid', 'unpaid']
    
    for i, user in enumerate(users[:4]):  # Create orders for first 4 users
        # Create 1-2 orders per user
        num_orders = random.randint(1, 2)
        
        for order_num in range(num_orders):
            order_exists = Order.objects.filter(user=user).count() >= num_orders
            if not order_exists:
                # Select random products for this order
                selected_products = random.sample(products, random.randint(1, 4))
                
                total_amount = Decimal('0.00')
                order_items_data = []
                
                for product in selected_products:
                    quantity = random.randint(1, 3)
                    unit_price = product.price
                    subtotal = unit_price * quantity
                    total_amount += subtotal
                    
                    order_items_data.append({
                        'product': product,
                        'quantity': quantity,
                        'unit_price': unit_price,
                        'subtotal': subtotal
                    })
                
                # Create the order
                order = Order.objects.create(
                    user=user,
                    status=random.choice(statuses),
                    payment_status=random.choice(payment_statuses),
                    total_amount=total_amount,
                    created_at=datetime.now() - timedelta(days=random.randint(1, 30))
                )
                
                # Create order items
                for item_data in order_items_data:
                    OrderItem.objects.create(
                        order=order,
                        **item_data
                    )
                
                print(f"✓ Created order #{order.id} for {user.email} (${total_amount})")


def create_reviews(users, products):
    """Create sample product reviews."""
    print("\nCreating reviews...")
    
    comments = [
        "Great product! Highly recommended.",
        "Good value for money.",
        "Fast delivery and excellent quality.",
        "Exactly as described. Very satisfied.",
        "Could be better, but decent for the price.",
        "Outstanding quality and service.",
        "Not what I expected, but still okay.",
        "Perfect! Will buy again.",
        "Good product but shipping was slow.",
        "Excellent customer service and product quality."
    ]
    
    # Create reviews for random user-product combinations
    for user in users:
        # Each user reviews 2-4 random products
        user_products = random.sample(products, min(random.randint(2, 4), len(products)))
        
        for product in user_products:
            if not Review.objects.filter(user=user, product=product).exists():
                review = Review.objects.create(
                    user=user,
                    product=product,
                    rating=random.randint(3, 5),  # Mostly positive reviews
                    comment=random.choice(comments),
                    created_at=datetime.now() - timedelta(days=random.randint(1, 60))
                )
                print(f"✓ Created review by {user.email} for {product.title} ({review.rating}★)")


def main():
    """Main function to run all seeding operations."""
    print("=== E-commerce Database Seeding Script ===\n")
    
    try:
        # Create users
        users = create_users()
        
        # Create addresses
        create_addresses(users)
        
        # Create categories
        categories = create_categories()
        
        # Create products
        products = create_products(categories)
        
        # Create carts and cart items
        create_carts_and_items(users, products)
        
        # Create orders and order items
        create_orders_and_items(users, products)
        
        # Create reviews
        create_reviews(users, products)
        
        print(f"\n=== Seeding Complete! ===")
        print(f"✓ Users: {User.objects.count()}")
        print(f"✓ Addresses: {Address.objects.count()}")
        print(f"✓ Categories: {Category.objects.count()}")
        print(f"✓ Products: {Product.objects.count()}")
        print(f"✓ Carts: {Cart.objects.count()}")
        print(f"✓ Cart Items: {CartItem.objects.count()}")
        print(f"✓ Orders: {Order.objects.count()}")
        print(f"✓ Order Items: {OrderItem.objects.count()}")
        print(f"✓ Reviews: {Review.objects.count()}")
        
        print(f"\nAdmin credentials:")
        print(f"Email: admin@ecommerce.com")
        print(f"Password: admin123")
        
    except Exception as e:
        print(f"❌ Error during seeding: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
