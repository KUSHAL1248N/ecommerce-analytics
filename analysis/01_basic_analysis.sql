USE ecommerce_analytics;

-- ============================================
-- 1. TOTAL CUSTOMERS
-- ============================================

SELECT COUNT(*) AS total_customers
FROM customers;


-- ============================================
-- 2. TOTAL PRODUCTS
-- ============================================

SELECT COUNT(*) AS total_products
FROM products;


-- ============================================
-- 3. TOTAL ORDERS
-- ============================================

SELECT COUNT(*) AS total_orders
FROM orders;


-- ============================================
-- 4. ORDERS BY STATUS
-- ============================================

SELECT
    status,
    COUNT(*) AS order_count
FROM orders
GROUP BY status
ORDER BY order_count DESC;


-- ============================================
-- 5. TOTAL REVENUE FROM DELIVERED ORDERS
-- ============================================

SELECT
    SUM(total_amount) AS total_revenue
FROM orders
WHERE status = 'Delivered';


-- ============================================
-- 6. AVERAGE ORDER VALUE
-- ============================================

SELECT
    ROUND(AVG(total_amount), 2) AS average_order_value
FROM orders
WHERE status = 'Delivered';


-- ============================================
-- 7. TOTAL ITEMS SOLD
-- ============================================

SELECT
    SUM(quantity) AS total_items_sold
FROM order_items oi
JOIN orders o
    ON oi.order_id = o.order_id
WHERE o.status = 'Delivered';