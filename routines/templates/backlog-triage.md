# Backlog Triage Routine

## Overview

Automatically label, assign, and prioritize new issues so the team starts each morning with a groomed queue.

## Configuration

| Setting | Value |
|---|---|
| **Trigger** | Schedule - Weeknights at 10:00 PM |
| **Connectors** | GitHub, Slack |
| **Repositories** | Repos with active issue tracking |
| **Run time** | ~2-4 minutes |

## Prompt

```
Triage all issues opened today in this repository that don't already have labels.

For each unlabeled issue:

1. CATEGORIZE - Apply one primary label:
   - "bug" - Something is broken or producing incorrect results
   - "feature" - New functionality request
   - "enhancement" - Improvement to existing functionality
   - "documentation" - Docs are missing, unclear, or wrong
   - "question" - User needs help, not reporting a bug
   - "good-first-issue" - Clear scope, well-documented, suitable for new contributors

2. PRIORITIZE - Apply one priority label:
   - "P0-critical" - Service is down, data loss, security vulnerability, blocks many users
   - "P1-important" - Significant impact, should fix this sprint
   - "P2-normal" - Should fix, but not urgent
   - "P3-low" - Nice to have, backlog candidate

3. ASSIGN - Check CODEOWNERS file and recent git blame for the affected area.
   Assign to the team member who most recently worked on that code.
   If unclear, leave unassigned.

4. DEDUPLICATE - Search existing open issues for duplicates:
   - If a clear duplicate exists, comment with a link and label "duplicate"
   - If related but not duplicate, add a comment linking the related issue

5. CHECK FOR EXISTING FIXES - For bugs, search recent PRs and commits:
   - If a fix was already merged, comment and close with "Fixed in [commit/PR]"
   - If a fix PR is open, comment with the PR link

After processing all issues, post to #triage:
- Total new issues processed: [count]
- By priority: P0: [n], P1: [n], P2: [n], P3: [n]
- By type: bugs: [n], features: [n], other: [n]
- Issues auto-closed as duplicates: [n]
- P0 issues requiring immediate attention: [list with links]

If no new unlabeled issues exist today, post "No new issues to triage" and exit.
```

## Customization

**Custom labels**: Replace the label scheme with your team's taxonomy.

**Auto-responses**: Add "For questions, post a helpful initial response based on the project's documentation and FAQ."

**SLA tracking**: Add "Flag any P0 issues that have been open for >4 hours without a response."
