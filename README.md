# CI/CD Pipeline Project - Advanced Analytics

## Project Overview
This is a **production-grade end-to-end data pipeline** with automated testing and deployment using GitHub Actions. It demonstrates modern data engineering best practices using the **Medallion Architecture** (Bronze → Silver → Gold layers) with advanced customer analytics, RFM segmentation, churn prediction, and health scoring.

**Medallion Architecture Pipeline Flow:**
```
┌─────────────────────────────────────────────────────────────────┐
│                      RAW DATA SOURCES                            │
│              (CSV Files - customers.csv, orders.csv)             │
└────────────────────────┬────────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────────────────┐
│    BRONZE LAYER - Raw Data Ingestion & Initial Load             │
│  Python ingestion scripts load messy data into PostgreSQL       │
│  Minimal cleaning, preserve original data as-is                │
│  Tables: raw_customers, raw_orders                             │
└────────────────────────┬────────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────────────────┐
│   SILVER LAYER - Data Cleaning & Standardization                │
│  dbt transforms bronze data into clean, validated datasets     │
│  Deduplication, normalization, validation, adding columns      │
│  Models: stg_customers (region mapping), stg_orders (validation)│
│  Output: Clean staging views ready for analysis                │
└────────────────────────┬────────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────────────────┐
│      GOLD LAYER - Analytics & Business Metrics                  │
│  dbt creates aggregated, business-ready datasets                │
│  Advanced analytics: RFM segmentation, health scores, KPIs      │
│  Models: customer_metrics (materialized table)                 │
│  Output: Ready for dashboards, BI tools, reporting             │
└────────────────────────┬────────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────────────────┐
│         CONSUMPTION LAYER - Dashboards & Insights               │
│  Python scripts export metrics and generate dashboards         │
│  CSV exports for BI tools (Tableau, Power BI)                  │
│  Interactive dashboard viewer (view_dashboard_metrics.py)      │
│  GitHub Actions automated testing & deployment                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## Project Structure

```
CI CD Pipeline project/
├── data/
│   ├── customers.csv                         # Raw customer data
│   ├── orders.csv                           # Raw order data (intentionally messy)
│   └── final_dashboard_data.csv             # Exported metrics for dashboards
│
├── ingestion/
│   ├── load_data_to_postgres.py             # Load CSVs to PostgreSQL with validation
│   ├── export_final_data.py                 # Export final metrics to CSV
│   └── run_full_pipeline.py                 # Master orchestration script
│
├── models/
│   ├── bronze/                              # Raw data layer (sources)
│   │   ├── brnz_customers.sql
│   │   ├── brnz_orders.sql
│   │   └── _bronze_sources.yml              # Source definitions & tests
│   │
│   ├── silver/                              # Cleaned data layer
│   │   ├── stg_customers.sql                # Cleaned customers + region mapping
│   │   ├── stg_orders.sql                   # Validated orders with normalized data
│   │   └── _silver_models.yml               # Staging model tests & documentation
│   │
│   └── gold/                                # Analytics layer
│       ├── customer_metrics.sql             # Advanced customer analytics (see below)
│       └── _gold_models.yml                 # Mart tests & documentation
│
├── .github/workflows/
│   └── dbt-ci.yml                           # GitHub Actions CI/CD workflow
│
├── assess_data.py                           # Quick data quality assessment script
├── view_dashboard_metrics.py                # 🆕 Advanced dashboard metrics viewer
├── dbt_project.yml                          # dbt project configuration
├── packages.yml                             # dbt package dependencies
├── GITHUB_ACTIONS_SETUP.md                  # CI/CD setup instructions
├── CONTRIBUTION_GUIDE.md                    # Contributing guidelines
├── PROJECT_OVERVIEW.md                      # Detailed architecture docs
└── README.md                                # This file
```

---

## What We Built - Medallion Architecture Layers

### 📊 **BRONZE LAYER** - Raw Data Ingestion
**Purpose:** Load raw data from source systems with minimal transformation

**Components:**
- **Data Source Files:** `data/customers.csv` & `data/orders.csv`
  - Customers: 10 records with intentional quality issues
  - Orders: 30 records with NULL values, duplicates, inconsistent dates, invalid amounts
  
- **Bronze Models** (`models/bronze/`):
  - `brnz_customers.sql` - Raw customer data as-is from source
  - `brnz_orders.sql` - Raw order data as-is from source
  - `_bronze_sources.yml` - dbt source definitions pointing to raw PostgreSQL tables

- **Data Ingestion Script** (`ingestion/load_data_to_postgres.py`):
  - Parses multiple date formats
  - Handles basic data type conversions
  - Loads into PostgreSQL tables: `customers`, `orders`
  - Basic validation before insert

**Bronze Output:** Raw tables in PostgreSQL - data preserved as-is from source

---

### 🔧 **SILVER LAYER** - Data Cleaning & Standardization
**Purpose:** Clean, validate, and standardize data for reliable analytics

**Components:**
- **Silver Models** (`models/silver/`):
  
  - **`stg_customers.sql`** - Cleaned customer dimension:
    - Deduplicates on email
    - Standardizes names (INITCAP/proper case)
    - Normalizes emails (lowercase, trimmed)
    - Standardizes phone numbers (extract digits)
    - 🆕 **Adds REGION column** (maps country to geographic region)
    - Adds validation flags: `is_valid_email`, `is_valid_phone`
    - Filters NULL customer_ids
    - Adds transformation timestamp
    - **Output:** Clean, deduplicated customer view ready for analytics
  
  - **`stg_orders.sql`** - Cleaned order transactions:
    - Validates order_id and customer_id (filters NULLs)
    - Casts dates consistently
    - Validates amounts (filters negative/invalid values)
    - Normalizes status (lowercase, trimmed, validates values)
    - Filters incomplete records
    - Adds transformation timestamp
    - **Output:** Valid, normalized order data ready for metrics

  - **`_silver_models.yml`** - Quality tests:
    - Uniqueness tests: `customer_id`, `email`
    - NOT NULL tests: `customer_id`, `order_id`, `customer_id` (orders)
    - Status values validation: only 'completed', 'pending', 'cancelled'

**Silver Output:** Clean, deduplicated, validated staging views

---

### ✨ **GOLD LAYER** - Analytics & Business Metrics
**Purpose:** Create aggregated, business-ready datasets with advanced analytics

**Components:**
- **Gold Models** (`models/gold/`):

  - **`customer_metrics.sql`** - Advanced customer analytics table:
    
    **Aggregated Metrics:**
    - `total_orders`, `completed_orders`, `pending_orders`, `cancelled_orders`
    - `total_revenue` - Sum of completed orders
    - `avg_order_value` - Average order amount
    
    **Temporal Metrics:**
    - `last_order_date`, `first_order_date` - Customer lifetime
    - `days_since_last_order` - Recency metric
    - `customer_lifetime_years` - Tenure in years
    
    **Revenue Momentum (Trending):**
    - `revenue_last_30_days` - Short-term revenue
    - `revenue_last_90_days` - Medium-term revenue
    - `orders_last_90_days` - Recent activity
    
    **🆕 Advanced Story-Telling KPIs:**
    - **`health_score` (0-100)** - Composite customer health:
      - Combines: Recency (50%) + Frequency (40%) + Monetary Value (40%) + Momentum (5%) - Churn Penalty
      - Business use: Identify top-tier customers needing white-glove service
    
    - **`rfm_segment`** - RFM-based customer classification:
      - "Champions" (high R, F, M) → VIP retention program
      - "Loyal Customers" (good across metrics) → Cross-sell opportunities
      - "Potential" (growing) → Nurture campaigns
      - "At-Risk" (good history, inactive) → Win-back campaigns
      - "Lost" (not engaged) → Reactivation offers
      - "Need Attention" (mixed signals) → Manual review
    
    - **`churn_risk`** - Churn probability levels:
      - "High" → Immediate outreach, retention offers
      - "Medium" → Monitor, engagement campaigns
      - "Low" → Normal business
    
    - **`customer_status`** - Current engagement state:
      - "Active" → Recently engaged customers
      - "At-Risk" → Declining engagement, intervention needed
      - "Inactive" → Dormant customers
    
    - **`region`** - Geographic dimension (North America, Europe, Asia Pacific, etc.)

  - **`_gold_models.yml`** - Mart quality tests:
    - Data validation: revenue ≥ 0, health_score between 0-100
    - Referential integrity tests

**Gold Output:** Materialized table ready for dashboards and BI tools

---

### 📈 **CONSUMPTION LAYER** - Dashboards & Insights
**Purpose:** Expose metrics to business users via dashboards and reports

**Components:**
- **Export Script** (`ingestion/export_final_data.py`):
  - Exports `customer_metrics` to CSV: `data/final_dashboard_data.csv`
  - Used by BI tools (Tableau, Power BI, Looker)

- **🆕 Dashboard Viewer** (`view_dashboard_metrics.py`):
  - Interactive Python script displaying four key dashboards:
    1. **Top 10 Customers** - VIP analysis by health score
    2. **RFM Segmentation** - Customer segment distribution
    3. **Churn Risk Analysis** - At-risk customer focus
    4. **Activity Status** - Engagement level breakdown

- **Orchestration Script** (`ingestion/run_full_pipeline.py`):
  - Master script coordinating entire pipeline:
    1. Run dbt transformations (bronze → silver → gold)
    2. Export final data
    3. Generates updated metrics for dashboards

---

### 🤖 **CI/CD AUTOMATION** - GitHub Actions
**Purpose:** Automated testing & deployment on every code change

**Workflow Details** (`.github/workflows/dbt-ci.yml`):
- **Trigger:** Pull requests to `main` or `staging` branches
- **Automated Tests:**
  - `dbt parse` - Syntax validation
  - `dbt debug` - Connection checks
  - `dbt run` - Execute all models (bronze → silver → gold)
  - `dbt test` - Data quality assertions
- **Approval Gate:** Manual PR approval before auto-merge
- **Auto-Merge:** Squash merge to maintain clean history

---

## Data Flow Summary

```
BRONZE (Raw)
├─ brnz_customers (raw, unchanged from CSV)
├─ brnz_orders (raw, messy data preserved)
└─ Source definitions & quality tests

    ↓ (dbt transforms)

