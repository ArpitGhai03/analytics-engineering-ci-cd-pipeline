{{
  config(
    materialized='view',
    tags=['staging']
  )
}}

SELECT
    order_id,
    customer_id,
    CASE 
        WHEN order_date IS NULL THEN NULL
        ELSE CAST(order_date AS DATE)
    END AS order_date,
    CASE 
        WHEN amount IS NULL OR amount <= 0 THEN NULL
        ELSE CAST(amount AS DECIMAL(10, 2))
    END AS amount,
    LOWER(TRIM(status)) AS status,
    CURRENT_TIMESTAMP AS created_at
FROM public.orders
WHERE 
    order_id IS NOT NULL
    AND customer_id IS NOT NULL
    AND order_date IS NOT NULL
