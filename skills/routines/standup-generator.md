# Standup Generator Routine

Builds a standup update from git history and issue tracker activity so you never have to think about what you did yesterday.

---

## Overview

| Property | Value |
|----------|-------|
| **Schedule** | `45 8 * * 1-5` (weekdays at 8:45 AM, before standup) |
| **Duration** | ~15 seconds to generate |
| **Sources** | Git log, GitHub PRs/issues |

## Setup

Create via `/schedule` in Claude Code: `/schedule weekdays at 8:45am: standup generator`

Or create at `claude.ai/code/routines` with cron `45 8 * * 1-5` and the prompt below.

### Basic

Use this prompt:

```markdown
Generate my standup update from yesterday's activity.

## Sources
- Git log: commits by me since yesterday
- GitHub: PRs I opened, reviewed, or merged
- Issues: status changes on issues assigned to me

## Output Format
**Yesterday:** [2-3 bullet points of what was accomplished]
**Today:** [2-3 bullet points based on open PRs and assigned issues]
**Blockers:** [any PRs waiting on review > 24h, failing CI, unresolved questions]

Keep it under 100 words. Use past tense for yesterday, future tense for today.
Group related commits into single accomplishments -- don't list every commit.
```

### Full (With Slack and Calendar)

```markdown
Generate my standup update from yesterday's activity.

## Sources
1. **Git**: commits by me since last standup
2. **GitHub**: PRs opened, reviewed, merged, or commented on
3. **Calendar**: meetings attended yesterday that produced action items
4. **Slack**: threads where I committed to doing something

## Output
**Yesterday:**
- [2-3 outcome-focused bullets, not activity-focused]

**Today:**
- [2-3 bullets based on open work, deadlines, and commitments]

**Blockers:**
- [PRs waiting on review > 24h]
- [CI failures I can't resolve alone]
- [Dependencies on other teams]

## Rules
- Focus on outcomes ("shipped rate limiting") not activity ("edited 4 files")
- Collapse WIP/fixup commits into their parent feature
- If I committed to something in Slack, include it in Today
- Keep under 100 words total
- After Monday weekends, cover Friday-Monday as "Last week"
```

### Monday Variant

Automatically handles the Friday-Monday gap:

```markdown
Generate my Monday standup. Cover activity from Friday through today.

**Last week (Friday):** [what I shipped or reviewed]
**This week:** [priorities based on open PRs, sprint board, and upcoming deadlines]
**Blockers:** [anything from last week still unresolved]

Keep under 120 words.
```

## Delivery Options

### Post to Slack

```markdown
After generating the standup, post it to #team-standup channel.
Format as a single message with bold section headers.
```

### Copy to Clipboard

```markdown
After generating the standup, copy the output to the system clipboard
so I can paste it into the standup tool.
```

## Example Output

```
**Yesterday:**
- Shipped rate limiting on auth endpoints (PR #234 merged)
- Reviewed database migration for user profiles (PR #228, approved)
- Fixed flaky payment processing test (PR #241)

**Today:**
- Start RFC for auth migration (sprint commitment, due Wednesday)
- Review PR #245 (promised @alex)
- Follow up on caching PR #239 (waiting on review since Tuesday)

**Blockers:**
- PR #239 waiting on @alex's review for 3 days
```
