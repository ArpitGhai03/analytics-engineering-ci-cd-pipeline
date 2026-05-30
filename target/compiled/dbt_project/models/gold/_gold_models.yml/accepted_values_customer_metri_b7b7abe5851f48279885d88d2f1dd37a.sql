
    
    

with all_values as (

    select
        customer_segment as value_field,
        count(*) as n_records

    from "dbt_project".public.customer_metrics
    group by customer_segment

)

select *
from all_values
where value_field not in (
    'High-Value','Medium-Value','Low-Value'
)


