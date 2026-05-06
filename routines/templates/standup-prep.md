# Standup Prep Routine

## Overview

Generate ready-to-paste standup notes from your actual git and issue tracker activity. No more trying to remember what you did yesterday.

## Configuration

| Setting | Value |
|---|---|
| **Trigger** | Schedule - Weekdays at 9:00 AM |
| **Connectors** | GitHub, Linear/Jira (optional: Slack) |
| **Repositories** | Your active repos |
| **Run time** | ~1-2 minutes |

## Prompt

```
Generate my standup notes for today.

Yesterday:
- List my merged PRs with one-line descriptions
- List issues I commented on or closed
- Note any PR reviews I completed

Today:
- List my open PRs and their status (needs review, changes requested, approved)
- List issues assigned to me sorted by priority
- Flag any blockers (failed CI, pending reviews >48h, dependency issues)

Blockers:
- Check if any of my PRs have failing CI
- Check if any assigned issues are blocked by other issues
- Check if any assigned issues have unresolved dependencies

Format as bullet points under three headers: Yesterday, Today, Blockers.
Keep it under 15 lines total.
Post to #standup or print to console.

If yesterday was Monday, check back to Friday 5 PM instead of yesterday.
```

## Customization

**For sprint-based teams**: Add a line showing sprint progress (e.g., "Sprint day 5/10, 60% of points completed").

**For async teams**: Post the standup to a thread in the team channel instead of a dedicated #standup channel.

## Example Output

```
Standup - May 6, 2026

Yesterday:
- Merged #452 "Add rate limiting to auth endpoints"
- Reviewed #450 (payment pipeline refactor) - left 3 comments
- Closed #198 "Fix flaky timezone test"

Today:
- #453 "Add OAuth2 PKCE flow" - needs review (opened yesterday)
- #199 "Implement password reset" - P1, starting today
- #201 "Login fails on Safari 18" - P0, investigating

Blockers:
- #453 CI failing: lint error in auth.test.ts
```
