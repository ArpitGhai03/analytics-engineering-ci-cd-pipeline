

WITH deduplicated AS (
    SELECT
        customer_id,
        customer_name,
        email,
        phone,
        country,
        loaded_at,
        ROW_NUMBER() OVER (PARTITION BY LOWER(TRIM(email)) ORDER BY customer_id) AS rn
    FROM "dbt_project".public.brnz_customers
    WHERE customer_id IS NOT NULL
),

cleaned AS (
    SELECT
        customer_id,
        -- Standardize name: Proper case (title case)
        INITCAP(TRIM(customer_name)) AS customer_name,
        -- Normalize email: lowercase and trim
        LOWER(TRIM(email)) AS email,
        -- Standardize phone: extract digits only
        REGEXP_REPLACE(phone, '[^0-9]', '') AS phone_digits,
        -- Map country to region
        CASE
            WHEN country IN ('USA', 'Canada', 'Mexico') THEN 'North America'
            WHEN country IN ('UK', 'Germany', 'France', 'Spain', 'Italy', 'Netherlands', 'Belgium', 'Sweden') THEN 'Europe'
            WHEN country IN ('India', 'Japan', 'Australia') THEN 'Asia Pacific'
            WHEN country IN ('Brazil') THEN 'South America'
            ELSE 'Other'
        END AS region,
        country,
        loaded_at,
        -- Data quality flags
        CASE
            WHEN email ~ '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}$' THEN TRUE
            ELSE FALSE
        END AS is_valid_email,
        CASE
            WHEN LENGTH(REGEXP_REPLACE(phone, '[^0-9]', '')) >= 10 THEN TRUE
            ELSE FALSE
        END AS is_valid_phone,
        CURRENT_TIMESTAMP AS transformed_at
    FROM deduplicated
    WHERE rn = 1  -- Keep only first occurrence of each email
)

SELECT * FROM cleaned