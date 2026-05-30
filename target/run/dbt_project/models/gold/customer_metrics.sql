
  
    

  create  table "dbt_project".public.customer_metrics__dbt_tmp
  
  
    as
  
  (
    

WITH customer_base AS (
    SELECT
        c.customer_id,
        c.customer_name,
        c.email,
        c.country,
        c.region,
        COUNT(DISTINCT o.order_id) AS total_orders,
        COUNT(DISTINCT CASE WHEN o.status = 'completed' THEN o.order_id END) AS completed_orders,
        COUNT(DISTINCT CASE WHEN o.status = 'pending' THEN o.order_id END) AS pending_orders,
        COUNT(DISTINCT CASE WHEN o.status = 'cancelled' THEN o.order_id END) AS cancelled_orders,
        COALESCE(SUM(CASE WHEN o.status = 'completed' THEN o.amount END), 0) AS total_revenue,
        COALESCE(SUM(CASE WHEN o.status = 'completed' AND o.order_date >= CURRENT_DATE - 30 THEN o.amount END), 0) AS revenue_last_30_days,
        COALESCE(SUM(CASE WHEN o.status = 'completed' AND o.order_date >= CURRENT_DATE - 90 THEN o.amount END), 0) AS revenue_last_90_days,
        ROUND(AVG(CASE WHEN o.status = 'completed' THEN o.amount END), 2) AS avg_order_value,
        MAX(o.order_date) AS last_order_date,
        MIN(o.order_date) AS first_order_date,
        COUNT(DISTINCT CASE WHEN o.status = 'completed' AND o.order_date >= CURRENT_DATE - 90 THEN o.order_id END) AS orders_last_90_days,
        CURRENT_DATE - MAX(o.order_date) AS days_since_last_order
    FROM "dbt_project".public.stg_customers c
    LEFT JOIN "dbt_project".public.stg_orders o ON c.customer_id = o.customer_id
    GROUP BY c.customer_id, c.customer_name, c.email, c.country, c.region
),

rfm_scoring AS (
    SELECT
        *,
        -- RFM Scoring (1-5 scale, 5 is best)
        NTILE(5) OVER (ORDER BY COALESCE(days_since_last_order, 999999) DESC) AS r_score,  -- Recency (lower days = higher score)
        NTILE(5) OVER (ORDER BY total_orders) AS f_score,  -- Frequency
        NTILE(5) OVER (ORDER BY total_revenue) AS m_score   -- Monetary
    FROM customer_base
),

customer_segmentation AS (
    SELECT
        *,
        -- RFM Segment (simplified: Champions, Core, At-Risk, Lost)
        CASE
            WHEN r_score >= 4 AND f_score >= 4 AND m_score >= 4 THEN 'Champions'
            WHEN r_score >= 3 AND f_score >= 3 AND m_score >= 3 THEN 'Loyal Customers'
            WHEN r_score >= 3 AND (f_score >= 2 OR m_score >= 2) THEN 'Potential'
            WHEN r_score <= 2 AND (f_score >= 3 OR m_score >= 3) THEN 'At-Risk'
            WHEN r_score <= 2 THEN 'Lost'
            ELSE 'Need Attention'
        END AS rfm_segment,
        
        -- Churn Risk (based on inactivity + trend)
        CASE
            WHEN days_since_last_order >= 180 THEN 'High'
            WHEN days_since_last_order >= 90 AND revenue_last_90_days = 0 THEN 'High'
            WHEN days_since_last_order >= 60 THEN 'Medium'
            WHEN revenue_last_30_days < revenue_last_90_days * 0.3 AND days_since_last_order >= 30 THEN 'Medium'
            ELSE 'Low'
        END AS churn_risk,
        
        -- Customer Activity Status
        CASE
            WHEN days_since_last_order <= 30 THEN 'Active'
            WHEN days_since_last_order <= 90 THEN 'At-Risk'
            ELSE 'Inactive'
        END AS customer_status
    FROM rfm_scoring
),

health_scores AS (
    SELECT
        *,
        -- Health Score (0-100): Composite of recency, frequency, value, and momentum
        ROUND(
            (r_score * 10) +  -- Recency weight: 50 points max
            (f_score * 8) +   -- Frequency weight: 40 points max
            (m_score * 8) +   -- Monetary weight: 40 points max
            CASE
                WHEN revenue_last_30_days > 0 AND revenue_last_90_days > 0 
                    AND revenue_last_30_days > (revenue_last_90_days / 3) THEN 5
                ELSE 0
            END -  -- Growth bonus: 5 points if revenue is trending up
            CASE
                WHEN churn_risk = 'High' THEN 15
                WHEN churn_risk = 'Medium' THEN 5
                ELSE 0
            END  -- Churn penalty
        ) AS health_score
    FROM customer_segmentation
)

SELECT
    customer_id,
    customer_name,
    email,
    country,
    region,
    -- Basic Metrics
    total_orders,
    completed_orders,
    pending_orders,
    cancelled_orders,
    total_revenue,
    avg_order_value,
    -- Temporal
    last_order_date,
    first_order_date,
    days_since_last_order,
    -- Revenue Momentum
    revenue_last_30_days,
    revenue_last_90_days,
    orders_last_90_days,
    ROUND((last_order_date - first_order_date) / 365.0, 1) AS customer_lifetime_years,
    -- Story-Telling KPIs
    health_score,
    rfm_segment,
    churn_risk,
    customer_status,
    -- Supporting Metrics for Filtering
    ROUND(AVG(avg_order_value) OVER (), 2) AS avg_order_value_overall,
    ROUND(AVG(total_revenue) OVER (), 2) AS avg_customer_revenue_overall,
    CURRENT_TIMESTAMP AS updated_at
FROM health_scores
ORDER BY health_score DESC, total_revenue DESC
  );
  