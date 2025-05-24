CREATE DATABASE IF NOT EXISTS foodexpress CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE foodexpress;


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


INSERT INTO categories (name) VALUES
    ('Main Dishes'),
    ('Sides'),
    ('Beverages'),
    ('Desserts'),
    ('Salads'),
    ('Sandwiches');


INSERT INTO menu_items (name, description, price, image_url, category_id, available) VALUES
    ('Classic Burger', 'Juicy beef patty with fresh vegetables, cheese, and our special sauce', 9.99, 'burger.jpg', 1, TRUE),
    ('Margherita Pizza', 'Traditional pizza with tomato sauce, mozzarella, and basil', 12.99, 'pizza.jpg', 1, TRUE),
    ('Veggie Burger', 'Plant-based patty with fresh vegetables and vegan mayo', 8.99, 'burger.jpg', 1, TRUE),
    ('French Fries', 'Crispy golden fries with seasoning', 3.99, 'fries.jpg', 2, TRUE),
    ('Cola', 'Refreshing cola drink', 1.99, 'cola.jpg', 3, TRUE),
    ('Chocolate Cake', 'Decadent chocolate cake with frosting', 5.99, 'cake.jpg', 4, TRUE),
    ('Caesar Salad', 'Romaine lettuce with caesar dressing, croutons, and parmesan', 7.99, 'salad.jpg', 5, TRUE),
    ('Club Sandwich', 'Triple-decker sandwich with chicken, bacon, lettuce, and tomato', 9.49, 'sandwich.jpg', 6, TRUE);


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
