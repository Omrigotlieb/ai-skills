# Morning Briefing

**Trigger:** Schedule | **Frequency:** Daily at 8am | **Category:** Standup

Delivers a concise morning status report covering overnight CI results, new issues, pending review requests, and upcoming deadlines. Developers report saving 30-45 minutes of daily context-gathering.

## Setup

```bash
claude /schedule create \
  --name "morning-briefing" \
  --cron "0 8 * * 1-5" \
  --prompt "$(cat <<'EOF'
You are generating a daily morning briefing for the development team.

## Task
1. Check CI/CD status:
   - Are all builds on the main branch passing?
   - Any overnight deploy failures?
   - List any currently failing pipelines with links

2. Review new activity since yesterday 5pm:
   - New issues opened (group by priority)
   - PRs awaiting review (who is blocking whom)
   - PRs merged overnight
   - New comments on open PRs that need attention

3. Check operational health:
   - Any new dependency vulnerability alerts
   - Any new error spikes in monitoring (if Sentry/Datadog MCP is configured)

4. Upcoming deadlines:
   - Milestones or releases due this week
   - Any scheduled maintenance windows

## Output Format
Send an email to the team with this structure:

### Morning Briefing - <date>

**CI Status:** [green/yellow/red] - [one-line summary]

**Needs Attention:**
- [Ranked list of items requiring immediate action]

**Overnight Activity:**
- [X] issues opened, [Y] PRs merged, [Z] PRs awaiting review

**This Week:**
- [Upcoming deadlines and milestones]

## Constraints
- Keep the briefing under 20 lines. Developers will not read a wall of text.
- Link to specific PRs and issues, do not just count them.
- If everything is green and quiet, say so in 2 lines and stop.
EOF
)"
```

## Customization

- **Channels:** Send to Slack, email, or both depending on team preference
- **Scope:** Filter to specific repos or teams for larger organizations
- **Schedule:** Adjust time zone and skip weekends with `1-5` day range
- **Depth:** Add or remove sections based on what your team finds useful

## Related

- [Standup Summary](standup-summary.md) for per-developer activity reports
- [PR Branch Monitor](pr-branch-monitor.md) for continuous PR status tracking
