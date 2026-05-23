{{
  config(
    materialized='table',
    tags=['marts', 'dashboard']
  )
}}

WITH customer_metrics AS (
    SELECT
        c.customer_id,
        c.customer_name,
        c.email,
        c.country,
        COUNT(DISTINCT o.order_id) AS total_orders,
        COUNT(DISTINCT CASE WHEN o.status = 'completed' THEN o.order_id END) AS completed_orders,
        COUNT(DISTINCT CASE WHEN o.status = 'pending' THEN o.order_id END) AS pending_orders,
        COALESCE(SUM(CASE WHEN o.status = 'completed' THEN o.amount END), 0) AS total_revenue,
        ROUND(AVG(CASE WHEN o.status = 'completed' THEN o.amount END), 2) AS avg_order_value,
        MAX(o.order_date) AS last_order_date,
        MIN(o.order_date) AS first_order_date
    FROM {{ ref('stg_customers') }} c
    LEFT JOIN {{ ref('stg_orders') }} o ON c.customer_id = o.customer_id
    GROUP BY c.customer_id, c.customer_name, c.email, c.country
)

SELECT
    customer_id,
    customer_name,
    email,
    country,
    total_orders,
    completed_orders,
    pending_orders,
    total_revenue,
    avg_order_value,
    last_order_date,
    first_order_date,
    (last_order_date - first_order_date) AS days_as_customer,
    CURRENT_TIMESTAMP AS updated_at
FROM customer_metrics
ORDER BY total_revenue DESC
