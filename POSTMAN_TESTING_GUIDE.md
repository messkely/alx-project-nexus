# 🧪 Complete EC2 API Testing Guide with Postman

## 🌐 Production Testing Environment

**Base URL:** `https://ecom-backend.store`  
**API Documentation:** https://ecom-backend.store/api/v1/docs/  
**Admin Panel:** https://ecom-backend.store/admin/  

---

## 🚀 Quick Setup

### Step 1: Create Postman Environment
1. Open Postman → Environments → Create Environment
2. Name: **"ALX E-Commerce Production"**
3. Add these variables:

| Variable | Initial Value | Description |
|----------|---------------|-------------|
| `base_url` | `https://ecom-backend.store` | Production server URL |
| `access_token` | *(empty)* | JWT access token (auto-filled) |
| `refresh_token` | *(empty)* | JWT refresh token (auto-filled) |
| `user_id` | *(empty)* | Current user ID (auto-filled) |
| `product_id` | *(empty)* | Test product ID (auto-filled) |
| `category_id` | *(empty)* | Test category ID (auto-filled) |
| `cart_item_id` | *(empty)* | Cart item ID (auto-filled) |
| `order_id` | *(empty)* | Order ID (auto-filled) |

### Step 2: Import Collection
Create a new collection: **"ALX E-Commerce API"**

---

## 🔐 1. Authentication & User Management

### 1.1 Health Check ✅
```
GET {{base_url}}/health/
```
**Expected Response:** `200 OK`
```json
{
  "status": "healthy",
  "timestamp": "2025-08-09T...",
  "database": "connected",
  "cache": "connected"
}
```

### 1.2 User Registration 👤
```
POST {{base_url}}/api/v1/users/register/
Content-Type: application/json

{
  "email": "testuser@example.com",
  "username": "testuser123",
  "first_name": "Test",
  "last_name": "User",
  "password": "SecurePass123!",
  "password_confirm": "SecurePass123!"
}
```

**Expected Response:** `201 Created`
```json
{
  "user": {
    "id": 1,
    "email": "testuser@example.com",
    "username": "testuser123",
    "first_name": "Test",
    "last_name": "User",
    "date_joined": "2025-08-09T..."
  },
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

**Post-Response Script:** (Add to Tests tab)
```javascript
if (pm.response.code === 201) {
    const response = pm.response.json();
    pm.environment.set("access_token", response.access);
    pm.environment.set("refresh_token", response.refresh);
    pm.environment.set("user_id", response.user.id);
}
```

### 1.3 User Login 🔑
```
POST {{base_url}}/api/v1/auth/login/
Content-Type: application/json

{
  "email": "testuser@example.com",
  "password": "SecurePass123!"
}
```

**Post-Response Script:**
```javascript
if (pm.response.code === 200) {
    const response = pm.response.json();
    pm.environment.set("access_token", response.access);
    pm.environment.set("refresh_token", response.refresh);
}
```

### 1.4 Get User Profile 👥
```
GET {{base_url}}/api/v1/users/profile/
Authorization: Bearer {{access_token}}
```

### 1.5 Update User Profile 📝
```
PUT {{base_url}}/api/v1/users/profile/
Authorization: Bearer {{access_token}}
Content-Type: application/json

{
  "first_name": "Updated Test",
  "last_name": "Updated User"
}
```

---

## 🛍️ 2. Product Catalog

### 2.1 List Categories 📂
```
GET {{base_url}}/api/v1/categories/
```

**Post-Response Script:**
```javascript
if (pm.response.code === 200) {
    const response = pm.response.json();
    if (response.results && response.results.length > 0) {
        pm.environment.set("category_id", response.results[0].id);
    }
}
```

### 2.2 Create Category (Admin Only) 🆕
```
POST {{base_url}}/api/v1/categories/
Authorization: Bearer {{access_token}}
Content-Type: application/json

