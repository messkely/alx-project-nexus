# ALX E-Commerce Backend - Final Project
**ALX ProDev Backend Development Program**  
**Student:** [Your Name]  
**Date:** August 7, 2025

---

## 🔗 Project Links

**GitHub Repository:**  
https://github.com/messkely/alx-project-nexus

**ERD Diagram:**  
https://github.com/messkely/alx-project-nexus/blob/main/assets/drawSQL-image-export-2025-08-01.png

---

## 📊 Entity Relationship Diagram

![Database ERD](https://github.com/messkely/alx-project-nexus/blob/main/assets/drawSQL-image-export-2025-08-01.png)

The ERD shows all data models and relationships including:
- Users with role-based permissions
- Product catalog with categories
- Shopping cart and order management
- Review system with ratings
- JWT token blacklisting for security

---

## 🎯 Project Overview

Production-ready e-commerce backend API demonstrating:
- **Django 5.2.1** with REST Framework
- **PostgreSQL 15** database design
- **JWT Authentication** with blacklisting
- **Docker containerization** for deployment
- **78+ comprehensive tests**

---

## 🏗️ Architecture

**Django Apps:**
- `users/` - Authentication & user management
- `catalog/` - Product catalog with search
- `cart/` - Shopping cart functionality  
- `orders/` - Order lifecycle management
- `reviews/` - Product reviews & ratings

**Infrastructure:**
- PostgreSQL database
- Redis for caching
- Nginx reverse proxy
- Docker Compose orchestration

---

## 🚀 Setup Instructions

1. **Clone & Setup:**
   ```
   git clone https://github.com/messkely/alx-project-nexus.git
   cd alx-project-nexus
   ```

2. **Docker Development:**
   ```
   docker compose -f docker-compose.yml -f docker-compose.dev.yml up --build
   ```

3. **Database & Seed Data:**
   ```
   python manage.py migrate
   python seed_database.py
   ```

4. **Access API:** http://localhost:8000/api/

---

## ✅ Key Features

**Authentication & Security:**
- JWT tokens with refresh mechanism
- Role-based permissions (Admin/Staff/Customer)
- Token blacklisting for secure logout

**API Functionality:**
- RESTful endpoints for all resources
- Advanced search and filtering
- Pagination for large datasets
- Comprehensive error handling

**Database Design:**
- Normalized schema with proper relationships
- Optimized indexes for performance
- Data integrity constraints

---

## 🧪 Testing

**Test Coverage:**
- Unit tests for models and views
- API endpoint integration tests
- Authentication flow testing
- **78+ total test cases**

**Run Tests:**
```
python manage.py test
```

---

## 📚 Documentation

- **[Main README](https://github.com/messkely/alx-project-nexus/blob/main/README.md)** - Setup and usage
- **[Database Design](https://github.com/messkely/alx-project-nexus/blob/main/DATABASE_DIAGRAM.md)** - ERD details
- **[Testing Guide](https://github.com/messkely/alx-project-nexus/blob/main/TESTING_README.md)** - Test strategy
- **[API Documentation](https://github.com/messkely/alx-project-nexus/blob/main/api_testing_with_postman.md)** - Postman collection

---

## 🔧 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/auth/register/` | POST | User registration |
| `/api/auth/login/` | POST | Authentication |
| `/api/products/` | GET/POST | Product catalog |
| `/api/cart/` | GET/POST/PUT/DELETE | Cart operations |
| `/api/orders/` | GET/POST | Order management |
| `/api/reviews/` | GET/POST | Product reviews |

---

## 📊 Project Statistics

- **5,000+** lines of code
- **12+** database tables
- **25+** API endpoints
- **78+** test cases
- **4** Docker services
- **10+** documentation files

---

## 🎓 Learning Outcomes

This project demonstrates mastery of:
- Advanced Django & DRF development
- PostgreSQL database design
- JWT authentication & security
- Docker containerization
- RESTful API principles
- Test-driven development
- Production deployment

---

## 🏆 Deliverables

✅ **GitHub Repository:** Complete codebase with documentation  
✅ **ERD Diagram:** Database schema visualization  
✅ **Google Doc:** This project presentation  
✅ **Production Code:** Fully functional backend API  
✅ **Test Suite:** Comprehensive testing coverage  
✅ **Documentation:** Setup guides and technical specs

---

**Project Status:** Complete & Production Ready ✅  
**ALX ProDev Backend Program - Final Submission**
