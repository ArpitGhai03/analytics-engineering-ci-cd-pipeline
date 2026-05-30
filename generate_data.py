import csv
import random
from datetime import datetime, timedelta

# Set seed for reproducibility
random.seed(42)

# Generate customers data
customers = []
customer_ids = list(range(1, 151))  # 150 customers
first_names = ['John', 'Jane', 'Michael', 'Sarah', 'David', 'Emily', 'James', 'Lisa', 'Robert', 'Mary', 
               'William', 'Patricia', 'Richard', 'Jennifer', 'Joseph', 'Linda', 'Thomas', 'Barbara', 'Charles', 'Susan']
last_names = ['Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller', 'Davis', 'Rodriguez', 'Martinez',
              'Hernandez', 'Lopez', 'Gonzalez', 'Wilson', 'Anderson', 'Thomas', 'Taylor', 'Moore', 'Jackson', 'Martin']
countries = ['USA', 'UK', 'Canada', 'Germany', 'France', 'India', 'Australia', 'Japan', 'Mexico', 'Brazil',
             'Spain', 'Italy', 'Netherlands', 'Sweden', 'Belgium']

for cid in customer_ids:
    first_name = random.choice(first_names)
    last_name = random.choice(last_names)
    email = f"{first_name.lower()}.{last_name.lower()}{cid}@email.com"
    phone = f"+1{random.randint(2000000000, 9999999999)}"
    country = random.choice(countries)
    customers.append([cid, f"{first_name} {last_name}", email, phone, country])

# Write customers
with open('data/customers.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['customer_id', 'customer_name', 'email', 'phone', 'country'])
    writer.writerows(customers)

print(f"✅ Generated {len(customers)} customers")

# Generate orders data
orders = []
order_id = 1
start_date = datetime(2025, 1, 1)
end_date = datetime(2026, 5, 25)  # Recent dates (just before today 2026-05-29)
date_range = (end_date - start_date).days
statuses = ['completed', 'completed', 'completed', 'pending', 'cancelled']  # More completed orders

# Each customer has 3-8 orders on average
orders_per_customer = {cid: random.randint(3, 8) for cid in customer_ids}

for cid in customer_ids:
    for _ in range(orders_per_customer[cid]):
        days_offset = random.randint(0, date_range)
        order_date = start_date + timedelta(days=days_offset)
        amount = round(random.uniform(50, 1500), 2)
        status = random.choice(statuses)
        orders.append([order_id, cid, order_date.strftime('%Y-%m-%d'), amount, status])
        order_id += 1

# Add recent orders for some customers (last 30 days) to create "Active" customers
recent_start = datetime(2026, 4, 29)
recent_end = datetime(2026, 5, 25)

# 40% of customers will have recent orders (Active)
active_customer_ids = random.sample(customer_ids, k=int(len(customer_ids) * 0.4))

for cid in active_customer_ids:
    # Add 1-3 recent orders per active customer
    num_recent = random.randint(1, 3)
    for _ in range(num_recent):
        days_offset = random.randint(0, (recent_end - recent_start).days)
        order_date = recent_start + timedelta(days=days_offset)
        amount = round(random.uniform(50, 1500), 2)
        status = random.choice(['completed', 'completed', 'pending'])  # Bias toward completed
        orders.append([order_id, cid, order_date.strftime('%Y-%m-%d'), amount, status])
        order_id += 1

# Write orders
with open('data/orders.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['order_id', 'customer_id', 'order_date', 'amount', 'status'])
    writer.writerows(orders)

print(f"✅ Generated {len(orders)} orders")
print(f"📊 Data summary:")
print(f"   - Customers: {len(customers)}")
print(f"   - Orders: {len(orders)}")
print(f"   - Avg orders per customer: {len(orders) / len(customers):.1f}")
print(f"   - Date range: {start_date.date()} to {end_date.date()}")
print(f"   - Active customers (last 30 days): {len(active_customer_ids)}")
