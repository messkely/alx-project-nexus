# Database Schema and Seeding Documentation

This directory contains comprehensive database schema and data seeding scripts for the Django e-commerce application.

## Files Overview

### 1. `database_schema.sql`
Complete PostgreSQL database schema that mirrors the Django models. This includes:
- All tables with proper relationships and constraints
- Indexes for performance optimization
- Django admin and auth system tables
- Comments for documentation

### 2. `seed_database.py`
Comprehensive Python script that uses Django ORM to populate the database with realistic sample data:
- Users (including admin)
- Addresses
- Categories and Products
- Shopping Carts
- Orders and Order Items
- Product Reviews

### 3. `scripts/django_seed_script.py`
Simplified Django shell script for quick data seeding using Django management commands.

### 4. `seed_data.sql`
Direct SQL script that can be run on PostgreSQL database to insert sample data without Django.

## Database Schema Overview

The e-commerce application consists of the following main entities:

### Users App
- **users_user**: Custom user model extending Django's AbstractUser
- **users_address**: User shipping addresses with default address support

### Catalog App  
- **catalog_category**: Product categories with slugs
- **catalog_product**: Products with pricing, inventory, and categorization

### Cart App
- **cart_cart**: Shopping carts for users
- **cart_cartitem**: Items within shopping carts

### Orders App
- **orders_order**: Customer orders with status tracking
- **orders_orderitem**: Individual items within orders

### Reviews App
- **reviews_review**: Product reviews with ratings (1-5 stars)

## Usage Instructions

### Option 1: Using Django ORM (Recommended)

1. **Ensure Django is properly configured:**
   ```bash
   cd /home/fedora/Projects/alx-project-nexus
   python manage.py migrate
   ```

2. **Run the comprehensive seeding script:**
   ```bash
   python seed_database.py
   ```

### Option 2: Using Django Shell

1. **Run migrations first:**
   ```bash
   python manage.py migrate
   ```

2. **Execute the Django shell script:**
   ```bash
   python manage.py shell < scripts/django_seed_script.py
   ```

### Option 3: Direct SQL Execution

1. **Create database schema:**
   ```bash
   psql -h localhost -U ecommerce_user -d ecommerce -f database_schema.sql
   ```

2. **Insert sample data:**
   ```bash
   psql -h localhost -U ecommerce_user -d ecommerce -f seed_data.sql
   ```

### Option 4: Using Docker Compose

If using the provided `docker-compose.yml`:

1. **Start the database:**
   ```bash
   docker-compose up -d db
   ```

2. **Wait for database to be ready, then run migrations:**
   ```bash
   python manage.py migrate
   ```

3. **Run seeding script:**
   ```bash
   python seed_database.py
   ```

## Sample Data Included

### Users
- **Admin User**: admin@ecommerce.com (password: admin123)
- **Regular Users**: 5 sample users with addresses
  - john.doe@email.com (password: userpass123)
  - jane.smith@email.com (password: userpass123)
  - bob.wilson@email.com (password: userpass123)
  - alice.brown@email.com (password: userpass123)
  - charlie.davis@email.com (password: userpass123)

### Products
- **25 sample products** across 8 categories:
  - Electronics (iPhone, Samsung, MacBook, etc.)
  - Clothing & Fashion (Jeans, Dresses, Shoes, etc.)
  - Home & Garden (Coffee Maker, Air Fryer, etc.)
  - Sports & Outdoors (Yoga Mat, Basketball, etc.)
  - Books & Media (Programming books, Fiction, etc.)
  - Health & Beauty
  - Toys & Games
  - Automotive

### Orders & Reviews
- Sample orders with different statuses
- Product reviews with ratings and comments
- Shopping cart items for testing

## Database Configuration

The application is configured to use PostgreSQL with the following default settings:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'ecommerce',
        'USER': 'ecommerce_user',
        'PASSWORD': 'ecommerce_pass',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

## Performance Considerations

The schema includes several indexes for optimal performance:
- Product price, creation date, and category indexes
- Order user and status indexes
- Review product and rating indexes
- Address user and default status indexes

## Views and Reporting

The SQL script creates helpful views:
- **order_summary**: Order overview with customer information
- **product_stats**: Product statistics with ratings and sales data

## Troubleshooting

### Common Issues

1. **Permission denied**: Ensure the PostgreSQL user has proper permissions
2. **Database connection errors**: Check database credentials in settings.py
3. **Migration conflicts**: Run `python manage.py makemigrations` if models have changed
4. **Duplicate data**: Scripts include conflict handling to prevent duplicate entries

### Verification

After running the scripts, verify the data:

```sql
-- Check record counts
SELECT 
    'Users' as entity, COUNT(*) as count FROM users_user
UNION ALL
SELECT 'Products', COUNT(*) FROM catalog_product
UNION ALL
SELECT 'Orders', COUNT(*) FROM orders_order
UNION ALL
SELECT 'Reviews', COUNT(*) FROM reviews_review;

-- View sample data
SELECT * FROM order_summary LIMIT 5;
SELECT * FROM product_stats LIMIT 10;
```

## Security Notes

- The sample passwords are hashed using Django's PBKDF2 algorithm
- Default passwords are provided for development/testing only
- Change all passwords before deploying to production
- Review user permissions and roles

## Extending the Data

To add more sample data:

1. Modify the respective arrays in `seed_database.py`
2. Adjust quantities and relationships as needed
3. Run the script again (it handles duplicates gracefully)

## Database Backup

Before making changes, backup your database:

```bash
pg_dump -h localhost -U ecommerce_user ecommerce > backup.sql
```

To restore:

```bash
psql -h localhost -U ecommerce_user -d ecommerce -f backup.sql
```
