
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    

with all_values as (

    select
        rfm_segment as value_field,
        count(*) as n_records

    from "dbt_project".public.customer_metrics
    group by rfm_segment

)

select *
from all_values
where value_field not in (
    'Champions','Loyal Customers','Potential','At-Risk','Lost','Need Attention'
)



  
  
      
    ) dbt_internal_test