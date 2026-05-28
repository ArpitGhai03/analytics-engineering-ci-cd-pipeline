# CI/CD Pipeline Project - Summary

## Project Overview
This is a complete end-to-end data pipeline project that demonstrates data ingestion, transformation, and export using Python, PostgreSQL, and dbt.

**Pipeline Flow:**
```
CSV Files (Raw Data) 
    ↓
Python Ingestion (Load to PostgreSQL)
    ↓
dbt Staging (Clean & Validate)
    ↓
dbt Marts (Create KPIs & Metrics)
    ↓
Export to Database & CSV
```

---

## Project Structure

```
CI CD Pipeline project/
├── data/
│   ├── customers.csv                    # Raw customer data (with some messy data)
│   ├── orders.csv                       # Raw order data (with nulls, duplicates, etc.)
│   └── final_dashboard_data.csv         # Final cleaned & transformed dashboard data
│
├── ingestion/
│   ├── load_data_to_postgres.py         # Script to load raw CSV data into PostgreSQL
│   ├── export_final_data.py             # Script to export final metrics to CSV
│   └── run_full_pipeline.py             # Master script - runs dbt + exports data
│
├── models/
│   ├── staging/
│   │   ├── stg_customers.sql            # dbt model - clean customer data
│   │   ├── stg_orders.sql               # dbt model - clean order data
│   │   └── sources.yml                  # dbt source definitions
│   │
│   └── marts/
│       └── customer_metrics.sql         # dbt model - KPI metrics table
│
├── dbt_project.yml                      # dbt project configuration
└── README.md                            # This file
```

---

## What We Built

### 1. **Raw Data Files** (`data/`)
- **customers.csv**: 10 customer records with fields: customer_id, name, email, phone, country
- **orders.csv**: 30 orders with intentional data quality issues:
  - NULL values (missing amounts, customer IDs, dates)
  - Inconsistent date formats (YYYY-MM-DD, MM/DD/YYYY, DD/MM/YYYY)
  - Invalid amounts (negative values, non-numeric strings)
  - Duplicate order IDs
  - Mixed case status values

### 2. **Data Ingestion** (`ingestion/load_data_to_postgres.py`)
Loads messy CSV data into PostgreSQL with intelligent error handling:
- Parses multiple date formats
- Converts invalid amounts to NULL
- Normalizes status values
- Skips duplicate records
- Creates proper table schema with foreign key constraints

**Database Tables Created:**
- `customers` - Clean customer dimension
- `orders` - Clean fact table with foreign key to customers

### 3. **dbt Staging Layer** (`models/staging/`)
Cleans and validates raw data:
- **stg_customers.sql**: Filters NULL customer_ids, adds timestamp
- **stg_orders.sql**: 
  - Validates order_id and customer_id
  - Casts date formats consistently
  - Handles invalid amounts
  - Normalizes status (lowercase, trimmed)
  - Filters incomplete records

### 4. **dbt Marts Layer** (`models/marts/`)
Creates business KPIs and dashboard metrics:
- **customer_metrics.sql** table includes:
  - `total_orders` - Total orders per customer
  - `completed_orders` - Successfully completed order count
  - `pending_orders` - Pending order count
  - `total_revenue` - Sum of completed order amounts
  - `avg_order_value` - Average order amount
  - `days_as_customer` - Customer tenure (in days)
  - `last_order_date` - Most recent order date
  - `first_order_date` - Oldest order date
  - Sorted by total_revenue (DESC) for easy ranking

### 5. **Export Process** (`ingestion/export_final_data.py`)
Exports final metrics to CSV for dashboard consumption:
- Queries `customer_metrics` table
- Saves to `data/final_dashboard_data.csv`
- Includes all KPI columns

---

## PostgreSQL Connection Details
```
Host: localhost
Port: 5432
Database: dbt_project
User: postgres
Password: Arpit_123
```

---

## How to Run

### Prerequisites
```bash
# Install required Python packages
pip install pandas psycopg2-binary

# Ensure PostgreSQL is running
# Ensure dbt is installed (already installed on your system)
```

### Option 1: Run Complete Pipeline (Recommended)
```bash
python ingestion/run_full_pipeline.py
```
This will:
1. Execute `dbt run` (create/update staging views and marts table)
2. Export final data to CSV
3. Update the `customer_metrics` table in PostgreSQL

