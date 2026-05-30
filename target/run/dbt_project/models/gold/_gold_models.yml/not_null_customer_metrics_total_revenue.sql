
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select total_revenue
from "dbt_project".public.customer_metrics
where total_revenue is null



  
  
      
    ) dbt_internal_test