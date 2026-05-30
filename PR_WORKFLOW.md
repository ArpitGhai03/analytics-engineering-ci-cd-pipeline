# Complete PR & Approval Workflow - Step by Step

This guide shows you EXACTLY how to create a Pull Request and approve it with terminal commands.

---

## Prerequisites

### Install GitHub CLI (One-time setup)
```bash
# Install GitHub CLI if you haven't already
# Go to: https://github.com/cli/cli/releases
# Or use Winget (Windows Package Manager):
winget install GitHub.cli
```

### Login to GitHub via CLI (One-time setup)
```bash
gh auth login
# When prompted:
# - Choose: GitHub.com
# - Choose: HTTPS
# - Choose: Y (Authenticate Git with your GitHub credentials?)
# - Choose: Login with a web browser
# - Follow the browser prompt to authorize
```

---

## Full Workflow: From Local Changes to Auto-Merge

### Step 1: Create a Feature Branch
```bash
cd "c:\Users\arpit\Jupyter Notebook\CI CD Pipeline project"

# Create and switch to new branch
git checkout -b feature/your-feature-name

# Example:
# git checkout -b feature/add-new-metric
# git checkout -b feature/fix-customer-logic
# git checkout -b feature/update-docs
```

---

### Step 2: Make Your Changes
Edit files in VS Code or your editor. For example:
```bash
# Edit models/marts/customer_metrics.sql
# Or create new models/marts/new_model.sql
# Or update ingestion/load_data_to_postgres.py
```

---

### Step 3: Commit Your Changes
```bash
# Check what files changed
git status

# Stage all changes
git add .

# Or stage specific files
git add models/
git add ingestion/

# Commit with descriptive message
git commit -m "feat: Add new customer segmentation model"

# Commit message format:
# feat: New feature
# fix: Bug fix
# docs: Documentation update
# refactor: Code refactoring
# test: Test additions
```

---

### Step 4: Push to GitHub
```bash
# Push your feature branch to GitHub
git push -u origin feature/your-feature-name

# Example:
# git push -u origin feature/add-new-metric
```

---

### Step 5: Create a Pull Request (PR)

#### Option A: Using GitHub CLI (Recommended - Faster)
```bash
# Create PR from your feature branch to main
gh pr create --base main --title "Add new customer segmentation model" --body "This PR adds a new model for customer segmentation. It includes data quality tests."

# Break it down:
# --base main                    = Target branch (where you want to merge)
# --title "..."                  = PR title
# --body "..."                   = PR description
```

**Example with real PR:**
```bash
gh pr create --base main --title "feat: Add customer segmentation model" --body "## Changes
- Added new marts model for customer segmentation
- Includes 3 new metrics: segment_id, segment_name, customer_count
- All data quality tests passing

## Testing
- Ran dbt test locally - all passed
- Verified with sample data

Closes #123"
```

#### Option B: Manual on GitHub Web Interface
```bash
# After push, go to:
# https://github.com/ArpitGhai03/analytics-engineering-ci-cd-pipeline/pulls
# Click: "New Pull Request"
# Choose base: main
# Choose compare: feature/your-feature-name
# Click: "Create Pull Request"
# Add title and description
# Click: "Create Pull Request"
```

---

### Step 6: Check PR Status (Monitor Tests)
```bash
# View your PR status
gh pr status

# View detailed PR info
gh pr view

# View PR checks/tests
gh pr checks

# Output will show:
# Status: PENDING / PASS / FAIL
# Tests: dbt run, dbt test, etc.
```

**Wait for tests to complete** (~3-5 minutes)

---

### Step 7: Review PR Details
```bash
# Open PR in browser to review
gh pr view --web

# This shows:
# - Changes made
# - Test results
# - Comments
# - Approval status
```

---

### Step 8: Approve the PR
```bash
# Approve the PR
gh pr review --approve

# Optional: Add approval comment
gh pr review --approve --body "Looks good! Approved."
```

---

