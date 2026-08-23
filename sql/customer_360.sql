CREATE TABLE analytics.customer_360 AS

SELECT

    c.customer_id,
    c.name,
    c.email,
    c.phone,
    c.age,
    c.gender,
    c.city,
    c.state,
    c.registration_date,
    c.acquisition_channel,

    COALESCE(p.total_orders, 0) AS total_orders,

    COALESCE(p.total_revenue, 0) AS total_revenue,

    COALESCE(p.average_order_value, 0)
        AS average_order_value,

    COALESCE(p.total_quantity, 0)
        AS total_quantity,

    p.first_order_date,
    p.last_order_date,

    COALESCE(p.delivered_orders, 0)
        AS delivered_orders,

    COALESCE(p.cancelled_orders, 0)
        AS cancelled_orders,

    COALESCE(p.returned_orders, 0)
        AS returned_orders,

    COALESCE(w.total_events, 0)
        AS total_website_events,

    COALESCE(w.total_sessions, 0)
        AS total_sessions,

    COALESCE(w.product_views, 0)
        AS product_views,

    COALESCE(w.searches, 0)
        AS searches,

    COALESCE(w.add_to_cart_count, 0)
        AS add_to_cart_count,

    COALESCE(w.remove_from_cart_count, 0)
        AS remove_from_cart_count,

    COALESCE(w.checkout_count, 0)
        AS checkout_count,

    COALESCE(w.website_purchase_events, 0)
        AS website_purchase_events,

    COALESCE(w.login_count, 0)
        AS login_count,

    w.first_event_time,
    w.last_event_time,

    COALESCE(m.total_campaigns, 0)
        AS total_campaigns,

    COALESCE(m.campaigns_opened, 0)
        AS campaigns_opened,

    COALESCE(m.campaigns_clicked, 0)
        AS campaigns_clicked,

    COALESCE(m.total_conversions, 0)
        AS total_marketing_conversions,

    COALESCE(m.open_rate, 0)
        AS marketing_open_rate,

    COALESCE(m.click_rate, 0)
        AS marketing_click_rate,

    COALESCE(m.conversion_rate, 0)
        AS marketing_conversion_rate,

    COALESCE(m.total_conversion_value, 0)
        AS marketing_conversion_value,

    m.first_campaign_date,
    m.last_campaign_date,

    COALESCE(s.total_tickets, 0)
        AS total_support_tickets,

    COALESCE(s.open_tickets, 0)
        AS open_tickets,

    COALESCE(s.in_progress_tickets, 0)
        AS in_progress_tickets,

    COALESCE(s.resolved_tickets, 0)
        AS resolved_tickets,

    COALESCE(s.closed_tickets, 0)
        AS closed_tickets,

    COALESCE(s.high_priority_tickets, 0)
        AS high_priority_tickets,

    COALESCE(s.critical_tickets, 0)
        AS critical_tickets,

    COALESCE(s.avg_resolution_time_hours, 0)
        AS avg_resolution_time_hours,

    COALESCE(s.avg_satisfaction_score, 0)
        AS avg_satisfaction_score,

    COALESCE(s.delivery_issues, 0)
        AS delivery_issues,

    COALESCE(s.product_issues, 0)
        AS product_issues,

    COALESCE(s.refund_issues, 0)
        AS refund_issues,

    COALESCE(s.payment_issues, 0)
        AS payment_issues,

    s.first_ticket_date,
    s.last_ticket_date

FROM staging.customers c

LEFT JOIN analytics.customer_purchase_metrics p
    ON c.customer_id = p.customer_id

LEFT JOIN analytics.customer_website_metrics w
    ON c.customer_id = w.customer_id

LEFT JOIN analytics.customer_marketing_metrics m
    ON c.customer_id = m.customer_id

LEFT JOIN analytics.customer_support_metrics s
    ON c.customer_id = s.customer_id;