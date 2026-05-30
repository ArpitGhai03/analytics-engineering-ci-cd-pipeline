
  
    

  create  table "dbt_project".public.brnz_orders__dbt_tmp
  
  
    as
  
  (
    

SELECT
    order_id,
    customer_id,
    order_date,
    amount,
    status,
    CURRENT_TIMESTAMP AS loaded_at
FROM "dbt_project"."public"."orders"
WHERE 
    order_id IS NOT NULL
    AND customer_id IS NOT NULL
  );
  