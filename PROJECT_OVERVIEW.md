# Analytics Engineering CI/CD Pipeline - Complete Project Overview

## 🎯 Project Vision

This is an **end-to-end data pipeline** with **automated testing and deployment** using GitHub Actions. It demonstrates modern data engineering best practices combining Python, PostgreSQL, dbt, and CI/CD automation.

---

## 📊 Project Architecture

```
Raw CSV Data
    ↓
Python Ingestion (data validation, cleaning)
    ↓
PostgreSQL (raw tables)
    ↓
dbt Staging Layer (data cleansing & validation)
    ↓
dbt Marts Layer (aggregations & business metrics)
    ↓
Export & Dashboard
    ↓
GitHub Actions (automated testing & deployment)
```

---

## 🗂️ Project Structure

```
CI CD Pipeline project/
├── data/                              # Raw CSV data
│   ├── customers.csv                 # 10 customers (clean data)
│   ├── orders.csv                    # 30 orders (messy data with quality issues)
│   └── final_dashboard_data.csv      # Exported metrics output
│
├── ingestion/                         # Python scripts
│   ├── load_data_to_postgres.py      # Load CSVs to PostgreSQL with validation
│   ├── export_final_data.py          # Export metrics to CSV
│   └── run_full_pipeline.py          # Master orchestration script
│
├── models/                            # dbt transformation models
│   ├── staging/
│   │   ├── stg_customers.sql         # Clean customer data (VIEW)
│   │   ├── stg_orders.sql            # Clean order data (VIEW)
│   │   ├── sources.yml               # Source definitions & tests
│   │   └── stg_models.yml            # Staging model tests
│   │
│   └── marts/
│       ├── customer_metrics.sql      # Customer KPIs (MATERIALIZED TABLE)
│       └── marts_models.yml          # Mart tests
│
├── dbt_project.yml                    # dbt configuration
├── .github/
│   └── workflows/
│       └── dbt-ci.yml                # GitHub Actions workflow
│
├── README.md                          # Quick start guide
├── GITHUB_ACTIONS_SETUP.md           # Workflow instructions
└── PROJECT_OVERVIEW.md               # This file
```

---

## 📦 Data Pipeline Components

### 1. **Raw Data Layer** (`data/`)

#### `customers.csv` (10 records)
- Clean customer records with: customer_id, customer_name, email, phone, country
- No data quality issues

#### `orders.csv` (30 records - INTENTIONALLY MESSY)
- Contains real-world data quality issues:
  - ✗ NULL values in order_id, customer_id, amount, status
  - ✗ Duplicate order IDs
  - ✗ Invalid amounts (negative values)
  - ✗ Inconsistent date formats (YYYY-MM-DD, DD/MM/YYYY, MM-DD-YYYY)
  - ✗ Mixed-case statuses (Completed, PENDING, cancelled)

**Result after ingestion:** 29/30 orders loaded (1 duplicate skipped)

---

### 2. **Python Ingestion Layer** (`ingestion/`)

#### `load_data_to_postgres.py`
Cleans and validates data before loading:
- **Date parsing:** Handles 3 different date formats
- **Amount validation:** Converts to float, filters negative values
- **Status normalization:** Converts to lowercase and trims whitespace
- **Duplicate detection:** Skips records with duplicate order_id
- **NULL handling:** Filters incomplete records
- **Result:** 10/10 customers, 29/30 orders successfully loaded

#### `export_final_data.py`
Exports the final `customer_metrics` table to CSV for dashboards/reports

#### `run_full_pipeline.py`
Master orchestration script that runs the complete pipeline:
1. Runs `dbt deps` (install dependencies)
2. Runs `dbt run` (execute all models)
3. Runs `dbt test` (validate data quality)
4. Exports final metrics to CSV

---

### 3. **dbt Staging Layer** (`models/staging/`)

Transforms raw data into clean, validated datasets.

#### `stg_customers.sql`
```sql
SELECT
  customer_id,
  customer_name,
  email,
  phone,
  country,
  CURRENT_TIMESTAMP AS created_at
FROM {{ source('raw', 'customers') }}
WHERE customer_id IS NOT NULL
```
- **Tests:**
  - ✅ Unique customer_id
  - ✅ Not null: customer_id, customer_name, email
  - ✅ Email format validation

