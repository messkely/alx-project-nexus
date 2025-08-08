-- ALX E-Commerce Backend Database Schema
-- Generated for Django 5.2.1-based e-commerce application
-- PostgreSQL Database
-- Last Updated: August 7, 2025

-- Drop existing tables if they exist (in proper order to handle foreign keys)
DROP TABLE IF EXISTS reviews_review CASCADE;
DROP TABLE IF EXISTS orders_orderitem CASCADE;
DROP TABLE IF EXISTS orders_order CASCADE;
DROP TABLE IF EXISTS cart_cartitem CASCADE;
DROP TABLE IF EXISTS cart_cart CASCADE;
DROP TABLE IF EXISTS users_address CASCADE;
DROP TABLE IF EXISTS catalog_product CASCADE;
DROP TABLE IF EXISTS catalog_category CASCADE;
DROP TABLE IF EXISTS users_user CASCADE;
DROP TABLE IF EXISTS users_user_groups CASCADE;
DROP TABLE IF EXISTS users_user_user_permissions CASCADE;
DROP TABLE IF EXISTS django_migrations CASCADE;
DROP TABLE IF EXISTS django_content_type CASCADE;
DROP TABLE IF EXISTS auth_permission CASCADE;
DROP TABLE IF EXISTS auth_group CASCADE;
DROP TABLE IF EXISTS auth_group_permissions CASCADE;
DROP TABLE IF EXISTS django_admin_log CASCADE;
DROP TABLE IF EXISTS django_session CASCADE;
DROP TABLE IF EXISTS authtoken_token CASCADE;
DROP TABLE IF EXISTS token_blacklist_blacklistedtoken CASCADE;
DROP TABLE IF EXISTS token_blacklist_outstandingtoken CASCADE;

