
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select customer_status
from "dbt_project".public.customer_metrics
where customer_status is null



  
  
      
    ) dbt_internal_test