#### `stg_orders.sql`
```sql
SELECT
  order_id,
  customer_id,
  CASE 
    WHEN order_date ~ '^\d{4}-\d{2}-\d{2}$' THEN order_date::DATE
    ELSE NULL 
  END AS order_date,
  CASE 
    WHEN amount > 0 THEN amount::NUMERIC
    ELSE NULL 
  END AS amount,
  LOWER(TRIM(status)) AS status
FROM {{ source('raw', 'orders') }}
WHERE order_id IS NOT NULL 
  AND customer_id IS NOT NULL
```
- **Transformations:**
  - Parses dates (handles format validation)
  - Validates amounts (converts, filters negatives)
  - Normalizes status (lowercase, trimmed)
  - Filters incomplete records

- **Tests:**
  - ✅ Unique order_id
  - ✅ Not null: order_id, customer_id
  - ✅ Foreign key: customer_id references customers
  - ✅ Accepted values for status: completed, pending, cancelled

---

### 4. **dbt Marts Layer** (`models/marts/`)

Business logic and aggregations for analytics.

#### `customer_metrics.sql` (MATERIALIZED TABLE)
```sql
SELECT
  c.customer_id,
  c.customer_name,
  COUNT(DISTINCT o.order_id) AS total_orders,
  SUM(CASE WHEN o.status = 'completed' THEN 1 ELSE 0 END) AS completed_orders,
  SUM(CASE WHEN o.status = 'pending' THEN 1 ELSE 0 END) AS pending_orders,
  COALESCE(SUM(CASE WHEN o.status = 'completed' THEN o.amount END), 0) AS total_revenue,
  COALESCE(AVG(CASE WHEN o.status = 'completed' THEN o.amount END), 0) AS avg_order_value,
  MIN(o.order_date) AS first_order_date,
  MAX(o.order_date) AS last_order_date,
  COALESCE(MAX(o.order_date) - MIN(o.order_date), 0) AS days_as_customer,
  CASE 
    WHEN (MAX(o.order_date) - MIN(o.order_date)) > 0 
    THEN ROUND(SUM(CASE WHEN o.status = 'completed' THEN o.amount END) / (MAX(o.order_date) - MIN(o.order_date))::NUMERIC, 2)
    ELSE SUM(CASE WHEN o.status = 'completed' THEN o.amount END)
  END AS customer_lifetime_value,
  CURRENT_TIMESTAMP AS updated_at
FROM stg_customers c
LEFT JOIN stg_orders o ON c.customer_id = o.customer_id
GROUP BY c.customer_id, c.customer_name
```

**Key Metrics:**
- **total_orders:** Count of all orders per customer
- **completed_orders:** Count of completed (paid) orders
- **pending_orders:** Count of pending orders
- **total_revenue:** Sum of completed order amounts
- **avg_order_value:** Average order value for completed orders
- **days_as_customer:** Date range from first to last order
- **customer_lifetime_value:** Total revenue divided by days as customer (revenue per day)
- **updated_at:** Refresh timestamp

**Example Output:**
| customer_id | customer_name | total_orders | completed_orders | total_revenue | customer_lifetime_value |
|---|---|---|---|---|---|
| 1 | Alice Johnson | 3 | 2 | 450.00 | 150.00 |
| 2 | Bob Smith | 4 | 3 | 600.50 | 200.17 |

---

## 🔄 GitHub Actions CI/CD Workflow

### **Workflow File:** `.github/workflows/dbt-ci.yml`

The workflow runs on every **Pull Request** to `main` or `staging` branch and includes 3 jobs:

### **Job 1: dbt-test (Automatic)** ✅
Runs on every PR automatically.

**Steps:**
1. Checkout code
2. Set up Python 3.11
3. Install dependencies (dbt-postgres 1.10.0, pandas, psycopg2)
4. Start PostgreSQL 15 service container
5. Seed test data (5 customers, 5 orders)
6. Run dbt commands:
   - `dbt deps` - Install packages
   - `dbt parse` - Validate dbt syntax
   - `dbt debug` - Check database connection
   - `dbt run` - Execute all models
   - `dbt test` - Run 18 data quality tests
   - `dbt docs generate` - Generate documentation