{
  "name": "Electronics",
  "description": "Electronic products and gadgets"
}
```

### 2.3 List Products 📦
```
GET {{base_url}}/api/v1/products/
```

**Post-Response Script:**
```javascript
if (pm.response.code === 200) {
    const response = pm.response.json();
    if (response.results && response.results.length > 0) {
        pm.environment.set("product_id", response.results[0].id);
    }
}
```

### 2.4 Create Product (Admin Only) 🛒
```
POST {{base_url}}/api/v1/products/
Authorization: Bearer {{access_token}}
Content-Type: application/json

{
  "name": "iPhone 15 Pro",
  "description": "Latest iPhone with advanced features",
  "price": "999.99",
  "stock_quantity": 50,
  "category": {{category_id}},
  "brand": "Apple",
  "is_featured": true,
  "is_available": true
}
```

### 2.5 Get Product Details 🔍
```
GET {{base_url}}/api/v1/products/{{product_id}}/
```

### 2.6 Update Product (Admin Only) ✏️
```
PUT {{base_url}}/api/v1/products/{{product_id}}/
Authorization: Bearer {{access_token}}
Content-Type: application/json

{
  "name": "iPhone 15 Pro - Updated",
  "price": "1099.99",
  "stock_quantity": 45
}
```

### 2.7 Filter Products 🔎
```
GET {{base_url}}/api/v1/products/?category={{category_id}}&min_price=100&max_price=2000&ordering=-created_at
```

### 2.8 Search Products 🔍
```
GET {{base_url}}/api/v1/products/?search=iPhone
```

---

## 🛒 3. Shopping Cart

### 3.1 Get Cart Items 📋
```
GET {{base_url}}/api/v1/cart/
Authorization: Bearer {{access_token}}
```

### 3.2 Add Item to Cart ➕
```
POST {{base_url}}/api/v1/cart/
Authorization: Bearer {{access_token}}
Content-Type: application/json

{
  "product": {{product_id}},
  "quantity": 2
}
```

**Post-Response Script:**
```javascript
if (pm.response.code === 201) {
    const response = pm.response.json();
    pm.environment.set("cart_item_id", response.id);
}
```

### 3.3 Update Cart Item 📝
```
PUT {{base_url}}/api/v1/cart/{{cart_item_id}}/
Authorization: Bearer {{access_token}}
Content-Type: application/json

{
  "quantity": 3
}
```

### 3.4 Remove Item from Cart ❌
```
DELETE {{base_url}}/api/v1/cart/{{cart_item_id}}/
Authorization: Bearer {{access_token}}
```

### 3.5 Clear Cart 🗑️
```
DELETE {{base_url}}/api/v1/cart/clear/
Authorization: Bearer {{access_token}}
```

---

## 📦 4. Order Management

### 4.1 Create Order 🛍️
```
POST {{base_url}}/api/v1/orders/
Authorization: Bearer {{access_token}}
Content-Type: application/json

{
  "shipping_address": {
    "street": "123 Main St",
    "city": "New York",
    "state": "NY",
    "postal_code": "10001",
    "country": "US"
  },
  "billing_address": {
    "street": "123 Main St", 
    "city": "New York",
    "state": "NY",
    "postal_code": "10001",
    "country": "US"
  },
  "payment_method": "credit_card"
}
```

**Post-Response Script:**
```javascript
if (pm.response.code === 201) {
    const response = pm.response.json();
    pm.environment.set("order_id", response.id);
}
```

### 4.2 List User Orders 📋
```
GET {{base_url}}/api/v1/orders/
Authorization: Bearer {{access_token}}
```

### 4.3 Get Order Details 🔍
```
GET {{base_url}}/api/v1/orders/{{order_id}}/
Authorization: Bearer {{access_token}}
```

### 4.4 Update Order Status (Admin Only) 📊
```
PATCH {{base_url}}/api/v1/orders/{{order_id}}/
Authorization: Bearer {{access_token}}
Content-Type: application/json

