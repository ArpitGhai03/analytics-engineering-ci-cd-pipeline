
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select health_score
from "dbt_project".public.customer_metrics
where health_score is null



  
  
      
    ) dbt_internal_test