# Contributing to the CI/CD Pipeline Project

Thank you for contributing! This guide will help you get started.

## Getting Started

### 1. Clone the Repository
```bash
git clone https://github.com/ArpitGhai03/analytics-engineering-ci-cd-pipeline.git
cd analytics-engineering-ci-cd-pipeline
```

### 2. Set Up Your Local Environment
```bash
# Create virtual environment
python -m venv .venv

# Activate it
.\.venv\Scripts\Activate.ps1

# Install dependencies
pip install pandas psycopg2-binary
```

### 3. Ensure PostgreSQL is Running
```bash
# Make sure PostgreSQL is running on your machine
# Default connection: localhost:5432
```

---

## Making Changes

### 1. Create a Feature Branch
```bash
git checkout -b feature/your-feature-name
```

**Branch naming conventions:**
- `feature/` - New features or models
- `fix/` - Bug fixes
- `docs/` - Documentation updates
- `refactor/` - Code refactoring
- `test/` - Test additions

### 2. Make Your Changes

#### Adding a New Model:
```bash
# Create file in models/staging/ or models/marts/
# Example: models/marts/new_metrics.sql
```

#### Updating Ingestion Scripts:
```bash
# Edit ingestion/load_data_to_postgres.py
# Or ingestion/export_final_data.py
```

#### Updating Documentation:
```bash
# Edit README.md, this file, or create new docs
```

### 3. Test Locally
```bash
# Run full pipeline locally
python ingestion/run_full_pipeline.py

# Or run dbt separately
dbt run
dbt test

# Check results
dbt debug
```

### 4. Commit Your Changes
```bash
git add .
git commit -m "feat: Description of what you changed"
```

**Commit message format:**
```
feat: Add new customer lifetime value metric
fix: Correct null handling in orders
docs: Update README with examples
refactor: Simplify customer segmentation logic
test: Add validation tests for orders
```

### 5. Push to GitHub
```bash
git push -u origin feature/your-feature-name
```

---

## Creating a Pull Request

### Using GitHub CLI (Recommended):
```bash
# Create PR
gh pr create --base main --title "Your PR Title" --body "Description of changes"

# Example:
gh pr create --base main --title "feat: Add customer lifetime value metric" --body "This PR adds a new KPI metric for customer lifetime value. Includes data quality tests."

# View your PR
gh pr view --web
```

### Or on GitHub Web:
1. Go to: https://github.com/ArpitGhai03/analytics-engineering-ci-cd-pipeline/pulls
2. Click "New Pull Request"
3. Select base: `main`, compare: `your-branch`
4. Add title and description
5. Click "Create Pull Request"

---

## Review Process

### Automated Tests (GitHub Actions)
Your PR will automatically run:
- ✅ `dbt parse` - Syntax validation
- ✅ `dbt debug` - Connection check
- ✅ `dbt run` - Execute models
- ✅ `dbt test` - Data quality tests

**Tests must pass before approval!**

### Manual Review
Once tests pass:
1. Invite reviewers (optional)
2. Respond to any comments
3. Make additional changes if needed

### Approval
```bash
# Approve the PR (from your side)
gh pr review --approve

# Or on GitHub, click "Approve"
```

---

## Auto-Merge

Once approved, the PR automatically merges using **squash merge** (clean history).

You can also manually merge:
```bash
gh pr merge --squash
```

---

## Common Issues

### Tests Failing
- Check PostgreSQL is running
- Verify data types match schema
- Run `dbt debug` for connection issues
- Check logs in `target/` folder

### Merge Conflicts
```bash
# Pull latest main
git fetch origin
git rebase origin/main

# Fix conflicts in your editor
git add .
git rebase --continue
git push -f origin feature/your-branch
```

### Need to Update PR
```bash
# Make changes, then:
git add .
git commit -m "fix: Address review comments"
git push origin feature/your-branch
```

The PR will automatically update!

---

## Best Practices

✅ **DO:**
- Create small, focused PRs (one feature per PR)
- Write clear commit messages
- Test locally before pushing
- Add comments to complex logic
- Reference issues in commit messages

❌ **DON'T:**
- Push directly to main
- Make multiple unrelated changes in one PR
- Skip local testing
- Commit credentials or secrets

---

## Questions?

- Check [README.md](README.md) for project overview
- See [GITHUB_ACTIONS_SETUP.md](GITHUB_ACTIONS_SETUP.md) for CI/CD details
- See [PR_WORKFLOW.md](PR_WORKFLOW.md) for workflow commands

---

Happy contributing! 🚀
