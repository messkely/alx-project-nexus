# 🛒 ALX E-Commerce Backend - Production Ready

A enterprise-grade, scalable, and secure backend system for an e-commerce platform deployed on AWS EC2 with HTTPS. This project demonstrates real-world backend architecture with comprehensive security, testing, Docker containerization, and production deployment.

**🌐 Live Production URL:** https://ecom-backend.store/

---

## 🚀 Features

### 🔐 **Security & Authentication**
- ✅ **JWT Authentication** - Secure token-based authentication with refresh tokens
- ✅ **Role-based Access Control** - Admin, staff, and customer permissions
- ✅ **Security Middleware** - Rate limiting, CORS, CSRF protection
- ✅ **Admin Security** - Protected admin endpoints with enhanced permissions
- ✅ **Input Validation** - Comprehensive request validation and sanitization

### 📦 **Product & Catalog Management**
- ✅ **Complete Product CRUD** - Create, read, update, delete operations
- ✅ **Category Management** - Hierarchical product categorization
- ✅ **Advanced Filtering** - Filter by category, price range, availability
- ✅ **Search & Sorting** - Full-text search with multiple sorting options
- ✅ **Image Upload** - Product image handling with S3 storage
- ✅ **Inventory Tracking** - Stock quantity management

### 🛒 **E-Commerce Features**
- ✅ **Shopping Cart** - Add, update, remove cart items
- ✅ **Order Management** - Complete order processing system
- ✅ **Order Status** - Track orders from creation to delivery
- ✅ **User Profiles** - Customer profile management
- ✅ **Reviews & Ratings** - Product review system with ratings

### 📊 **API & Performance**
- ✅ **RESTful API Design** - Clean, consistent API endpoints
- ✅ **Pagination** - Efficient large dataset handling
- ✅ **Database Optimization** - Indexed queries and efficient relations
- ✅ **Caching** - ElastiCache Redis for improved performance
- ✅ **API Documentation** - Interactive Swagger/OpenAPI docs

### 🧪 **Testing & Quality**
- ✅ **Comprehensive Test Suite** - 63+ unit tests across all apps
- ✅ **API Testing** - Complete endpoint testing with authentication
- ✅ **Security Testing** - Vulnerability and permission testing
- ✅ **Test Coverage** - High test coverage for critical functionality

### 🐳 **Docker Containerization**
- ✅ **Multi-Container Setup** - Django, PostgreSQL, Redis, Nginx
- ✅ **Development Environment** - Hot reload with Docker Compose
- ✅ **Production Environment** - Optimized containers with Gunicorn
- ✅ **Nginx Reverse Proxy** - Static files and load balancing
- ✅ **Health Checks** - Container monitoring and auto-restart
- ✅ **Volume Management** - Persistent data and easy backups
- ✅ **SSL Ready** - HTTPS configuration with certificate support

### 🔒 **SSL/HTTPS Security**
- ✅ **Let's Encrypt SSL** - Trusted SSL certificates with auto-renewal
- ✅ **HTTPS Enforcement** - Automatic HTTP to HTTPS redirects
- ✅ **Domain Security** - Production domain (ecom-backend.store)
- ✅ **Security Headers** - HSTS, CSP, X-Frame-Options protection
- ✅ **HTTP/2 Support** - Modern protocol for better performance

### ☁️ **AWS EC2 Production Deployment**
- ✅ **EC2 Ubuntu Server** - Production server on AWS (98.87.47.179)
- ✅ **Docker Production** - Multi-container production setup
- ✅ **Nginx Reverse Proxy** - SSL termination and load balancing
- ✅ **Let's Encrypt Integration** - Automated certificate management
- ✅ **Health Monitoring** - Container health checks and auto-restart
- ✅ **Production Logging** - Comprehensive logging and monitoring

---

## 🧑‍💻 Tech Stack

### Backend Framework
| Technology | Version | Purpose |
|------------|---------|---------|
| **Django** | 5.2.1 | Web framework & ORM |
| **Django REST Framework** | 3.16.0 | API development |
| **PostgreSQL** | 15+ | Primary database |
| **Redis** | 7+ | Caching & sessions |

