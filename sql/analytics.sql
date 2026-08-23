-- CUSTOMER PURCHASE METRICS
CREATE Table analytics.customer_purchase_metrics AS
SELECT
    customer_id,
    COUNT(DISTINCT order_id) AS total_orders,
    SUM(revenue) AS total_revenue,
    ROUND(
        SUM(revenue) / NULLIF(COUNT(DISTINCT order_id), 0), 2
    ) AS average_order_value,
    SUM(quantity) AS total_quantity,
    MIN(order_date) AS first_order_date,
    MAX(order_date) AS last_order_date,
    COUNT(
        CASE
            WHEN order_status = 'Delivered'
            THEN 1
        END
    ) AS delivered_orders,

    COUNT(
        CASE
            WHEN order_status = 'Cancelled'
            THEN 1
        END
    ) AS cancelled_orders,

    COUNT(
        CASE
            WHEN order_status = 'Returned'
            THEN 1
        END
    ) AS returned_orders

FROM staging.orders
GROUP BY customer_id;

-- CUSTOMER WEBSITE ENGAGEMENT METRICS
CREATE TABLE analytics.customer_website_metrics AS
SELECT
    customer_id,
    COUNT(*) AS total_events,
    COUNT(DISTINCT session_id) AS total_sessions,
    COUNT(
        CASE
            WHEN event_type = 'product_view'
            THEN 1
        END
    ) AS product_view,

    COUNT(
        CASE
            WHEN event_type = 'search'
            THEN 1
        END
    ) AS searches,

    COUNT(
        CASE
            WHEN event_type = 'add_to_cart'
            THEN 1
        END
    ) AS add_to_cart_count,

    COUNT(
        CASE
            WHEN event_type = 'remove_from_cart'
            THEN 1
        END
    ) AS remove_from_cart_count,

    COUNT(
        CASE
            WHEN event_type = 'checkout'
            THEN 1
        END
    ) AS checkout_count,

    COUNT(
        CASE
            WHEN event_type = 'purchase'
            THEN 1
        END
    ) AS website_purchase_events,

    COUNT(
        CASE
            WHEN event_type = 'login'
            THEN 1
        END
    ) AS login_count,

    MIN(event_time) AS first_event_time,
    MAX(event_time) AS last_event_time

FROM staging.website_events
GROUP BY customer_id;

