USE ecommerce_analytics;

INSERT INTO payments
(order_id, payment_date, payment_method, payment_status, amount)
SELECT
    order_id,
    order_date,
    CASE
        WHEN MOD(order_id, 4) = 0 THEN 'UPI'
        WHEN MOD(order_id, 4) = 1 THEN 'Credit Card'
        WHEN MOD(order_id, 4) = 2 THEN 'Debit Card'
        ELSE 'Net Banking'
    END AS payment_method,
    CASE
        WHEN status = 'Cancelled' THEN 'Refunded'
        ELSE 'Completed'
    END AS payment_status,
    total_amount
FROM orders;