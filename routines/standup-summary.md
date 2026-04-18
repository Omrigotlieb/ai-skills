# Standup Summary

**Trigger:** Schedule | **Frequency:** Daily before standup | **Category:** Standup

Aggregates each developer's commits, PRs opened/merged, issues closed, and blockers from the previous day. Posts a pre-formatted standup report so the team can focus on problem-solving instead of status reporting.

## Setup

```bash
claude /schedule create \
  --name "standup-summary" \
  --cron "15 8 * * 1-5" \
  --prompt "$(cat <<'EOF'
You are generating a daily standup summary for the team.

## Task
1. For each active contributor (committed or commented in the last 7 days):
   - List commits pushed yesterday (group by PR/branch)
   - List PRs opened, updated, or merged yesterday
   - List issues closed or commented on yesterday
   - Identify any PRs blocked on review (open > 24 hours with no review)

2. Identify team-level blockers:
   - PRs with merge conflicts
   - Failed CI on the main branch
   - Issues marked "blocked" or "needs-help"

## Output Format
Post to the standup channel:

### Daily Standup - <date>

**Team Blockers:**
- [list or "None"]

---

**<Developer Name>**
- Yesterday: [1-2 line summary of commits/PRs/issues]
- Blocked: [any blocked PRs or "None"]

**<Developer Name>**
- Yesterday: [1-2 line summary]
- Blocked: [any blocked PRs or "None"]

---
*Generated from git activity. Reply to add context or corrections.*

## Constraints
- Keep each developer's section to 3 lines maximum.
- Do not infer "what they will do today" - only report what happened.
- If a developer had no activity, omit them rather than reporting "no activity."
- Respect any .standup-ignore file listing developers who opted out.
EOF
)"
```

## Customization

- **Channel:** Post to Slack, email, or a GitHub Discussion
- **Scope:** Filter to specific repos for multi-repo teams
- **Format:** Adjust the template to match your standup format (Yesterday/Today/Blockers)
- **Timing:** Run 15 minutes before your standup meeting time

## Related

- [Morning Briefing](morning-briefing.md) for operational status beyond individual activity
- [Weekly Quality Dashboard](weekly-quality-dashboard.md) for aggregate trends
