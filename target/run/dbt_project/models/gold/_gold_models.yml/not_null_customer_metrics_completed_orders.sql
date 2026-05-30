
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select completed_orders
from "dbt_project".public.customer_metrics
where completed_orders is null



  
  
      
    ) dbt_internal_test