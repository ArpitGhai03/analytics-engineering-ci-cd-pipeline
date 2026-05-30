
    
    

with all_values as (

    select
        churn_risk as value_field,
        count(*) as n_records

    from "dbt_project".public.customer_metrics
    group by churn_risk

)

select *
from all_values
where value_field not in (
    'Low','Medium','High'
)


