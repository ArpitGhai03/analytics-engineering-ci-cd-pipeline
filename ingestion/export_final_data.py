import pandas as pd
import psycopg2
from psycopg2 import sql

# PostgreSQL credentials
DB_CONFIG = {
    'host': 'localhost',
    'port': 5432,
    'database': 'dbt_project',
    'user': 'postgres',
    'password': 'Arpit_123'
}

def export_final_data_to_csv():
    """Export the final customer metrics data to CSV"""
    try:
        # Connect to database
        conn = psycopg2.connect(
            host=DB_CONFIG['host'],
            port=DB_CONFIG['port'],
            database=DB_CONFIG['database'],
            user=DB_CONFIG['user'],
            password=DB_CONFIG['password']
        )
        
        # Query the customer_order_metrics table
        query = """
        SELECT * FROM public.customer_order_metrics
        ORDER BY total_revenue DESC
        """
        
        df = pd.read_sql(query, conn)
        conn.close()
        
        # Export to CSV
        output_path = 'data/final_dashboard_data.csv'
        df.to_csv(output_path, index=False)
        
        print("="*70)
        print("✓ Final Data Successfully Exported to CSV!")
        print("="*70)
        print(f"\nFile saved: {output_path}")
        print(f"Total records: {len(df)}")
        print("\nData Preview:")
        print(df.to_string())
        print("\n" + "="*70)
        
    except Exception as e:
        print(f"✗ Error exporting data: {e}")

if __name__ == "__main__":
    export_final_data_to_csv()
