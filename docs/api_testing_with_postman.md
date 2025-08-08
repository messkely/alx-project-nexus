# 🧪 Comprehensive API Testing Guide with Postman

This guide provides step-by-step instructions for testing all API endpoints, permissions, and routes using Postman.

## 📋 Table of Contents
1. [Environment Setup](#environment-setup)
2. [Authentication Testing](#authentication-testing)
3. [User Management Testing](#user-management-testing)
4. [Catalog Testing (Products & Categories)](#catalog-testing)
5. [Cart Management Testing](#cart-management-testing)
6. [Order Management Testing](#order-management-testing)
7. [Review System Testing](#review-system-testing)
8. [Permission Testing](#permission-testing)
9. [Admin Functionality Testing](#admin-functionality-testing)

---

## 🔧 Environment Setup

### Step 1: Create Postman Environment
1. Open Postman and click on "Environments" in the left sidebar
2. Click "Create Environment"
3. Name it "E-Commerce API"
4. Add the following variables:

| Variable Name | Initial Value | Current Value |
|---------------|---------------|---------------|
| `base_url` | `http://127.0.0.1:8001` | `http://127.0.0.1:8001` |
| `access_token` | | (will be set automatically) |
| `refresh_token` | | (will be set automatically) |
| `admin_access_token` | | (will be set automatically) |
| `user_id` | | (will be set automatically) |
| `product_id` | | (will be set automatically) |
| `category_id` | | (will be set automatically) |
| `cart_item_id` | | (will be set automatically) |
| `order_id` | | (will be set automatically) |
| `review_id` | | (will be set automatically) |

### Step 2: Create Collection
1. Create a new Collection named "E-Commerce API Tests"
2. Set the collection authorization to "No Auth" (we'll set it per request)

---

## 🔐 Authentication Testing

⚠️ **System Update (August 2025)**: This e-commerce API uses **email-based authentication** with a custom JWT implementation.

### Key Authentication Facts:
- **Login Field**: Use `email`, not `username`
- **Access Token**: Short-lived (15 minutes), used in Authorization header
- **Refresh Token**: Long-lived (7 days), used in request body for logout/refresh
- **Logout Response**: Returns HTTP 205 (Reset Content) - this is correct behavior
- **Token Blacklisting**: Fully implemented and working
- **Available Test Accounts**:
  - Admin: `admin@ecommerce.com` / `adminpassword123`
  - User: `janedoe@example.com` / (use registration to create)

### Test 1: User Registration
**Endpoint**: `POST {{base_url}}/api/v1/auth/register/`
**Permission**: Public (No authentication required)

**Request Body**:
```json
{
  "username": "testuser123",
  "email": "testuser@example.com",
  "password": "SecurePassword123!",
  "password_confirm": "SecurePassword123!",
  "first_name": "Test",
  "last_name": "User"
}
```

**Expected Behavior**:
- ✅ **Success (201)**: User created successfully with JWT tokens
- ❌ **Error (400)**: Validation errors (email already exists, weak password, password mismatch, etc.)

**Tests Tab Script**:
```javascript
pm.test("User registration successful", function () {
    pm.expect(pm.response.code).to.be.oneOf([201, 400]);
    
    if (pm.response.code === 201) {
        var jsonData = pm.response.json();
        pm.environment.set("user_id", jsonData.user.id);
        pm.environment.set("access_token", jsonData.access);
        pm.environment.set("refresh_token", jsonData.refresh);
        console.log("User registered successfully with ID:", jsonData.user.id);
        console.log("Tokens automatically set for immediate testing");
    } else {
        console.log("Registration failed:", pm.response.text());
    }
});
```

### Test 2: User Login
**Endpoint**: `POST {{base_url}}/api/v1/auth/login/`
**Permission**: Public

⚠️ **Important**: This system uses email-based authentication, not username.

**Request Body**:
```json
{
  "email": "admin@ecommerce.com",
  "password": "adminpassword123"
}
```

**Alternative Test User Credentials**:
- Email: `testuser@example.com` (regular user)
- Email: `janedoe@example.com` (regular user)
- Password: Use the password you set during registration

**Expected Behavior**:
- ✅ **Success (200)**: Returns access and refresh tokens
- ❌ **Error (400)**: Invalid email or password
- ❌ **Error (403)**: Rate limit exceeded (wait 5 minutes)

**Tests Tab Script**:
```javascript
pm.test("Login successful", function () {
    pm.expect(pm.response.code).to.equal(200);
    
    if (pm.response.code === 200) {
        var jsonData = pm.response.json();
        pm.environment.set("access_token", jsonData.access);
        pm.environment.set("refresh_token", jsonData.refresh);
        
        console.log("Access token set:", jsonData.access.substring(0, 20) + "...");
        console.log("Refresh token set:", jsonData.refresh.substring(0, 20) + "...");
        
        // Verify token types for logout testing
        console.log("✅ Ready for logout test - tokens properly separated");
    } else {
        console.log("Login failed:", pm.response.text());
    }
});
```

### Test 3: Token Refresh
**Endpoint**: `POST {{base_url}}/api/v1/auth/token/refresh/`
**Permission**: Public

**Request Body**:
```json
{
  "refresh": "{{refresh_token}}"
}
```

**Expected Behavior**:
- ✅ **Success (200)**: Returns new access token
- ❌ **Error (401)**: Invalid or expired refresh token

### Test 4: Logout
**Endpoint**: `POST {{base_url}}/api/v1/auth/logout/`
**Permission**: Authenticated users only
**Authorization**: Bearer Token `{{access_token}}`

⚠️ **Critical Setup Requirements:**
- **Authorization Header**: Must contain ACCESS token (Bearer {{access_token}})
- **Request Body**: Must contain REFRESH token (refresh_token field)
- **Common Error**: "Token has wrong type" occurs when tokens are swapped

**Request Body**:
```json
{
  "refresh_token": "{{refresh_token}}"
}
```

**Expected Behavior**:
- ✅ **Success (205)**: User logged out successfully, refresh token blacklisted
- ❌ **Error (401)**: Authentication credentials were not provided (missing/invalid access token in header)
- ❌ **Error (400)**: Invalid or missing refresh_token in request body
- ❌ **Error (400)**: "Token has wrong type" (access/refresh tokens swapped)

**Troubleshooting "Token has wrong type" Error:**
1. Ensure Authorization header uses ACCESS token: `Bearer eyJ...access_token...`
2. Ensure request body uses REFRESH token: `"refresh_token": "eyJ...refresh_token..."`
3. Get fresh tokens if expired (tokens expire after 15 minutes)

**Tests Tab Script**:
```javascript
pm.test("Logout successful", function () {
    pm.expect(pm.response.code).to.equal(205);
    
    if (pm.response.code === 205) {
        // Clear tokens from environment after successful logout
        pm.environment.unset("access_token");
        pm.environment.unset("refresh_token");
        console.log("User logged out successfully, tokens cleared");
    } else {
        console.log("Logout failed:", pm.response.text());
    }
});
```

---

## � Authentication Troubleshooting Guide

### Common Issues and Solutions

#### Issue 1: "Authentication credentials were not provided" (401)
**Symptoms**: 401 error on protected endpoints
**Causes & Solutions**:
- ❌ **No Authorization header**: Add `Authorization: Bearer {{access_token}}`
- ❌ **Wrong header format**: Use `Bearer` (not `Token` or `JWT`)
- ❌ **Token in wrong place**: Access token goes in header, refresh token in body (for logout)

#### Issue 2: "Token has wrong type" Error (400)
**Symptoms**: `{"detail":"Given token not valid for any token type","code":"token_not_valid","messages":[{"token_class":"AccessToken","token_type":"access","message":"Token has wrong type"}]}`

**Root Cause**: Mixing up access and refresh tokens

**Solution**:
```
✅ CORRECT Setup:
Authorization Header: Bearer {{access_token}}
Request Body (logout): {"refresh_token": "{{refresh_token}}"}

❌ WRONG Setup:
Authorization Header: Bearer {{refresh_token}}  ← This causes the error
Request Body: {"refresh_token": "{{access_token}}"}
```

#### Issue 3: "Invalid email or password" (400)
**Symptoms**: Login fails with valid credentials
**Causes & Solutions**:
- ❌ **Wrong field name**: Use `"email"`, not `"username"`
- ❌ **User doesn't exist**: Check database or create user first
- ❌ **Password mismatch**: Reset password or use correct password

#### Issue 4: Rate Limiting (403)
**Symptoms**: "Rate limit exceeded. Please try again later."
**Solution**: Wait 5 minutes between failed login attempts

#### Issue 5: Expired Tokens (401)
**Symptoms**: Previously working tokens now return 401
**Solution**: 
1. Get fresh tokens via login
2. Access tokens expire in 15 minutes
3. Use refresh token to get new access token

### 🔧 Quick Fixes

#### Get Fresh Tokens for Testing
```bash
# Quick login test
POST {{base_url}}/api/v1/auth/login/
{
  "email": "admin@ecommerce.com",
  "password": "adminpassword123"
}
```

#### Verify Token Setup
```javascript
// Add to Tests tab to debug tokens
console.log("Access token:", pm.environment.get("access_token").substring(0, 20));
console.log("Refresh token:", pm.environment.get("refresh_token").substring(0, 20));
```

#### Test Token Validity
```bash
# Test if access token works
GET {{base_url}}/api/v1/auth/profile/
Authorization: Bearer {{access_token}}
```

---

## �👤 User Management Testing

### Test 5: Get User Profile
**Endpoint**: `GET {{base_url}}/api/v1/auth/profile/`
**Permission**: Authenticated users only
**Authorization**: Bearer Token `{{access_token}}`

**Expected Behavior**:
- ✅ **Success (200)**: Returns user profile data
- ❌ **Error (401)**: No authentication provided

### Test 6: Update User Profile
**Endpoint**: `PUT {{base_url}}/api/v1/auth/profile/update/`
**Permission**: Authenticated users only
**Authorization**: Bearer Token `{{access_token}}`

**Request Body**:
```json
{
  "first_name": "Updated",
  "last_name": "Name",
  "email": "updated@example.com"
}
```

**Expected Behavior**:
- ✅ **Success (200)**: Profile updated successfully
- ❌ **Error (401)**: No authentication provided

### Test 7: Change Password
**Endpoint**: `POST {{base_url}}/api/v1/auth/password/change/`
**Permission**: Authenticated users only
**Authorization**: Bearer Token `{{access_token}}`

**Request Body**:
```json
{
  "old_password": "SecurePassword123!",
  "new_password": "NewSecurePassword123!",
  "new_password_confirm": "NewSecurePassword123!"
}
```

**Expected Behavior**:
- ✅ **Success (200)**: Password changed successfully
- ❌ **Error (400)**: Invalid old password or password mismatch

### Test 8: Add User Address
**Endpoint**: `POST {{base_url}}/api/v1/auth/addresses/`
**Permission**: Authenticated users only
**Authorization**: Bearer Token `{{access_token}}`

**Request Body**:
```json
{
  "street": "123 Main Street",
  "city": "Test City",
  "state": "TS",
  "postal_code": "12345",
  "country": "Test Country",
  "is_default": true
}
```

**Expected Behavior**:
- ✅ **Success (201)**: Address created successfully
- ❌ **Error (401)**: No authentication provided

---

## 📦 Catalog Testing

### Test 9: List All Products (Public)
**Endpoint**: `GET {{base_url}}/api/v1/products/`
**Permission**: Public (No authentication required)

**Expected Behavior**:
- ✅ **Success (200)**: Returns paginated list of products
- Includes product details: id, title, price, category, etc.

**Tests Tab Script**:
```javascript
pm.test("Products list retrieved", function () {
    pm.expect(pm.response.code).to.equal(200);
    
    var jsonData = pm.response.json();
    if (jsonData.results && jsonData.results.length > 0) {
        pm.environment.set("product_id", jsonData.results[0].id);
        console.log("Product ID set:", jsonData.results[0].id);
    }
});
```

### Test 10: Get Product by ID
**Endpoint**: `GET {{base_url}}/api/v1/products/{{product_id}}/`
**Permission**: Public

**Expected Behavior**:
- ✅ **Success (200)**: Returns detailed product information
- ❌ **Error (404)**: Product not found

### Test 11: Get Product by Slug
**Endpoint**: `GET {{base_url}}/api/v1/products/iphone-15-pro/`
**Permission**: Public

**Expected Behavior**:
- ✅ **Success (200)**: Returns product information by slug
- ❌ **Error (404)**: Product not found

### Test 12: Search Products
**Endpoint**: `GET {{base_url}}/api/v1/products/search/?q=iPhone`
**Permission**: Public

**Query Parameters**: `q=iPhone` (or any search term)

**Search Capabilities**:
- **Product Title**: Searches in product names (case-insensitive)
- **Product Description**: Searches in product descriptions  
- **Category Name**: Searches in category names

**Expected Behavior**:
- ✅ **Success (200)**: Returns paginated products matching search query
- ✅ **No Results (200)**: Returns empty results array when no matches found
- ✅ **No Query (200)**: Returns empty results when no 'q' parameter provided

**Example Search Terms**:
- `q=iPhone` → Finds "iPhone 15 Pro"
- `q=Sony` → Finds "Sony Headphones"  
- `q=Electronics` → Finds all products in Electronics category
- `q=Pro` → Finds products with "Pro" in title or description

**Response Format**:
```json
{
  "count": 1,
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
      "stock_quantity": 0,
      "created_at": "2025-08-05T11:09:25.452873Z",
      "updated_at": "2025-08-05T11:09:25.452908Z",
      "average_rating": 4.5,
      "reviews_count": 2
    }
  ]
}
```

### Test 13: Get Featured Products
**Endpoint**: `GET {{base_url}}/api/v1/products/featured/`
**Permission**: Public

**Expected Behavior**:
- ✅ **Success (200)**: Returns list of featured products

### Test 14: Get Latest Products
**Endpoint**: `GET {{base_url}}/api/v1/products/latest/`
**Permission**: Public

**Expected Behavior**:
- ✅ **Success (200)**: Returns recently added products

### Test 15: List Categories
**Endpoint**: `GET {{base_url}}/api/v1/categories/`
**Permission**: Public

**Expected Behavior**:
- ✅ **Success (200)**: Returns list of all categories

**Tests Tab Script**:
```javascript
pm.test("Categories list retrieved", function () {
    pm.expect(pm.response.code).to.equal(200);
    
    var jsonData = pm.response.json();
    if (jsonData.results && jsonData.results.length > 0) {
        pm.environment.set("category_id", jsonData.results[0].id);
        console.log("Category ID set:", jsonData.results[0].id);
    }
});
```

### Test 16: Get Category by ID
**Endpoint**: `GET {{base_url}}/api/v1/categories/{{category_id}}/`
**Permission**: Public

**Expected Behavior**:
- ✅ **Success (200)**: Returns category details
- ❌ **Error (404)**: Category not found

### Test 17: Get Products by Category
**Endpoint**: `GET {{base_url}}/api/v1/categories/{{category_id}}/products/`
**Permission**: Public

**Expected Behavior**:
- ✅ **Success (200)**: Returns products in specified category
- ❌ **Error (404)**: Category not found

---

## 🛒 Cart Management Testing

### Test 18: View Empty Cart
**Endpoint**: `GET {{base_url}}/api/v1/cart/`
**Permission**: Authenticated users only
**Authorization**: Bearer Token `{{access_token}}`

**Expected Behavior**:
- ✅ **Success (200)**: Returns empty cart or existing cart items
- ❌ **Error (401)**: No authentication provided

### Test 19: Add Item to Cart
**Endpoint**: `POST {{base_url}}/api/v1/cart/add/`
**Permission**: Authenticated users only
**Authorization**: Bearer Token `{{access_token}}`

**Request Body**:
```json
{
  "product_id": {{product_id}},
  "quantity": 2
}
```

**Expected Behavior**:
- ✅ **Success (201)**: Item added to cart successfully
- ❌ **Error (400)**: Invalid product ID or insufficient stock

**Tests Tab Script**:
```javascript
pm.test("Item added to cart", function () {
    pm.expect(pm.response.code).to.be.oneOf([200, 201]);
    
    if (pm.response.code === 201 || pm.response.code === 200) {
        var jsonData = pm.response.json();
        if (jsonData.id) {
            pm.environment.set("cart_item_id", jsonData.id);
            console.log("Cart item ID set:", jsonData.id);
        }
    }
});
```

### Test 20: Update Cart Item Quantity
**Endpoint**: `PUT {{base_url}}/api/v1/cart/update/{{cart_item_id}}/`
**Permission**: Authenticated users only (item owner)
**Authorization**: Bearer Token `{{access_token}}`

**Request Body**:
```json
{
  "quantity": 3
}
```

**Expected Behavior**:
- ✅ **Success (200)**: Cart item quantity updated
- ❌ **Error (404)**: Cart item not found
- ❌ **Error (403)**: Not the owner of the cart item

### Test 21: Increase Item Quantity
**Endpoint**: `POST {{base_url}}/api/v1/cart/increase/{{cart_item_id}}/`
**Permission**: Authenticated users only (item owner)
**Authorization**: Bearer Token `{{access_token}}`

**Expected Behavior**:
- ✅ **Success (200)**: Cart item quantity increased by 1

### Test 22: Decrease Item Quantity
**Endpoint**: `POST {{base_url}}/api/v1/cart/decrease/{{cart_item_id}}/`
**Permission**: Authenticated users only (item owner)
**Authorization**: Bearer Token `{{access_token}}`

**Expected Behavior**:
- ✅ **Success (200)**: Cart item quantity decreased by 1

### Test 23: Get Cart Item Count
**Endpoint**: `GET {{base_url}}/api/v1/cart/count/`
**Permission**: Authenticated users only
**Authorization**: Bearer Token `{{access_token}}`

**Expected Behavior**:
- ✅ **Success (200)**: Returns total number of items in cart

### Test 24: Get Cart Total
**Endpoint**: `GET {{base_url}}/api/v1/cart/total/`
**Permission**: Authenticated users only
**Authorization**: Bearer Token `{{access_token}}`

**Expected Behavior**:
- ✅ **Success (200)**: Returns cart total amount and item count

### Test 25: Remove Item from Cart
**Endpoint**: `DELETE {{base_url}}/api/v1/cart/remove/{{cart_item_id}}/`
**Permission**: Authenticated users only (item owner)
**Authorization**: Bearer Token `{{access_token}}`

**Expected Behavior**:
- ✅ **Success (204)**: Item removed from cart
- ❌ **Error (404)**: Cart item not found

### Test 26: Clear Cart
**Endpoint**: `DELETE {{base_url}}/api/v1/cart/clear/`
**Permission**: Authenticated users only
**Authorization**: Bearer Token `{{access_token}}`

**Expected Behavior**:
- ✅ **Success (200)**: All items removed from cart

---

## 📝 Order Management Testing

### Test 27: Create Order from Cart
**Endpoint**: `POST {{base_url}}/api/v1/orders/create/`
**Permission**: Authenticated users only
**Authorization**: Bearer Token `{{access_token}}`

**Request Body**:
```json
{
  "items": [
    {
      "product_id": {{product_id}},
      "quantity": 1,
      "price": "999.99"
    }
  ],
  "shipping_address": {
    "street": "123 Test Street",
    "city": "Test City",
    "state": "TS",
    "postal_code": "12345",
    "country": "Test Country"
  }
}
```

**Expected Behavior**:
- ✅ **Success (201)**: Order created successfully
- ❌ **Error (400)**: Invalid order data or empty cart

**Tests Tab Script**:
```javascript
pm.test("Order created successfully", function () {
    pm.expect(pm.response.code).to.equal(201);
    
    var jsonData = pm.response.json();
    pm.environment.set("order_id", jsonData.id);
    console.log("Order ID set:", jsonData.id);
});
```

### Test 28: List User Orders
**Endpoint**: `GET {{base_url}}/api/v1/orders/`
**Permission**: Authenticated users only
**Authorization**: Bearer Token `{{access_token}}`

**Expected Behavior**:
- ✅ **Success (200)**: Returns user's order history
- ❌ **Error (401)**: No authentication provided

### Test 29: Get Order Details
**Endpoint**: `GET {{base_url}}/api/v1/orders/{{order_id}}/`
**Permission**: Authenticated users only (order owner)
**Authorization**: Bearer Token `{{access_token}}`

**Expected Behavior**:
- ✅ **Success (200)**: Returns detailed order information
- ❌ **Error (404)**: Order not found
- ❌ **Error (403)**: Not the owner of the order

### Test 30: Get Order Status
**Endpoint**: `GET {{base_url}}/api/v1/orders/{{order_id}}/status/`
**Permission**: Authenticated users only (order owner)
**Authorization**: Bearer Token `{{access_token}}`

**Expected Behavior**:
- ✅ **Success (200)**: Returns current order status

### Test 31: Track Order
**Endpoint**: `GET {{base_url}}/api/v1/orders/{{order_id}}/track/`
**Permission**: Authenticated users only (order owner)
**Authorization**: Bearer Token `{{access_token}}`

**Expected Behavior**:
- ✅ **Success (200)**: Returns order tracking information

### Test 32: Get Order History
**Endpoint**: `GET {{base_url}}/api/v1/orders/history/`
**Permission**: Authenticated users only
**Authorization**: Bearer Token `{{access_token}}`

**Expected Behavior**:
- ✅ **Success (200)**: Returns user's complete order history

### Test 33: Cancel Order
**Endpoint**: `POST {{base_url}}/api/v1/orders/{{order_id}}/cancel/`
**Permission**: Authenticated users only (order owner)
**Authorization**: Bearer Token `{{access_token}}`

**Request Body**: None (empty POST request)

**Expected Behavior**:
- ✅ **Success (200)**: Order cancelled successfully
- ❌ **Error (400)**: Order cannot be cancelled (already completed, delivered, cancelled, or shipped)
- ❌ **Error (404)**: Order not found
- ❌ **Error (403)**: Not authorized (not order owner)

**Success Response Example**:
```json
{
  "message": "Order cancelled successfully.",
  "order": {
    "id": 1,
    "status": "cancelled",
    "payment_status": "paid",
    "total_amount": "999.99",
    "created_at": "2025-08-05T11:09:25.718563Z",
    "updated_at": "2025-08-07T10:26:34.937917Z"
  }
}
```

**Tests Tab Script**:
```javascript
pm.test("Cancel order successful", function () {
    if (pm.response.code === 200) {
        var jsonData = pm.response.json();
        pm.expect(jsonData.message).to.include("cancelled successfully");
        pm.expect(jsonData.order.status).to.equal("cancelled");
        console.log("Order cancelled successfully:", jsonData.order.id);
    } else if (pm.response.code === 400) {
        var errorData = pm.response.json();
        console.log("Cannot cancel order:", errorData.error);
        pm.expect(errorData.error).to.exist;
    }
    pm.expect(pm.response.code).to.be.oneOf([200, 400, 403, 404]);
});
```

### Test 34: Process Payment
**Endpoint**: `POST {{base_url}}/api/v1/orders/{{order_id}}/payment/`
**Permission**: Authenticated users only (order owner)
**Authorization**: Bearer Token `{{access_token}}`

⚠️ **Prerequisites**: 
- Must have an unpaid order (`payment_status: 'unpaid'`)
- Use an `order_id` from your orders list (Test 29)

**Request Body**:
```json
{
  "payment_method": "card",
  "payment_details": {
    "card_number": "4111111111111111",
    "expiry_month": "12",
    "expiry_year": "2025",
    "cvv": "123"
  }
}
```

**Alternative Payment Methods**:
- `"card"` (credit/debit card)
- `"credit_card"` 
- `"debit_card"`
- `"paypal"`
- `"bank_transfer"`

**Expected Behavior**:
- ✅ **Success (200)**: Payment processed successfully, order status updated to 'completed'
- ❌ **Error (400)**: Order already paid, invalid payment method, or validation errors
- ❌ **Error (404)**: Order not found
- ❌ **Error (403)**: Not authorized (not order owner)

**Success Response Example**:
```json
{
  "message": "Payment processed successfully.",
  "payment_method": "card",
  "order": {
    "id": 4,
    "status": "completed",
    "payment_status": "paid",
    "total_amount": "299.99",
    "user_email": "user@example.com"
  }
}
```

**Tests Tab Script**:
```javascript
pm.test("Payment processing", function () {
    if (pm.response.code === 200) {
        var jsonData = pm.response.json();
        pm.expect(jsonData.message).to.include("processed successfully");
        pm.expect(jsonData.order.payment_status).to.equal("paid");
        pm.expect(jsonData.order.status).to.equal("completed");
        console.log("Payment successful for order:", jsonData.order.id);
    } else if (pm.response.code === 400) {
        var errorData = pm.response.json();
        console.log("Payment failed:", errorData.error || errorData);
        // Common error cases
        if (errorData.error && errorData.error.includes("already paid")) {
            console.log("Order is already paid - use a different order");
        }
    }
    pm.expect(pm.response.code).to.be.oneOf([200, 400, 403, 404]);
});
```

---

## ⭐ Review System Testing

### Test 35: Get Product Reviews
**Endpoint**: `GET {{base_url}}/api/v1/reviews/product/{{product_id}}/`
**Permission**: Public

**Expected Behavior**:
- ✅ **Success (200)**: Returns reviews for the specified product

### Test 36: Get Product Review Stats
**Endpoint**: `GET {{base_url}}/api/v1/reviews/product/{{product_id}}/stats/`
**Permission**: Public

**Expected Behavior**:
- ✅ **Success (200)**: Returns review statistics (average rating, count, etc.)

### Test 37: Create Product Review
**Endpoint**: `POST {{base_url}}/api/v1/reviews/create/`
**Permission**: Authenticated users only
**Authorization**: Bearer Token `{{access_token}}`

**Request Body**:
```json
{
  "product": {{product_id}},
  "rating": 5,
  "title": "Excellent Product!",
  "comment": "This product exceeded my expectations. Highly recommended!"
}
```

**Expected Behavior**:
- ✅ **Success (201)**: Review created successfully
- ❌ **Error (400)**: Invalid rating or duplicate review

**Tests Tab Script**:
```javascript
pm.test("Review created successfully", function () {
    pm.expect(pm.response.code).to.equal(201);
    
    var jsonData = pm.response.json();
    pm.environment.set("review_id", jsonData.id);
    console.log("Review ID set:", jsonData.id);
});
```

### Test 38: Get Review Details
**Endpoint**: `GET {{base_url}}/api/v1/reviews/{{review_id}}/`
**Permission**: Public

**Expected Behavior**:
- ✅ **Success (200)**: Returns detailed review information
- ❌ **Error (404)**: Review not found

### Test 39: Update Review
**Endpoint**: `PUT {{base_url}}/api/v1/reviews/{{review_id}}/update/`
**Permission**: Authenticated users only (review owner)
**Authorization**: Bearer Token `{{access_token}}`

⚠️ **Prerequisites**: 
- Must have a review created by the authenticated user
- Use a `review_id` from your reviews (Test 41: Get User's Reviews)

**Request Body**:
```json
{
  "rating": 4,
  "comment": "Updated review: Good product but could be better."
}
```

**Field Validation**:
- `rating`: Integer between 1-5 (required)
- `comment`: Text field (optional, can be empty string)

**Expected Behavior**:
- ✅ **Success (200)**: Review updated successfully
- ❌ **Error (400)**: Validation errors (invalid rating, etc.)
- ❌ **Error (403)**: Not the owner of the review
- ❌ **Error (404)**: Review not found

**Success Response Example**:
```json
{
  "id": 1,
  "user": 2,
  "user_email": "user@example.com",
  "product": 5,
  "product_title": "iPhone 15 Pro",
  "rating": 4,
  "comment": "Updated review: Good product but could be better.",
  "created_at": "2025-08-07T10:15:00Z"
}
```

**Tests Tab Script**:
```javascript
pm.test("Update review", function () {
    if (pm.response.code === 200) {
        var jsonData = pm.response.json();
        pm.expect(jsonData.rating).to.exist;
        pm.expect(jsonData.comment).to.exist;
        pm.expect(jsonData.id).to.exist;
        console.log("Review updated successfully:", jsonData.id);
        
        // Validate rating is within range
        pm.expect(jsonData.rating).to.be.within(1, 5);
    } else if (pm.response.code === 403) {
        console.log("Access denied - not the review owner");
        pm.expect(pm.response.json().detail).to.exist;
    } else if (pm.response.code === 400) {
        var errorData = pm.response.json();
        console.log("Validation error:", errorData);
        pm.expect(errorData).to.exist;
    }
    
    pm.expect(pm.response.code).to.be.oneOf([200, 400, 403, 404]);
});
```

### Test 40: Delete Review
**Endpoint**: `DELETE {{base_url}}/api/v1/reviews/{{review_id}}/delete/`
**Permission**: Authenticated users only (review owner)
**Authorization**: Bearer Token `{{access_token}}`

**Expected Behavior**:
- ✅ **Success (204)**: Review deleted successfully
- ❌ **Error (403)**: Not the owner of the review

### Test 41: Get User's Reviews
**Endpoint**: `GET {{base_url}}/api/v1/reviews/user/`
**Permission**: Authenticated users only
**Authorization**: Bearer Token `{{access_token}}`

**Expected Behavior**:
- ✅ **Success (200)**: Returns all reviews by the authenticated user

### Test 42: Mark Review as Helpful
**Endpoint**: `POST {{base_url}}/api/v1/reviews/{{review_id}}/helpful/`
**Permission**: Authenticated users only
**Authorization**: Bearer Token `{{access_token}}`

**Expected Behavior**:
- ✅ **Success (200)**: Review marked as helpful

### Test 43: Report Review
**Endpoint**: `POST {{base_url}}/api/v1/reviews/{{review_id}}/report/`
**Permission**: Authenticated users only
**Authorization**: Bearer Token `{{access_token}}`

**Request Body**:
```json
{
  "reason": "inappropriate_content"
}
```

**Expected Behavior**:
- ✅ **Success (200)**: Review reported successfully

---

## 🔒 Permission Testing

### Test 44: Access Protected Endpoint Without Token
**Endpoint**: `GET {{base_url}}/api/v1/cart/`
**Permission**: None (Remove Authorization header)

**Expected Behavior**:
- ❌ **Error (401)**: Authentication credentials were not provided

### Test 45: Access Protected Endpoint with Invalid Token
**Endpoint**: `GET {{base_url}}/api/v1/cart/`
**Permission**: Bearer Token `invalid_token_here`

⚠️ **Purpose**: Verify that the API properly rejects invalid authentication tokens

**Test Scenarios**:

1. **Invalid Token Format**:
   ```
   Authorization: Bearer invalid_token_here
   ```

2. **Empty Bearer Token**:
   ```
   Authorization: Bearer
   ```

3. **No Authorization Header**:
   ```
   (No Authorization header)
   ```

4. **Wrong Authorization Format**:
   ```
   Authorization: InvalidFormat token123
   ```

**Expected Behavior**:
- ❌ **Error (401)**: Invalid token → `"Given token not valid for any token type"`
- ❌ **Error (401)**: Empty token → `"Authorization header must contain two space-delimited values"`
- ❌ **Error (401)**: No auth header → `"Authentication credentials were not provided"`
- ❌ **Error (401)**: Wrong format → `"Authentication credentials were not provided"`

**Success Response Examples**:
```json
{
  "detail": "Given token not valid for any token type",
  "code": "token_not_valid",
  "messages": [
    {
      "token_class": "AccessToken",
      "token_type": "access", 
      "message": "Token is invalid"
    }
  ]
}
```

**Alternative Endpoints to Test**:
- `GET {{base_url}}/api/v1/orders/`
- `GET {{base_url}}/api/v1/reviews/user/`
- `GET {{base_url}}/api/v1/users/profile/`

**Tests Tab Script**:
```javascript
pm.test("Invalid token rejection", function () {
    pm.expect(pm.response.code).to.equal(401);
    
    var jsonData = pm.response.json();
    pm.expect(jsonData.detail).to.exist;
    
    // Check for different types of auth errors
    var authErrors = [
        "Given token not valid for any token type",
        "Authentication credentials were not provided", 
        "Authorization header must contain two space-delimited values"
    ];
    
    var hasValidError = authErrors.some(error => 
        jsonData.detail.includes(error) || jsonData.detail === error
    );
    
    pm.expect(hasValidError).to.be.true;
    console.log("Authentication properly rejected:", jsonData.detail);
});
```

### Test 46: Access Other User's Cart
Create a second user and try to access first user's cart with second user's token.

**Expected Behavior**:
- ❌ **Error (403/404)**: Access denied or resource not found

### Test 47: Access Other User's Orders
**Endpoint**: `GET {{base_url}}/api/v1/orders/999999/`
**Permission**: Authenticated users only
**Authorization**: Bearer Token `{{access_token}}`

**Expected Behavior**:
- ❌ **Error (404)**: Order not found (or 403 if order exists but belongs to another user)

### Test 48: Modify Other User's Review
Try to update a review created by another user.

**Expected Behavior**:
- ❌ **Error (403)**: Permission denied

---

## 👑 Admin Functionality Testing

> **Note**: Create an admin user first using Django management command:
> ```bash
> python manage.py createsuperuser
> ```

### Test 49: Admin Login
**Endpoint**: `POST {{base_url}}/api/v1/auth/login/`
**Permission**: Public

⚠️ **Important**: Use email for admin login, not username

**Request Body**:
```json
{
  "email": "admin@ecommerce.com",
  "password": "adminpassword123"
}
```

**Tests Tab Script**:
```javascript
pm.test("Admin login successful", function () {
    pm.expect(pm.response.code).to.equal(200);
    
    if (pm.response.code === 200) {
        var jsonData = pm.response.json();
        pm.environment.set("admin_access_token", jsonData.access);
        pm.environment.set("admin_refresh_token", jsonData.refresh);
        console.log("Admin access token set");
    } else {
        console.log("Admin login failed:", pm.response.text());
    }
});
```

### Test 50: Create Product (Admin Only)
**Endpoint**: `POST {{base_url}}/api/v1/admin/products/`
**Permission**: Admin users only
**Authorization**: Bearer Token

**Request Body**:
```json
{
  "name": "Test Product Admin",
  "description": "This is a test product created by admin",
  "price": "99.99",
  "category": 1,
  "stock": 100
}
```

**Security Validation Steps**:

1. **Without Authentication**:
   ```bash
   POST {{base_url}}/api/v1/admin/products/
   # Expected: 401 Unauthorized
   ```

2. **With Regular User Token** `{{access_token}}`:
   ```bash
   POST {{base_url}}/api/v1/admin/products/
   Authorization: Bearer {{access_token}}
   # Expected: 403 Forbidden
   ```

3. **With Admin Token** `{{admin_access_token}}`:
   ```bash
   POST {{base_url}}/api/v1/admin/products/
   Authorization: Bearer {{admin_access_token}}
   # Expected: 201 Created
   ```

**Expected Behavior**:
- ✅ **Success (201)**: Product created successfully (Admin users only)
- ❌ **Error (401)**: Authentication required (No token)
- ❌ **Error (403)**: "You do not have permission to perform this action." (Regular users)

**Postman Tests**:
```javascript
pm.test("Status code validation", function () {
    if (pm.request.headers.get("Authorization")) {
        if (pm.globals.get("admin_access_token") && 
            pm.request.headers.get("Authorization").includes(pm.globals.get("admin_access_token"))) {
            pm.response.to.have.status(201);
            pm.test("Product created by admin", function () {
                pm.expect(pm.response.json()).to.have.property('id');
                pm.expect(pm.response.json()).to.have.property('name');
            });
        } else {
            pm.response.to.have.status(403);
            pm.test("Regular user properly blocked", function () {
                pm.expect(pm.response.json().detail).to.include("permission");
            });
        }
    } else {
        pm.response.to.have.status(401);
    }
});
```

**Note**: This endpoint properly enforces admin-only access using the `IsAdminOrReadOnly` permission class. Regular users can read products (GET) but cannot create, update, or delete them (POST/PUT/DELETE).

### Test 51: Update Product (Admin Only)
**Endpoint**: `PUT {{base_url}}/api/v1/admin/products/{{product_id}}/`
**Permission**: Admin users only
**Authorization**: Bearer Token `{{admin_access_token}}`

**Request Body**:
```json
{
  "title": "Updated Test Product",
  "price": "199.99"
}
```

**Expected Behavior**:
- ✅ **Success (200)**: Product updated successfully (Admin)
- ❌ **Error (403)**: Permission denied (Regular user)

### Test 51.5: Admin Root Endpoint Security
**Endpoint**: `GET {{base_url}}/api/v1/admin/`
**Permission**: Admin users only (Information Disclosure Prevention)
**Security Focus**: Prevents unauthorized access to admin endpoint directory

**Security Validation Steps**:

1. **Without Authentication**:
   ```bash
   GET {{base_url}}/api/v1/admin/
   # Expected: 401 Unauthorized
   ```

2. **With Regular User Token** `{{access_token}}`:
   ```bash
   GET {{base_url}}/api/v1/admin/
   Authorization: Bearer {{access_token}}
   # Expected: 403 Forbidden
   ```

3. **With Admin Token** `{{admin_access_token}}`:
   ```bash
   GET {{base_url}}/api/v1/admin/
   Authorization: Bearer {{admin_access_token}}
   # Expected: 200 OK with admin endpoints list
   ```

**Expected Behavior**:
- ✅ **Success (200)**: Returns admin endpoint directory (Admin users only)
- ❌ **Error (401)**: Authentication required (No token)
- ❌ **Error (403)**: "You do not have permission to perform this action." (Regular users)

**Security Importance**:
This test prevents **information disclosure vulnerability** where regular users could discover admin endpoint structures. Fixed in August 2025 security update.

**Postman Tests**:
```javascript
pm.test("Admin root security validation", function () {
    if (!pm.request.headers.get("Authorization")) {
        pm.response.to.have.status(401);
        pm.test("Authentication required", function () {
            pm.expect(pm.response.json().detail).to.include("Authentication credentials");
        });
    } else if (pm.globals.get("admin_access_token") && 
               pm.request.headers.get("Authorization").includes(pm.globals.get("admin_access_token"))) {
        pm.response.to.have.status(200);
        pm.test("Admin can access endpoint directory", function () {
            pm.expect(pm.response.json()).to.have.property('products');
            pm.expect(pm.response.json()).to.have.property('categories');
        });
    } else {
        pm.response.to.have.status(403);
        pm.test("Regular user properly blocked", function () {
            pm.expect(pm.response.json().detail).to.include("permission");
        });
    }
});
```

### Test 52: Create Category (Admin Only)
**Endpoint**: `POST {{base_url}}/api/v1/admin/categories/`
**Permission**: Admin users only
**Authorization**: Bearer Token `{{admin_access_token}}`

**Request Body**:
```json
{
  "name": "Test Category",
  "description": "This is a test category"
}
```

**Expected Behavior**:
- ✅ **Success (201)**: Category created successfully (Admin)
- ❌ **Error (403)**: Permission denied (Regular user)

### Test 53: View All Orders (Admin Only)
**Endpoint**: `GET {{base_url}}/api/v1/orders/admin/all/`
**Permission**: Admin users only
**Authorization**: Bearer Token `{{admin_access_token}}`

**Expected Behavior**:
- ✅ **Success (200)**: Returns all orders in the system (Admin)
- ❌ **Error (403)**: Permission denied (Regular user)

### Test 54: Update Order Status (Admin Only)
**Endpoint**: `POST {{base_url}}/api/v1/orders/admin/{{order_id}}/update-status/`
**Permission**: Admin users only
**Authorization**: Bearer Token `{{admin_access_token}}`

**Request Body**:
```json
{
  "status": "shipped"
}
```

**Expected Behavior**:
- ✅ **Success (200)**: Order status updated (Admin)
- ❌ **Error (403)**: Permission denied (Regular user)

### Test 55: Delete Product (Admin Only)
**Endpoint**: `DELETE {{base_url}}/api/v1/admin/products/{{product_id}}/`
**Permission**: Admin users only
**Authorization**: Bearer Token `{{admin_access_token}}`

**Expected Behavior**:
- ✅ **Success (204)**: Product deleted successfully (Admin)
- ❌ **Error (403)**: Permission denied (Regular user)

### Test 56: Delete Category (Admin Only)
**Endpoint**: `DELETE {{base_url}}/api/v1/admin/categories/{{category_id}}/`
**Permission**: Admin users only
**Authorization**: Bearer Token `{{admin_access_token}}`

**Expected Behavior**:
- ✅ **Success (204)**: Category deleted successfully (Admin)
- ❌ **Error (403)**: Permission denied (Regular user)

---

## 🧪 Edge Case Testing

### Test 57: Large Cart Test
Add 50+ items to cart to test performance and limits.

### Test 58: Concurrent User Test
Test same product purchase by multiple users simultaneously.

### Test 59: Invalid Data Test
Send malformed JSON, invalid UUIDs, negative quantities, etc.

### Test 60: Rate Limiting Test
Make rapid successive requests to test rate limiting.

---

## 📊 Testing Summary

### Expected Response Codes:
- **200**: Successful GET, PUT requests
- **201**: Successful POST requests (creation)
- **204**: Successful DELETE requests
- **205**: Successful logout (Reset Content) - this is the correct logout response
- **400**: Bad request (validation errors, token type mismatch)
- **401**: Unauthorized (no token, invalid token, expired token)
- **403**: Forbidden (insufficient permissions, rate limiting)
- **404**: Resource not found
- **429**: Too many requests (rate limiting)

### Authentication System Status:
- ✅ **Email-based login**: Fixed and working
- ✅ **JWT token generation**: Custom serializer implemented
- ✅ **Access/Refresh tokens**: Properly separated and functional
- ✅ **Logout endpoint**: Returns 205 status (correct behavior)
- ✅ **Token blacklisting**: Implemented and working
- ✅ **Rate limiting**: Active (5 login attempts per 5 minutes)
- ✅ **Debug logging**: Enhanced error reporting for troubleshooting

### Permission Levels:
1. **Public**: No authentication required
2. **Authenticated**: Valid JWT token required
3. **Owner**: Must be the owner of the resource
4. **Admin**: Admin/superuser privileges required

### Security Features Tested:
- JWT token authentication and refresh
- Role-based access control (User vs Admin)
- Resource ownership validation
- Input validation and sanitization
- Cross-user resource access prevention
- Rate limiting protection
- Password security requirements

### Complete Endpoint Coverage:

#### Authentication & User Management (8 tests):
- User registration, login, logout
- Token refresh, password change
- Profile management, address management

#### Catalog Management (9 tests):
- Product listing, search, featured products
- Category management and product filtering
- Public access validation

#### Cart Management (9 tests):
- Cart operations (add, update, remove, clear)
- Quantity management
- Cart totals and item counts

#### Order Management (8 tests):
- Order creation, listing, tracking
- Payment processing
- Order status management

#### Review System (9 tests):
- Review CRUD operations
- Review statistics and reporting
- User review management

#### Permission Testing (5 tests):
- Authentication validation
- Cross-user access prevention
- Token validation

#### Admin Functionality (8 tests):
- Product and category CRUD (admin only)
- Order management (admin only)
- Permission validation

#### Edge Cases (4 tests):
- Performance testing
- Data validation
- Rate limiting

**Total: 60 Comprehensive Tests**

---

## 🔍 Testing Best Practices

### Before Testing:
1. **Ensure server is running**: `python manage.py runserver 0.0.0.0:8001`
2. **Database has seed data**: Run the seeding script
3. **Environment variables set**: Check Postman environment
4. **Create test users**: Both regular and admin users
5. **Verify authentication**: Test login with `admin@ecommerce.com` / `adminpassword123`

### During Testing:
1. **Run tests in order**: Authentication → User → Catalog → Cart → Orders → Reviews → Admin
2. **Monitor console logs**: Check for successful variable setting
3. **Verify response data**: Ensure returned data matches expectations
4. **Test edge cases**: Try invalid data, missing fields, token swapping
5. **Check authentication flow**: Login → Test protected endpoint → Logout (205 response)

### Common Testing Pitfalls:
- ❌ Using `username` instead of `email` for login
- ❌ Swapping access and refresh tokens in logout requests
- ❌ Expecting 200 instead of 205 for logout success
- ❌ Not waiting for rate limit reset (5 minutes)
- ❌ Using expired tokens (get fresh ones via login)

### After Testing:
1. **Review security logs**: Check `logs/security.log` for security events
2. **Verify logout behavior**: Ensure 205 response and token blacklisting works
3. **Test token expiration**: Verify expired tokens return 401
4. **Clean up test data**: Remove test users and orders if needed

---

## 🚀 Quick Start Checklist

- [ ] Django server running on port 8001
- [ ] Postman environment created with variables
- [ ] Collection imported with all 60 tests
- [ ] Admin user created via Django admin
- [ ] Database seeded with sample data
- [ ] Authentication tests passing
- [ ] Permission validations working
- [ ] All endpoints responding correctly

---

## 🎯 Expected Test Results

After running all 60 tests, you should see:
- **✅ Authentication system**: Secure login/logout with JWT
- **✅ Permission system**: Proper access control enforcement
- **✅ Data validation**: Input sanitization and validation working
- **✅ Business logic**: Cart, orders, reviews functioning correctly
- **✅ Admin controls**: Admin-only operations properly restricted
- **✅ Security measures**: Rate limiting and security headers active

**Happy Testing! 🎉**

---

*This comprehensive guide covers all API endpoints, permission levels, and security features of the E-Commerce backend. Each test includes expected behaviors, proper error handling, and security validations.*
