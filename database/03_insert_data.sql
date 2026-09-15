USE ecommerce_analytics;

-- ============================================
-- 1. CATEGORIES
-- ============================================

INSERT INTO categories (category_name) VALUES
('Electronics'),
('Fashion'),
('Home & Kitchen'),
('Books'),
('Beauty'),
('Sports'),
('Grocery'),
('Accessories');


-- ============================================
-- 2. SELLERS
-- ============================================

INSERT INTO sellers
(seller_name, email, city, rating)
VALUES
('TechWorld India', 'techworld@gmail.com', 'Kolkata', 4.60),
('StyleHub', 'stylehub@gmail.com', 'Mumbai', 4.30),
('HomeNeeds', 'homeneeds@gmail.com', 'Delhi', 4.50),
('BookMart', 'bookmart@gmail.com', 'Bangalore', 4.70),
('BeautyCare Store', 'beautycare@gmail.com', 'Pune', 4.20),
('SportZone', 'sportzone@gmail.com', 'Chennai', 4.40),
('FreshBasket', 'freshbasket@gmail.com', 'Kolkata', 4.10),
('AccessoryWorld', 'accessoryworld@gmail.com', 'Hyderabad', 4.35);


-- ============================================
-- 3. CUSTOMERS
-- ============================================

INSERT INTO customers
(first_name, last_name, email, phone, city, registration_date)
VALUES
('Aarav', 'Sharma', 'aarav.sharma@gmail.com', '9876500001', 'Kolkata', '2025-01-15'),
('Priya', 'Das', 'priya.das@gmail.com', '9876500002', 'Mumbai', '2025-02-10'),
('Rahul', 'Roy', 'rahul.roy@gmail.com', '9876500003', 'Delhi', '2025-02-25'),
('Sneha', 'Sen', 'sneha.sen@gmail.com', '9876500004', 'Kolkata', '2025-03-12'),
('Arjun', 'Patel', 'arjun.patel@gmail.com', '9876500005', 'Ahmedabad', '2025-03-20'),
('Ananya', 'Gupta', 'ananya.gupta@gmail.com', '9876500006', 'Bangalore', '2025-04-05'),
('Rohan', 'Mehta', 'rohan.mehta@gmail.com', '9876500007', 'Pune', '2025-04-18'),
('Ishita', 'Ghosh', 'ishita.ghosh@gmail.com', '9876500008', 'Kolkata', '2025-05-01'),
('Vikram', 'Singh', 'vikram.singh@gmail.com', '9876500009', 'Jaipur', '2025-05-15'),
('Neha', 'Verma', 'neha.verma@gmail.com', '9876500010', 'Delhi', '2025-05-28'),
('Aditya', 'Bose', 'aditya.bose@gmail.com', '9876500011', 'Kolkata', '2025-06-10'),
('Riya', 'Chatterjee', 'riya.chatterjee@gmail.com', '9876500012', 'Chennai', '2025-06-22'),
('Kunal', 'Shah', 'kunal.shah@gmail.com', '9876500013', 'Mumbai', '2025-07-05'),
('Tanya', 'Malhotra', 'tanya.malhotra@gmail.com', '9876500014', 'Delhi', '2025-07-18'),
('Sourav', 'Dutta', 'sourav.dutta@gmail.com', '9876500015', 'Kolkata', '2025-08-01'),
('Meera', 'Iyer', 'meera.iyer@gmail.com', '9876500016', 'Bangalore', '2025-08-15'),
('Amit', 'Kumar', 'amit.kumar@gmail.com', '9876500017', 'Patna', '2025-09-02'),
('Pooja', 'Nair', 'pooja.nair@gmail.com', '9876500018', 'Kochi', '2025-09-20'),
('Sahil', 'Agarwal', 'sahil.agarwal@gmail.com', '9876500019', 'Hyderabad', '2025-10-05'),
('Moumita', 'Basu', 'moumita.basu@gmail.com', '9876500020', 'Kolkata', '2025-10-20');


-- ============================================
-- 4. PRODUCTS
-- ============================================

INSERT INTO products
(product_name, category_id, seller_id, price, cost_price)
VALUES
('Wireless Headphones', 1, 1, 2499.00, 1600.00),
('Bluetooth Speaker', 1, 1, 1999.00, 1200.00),
('Mechanical Keyboard', 1, 1, 3499.00, 2400.00),
('Wireless Mouse', 1, 1, 899.00, 500.00),
('USB-C Charger', 1, 1, 1299.00, 750.00),

('Men Cotton T-Shirt', 2, 2, 799.00, 400.00),
('Women Kurti', 2, 2, 1299.00, 700.00),
('Denim Jeans', 2, 2, 1799.00, 1000.00),
('Running Shoes', 2, 2, 2999.00, 1900.00),

('Non-Stick Cookware Set', 3, 3, 2499.00, 1500.00),
('Electric Kettle', 3, 3, 1599.00, 900.00),
('Table Lamp', 3, 3, 999.00, 550.00),

('The Psychology of Money', 4, 4, 499.00, 250.00),
('Atomic Habits', 4, 4, 599.00, 300.00),
('Clean Code', 4, 4, 799.00, 450.00),

('Face Wash', 5, 5, 399.00, 200.00),
('Moisturizer', 5, 5, 599.00, 300.00),
('Sunscreen SPF 50', 5, 5, 699.00, 350.00),

('Yoga Mat', 6, 6, 799.00, 400.00),
('Dumbbell Set', 6, 6, 1999.00, 1200.00),
('Football', 6, 6, 899.00, 500.00),

('Basmati Rice 5kg', 7, 7, 699.00, 500.00),
('Organic Green Tea', 7, 7, 399.00, 220.00),
('Premium Coffee 500g', 7, 7, 599.00, 350.00),

('Smart Watch', 8, 8, 3999.00, 2700.00),
('Laptop Backpack', 8, 8, 1499.00, 850.00),
('Leather Wallet', 8, 8, 999.00, 550.00),
('Travel Bottle', 8, 8, 499.00, 250.00),
('Sunglasses', 8, 8, 1299.00, 700.00);


-- ============================================
-- 5. INVENTORY
-- ============================================

INSERT INTO inventory
(product_id, stock_quantity, reorder_level)
VALUES
(1, 45, 10),
(2, 32, 8),
(3, 20, 5),
(4, 75, 15),
(5, 50, 10),
(6, 100, 20),
(7, 60, 15),
(8, 40, 10),
(9, 25, 8),
(10, 30, 8),
(11, 55, 12),
(12, 80, 15),
(13, 70, 15),
(14, 65, 15),
(15, 25, 5),
(16, 90, 20),
(17, 50, 10),
(18, 35, 8),
(19, 60, 15),
(20, 25, 8),
(21, 40, 10),
(22, 100, 20),
(23, 70, 15),
(24, 45, 10),
(25, 20, 5),
(26, 35, 8),
(27, 50, 10),
(28, 80, 15),
(29, 65, 15);