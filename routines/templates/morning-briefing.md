# Morning Briefing Routine

## Overview

Start every day with a clear picture of what happened overnight. This routine compiles PR activity, CI health, and new issues into a single Slack message before standup.

## Configuration

| Setting | Value |
|---|---|
| **Trigger** | Schedule - Daily at 7:00 AM |
| **Connectors** | GitHub, Slack |
| **Repositories** | Your team's primary repos |
| **Run time** | ~2-3 minutes |

## Prompt

```
Compile a morning briefing for the team. Check all connected repositories.

PRs Merged (since yesterday 5:00 PM):
- List each with: title, author, target branch, and a one-line summary of the change
- Highlight any PRs that touched critical paths: auth, payments, database migrations

PRs Awaiting Review (open >24 hours without approval):
- List with: title, author, assigned reviewers, and hours waiting
- Bold any PRs waiting >48 hours

CI Status:
- Check the latest CI run on the main/default branch of each repo
- If any are failing: include the job name, failing step, and a one-line diagnosis
- If all green: report "All CI passing"

New Issues (opened since yesterday 5:00 PM):
- Group by label: bugs, features, questions
- Include issue number, title, and author
- Flag any labeled P0 or urgent

Format as a Slack message using sections with headers.
Post to #dev-standup.

If nothing noteworthy happened overnight, post:
"All clear overnight. No new PRs, no CI failures, no urgent issues."
```

## Customization

**For smaller teams** (< 5 engineers): Remove the "PRs Awaiting Review" section.

**For monorepos**: Add grouping by package/service area instead of by repo.

**For distributed teams**: Adjust the time window to match your timezone spread (e.g., "since the last briefing" instead of "since 5 PM").

**Adding Slack threads**: Append a section that checks for Slack threads mentioning you or threads in key channels (#incidents, #deploys) from the last 12 hours.

## Example Output

```
Morning Briefing - May 6, 2026

PRs Merged (3):
- #452 "Add rate limiting to auth endpoints" - @alice (main)
- #449 "Fix timezone handling in scheduler" - @bob (main)
- #451 "Update dependencies for security patches" - @charlie (main)

Awaiting Review (1):
- #450 "Refactor payment processing pipeline" - @dave
  Reviewers: @alice, @eve | Waiting: 36 hours

CI: All passing

New Issues (2):
- Bugs: #201 "Login fails on Safari 18" (@user123)
- Features: #202 "Add dark mode support" (@user456)
```
