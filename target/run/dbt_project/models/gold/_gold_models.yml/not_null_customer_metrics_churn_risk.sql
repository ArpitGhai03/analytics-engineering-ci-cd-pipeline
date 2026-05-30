
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select churn_risk
from "dbt_project".public.customer_metrics
where churn_risk is null



  
  
      
    ) dbt_internal_test