{{
  config(
    materialized='table',
    tags=['bronze', 'raw']
  )
}}

SELECT
    customer_id,
    customer_name,
    email,
    phone,
    country,
    CURRENT_TIMESTAMP AS loaded_at
FROM {{ source('raw', 'customers') }}
WHERE customer_id IS NOT NULL
