# Claude Code Routines & Scheduled Tasks

Automate recurring development workflows with Claude Code. Routines run prompts on a schedule, on events, or via API without requiring an open terminal.

> **Three tiers:** Session-scoped `/loop` | Desktop scheduled tasks | Cloud routines

---

## Quick Navigation

- [Choosing the Right Tier](#choosing-the-right-tier)
- [Session Loops (/loop)](#session-loops-loop)
- [Desktop Scheduled Tasks](#desktop-scheduled-tasks)
- [Cloud Routines](#cloud-routines)
- [Routine Catalog](#routine-catalog)
- [Writing Good Routine Prompts](#writing-good-routine-prompts)
- [Example loop.md Files](#example-loopmd-files)

---

## Choosing the Right Tier

| | Cloud Routines | Desktop Tasks | `/loop` |
|---|---|---|---|
| **Runs on** | Anthropic cloud | Your machine | Your machine |
| **Machine must be on** | No | Yes | Yes |
| **Open session required** | No | No | Yes |
| **Survives restarts** | Yes | Yes | Restored on `--resume` |
| **Access to local files** | No (fresh clone) | Yes | Yes |
| **MCP servers** | Connectors per task | Config files | Inherits session |
| **Minimum interval** | 1 hour | 1 minute | 1 minute |
| **Daily run limits** | Pro: 5, Max: 15, Team: 25 | Unlimited | Unlimited |

**Rule of thumb:**
- Quick polling during active work → `/loop`
- Local automation that needs your files → Desktop tasks
- Unattended, always-on automation → Cloud routines

---

## Session Loops (/loop)

The fastest way to run a prompt on repeat while your session is open.

### Fixed interval

```
/loop 5m check if the deployment finished and tell me what happened
```

### Self-paced (Claude picks the interval)

```
/loop check whether CI passed and address any review comments
```

### Built-in maintenance (no prompt)

```
/loop
```

Runs the default maintenance prompt: continue unfinished work, tend to the current PR, run cleanup passes. Customize with a `loop.md` file.

### Customize with loop.md

Place at `.claude/loop.md` (project) or `~/.claude/loop.md` (global). The file replaces the built-in maintenance prompt for bare `/loop`.

```markdown
# .claude/loop.md

Check the `release/next` PR. If CI is red, pull the failing job log,
diagnose, and push a minimal fix. If new review comments have arrived,
address each one and resolve the thread. If everything is green and
quiet, say so in one line.
```

See [example loop.md files](examples/) for more templates.

### Stop a loop

Press `Esc` to cancel the pending wakeup.

---

## Desktop Scheduled Tasks

Run locally on your machine, each firing a fresh session at the time and frequency you choose. Tasks persist across restarts.

### Create via CLI

```bash
# Interactive setup
claude schedule create

# Or use /schedule in a session
/schedule
```

### Task file structure

Tasks live at `~/.claude/scheduled-tasks/<task-name>/SKILL.md`:

```markdown
---
name: morning-briefing
description: Daily development status briefing
---

Review all open PRs in this repository. For each PR:
- Check CI status
- Summarize recent review comments
- Flag any that are stale (>3 days without activity)

Post a summary listing what needs attention today.
```

---

## Cloud Routines

Run on Anthropic-managed infrastructure. No open laptop required.

### Create a routine

1. Navigate to `claude.ai/code/routines`
2. Click **New Routine**
3. Write your prompt
4. Connect repositories
5. Choose triggers (schedule, API, GitHub events)

### Trigger types

| Trigger | Use Case | Example |
|---|---|---|
| **Schedule** | Recurring cadence | Daily at 9am, weekdays only |
| **API** | Event-driven | Monitoring alert fires POST to endpoint |
| **GitHub** | Repository events | PR opened, release published |

Triggers can be combined on a single routine.

### API trigger

```bash
curl -X POST \
  "https://api.anthropic.com/v1/claude_code/routines/{trigger_id}/fire" \
  -H "Authorization: Bearer $TOKEN" \
  -H "anthropic-beta: experimental-cc-routine-2026-04-01" \
  -H "anthropic-version: 2023-06-01" \
  -H "Content-Type: application/json" \
  -d '{"text": "Production alert: error rate exceeded 5% on /api/checkout"}'
```

### GitHub trigger events

- `pull_request`: opened, closed, assigned, labeled, synchronized
- `release`: created, published, edited, deleted

Filter by: author, title, body, base/head branch, labels, draft status, merged status.

---

## Routine Catalog

Practical routines organized by use case. Each includes the prompt template and recommended trigger.

### Developer Daily Workflows

#### Morning Standup Brief

**Trigger:** Schedule, weekdays at 8:30am

```
Read all open PRs and recent commits in the repository.
Post a summary to the #dev-standup Slack channel with:

- What landed yesterday (merged PRs with one-line descriptions)
- What's in flight (open PRs with CI status)
- What's blocked or stale (PRs older than 3 days without activity)

Use bullet points. If nothing changed overnight: "No updates since yesterday."
```

#### PR Triage & Review

**Trigger:** GitHub `pull_request.opened`

```
A new pull request has been opened. Review against this checklist:

## Security
- Hardcoded secrets, API keys, or credentials in diff?
- Unvalidated user inputs that could enable injection?
- New dependencies with known CVEs?

## Performance
- N+1 query patterns in ORM calls?
- Missing database indexes for new query patterns?
- Large synchronous operations that should be async?

## Code Quality
- Follows project linting configuration?
- Consistent naming with existing codebase?
- Tests for new functionality?

Leave inline comments on each issue with specific fix suggestions.
Post a top-level summary: pass/fail for each category.
If all clear: "LGTM — no mechanical issues found."
```

#### CI Failure Monitor

**Trigger:** `/loop 5m` or Schedule hourly

```
Check the latest CI run on the current branch.
If any jobs failed:
1. Pull the failing job log
2. Identify the root cause
3. If it's a flaky test, re-run the job
4. If it's a real failure, diagnose and propose a fix

If all jobs passed: "CI green ✓" (one line, no details).
```

---

### Repository Maintenance

#### Nightly Issue Triage

**Trigger:** Schedule, daily at 11pm

```
Read all GitHub issues opened today in this repository.

For each issue:
- Apply a label from: bug, feature, docs, question, needs-triage
- Assign based on referenced files/directories (check CODEOWNERS)
- If missing reproduction steps, comment requesting more info

After processing, post a summary to #dev-triage:
- Total issues processed
- Breakdown by label
- Issues flagged for human attention

If zero new issues: "No new issues today."
```

#### Weekly Docs Drift Detection

**Trigger:** Schedule, Mondays at 9am

```
Scan all pull requests merged in the past 7 days.
For each PR, identify any documentation files that reference
modified functions, APIs, or configuration options.

If documentation is outdated relative to code changes,
open a PR with suggested updates targeting the docs.

Post summary to #docs channel:
- Number of docs PRs opened
- Which APIs/functions had documentation gaps
- Any docs that need manual review
```

#### Stale Branch Cleanup Report

**Trigger:** Schedule, Fridays at 4pm

```
List all remote branches in this repository.
Identify branches that:
- Have no commits in the past 30 days
- Are not protected branches (main, develop, release/*)
- Have no associated open PRs

Generate a report with:
- Branch name and last commit date
- Author of last commit
- Whether it was merged to main

Do NOT delete any branches. Post the report for human review.
```

#### Dependency Update Check

**Trigger:** Schedule, weekly

```
Check for outdated dependencies in this project.
For each outdated package:
- Current version vs latest version
- Whether it's a major/minor/patch update
- Check for known security advisories
- Note any breaking changes in changelog

Group by priority:
1. Security vulnerabilities (update immediately)
2. Major version bumps (review needed)
3. Minor/patch updates (safe to batch)

Create an issue summarizing findings.
```

---

### Incident Response

#### Alert Triage

**Trigger:** API (called by Datadog/Sentry/PagerDuty)

```
A production alert has fired. The alert context is provided below.

1. Extract the stack trace and error details
2. Correlate with commits from the past 24 hours using git log
3. Identify the most likely root cause
4. Generate a draft pull request with a proposed fix
5. Include the alert ID and link in the PR description

Create the PR as a draft. Never merge automatically.
Post findings to #incidents Slack channel.
```

#### Deploy Verification

**Trigger:** API (called by CD pipeline after deploy)

```
A new version has been deployed to production.

1. Run smoke checks against the deployed build
2. Check error monitoring (Sentry) for new error patterns
3. Compare error rates before/after deploy (15-minute window)
4. Check key API endpoint response times

Post go/no-go assessment to #releases:
- GREEN: No regressions detected
- YELLOW: Minor anomalies (list them)
- RED: Regression detected (include details and recommended action)
```

---

### Communication & Reporting

#### Daily Email Triage

**Trigger:** Schedule, weekdays at 8am

```
Check Gmail inbox for unread messages received since yesterday.

For each message:
- Categorize: urgent, needs-reply, informational, can-ignore
- For urgent items: draft a reply and save as draft
- For needs-reply: summarize what's being asked

Post a morning briefing to Slack DM:
- Urgent items requiring immediate attention
- Messages needing replies (with draft links)
- Informational items (one-line summaries)
- Total unread count

Keep the briefing scannable. No more than 20 lines.
```

#### Weekly Project Summary

**Trigger:** Schedule, Fridays at 5pm

```
Generate a weekly project summary covering the past 7 days:

## Activity
- PRs merged (count and titles)
- Issues opened vs closed
- Lines of code changed

## Highlights
- Notable features shipped
- Bugs fixed
- Performance improvements

## Looking Ahead
- Open PRs needing review
- Upcoming milestones or deadlines
- Known blockers

Keep it concise. Format for pasting into a status update.
```

---

### Multi-Language & SDK Sync

#### Library Port on Merge

**Trigger:** GitHub `pull_request.closed` (filtered to merged)

```
A pull request has been merged to the Python SDK.

1. Read the merged diff carefully
2. Port the changes to the equivalent Go SDK files
3. Maintain Go idioms (error handling, naming conventions)
4. Update corresponding Go tests
5. Open a draft PR in the Go SDK repository

Title format: "Port: [original PR title]"
Include link to original Python PR in description.
Never merge automatically. Flag any changes that don't have a clean Go equivalent.
```

---

## Writing Good Routine Prompts

Routines run autonomously with no interactive approval. The prompt carries the full cognitive load.

### Do

- **Be explicit about outputs**: "Post to #dev-standup" not "share the results"
- **Define boundaries**: "Create draft PRs only. Never merge. Never push to main."
- **Handle the empty case**: "If no new issues opened since last run, post 'nothing to triage'"
- **Name connectors explicitly**: Specify which Slack workspace, Sentry project, or Linear team
- **Set success criteria**: "If all checks pass, post single-line confirmation"

### Don't

- Leave actions ambiguous: "Review the PRs" (review how? comment where?)
- Assume context from prior runs: Each routine starts a fresh session
- Skip edge cases: What if there are zero items? What if a connector fails?
- Use vague success criteria: "Make sure everything looks good"

### Prompt structure

```
[Context: What this routine does and when it runs]

[Step-by-step instructions with numbered actions]

[Output specification: where and how to report results]

[Edge cases and boundary conditions]

[Safety constraints: what the routine must NOT do]
```

---

## Example loop.md Files

Ready-to-use templates in the [examples/](examples/) directory:

| Template | Description |
|---|---|
| [pr-shepherd.md](examples/pr-shepherd.md) | Keep a PR healthy: fix CI, respond to reviews, rebase |
| [release-guard.md](examples/release-guard.md) | Monitor a release branch through the deploy pipeline |
| [morning-brief.md](examples/morning-brief.md) | Morning development briefing across repos |
| [issue-triage.md](examples/issue-triage.md) | Triage and label incoming GitHub issues |
| [deploy-watch.md](examples/deploy-watch.md) | Watch a deployment and report status changes |

---

## Cron Expression Reference

For `CronCreate` and Desktop tasks:

| Expression | Meaning |
|---|---|
| `*/5 * * * *` | Every 5 minutes |
| `0 * * * *` | Every hour on the hour |
| `0 9 * * *` | Daily at 9am local |
| `0 9 * * 1-5` | Weekdays at 9am local |
| `0 17 * * 5` | Fridays at 5pm local |
| `0 23 * * 0-4` | Sun-Thu at 11pm local |

Day-of-week: `0` or `7` = Sunday, `1` = Monday, ... `6` = Saturday.

---

## Resources

### Official
- [Scheduled Tasks (docs)](https://code.claude.com/docs/en/scheduled-tasks)
- [Cloud Routines (docs)](https://code.claude.com/docs/en/routines)
- [Desktop Scheduled Tasks (docs)](https://code.claude.com/docs/en/desktop-scheduled-tasks)
- [Introducing Routines (blog)](https://claude.com/blog/introducing-routines-in-claude-code)

### Guides
- [Routines Practical Guide](https://nimbalyst.com/blog/claude-code-routines-practical-guide/)
- [Scheduled Tasks Setup Guide](https://claudefa.st/blog/guide/development/scheduled-tasks)
- [Loop vs Scheduled Tasks](https://www.mindstudio.ai/blog/claude-code-loop-vs-scheduled-tasks)
- [Routines Tutorial (Builder.io)](https://www.builder.io/blog/claude-code-routines)
- [Schedule GitHub Issue Triage](https://startdebugging.net/2026/04/how-to-schedule-a-recurring-claude-code-task-that-triages-github-issues/)

### Community
- [claude-mcp-scheduler](https://github.com/tonybentley/claude-mcp-scheduler) - Cron scheduling with MCP servers
- [Daily Briefing with Claude Cowork](https://petrvojacek.cz/en/blog/claude-cowork-daily-briefing/)
- [Routines for Solopreneurs](https://medium.com/@christianaistudio/your-business-runs-while-you-sleep-13-claude-routines-that-react-without-you-5ddb96da66f7)
