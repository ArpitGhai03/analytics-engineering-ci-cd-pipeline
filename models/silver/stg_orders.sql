{{
  config(
    materialized='view',
    tags=['silver', 'cleaned']
  )
}}

WITH validated AS (
    SELECT
        order_id,
        customer_id,
        CAST(order_date AS DATE) AS order_date,
        CAST(amount AS DECIMAL(10, 2)) AS amount,
        LOWER(TRIM(status)) AS status,
        loaded_at,
        -- Data quality flags
        CASE
            WHEN order_date IS NULL THEN FALSE
            ELSE TRUE
        END AS is_valid_date,
        CASE
            WHEN amount <= 0 THEN FALSE
            WHEN amount > 10000 THEN FALSE  -- Flag suspicious high amounts
            ELSE TRUE
        END AS is_valid_amount,
        CASE
            WHEN LOWER(TRIM(status)) IN ('completed', 'pending', 'cancelled') THEN TRUE
            ELSE FALSE
        END AS is_valid_status,
        -- Outlier detection
        CASE
            WHEN amount > (SELECT PERCENTILE_CONT(0.95) WITHIN GROUP (ORDER BY amount) FROM {{ ref('brnz_orders') }}) THEN TRUE
            ELSE FALSE
        END AS is_high_value_order,
        CASE
            WHEN amount < (SELECT PERCENTILE_CONT(0.05) WITHIN GROUP (ORDER BY amount) FROM {{ ref('brnz_orders') }}) THEN TRUE
            ELSE FALSE
        END AS is_low_value_order,
        CURRENT_TIMESTAMP AS transformed_at
    FROM {{ ref('brnz_orders') }}
    WHERE 
        order_id IS NOT NULL
        AND customer_id IS NOT NULL
        AND order_date IS NOT NULL
        AND LOWER(TRIM(status)) IN ('completed', 'pending', 'cancelled')
)

SELECT * FROM validated
