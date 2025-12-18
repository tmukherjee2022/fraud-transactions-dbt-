# Fraud Detection Data Pipeline - dbt + Snowflake

E-commerce fraud detection system using synthetic transaction data, dbt transformations, and Snowflake data warehouse.

## 🎯 Project Overview

This portfolio project demonstrates end-to-end data engineering skills for fraud detection in e-commerce transactions, built with modern ELT practices.

**Tech Stack:**
- **Data Warehouse:** Snowflake
- **Transformation:** dbt (data build tool)
- **Data Generation:** Python (Faker, Pandas, NumPy)
- **Version Control:** Git/GitHub

## 📊 Project Structure
```
fraud-transactions-dbt/
├── data_generation/          # Synthetic data generation scripts
│   ├── generate_fraud_data.py
│   ├── requirements.txt
│   └── README.md
│
├── oms_dbt_proj/            # dbt transformation models
│   ├── models/
│   │   ├── staging/         # Clean, typed source data
│   │   ├── intermediate/    # Business logic transformations
│   │   └── marts/          # Analytics-ready models
│   ├── tests/
│   └── dbt_project.yml
│
└── .gitignore
```

## 🚀 Getting Started

### Prerequisites
- Python 3.10+
- Snowflake account
- dbt-core and dbt-snowflake

### 1. Data Generation
```bash
cd data_generation
python3 -m venv data_gen_venv
source data_gen_venv/bin/activate
pip install -r requirements.txt
python generate_fraud_data.py
```

### 2. Load Data to Snowflake

1. Create schemas in Snowflake: `RAW`, `STAGING`, `ANALYTICS`
2. Create internal stage for CSV uploads
3. Upload generated CSVs
4. Run COPY INTO commands to load tables

### 3. Run dbt Transformations
```bash
cd oms_dbt_proj
python3 -m venv ../dbt_venv
source ../dbt_venv/bin/activate
pip install dbt-core dbt-snowflake
dbt debug  # Verify connection
dbt run    # Run transformations
dbt test   # Run data quality tests
```

## 📈 Data Model

### Source Tables (RAW Schema)
| Table | Records | Description |
|-------|---------|-------------|
| customers | 10,000 | Customer master data |
| orders | 50,000 | Order transactions (~3% fraudulent) |
| order_items | 150,000+ | Line-level order details |
| products | 500 | Product catalog |
| stores | 50 | Store locations |
| employees | 200 | Employee information |
| suppliers | 30 | Supplier data |
| dates | 1,095+ | Date dimension |

### Key Fraud Indicators
- **Temporal patterns:** Late-night transactions (1-5 AM)
- **Network patterns:** Shared IP addresses across accounts
- **Behavioral patterns:** High order quantities (5-15 items)
- **Payment patterns:** Preference for credit cards and gift cards
- **Value patterns:** Higher average order values ($500+ vs $150)

## 🎓 Skills Demonstrated

- **Data Engineering:** ELT pipeline design, dimensional modeling, staging patterns
- **dbt Best Practices:** Modular SQL, ref() functions, incremental models
- **SQL Mastery:** Complex joins, window functions, CTEs, aggregations
- **Data Quality:** dbt tests (uniqueness, not_null, relationships, accepted_values)
- **Version Control:** Git workflows, .gitignore security patterns
- **Domain Knowledge:** Fraud detection, e-commerce analytics, risk scoring

## 🔐 Security

Snowflake credentials are stored locally in `~/.dbt/profiles.yml` and never committed to version control. The `.gitignore` file prevents accidental credential exposure.

## 📝 Configuration

Create `~/.dbt/profiles.yml` with your Snowflake credentials:
```yaml
oms_dbt_project:
  target: dev
  outputs:
    dev:
      type: snowflake
      account: YOUR_ACCOUNT.us-east-1
      user: YOUR_USERNAME
      password: YOUR_PASSWORD
      role: ACCOUNTADMIN
      database: DBTPROJECT
      warehouse: COMPUTE_WH
      schema: ANALYTICS
      threads: 4
```

## 📊 Future Enhancements

- [ ] Real-time fraud scoring with Snowflake streams
- [ ] Machine learning model integration for anomaly detection
- [ ] Dashboard visualization with Tableau/Looker
- [ ] Automated alerting for high-risk transactions
- [ ] A/B testing framework for fraud rules

## 📫 Contact

Built by Tanaya Mukherjee as a portfolio project demonstrating production-ready data engineering practices.


