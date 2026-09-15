USE ecommerce_analytics;


-- 1. Monthly Revenue View
CREATE OR REPLACE VIEW monthly_revenue AS
SELECT
    DATE_FORMAT(order_date, '%Y-%m') AS month,
    COUNT(*) AS total_orders,
    SUM(total_amount) AS revenue
FROM orders
WHERE status = 'Delivered'
GROUP BY DATE_FORMAT(order_date, '%Y-%m');


-- 2. Customer Lifetime Value View
CREATE OR REPLACE VIEW customer_lifetime_value AS
SELECT
    c.customer_id,
    CONCAT(c.first_name, ' ', c.last_name) AS customer_name,
    c.city,
    COUNT(o.order_id) AS total_orders,
    SUM(o.total_amount) AS lifetime_value
FROM customers c
JOIN orders o
    ON c.customer_id = o.customer_id
WHERE o.status = 'Delivered'
GROUP BY
    c.customer_id,
    c.first_name,
    c.last_name,
    c.city;


-- 3. Product Performance View
CREATE OR REPLACE VIEW product_performance AS
SELECT
    p.product_id,
    p.product_name,
    c.category_name,
    s.seller_name,
    SUM(oi.quantity) AS units_sold,
    SUM(oi.quantity * oi.unit_price) AS revenue,
    SUM(
        oi.quantity * (p.price - p.cost_price)
    ) AS profit
FROM products p
JOIN categories c
    ON p.category_id = c.category_id
JOIN sellers s
    ON p.seller_id = s.seller_id
JOIN order_items oi
    ON p.product_id = oi.product_id
JOIN orders o
    ON oi.order_id = o.order_id
WHERE o.status = 'Delivered'
GROUP BY
    p.product_id,
    p.product_name,
    c.category_name,
    s.seller_name;


-- 4. Seller Performance View
CREATE OR REPLACE VIEW seller_performance AS
SELECT
    s.seller_id,
    s.seller_name,
    COUNT(DISTINCT o.order_id) AS total_orders,
    SUM(oi.quantity * oi.unit_price) AS revenue,
    SUM(
        oi.quantity * (p.price - p.cost_price)
    ) AS profit
FROM sellers s
JOIN products p
    ON s.seller_id = p.seller_id
JOIN order_items oi
    ON p.product_id = oi.product_id
JOIN orders o
    ON oi.order_id = o.order_id
WHERE o.status = 'Delivered'
GROUP BY
    s.seller_id,
    s.seller_name;