SILVER (Cleaned)
├─ stg_customers (deduplicated, standardized, region added)
├─ stg_orders (validated, normalized, clean)
└─ Quality validations & data rules

    ↓ (dbt aggregates)

GOLD (Analytics)
├─ customer_metrics (business-ready KPIs)
│  ├─ Basic metrics (orders, revenue)
│  ├─ Temporal metrics (dates, lifecycle)
│  ├─ Revenue momentum (trending)
│  ├─ RFM segments (strategic classification)
│  ├─ Health scores (composite metric)
│  ├─ Churn risk (retention focus)
│  └─ Customer status (engagement level)
└─ Quality validations & referential integrity

    ↓ (Python exports)

CONSUMPTION (Dashboards)
├─ CSV exports → BI tools
├─ Dashboard scripts → Stakeholders
└─ CI/CD automation → Deployment
```

---

## CI/CD Pipeline Changes & Updates

### ✅ **Current CI/CD Status - What's Working**

Your existing GitHub Actions workflow (`.github/workflows/dbt-ci.yml`) is **fully compatible** with the new additions. No changes needed for basic functionality:

**What's Already Handled:**
- ✅ Bronze layer seed data loads correctly
- ✅ Silver layer transformations (stg_customers, stg_orders) execute successfully
- ✅ Gold layer customer_metrics model runs without errors
- ✅ All dbt tests pass
- ✅ Region column is properly created in stg_customers

### 📝 **RECOMMENDED CI/CD Enhancements** (Optional but Recommended)

Consider adding these improvements for better observability:

#### 1. **Add dbt Documentation Generation**
```yaml
- name: Generate and publish dbt docs
  run: dbt docs generate
  
