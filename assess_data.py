import pandas as pd

# Load the data
customers = pd.read_csv('data/customers.csv')
orders = pd.read_csv('data/orders.csv')

print("=" * 60)
print("CUSTOMERS DATA QUALITY ASSESSMENT")
print("=" * 60)
print(f"Total records: {len(customers)}")
print(f"Duplicates: {customers.duplicated().sum()}")
print(f"Null values:\n{customers.isnull().sum()}")
print(f"\nEmail format issues: {customers[~customers['email'].str.contains('@')].shape[0]}")
print(f"Phone format issues: {customers[customers['phone'].isna()].shape[0]}")

print("\n" + "=" * 60)
print("ORDERS DATA QUALITY ASSESSMENT")
print("=" * 60)
print(f"Total records: {len(orders)}")
print(f"Duplicates: {orders.duplicated().sum()}")
print(f"Null values:\n{orders.isnull().sum()}")
print(f"Invalid amounts (<=0): {(orders['amount'] <= 0).sum()}")
print(f"Invalid status values: {(~orders['status'].isin(['completed', 'pending', 'cancelled'])).sum()}")
print(f"Date format issues: {pd.to_datetime(orders['order_date'], errors='coerce').isna().sum()}")

print("\n" + "=" * 60)
print("DATA DISTRIBUTION")
print("=" * 60)
print(f"\nStatus distribution:\n{orders['status'].value_counts()}")
print(f"\nAmount statistics:\n{orders['amount'].describe()}")
print(f"\nCountry distribution:\n{customers['country'].value_counts().head(10)}")