### Authentication & Security
| Technology | Version | Purpose |
|------------|---------|---------|
| **djangorestframework-simplejwt** | 5.5.0 | JWT authentication |
| **django-filter** | 25.1 | API filtering |
| **cryptography** | 44.0.0 | Security utilities |

### DevOps & Deployment
| Technology | Version | Purpose |
|------------|---------|---------|
| **AWS EC2** | Ubuntu 20.04+ | Virtual private server |
| **Nginx** | Latest | Reverse proxy and web server |
| **Gunicorn** | 23.0.0 | WSGI HTTP Server |
| **Supervisor** | Latest | Process control system |
| **Let's Encrypt** | Latest | SSL certificate automation |

### Documentation & Testing
| Technology | Version | Purpose |
|------------|---------|---------|
| **drf-yasg** | 1.21.7 | API documentation |
| **Django Test Framework** | Built-in | Unit & integration testing |

---

## 📁 Project Architecture

```
alx-project-nexus/
├── ☁️ AWS EC2 Deployment
│   ├── scripts/deploy-ec2.sh       # Automated EC2 Ubuntu deployment
│   └── .env.example                # Local environment template
│
├── 🏗️ Django Applications
│   ├── ecommerce_backend/           # Main Django project
│   │   ├── settings.py              # Environment-aware configuration
│   │   ├── urls.py                  # URL routing
│   │   ├── health_views.py          # AWS health check endpoints
│   │   ├── security_config.py       # Security settings
│   │   └── security_middleware.py   # Custom security middleware
│   │
│   ├── users/                       # User management & authentication
│   │   ├── models.py                # Custom user model
│   │   ├── views.py                 # Authentication views
│   │   ├── serializers.py           # User data serialization
│   │   └── permissions.py           # Custom permissions
│   │
│   ├── catalog/                     # Product & category management
│   │   ├── models.py                # Product, Category models
│   │   ├── views.py                 # CRUD operations
│   │   ├── serializers.py           # API serialization
│   │   └── permissions.py           # Product permissions
│   │
│   ├── cart/                        # Shopping cart functionality
│   │   ├── models.py                # Cart & CartItem models
│   │   ├── views.py                 # Cart operations
│   │   └── serializers.py           # Cart serialization
│   │
│   ├── orders/                      # Order processing
│   │   ├── models.py                # Order & OrderItem models
│   │   ├── views.py                 # Order management
│   │   └── serializers.py           # Order serialization
│   │
│   └── reviews/                     # Product reviews & ratings
│       ├── models.py                # Review model
│       ├── views.py                 # Review operations
│       └── serializers.py           # Review serialization
│
├── 🧪 Testing Suite
│   ├── tests/                       # Integration tests
│   │   ├── test_auth_endpoints.py   # Authentication testing
│   │   ├── test_products_api.py     # Product API testing
│   │   └── test_categories_api.py   # Category API testing
│   │
│   └── {app}/tests/                 # Unit tests per app
│       ├── test_models.py           # Model testing
│       ├── test_views.py            # View testing
│       └── test_serializers.py      # Serializer testing
│
├── 📚 Documentation
│   ├── README.md                    # Main documentation
│   ├── docs/                        # Documentation directory
│   │   ├── README.md                # Documentation index
│   │   ├── AWS_DEPLOYMENT.md        # AWS serverless deployment guide
│   │   ├── DATABASE_README.md        # Database schema docs
│   │   ├── DOCKER_README.md          # Docker deployment guide
│   │   ├── PRODUCTION_DEPLOYMENT.md  # VPS deployment guide
│   │   ├── TESTING_README.md         # Testing documentation
│   │   ├── SECURITY_AUDIT_REPORT.md  # Security assessment
│   │   └── api_testing_with_postman.md # API testing guide
│
├── ⚙️ Configuration & Scripts
│   ├── requirements-docker.txt      # Production dependencies
│   ├── scripts/                     # Automation and seeding scripts
│   │   ├── django_seed_script.py    # Django shell seeding script
│   │   ├── seed_database.py         # Comprehensive seeding script
│   │   └── deploy.sh                # Production deployment automation
│   ├── database_schema.sql          # Database schema
│   ├── seed_data.sql               # Sample data SQL
│   └── manage.py                   # Django management
│
└── 📦 Static & Media
    ├── static/                      # Static files
    ├── staticfiles/                 # Collected static files
    ├── media/                       # User uploads
    └── logs/                        # Application logs
```

