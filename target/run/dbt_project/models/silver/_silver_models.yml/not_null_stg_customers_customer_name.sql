
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select customer_name
from "dbt_project".public.stg_customers
where customer_name is null



  
  
      
    ) dbt_internal_test