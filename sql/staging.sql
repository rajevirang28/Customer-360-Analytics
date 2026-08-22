-- STAGING CUSTOMERS
CREATE TABLE staging.customers AS
SELECT
    customers_id,
    TRIM(name) AS name.
    LOWER(TRIM(email)) AS email,
    TRIM(phone) AS phone,
    age,
    gender,
    TRIM(state) AS state,
    registration_date,
    acquisition_channel
FROM raw.customers;

-- STAGING PRODUCTS
CREATE TABLE staging.products AS
SELECT
    product_id,
    TRIM(product_name) AS product_name,
    TRIM(category) AS category,
    TRIM(subcategory) AS subcategory,
    TRIM(brand) AS brand,
    unit_cost,
    unit_price
FROM raw.products;

-- STAGING ORDERS
CREATE TABLE staging.orders AS
SELECT
    order_id,
    customer_id,
    order_date,
    product_id,
    quantity,
    unit_price,
    discount,
    payment_method,
    order_status,
    revenue
FROM raw.orders
WHERE quantity > 0
    AND unit_price >= 0
    AND discount BETWEEN 0 AND 100
    AND revenue >= 0;

-- STAGING WEBSITE EVENTS
CREATE TABLE staging.website_events AS
SELECT
    event_id,
    customer_id,
    event_time,
    session_id,
    event_type,
    page,
    device,
    traffic_source
FROM raw.website_events
WHERE event_id IS NOT NULL
    AND customer_id IS NOT NULL
    AND event_time IS NOT NULL;

-- STAGING MARKETING
CREATE TABLE staging.marketing AS
SELECT
    campaign_id,
    customer_id,
    TRIM(campaign_name) AS campaign_name,
    TRIM(channel) AS channel,
    sent_date,
    opened,
    clicked,
    converted,
    conversion_value
FROM raw.marketing
WHERE campaign_id IS NOT NULL
    AND customer_id IS NOT NULL
    AND opened IN (0,1)
    AND clicked IN (0,1)
    AND converted IN (0,1)
    AND conversion_value >= 0;

-- STAGING SUPPORT TICKETS
CREATE TABLE staging.support_tickets AS
SELECT
    ticket_id,
    customer_id,
    created_date,
    TRIM(issue_type) AS issue_type,
    TRIM(priority) AS priority,
    TRIM(status) AS status,
    resolution_time_hours,
    satisfaction_score
FROM raw.support_tickets
WHERE ticket_id IS NOT NULL
    AND customer_id IS NOT NULL
    AND(
        resolution_time_hours IS NULL
        OR resolution_time_hours >= 0
        )
    AND(
        satisfaction_score IS NULL
        OR satisfaction_score BETWEEN 1 AND 5
        );

