
  
    

  create  table "dbt_project".public.brnz_customers__dbt_tmp
  
  
    as
  
  (
    

SELECT
    customer_id,
    customer_name,
    email,
    phone,
    country,
    CURRENT_TIMESTAMP AS loaded_at
FROM "dbt_project"."public"."customers"
WHERE customer_id IS NOT NULL
  );
  