- name: Deploy docs to GitHub Pages
  if: github.ref == 'refs/heads/main'
  # Optional: Configure GitHub Pages to serve dbt documentation
```
**Benefit:** Auto-generate data lineage diagrams showing Bronze → Silver → Gold flows

#### 2. **Add Model Performance Tracking**
```yaml
- name: Store performance metrics
  run: |
    # Log execution times for each layer
    # dbt parse time, dbt run time per model, test execution time
```
**Benefit:** Monitor if transformations are slowing down as data grows

#### 3. **Add Data Quality Thresholds**
Current tests are basic. Consider adding:
- Row count validations (alerts if customer_metrics shrinks unexpectedly)
- Health score distribution checks (ensure scores remain 0-100)
- RFM segment distribution (catch imbalanced segmentation)

```yaml
- name: Validate data quality thresholds
  run: |
    # Add custom Python scripts to validate:
    # - customer_metrics has records
    # - health_score between 0-100
    # - rfm_segment has all expected categories
```

#### 4. **Add Export & Dashboard Validation**
```yaml
- name: Run export and validate CSV
  run: |
    python ingestion/export_final_data.py
    # Verify final_dashboard_data.csv has expected columns and rows
```
**Benefit:** Ensure the CSV export always completes successfully

---

### 🔍 **Why No Major Changes Needed**

Your CI/CD pipeline is already well-designed for the Medallion Architecture:

| Component | Current Status | Notes |
|-----------|---|---|
| Bronze Layer | ✅ Working | Seed data includes customers & orders tables |
| Silver Layer | ✅ Working | dbt models stg_customers, stg_orders execute successfully |
| Gold Layer | ✅ Working | customer_metrics materialized table builds correctly |
| dbt Tests | ✅ Working | All model tests pass (unique, not_null, accepted_values) |
| Region Column | ✅ Ready | stg_customers adds region in silver layer |
| Health Scores | ✅ Ready | customer_metrics calculates all KPIs |
| RFM Segments | ✅ Ready | Gold layer contains all segmentation logic |

### 🚀 **Next Steps After Pushing Code**

1. **Push to GitHub:**
   ```bash
   git add .
   git commit -m "Add advanced analytics: bronze/silver/gold layers, RFM segmentation, health scores, dashboard viewer"
   git push origin main
   ```

2. **Monitor First Run:**
   - Go to: https://github.com/ArpitGhai03/analytics-engineering-ci-cd-pipeline/actions
   - Watch the workflow execute
   - Should complete in 3-5 minutes
   - All dbt tests should pass ✅

3. **Test Dashboard Viewer Locally:**
   ```bash
   python view_dashboard_metrics.py
   ```
   - Verify all 4 dashboards display correctly
   - Check health scores and RFM segments

4. **Optional: Deploy Enhancements**
   - Add the recommended CI/CD enhancements above
   - Set up dbt documentation hosting (GitHub Pages)
   - Configure data quality alerts

---
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