---

## 🚀 Quick Start

### 🌐 Production Access
The application is currently deployed and accessible at:
- **API Base URL:** https://ecom-backend.store/
- **Health Check:** https://ecom-backend.store/health/
- **Admin Panel:** https://ecom-backend.store/admin/ (secure login required)
- **API Documentation:** https://ecom-backend.store/api/v1/docs/

### 🐳 Docker Deployment (Recommended)

#### Development Environment
```bash
# Clone repository
git clone https://github.com/messkely/alx-project-nexus.git
cd alx-project-nexus

# Start development environment with hot reload
make docker-dev

# Access application
# API: http://localhost:8000
# Admin: http://localhost:8000/admin (admin/admin123)
# API Documentation: http://localhost:8000/api/v1/docs/
```

#### Production Environment
```bash
# Build and start production containers
make docker-prod

# Setup SSL certificates (optional)
sudo mkdir -p ssl/
# Copy your SSL certificate files to the ssl/ directory

# Application will be available at:
# HTTP: http://localhost
# HTTPS: https://localhost (with SSL certificates)
```

### 💻 Local Development Setup

#### Prerequisites
- Python 3.11+
- PostgreSQL 13+ (optional, uses SQLite by default)

#### 1. Setup Local Environment
```bash
# Clone repository
git clone https://github.com/messkely/alx-project-nexus.git
cd alx-project-nexus

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
make setup

# Configure local environment
cp .env.example .env
# Edit .env with your local configuration

# Setup database and run server
make migrate
make superuser
make run
```

#### 2. Access Local Development
```bash
# API Documentation: http://127.0.0.1:8000/
# Admin Panel: http://127.0.0.1:8000/admin/
# Health Check: http://127.0.0.1:8000/health/
```

### ☁️ AWS EC2 Ubuntu Deployment

#### Prerequisites  
- AWS EC2 instance running Ubuntu 20.04 or later
- SSH access to your EC2 instance
- Domain name pointed to your EC2 instance (optional for SSL)

#### 1. EC2 Instance Setup
```bash
# Connect to your EC2 instance
ssh -i your-key.pem ubuntu@your-ec2-ip

# Clone the project
git clone https://github.com/messkely/alx-project-nexus.git
cd alx-project-nexus

# Run automated deployment
chmod +x scripts/deploy-ec2.sh
sudo ./scripts/deploy-ec2.sh init
```

#### 2. Access Your Application
```bash
# API Base URL: http://your-ec2-ip/ or https://yourdomain.com/
# Admin Panel: http://your-ec2-ip/admin/ (admin/admin123)
# API Documentation: http://your-ec2-ip/api/v1/docs/
```

📚 **[Complete EC2 Deployment Guide](docs/EC2_DEPLOYMENT.md)**  
📚 **[Docker Deployment Guide](docs/DOCKER_DEPLOYMENT.md)**

---

## 🛠️ Makefile Commands

### 🐳 Docker Commands
```bash
# Development
make docker-dev          # Start development environment with hot reload
make docker-logs         # View container logs  
make docker-shell        # Access Django container shell
make docker-migrate      # Run database migrations in container
make docker-superuser    # Create superuser in container
make docker-test         # Run tests in container

# Production  
make docker-prod         # Start production environment
make docker-build        # Build Docker images

# Management
make docker-stop         # Stop all containers
make docker-clean        # Clean up Docker resources
make docker-restart      # Restart all containers
```

### 💻 Local Development Commands
```bash
# Environment Setup
make setup               # Create virtual environment and install dependencies
make install             # Install/update dependencies
make migrate             # Run database migrations
make superuser           # Create Django superuser
make run                 # Start development server

# Database Management
make backup-db           # Create database backup
make restore-db          # Restore database from backup
make seed-data           # Populate database with sample data

# Testing & Quality
make test                # Run test suite
make test-coverage       # Run tests with coverage report
make lint                # Run code linting
```

