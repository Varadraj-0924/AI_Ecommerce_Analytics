-- ============================================================
-- AI-DRIVEN E-COMMERCE SALES, CUSTOMER & BUSINESS ANALYTICS
-- PostgreSQL Business Analysis
-- ============================================================


-- ============================================================
-- 1. OVERALL BUSINESS KPIs
-- ============================================================

-- Total Revenue
SELECT
    ROUND(SUM(price), 2) AS total_revenue
FROM order_items;


-- Total Orders
SELECT
    COUNT(DISTINCT order_id) AS total_orders
FROM orders;


-- Unique Customers
SELECT
    COUNT(DISTINCT customer_unique_id) AS unique_customers
FROM customers;


-- Average Order Value including freight
SELECT
    ROUND(
        AVG(order_total),
        2
    ) AS average_order_value
FROM (
    SELECT
        oi.order_id,
        SUM(oi.price + oi.freight_value) AS order_total
    FROM order_items oi
    GROUP BY oi.order_id
) x;


-- ============================================================
-- 2. MONTHLY REVENUE TREND
-- ============================================================

SELECT
    DATE_TRUNC('month', o.order_purchase_timestamp)::date AS month,
    ROUND(SUM(oi.price), 2) AS revenue
FROM orders o
JOIN order_items oi
    ON o.order_id = oi.order_id
GROUP BY 1
ORDER BY 1;


-- ============================================================
-- 3. MONTHLY ORDERS
-- ============================================================

SELECT
    DATE_TRUNC('month', order_purchase_timestamp)::date AS month,
    COUNT(DISTINCT order_id) AS total_orders
FROM orders
GROUP BY 1
ORDER BY 1;


-- ============================================================
-- 4. TOP 10 PRODUCT CATEGORIES BY REVENUE
-- ============================================================

SELECT
    COALESCE(p.product_category_name, 'Unknown') AS category,
    ROUND(SUM(oi.price), 2) AS revenue
FROM order_items oi
JOIN products p
    ON oi.product_id = p.product_id
GROUP BY 1
ORDER BY revenue DESC
LIMIT 10;


-- ============================================================
-- 5. REVENUE BY CUSTOMER STATE
-- ============================================================

SELECT
    c.customer_state,
    COUNT(DISTINCT o.order_id) AS total_orders,
    ROUND(SUM(oi.price), 2) AS revenue
FROM customers c
JOIN orders o
    ON c.customer_id = o.customer_id
JOIN order_items oi
    ON o.order_id = oi.order_id
GROUP BY c.customer_state
ORDER BY revenue DESC;


-- ============================================================
-- 6. PAYMENT METHOD ANALYSIS
-- ============================================================

SELECT
    payment_type,
    COUNT(DISTINCT order_id) AS total_orders,
    ROUND(SUM(payment_value), 2) AS total_payment_value,
    ROUND(AVG(payment_value), 2) AS average_payment_value
FROM payments
GROUP BY payment_type
ORDER BY total_payment_value DESC;


-- ============================================================
-- 7. CUSTOMER REPEAT PURCHASE ANALYSIS
-- ============================================================

SELECT
    CASE
        WHEN order_count > 1 THEN 'Repeat'
        ELSE 'One-time'
    END AS customer_type,
    COUNT(*) AS customers
FROM (
    SELECT
        c.customer_unique_id,
        COUNT(DISTINCT o.order_id) AS order_count
    FROM customers c
    JOIN orders o
        ON c.customer_id = o.customer_id
    GROUP BY c.customer_unique_id
) x
GROUP BY 1
ORDER BY customers DESC;


-- ============================================================
-- 8. CUSTOMER REVIEW ANALYSIS
-- ============================================================

SELECT
    review_score,
    COUNT(*) AS review_count
FROM reviews
GROUP BY review_score
ORDER BY review_score;


-- Average Review Score
SELECT
    ROUND(AVG(review_score), 2) AS average_review_score
FROM reviews;


-- ============================================================
-- 9. DELIVERY PERFORMANCE
-- ============================================================

SELECT
    CASE
        WHEN order_delivered_customer_date IS NULL
            THEN 'Not Delivered'
        WHEN order_delivered_customer_date
             <= order_estimated_delivery_date
            THEN 'On Time'
        ELSE 'Late'
    END AS delivery_status,
    COUNT(DISTINCT order_id) AS total_orders
FROM orders
GROUP BY 1
ORDER BY total_orders DESC;


-- ============================================================
-- 10. AVERAGE DELIVERY TIME
-- ============================================================

SELECT
    ROUND(
        AVG(
            EXTRACT(
                EPOCH FROM (
                    order_delivered_customer_date
                    - order_purchase_timestamp
                )
            ) / 86400
        ),
        2
    ) AS average_delivery_days
FROM orders
WHERE order_delivered_customer_date IS NOT NULL;


-- ============================================================
-- 11. DELIVERY PERFORMANCE BY STATE
-- ============================================================

SELECT
    c.customer_state,
    ROUND(
        AVG(
            EXTRACT(
                EPOCH FROM (
                    o.order_delivered_customer_date
                    - o.order_purchase_timestamp
                )
            ) / 86400
        ),
        2
    ) AS average_delivery_days
FROM customers c
JOIN orders o
    ON c.customer_id = o.customer_id
WHERE o.order_delivered_customer_date IS NOT NULL
GROUP BY c.customer_state
ORDER BY average_delivery_days DESC;


-- ============================================================
-- 12. TOP SELLERS BY REVENUE
-- ============================================================

SELECT
    oi.seller_id,
    COUNT(DISTINCT oi.order_id) AS total_orders,
    ROUND(SUM(oi.price), 2) AS revenue
FROM order_items oi
GROUP BY oi.seller_id
ORDER BY revenue DESC
LIMIT 10;


-- ============================================================
-- 13. CUSTOMER RFM ANALYSIS
-- ============================================================

CREATE OR REPLACE VIEW customer_rfm AS
SELECT
    c.customer_unique_id,

    DATE '2018-10-17'
        - DATE(MAX(o.order_purchase_timestamp)) AS recency,

    COUNT(DISTINCT o.order_id) AS frequency,

    ROUND(
        SUM(oi.price + oi.freight_value),
        2
    ) AS monetary

FROM customers c
JOIN orders o
    ON c.customer_id = o.customer_id
JOIN order_items oi
    ON o.order_id = oi.order_id

GROUP BY c.customer_unique_id;


-- View RFM data
SELECT *
FROM customer_rfm
ORDER BY monetary DESC;


-- ============================================================
-- 14. RFM SUMMARY
-- ============================================================

SELECT
    COUNT(*) AS customers,
    ROUND(AVG(recency), 2) AS avg_recency,
    ROUND(AVG(frequency), 2) AS avg_frequency,
    ROUND(AVG(monetary), 2) AS avg_monetary
FROM customer_rfm;


-- ============================================================
-- END OF BUSINESS ANALYSIS
-- ============================================================