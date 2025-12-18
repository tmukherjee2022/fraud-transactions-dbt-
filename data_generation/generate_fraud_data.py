import pandas as pd
import numpy as np
from faker import Faker
from datetime import datetime, timedelta
import random

# Initialize Faker
fake = Faker()
Faker.seed(42)
np.random.seed(42)
random.seed(42)

# Configuration
NUM_CUSTOMERS = 10000
NUM_STORES = 50
NUM_EMPLOYEES = 200
NUM_SUPPLIERS = 30
NUM_PRODUCTS = 500
NUM_ORDERS = 50000
FRAUD_RATE = 0.03  # 3% of transactions are fraudulent

# Date range for historical data
START_DATE = datetime(2023, 1, 1)
END_DATE = datetime(2025, 12, 18)

print("Generating synthetic e-commerce data with fraud patterns...")

# ============================================================================
# 1. DATES DIMENSION TABLE
# ============================================================================
print("\n1. Creating Dates dimension...")

def generate_dates_dimension(start_date, end_date):
    dates = pd.date_range(start=start_date, end=end_date, freq='D')
    
    dates_data = []
    for date in dates:
        dates_data.append({
            'Date': date.date(),
            'Day': date.strftime('%A')[:3],  # Mon, Tue, etc.
            'Month': date.strftime('%B')[:10],  # January, etc.
            'Year': str(date.year)[:4],
            'Quarter': f'Q{date.quarter}',
            'DayOfWeek': date.strftime('%A')[:10],
            'WeekOfYear': date.isocalendar()[1],
            'Updated_at': datetime.now()
        })
    
    return pd.DataFrame(dates_data)

df_dates = generate_dates_dimension(START_DATE, END_DATE)

# ============================================================================
# 2. STORES TABLE
# ============================================================================
print("2. Creating Stores table...")

stores_data = []
for store_id in range(1, NUM_STORES + 1):
    stores_data.append({
        'StoreID': store_id,
        'StoreName': f"{fake.company()} - {fake.city()}",
        'Address': fake.street_address()[:200],
        'City': fake.city()[:50],
        'State': fake.state_abbr()[:50],
        'ZipCode': fake.zipcode()[:10],
        'Email': fake.company_email()[:200],
        'Phone': fake.phone_number()[:50],
        'Updated_at': datetime.now()
    })

df_stores = pd.DataFrame(stores_data)

# ============================================================================
# 3. EMPLOYEES TABLE
# ============================================================================
print("3. Creating Employees table...")

employees_data = []
for emp_id in range(1, NUM_EMPLOYEES + 1):
    hire_date = fake.date_between(start_date='-5y', end_date='today')
    
    employees_data.append({
        'EmployeeID': emp_id,
        'FirstName': fake.first_name()[:100],
        'LastName': fake.last_name()[:100],
        'Email': fake.email()[:200],
        'JobTitle': random.choice(['Sales Associate', 'Store Manager', 'Assistant Manager', 
                                  'Cashier', 'Stock Clerk', 'Department Manager'])[:100],
        'HireDate': hire_date,
        'ManagerID': random.choice([None] + list(range(1, min(20, NUM_EMPLOYEES)))),
        'Address': fake.street_address()[:200],
        'City': fake.city()[:50],
        'State': fake.state_abbr()[:50],
        'ZipCode': fake.zipcode()[:10],
        'Updated_at': datetime.now()
    })

df_employees = pd.DataFrame(employees_data)

# ============================================================================
# 4. SUPPLIERS TABLE
# ============================================================================
print("4. Creating Suppliers table...")

suppliers_data = []
for supplier_id in range(1, NUM_SUPPLIERS + 1):
    suppliers_data.append({
        'SupplierID': supplier_id,
        'SupplierName': fake.company()[:100],
        'ContactPerson': fake.name()[:100],
        'Email': fake.company_email()[:200],
        'Phone': fake.phone_number()[:50],
        'Address': fake.street_address()[:50],
        'City': fake.city()[:50],
        'State': fake.state_abbr()[:10],
        'ZipCode': fake.zipcode()[:10],
        'Updated_at': datetime.now()
    })

df_suppliers = pd.DataFrame(suppliers_data)

# ============================================================================
# 5. PRODUCTS TABLE
# ============================================================================
print("5. Creating Products table...")

categories = ['Electronics', 'Clothing', 'Home & Garden', 'Sports', 'Toys', 
              'Books', 'Beauty', 'Automotive', 'Food', 'Health']

products_data = []
for product_id in range(1, NUM_PRODUCTS + 1):
    category = random.choice(categories)
    retail_price = round(random.uniform(5.99, 999.99), 2)
    supplier_price = round(retail_price * random.uniform(0.4, 0.7), 2)
    
    products_data.append({
        'ProductID': product_id,
        'Name': fake.catch_phrase()[:100],
        'Category': category[:100],
        'RetailPrice': retail_price,
        'SupplierPrice': supplier_price,
        'SupplierID': random.randint(1, NUM_SUPPLIERS),
        'Updated_at': datetime.now()
    })

