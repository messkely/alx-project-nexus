# Database Entity Relationship Diagram

```mermaid
erDiagram
    users_user {
        bigint id PK
        varchar password
        timestamp last_login
        boolean is_superuser
        varchar username UK
        varchar first_name
        varchar last_name
        varchar email UK
        boolean is_staff
        boolean is_active
        timestamp date_joined
    }
    
    users_address {
        bigint id PK
        bigint user_id FK
        varchar first_name
        varchar last_name
        varchar address_line_1
        varchar address_line_2
        varchar city
        varchar postal_code
        varchar country
        varchar phone_number
        boolean is_default
    }
    
    catalog_category {
        bigint id PK
        varchar name UK
        varchar slug UK
        timestamp created_at
    }
    
    catalog_product {
        bigint id PK
        varchar title
        text description
        decimal price
        integer inventory
        varchar slug UK
        bigint category_id FK
        boolean is_active
        timestamp created_at
        timestamp updated_at
    }
    
    cart_cart {
        bigint id PK
        bigint user_id FK
        timestamp created_at
    }
    
    cart_cartitem {
        bigint id PK
        bigint cart_id FK
        bigint product_id FK
        integer quantity
    }
    
    orders_order {
        bigint id PK
        bigint user_id FK
        varchar status
        varchar payment_status
        decimal total_amount
        timestamp created_at
        timestamp updated_at
    }
    
    orders_orderitem {
        bigint id PK
        bigint order_id FK
        bigint product_id FK
        integer quantity
        decimal unit_price
        decimal subtotal
    }
    
    reviews_review {
        bigint id PK
        bigint user_id FK
        bigint product_id FK
        integer rating
        text comment
        timestamp created_at
    }

    %% Relationships
    users_user ||--o{ users_address : has
    users_user ||--o{ cart_cart : owns
    users_user ||--o{ orders_order : places
    users_user ||--o{ reviews_review : writes
    
    catalog_category ||--o{ catalog_product : contains
    
    catalog_product ||--o{ cart_cartitem : "added_to"
    catalog_product ||--o{ orders_orderitem : "ordered_as"
    catalog_product ||--o{ reviews_review : "reviewed_in"
    
    cart_cart ||--o{ cart_cartitem : contains
    
    orders_order ||--o{ orders_orderitem : contains
```

## Database Schema Summary

### Core Entities

#### 1. User Management
- **users_user**: Extended Django user model with email-based authentication
- **users_address**: Multiple shipping addresses per user with default selection

#### 2. Product Catalog
- **catalog_category**: Hierarchical product categorization
- **catalog_product**: Product information with pricing, inventory, and metadata

#### 3. Shopping Experience
- **cart_cart**: User shopping carts (can be anonymous)
- **cart_cartitem**: Items in shopping carts with quantities

#### 4. Order Management
- **orders_order**: Order headers with status tracking
- **orders_orderitem**: Individual line items within orders

#### 5. Customer Feedback
- **reviews_review**: Product reviews with 1-5 star ratings

### Key Relationships

1. **One-to-Many**:
   - User → Addresses (1:M)
   - User → Carts (1:M)
   - User → Orders (1:M)
   - User → Reviews (1:M)
   - Category → Products (1:M)
   - Cart → CartItems (1:M)
   - Order → OrderItems (1:M)

2. **Many-to-Many** (through intermediary tables):
   - User ↔ Products (through Cart/Order/Review)
   - Cart ↔ Products (through CartItems)
   - Order ↔ Products (through OrderItems)

3. **Unique Constraints**:
   - User can only review a product once (user_id, product_id unique)
   - Email addresses must be unique
   - Product and category slugs must be unique

### Business Rules Enforced

1. **User Management**:
   - Email-based authentication
   - Multiple shipping addresses per user
   - Default address selection

2. **Product Catalog**:
   - Products must belong to a category
   - Inventory tracking with non-negative constraints
   - URL-friendly slugs for SEO

3. **Shopping Cart**:
   - Items have positive quantities
   - Anonymous carts supported (user_id can be null)

4. **Orders**:
   - Order status workflow (pending → completed/failed)
   - Payment status tracking
   - Historical pricing preservation in order items

5. **Reviews**:
   - Rating scale 1-5 stars
   - One review per user per product
   - Optional comment field

### Performance Optimizations

#### Indexes Created:
- `catalog_product(price)` - for price-based filtering
- `catalog_product(created_at)` - for chronological sorting
- `catalog_product(category_id)` - for category browsing
- `orders_order(user_id)` - for user order history
- `orders_order(status)` - for order management
- `reviews_review(product_id)` - for product reviews
- `users_address(user_id)` - for user addresses

#### Views for Reporting:
- `order_summary` - Order overview with customer details
- `product_stats` - Product performance metrics

### Data Integrity

#### Foreign Key Constraints:
- Addresses → Users (CASCADE DELETE)
- Products → Categories (CASCADE DELETE)
- CartItems → Carts (CASCADE DELETE)
- CartItems → Products (CASCADE DELETE)
- OrderItems → Orders (CASCADE DELETE)
- OrderItems → Products (RESTRICT DELETE)
- Reviews → Users (CASCADE DELETE)
- Reviews → Products (CASCADE DELETE)

#### Check Constraints:
- Product inventory ≥ 0
- CartItem quantity > 0
- OrderItem quantity > 0
- Review rating between 1 and 5
- Order status in allowed values
- Payment status in allowed values

This schema supports a full-featured e-commerce application with user management, product catalog, shopping cart, order processing, and customer review functionality.
