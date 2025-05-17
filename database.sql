-- Create the database if it doesn't exist
CREATE DATABASE IF NOT EXISTS foodexpress CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE foodexpress;

-- Create the tables
CREATE TABLE IF NOT EXISTS user (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    password_hash VARCHAR(128) NOT NULL,
    address VARCHAR(200),
    contact VARCHAR(20),
    is_admin BOOLEAN DEFAULT FALSE,
    date_joined DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS categories (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) NOT NULL
);

CREATE TABLE IF NOT EXISTS menu_items (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    price FLOAT NOT NULL,
    image_url VARCHAR(200) DEFAULT 'default-food.jpg',
    available BOOLEAN DEFAULT TRUE,
    category_id INT NOT NULL,
    FOREIGN KEY (category_id) REFERENCES categories(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS cart_items (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    menu_item_id INT NOT NULL,
    quantity INT DEFAULT 1,
    date_added DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES user(id) ON DELETE CASCADE,
    FOREIGN KEY (menu_item_id) REFERENCES menu_items(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS orders (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    order_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    total FLOAT NOT NULL,
    status VARCHAR(20) DEFAULT 'pending',
    delivery_address VARCHAR(200) NOT NULL,
    contact VARCHAR(20) NOT NULL,
    delivery_option VARCHAR(20) NOT NULL,
    special_instructions TEXT,
    FOREIGN KEY (user_id) REFERENCES user(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS order_items (
    id INT AUTO_INCREMENT PRIMARY KEY,
    order_id INT NOT NULL,
    menu_item_id INT NOT NULL,
    quantity INT NOT NULL,
    price FLOAT NOT NULL,
    FOREIGN KEY (order_id) REFERENCES orders(id) ON DELETE CASCADE,
    FOREIGN KEY (menu_item_id) REFERENCES menu_items(id) ON DELETE CASCADE
);

-- Insert default categories
INSERT INTO categories (name) VALUES
    ('Main Dishes'),
    ('Sides'),
    ('Beverages'),
    ('Desserts'),
    ('Salads'),
    ('Sandwiches');

-- Insert sample menu items (at least 15 items across categories)
INSERT INTO menu_items (name, description, price, image_url, category_id, available) VALUES
    -- Main Dishes
    ('Classic Burger', 'Juicy beef patty with fresh vegetables, cheese, and our special sauce', 9.99, 'burger.jpg', 1, TRUE),
    ('Veggie Burger', 'Plant-based patty with fresh vegetables and vegan mayo', 8.99, 'veggie-burger.jpg', 1, TRUE),
    ('Margherita Pizza', 'Traditional pizza with tomato sauce, mozzarella, and basil', 12.99, 'pizza.jpg', 1, TRUE),
    ('Grilled Chicken', 'Herb-marinated chicken breast with roasted vegetables', 11.99, 'grilled-chicken.jpg', 1, TRUE),
    ('Pasta Alfredo', 'Fettuccine pasta with creamy alfredo sauce and parmesan', 10.99, 'pasta.jpg', 1, TRUE),
    
    -- Sides
    ('French Fries', 'Crispy golden fries with seasoning', 3.99, 'fries.jpg', 2, TRUE),
    ('Onion Rings', 'Crispy battered onion rings with dipping sauce', 4.99, 'onion-rings.jpg', 2, TRUE),
    ('Garlic Bread', 'Toasted bread with garlic butter and herbs', 3.49, 'garlic-bread.jpg', 2, TRUE),
    
    -- Beverages
    ('Cola', 'Refreshing cola drink', 1.99, 'cola.jpg', 3, TRUE),
    ('Lemonade', 'Freshly squeezed lemonade with mint', 2.99, 'lemonade.jpg', 3, TRUE),
    ('Iced Tea', 'Homemade iced tea with lemon', 2.49, 'iced-tea.jpg', 3, TRUE),
    
    -- Desserts
    ('Chocolate Cake', 'Decadent chocolate cake with frosting', 5.99, 'cake.jpg', 4, TRUE),
    ('Cheesecake', 'New York style cheesecake with berry compote', 6.99, 'cheesecake.jpg', 4, TRUE),
    
    -- Salads
    ('Caesar Salad', 'Romaine lettuce with caesar dressing, croutons, and parmesan', 7.99, 'caesar-salad.jpg', 5, TRUE),
    ('Greek Salad', 'Fresh vegetables, feta cheese, and olives with vinaigrette', 8.49, 'greek-salad.jpg', 5, TRUE),
    
    -- Sandwiches
    ('Club Sandwich', 'Triple-decker sandwich with chicken, bacon, lettuce, and tomato', 9.49, 'club-sandwich.jpg', 6, TRUE);

-- Insert admin users (at least 2)
INSERT INTO user (username, email, password_hash, address, contact, is_admin) VALUES
    ('admin', 'admin@foodexpress.com', 'pbkdf2:sha256:260000$vy1aBMEzaekOB9wW$eb82e50cfb6e7a9567a513c8c581074126a7ded87d5ff64030621dab79911772', '123 Admin Street, Downtown', '555-123-4567', TRUE),
    ('manager', 'manager@foodexpress.com', 'pbkdf2:sha256:260000$vy1aBMEzaekOB9wW$eb82e50cfb6e7a9567a513c8c581074126a7ded87d5ff64030621dab79911772', '456 Manager Avenue, Uptown', '555-987-6543', TRUE);

-- Insert regular users (at least 4)
INSERT INTO user (username, email, password_hash, address, contact, is_admin) VALUES
    ('john_doe', 'john@example.com', 'pbkdf2:sha256:260000$vy1aBMEzaekOB9wW$eb82e50cfb6e7a9567a513c8c581074126a7ded87d5ff64030621dab79911772', '789 Oak Street, Suburb', '555-111-2222', FALSE),
    ('jane_smith', 'jane@example.com', 'pbkdf2:sha256:260000$vy1aBMEzaekOB9wW$eb82e50cfb6e7a9567a513c8c581074126a7ded87d5ff64030621dab79911772', '101 Pine Avenue, Westside', '555-333-4444', FALSE),
    ('bob_johnson', 'bob@example.com', 'pbkdf2:sha256:260000$vy1aBMEzaekOB9wW$eb82e50cfb6e7a9567a513c8c581074126a7ded87d5ff64030621dab79911772', '202 Maple Drive, Eastside', '555-555-6666', FALSE),
    ('sarah_wilson', 'sarah@example.com', 'pbkdf2:sha256:260000$vy1aBMEzaekOB9wW$eb82e50cfb6e7a9567a513c8c581074126a7ded87d5ff64030621dab79911772', '303 Cedar Lane, Northside', '555-777-8888', FALSE);

-- Insert sample orders with different delivery options (at least 3)
INSERT INTO orders (user_id, total, status, delivery_address, contact, delivery_option, special_instructions) VALUES
    (3, 28.96, 'completed', '789 Oak Street, Suburb', '555-111-2222', 'express', 'Please ring doorbell upon arrival'),
    (4, 18.47, 'pending', '101 Pine Avenue, Westside', '555-333-4444', 'standard', 'Leave at the door'),
    (5, 14.98, 'processing', '202 Maple Drive, Eastside', '555-555-6666', 'pickup', 'Will pick up around 6 PM');

-- Insert order items for the first order
INSERT INTO order_items (order_id, menu_item_id, quantity, price) VALUES
    (1, 1, 2, 9.99),  -- 2 Classic Burgers
    (1, 6, 1, 3.99),  -- 1 French Fries
    (1, 9, 2, 1.99);  -- 2 Colas

-- Insert order items for the second order
INSERT INTO order_items (order_id, menu_item_id, quantity, price) VALUES
    (2, 3, 1, 12.99), -- 1 Margherita Pizza
    (2, 10, 1, 2.99); -- 1 Lemonade

-- Insert order items for the third order
INSERT INTO order_items (order_id, menu_item_id, quantity, price) VALUES
    (3, 14, 1, 7.99),  -- 1 Caesar Salad
    (3, 6, 1, 3.99),   -- 1 French Fries
    (3, 11, 1, 2.49);  -- 1 Iced Tea

-- Create a view for quick access to cart with product information
CREATE OR REPLACE VIEW cart_view AS
SELECT 
    ci.id, 
    ci.user_id, 
    ci.menu_item_id, 
    ci.quantity, 
    mi.name, 
    mi.price, 
    (mi.price * ci.quantity) AS total_price,
    mi.image_url
FROM cart_items ci
JOIN menu_items mi ON ci.menu_item_id = mi.id;

-- Create a view for order summaries
CREATE OR REPLACE VIEW order_summary AS
SELECT 
    o.id,
    o.user_id,
    u.username,
    u.email,
    o.order_date,
    o.total,
    o.status,
    o.delivery_option,
    COUNT(oi.id) AS item_count,
    SUM(oi.quantity) AS total_items
FROM orders o
JOIN user u ON o.user_id = u.id
JOIN order_items oi ON o.id = oi.order_id
GROUP BY o.id;

-- Instructions for client
-- 1. Create a MySQL database
-- 2. Run this script to set up all necessary tables and sample data
-- 3. Update the .env file with your database credentials
-- 4. Install required Python packages using: pip install -r requirements.txt
-- 5. Run the application using: python run.py
-- 6. Access the application at: http://localhost:5000
--
-- Default Admin Login:
-- Email: admin@foodexpress.com
-- Password: admin123
--
-- Default User Login:
-- Email: john@example.com
-- Password: admin123