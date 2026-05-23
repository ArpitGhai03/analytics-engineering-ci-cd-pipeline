import pandas as pd
import psycopg2
from psycopg2 import sql
import os
import sys

# PostgreSQL credentials
DB_CONFIG = {
    'host': 'localhost',
    'port': 5432,
    'database': 'dbt_project',
    'user': 'postgres',
    'password': 'Arpit_123'
}

# CSV file paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CUSTOMERS_CSV = os.path.join(BASE_DIR, 'data', 'customers.csv')
ORDERS_CSV = os.path.join(BASE_DIR, 'data', 'orders.csv')

def create_connection():
    """Create a connection to PostgreSQL database"""
    try:
        conn = psycopg2.connect(
            host=DB_CONFIG['host'],
            port=DB_CONFIG['port'],
            database=DB_CONFIG['database'],
            user=DB_CONFIG['user'],
            password=DB_CONFIG['password']
        )
        print("✓ Connected to PostgreSQL database successfully")
        return conn
    except psycopg2.Error as e:
        print(f"✗ Error connecting to PostgreSQL: {e}")
        sys.exit(1)

def create_tables(conn):
    """Create customers and orders tables if they don't exist"""
    cursor = conn.cursor()
    
    try:
        # Create customers table
        create_customers_table = """
        CREATE TABLE IF NOT EXISTS customers (
            customer_id INTEGER PRIMARY KEY,
            customer_name VARCHAR(255),
            email VARCHAR(255),
            phone VARCHAR(20),
            country VARCHAR(100)
        );
        """
        cursor.execute(create_customers_table)
        print("✓ Customers table created/verified")
        
        # Create orders table
        create_orders_table = """
        CREATE TABLE IF NOT EXISTS orders (
            order_id INTEGER PRIMARY KEY,
            customer_id INTEGER,
            order_date DATE,
            amount DECIMAL(10, 2),
            status VARCHAR(50),
            FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
        );
        """
        cursor.execute(create_orders_table)
        print("✓ Orders table created/verified")
        
        conn.commit()
    except psycopg2.Error as e:
        print(f"✗ Error creating tables: {e}")
        conn.rollback()
        sys.exit(1)
    finally:
        cursor.close()

def load_customers(conn):
    """Load customers data from CSV to database"""
    try:
        df_customers = pd.read_csv(CUSTOMERS_CSV)
        print(f"\n✓ Loaded {len(df_customers)} customer records from CSV")
        
        cursor = conn.cursor()
        
        # Clear existing data (optional)
        cursor.execute("TRUNCATE TABLE customers CASCADE;")
        
        insert_count = 0
        for index, row in df_customers.iterrows():
            try:
                insert_query = """
                INSERT INTO customers (customer_id, customer_name, email, phone, country)
                VALUES (%s, %s, %s, %s, %s)
                """
                cursor.execute(insert_query, (
                    int(row['customer_id']) if pd.notna(row['customer_id']) else None,
                    row['customer_name'] if pd.notna(row['customer_name']) else None,
                    row['email'] if pd.notna(row['email']) else None,
                    row['phone'] if pd.notna(row['phone']) else None,
                    row['country'] if pd.notna(row['country']) else None
                ))
                insert_count += 1
            except Exception as e:
                print(f"  ⚠ Skipping row {index + 1}: {e}")
                conn.rollback()
                cursor = conn.cursor()
                continue
        
        conn.commit()
        print(f"✓ Inserted {insert_count} customer records into database")
        cursor.close()
        
    except FileNotFoundError:
        print(f"✗ Error: {CUSTOMERS_CSV} not found")
        sys.exit(1)
    except Exception as e:
        print(f"✗ Error loading customers: {e}")
        sys.exit(1)

def load_orders(conn):
    """Load orders data from CSV to database"""
    try:
        df_orders = pd.read_csv(ORDERS_CSV)
        print(f"\n✓ Loaded {len(df_orders)} order records from CSV")
        
        cursor = conn.cursor()
        
        # Clear existing data (optional)
        cursor.execute("TRUNCATE TABLE orders CASCADE;")
        
        insert_count = 0
        skip_count = 0
        
        for index, row in df_orders.iterrows():
            try:
                # Handle messy data
                order_id = int(row['order_id']) if pd.notna(row['order_id']) else None
                customer_id = int(row['customer_id']) if pd.notna(row['customer_id']) else None
                
                # Try to parse date
                try:
                    order_date = pd.to_datetime(row['order_date']).date() if pd.notna(row['order_date']) else None
                except:
                    order_date = None
                
                # Try to parse amount
                try:
                    amount = float(row['amount']) if pd.notna(row['amount']) and row['amount'] != 'amount_not_provided' else None
                except:
                    amount = None
                
                # Normalize status
                status = str(row['status']).lower() if pd.notna(row['status']) else None
                
                # Skip if critical fields are missing
                if order_id is None:
                    skip_count += 1
                    continue
                
                insert_query = """
                INSERT INTO orders (order_id, customer_id, order_date, amount, status)
                VALUES (%s, %s, %s, %s, %s)
                """
                cursor.execute(insert_query, (order_id, customer_id, order_date, amount, status))
                insert_count += 1
                
            except Exception as e:
                skip_count += 1
                print(f"  ⚠ Skipping row {index + 1}: {e}")
                conn.rollback()
                cursor = conn.cursor()
                continue
        
        conn.commit()
        print(f"✓ Inserted {insert_count} order records into database")
        if skip_count > 0:
            print(f"  ⚠ Skipped {skip_count} invalid records")
        cursor.close()
        
    except FileNotFoundError:
        print(f"✗ Error: {ORDERS_CSV} not found")
        sys.exit(1)
    except Exception as e:
        print(f"✗ Error loading orders: {e}")
        sys.exit(1)

def verify_data(conn):
    """Verify data was loaded successfully"""
    cursor = conn.cursor()
    
    try:
        cursor.execute("SELECT COUNT(*) FROM customers;")
        customer_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM orders;")
        order_count = cursor.fetchone()[0]
        
        print(f"\n✓ Data Verification:")
        print(f"  - Customers in DB: {customer_count}")
        print(f"  - Orders in DB: {order_count}")
        
    except Exception as e:
        print(f"✗ Error verifying data: {e}")
    finally:
        cursor.close()

def main():
    """Main execution function"""
    print("="*60)
    print("PostgreSQL Data Ingestion Script")
    print("="*60)
    
    # Create connection
    conn = create_connection()
    
    try:
        # Create tables
        create_tables(conn)
        
        # Load data
        load_customers(conn)
        load_orders(conn)
        
        # Verify
        verify_data(conn)
        
        print("\n" + "="*60)
        print("✓ Data ingestion completed successfully!")
        print("="*60)
        
    finally:
        conn.close()

if __name__ == "__main__":
    main()
