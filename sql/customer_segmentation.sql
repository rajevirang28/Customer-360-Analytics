CREATE TABLE analytics.customer_segments AS
WITH customer_rfm AS(
    SELECT
        customer_id,
        total_orders,
        total_revenue,
        last_order_date,
        first_order_date,
        total_website_events,
        total_sessions,
        total_marketing_conversions,
        total_support_tickets,
        avg_satisfaction_score,

        CASE
            WHEN last_order_date IS NULL
                THEN NULL
            ELSE
                CURRENT_DATE - last_order_date
        END AS recency_days,

        total_orders AS frequency,

        total_revenue AS monetary

    FROM analytics.customer_360
)

SELECT *,

    CASE
        WHEN recency_days IS NULL THEN 0
        WHEN recency_days <= 30 THEN 5
        WHEN recency_days <= 90 THEN 4
        WHEN recency_days <= 180 THEN 3
        WHEN recency_days <= 365 THEN 2
        ELSE 1
    END AS recency_score,

    CASE
        WHEN frequency = 0 THEN 0
        WHEN frequency >= 20 THEN 5
        WHEN frequency >= 10 THEN 4
        WHEN frequency >= 5 THEN 3
        WHEN frequency >= 2 THEN 2
        ELSE 1
    END AS frequency_score,

    CASE
        WHEN monetary = 0 THEN 0
        WHEN monetary >= 500000 THEN 5
        WHEN monetary >= 250000 THEN 4
        WHEN monetary >= 100000 THEN 3
        WHEN monetary >= 50000 THEN 2
        ELSE 1
    END AS monetary_score
FROM customer_rfm;

SELECT
    customer_id,
    total_orders,
    total_revenue,
    recency_days,
    frequency,
    monetary,
    recency_score,
    frequency_score,
    monetary_score
FROM analytics.customer_segments
ORDER BY total_revenue DESC
LIMIT 10;

ALTER TABLE analytics.customer_segments
ADD COLUMN customer_segment VARCHAR(50);

UPDATE analytics.customer_segments
SET customer_segment = 

    CASE
        WHEN recency_score >= 4
        AND frequency_score >= 4
        AND monetary_score >= 4
        THEN 'VIP Customer'

        WHEN frequency_score >= 4
        AND monetary_score >= 3
        THEN 'Loyal Customer'

        WHEN monetary_score >= 4
        THEN 'High Value Customer'

        WHEN recency_score <= 2
        AND frequency_score >= 3
        THEN 'At Risk Customer'

        WHEN recency_score >= 4
        AND frequency_score <= 2
        THEN 'New Customer'

        WHEN total_website_events >= 50
        AND total_orders = 0
        THEN 'Browsing Customer'

        WHEN total_orders = 0
        AND total_website_events < 50
        THEN 'Inactive Customer'

        ELSE 'Regular Customer'
    END;

SELECT
    customer_segment,
    COUNT(*) AS customer_count
FROM analytics.customer_segments
GROUP BY customer_segment
ORDER BY customer_count DESC;

SELECT
    COUNT(*) AS total_customers,
    COUNT(DISTINCT customer_id) AS unique_customers
FROM analytics.customer_segments;