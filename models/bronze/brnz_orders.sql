{{
  config(
    materialized='table',
    tags=['bronze', 'raw']
  )
}}

SELECT
    order_id,
    customer_id,
    order_date,
    amount,
    status,
    CURRENT_TIMESTAMP AS loaded_at
FROM {{ source('raw', 'orders') }}
WHERE 
    order_id IS NOT NULL
    AND customer_id IS NOT NULL