{
  "status": "shipped"
}
```

---

## ⭐ 5. Review System

### 5.1 Create Product Review 📝
```
POST {{base_url}}/api/v1/reviews/
Authorization: Bearer {{access_token}}
Content-Type: application/json

{
  "product": {{product_id}},
  "rating": 5,
  "comment": "Excellent product! Highly recommended."
}
```

### 5.2 List Product Reviews 📋
```
GET {{base_url}}/api/v1/reviews/?product={{product_id}}
```

### 5.3 Update Review ✏️
```
PUT {{base_url}}/api/v1/reviews/{{review_id}}/
Authorization: Bearer {{access_token}}
Content-Type: application/json

{
  "rating": 4,
  "comment": "Good product, but could be better."
}
```

### 5.4 Delete Review ❌
```
DELETE {{base_url}}/api/v1/reviews/{{review_id}}/
Authorization: Bearer {{access_token}}
```

---

## 🔒 6. Admin Endpoints

### 6.1 Admin Dashboard 👑
```
GET {{base_url}}/api/v1/admin/dashboard/
Authorization: Bearer {{access_token}}
```

### 6.2 List All Orders (Admin) 📊
```
GET {{base_url}}/api/v1/admin/orders/
Authorization: Bearer {{access_token}}
```

### 6.3 User Management (Admin) 👥
```
GET {{base_url}}/api/v1/admin/users/
Authorization: Bearer {{access_token}}
```

---

## 🧪 7. Testing Scenarios

### Scenario 1: Complete User Journey 🛒
1. **Register** new user
2. **Login** to get tokens
3. **Browse** products and categories
4. **Add** products to cart
5. **Create** order
6. **Leave** product review

### Scenario 2: Admin Operations 👑
1. **Login** as admin
2. **Create** new categories
3. **Add** products
4. **Manage** orders
5. **Update** product inventory

### Scenario 3: Error Testing ❌
1. **Invalid** credentials
2. **Unauthorized** access
3. **Missing** required fields
4. **Invalid** data formats

---

## 📊 Expected Response Codes

| Code | Meaning | When to Expect |
|------|---------|----------------|
| **200** | OK | Successful GET, PUT requests |
| **201** | Created | Successful POST requests |
| **204** | No Content | Successful DELETE requests |
| **400** | Bad Request | Invalid data format |
| **401** | Unauthorized | Missing/invalid authentication |
| **403** | Forbidden | Insufficient permissions |
| **404** | Not Found | Resource doesn't exist |
| **500** | Server Error | Internal server issues |

---

## 🔧 Common Headers

**For All Requests:**
```
Content-Type: application/json
Accept: application/json
```

**For Authenticated Requests:**
```
Authorization: Bearer {{access_token}}
```

---

## 🐛 Troubleshooting

### CORS Issues
If you get CORS errors, the API now has CORS properly configured for production.

### Authentication Issues
- Ensure you're using **email** for login, not username
- Check that tokens are properly set in environment variables
- Verify token hasn't expired (default: 1 hour)

### SSL Certificate Issues
- All requests must use HTTPS (`https://ecom-backend.store`)
- Certificate is valid and auto-renewing

---

## 📝 Test Results Documentation

Create a test report documenting:
1. ✅ **Successful Endpoints** - All working endpoints
2. ❌ **Failed Tests** - Any issues encountered  
3. 📊 **Performance** - Response times
4. 🔒 **Security** - Authentication/authorization working
5. 📈 **API Coverage** - Percentage of endpoints tested

---

## 🎯 Quick Test Checklist

- [ ] Health check endpoint
- [ ] User registration and login
- [ ] JWT token generation and usage
- [ ] Product CRUD operations
- [ ] Category management
- [ ] Shopping cart functionality
- [ ] Order creation and management
- [ ] Review system
- [ ] Admin permissions
- [ ] Error handling
- [ ] HTTPS security
- [ ] CORS functionality

**Happy Testing! 🚀**

---

*For additional help, check the live API documentation at: https://ecom-backend.store/api/v1/docs/*