**Output:** 
- ✅ All 18 tests pass
- 📊 dbt artifacts uploaded
- ⏱️ Duration: 5-8 minutes

**Tests Run:**
```
 1. accepted_values_stg_orders_status
 2. not_null_customer_metrics_completed_orders
 3. not_null_customer_metrics_customer_id
 4. not_null_customer_metrics_customer_lifetime_value
 5. not_null_customer_metrics_total_orders
 6. not_null_customer_metrics_total_revenue
 7. not_null_stg_customers_customer_id
 8. not_null_stg_customers_customer_name
 9. not_null_stg_orders_customer_id
10. not_null_stg_orders_order_id
11. relationships_stg_orders_customer_id
12. source_not_null_raw_customers_customer_id
13. source_unique_raw_customers_customer_id
14. source_unique_raw_orders_order_id
15. unique_customer_metrics_customer_id
16. unique_stg_customers_customer_id
17. unique_stg_customers_email
18. (additional relationship tests)
```

---

### **Job 2: approval (Manual Approval Gate)** 🔔
Triggered AFTER dbt-test passes. Waits for human approval.

**Steps:**
1. Posts comment on PR: "✅ All dbt checks passed! 🔔 Awaiting approval for merge"
2. Waits for PR approval from code owner
3. Job succeeds when approval received

**Purpose:** Gate deployment behind human review

---

### **Job 3: auto-merge (Automatic Post-Approval)** 🚀
Triggered AFTER approval job succeeds. Automatically merges the PR.

**Steps:**
1. Merge PR using **squash** method
2. Delete feature branch automatically
3. Cleanup and complete

**Result:** PR automatically merged to main, branch deleted

---

## 🗄️ Database Configuration

### PostgreSQL Setup
- **Version:** PostgreSQL 15 (Alpine Linux)
- **Local Connection:** localhost:5432
- **Default Credentials:**
  - Username: postgres
  - Password: Arpit_123
  - Database: dbt_project

### CI/CD Database
- **Connection:** PostgreSQL 15 container in GitHub Actions
- **Database:** dbt_test
- **Schema:** public

### Tables Created
```sql
-- Raw tables (created by Python ingestion)
public.customers (customer_id, customer_name, email, phone, country)
public.orders (order_id, customer_id, order_date, amount, status)

-- dbt staging views
analytics.stg_customers (view)
analytics.stg_orders (view)

-- dbt marts tables
analytics.customer_metrics (materialized table with KPIs)
```

---

## 🚀 How to Use the Pipeline

### **Locally**

#### 1. Run the full pipeline:
```powershell
cd "c:\Users\arpit\Jupyter Notebook\CI CD Pipeline project"
python ingestion/run_full_pipeline.py
```

**Output:**
- PostgreSQL loaded with customer/order data
- dbt models created
- 18 tests pass
- `data/final_dashboard_data.csv` exported

#### 2. Or run individual components:
```powershell
# Just load data
python ingestion/load_data_to_postgres.py

# Just export metrics
python ingestion/export_final_data.py

# Just run dbt
dbt run
dbt test
```

---

### **Via GitHub Actions (CI/CD)**

#### 1. Create a feature branch:
```bash
git checkout -b feature/my-new-metric
```

#### 2. Make changes to a dbt model:
```sql
-- Example: Add new column to customer_metrics.sql
SELECT ..., NEW_METRIC AS column_name FROM ...
```

#### 3. Commit and push:
```bash
git add models/marts/customer_metrics.sql
git commit -m "feat: Add new customer metric"
git push -u origin feature/my-new-metric
```

#### 4. Create Pull Request on GitHub:
- Go to https://github.com/ArpitGhai03/analytics-engineering-ci-cd-pipeline
- Click "New Pull Request"
- Select `feature/my-new-metric` → `main`
- Click "Create Pull Request"

#### 5. Watch GitHub Actions run:
- ✅ dbt-test job runs automatically (5-8 minutes)
- All 18 tests validate your changes
- If all pass → 🔔 approval job waits

