-- SQL Data Seeding Script for ALX E-commerce Database
-- This script inserts comprehensive sample data for testing and development
-- Run after migrations have been applied: python manage.py migrate

-- Insert sample users (passwords are hashed using Django's PBKDF2 algorithm)
-- Default password for all users is 'testpass123'
INSERT INTO users_user (password, last_login, is_superuser, username, first_name, last_name, email, is_staff, is_active, date_joined) VALUES
('pbkdf2_sha256$600000$YQAb7oAI2HyNqQe0kWe5WG$QX5nCLmZBNhJ1LFvTbOv4fOuJMu4I2BcHhOcwGxm5nM=', NULL, true, 'admin', 'Admin', 'User', 'admin@alxecommerce.com', true, true, NOW()),
('pbkdf2_sha256$600000$YQAb7oAI2HyNqQe0kWe5WG$QX5nCLmZBNhJ1LFvTbOv4fOuJMu4I2BcHhOcwGxm5nM=', NULL, false, 'johndoe', 'John', 'Doe', 'john.doe@example.com', false, true, NOW()),
('pbkdf2_sha256$600000$YQAb7oAI2HyNqQe0kWe5WG$QX5nCLmZBNhJ1LFvTbOv4fOuJMu4I2BcHhOcwGxm5nM=', NULL, false, 'janesmith', 'Jane', 'Smith', 'jane.smith@example.com', false, true, NOW()),
('pbkdf2_sha256$600000$YQAb7oAI2HyNqQe0kWe5WG$QX5nCLmZBNhJ1LFvTbOv4fOuJMu4I2BcHhOcwGxm5nM=', NULL, false, 'bobwilson', 'Bob', 'Wilson', 'bob.wilson@example.com', false, true, NOW()),
('pbkdf2_sha256$600000$YQAb7oAI2HyNqQe0kWe5WG$QX5nCLmZBNhJ1LFvTbOv4fOuJMu4I2BcHhOcwGxm5nM=', NULL, false, 'alicebrown', 'Alice', 'Brown', 'alice.brown@example.com', false, true, NOW()),
('pbkdf2_sha256$600000$YQAb7oAI2HyNqQe0kWe5WG$QX5nCLmZBNhJ1LFvTbOv4fOuJMu4I2BcHhOcwGxm5nM=', NULL, false, 'charliedavis', 'Charlie', 'Davis', 'charlie.davis@example.com', false, true, NOW()),
('pbkdf2_sha256$600000$YQAb7oAI2HyNqQe0kWe5WG$QX5nCLmZBNhJ1LFvTbOv4fOuJMu4I2BcHhOcwGxm5nM=', NULL, false, 'sarahjones', 'Sarah', 'Jones', 'sarah.jones@example.com', false, true, NOW()),
('pbkdf2_sha256$600000$YQAb7oAI2HyNqQe0kWe5WG$QX5nCLmZBNhJ1LFvTbOv4fOuJMu4I2BcHhOcwGxm5nM=', NULL, false, 'mikethompson', 'Mike', 'Thompson', 'mike.thompson@example.com', false, true, NOW())
ON CONFLICT (email) DO NOTHING;

-- Insert sample addresses
INSERT INTO users_address (user_id, first_name, last_name, address_line_1, address_line_2, city, postal_code, country, phone_number, is_default) VALUES
((SELECT id FROM users_user WHERE email = 'john.doe@example.com'), 'John', 'Doe', '123 Main Street', 'Apt 4B', 'New York', '10001', 'United States', '+1-555-0101', true),
((SELECT id FROM users_user WHERE email = 'jane.smith@example.com'), 'Jane', 'Smith', '456 Oak Avenue', '', 'Los Angeles', '90210', 'United States', '+1-555-0102', true),
((SELECT id FROM users_user WHERE email = 'bob.wilson@example.com'), 'Bob', 'Wilson', '789 Pine Road', 'Suite 300', 'Chicago', '60601', 'United States', '+1-555-0103', true),
((SELECT id FROM users_user WHERE email = 'alice.brown@example.com'), 'Alice', 'Brown', '321 Elm Street', '', 'Houston', '77001', 'United States', '+1-555-0104', true),
((SELECT id FROM users_user WHERE email = 'charlie.davis@example.com'), 'Charlie', 'Davis', '654 Maple Drive', 'Unit 12', 'Phoenix', '85001', 'United States', '+1-555-0105', true),
((SELECT id FROM users_user WHERE email = 'sarah.jones@example.com'), 'Sarah', 'Jones', '987 Cedar Lane', '', 'Miami', '33101', 'United States', '+1-555-0106', true),
((SELECT id FROM users_user WHERE email = 'mike.thompson@example.com'), 'Mike', 'Thompson', '147 Birch Avenue', 'Floor 2', 'Seattle', '98101', 'United States', '+1-555-0107', true);

-- Insert categories
INSERT INTO catalog_category (name, slug, created_at) VALUES
('Electronics', 'electronics', NOW()),
('Clothing & Fashion', 'clothing-fashion', NOW()),
('Home & Garden', 'home-garden', NOW()),
('Sports & Outdoors', 'sports-outdoors', NOW()),
('Books & Media', 'books-media', NOW()),
('Health & Beauty', 'health-beauty', NOW()),
('Toys & Games', 'toys-games', NOW()),
('Automotive', 'automotive', NOW())
ON CONFLICT (name) DO NOTHING;

-- Insert sample products
INSERT INTO catalog_product (name, description, price, stock_quantity, category_id, is_active, image_url, created_at, updated_at) VALUES
('Wireless Bluetooth Headphones', 'Premium noise-canceling wireless headphones with 30-hour battery life', 149.99, 50, (SELECT id FROM catalog_category WHERE name = 'Electronics'), true, 'products/headphones1.jpg', NOW(), NOW()),
('Gaming Mechanical Keyboard', 'RGB backlit mechanical gaming keyboard with Cherry MX switches', 89.99, 75, (SELECT id FROM catalog_category WHERE name = 'Electronics'), true, 'products/keyboard1.jpg', NOW(), NOW()),
('Smartphone Case', 'Durable protective case for smartphones with shock absorption', 19.99, 200, (SELECT id FROM catalog_category WHERE name = 'Electronics'), true, 'products/case1.jpg', NOW(), NOW()),
('Leather Jacket', 'Premium genuine leather jacket in classic black', 199.99, 25, (SELECT id FROM catalog_category WHERE name = 'Clothing'), true, 'products/jacket1.jpg', NOW(), NOW()),
('Cotton T-Shirt', 'Comfortable 100% cotton t-shirt available in multiple colors', 24.99, 150, (SELECT id FROM catalog_category WHERE name = 'Clothing'), true, 'products/tshirt1.jpg', NOW(), NOW()),
('Running Sneakers', 'Lightweight running shoes with advanced cushioning technology', 129.99, 100, (SELECT id FROM catalog_category WHERE name = 'Clothing'), true, 'products/sneakers1.jpg', NOW(), NOW()),
('Bestselling Novel', 'Award-winning fiction novel by renowned author', 14.99, 300, (SELECT id FROM catalog_category WHERE name = 'Books'), true, 'products/book1.jpg', NOW(), NOW()),
('Programming Guide', 'Comprehensive guide to modern web development', 39.99, 80, (SELECT id FROM catalog_category WHERE name = 'Books'), true, 'products/book2.jpg', NOW(), NOW()),
('Cook Book Collection', 'Professional chef recipes and cooking techniques', 29.99, 120, (SELECT id FROM catalog_category WHERE name = 'Books'), true, 'products/cookbook1.jpg', NOW(), NOW()),
('Yoga Mat', 'Non-slip exercise yoga mat with carrying strap', 34.99, 90, (SELECT id FROM catalog_category WHERE name = 'Sports'), true, 'products/yogamat1.jpg', NOW(), NOW()),
('Dumbbell Set', 'Adjustable dumbbell set for home gym workouts', 249.99, 35, (SELECT id FROM catalog_category WHERE name = 'Sports'), true, 'products/dumbbells1.jpg', NOW(), NOW()),
('Tennis Racket', 'Professional grade tennis racket for competitive play', 159.99, 60, (SELECT id FROM catalog_category WHERE name = 'Sports'), true, 'products/racket1.jpg', NOW(), NOW()),
('Smart Watch', 'Advanced fitness tracking smartwatch with heart rate monitor', 299.99, 40, (SELECT id FROM catalog_category WHERE name = 'Electronics'), true, 'products/smartwatch1.jpg', NOW(), NOW()),
('Bluetooth Speaker', 'Portable wireless speaker with rich bass and 12-hour battery', 79.99, 85, (SELECT id FROM catalog_category WHERE name = 'Electronics'), true, 'products/speaker1.jpg', NOW(), NOW()),
('Designer Jeans', 'Premium denim jeans with modern fit and styling', 89.99, 70, (SELECT id FROM catalog_category WHERE name = 'Clothing'), true, 'products/jeans1.jpg', NOW(), NOW()),
('Winter Jacket', 'Insulated winter jacket for extreme cold weather', 179.99, 45, (SELECT id FROM catalog_category WHERE name = 'Clothing'), true, 'products/winterjacket1.jpg', NOW(), NOW()),
('Science Fiction Novel', 'Thrilling space adventure story with compelling characters', 16.99, 180, (SELECT id FROM catalog_category WHERE name = 'Books'), true, 'products/scifibook1.jpg', NOW(), NOW()),
('History Biography', 'Detailed biography of influential historical figure', 22.99, 95, (SELECT id FROM catalog_category WHERE name = 'Books'), true, 'products/biography1.jpg', NOW(), NOW()),
('Basketball', 'Official size and weight basketball for indoor/outdoor play', 49.99, 110, (SELECT id FROM catalog_category WHERE name = 'Sports'), true, 'products/basketball1.jpg', NOW(), NOW()),
('Fitness Tracker', 'Waterproof fitness band with sleep and activity monitoring', 99.99, 120, (SELECT id FROM catalog_category WHERE name = 'Sports'), true, 'products/fitnesstracker1.jpg', NOW(), NOW());

-- Insert sample carts
INSERT INTO cart_cart (user_id, created_at) VALUES
((SELECT id FROM users_user WHERE email = 'john.doe@email.com'), NOW()),
((SELECT id FROM users_user WHERE email = 'jane.smith@email.com'), NOW()),
((SELECT id FROM users_user WHERE email = 'bob.wilson@email.com'), NOW())
ON CONFLICT DO NOTHING;

-- Insert cart items
INSERT INTO cart_cartitem (cart_id, product_id, quantity) VALUES
((SELECT c.id FROM cart_cart c JOIN users_user u ON c.user_id = u.id WHERE u.email = 'john.doe@example.com'), (SELECT id FROM catalog_product WHERE name = 'Wireless Bluetooth Headphones'), 1),
((SELECT c.id FROM cart_cart c JOIN users_user u ON c.user_id = u.id WHERE u.email = 'john.doe@example.com'), (SELECT id FROM catalog_product WHERE name = 'Gaming Mechanical Keyboard'), 1),
((SELECT c.id FROM cart_cart c JOIN users_user u ON c.user_id = u.id WHERE u.email = 'jane.smith@example.com'), (SELECT id FROM catalog_product WHERE name = 'Cotton T-Shirt'), 2),
((SELECT c.id FROM cart_cart c JOIN users_user u ON c.user_id = u.id WHERE u.email = 'jane.smith@example.com'), (SELECT id FROM catalog_product WHERE name = 'Running Sneakers'), 1),
((SELECT c.id FROM cart_cart c JOIN users_user u ON c.user_id = u.id WHERE u.email = 'bob.wilson@example.com'), (SELECT id FROM catalog_product WHERE name = 'Bluetooth Speaker'), 1),
((SELECT c.id FROM cart_cart c JOIN users_user u ON c.user_id = u.id WHERE u.email = 'bob.wilson@example.com'), (SELECT id FROM catalog_product WHERE name = 'Yoga Mat'), 2);

-- Insert sample orders
INSERT INTO orders_order (user_id, status, payment_status, total_amount, created_at, updated_at) VALUES
((SELECT id FROM users_user WHERE email = 'john.doe@example.com'), 'completed', 'paid', 239.98, NOW() - INTERVAL '5 days', NOW() - INTERVAL '5 days'),
((SELECT id FROM users_user WHERE email = 'jane.smith@example.com'), 'completed', 'paid', 154.98, NOW() - INTERVAL '3 days', NOW() - INTERVAL '3 days'),
((SELECT id FROM users_user WHERE email = 'bob.wilson@example.com'), 'pending', 'unpaid', 79.99, NOW() - INTERVAL '1 day', NOW() - INTERVAL '1 day'),
((SELECT id FROM users_user WHERE email = 'alice.brown@example.com'), 'completed', 'paid', 184.97, NOW() - INTERVAL '7 days', NOW() - INTERVAL '7 days'),
((SELECT id FROM users_user WHERE email = 'charlie.davis@example.com'), 'processing', 'paid', 299.99, NOW() - INTERVAL '2 days', NOW() - INTERVAL '2 days'),
((SELECT id FROM users_user WHERE email = 'sarah.jones@example.com'), 'shipped', 'paid', 129.99, NOW() - INTERVAL '4 days', NOW() - INTERVAL '4 days'),
((SELECT id FROM users_user WHERE email = 'mike.thompson@example.com'), 'delivered', 'paid', 89.99, NOW() - INTERVAL '6 days', NOW() - INTERVAL '6 days');

-- Insert order items
INSERT INTO orders_orderitem (order_id, product_id, quantity, unit_price, subtotal) VALUES
-- John's order
((SELECT o.id FROM orders_order o JOIN users_user u ON o.user_id = u.id WHERE u.email = 'john.doe@example.com' AND o.total_amount = 239.98), (SELECT id FROM catalog_product WHERE name = 'Wireless Bluetooth Headphones'), 1, 149.99, 149.99),
((SELECT o.id FROM orders_order o JOIN users_user u ON o.user_id = u.id WHERE u.email = 'john.doe@example.com' AND o.total_amount = 239.98), (SELECT id FROM catalog_product WHERE name = 'Gaming Mechanical Keyboard'), 1, 89.99, 89.99),
-- Jane's order
((SELECT o.id FROM orders_order o JOIN users_user u ON o.user_id = u.id WHERE u.email = 'jane.smith@example.com'), (SELECT id FROM catalog_product WHERE name = 'Cotton T-Shirt'), 2, 24.99, 49.98),
((SELECT o.id FROM orders_order o JOIN users_user u ON o.user_id = u.id WHERE u.email = 'jane.smith@example.com'), (SELECT id FROM catalog_product WHERE name = 'Running Sneakers'), 1, 129.99, 129.99),
((SELECT o.id FROM orders_order o JOIN users_user u ON o.user_id = u.id WHERE u.email = 'jane.smith@example.com'), (SELECT id FROM catalog_product WHERE name = 'Cotton T-Shirt'), 1, 24.99, 24.99),
-- Bob's order
((SELECT o.id FROM orders_order o JOIN users_user u ON o.user_id = u.id WHERE u.email = 'bob.wilson@example.com'), (SELECT id FROM catalog_product WHERE name = 'Bluetooth Speaker'), 1, 79.99, 79.99),
-- Alice's order
((SELECT o.id FROM orders_order o JOIN users_user u ON o.user_id = u.id WHERE u.email = 'alice.brown@example.com'), (SELECT id FROM catalog_product WHERE name = 'Yoga Mat'), 2, 34.99, 69.98),
((SELECT o.id FROM orders_order o JOIN users_user u ON o.user_id = u.id WHERE u.email = 'alice.brown@example.com'), (SELECT id FROM catalog_product WHERE name = 'Programming Guide'), 1, 39.99, 39.99),
((SELECT o.id FROM orders_order o JOIN users_user u ON o.user_id = u.id WHERE u.email = 'alice.brown@example.com'), (SELECT id FROM catalog_product WHERE name = 'Cotton T-Shirt'), 3, 24.99, 74.97),
-- Charlie's order
((SELECT o.id FROM orders_order o JOIN users_user u ON o.user_id = u.id WHERE u.email = 'charlie.davis@example.com'), (SELECT id FROM catalog_product WHERE name = 'Smart Watch'), 1, 299.99, 299.99),
-- Sarah's order
((SELECT o.id FROM orders_order o JOIN users_user u ON o.user_id = u.id WHERE u.email = 'sarah.jones@example.com'), (SELECT id FROM catalog_product WHERE name = 'Running Sneakers'), 1, 129.99, 129.99),
-- Mike's order
((SELECT o.id FROM orders_order o JOIN users_user u ON o.user_id = u.id WHERE u.email = 'mike.thompson@example.com'), (SELECT id FROM catalog_product WHERE name = 'Designer Jeans'), 1, 89.99, 89.99);

-- Insert sample reviews
INSERT INTO reviews_review (user_id, product_id, rating, comment, created_at) VALUES
((SELECT id FROM users_user WHERE email = 'john.doe@example.com'), (SELECT id FROM catalog_product WHERE name = 'Wireless Bluetooth Headphones'), 5, 'Excellent headphones! The sound quality is amazing and the battery life is outstanding.', NOW() - INTERVAL '3 days'),
((SELECT id FROM users_user WHERE email = 'john.doe@example.com'), (SELECT id FROM catalog_product WHERE name = 'Gaming Mechanical Keyboard'), 5, 'Best keyboard I''ve ever owned. The keys are responsive and the RGB lighting is great.', NOW() - INTERVAL '3 days'),
((SELECT id FROM users_user WHERE email = 'jane.smith@example.com'), (SELECT id FROM catalog_product WHERE name = 'Cotton T-Shirt'), 4, 'Comfortable shirt with good quality fabric. Fits perfectly and colors are vibrant.', NOW() - INTERVAL '2 days'),
((SELECT id FROM users_user WHERE email = 'jane.smith@example.com'), (SELECT id FROM catalog_product WHERE name = 'Running Sneakers'), 5, 'Super comfortable for running. Great support and cushioning for long distances.', NOW() - INTERVAL '2 days'),
((SELECT id FROM users_user WHERE email = 'bob.wilson@example.com'), (SELECT id FROM catalog_product WHERE name = 'Bluetooth Speaker'), 4, 'Great sound quality and the battery lasts all day. Perfect for outdoor activities.', NOW() - INTERVAL '1 day'),
((SELECT id FROM users_user WHERE email = 'alice.brown@example.com'), (SELECT id FROM catalog_product WHERE name = 'Yoga Mat'), 5, 'Perfect for my daily yoga practice. Non-slip surface works great even during sweaty sessions.', NOW() - INTERVAL '5 days'),
((SELECT id FROM users_user WHERE email = 'alice.brown@example.com'), (SELECT id FROM catalog_product WHERE name = 'Programming Guide'), 5, 'Excellent book for learning web development. Clear explanations and practical examples.', NOW() - INTERVAL '5 days'),
((SELECT id FROM users_user WHERE email = 'charlie.davis@example.com'), (SELECT id FROM catalog_product WHERE name = 'Smart Watch'), 4, 'Great fitness tracking features and the display is crisp. Battery could last longer though.', NOW() - INTERVAL '10 days'),
((SELECT id FROM users_user WHERE email = 'sarah.jones@example.com'), (SELECT id FROM catalog_product WHERE name = 'Basketball'), 5, 'Great quality basketball. Perfect grip and bounces well on different surfaces.', NOW() - INTERVAL '8 days'),
((SELECT id FROM users_user WHERE email = 'mike.thompson@example.com'), (SELECT id FROM catalog_product WHERE name = 'Designer Jeans'), 4, 'Good quality denim with excellent fit. Worth the price for the comfort and style.', NOW() - INTERVAL '6 days'),
((SELECT id FROM users_user WHERE email = 'sarah.jones@example.com'), (SELECT id FROM catalog_product WHERE name = 'Bestselling Novel'), 5, 'Engaging story that kept me hooked from start to finish. Highly recommend!', NOW() - INTERVAL '4 days'),
((SELECT id FROM users_user WHERE email = 'mike.thompson@example.com'), (SELECT id FROM catalog_product WHERE name = 'Fitness Tracker'), 4, 'Good value for money. Tracks steps and sleep well, though the heart rate monitor could be more accurate.', NOW() - INTERVAL '3 days');

-- Update sequences to continue from current max values
SELECT setval('users_user_id_seq', (SELECT MAX(id) FROM users_user));
SELECT setval('users_address_id_seq', (SELECT MAX(id) FROM users_address));
SELECT setval('catalog_category_id_seq', (SELECT MAX(id) FROM catalog_category));
SELECT setval('catalog_product_id_seq', (SELECT MAX(id) FROM catalog_product));
SELECT setval('cart_cart_id_seq', (SELECT MAX(id) FROM cart_cart));
SELECT setval('cart_cartitem_id_seq', (SELECT MAX(id) FROM cart_cartitem));
SELECT setval('orders_order_id_seq', (SELECT MAX(id) FROM orders_order));
SELECT setval('orders_orderitem_id_seq', (SELECT MAX(id) FROM orders_orderitem));
SELECT setval('reviews_review_id_seq', (SELECT MAX(id) FROM reviews_review));

-- Create some helpful views for reporting
CREATE OR REPLACE VIEW order_summary AS
SELECT 
    o.id as order_id,
    u.email,
    u.first_name || ' ' || u.last_name as customer_name,
    o.status,
    o.payment_status,
    o.total_amount,
    o.created_at as order_date,
    COUNT(oi.id) as item_count
FROM orders_order o
JOIN users_user u ON o.user_id = u.id
LEFT JOIN orders_orderitem oi ON o.id = oi.order_id
GROUP BY o.id, u.email, u.first_name, u.last_name, o.status, o.payment_status, o.total_amount, o.created_at
ORDER BY o.created_at DESC;

CREATE OR REPLACE VIEW product_stats AS
SELECT 
    p.id,
    p.name,
    c.name as category,
    p.price,
    p.stock_quantity,
    COALESCE(AVG(r.rating), 0) as avg_rating,
    COUNT(r.id) as review_count,
    COALESCE(SUM(oi.quantity), 0) as total_sold
FROM catalog_product p
LEFT JOIN catalog_category c ON p.category_id = c.id
LEFT JOIN reviews_review r ON p.id = r.product_id
LEFT JOIN orders_orderitem oi ON p.id = oi.product_id
GROUP BY p.id, p.name, c.name, p.price, p.stock_quantity
ORDER BY total_sold DESC;

-- Create indexes for better performance on the new data
CREATE INDEX IF NOT EXISTS idx_orders_order_created_at ON orders_order(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_reviews_review_created_at ON reviews_review(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_cart_cartitem_cart_product ON cart_cartitem(cart_id, product_id);

COMMENT ON VIEW order_summary IS 'Summary view of orders with customer information';
COMMENT ON VIEW product_stats IS 'Product statistics including ratings and sales data';

-- Display summary of inserted data
SELECT 
    'Users' as entity, COUNT(*) as count FROM users_user
UNION ALL
SELECT 'Categories', COUNT(*) FROM catalog_category
UNION ALL
SELECT 'Products', COUNT(*) FROM catalog_product
UNION ALL
SELECT 'Orders', COUNT(*) FROM orders_order
UNION ALL
SELECT 'Reviews', COUNT(*) FROM reviews_review
UNION ALL
SELECT 'Cart Items', COUNT(*) FROM cart_cartitem;

-- Note: Default password for all users is 'userpass123' (except admin which is 'admin123')
-- The password hash used is a placeholder - in real Django, passwords should be properly hashed
