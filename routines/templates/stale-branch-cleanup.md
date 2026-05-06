# Stale Branch Cleanup Routine

## Overview

Weekly cleanup of merged and abandoned branches. Keeps the repository tidy without accidentally deleting in-progress work.

## Configuration

| Setting | Value |
|---|---|
| **Trigger** | Schedule - Weekly (Sundays at 11:00 PM) |
| **Connectors** | GitHub |
| **Repositories** | Your team's repos |
| **Run time** | ~2-3 minutes |

## Prompt

```
Clean up stale branches in this repository.

1. List all remote branches not updated in the last 30 days

2. Exclude from cleanup:
   - main, master, develop, staging, production
   - release/* and hotfix/* branches
   - Any branch with an open pull request
   - Branches matching patterns in .github/branch-protection.yml (if it exists)

3. For each candidate branch:
   - Check if the branch was merged into main/master
   - If merged: delete the remote branch (safe cleanup)
   - If not merged and no activity in 60+ days: create an issue tagging the
     branch author titled "Stale branch: [branch-name] - still needed?"
   - If not merged and 30-60 days stale: skip for now (will be caught next cycle)

4. Report:
   - Count of branches deleted (merged and stale)
   - Count of branches flagged for author review
   - Count of protected branches skipped
   - Total branch count before and after cleanup

Post summary to #dev-ops or print to console.
If no stale branches found, post "Repository branches are tidy" and exit.
```

## Customization

**For monorepos with many contributors**: Reduce the stale threshold to 14 days for merged branches.

**For repos with long-lived feature branches**: Add a whitelist of branch patterns to exclude (e.g., `epic/*`).
