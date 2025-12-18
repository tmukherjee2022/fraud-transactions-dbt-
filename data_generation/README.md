# Fraud Detection Data Generation

## Overview
Generates synthetic e-commerce transaction data with embedded fraud patterns for dbt Snowflake portfolio project.

## Setup

1. Create and activate virtual environment:
```bash
python3 -m venv data_gen_venv
source data_gen_venv/bin/activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

Run the data generation script:
```bash
python generate_fraud_data.py
```

This will create 8 CSV files:
- `customers.csv` - Customer information (10,000 records)
- `orders.csv` - Order transactions with fraud patterns (50,000 records)
- `order_items.csv` - Line items for each order
- `products.csv` - Product catalog (500 products)
- `stores.csv` - Store locations (50 stores)
- `employees.csv` - Employee information (200 employees)
- `dates.csv` - Date dimension table
- `suppliers.csv` - Supplier information (30 suppliers)

## Fraud Patterns Embedded
1. High-risk customer segments (5% of customers with 40% fraud rate)
2. Late-night transactions (1-5 AM)
3. Higher order quantities (5-15 items vs 1-5 for legitimate)
4. Shared IP addresses across fraudulent accounts
5. Payment method preferences (credit cards, gift cards)
6. Higher average order values

## Next Steps
Upload CSVs to Snowflake RAW schema and build dbt transformation models.