### Option 2: Step-by-Step
```bash
# Step 1: Load raw CSV data to PostgreSQL
python ingestion/load_data_to_postgres.py

# Step 2: Run dbt transformations
dbt run

# Step 3: Export final data to CSV
python ingestion/export_final_data.py
```

---

## CI/CD Pipeline (GitHub Actions)

This project includes an automated CI/CD pipeline using GitHub Actions that validates all changes before merging to production.

### How It Works

#### 1. **Trigger** 🚀
- Automatically activates when you create a Pull Request (PR) to `main` or `staging` branch
- Only runs if changes are in: `models/`, `dbt_project.yml`, `ingestion/`, or workflow files

#### 2. **Automated Tests** ✅
The pipeline runs the following checks automatically (~3-5 minutes):
- **`dbt parse`** - Validates dbt syntax
- **`dbt debug`** - Checks database connection
- **`dbt run`** - Executes all models (staging + marts)
- **`dbt test`** - Runs data quality tests:
  - `customer_id`: must be unique and not null
  - `email`: must be unique
  - `order_id`: must be unique and not null
  - `status`: only allowed values (completed, pending, cancelled)
  - `total_revenue`: must be ≥ 0

**If tests fail:** ❌ PR is blocked with error details in comments

#### 3. **Approval & Auto-Merge** 🚀
- Once all tests pass ✅, the PR requires your manual approval
- You review the changes on GitHub and approve
- Auto-merge happens automatically using squash merge (clean commit history)

### Creating a Change

```bash
# Create feature branch
git checkout -b feature/new-model

# Make changes to models or ingestion scripts
git add models/ ingestion/
git commit -m "Add new model or feature"
git push -u origin feature/new-model

# Create Pull Request on GitHub
# GitHub Actions runs tests automatically
# Review results and approve
# Auto-merge to main happens automatically
```

### View Workflow Runs
1. Go to: https://github.com/ArpitGhai03/analytics-engineering-ci-cd-pipeline/actions
2. View test results, logs, and approval status

### Setup Details
See [GITHUB_ACTIONS_SETUP.md](GITHUB_ACTIONS_SETUP.md) for:
- Initial GitHub setup instructions
- Detailed workflow configuration
- Environment variables and secrets
- Troubleshooting guide

---

## Database Objects Created

### Tables
- `customers` - Raw customer data
- `orders` - Raw order data
- `customer_metrics` - Final KPI metrics (materialized table)

### Views
- `stg_customers` - Cleaned customer staging view
- `stg_orders` - Cleaned orders staging view

---

## Output Files

### Data Files
- `data/customers.csv` - Raw customer data with 10 records
- `data/orders.csv` - Raw order data with 30 records (messy)
- `data/final_dashboard_data.csv` - Cleaned, transformed metrics ready for dashboards

### Results
- **Database**: `customer_metrics` table with 10 customer records and their KPIs
- **CSV**: Final dashboard data exported for BI tools (Tableau, Power BI, etc.)

---

## Data Quality Improvements

**Raw Data Issues Handled:**
- ✓ NULL values in critical fields
- ✓ Inconsistent date formatting
- ✓ Invalid numeric values (negative, text)
- ✓ Duplicate records
- ✓ Inconsistent case/formatting

**Staging Results:**
- 10/10 customers successfully loaded
- 29/30 orders successfully loaded (1 duplicate skipped)
- All data normalized and validated
- Ready for analytics and reporting

---

## Technology Stack
- **Language**: Python 3.13
- **Data Warehouse**: PostgreSQL
- **Transformation Tool**: dbt (1.10.8)
- **Python Libraries**: pandas, psycopg2
- **Data Format**: CSV

---

## Key Features
✅ End-to-end automated pipeline
✅ Intelligent data quality handling
✅ Staging layer for data cleaning
✅ Marts layer for business metrics
✅ Single command execution (`run_full_pipeline.py`)
✅ Database + CSV export
✅ Reproducible and scalable

---

## Next Steps for Production
- Add dbt tests for data validation
- Implement data quality checks
- Schedule automated runs (cron/airflow)
- Add logging and monitoring
- Create data lineage documentation
- Set up CI/CD with git integration

---

## Summary Statistics
- **Total Customers**: 10
- **Total Orders**: 30 (raw), 29 (cleaned)
- **Data Quality**: Handles messy real-world data
- **Transformation Logic**: 3 dbt models (2 views, 1 table)
- **Output**: 10 customer KPI records with business metrics

---

**Created**: May 23, 2026
**Status**: ✓ Complete and Tested
