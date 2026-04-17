# End-of-Day Summary Routine

## Overview

Automatically compile your daily development activity into a clean summary for personal tracking and async team visibility.

## Configuration

| Setting | Value |
|---|---|
| **Trigger** | Schedule - Weekdays at 6:00 PM |
| **Connectors** | GitHub, Slack (optional) |
| **Repositories** | Repos you contribute to |
| **Run time** | ~1-2 minutes |

## Prompt

```
Compile my end-of-day development summary for today.

COMPLETED:
- List all commits I pushed today (group by PR if applicable)
- List PRs I opened, reviewed, or merged with one-line descriptions
- List issues I closed or made significant progress on
- Note any documentation I updated

IN PROGRESS:
- List my open PRs with current status:
  - Waiting for review (who?)
  - Changes requested (what?)
  - CI failing (which job?)
  - Approved but not merged (why?)

TOMORROW'S PRIORITIES:
- List my highest-priority assigned issues (top 3)
- Flag any open PRs that need immediate attention tomorrow
- Note any deadlines within the next 3 business days
- Flag any meetings that might block coding time (if calendar connector available)

FORMAT:
- Use bullet points, keep total under 20 lines
- Lead with the most impactful work
- Skip trivial commits (typos, formatting)

If today is Friday, add a WEEKLY HIGHLIGHTS section:
- Key accomplishments this week (top 3)
- Metrics: PRs merged, issues closed, reviews completed
- Carry-over items for next week

Post to #daily-updates or print to console.
If no meaningful activity today (vacation, meetings-only day), report "No code activity today" and exit.
```

## Customization

**Manager visibility**: Add "Also post a condensed 3-line version to #team-leads."

**Sprint tracking**: Add "Note which sprint items this work relates to and update remaining estimate."

**Personal journal**: Add "Save a copy to a local markdown file at ~/dev-journal/YYYY-MM-DD.md."
