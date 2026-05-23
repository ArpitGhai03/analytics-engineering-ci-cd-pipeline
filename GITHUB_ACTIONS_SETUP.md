# GitHub Actions Setup Guide

## Quick Start

### 1. Initialize Git Repository (if not already done)
```bash
cd "c:\Users\arpit\Jupyter Notebook\CI CD Pipeline project"
git init
git add .
git commit -m "Initial commit: Complete dbt CI/CD pipeline"
```

### 2. Add Remote Repository
```bash
git remote add origin https://github.com/ArpitGhai03/analytics-engineering-ci-cd-pipeline.git
git branch -M main
git push -u origin main
```

### 3. Create a Development Branch
```bash
git checkout -b develop
git push -u origin develop
```

---

## GitHub Actions Workflow Explained

### Files Created:
- **`.github/workflows/dbt-ci.yml`** - Main CI/CD pipeline workflow

### What Happens:

#### 1. **Trigger** 🚀
- When someone pushes code to a PR targeting `main` or `staging`
- Only runs if changes are in: `models/`, `dbt_project.yml`, `ingestion/`, or workflows

#### 2. **Test Job** (Automatic) ✅
- Spins up PostgreSQL container
- Loads sample data
- Runs:
  - `dbt parse` - Syntax validation
  - `dbt debug` - Connection check
  - `dbt run` - Execute all models
  - `dbt test` - Data quality checks
- Duration: ~3-5 minutes
- If fails: Blocks PR, shows error details

#### 3. **Approval Job** (Manual) 🔔
- If tests pass, adds comment: "Awaiting approval"
- You review the PR on GitHub
- You click "Approve and Comment"

#### 4. **Auto-Merge Job** (Automatic) 🚀
- Waits for your approval (polls every 5 seconds)
- Once approved, auto-merges to main
- Uses squash merge for clean history

---

## How to Use

### Creating a Change
```bash
# Create feature branch
git checkout -b feature/new-model

# Make changes to models
# Edit models/staging/stg_customers.sql
# Or create new models/marts/new_metric.sql

# Commit and push
git add models/
git commit -m "Add new customer segmentation model"
git push -u origin feature/new-model
```

### On GitHub:
1. ✅ Create Pull Request
2. ⏳ GitHub Actions runs tests automatically
3. 💬 Tests show results as comments
4. 🔔 When all pass, review request appears
5. ✅ You approve the PR
6. 🚀 Auto-merge happens

---

## Test Checks Included

### Staging Models Tests:
- **customer_id**: unique, not_null
- **customer_name**: not_null
- **email**: unique
- **order_id**: unique, not_null
- **customer_id (FK)**: not_null, relationships check
- **status**: only allowed values (completed, pending, cancelled)

### Marts Models Tests:
- **customer_id**: unique, not_null
- **total_orders**: not_null, must be integer
- **total_revenue**: not_null, >= 0

---

## Monitoring & Logs

### View Workflow Runs:
1. Go to: https://github.com/ArpitGhai03/analytics-engineering-ci-cd-pipeline/actions
2. Click on workflow runs to see:
   - ✅ Passed tests
   - ❌ Failed tests with error messages
   - 🔔 Approval status

### View Artifacts:
- dbt generates docs at: `target/compiled/` (available as download)

---

## Environment Variables (Optional)

If you need different settings, add to workflow:
```yaml
env:
  DBT_PROFILES_DIR: ~/.dbt
  DBT_VERSION: 1.10.8
```

---

## Troubleshooting

### Tests Failing on GitHub but Pass Locally?
- Check PostgreSQL version matches (15-alpine used in CI)
- Ensure seed data is being created
- Check timezone settings

### Auto-Merge Not Working?
- Ensure GITHUB_TOKEN has permissions
- Check branch protection rules on main
- Verify you have admin/write access

### Timeout Issues?
- dbt run should complete in < 1 minute
- Tests should complete in < 2 minutes
- Total pipeline: < 10 minutes

---

## Security Notes

⚠️ **Important:**
- GitHub Actions runs have access to repository secrets
- Credentials are stored as GitHub Secrets (NOT in code)
- The workflow uses ephemeral PostgreSQL (deleted after run)
- No sensitive data is exposed

---

## Next Steps

1. ✅ Push code to GitHub
2. ✅ Create a test PR with model changes
3. ✅ Watch workflow run
4. ✅ Review and approve
5. ✅ See auto-merge happen! 🎉

---

## Customization

To add more tests:
1. Edit `.yml` files in models/
2. Add test types: `unique`, `not_null`, `relationships`, `accepted_values`
3. Or add custom tests in `tests/` directory
4. Commit and push - workflow runs automatically

For more: https://docs.getdbt.com/docs/build/tests
