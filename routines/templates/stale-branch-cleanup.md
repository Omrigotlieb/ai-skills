# Stale Branch Cleanup Routine

## Overview

Keep your repository clean by automatically removing merged branches and flagging abandoned work.

## Configuration

| Setting | Value |
|---|---|
| **Trigger** | Schedule - Weekly (Sundays at 11:00 PM) |
| **Connectors** | GitHub |
| **Repositories** | Repos with active development |
| **Run time** | ~2-3 minutes |

## Prompt

```
Clean up stale branches in this repository.

1. IDENTIFY STALE BRANCHES:
   - List all remote branches not updated in the last 30 days
   - Exclude protected branches: main, master, develop, staging, production
   - Exclude release branches: release/*, hotfix/*
   - Exclude branches with open PRs

2. CATEGORIZE:
   Merged and stale (safe to delete):
   - Branch was merged into main/master/develop
   - No open PR exists
   - Action: Delete the remote branch

   Unmerged and stale (needs author input):
   - Branch was NOT merged
   - No activity in 30+ days
   - No open PR exists
   - Action: Create an issue tagging the branch author
     Title: "Stale branch: [branch-name] - still needed?"
     Body: Last commit date, author, summary of changes, and ask whether to keep or delete

   Recently abandoned (warning only):
   - Branch was NOT merged
   - No activity in 14-30 days
   - No open PR exists
   - Action: Include in report only, no action taken

3. REPORT - Post to #dev-ops or print to console:
   - Branches deleted (merged, stale): [count] - [list]
   - Issues created for unmerged stale branches: [count] - [list with links]
   - Recently abandoned (watch list): [count] - [list]
   - Protected branches skipped: [count]
   - Total branches remaining: [count]

If no stale branches found, report "Repository is clean. No stale branches detected." and exit.

RESTRICTIONS:
- Never delete branches that have open PRs
- Never delete protected or release branches
- Never force-delete branches (always use safe delete that only works for merged branches)
- For unmerged branches, always create an issue instead of deleting
```

## Customization

**Stricter cleanup**: Reduce the stale threshold from 30 days to 14 days for fast-moving repos.

**Team notifications**: Add "DM branch authors on Slack instead of creating issues."

**Archive instead of delete**: Add "Instead of deleting, create a tag at the branch tip before removing."
