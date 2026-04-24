# Morning Briefing Routine

**Schedule:** Daily, 7–8 AM · **Duration:** Produces a 3-minute read · **Requires:** Google Calendar MCP (optional), task tracker MCP (optional)

## What It Does

Produces a structured morning briefing that replaces 20–30 minutes of manual inbox/calendar/task scanning with a single document you can read over coffee.

## Setup

### As a Scheduled Task

```bash
claude schedule create \
  --name "morning-briefing" \
  --cron "0 7 * * 1-5" \
  --prompt "$(cat <<'EOF'
Generate my morning briefing for today.

## Steps
1. Check my calendar for today's meetings
2. Review open tasks and their deadlines
3. Scan recent Slack activity for anything urgent
4. Check CI/CD status for any failing builds

## Output Format
Write the briefing to `briefs/YYYY-MM-DD.md` using this structure:

### 🎯 Top 3 Priorities
[Ranked by urgency × importance. Each gets one line explaining WHY it's a priority today.]

### 📅 Calendar
[For each meeting: title, time, attendees, one-line objective, one preparation note, one smart question to ask]

### 🚨 Urgent
[Items that need a response or decision before noon. Include sender/source and suggested action.]

### ⚡ Quick Wins
[2-3 tasks that take under 15 minutes and clear mental load. Pull from task backlog.]

### ⚠️ Watch
[Risks, blockers, or conflicts to monitor. Include what triggers escalation.]

Keep the entire briefing under 500 words. Be specific — names, deadlines, PR numbers.
EOF
)"
```

### As a Custom Command

Create `.claude/commands/morning-brief.md`:

```markdown
Generate my morning briefing for today.

## Steps
1. Check my calendar for today's meetings
2. Review open tasks and their deadlines
3. Scan recent activity for anything requiring attention
4. Check CI/CD status for any failing builds

## Output
Write to `briefs/YYYY-MM-DD.md` with sections:
- Top 3 Priorities (ranked by urgency × importance)
- Calendar (meetings with prep notes)
- Urgent (items needing response before noon)
- Quick Wins (under 15 min, clears mental load)
- Watch (risks and blockers)

Keep under 500 words. Be specific.
```

Usage: `/project:morning-brief`

## Example Output

```markdown
# Morning Briefing — 2026-04-24

### 🎯 Top 3 Priorities
1. **Ship auth migration PR #847** — QA approved yesterday, merge window closes at 3 PM
2. **Respond to design review** — Sarah's waiting on component feedback since Tuesday
3. **Fix flaky test in CI** — payments-service pipeline blocked for 2 days

### 📅 Calendar
- **10:00 Sprint Planning** (45 min) — Team leads. Objective: scope next sprint.
  Prep: review backlog priorities. Ask: "Can we defer the dashboard rework?"
- **14:00 1:1 with Alex** (30 min) — Objective: discuss promotion timeline.
  Prep: bring project impact summary. Ask: "What does the next level look like?"

### 🚨 Urgent
- **Slack DM from ops**: Production memory spike on payments-service. Investigate before standup.
- **Email from legal**: Data retention policy sign-off due today.

### ⚡ Quick Wins
- Close 3 stale PRs from last sprint (5 min)
- Update README with new env var from yesterday's deploy (5 min)

### ⚠️ Watch
- Deploy freeze starts Friday for mobile release — get all non-critical merges in by Thursday EOD
```

## Customization

**Add MCP servers** to pull from your actual systems:

| Data Source | MCP Server | What It Provides |
|-------------|-----------|------------------|
| Calendar | Google Calendar | Today's meetings, attendees, conflicts |
| Email | Gmail | Urgent messages, threads awaiting reply |
| Tasks | Linear / Todoist | Open tasks, deadlines, sprint items |
| Chat | Slack | Unread DMs, mentions, channel activity |
| CI/CD | GitHub | Failing builds, open PRs, review requests |

**Adjust the prompt** for your role:
- **Engineering lead**: Add "check team PR queue" and "review on-call handoff notes"
- **Product manager**: Add "check customer feedback channels" and "review metric dashboards"
- **Founder**: Add "check pipeline/CRM updates" and "review cash position"

## Tips

- **Start simple**: Calendar + tasks is enough for week one. Add more data sources as you see gaps.
- **Output to where you'll read it**: Slack DM to yourself, a pinned file, or a Notion page.
- **Refine weekly**: After 5 briefings, adjust what's noisy vs. what's missing.
