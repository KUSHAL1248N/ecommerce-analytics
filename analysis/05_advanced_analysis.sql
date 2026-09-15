USE ecommerce_analytics;


-- 1. Monthly revenue
SELECT
    DATE_FORMAT(order_date, '%Y-%m') AS month,
    SUM(total_amount) AS revenue
FROM orders
WHERE status = 'Delivered'
GROUP BY DATE_FORMAT(order_date, '%Y-%m')
ORDER BY month;


-- 2. Monthly order count
SELECT
    DATE_FORMAT(order_date, '%Y-%m') AS month,
    COUNT(*) AS total_orders
FROM orders
WHERE status = 'Delivered'
GROUP BY DATE_FORMAT(order_date, '%Y-%m')
ORDER BY month;


-- 3. Top customers using RANK()
WITH customer_sales AS (
    SELECT
        c.customer_id,
        CONCAT(c.first_name, ' ', c.last_name) AS customer_name,
        SUM(o.total_amount) AS total_spent
    FROM customers c
    JOIN orders o
        ON c.customer_id = o.customer_id
    WHERE o.status = 'Delivered'
    GROUP BY c.customer_id, c.first_name, c.last_name
)
SELECT
    customer_id,
    customer_name,
    total_spent,
    RANK() OVER (ORDER BY total_spent DESC) AS customer_rank
FROM customer_sales
ORDER BY customer_rank;


-- 4. Product ranking using RANK()
WITH product_sales AS (
    SELECT
        p.product_id,
        p.product_name,
        SUM(oi.quantity * oi.unit_price) AS revenue
    FROM products p
    JOIN order_items oi
        ON p.product_id = oi.product_id
    JOIN orders o
        ON oi.order_id = o.order_id
    WHERE o.status = 'Delivered'
    GROUP BY p.product_id, p.product_name
)
SELECT
    product_id,
    product_name,
    revenue,
    RANK() OVER (ORDER BY revenue DESC) AS product_rank
FROM product_sales
ORDER BY product_rank;


-- 5. Top product for each category using ROW_NUMBER()
WITH category_products AS (
    SELECT
        c.category_name,
        p.product_name,
        SUM(oi.quantity * oi.unit_price) AS revenue
    FROM categories c
    JOIN products p
        ON c.category_id = p.category_id
    JOIN order_items oi
        ON p.product_id = oi.product_id
    JOIN orders o
        ON oi.order_id = o.order_id
    WHERE o.status = 'Delivered'
    GROUP BY c.category_id, c.category_name,
             p.product_id, p.product_name
),
ranked_products AS (
    SELECT
        category_name,
        product_name,
        revenue,
        ROW_NUMBER() OVER (
            PARTITION BY category_name
            ORDER BY revenue DESC
        ) AS product_rank
    FROM category_products
)
SELECT
    category_name,
    product_name,
    revenue
FROM ranked_products
WHERE product_rank = 1
ORDER BY category_name;


-- 6. Month-over-month revenue using LAG()
WITH monthly_sales AS (
    SELECT
        DATE_FORMAT(order_date, '%Y-%m') AS month,
        SUM(total_amount) AS revenue
    FROM orders
    WHERE status = 'Delivered'
    GROUP BY DATE_FORMAT(order_date, '%Y-%m')
)
SELECT
    month,
    revenue,
    LAG(revenue) OVER (ORDER BY month) AS previous_month_revenue,
    revenue - LAG(revenue) OVER (ORDER BY month) AS revenue_change
FROM monthly_sales
ORDER BY month;