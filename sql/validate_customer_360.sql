-- row count
SELECT COUNT(*) AS total_customers
FROM analytics.customer_360;

-- Unique customers
SELECT
    COUNT(*) AS total_rows,
    COUNT(DISTINCT customer_id) AS unique_customers
FROM analytics.customer_360;

-- Duplicate customer IDs
SELECT
    customer_id,
    COUNT(*) AS occurrences
FROM analytics.customer_360
GROUP BY customer_id
HAVING COUNT(*) > 1;

-- Customers without orders
SELECT COUNT(*) AS customer_without_orders
FROM analytics.customer_360
WHERE total_orders = 0;

-- Customers with orders
SELECT COUNT(*) AS  customer_with_orders
FROM analytics.customer_360
WHERE total_orders > 0;