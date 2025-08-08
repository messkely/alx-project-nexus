# Database Schema and Seeding Documentation
**Updated:** August 8, 2025

This directory contains comprehensive database schema and data seeding scripts for the ALX E-Commerce Django application.

## Files Overview

### 1. `database_schema.sql`
Complete PostgreSQL database schema that mirrors the Django models. This includes:
- All tables with proper relationships and constraints
- Indexes for performance optimization
- Django admin and auth system tables
- Comments for documentation

### 2. `seed_database.py`
Comprehensive Python script that uses Django ORM to populate the database with realistic sample data:
- Users (including admin user)
- User addresses with default address support
- Product categories with slugs
- Products with pricing, inventory, and categorization
- Shopping carts and cart items
- Orders with various statuses and order items
- Product reviews with 1-5 star ratings

### 3. `seed_data.sql`
Direct SQL script that can be run on PostgreSQL database to insert sample data without Django.
Useful for Docker initialization and production data seeding.

## Database Schema Overview

The e-commerce application consists of the following main entities:

### Users App
- **users_user**: Custom user model extending Django's AbstractUser
  - Email-based authentication
  - Profile information (first_name, last_name, phone)
  - Role-based permissions (staff, superuser)
- **users_address**: User shipping addresses with default address support
  - Multiple addresses per user
  - Default address selection
  - Complete address information

### Catalog App  
- **catalog_category**: Product categories with hierarchical support
  - SEO-friendly slugs
  - Category descriptions
  - Nested category support
- **catalog_product**: Products with comprehensive details
  - Pricing and inventory management
  - SEO-friendly slugs
  - Image upload support
  - Category relationships
  - Stock quantity tracking

### Cart App
- **cart_cart**: Shopping carts for authenticated users
  - One cart per user
  - Automatic cart creation
  - Total calculation
- **cart_cartitem**: Items within shopping carts
  - Product-cart relationships
  - Quantity management
  - Subtotal calculations

### Orders App
- **orders_order**: Customer orders with status tracking
  - Order status workflow (pending, processing, shipped, delivered)
  - Order totals and timestamps
  - User relationships
- **orders_orderitem**: Individual items within orders
  - Product snapshot at order time
  - Quantity and pricing preservation
  - Order-product relationships

### Reviews App
- **reviews_review**: Product reviews with ratings
  - 1-5 star rating system
  - Review text and timestamps
  - User-product relationships
  - One review per user per product

## Production Usage Instructions

### Option 1: Automated Production Deployment
```bash
# Deploy with automated script (includes database setup)
./deploy.sh init

# The deployment script automatically:
# - Creates database schema
# - Runs Django migrations
# - Seeds with sample data (optional)
```

### Option 2: Manual Django ORM Setup (Development)

1. **Ensure Django environment is properly configured:**
   ```bash
   cd /home/fedora/Projects/alx-project-nexus
   source venv/bin/activate  # If using virtual environment
   python manage.py migrate
   ```

2. **Run the comprehensive seeding script:**
   ```bash
   python seed_database.py
   ```

### Option 3: Docker Production Environment

1. **Using production Docker setup:**
   ```bash
   # Start production environment
   docker compose -f docker-compose.production.yml up -d

   # Run migrations
   docker compose -f docker-compose.production.yml exec web python manage.py migrate

   # Seed database (optional)
   docker compose -f docker-compose.production.yml exec web python seed_database.py
   ```

### Option 4: Direct SQL Execution (Advanced)

1. **Create database schema:**
   ```bash
   psql -h localhost -U ecommerce_user -d ecommerce -f database_schema.sql
   ```

2. **Insert sample data:**
   ```bash
   psql -h localhost -U ecommerce_user -d ecommerce -f seed_data.sql
   ```

## Sample Data Contents

### Users
- **Admin User**: `admin@ecommerce.com` / `adminpass123`
- **Test Customer**: `john.doe@example.com` / `testpass123`
- **Staff User**: `staff@ecommerce.com` / `staffpass123`

### Categories
- Electronics (smartphones, laptops, tablets)
- Clothing (men's, women's, accessories)
- Home & Garden (furniture, decor, appliances)
- Books (fiction, non-fiction, educational)

### Products
- 20+ sample products across all categories
- Realistic pricing and descriptions
- Stock quantities for inventory testing
- SEO-friendly slugs

### Orders & Reviews
- Sample orders in various statuses
- Product reviews with ratings
- Realistic order data for testing

## Database Performance Considerations

### Indexes
The schema includes optimized indexes for:
- User lookups (email, username)
- Product searches (title, category, price)
- Order queries (user, date, status)
- Review lookups (product, user)

### Relationships
- Foreign key constraints maintain data integrity
- Optimized JOIN operations for API queries
- Cascading deletes where appropriate

### Production Optimization
```sql
-- Example performance queries
SELECT schemaname, tablename, attname, n_distinct 
FROM pg_stats 
WHERE schemaname='public' 
ORDER BY n_distinct DESC;

-- Analyze table statistics
ANALYZE catalog_product;
ANALYZE orders_order;
```

## Backup and Recovery

### Automated Backups (Production)
```bash
# Create backup using deployment script
./deploy.sh backup

# Backups are stored in backups/ directory with timestamps
```

### Manual Backup
```bash
# Database dump
pg_dump -h localhost -U ecommerce_user ecommerce > backup_$(date +%Y%m%d_%H%M%S).sql

# Restore from backup
psql -h localhost -U ecommerce_user ecommerce < backup_file.sql
```

### Docker Backup
```bash
# Backup from Docker container
docker compose -f docker-compose.production.yml exec db pg_dump -U ecommerce_user ecommerce > backup.sql

# Restore to Docker container
docker compose -f docker-compose.production.yml exec -T db psql -U ecommerce_user ecommerce < backup.sql
```

---

**Database schema is production-ready and optimized for high-performance e-commerce operations.**
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
