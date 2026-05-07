# End-of-Day Wrap-Up Routine

Summarizes the day's work, captures decisions, and prepares tomorrow's priorities so you can start fresh without morning ramp-up time.

---

## Overview

| Property | Value |
|----------|-------|
| **Schedule** | `0 17 * * 1-5` (weekdays at 5 PM) |
| **Duration** | ~30 seconds to generate |
| **Sources** | Git log, GitHub PRs/issues, calendar |

## Setup

Create via `/schedule` in Claude Code: `/schedule weekdays at 5pm: end-of-day wrapup`

Or create at `claude.ai/code/routines` with cron `0 17 * * 1-5` and the prompt below.

### Basic: Git-Based Summary

Use this prompt:

```markdown
Generate my end-of-day summary from today's activity.

## Sources
1. Git log: my commits from today
2. GitHub: PRs I opened, reviewed, merged, or commented on
3. Issues: status changes on my assigned issues

## Output

### What I Shipped
- [Completed work, grouped by feature/area]

### What I Reviewed
- [PRs reviewed with verdict]

### Still In Progress
- [Open PRs, unfinished work -- include current status and what's blocking]

### Decisions Made
- [Any design or architecture decisions visible in PR comments or commit messages]

### Tomorrow's Top 3
1. [Highest priority based on deadlines and what's blocking others]
2. [Next priority]
3. [Next priority]

## Rules
- Group commits by logical change, not individual commits
- Collapse WIP/fixup commits into their parent feature
- Focus on outcomes ("shipped rate limiting") not activity ("edited 4 files")
- Keep under 200 words
```

### Full: Multi-Source Summary

```markdown
Generate a comprehensive end-of-day summary.

## Sources
1. **Git**: commits and branches touched today
2. **GitHub**: PRs, issues, and review activity
3. **Calendar**: meetings attended -- capture any action items
4. **Slack**: threads where I committed to doing something

## Output

### Accomplished
- [Outcome-focused bullets grouped by area]

### Meetings -> Action Items
| Meeting | Key Outcome | My Action Items |
|---------|-------------|-----------------|
| ... | ... | ... |

### Commitments Made
- [Things I said I would do in Slack, PR comments, or meetings]
- [Include who I committed to and when]

### Open Loops
- [Unfinished work with current status]
- [Questions I asked that haven't been answered]
- [Things I'm waiting on from others]

### Tomorrow's Plan
1. [Must do -- deadline or blocking someone]
2. [Should do -- important but flexible]
3. [Could do -- if time permits]

## Rules
- Be honest about what did not get done
- Surface commitments I made so I don't forget them
- Keep under 300 words
```

## Delivery Options

**Email to self:**
```markdown
After generating the summary, email it to me with subject line:
"EOD Summary - [today's date]"
```

**Slack channel:**
```markdown
After generating the summary, post it to #my-daily-log channel.
```

**Append to daily note:**
```markdown
After generating the summary, append it to ~/notes/daily/[YYYY-MM-DD].md
Create the file if it doesn't exist.
```

## Weekly Rollup

Combine daily summaries into a weekly report every Friday:

```markdown
Generate a weekly summary from this week's git and GitHub activity.

## Output

### This Week's Highlights
- [Top 3-5 accomplishments]

### Shipped
- [Features/fixes that landed in main]

### In Review
- [Open PRs with status]

### Metrics
- Commits: [N]
- PRs merged: [N]
- PRs reviewed: [N]
- Issues closed: [N]

### Next Week's Focus
1. [Based on open work and upcoming deadlines]
2. [...]
3. [...]

Keep under 300 words. Focus on impact, not activity.
```

## Customization

### For Team Leads

Add a team section:

```markdown
### Team Activity
- [Team member]: [key PR or accomplishment]
- Blockers affecting the team: [list]
- PRs needing attention: [list with reviewer needed]
```

### For On-Call Rotations

Add an on-call handoff section:

```markdown
### On-Call Handoff
- Active incidents: [none / list]
- Alerts that fired today: [count, any patterns]
- Things to watch overnight: [specific concerns]
- Runbook updates needed: [any gaps found today]
```

## Example Output

```
### Accomplished
- Shipped rate limiting on auth endpoints (PR #234 merged)
- Reviewed and approved database migration for user profiles (PR #228)
- Fixed flaky test in payment processing suite (PR #241)

### Meetings -> Action Items
| Meeting | Key Outcome | My Action Items |
|---------|-------------|-----------------|
| Sprint planning | Committed to auth migration | Start RFC by Wednesday |
| Design review | Approved new API versioning scheme | Update API docs |

### Commitments Made
- Promised @sarah: API versioning doc update by Thursday
- Told @alex: will review PR #245 tomorrow morning

### Open Loops
- PR #239 (caching layer) waiting on @alex's review since yesterday
- Question in #architecture about event sourcing -- no response yet

### Tomorrow's Plan
1. Review PR #245 (promised @alex)
2. Start RFC for auth migration (sprint commitment)
3. Follow up on caching PR #239
```
