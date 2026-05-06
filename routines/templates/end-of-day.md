# End-of-Day Summary Routine

## Overview

Compile a daily progress report automatically. Tracks what you accomplished, surfaces tomorrow's priorities, and catches upcoming deadlines.

## Configuration

| Setting | Value |
|---|---|
| **Trigger** | Schedule - Weekdays at 6:00 PM |
| **Connectors** | GitHub, Slack (optional: Linear/Jira) |
| **Run time** | ~2-3 minutes |

## Prompt

```
Compile my end-of-day development summary.

Activity:
- List all commits I pushed today with one-line messages
- List PRs I opened, reviewed, or merged
- List issues I closed or commented on

Progress:
- Summarize what was accomplished in 2-3 sentences
- Note any items that took longer than expected and why

Tomorrow:
- List my open PRs that need attention (failing CI, review comments)
- List highest-priority assigned issues for tomorrow
- Flag any upcoming deadlines within 3 days

Format as a clean summary under three headers: Activity, Progress, Tomorrow.
Keep it under 20 lines.

If this is Friday, also include a "This Week" section with weekly highlights
and a "Next Week" section with planned priorities.

Post to #daily-updates or print to console.
If no activity today (sick day, PTO), post "No development activity today" and exit.
```

## Customization

**For managers**: Add a team-wide activity summary instead of individual activity.

**For contractors/freelancers**: Add a time-tracking summary and billable hours estimate.

**For sprint teams**: Add sprint burndown progress and velocity comparison.

## Example Output

```
End of Day - May 6, 2026

Activity:
- Merged #452 "Add rate limiting to auth endpoints"
- Opened #453 "Add OAuth2 PKCE flow"
- Reviewed #450 (payment pipeline refactor)
- Closed #198, #201

Progress:
Auth rate limiting shipped to main. Started OAuth2 PKCE implementation,
about 60% complete. Safari login bug (#201) was a timezone issue in the
session cookie - quick fix.

Tomorrow:
- #453 needs CI fix (lint error in auth.test.ts) then review
- #199 "Implement password reset" - P1, blocked until #453 merges
- Deadline: API v2 deprecation notice due Thursday
```
