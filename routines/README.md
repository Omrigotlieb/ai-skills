# Claude Code Routines

Routines are scheduled or recurring automations that run Claude Code on your behalf. They combine skills, MCP servers, and prompts into workflows that execute on a schedule — daily briefings, nightly maintenance, weekly reviews.

> **New to routines?** Start with [Morning Briefing](#morning-briefing) and [Email Triage](#email-triage) — they deliver the highest value with minimal setup.

## Quick Navigation

- [Morning Briefing](#morning-briefing)
- [Email Triage](#email-triage)
- [PR Monitor](#pr-monitor)
- [Nightly Maintenance](#nightly-maintenance)
- [Evening Review](#evening-review)
- [Weekly Retrospective](#weekly-retrospective)
- [Building Your Own](#building-your-own)
- [Recommended Daily Schedule](#recommended-daily-schedule)

---

## Morning Briefing

**Schedule:** Daily, 7–8 AM · **Trigger:** Cron or scheduled task

Produces a "readable in under 3 minutes" briefing covering your calendar, tasks, and priorities.

**Output sections:**
1. Top 3 priorities with rationale
2. Calendar — meetings with prep notes and smart questions
3. Urgent items requiring immediate attention
4. Quick wins (10–15 minute tasks)
5. Risks or conflicts to watch

→ [Full template and setup](morning-briefing.md)

---

## Email Triage

**Schedule:** Daily, 7 AM · **Trigger:** Cron or scheduled task · **Requires:** Gmail MCP

The single most recommended starting automation. Classifies inbox, drafts replies, and posts a summary.

**What it does:**
1. Fetches unread emails from the last 24 hours
2. Classifies as: urgent / action-required / FYI / newsletter
3. Drafts replies for urgent emails
4. Labels and archives low-priority items
5. Outputs summary to Slack or file

→ [Full template and setup](email-triage.md)

---

## PR Monitor

**Schedule:** Every 15–30 min during work hours · **Trigger:** `/loop` or cron · **Requires:** GitHub CLI

Watches open PRs from push to merge — runs CI checks, triages review feedback, implements fixes.

**What it does:**
1. Checks PR status and CI results
2. Fetches and triages code review comments
3. Implements fixes for actionable feedback
4. Re-triggers checks and validates
5. Escalates blocking issues

→ [Full template and setup](pr-monitor.md)

---

## Nightly Maintenance

**Schedule:** Nightly, midnight–2 AM · **Trigger:** Cron or scheduled task

Runs background housekeeping while you sleep — backlog triage, test coverage, dependency checks.

**Includes:**
- Issue triage and labeling
- Test coverage gap detection
- Dependency vulnerability scanning
- Documentation drift detection
- Optional: automated bug fix attempts with draft PRs

→ [Full template and setup](nightly-maintenance.md)

---

## Evening Review

**Schedule:** Daily, 6 PM · **Trigger:** Cron or manual

A structured 15-minute daily reflection that captures what happened and sets up tomorrow.

**6-question framework:**
1. Mood and energy level
2. Key activities — 2–3 most significant things
3. Progress toward goals — what moved the needle
4. Blockers and friction points
5. Tomorrow's focus and priorities
6. Creative thoughts to capture

→ [Full template and setup](evening-review.md)

---

## Weekly Retrospective

**Schedule:** Sunday evening · **Trigger:** Cron or manual

Synthesizes daily reviews into a weekly picture with trend analysis and forward planning.

**Five phases:**
1. Theme sentence — one phrase that defines the week
2. Highlights and wins
3. Challenges and what didn't go as planned
4. Meta reflection — lessons learned
5. Forward look — the one thing to nail next week

→ [Full template and setup](weekly-retro.md)

---

## Recommended Daily Schedule

| Time | Routine | Priority |
|------|---------|----------|
| 7:00 AM | [Email Triage](email-triage.md) | Start here |
| 7:30 AM | [Morning Briefing](morning-briefing.md) | Start here |
| Work hours | [PR Monitor](pr-monitor.md) (every 15–30 min) | After basics work |
| 6:00 PM | [Evening Review](evening-review.md) | When ready |
| Midnight | [Nightly Maintenance](nightly-maintenance.md) | When ready |
| Sunday PM | [Weekly Retrospective](weekly-retro.md) | When ready |

**Progression path:** Start with Email Triage + Morning Briefing for one week. Add PR Monitor next. Then layer in Evening Review and Nightly Maintenance once the basics feel natural.

---

## Building Your Own

### Routine Structure

Every routine needs three things:

1. **Trigger** — when it runs (cron schedule, webhook, `/loop`, or manual)
2. **Context** — what information it needs (MCP servers, files, APIs)
3. **Output** — where results go (file, Slack, email, PR)

### Setup Methods

**Scheduled tasks (recommended for daily routines):**
```bash
claude schedule create \
  --name "morning-briefing" \
  --cron "0 7 * * *" \
  --prompt "Run the morning briefing routine..."
```

**Loop mode (recommended for monitoring):**
```bash
claude /loop 15m "Check PR #123 status and fix any review comments"
```

**Desktop tasks (recommended for interactive routines):**
Use Claude Desktop's task scheduling for routines that benefit from human-in-the-loop interaction, like Evening Review.

### Best Practices

1. **Be explicit about success criteria** — "run npm audit, filter for severity high or critical" beats "check for issues"
2. **Start human-in-the-loop** before going fully autonomous
3. **Scope MCP connectors** to only what the routine needs
4. **Use a shared context file** (`SHARED_TASK_NOTES.md`) for context persistence between iterations
5. **Save your best prompts as templates** — rewriting prompts wastes time
6. **Separate capture from synthesis** — don't try to simultaneously experience your day and make sense of it

### MCP Servers Commonly Used

| Server | Used By |
|--------|---------|
| Gmail | Email Triage |
| Google Calendar | Morning Briefing |
| GitHub | PR Monitor, Nightly Maintenance |
| Slack | All (for output delivery) |
| Linear / Jira | Nightly Maintenance (issue triage) |
| Notion / Obsidian | Evening Review, Weekly Retro |

See [MCP Server guides](../mcp-servers/README.md) for setup instructions.

---

## Resources

- [Claude Code Documentation](https://code.claude.com/docs) — official docs, including scheduled tasks and automation
- [Anthropic Best Practices](https://www.anthropic.com/engineering/claude-code-best-practices) — engineering guidance for Claude Code workflows
- [Workflows](../workflows/README.md) — related one-off patterns for development tasks
- [Hooks Guide](../hooks/README.md) — lifecycle automation for event-driven workflows
- [MCP Server Guides](../mcp-servers/README.md) — set up the integrations routines depend on
