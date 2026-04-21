# Morning Briefing Routine

A comprehensive guide to setting up an automated morning briefing that aggregates signals from your development tools into a single prioritized summary.

---

## Overview

| Property | Value |
|----------|-------|
| **Schedule** | `0 7 * * 1-5` (weekdays at 7 AM) |
| **Duration** | ~30 seconds to generate |
| **Time saved** | 30-45 minutes of manual dashboard checking per day |
| **Sources** | Email, calendar, GitHub, Slack |

## Setup

### Basic (GitHub-only)

```bash
claude schedule create \
  --name "morning-briefing" \
  --cron "0 7 * * 1-5" \
  --prompt "$(cat <<'EOF'
Generate my morning briefing from GitHub activity in the last 24 hours.

## Check
1. PRs assigned to me for review
2. PRs I authored -- status (CI, reviews, merge conflicts)
3. Issues assigned to me -- any new comments or status changes
4. Repositories I watch -- any failing CI on main branch

## Output
### Needs Action
- [PR/issue with one-line context and link]

### My PRs Status
- [PR title] -- [status: approved/changes-requested/waiting/CI-failing]

### New Issues
- [issue title] -- [priority estimate]

If nothing needs action, say "All clear" and list today's open PR count.
EOF
)"
```

### Full (Multi-Source with MCP)

Requires MCP servers for Gmail, Google Calendar, and Slack:

```json
{
  "mcpServers": {
    "gmail": {
      "command": "npx",
      "args": ["-y", "@anthropic/mcp-gmail"],
      "env": { "GMAIL_CREDENTIALS": "${GMAIL_CREDENTIALS}" }
    },
    "google-calendar": {
      "command": "npx",
      "args": ["-y", "@anthropic/mcp-google-calendar"],
      "env": { "GCAL_CREDENTIALS": "${GCAL_CREDENTIALS}" }
    },
    "slack": {
      "command": "npx",
      "args": ["-y", "@anthropic/mcp-slack"],
      "env": { "SLACK_TOKEN": "${SLACK_TOKEN}" }
    }
  }
}
```

```bash
claude schedule create \
  --name "morning-briefing-full" \
  --cron "0 7 * * 1-5" \
  --prompt "$(cat <<'EOF'
Generate my morning briefing. Scan these sources for the last 24 hours:

## Sources
1. **Email** (via Gmail MCP):
   - Threads needing a reply (skip newsletters and automated notifications)
   - Anything mentioning a deadline within 48 hours
2. **Calendar** (via Google Calendar MCP):
   - Today's meetings with attendees and one-line purpose
   - Flag any conflicts or back-to-back blocks > 2 hours
3. **GitHub** (via gh CLI):
   - PRs I need to review
   - My PR statuses
   - Issues assigned to me with new activity
4. **Slack** (via Slack MCP):
   - Unread DMs
   - Channel mentions I haven't responded to
   - Threads where I was asked a question

## Output Format

### Needs Action (do first)
- [icon] [item] -- [one-line context] [source]

### Today's Schedule
| Time | Meeting | Prep Needed |
|------|---------|-------------|
| ... | ... | ... |

### Awareness (no action yet)
- [item] -- [context]

## Rules
- Maximum 15 items total across all sections
- Skip anything purely informational
- If a meeting has no clear agenda, flag it as "agenda needed"
- Prioritize by: deadline proximity > blocking others > assigned to me
EOF
)"
```

## Customization Tips

### Adjusting Priority

Add project-specific priority rules:

```markdown
## Priority Overrides
- Anything from the #incidents channel is always top priority
- PRs touching the payments/ directory get flagged as high-priority
- Issues labeled "P0" or "P1" always appear in Needs Action
```

### Delivery Options

**Email delivery:**
```markdown
After generating the briefing, send it to my email address as a formatted summary.
```

**Slack delivery:**
```markdown
After generating the briefing, post it to my #daily-briefing Slack channel.
```

### Weekend Mode

For on-call weekends, create a lighter version:

```bash
claude schedule create \
  --name "weekend-oncall-check" \
  --cron "0 9 * * 0,6" \
  --prompt "Quick oncall check: any P0/P1 issues opened? Any alerts fired? Any PRs marked urgent? If all clear, say 'All clear' in one line."
```

## Iteration Guide

After the first week of running the briefing:

1. **Too noisy?** Add more items to the skip list (automated notifications, bot PRs)
2. **Missing context?** Add specific repos or channels to scan
3. **Wrong priorities?** Adjust the priority rules to match your actual workflow
4. **Too long?** Reduce the max items or tighten the "Needs Action" criteria
5. **Not actionable?** Require each item to have a clear next step

## Example Output

```
### Needs Action (do first)
- Review PR #234 "Add rate limiting to auth endpoints" -- requested 18h ago, 2 approvals needed [GitHub]
- Reply to thread from @sarah about API versioning strategy -- question asked yesterday [Slack]
- Email from legal@ re: data retention policy changes -- deadline Friday [Email]

### Today's Schedule
| Time | Meeting | Prep Needed |
|------|---------|-------------|
| 10:00 | Sprint planning | Review backlog items tagged "next-sprint" |
| 14:00 | 1:1 with manager | Prepare status update on auth migration |
| 16:00 | Design review | Read RFC-042 beforehand |

### Awareness (no action yet)
- PR #228 CI is green, waiting on @alex's review [GitHub]
- New issue #301 "Improve error messages" assigned to me, P3 [GitHub]
```
