USE ecommerce_analytics;

-- ============================================
-- 1. PRODUCT SALES
-- ============================================

SELECT
    p.product_id,
    p.product_name,
    SUM(oi.quantity) AS units_sold,
    SUM(oi.quantity * oi.unit_price) AS revenue
FROM products p
JOIN order_items oi
    ON p.product_id = oi.product_id
JOIN orders o
    ON oi.order_id = o.order_id
WHERE o.status = 'Delivered'
GROUP BY
    p.product_id,
    p.product_name
ORDER BY revenue DESC;


-- ============================================
-- 2. TOP 5 PRODUCTS BY REVENUE
-- ============================================

SELECT
    p.product_name,
    SUM(oi.quantity * oi.unit_price) AS revenue
FROM products p
JOIN order_items oi
    ON p.product_id = oi.product_id
JOIN orders o
    ON oi.order_id = o.order_id
WHERE o.status = 'Delivered'
GROUP BY
    p.product_id,
    p.product_name
ORDER BY revenue DESC
LIMIT 5;


-- ============================================
-- 3. TOP 5 PRODUCTS BY UNITS SOLD
-- ============================================

SELECT
    p.product_name,
    SUM(oi.quantity) AS units_sold
FROM products p
JOIN order_items oi
    ON p.product_id = oi.product_id
JOIN orders o
    ON oi.order_id = o.order_id
WHERE o.status = 'Delivered'
GROUP BY
    p.product_id,
    p.product_name
ORDER BY units_sold DESC
LIMIT 5;


-- ============================================
-- 4. REVENUE BY CATEGORY
-- ============================================

SELECT
    c.category_name,
    SUM(oi.quantity * oi.unit_price) AS revenue
FROM categories c
JOIN products p
    ON c.category_id = p.category_id
JOIN order_items oi
    ON p.product_id = oi.product_id
JOIN orders o
    ON oi.order_id = o.order_id
WHERE o.status = 'Delivered'
GROUP BY
    c.category_id,
    c.category_name
ORDER BY revenue DESC;


-- ============================================
-- 5. AVERAGE PRODUCT RATING
-- ============================================

SELECT
    p.product_name,
    ROUND(AVG(r.rating), 2) AS average_rating,
    COUNT(r.review_id) AS review_count
FROM products p
LEFT JOIN reviews r
    ON p.product_id = r.product_id
GROUP BY
    p.product_id,
    p.product_name
HAVING COUNT(r.review_id) > 0
ORDER BY average_rating DESC;


-- ============================================
-- 6. PRODUCTS WITH LOW STOCK
-- ============================================

SELECT
    p.product_id,
    p.product_name,
    i.stock_quantity,
    i.reorder_level
FROM products p
JOIN inventory i
    ON p.product_id = i.product_id
WHERE i.stock_quantity <= i.reorder_level
ORDER BY i.stock_quantity;