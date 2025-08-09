# 🛒 ALX E-Commerce Backend

A## 🛠️ Tech Stack

**Backend:** Django 5.2.1, Django REST Framework  
**Database:** PostgreSQL 15  
**Cache:** Redis 7  
**Server:** Nginx + Gunicorn  
**Security:** JWT Authentication, HTTPS/SSL  
**Deployment:** Docker, AWS EC2

## 📁 Project Structureoduction-ready e-commerce backend built with Django REST Framework, containerized with Docker, and deployed on AWS EC2 with HTTPS.

**🌐 Live API:** https://ecom-backend.store/

## 🚀 Quick Start

### Production Deployment
```bash
# Clone repository
git clone https://github.com/messkely/alx-project-nexus.git
cd alx-project-nexus

# Deploy to production
docker compose -f docker-compose.prod.yml up -d
```

### Development Setup
```bash
# Start development environment
docker compose up -d

# Run migrations
docker compose exec web python manage.py migrate

# Create superuser
docker compose exec web python manage.py createsuperuser
```

## �️ Tech Stack

## 📁 Project Structure

```
alx-project-nexus/
├── cart/                    # Shopping cart app
├── catalog/                 # Products & categories
├── ecommerce_backend/       # Django settings
├── orders/                  # Order management
├── reviews/                 # Product reviews
├── users/                   # User management
├── nginx/                   # Nginx configuration
├── scripts/                 # Deployment scripts
└── docker-compose.prod.yml  # Production containers
```

## 🌐 API Endpoints

**Authentication:**
- `POST /api/v1/auth/register/` - User registration
- `POST /api/v1/auth/login/` - User login
- `POST /api/v1/auth/refresh/` - Token refresh

**Products:**
- `GET /api/v1/catalog/products/` - List products
- `POST /api/v1/catalog/products/` - Create product (admin)
- `GET /api/v1/catalog/categories/` - List categories

**Orders & Cart:**
- `GET /api/v1/cart/` - View cart
- `POST /api/v1/cart/add/` - Add to cart
- `POST /api/v1/orders/` - Create order

## 🔧 Environment Variables

```env
DEBUG=False
SECRET_KEY=your_secret_key
ALLOWED_HOSTS=yourdomain.com,your-ip-address
DB_NAME=ecommerce_db
DB_USER=ecommerce_user
DB_PASSWORD=your_password
DB_HOST=db
REDIS_URL=redis://redis:6379
```

## 🧪 Testing

```bash
# Run all tests
docker compose exec web python manage.py test

# Run specific app tests
docker compose exec web python manage.py test catalog

# Check test coverage
docker compose exec web coverage run --source='.' manage.py test
docker compose exec web coverage report
```

## 📝 License

This project is licensed under the MIT License.