---

### Option 3: Local Development (For Development Only)

#### Prerequisites
- Python 3.11+
- PostgreSQL 15+
- Redis 7+

#### 1. Setup Environment
```bash
git clone https://github.com/messkely/alx-project-nexus.git
cd alx-project-nexus

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

# Install dependencies
pip install -r requirements.txt
```

#### 2. Configure Development Environment
Create a `.env` file for development:
```env
# Django Settings (Development Only)
DEBUG=True
SECRET_KEY=your-super-secret-key-change-in-production
ALLOWED_HOSTS=localhost,127.0.0.1

# Database Configuration
DATABASE_URL=postgresql://username:password@localhost:5432/ecommerce
DB_NAME=ecommerce
DB_USER=username
DB_PASSWORD=password
DB_HOST=localhost
DB_PORT=5432

# Redis Configuration
REDIS_URL=redis://localhost:6379/0
CACHE_URL=redis://localhost:6379/1

# CORS Settings (Development)
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
CSRF_TRUSTED_ORIGINS=http://localhost:8000,http://127.0.0.1:8000

# JWT Settings
ACCESS_TOKEN_LIFETIME=60  # minutes
REFRESH_TOKEN_LIFETIME=7  # days
```

#### 3. Database Setup
```bash
# Create database
createdb ecommerce

# Run migrations
python manage.py migrate

# Load sample data (optional)
python scripts/seed_database.py

# Create superuser
python manage.py createsuperuser
```

#### 4. Start Development Server
```bash
python manage.py runserver
```

---

## � Database Schema Overview

Our e-commerce platform uses a well-structured relational database design optimized for performance and scalability:

![Database Schema](drawSQL-image-export-2025-08-08.png)

### Core Tables:
- **users**: Customer and admin user management with authentication
- **categories**: Product categorization and organization  
- **products**: Complete product catalog with pricing and inventory
- **orders & order_items**: Order processing and line item tracking
- **cart_items**: Shopping cart functionality
- **shipping_address**: Customer shipping information management
- **reviews**: Product reviews and ratings (extended in our implementation)

> **Note**: The actual implementation includes additional features like enhanced address management, product reviews, and advanced indexing for better performance.

---

## �🔐 Authentication & Authorization

### JWT Authentication Flow

#### 1. User Registration
```http
POST /api/v1/auth/users/
Content-Type: application/json

{
  "email": "user@example.com",
  "username": "newuser",
  "password": "securepassword123",
  "first_name": "John",
  "last_name": "Doe"
}
```

#### 2. Obtain Access Token
```http
POST /api/v1/auth/jwt/create/
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "securepassword123"
}

Response:
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

#### 3. Using Access Token
```http
GET /api/v1/products/
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
```

#### 4. Refresh Token
```http
POST /api/v1/auth/jwt/refresh/
Content-Type: application/json