df_products = pd.DataFrame(products_data)

# ============================================================================
# 6. CUSTOMERS TABLE (with fraud risk indicators)
# ============================================================================
print("6. Creating Customers table...")

customers_data = []
# Create some high-risk customers (fraudsters)
high_risk_customer_ids = random.sample(range(1, NUM_CUSTOMERS + 1), int(NUM_CUSTOMERS * 0.05))

for customer_id in range(1, NUM_CUSTOMERS + 1):
    is_high_risk = customer_id in high_risk_customer_ids
    
    customers_data.append({
        'CustomerID': customer_id,
        'FirstName': fake.first_name()[:100],
        'LastName': fake.last_name()[:100],
        'Email': fake.email()[:200],
        'Phone': fake.phone_number()[:50],
        'Address': fake.street_address()[:200],
        'City': fake.city()[:50],
        'State': fake.state_abbr()[:50],
        'ZipCode': fake.zipcode()[:10],
        'Updated_at': datetime.now(),
        # Hidden field for fraud generation (won't export to final table)
        '_is_high_risk': is_high_risk
    })

df_customers = pd.DataFrame(customers_data)

# ============================================================================
# 7. ORDERS TABLE (with fraud patterns)
# ============================================================================
print("7. Creating Orders table with fraud patterns...")

order_statuses = ['Completed', 'Pending', 'Cancelled', 'Refunded', 'Shipped']

orders_data = []
fraud_indicators = []

for order_id in range(1, NUM_ORDERS + 1):
    customer_id = random.randint(1, NUM_CUSTOMERS)
    is_high_risk_customer = customer_id in high_risk_customer_ids
    
    # Determine if this order is fraudulent
    is_fraud = random.random() < FRAUD_RATE
    
    # If customer is high risk, increase fraud probability
    if is_high_risk_customer:
        is_fraud = random.random() < 0.4  # 40% fraud rate for high-risk customers
    
    order_date = fake.date_time_between(start_date=START_DATE, end_date=END_DATE)
    
    # Fraud pattern 1: Unusual order times (late night/early morning)
    if is_fraud and random.random() < 0.6:
        order_date = order_date.replace(hour=random.randint(1, 5))
    
    # Fraud pattern 2: Different shipping/billing locations
    shipping_state_different = is_fraud and random.random() < 0.7
    
    orders_data.append({
        'OrderID': order_id,
        'OrderDate': order_date.date(),
        'CustomerID': customer_id,
        'EmployeeID': random.randint(1, NUM_EMPLOYEES),
        'StoreID': random.randint(1, NUM_STORES),
        'Status': random.choice(order_statuses)[:10],
        'Updated_at': datetime.now(),
        # Hidden fields for fraud analysis
        '_is_fraud': is_fraud,
        '_order_hour': order_date.hour,
        '_shipping_state_different': shipping_state_different
    })
    
    # Track fraud indicators for later analysis
    fraud_indicators.append({
        'OrderID': order_id,
        'IsFraud': is_fraud,
        'CustomerID': customer_id,
        'OrderHour': order_date.hour,
        'IsHighRiskCustomer': is_high_risk_customer
    })

df_orders = pd.DataFrame(orders_data)
df_fraud_indicators = pd.DataFrame(fraud_indicators)

# ============================================================================
# 8. ORDER ITEMS TABLE (with fraud patterns in quantities/prices)
# ============================================================================
print("8. Creating OrderItems table...")

order_items_data = []
order_item_id = 1

for _, order in df_orders.iterrows():
    order_id = order['OrderID']
    is_fraud = order['_is_fraud']
    
    # Fraud pattern 3: Fraudulent orders tend to have more items
    if is_fraud:
        num_items = random.randint(5, 15)  # More items
    else:
        num_items = random.randint(1, 5)  # Normal orders
    
    # Select random products for this order
    selected_products = random.sample(range(1, NUM_PRODUCTS + 1), num_items)
    
    for product_id in selected_products:
        product_price = df_products[df_products['ProductID'] == product_id]['RetailPrice'].values[0]
        
        # Fraud pattern 4: High-value items in fraudulent orders
        if is_fraud:
            quantity = random.randint(2, 10)  # Higher quantities
            # Sometimes discounted prices (stolen cards don't care about deals)
            unit_price = round(product_price * random.uniform(0.8, 1.0), 2)
        else:
            quantity = random.randint(1, 3)  # Normal quantities
            unit_price = product_price
        
        order_items_data.append({
            'OrderItemID': order_item_id,
            'OrderID': order_id,
            'ProductID': product_id,
            'Quantity': quantity,
            'UnitPrice': unit_price,
            'Updated_at': datetime.now()
        })
        
        order_item_id += 1

df_order_items = pd.DataFrame(order_items_data)

# ============================================================================
# CALCULATE ORDER TOTALS & ADD FRAUD PATTERNS
# ============================================================================
print("\n9. Calculating order totals and finalizing fraud patterns...")

