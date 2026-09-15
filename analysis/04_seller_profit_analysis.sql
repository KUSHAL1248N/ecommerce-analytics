USE ecommerce_analytics;

-- 1. Seller revenue
SELECT
    s.seller_id,
    s.seller_name,
    SUM(oi.quantity * oi.unit_price) AS revenue
FROM sellers s
JOIN products p
    ON s.seller_id = p.seller_id
JOIN order_items oi
    ON p.product_id = oi.product_id
JOIN orders o
    ON oi.order_id = o.order_id
WHERE o.status = 'Delivered'
GROUP BY s.seller_id, s.seller_name
ORDER BY revenue DESC;


-- 2. Seller profit
SELECT
    s.seller_id,
    s.seller_name,
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
GROUP BY s.seller_id, s.seller_name
ORDER BY profit DESC;


-- 3. Product profit
SELECT
    p.product_id,
    p.product_name,
    SUM(oi.quantity) AS units_sold,
    SUM(
        oi.quantity * (p.price - p.cost_price)
    ) AS profit
FROM products p
JOIN order_items oi
    ON p.product_id = oi.product_id
JOIN orders o
    ON oi.order_id = o.order_id
WHERE o.status = 'Delivered'
GROUP BY p.product_id, p.product_name
ORDER BY profit DESC;


-- 4. Top 5 products by profit margin
SELECT
    p.product_name,
    p.price,
    p.cost_price,
    ROUND(
        ((p.price - p.cost_price) / p.price) * 100,
        2
    ) AS profit_margin_percent
FROM products p
ORDER BY profit_margin_percent DESC
LIMIT 5;


-- 5. Seller performance
SELECT
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
GROUP BY s.seller_id, s.seller_name
ORDER BY profit DESC;