#### 6. Approve the PR:
- Go to PR → "Checks" tab
- Click "Review deployments" button
- Select "Approve"

#### 7. Auto-merge happens:
- 🚀 auto-merge job runs automatically
- PR merged with squash method
- Feature branch deleted

---

## 📝 Key Files

| File | Purpose |
|------|---------|
| `README.md` | Quick start & basic setup |
| `GITHUB_ACTIONS_SETUP.md` | Detailed workflow instructions |
| `dbt_project.yml` | dbt configuration |
| `.dbt/profiles.yml` | Database connection profiles |
| `.github/workflows/dbt-ci.yml` | GitHub Actions workflow |
| `ingestion/run_full_pipeline.py` | Master pipeline orchestration |
| `models/staging/` | Data cleaning & validation |
| `models/marts/` | Business metrics & aggregations |

---

## 🎓 What You Learned

### Technologies
- ✅ **PostgreSQL:** Relational database & SQL
- ✅ **Python:** Data ingestion, validation, ETL
- ✅ **dbt:** Data transformation framework
- ✅ **Git/GitHub:** Version control & PR workflow
- ✅ **GitHub Actions:** CI/CD automation

### Concepts
- ✅ **ETL Pipeline:** Extract → Transform → Load
- ✅ **Data Quality:** Testing, validation, error handling
- ✅ **Layered Architecture:** Raw → Staging → Marts
- ✅ **CI/CD:** Automated testing & deployment gates
- ✅ **Approval Gates:** Manual reviews before production

### Data Engineering Best Practices
- ✅ Handle messy real-world data
- ✅ Validate data quality with tests
- ✅ Use version control for transformations
- ✅ Automate deployment with CI/CD
- ✅ Document data models and metrics

---

## 🐛 Common Issues & Solutions

### Issue: dbt parse fails
**Solution:** Run `dbt deps` first to install packages

### Issue: PostgreSQL connection error
**Solution:** Verify `~/.dbt/profiles.yml` has correct credentials

### Issue: GitHub Actions fails on PR
**Solution:** Check workflow has proper permissions in `.github/workflows/dbt-ci.yml`

### Issue: Duplicate orders not loading
**Solution:** `load_data_to_postgres.py` intentionally skips duplicates (data quality check)

---

## 📊 Example Workflow: Adding a New Metric

Want to add a new metric like **Repeat Customer Rate**?

### Step 1: Update the model
Edit `models/marts/customer_metrics.sql`:
```sql
SELECT
  ...,
  -- Calculate repeat customer rate
  CASE 
    WHEN total_orders > 1 THEN ROUND(100.0 * completed_orders / total_orders, 2)
    ELSE 0
  END AS repeat_customer_rate
FROM ...
```

### Step 2: Create feature branch & push
```bash
git checkout -b feature/repeat-customer-rate
git add models/marts/customer_metrics.sql
git commit -m "feat: Add repeat customer rate metric"
git push -u origin feature/repeat-customer-rate
```

### Step 3: Create PR on GitHub
GitHub Actions automatically:
- ✅ Runs dbt models with new metric
- ✅ Validates 18 tests pass
- ✅ Posts approval request

### Step 4: Review & Approve
- Review the PR changes
- Click "Review deployments" → "Approve"
- Auto-merge happens automatically 🚀

### Step 5: Pull to local
```bash
git checkout main
git pull
```

Done! Your new metric is in production! 🎉

---

## 🔗 Resources

- **dbt Documentation:** https://docs.getdbt.com
- **PostgreSQL Documentation:** https://www.postgresql.org/docs
- **GitHub Actions Documentation:** https://docs.github.com/actions
- **Analytics Engineering:** https://www.startdataengineering.com/

---

## 📞 Project Status

✅ **Complete & Production-Ready**
- Data pipeline: LIVE
- dbt transformations: VALIDATED
- GitHub Actions CI/CD: AUTOMATED
- 18 data quality tests: PASSING
- Auto-deployment: ENABLED

**Next Steps:** Create your own feature branches and practice the workflow! 🚀

---

**Created:** May 2026
**Status:** Active CI/CD Pipeline
**Maintainer:** Analytics Engineering Team
