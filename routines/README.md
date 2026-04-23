# Claude Code Routines & Scheduled Tasks

Routines are recurring tasks that Claude Code runs on a schedule, in response to events, or as part of a CI/CD pipeline. They turn Claude from a reactive assistant into a proactive teammate that monitors, reviews, and maintains your codebase autonomously.

> Links last verified: 2026-04-23

## Quick Navigation

- [Daily Routines](daily.md) -- Morning briefing, code review, activity summary
- [Weekly Routines](weekly.md) -- Dependency audit, code quality, security scan, docs drift
- [Event-Driven Routines](event-driven.md) -- PR review, deploy verification, alert triage
- [GitHub Actions Examples](github-actions.md) -- CI/CD workflow templates

---

## How Routines Work

Routines run in three tiers, each suited to different use cases:

| Tier | Where it runs | Trigger types | Best for |
|------|--------------|---------------|----------|
| **Cloud Routines** | Anthropic infrastructure | Schedule, API, GitHub events | Mission-critical recurring tasks |
| **Desktop Scheduled Tasks** | Local machine | Cron schedule | Environment-specific work needing local file/MCP access |
| **CLI Session Tasks** (`/loop`) | Active terminal session | Interval or self-paced | Quick polling and in-session monitoring |

### Cloud Routines (claude.ai/code/routines)

Available on Team and Enterprise plans. Create them from the Claude Code web dashboard:

```
Schedule  -->  Claude reads your repo  -->  Takes action  -->  Reports results
```

Plan limits:
| Plan | Daily runs |
|------|-----------|
| Pro | 5 |
| Max | 15 |
| Team | 25 |
| Enterprise | 25 |

### Desktop Scheduled Tasks

Local scheduled tasks run on your machine with full access to your filesystem, MCP servers, and skills:

```bash
# Create a scheduled task
claude schedule create --name "morning-briefing" \
  --cron "30 8 * * 1-5" \
  --prompt "Run the morning briefing routine"

# List scheduled tasks
claude schedule list

# Run a task immediately
claude schedule run morning-briefing
```

### Session-Scoped Tasks (`/loop`)

Ephemeral tasks that live within a terminal session:

```
/loop 5m check build status and report any failures
```

---

## Writing Good Routine Prompts

The quality of a routine depends on the specificity of its prompt.

**Bad:**
```
Check for errors
```

**Good:**
```
Pull the last 24 hours of error logs from the production API.
Summarize the top 5 errors by frequency.
Write the report to /reports/daily-errors-YYYY-MM-DD.md
```

### Prompt Checklist

- State the **scope** (which files, directories, or systems)
- Define the **output format** (markdown report, PR, Slack message, commit)
- Set **thresholds** (what counts as a problem worth flagging)
- Specify **time range** (last 24h, since last run, past week)
- Include **skip conditions** (don't run if no changes, skip weekends)

---

## CLAUDE.md Integration

Routines read your project's `CLAUDE.md` for context. Add a section for routine-specific instructions:

```markdown
## Routine Instructions

### Code Quality Reviews
- Skip test files when counting complexity
- Flag functions over 50 lines
- Ignore vendor/ and generated/ directories

### Dependency Audits
- Pre-approved packages: lodash, zod, prisma, vitest
- Block any package with Critical CVEs
- Auto-update patch versions only
```

---

## Key Resources

| Resource | Description |
|----------|-------------|
| [Official Routines Docs](https://code.claude.com/docs/en/routines) | Anthropic's guide to cloud routines |
| [Scheduled Tasks Docs](https://code.claude.com/docs/en/scheduled-tasks) | Desktop scheduled task documentation |
| [claude-code-scheduler](https://github.com/jshchnz/claude-code-scheduler) | Open-source scheduler with task examples |
| [claude-skills-weekly](https://github.com/er1chu/claude-skills-weekly) | Monday/Daily/Friday productivity cycle |
| [claude-code-showcase](https://github.com/ChrisWiles/claude-code-showcase) | Complete project config with Actions workflows |
