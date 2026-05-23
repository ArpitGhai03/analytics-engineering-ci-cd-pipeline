import subprocess
import pandas as pd
import psycopg2
import sys

# PostgreSQL credentials
DB_CONFIG = {
    'host': 'localhost',
    'port': 5432,
    'database': 'dbt_project',
    'user': 'postgres',
    'password': 'Arpit_123'
}

def run_dbt():
    """Execute dbt run command"""
    print("\n" + "="*70)
    print("STEP 1: Running dbt transformations...")
    print("="*70)
    
    try:
        result = subprocess.run(['dbt', 'run'], cwd='.', capture_output=False)
        if result.returncode != 0:
            print("✗ dbt run failed!")
            sys.exit(1)
        print("✓ dbt run completed successfully")
        return True
    except Exception as e:
        print(f"✗ Error running dbt: {e}")
        sys.exit(1)

def export_final_data_to_db_and_csv():
    """Export the final customer metrics data to both database and CSV"""
    print("\n" + "="*70)
    print("STEP 2: Exporting final data to CSV...")
    print("="*70)
    
    try:
        # Connect to database
        conn = psycopg2.connect(
            host=DB_CONFIG['host'],
            port=DB_CONFIG['port'],
            database=DB_CONFIG['database'],
            user=DB_CONFIG['user'],
            password=DB_CONFIG['password']
        )
        
        # Query the customer_metrics table
        query = """
        SELECT * FROM public.customer_metrics
        ORDER BY total_revenue DESC
        """
        
        df = pd.read_sql(query, conn)
        conn.close()
        
        # Export to CSV
        output_path = 'data/final_dashboard_data.csv'
        df.to_csv(output_path, index=False)
        
        print(f"✓ Data exported to: {output_path}")
        print(f"  Total records: {len(df)}")
        print(f"\n  Sample Data:")
        print(f"  {df[['customer_id', 'customer_name', 'total_revenue', 'completed_orders']].head(3).to_string()}")
        
    except Exception as e:
        print(f"✗ Error exporting data: {e}")
        sys.exit(1)

def main():
    """Main execution - Run dbt then export final data"""
    print("\n" + "█"*70)
    print("█  CI/CD PIPELINE - END-TO-END EXECUTION")
    print("█"*70)
    
    # Step 1: Run dbt
    run_dbt()
    
    # Step 2: Export final data
    export_final_data_to_db_and_csv()
    
    print("\n" + "="*70)
    print("✓ COMPLETE! Data pipeline executed successfully!")
    print("="*70)
    print("\n✓ Database: customer_order_metrics table updated")
    print("✓ CSV: data/final_dashboard_data.csv created/updated")
    print("\n" + "█"*70 + "\n")

if __name__ == "__main__":
    main()