### Step 9: Auto-Merge (The workflow does this automatically!)
```bash
# The GitHub Actions workflow will automatically merge once approved
# But you can manually merge if needed:
gh pr merge --squash

# Squash merge = all commits combined into one
# This keeps main history clean
```

**What happens automatically:**
1. ✅ Tests pass
2. ✅ You approve
3. ✅ Auto-merge happens (squash merge to main)
4. ✅ Feature branch deleted
5. ✅ Changes live on main!

---

## Real-World Example: Complete Workflow

### Scenario: Add new metric to customer_metrics.sql

```bash
# Step 1: Create feature branch
cd "c:\Users\arpit\Jupyter Notebook\CI CD Pipeline project"
git checkout -b feature/add-annual-revenue-metric

# Step 2: Edit the file (do this in VS Code)
# Edit models/marts/customer_metrics.sql
# Add: annual_revenue = sum(order_amount) * 12

# Step 3: Commit changes
git add models/
git commit -m "feat: Add annual revenue metric to customer_metrics"

# Step 4: Push to GitHub
git push -u origin feature/add-annual-revenue-metric

# Step 5: Create PR using CLI
gh pr create --base main --title "feat: Add annual revenue metric" --body "Adds annual revenue calculation to customer metrics. Multiplies total revenue by 12 for annual projection."

# Step 6: Monitor tests
gh pr checks

# Wait for tests... (should be green ✅)

# Step 7: Open PR in browser to review
gh pr view --web

# Step 8: Approve the PR
gh pr review --approve --body "Approved - verified calculations look correct"

# Step 9: Auto-merge happens automatically! 🎉
# GitHub Actions merges the PR to main

# Step 10 (Optional): Verify on main
git checkout main
git pull origin main
git log --oneline
# Should see your commit merged
```

---

## Useful GitHub CLI Commands

### PR Management
```bash
# List all open PRs
gh pr list

# View specific PR
gh pr view <pr-number>

# View PR in browser
gh pr view <pr-number> --web

# Check PR status
gh pr status

# View checks/tests
gh pr checks <pr-number>

# View PR diff
gh pr diff <pr-number>
```

### PR Review
```bash
# Approve PR
gh pr review <pr-number> --approve

# Request changes
gh pr review <pr-number> --request-changes --body "Please fix the issue"

# Comment on PR
gh pr comment <pr-number> --body "Great work!"
```

### PR Merging
```bash
# Merge PR (squash merge)
gh pr merge <pr-number> --squash

# Merge PR (regular merge)
gh pr merge <pr-number>

# Merge PR (rebase)
gh pr merge <pr-number> --rebase
```

---

## Checking Your Current Branch

```bash
# See all local branches
git branch

# See all branches (local + remote)
git branch -a

# See current branch (has *)
git branch

# Current branch info
git status
```

---

## Undoing Things

### If you made a mistake on a feature branch:

```bash
# Undo last commit (keep changes)
git reset --soft HEAD~1

# Undo last commit (discard changes)
git reset --hard HEAD~1

# Switch to different branch
git checkout main

# Delete a branch
git branch -d feature/your-feature-name
git branch -D feature/your-feature-name  # Force delete
```

---

## Your Current Status

You're currently on: `feature/add-customer-segmentation`

### To create a PR for this branch:
```bash
# Create PR for your current branch
gh pr create --base main --title "docs: Add CI/CD Pipeline section to README" --body "Adds comprehensive documentation about the GitHub Actions CI/CD workflow to the README."

# Then approve it
gh pr review --approve

# Done! Auto-merge will happen
```

---

## Summary: Quick Commands Cheat Sheet

```bash
# Create branch
git checkout -b feature/my-feature

# Make changes, then:
git add .
git commit -m "feat: Description of change"
git push -u origin feature/my-feature

# Create PR
gh pr create --base main --title "Title" --body "Description"

# Monitor tests
gh pr checks

# Approve
gh pr review --approve

# That's it! Auto-merge happens automatically 🚀
```

---