{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

### Permission Levels
- **Anonymous**: Read-only access to products and categories
- **Customer**: Cart management, orders, reviews
- **Staff**: Product and category management
- **Admin**: Full system access including user management

---

## 📚 API Documentation

### Interactive Documentation
- **Swagger UI**: `http://localhost:8000/api/v1/docs/`
- **ReDoc**: `http://localhost:8000/api/v1/redoc/`
- **OpenAPI Schema**: `http://localhost:8000/api/v1/schema/`

### Health Check
```http
GET /api/v1/health/
Response: {"status": "healthy", "service": "ecommerce-api"}
```

---

## 🌐 API Endpoints

### Authentication Endpoints
| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| `POST` | `/api/v1/auth/users/` | User registration | No |
| `POST` | `/api/v1/auth/jwt/create/` | Login (get tokens) | No |
| `POST` | `/api/v1/auth/jwt/refresh/` | Refresh access token | No |
| `POST` | `/api/v1/auth/jwt/verify/` | Verify token validity | No |
| `GET` | `/api/v1/auth/users/me/` | Get user profile | Yes |
| `PUT` | `/api/v1/auth/users/me/` | Update user profile | Yes |

### Product Management
| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| `GET` | `/api/v1/products/` | List products (with filtering) | No |
| `POST` | `/api/v1/products/` | Create product | Admin |
| `GET` | `/api/v1/products/{id}/` | Get product details | No |
| `PUT` | `/api/v1/products/{id}/` | Update product | Admin |
| `DELETE` | `/api/v1/products/{id}/` | Delete product | Admin |

### Category Management
| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| `GET` | `/api/v1/categories/` | List categories | No |
| `POST` | `/api/v1/categories/` | Create category | Admin |
| `GET` | `/api/v1/categories/{id}/` | Get category details | No |
| `PUT` | `/api/v1/categories/{id}/` | Update category | Admin |
| `DELETE` | `/api/v1/categories/{id}/` | Delete category | Admin |

### Shopping Cart
| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| `GET` | `/api/v1/cart/` | Get user's cart | Customer |
| `POST` | `/api/v1/cart/add/` | Add item to cart | Customer |
| `PUT` | `/api/v1/cart/update/{id}/` | Update cart item | Customer |
| `DELETE` | `/api/v1/cart/remove/{id}/` | Remove cart item | Customer |
| `DELETE` | `/api/v1/cart/clear/` | Clear entire cart | Customer |

### Order Management
| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| `GET` | `/api/v1/orders/` | List user orders | Customer |
| `POST` | `/api/v1/orders/` | Create order from cart | Customer |
| `GET` | `/api/v1/orders/{id}/` | Get order details | Customer |
| `PUT` | `/api/v1/orders/{id}/` | Update order status | Admin |

### Reviews & Ratings
| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| `GET` | `/api/v1/reviews/` | List reviews | No |
| `POST` | `/api/v1/reviews/` | Create review | Customer |
| `GET` | `/api/v1/reviews/{id}/` | Get review details | No |
| `PUT` | `/api/v1/reviews/{id}/` | Update review | Owner |
| `DELETE` | `/api/v1/reviews/{id}/` | Delete review | Owner/Admin |

---

## 🔍 Advanced API Features

### Product Filtering & Search
```http
# Filter by category
GET /api/v1/products/?category=electronics

# Filter by price range
GET /api/v1/products/?price_min=100&price_max=500

# Search by title or description
GET /api/v1/products/?search=iphone

# Combine filters
GET /api/v1/products/?category=electronics&price_max=1000&search=pro
```

### Sorting Options
```http
# Sort by price (ascending)
GET /api/v1/products/?ordering=price

# Sort by price (descending)
GET /api/v1/products/?ordering=-price

# Sort by creation date (newest first)
GET /api/v1/products/?ordering=-created_at

# Multiple sorting
GET /api/v1/products/?ordering=category,-price
```

### Pagination
```http
# Default pagination (20 items per page)
GET /api/v1/products/

# Custom page size
GET /api/v1/products/?page_size=10

# Specific page
GET /api/v1/products/?page=2

# Response includes navigation info
{
  "count": 150,
  "next": "http://localhost:8000/api/v1/products/?page=3",
  "previous": "http://localhost:8000/api/v1/products/?page=1",
  "results": [...]
}
```

### Response Examples

#### Product List Response
```json
{
  "count": 13,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "title": "iPhone 15 Pro",
      "slug": "iphone-15-pro",
      "description": "Latest iPhone with advanced camera",
      "price": "999.99",
      "category": 1,
      "category_name": "Electronics",
      "image": null,
      "stock_quantity": 50,
      "created_at": "2025-08-07T12:00:00Z",
      "updated_at": "2025-08-07T12:00:00Z",
      "average_rating": 4.5,
      "reviews_count": 15
    }
  ]
}
```

#### Cart Response
```json
{
  "id": 1,
  "user": 1,
  "items": [
    {
      "id": 1,
      "product": {
        "id": 1,
        "title": "iPhone 15 Pro",
        "price": "999.99"
      },
      "quantity": 2,
      "subtotal": "1999.98"
    }
  ],
  "total": "1999.98",
  "created_at": "2025-08-07T12:00:00Z",
  "updated_at": "2025-08-07T12:00:00Z"
}
```

---

## ⚡ Performance & Security

### Database Optimizations
- **Indexing**: Strategic indexes on frequently queried fields (price, category, created_at)
- **Query Optimization**: `select_related()` and `prefetch_related()` for efficient joins
- **Connection Pooling**: Optimized database connection management
- **Pagination**: Efficient pagination to handle large datasets

### Caching Strategy
- **Redis Caching**: Caches frequently accessed data (product lists, categories)
- **Database Query Caching**: Reduces database load for repeated queries
- **Static File Caching**: Nginx handles static file caching in production

### Security Features
- **JWT Token Security**: Short-lived access tokens with refresh token rotation
- **Rate Limiting**: API endpoint rate limiting to prevent abuse
- **CORS Protection**: Configured CORS policies for cross-origin requests
- **CSRF Protection**: CSRF tokens for state-changing operations
- **Input Validation**: Comprehensive request data validation
- **SQL Injection Prevention**: ORM-based queries prevent SQL injection
- **XSS Protection**: Output sanitization and CSP headers

### Production Optimizations
- **Gunicorn Workers**: Multi-worker WSGI server for handling concurrent requests
- **Nginx Reverse Proxy**: Load balancing and static file serving
- **Docker Multi-stage Builds**: Optimized container images
- **Health Checks**: Container and application health monitoring
- **Logging**: Structured logging for monitoring and debugging

---

## 🧪 Testing

### Comprehensive Test Suite
Our project includes 63+ unit tests covering all major functionality:

```bash
# Run all tests
make test                    # Docker
python manage.py test        # Local

# Run specific test modules
python manage.py test users.tests
python manage.py test catalog.tests
python manage.py test tests.test_auth_endpoints

# Run with coverage report
coverage run --source='.' manage.py test
coverage report
coverage html  # Generate HTML report
```

### Test Coverage Areas
- **Authentication**: JWT token handling, user permissions
- **Product Management**: CRUD operations, filtering, search
- **Cart Operations**: Add, update, remove items
- **Order Processing**: Order creation, status updates
- **Review System**: Create, update, delete reviews
- **API Security**: Permission checks, input validation
- **Database Models**: Model constraints and relationships

### Test Structure
```
tests/
├── test_auth_endpoints.py      # Authentication API tests
├── test_products_api.py        # Product API tests
├── test_categories_api.py      # Category API tests
└── {app}/tests/
    ├── test_models.py          # Model unit tests
    ├── test_views.py           # View tests
    └── test_serializers.py     # Serializer tests
```

### Security Testing
- Token validation and expiration
- Permission-based access control
- Input sanitization and validation
- Admin endpoint protection
- Rate limiting verification

---

## � Deployment

### Docker Production Deployment

## 🚀 Production Deployment

### Automated VPS Deployment (Recommended)

#### 1. Server Requirements
- **OS:** Ubuntu 20.04+ / CentOS 8+ / Debian 11+
- **RAM:** 2GB minimum (4GB recommended)
- **Storage:** 20GB SSD minimum
- **CPU:** 2 cores minimum
- **Domain:** Registered domain with DNS pointing to server IP

#### 2. Quick Deployment
```bash
# On your VPS server
git clone https://github.com/messkely/alx-project-nexus.git
cd alx-project-nexus

# Configure production environment
cp .env.prod.example .env.prod
# Edit .env.prod with your production values

# Run automated deployment
chmod +x deploy.sh
./deploy.sh init
```

#### 3. SSL Setup (Optional but Recommended)
```bash
# Automatic SSL with Let's Encrypt
./deploy.sh ssl yourdomain.com
```

### Production Environment Variables (.env.prod)
```env
# Production Django Settings
DEBUG=False
DJANGO_SECRET_KEY=your-super-secure-production-key-50-plus-characters
DJANGO_ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com

# Database Configuration (Use managed database in production)
DB_NAME=ecommerce_prod
DB_USER=ecommerce_prod_user  
DB_PASSWORD=super-secure-database-password
DB_HOST=localhost  # Or managed database host
DB_PORT=5432

# Redis Configuration (Use managed Redis in production)
REDIS_URL=redis://localhost:6379/0
CACHE_URL=redis://localhost:6379/1

# Security Settings (Required for Production)
SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True

# Email Configuration (For notifications)
EMAIL_HOST=smtp.yourdomain.com
EMAIL_PORT=587
EMAIL_HOST_USER=noreply@yourdomain.com
EMAIL_HOST_PASSWORD=your-email-password
DEFAULT_FROM_EMAIL=noreply@yourdomain.com
```

### Manual Server Setup (Alternative)

If you prefer manual setup instead of the automated deployment script:

#### 1. Install Dependencies
```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER

# Install Docker Compose
sudo apt install docker-compose-plugin

# Reboot or logout/login to apply group changes
```

#### 2. Application Deployment
```bash
# Clone repository
git clone https://github.com/messkely/alx-project-nexus.git
cd alx-project-nexus

# Configure environment
cp .env.prod.example .env.prod
nano .env.prod  # Edit with your settings

# Deploy application
docker compose -f docker-compose.production.yml up -d --build
```

#### 3. Post-Deployment Tasks
```bash
# Create database tables
docker compose -f docker-compose.production.yml exec web python manage.py migrate

# Collect static files  
docker compose -f docker-compose.production.yml exec web python manage.py collectstatic --noinput

# Create admin user
docker compose -f docker-compose.production.yml exec web python manage.py createsuperuser

# Seed database (optional)
docker compose -f docker-compose.production.yml exec web python seed_database.py
```

### Cloud Deployment Options

#### AWS Deployment
- **ECS/Fargate**: Container-based deployment
- **RDS**: Managed PostgreSQL database
- **ElastiCache**: Managed Redis service
- **CloudFront**: CDN for static files
- **ALB**: Application load balancer

#### Google Cloud Platform
- **Cloud Run**: Serverless container deployment
- **Cloud SQL**: Managed PostgreSQL
- **Cloud Memorystore**: Managed Redis
- **Cloud CDN**: Content delivery network

#### DigitalOcean
- **App Platform**: Platform-as-a-service deployment
- **Managed Databases**: PostgreSQL and Redis
- **Spaces CDN**: Object storage and CDN

---

## � Development Guidelines

### Code Quality Standards
- **PEP 8 Compliance**: Follow Python style guidelines
- **Type Hints**: Use type hints for function parameters and returns
- **Docstrings**: Document all classes and functions
- **Code Reviews**: All changes require peer review
- **Testing**: Maintain high test coverage (>90%)

### Git Workflow
```bash
# Feature development
git checkout -b feature/new-feature
git commit -m "feat: add new feature"
git push origin feature/new-feature

# Bug fixes
git checkout -b fix/bug-description
git commit -m "fix: resolve bug description"

# Documentation
git commit -m "docs: update API documentation"
```

### Commit Message Convention
- `feat:` New feature implementation
- `fix:` Bug fixes and patches
- `docs:` Documentation updates
- `style:` Code formatting and style changes
- `refactor:` Code restructuring without feature changes
- `test:` Adding or updating tests
- `perf:` Performance improvements
- `security:` Security-related changes

### Database Migrations
```bash
# Create migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Data migrations
python manage.py makemigrations --empty app_name
# Edit the migration file to add data operations
```

### Environment Management
- **Development**: Debug enabled, local database
- **Staging**: Production-like environment for testing
- **Production**: Optimized for performance and security

---

## 📊 Monitoring & Maintenance

### Health Monitoring
- **Health Check Endpoint**: `/api/v1/health/`
- **Database Connection**: Monitor database connectivity
- **Redis Connection**: Cache service monitoring
- **Disk Space**: Monitor storage usage
- **Memory Usage**: Track application memory consumption

### Logging
```python
# Application logs location
logs/
├── django.log          # General application logs
├── security.log        # Security-related events
├── error.log          # Error logs
└── access.log         # API access logs
```

### Backup Strategy
```bash
# Database backup
pg_dump ecommerce > backup_$(date +%Y%m%d_%H%M%S).sql

# Media files backup
tar -czf media_backup_$(date +%Y%m%d_%H%M%S).tar.gz media/

# Automated backup script
# Add to crontab for regular backups
0 2 * * * /path/to/backup_script.sh
```

### Performance Monitoring
- **Database Query Analysis**: Use Django Debug Toolbar in development
- **API Response Times**: Monitor endpoint performance
- **Cache Hit Rates**: Track Redis cache effectiveness
- **Error Rates**: Monitor application error frequency

---

## 🤝 Contributing

### Getting Started
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add/update tests
5. Ensure all tests pass
6. Update documentation
7. Submit a pull request

### Development Setup
```bash
# Fork and clone
git clone https://github.com/your-username/alx-project-nexus.git
cd alx-project-nexus

# Setup development environment
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install -r requirements-dev.txt  # Development dependencies

# Setup pre-commit hooks
pre-commit install

# Run tests
python manage.py test
```

### Pull Request Guidelines
- Clear description of changes
- Reference related issues
- Include tests for new features
- Update documentation as needed
- Ensure CI/CD checks pass

---

## 📞 Support & Contact

### Documentation Resources
- **Main Documentation**: [README.md](README.md)
- **Database Schema**: [docs/DATABASE_README.md](docs/DATABASE_README.md)  
- **Docker Setup**: [docs/DOCKER_README.md](docs/DOCKER_README.md)
- **Production Deployment**: [docs/PRODUCTION_DEPLOYMENT.md](docs/PRODUCTION_DEPLOYMENT.md)
- **Testing Guide**: [docs/TESTING_README.md](docs/TESTING_README.md)
- **Security Report**: [docs/SECURITY_AUDIT_REPORT.md](docs/SECURITY_AUDIT_REPORT.md)
- **API Testing**: [docs/api_testing_with_postman.md](docs/api_testing_with_postman.md)

### Getting Help
- **GitHub Issues**: Report bugs or request features
- **Discussions**: Community discussions and Q&A
- **Wiki**: Additional documentation and guides

### Project Maintainers
- **Lead Developer**: [@messkely](https://github.com/messkely)
- **Project Repository**: [alx-project-nexus](https://github.com/messkely/alx-project-nexus)

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

### MIT License Summary
- ✅ Commercial use permitted
- ✅ Modification permitted
- ✅ Distribution permitted
- ✅ Private use permitted
- ❌ Liability not provided
- ❌ Warranty not provided

---

## 🙏 Acknowledgments

- **Django Community**: For the excellent web framework
- **Django REST Framework**: For powerful API development tools
- **ALX Africa**: For providing the learning platform and project guidance
- **Open Source Contributors**: For the various packages and tools used

---

## 📈 Project Status

### Current Version: 1.2.0 (Production Ready)
**Last Updated:** August 8, 2025

- ✅ **Core Features**: Complete e-commerce functionality
- ✅ **Security**: Enterprise-grade security with CSP, SSL, JWT
- ✅ **Testing**: Comprehensive test coverage (63+ tests)
- ✅ **Production Deployment**: Automated Docker deployment with SSL
- ✅ **Documentation**: Complete project and deployment documentation
- ✅ **Performance**: Optimized with Redis caching and Nginx
- ✅ **Monitoring**: Health checks and logging
- ✅ **Backup**: Automated backup and recovery system

### Recent Updates (August 2025)
- ✅ **Production Infrastructure**: Complete automated deployment with `deploy.sh`
- ✅ **SSL Integration**: Let's Encrypt SSL certificate automation
- ✅ **Security Hardening**: Updated CSP headers, admin permissions
- ✅ **Docker Optimization**: Multi-stage builds and production containers
- ✅ **Documentation**: Comprehensive deployment and production guides

### Future Enhancements
- [ ] **Payment Integration**: Stripe/PayPal integration
- [ ] **Email Notifications**: Order confirmation emails  
- [ ] **Real-time Updates**: WebSocket notifications
- [ ] **Analytics Dashboard**: Admin analytics interface
- [ ] **Mobile API**: Mobile-optimized API endpoints
- [ ] **Internationalization**: Multi-language support

---

*Built with ❤️ by the ALX Africa Backend Development Program*