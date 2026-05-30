import psycopg2
import pandas as pd

DB_CONFIG = {
    'host': 'localhost',
    'port': 5432,
    'database': 'dbt_project',
    'user': 'postgres',
    'password': 'Arpit_123'
}

try:
    conn = psycopg2.connect(**DB_CONFIG)
    
    # Get top 10 customers by health score
    query = """
    SELECT 
        customer_name,
        region,
        health_score,
        rfm_segment,
        churn_risk,
        customer_status,
        total_revenue::INT,
        revenue_last_30_days::INT,
        days_since_last_order,
        total_orders
    FROM public.customer_metrics
    ORDER BY health_score DESC
    LIMIT 10;
    """
    
    df = pd.read_sql(query, conn)
    print("\n" + "="*120)
    print("TOP 10 CUSTOMERS - THE STORY YOUR DASHBOARD TELLS")
    print("="*120)
    print(df.to_string(index=False))
    
    # Get segment breakdown
    print("\n" + "="*120)
    print("RFM SEGMENTATION - WHERE YOUR CUSTOMERS ARE")
    print("="*120)
    segment_query = """
    SELECT 
        rfm_segment,
        COUNT(*) as customer_count,
        CAST(AVG(health_score) AS INT) as avg_health_score,
        CAST(SUM(total_revenue) AS INT) as total_revenue
    FROM public.customer_metrics
    GROUP BY rfm_segment
    ORDER BY total_revenue DESC;
    """
    
    df_segments = pd.read_sql(segment_query, conn)
    print(df_segments.to_string(index=False))
    
    # Get churn risk breakdown
    print("\n" + "="*120)
    print("CHURN RISK - WHO TO FOCUS ON")
    print("="*120)
    churn_query = """
    SELECT 
        churn_risk,
        COUNT(*) as customers_at_risk,
        CAST(AVG(days_since_last_order) AS INT) as avg_days_inactive,
        CAST(SUM(total_revenue) AS INT) as at_risk_revenue
    FROM public.customer_metrics
    GROUP BY churn_risk
    ORDER BY customers_at_risk DESC;
    """
    
    df_churn = pd.read_sql(churn_query, conn)
    print(df_churn.to_string(index=False))
    
    # Get activity status
    print("\n" + "="*120)
    print("CUSTOMER ACTIVITY STATUS - ENGAGEMENT LEVELS")
    print("="*120)
    status_query = """
    SELECT 
        customer_status,
        COUNT(*) as customer_count,
        CAST(AVG(revenue_last_30_days) AS INT) as avg_monthly_revenue,
        CAST(SUM(revenue_last_30_days) AS INT) as total_monthly_revenue
    FROM public.customer_metrics
    GROUP BY customer_status
    ORDER BY total_monthly_revenue DESC;
    """
    
    df_status = pd.read_sql(status_query, conn)
    print(df_status.to_string(index=False))
    
    conn.close()
    
except Exception as e:
    print(f"Error: {e}")