-- Create Users table (extends Django's AbstractUser)
CREATE TABLE users_user (
    id BIGSERIAL PRIMARY KEY,
    password VARCHAR(128) NOT NULL,
    last_login TIMESTAMP WITH TIME ZONE,
    is_superuser BOOLEAN NOT NULL DEFAULT FALSE,
    username VARCHAR(150) NOT NULL UNIQUE,
    first_name VARCHAR(150) NOT NULL DEFAULT '',
    last_name VARCHAR(150) NOT NULL DEFAULT '',
    email VARCHAR(254) NOT NULL UNIQUE,
    is_staff BOOLEAN NOT NULL DEFAULT FALSE,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    date_joined TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW()
);

-- Create Address table
CREATE TABLE users_address (
    id BIGSERIAL PRIMARY KEY,
    user_id BIGINT NOT NULL REFERENCES users_user(id) ON DELETE CASCADE,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    address_line_1 VARCHAR(255) NOT NULL,
    address_line_2 VARCHAR(255) DEFAULT '',
    city VARCHAR(100) NOT NULL,
    postal_code VARCHAR(20) NOT NULL,
    country VARCHAR(100) NOT NULL,
    phone_number VARCHAR(20) NOT NULL,
    is_default BOOLEAN NOT NULL DEFAULT FALSE
);

-- Create Category table
CREATE TABLE catalog_category (
    id BIGSERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL UNIQUE,
    slug VARCHAR(255) NOT NULL UNIQUE,
    description TEXT DEFAULT '',
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW()
);

-- Create Product table
CREATE TABLE catalog_product (
    id BIGSERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT DEFAULT '',
    price DECIMAL(10, 2) NOT NULL,
    stock_quantity INTEGER NOT NULL CHECK (stock_quantity >= 0) DEFAULT 0,
    image VARCHAR(100) DEFAULT '',
    slug VARCHAR(255) NOT NULL UNIQUE,
    category_id BIGINT NOT NULL REFERENCES catalog_category(id) ON DELETE CASCADE,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW()
);

-- Create Cart table
CREATE TABLE cart_cart (
    id BIGSERIAL PRIMARY KEY,
    user_id BIGINT REFERENCES users_user(id) ON DELETE SET NULL,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW()
);

-- Create CartItem table
CREATE TABLE cart_cartitem (
    id BIGSERIAL PRIMARY KEY,
    cart_id BIGINT NOT NULL REFERENCES cart_cart(id) ON DELETE CASCADE,
    product_id BIGINT NOT NULL REFERENCES catalog_product(id) ON DELETE CASCADE,
    quantity INTEGER NOT NULL CHECK (quantity > 0) DEFAULT 1
);

-- Create Order table
CREATE TABLE orders_order (
    id BIGSERIAL PRIMARY KEY,
    user_id BIGINT NOT NULL REFERENCES users_user(id) ON DELETE CASCADE,
    status VARCHAR(20) NOT NULL DEFAULT 'pending' CHECK (status IN ('pending', 'processing', 'shipped', 'delivered', 'cancelled', 'completed', 'failed')),
    payment_status VARCHAR(20) NOT NULL DEFAULT 'unpaid' CHECK (payment_status IN ('paid', 'unpaid')),
    total_amount DECIMAL(10, 2) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW()
);

-- Create OrderItem table
CREATE TABLE orders_orderitem (
    id BIGSERIAL PRIMARY KEY,
    order_id BIGINT NOT NULL REFERENCES orders_order(id) ON DELETE CASCADE,
    product_id BIGINT NOT NULL REFERENCES catalog_product(id) ON DELETE CASCADE,
    quantity INTEGER NOT NULL CHECK (quantity > 0),
    unit_price DECIMAL(10, 2) NOT NULL,
    subtotal DECIMAL(10, 2) NOT NULL
);

-- Create Review table
CREATE TABLE reviews_review (
    id BIGSERIAL PRIMARY KEY,
    user_id BIGINT NOT NULL REFERENCES users_user(id) ON DELETE CASCADE,
    product_id BIGINT NOT NULL REFERENCES catalog_product(id) ON DELETE CASCADE,
    rating INTEGER NOT NULL CHECK (rating >= 1 AND rating <= 5),
    comment TEXT DEFAULT '',
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    UNIQUE(user_id, product_id)
);

-- Create indexes for better performance
CREATE INDEX idx_catalog_product_price ON catalog_product(price);
CREATE INDEX idx_catalog_product_created_at ON catalog_product(created_at DESC);
CREATE INDEX idx_catalog_product_category ON catalog_product(category_id);
CREATE INDEX idx_catalog_product_is_active ON catalog_product(is_active);
CREATE INDEX idx_catalog_product_stock_quantity ON catalog_product(stock_quantity);
CREATE INDEX idx_catalog_category_slug ON catalog_category(slug);
CREATE INDEX idx_orders_order_user ON orders_order(user_id);
CREATE INDEX idx_orders_order_status ON orders_order(status);
CREATE INDEX idx_orders_order_created_at ON orders_order(created_at DESC);
CREATE INDEX idx_reviews_review_product ON reviews_review(product_id);
CREATE INDEX idx_reviews_review_rating ON reviews_review(rating);
CREATE INDEX idx_users_address_user ON users_address(user_id);
CREATE INDEX idx_users_address_is_default ON users_address(is_default);
CREATE INDEX idx_cart_cart_user ON cart_cart(user_id);
CREATE INDEX idx_cart_cartitem_cart ON cart_cartitem(cart_id);
CREATE INDEX idx_orders_orderitem_order ON orders_orderitem(order_id);

-- Create Django required tables for admin and auth
CREATE TABLE auth_group (
    id SERIAL PRIMARY KEY,
    name VARCHAR(150) NOT NULL UNIQUE
);

CREATE TABLE django_content_type (
    id SERIAL PRIMARY KEY,
    app_label VARCHAR(100) NOT NULL,
    model VARCHAR(100) NOT NULL,
    UNIQUE(app_label, model)
);

CREATE TABLE auth_permission (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    content_type_id INTEGER NOT NULL REFERENCES django_content_type(id),
    codename VARCHAR(100) NOT NULL,
    UNIQUE(content_type_id, codename)
);

CREATE TABLE auth_group_permissions (
    id BIGSERIAL PRIMARY KEY,
    group_id INTEGER NOT NULL REFERENCES auth_group(id),
    permission_id INTEGER NOT NULL REFERENCES auth_permission(id),
    UNIQUE(group_id, permission_id)
);

CREATE TABLE users_user_groups (
    id BIGSERIAL PRIMARY KEY,
    user_id BIGINT NOT NULL REFERENCES users_user(id) ON DELETE CASCADE,
    group_id INTEGER NOT NULL REFERENCES auth_group(id) ON DELETE CASCADE,
    UNIQUE(user_id, group_id)
);

CREATE TABLE users_user_user_permissions (
    id BIGSERIAL PRIMARY KEY,
    user_id BIGINT NOT NULL REFERENCES users_user(id) ON DELETE CASCADE,
    permission_id INTEGER NOT NULL REFERENCES auth_permission(id) ON DELETE CASCADE,
    UNIQUE(user_id, permission_id)
);

CREATE TABLE django_admin_log (
    id SERIAL PRIMARY KEY,
    action_time TIMESTAMP WITH TIME ZONE NOT NULL,
    object_id TEXT,
    object_repr VARCHAR(200) NOT NULL,
    action_flag SMALLINT NOT NULL CHECK (action_flag >= 0),
    change_message TEXT NOT NULL,
    content_type_id INTEGER REFERENCES django_content_type(id) ON DELETE SET NULL,
    user_id BIGINT NOT NULL REFERENCES users_user(id) ON DELETE CASCADE
);

CREATE TABLE django_session (
    session_key VARCHAR(40) PRIMARY KEY,
    session_data TEXT NOT NULL,
    expire_date TIMESTAMP WITH TIME ZONE NOT NULL
);

CREATE INDEX idx_django_session_expire_date ON django_session(expire_date);

CREATE TABLE authtoken_token (
    key VARCHAR(40) PRIMARY KEY,
    created TIMESTAMP WITH TIME ZONE NOT NULL,
    user_id BIGINT NOT NULL UNIQUE REFERENCES users_user(id) ON DELETE CASCADE
);

-- JWT Token Blacklist tables
CREATE TABLE token_blacklist_outstandingtoken (
    id BIGSERIAL PRIMARY KEY,
    token TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL,
    expires_at TIMESTAMP WITH TIME ZONE NOT NULL,
    user_id BIGINT REFERENCES users_user(id) ON DELETE CASCADE,
    jti VARCHAR(255) NOT NULL UNIQUE
);

CREATE TABLE token_blacklist_blacklistedtoken (
    id BIGSERIAL PRIMARY KEY,
    blacklisted_at TIMESTAMP WITH TIME ZONE NOT NULL,
    token_id BIGINT NOT NULL UNIQUE REFERENCES token_blacklist_outstandingtoken(id) ON DELETE CASCADE
);

CREATE INDEX idx_token_blacklist_outstandingtoken_user ON token_blacklist_outstandingtoken(user_id);
CREATE INDEX idx_token_blacklist_outstandingtoken_jti ON token_blacklist_outstandingtoken(jti);

-- Django Migrations table
CREATE TABLE django_migrations (
    id SERIAL PRIMARY KEY,
    app VARCHAR(255) NOT NULL,
    name VARCHAR(255) NOT NULL,
    applied TIMESTAMP WITH TIME ZONE NOT NULL
);

-- Insert Django content types
INSERT INTO django_content_type (app_label, model) VALUES
('admin', 'logentry'),
('auth', 'permission'),
('auth', 'group'),
('contenttypes', 'contenttype'),
('sessions', 'session'),
('authtoken', 'token'),
('authtoken', 'tokenproxy'),
('token_blacklist', 'blacklistedtoken'),
('token_blacklist', 'outstandingtoken'),
('users', 'user'),
('users', 'address'),
('catalog', 'category'),
('catalog', 'product'),
('cart', 'cart'),
('cart', 'cartitem'),
('orders', 'order'),
('orders', 'orderitem'),
('reviews', 'review');

-- Insert permissions for each model
INSERT INTO auth_permission (name, content_type_id, codename) VALUES
-- Users app permissions
('Can add user', (SELECT id FROM django_content_type WHERE app_label='users' AND model='user'), 'add_user'),
('Can change user', (SELECT id FROM django_content_type WHERE app_label='users' AND model='user'), 'change_user'),
('Can delete user', (SELECT id FROM django_content_type WHERE app_label='users' AND model='user'), 'delete_user'),
('Can view user', (SELECT id FROM django_content_type WHERE app_label='users' AND model='user'), 'view_user'),
('Can add address', (SELECT id FROM django_content_type WHERE app_label='users' AND model='address'), 'add_address'),
('Can change address', (SELECT id FROM django_content_type WHERE app_label='users' AND model='address'), 'change_address'),
('Can delete address', (SELECT id FROM django_content_type WHERE app_label='users' AND model='address'), 'delete_address'),
('Can view address', (SELECT id FROM django_content_type WHERE app_label='users' AND model='address'), 'view_address'),
-- Catalog app permissions
('Can add category', (SELECT id FROM django_content_type WHERE app_label='catalog' AND model='category'), 'add_category'),
('Can change category', (SELECT id FROM django_content_type WHERE app_label='catalog' AND model='category'), 'change_category'),
('Can delete category', (SELECT id FROM django_content_type WHERE app_label='catalog' AND model='category'), 'delete_category'),
('Can view category', (SELECT id FROM django_content_type WHERE app_label='catalog' AND model='category'), 'view_category'),
('Can add product', (SELECT id FROM django_content_type WHERE app_label='catalog' AND model='product'), 'add_product'),
('Can change product', (SELECT id FROM django_content_type WHERE app_label='catalog' AND model='product'), 'change_product'),
('Can delete product', (SELECT id FROM django_content_type WHERE app_label='catalog' AND model='product'), 'delete_product'),
('Can view product', (SELECT id FROM django_content_type WHERE app_label='catalog' AND model='product'), 'view_product'),
-- Cart app permissions
('Can add cart', (SELECT id FROM django_content_type WHERE app_label='cart' AND model='cart'), 'add_cart'),
('Can change cart', (SELECT id FROM django_content_type WHERE app_label='cart' AND model='cart'), 'change_cart'),
('Can delete cart', (SELECT id FROM django_content_type WHERE app_label='cart' AND model='cart'), 'delete_cart'),
('Can view cart', (SELECT id FROM django_content_type WHERE app_label='cart' AND model='cart'), 'view_cart'),
('Can add cart item', (SELECT id FROM django_content_type WHERE app_label='cart' AND model='cartitem'), 'add_cartitem'),
('Can change cart item', (SELECT id FROM django_content_type WHERE app_label='cart' AND model='cartitem'), 'change_cartitem'),
('Can delete cart item', (SELECT id FROM django_content_type WHERE app_label='cart' AND model='cartitem'), 'delete_cartitem'),
('Can view cart item', (SELECT id FROM django_content_type WHERE app_label='cart' AND model='cartitem'), 'view_cartitem'),
-- Orders app permissions
('Can add order', (SELECT id FROM django_content_type WHERE app_label='orders' AND model='order'), 'add_order'),
('Can change order', (SELECT id FROM django_content_type WHERE app_label='orders' AND model='order'), 'change_order'),
('Can delete order', (SELECT id FROM django_content_type WHERE app_label='orders' AND model='order'), 'delete_order'),
('Can view order', (SELECT id FROM django_content_type WHERE app_label='orders' AND model='order'), 'view_order'),
('Can add order item', (SELECT id FROM django_content_type WHERE app_label='orders' AND model='orderitem'), 'add_orderitem'),
('Can change order item', (SELECT id FROM django_content_type WHERE app_label='orders' AND model='orderitem'), 'change_orderitem'),
('Can delete order item', (SELECT id FROM django_content_type WHERE app_label='orders' AND model='orderitem'), 'delete_orderitem'),
('Can view order item', (SELECT id FROM django_content_type WHERE app_label='orders' AND model='orderitem'), 'view_orderitem'),
-- Reviews app permissions
('Can add review', (SELECT id FROM django_content_type WHERE app_label='reviews' AND model='review'), 'add_review'),
('Can change review', (SELECT id FROM django_content_type WHERE app_label='reviews' AND model='review'), 'change_review'),
('Can delete review', (SELECT id FROM django_content_type WHERE app_label='reviews' AND model='review'), 'delete_review'),
('Can view review', (SELECT id FROM django_content_type WHERE app_label='reviews' AND model='review'), 'view_review');

-- Table comments
COMMENT ON TABLE users_user IS 'Custom user model extending Django AbstractUser with email authentication';
COMMENT ON TABLE users_address IS 'User shipping and billing addresses with default address support';
COMMENT ON TABLE catalog_category IS 'Product categories for organizing the product catalog';
COMMENT ON TABLE catalog_product IS 'Products available in the e-commerce store with inventory tracking';
COMMENT ON TABLE cart_cart IS 'Shopping carts for registered and anonymous users';
COMMENT ON TABLE cart_cartitem IS 'Individual items within shopping carts with quantity tracking';
COMMENT ON TABLE orders_order IS 'Customer orders with status and payment tracking';
COMMENT ON TABLE orders_orderitem IS 'Individual items within each order with pricing details';
COMMENT ON TABLE reviews_review IS 'Product reviews and ratings by customers';
COMMENT ON TABLE token_blacklist_outstandingtoken IS 'Outstanding JWT tokens for blacklist management';
COMMENT ON TABLE token_blacklist_blacklistedtoken IS 'Blacklisted JWT tokens to prevent reuse';

-- Column comments
COMMENT ON COLUMN catalog_product.stock_quantity IS 'Current inventory level (replaces inventory field)';
COMMENT ON COLUMN catalog_product.image IS 'Path to product image file in media storage';
COMMENT ON COLUMN orders_order.status IS 'Order processing status: pending, processing, shipped, delivered, cancelled, completed, failed';
COMMENT ON COLUMN orders_order.payment_status IS 'Payment status: paid or unpaid';
COMMENT ON COLUMN reviews_review.rating IS 'Product rating from 1 to 5 stars';

-- Summary
-- This schema supports:
-- - JWT-based authentication with token blacklisting
-- - Multi-category product catalog with inventory management
-- - Shopping cart functionality for registered users
-- - Complete order processing workflow
-- - Product review and rating system
-- - Django admin interface integration
-- - Comprehensive indexing for performance optimization