# Calculate total amount per order
order_totals = df_order_items.groupby('OrderID').apply(
    lambda x: (x['Quantity'] * x['UnitPrice']).sum()
).reset_index()
order_totals.columns = ['OrderID', 'OrderTotal']

# Merge back to orders
df_orders = df_orders.merge(order_totals, on='OrderID', how='left')

# Add payment method and fraud indicators
payment_methods = ['Credit Card', 'Debit Card', 'PayPal', 'Gift Card', 'Cash']

def assign_payment_method(row):
    if row['_is_fraud']:
        # Fraudsters prefer credit cards and gift cards
        return random.choice(['Credit Card', 'Gift Card', 'Credit Card', 'Credit Card'])
    else:
        return random.choice(payment_methods)

df_orders['PaymentMethod'] = df_orders.apply(assign_payment_method, axis=1)

# Add IP address (fraud pattern: same IP for multiple customers)
fraudster_ips = [fake.ipv4() for _ in range(20)]

def assign_ip(row):
    if row['_is_fraud'] and random.random() < 0.6:
        return random.choice(fraudster_ips)  # Shared IPs for fraudsters
    else:
        return fake.ipv4()

df_orders['IPAddress'] = df_orders.apply(assign_ip, axis=1)

# Add device fingerprint
def assign_device(row):
    if row['_is_fraud']:
        return random.choice(['Mobile', 'Desktop', 'Tablet'])
    else:
        return random.choice(['Mobile', 'Mobile', 'Desktop', 'Tablet'])  # More mobile for legit

df_orders['DeviceType'] = df_orders.apply(assign_device, axis=1)

# ============================================================================
# EXPORT DATA TO CSV
# ============================================================================
print("\n10. Exporting data to CSV files...")

# Clean up hidden columns before export
df_customers_clean = df_customers.drop(columns=['_is_high_risk'])
df_orders_clean = df_orders.drop(columns=['_is_fraud', '_order_hour', '_shipping_state_different'])

# Export all tables
df_dates.to_csv('dates.csv', index=False)
df_stores.to_csv('stores.csv', index=False)
df_employees.to_csv('employees.csv', index=False)
df_suppliers.to_csv('suppliers.csv', index=False)
df_products.to_csv('products.csv', index=False)
df_customers_clean.to_csv('customers.csv', index=False)
df_orders_clean.to_csv('orders.csv', index=False)
df_order_items.to_csv('order_items.csv', index=False)

# Export fraud indicators separately (for your reference/validation)
df_fraud_indicators.to_csv('fraud_labels.csv', index=False)

# ============================================================================
# SUMMARY STATISTICS
# ============================================================================
print("\n" + "="*70)
print("DATA GENERATION COMPLETE!")
print("="*70)
print(f"\n📊 Summary Statistics:")
print(f"   • Customers: {len(df_customers):,}")
print(f"   • Orders: {len(df_orders):,}")
print(f"   • Order Items: {len(df_order_items):,}")
print(f"   • Products: {len(df_products):,}")
print(f"   • Stores: {len(df_stores):,}")
print(f"   • Employees: {len(df_employees):,}")
print(f"   • Suppliers: {len(df_suppliers):,}")
print(f"   • Date Records: {len(df_dates):,}")

print(f"\n🚨 Fraud Statistics:")
print(f"   • Fraudulent Orders: {df_fraud_indicators['IsFraud'].sum():,} ({df_fraud_indicators['IsFraud'].mean()*100:.1f}%)")
print(f"   • High-Risk Customers: {len(high_risk_customer_ids):,}")

print(f"\n💰 Order Value Statistics:")
print(f"   • Average Order Value: ${df_orders['OrderTotal'].mean():.2f}")
print(f"   • Median Order Value: ${df_orders['OrderTotal'].median():.2f}")
print(f"   • Total Revenue: ${df_orders['OrderTotal'].sum():,.2f}")

fraud_orders = df_orders[df_orders['_is_fraud'] == True]
legit_orders = df_orders[df_orders['_is_fraud'] == False]

print(f"\n   • Avg Fraudulent Order: ${fraud_orders['OrderTotal'].mean():.2f}")
print(f"   • Avg Legitimate Order: ${legit_orders['OrderTotal'].mean():.2f}")

print("\n📁 Files Created:")
print("   ✓ customers.csv")
print("   ✓ orders.csv")
print("   ✓ order_items.csv")
print("   ✓ products.csv")
print("   ✓ stores.csv")
print("   ✓ employees.csv")
print("   ✓ dates.csv")
print("   ✓ suppliers.csv")
print("   ✓ fraud_labels.csv (for validation)")

print("\n🎯 Fraud Patterns Embedded:")
print("   1. High-risk customer segments (5% of customers)")
print("   2. Unusual transaction times (late night/early morning)")
print("   3. High order quantities and values")
print("   4. Shared IP addresses across different customers")
print("   5. Payment method preferences (credit cards, gift cards)")
print("   6. Multiple items per transaction")

print("\n✅ Ready for Snowflake upload!")
print("="*70)