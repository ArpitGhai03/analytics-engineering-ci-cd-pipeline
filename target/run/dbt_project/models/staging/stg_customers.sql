
  create view "dbt_project".public.stg_customers__dbt_tmp
    
    
  as (
    

SELECT
    customer_id,
    customer_name,
    email,
    phone,
    country,
    CURRENT_TIMESTAMP AS created_at
FROM public.customers
WHERE customer_id IS NOT NULL
  );