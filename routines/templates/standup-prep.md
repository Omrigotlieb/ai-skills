# Standup Prep Routine

## Overview

Auto-generate your daily standup notes from actual git and issue tracker activity. No more scrambling to remember what you did yesterday.

## Configuration

| Setting | Value |
|---|---|
| **Trigger** | Schedule - Weekdays at 9:00 AM |
| **Connectors** | GitHub, Linear/Jira (optional), Slack (optional) |
| **Repositories** | Repos you actively contribute to |
| **Run time** | ~1-2 minutes |

## Prompt

```
Generate my standup notes for today based on my actual activity.

YESTERDAY (completed work):
- List my merged PRs with one-line descriptions
- List issues I commented on or closed
- List PR reviews I completed (approved, changes requested, or commented)
- Note any commits pushed that aren't part of a PR

TODAY (planned work):
- List my open PRs and their current status:
  - Needs review (no reviewers assigned or no reviews yet)
  - Changes requested (has review requesting changes)
  - Approved (ready to merge)
  - CI failing (needs attention)
- List issues assigned to me, sorted by priority
- Note any PR reviews requested from me

BLOCKERS:
- Flag PRs with failing CI that I own
- Flag PRs with review requests pending >48 hours
- Flag issues assigned to me that are blocked by other issues
- Flag any merge conflicts in my open PRs

Format as bullet points under Yesterday/Today/Blockers headers.
Keep total output under 15 lines.
Do not include automated bot activity (dependabot, CI updates).

If posting to Slack, use #standup channel.
Otherwise, print to console.
```

## Customization

**Add time tracking**: If your team uses time tracking, add "Include time spent per PR based on first commit to merge timestamp."

**Multi-repo teams**: Add "Group activity by repository" to the format instructions.

**Sprint context**: Add "Reference the current sprint goal and note which items contribute to it."
