# Claude Code Routines & Scheduled Automation

Production-ready routines, scheduled task patterns, and daily automation workflows for Claude Code. Routines run on Anthropic's cloud infrastructure while your machine stays off.

> **Official docs:** [Routines](https://code.claude.com/docs/en/routines) · [Scheduled Tasks](https://code.claude.com/docs/en/scheduled-tasks) · [Desktop Scheduled Tasks](https://code.claude.com/docs/en/desktop-scheduled-tasks)

---

## Quick Start

```bash
# Create a routine from the CLI
/schedule daily PR review at 9am

# One-off scheduled task
/schedule tomorrow at 9am, summarize yesterday's merged PRs

# Quick polling loop (session-scoped)
/loop 5m check if the deployment finished

# Dynamic interval (Claude picks timing)
/loop check whether CI passed and address any review comments
```

---

## Scheduling Options Compared

| Feature | Cloud Routines | Desktop Tasks | `/loop` |
|---------|---------------|---------------|---------|
| Runs on | Anthropic cloud | Your machine | Your machine |
| Machine required | No | Yes (app open) | Yes (session open) |
| Survives restart | Yes | Yes | Only with `--resume` |
| Local file access | No (fresh clone) | Yes | Yes |
| Min interval | 1 hour | 1 minute | 1 minute |
| Triggers | Cron, API, GitHub events | Cron | Cron or dynamic |
| Daily run caps | Pro: 5, Max: 15, Team: 25 | None | None |

**Rule of thumb:** Cloud routines for unattended work. Desktop tasks for local file access. `/loop` for quick session polling.

---

## Production Routine Prompts

### 1. Nightly Issue Triage

**Trigger:** Schedule, daily at 11pm
**Connectors:** GitHub, Slack

```
Read all GitHub issues opened in the last 24 hours in this repository.

For each issue:
1. Classify as bug, feature-request, question, or docs
2. Apply the matching label
3. Estimate priority (P0-P3) based on how many users or systems are affected
4. If a specific code area is mentioned, assign the CODEOWNERS contact

Post a triage summary to #engineering-triage on Slack with:
- Total new issues
- Breakdown by type and priority
- Any P0/P1 items that need immediate attention

Do not close or comment on issues. Label and assign only.
```

---

### 2. Morning Standup Prep

**Trigger:** Schedule, weekdays at 8:30am
**Connectors:** GitHub, Slack (optional)

```
Prepare a standup digest for the team. Check the last 24 hours:

1. PRs merged to main — list title, author, and files changed
2. PRs currently open and awaiting review — flag any older than 48 hours
3. CI failures on main — link to the failing run and identify the breaking commit
4. Issues moved to "In Progress" — who picked them up

Format as a concise digest:
## What shipped
## Waiting for review
## CI status
## In progress

Keep each section to bullet points. If nothing happened in a section, say "None."
```

---

### 3. PR Code Review

**Trigger:** GitHub event — `pull_request.opened`, filter: `is_draft = false`
**Connectors:** GitHub

```
Review this pull request using the team's review checklist:

1. Security: check for injection vulnerabilities, hardcoded secrets, unsafe deserialization
2. Performance: identify N+1 queries, unnecessary allocations, missing indexes
3. Correctness: trace the logic path, check edge cases, verify error handling
4. Style: flag deviations from project conventions in CLAUDE.md
5. Tests: confirm new behavior has test coverage, check for missing edge case tests

Leave inline comments on specific lines for issues found.
Post a summary comment with:
- Overall assessment (approve, request changes, or comment)
- Top 3 items to address (if any)
- What looks good

Do not approve or merge. Comment only.
```

---

### 4. Deploy Verification

**Trigger:** API (called from CD pipeline after deploy)
**Connectors:** GitHub, Slack

```
A production deploy just completed. The deploy details are in the trigger text.

Run verification:
1. Check the health endpoint returns 200
2. Run smoke tests against the production URL
3. Scan the last 15 minutes of error logs for new error patterns
4. Compare error rates to the pre-deploy baseline

Post results to #deploys on Slack:
- PASS or FAIL verdict
- Health check status
- Any new errors detected
- Smoke test results

If FAIL, tag @oncall in the Slack message and open a GitHub issue
with the error details and a link to the deploy commit.
```

---

### 5. Weekly Docs Drift Detection

**Trigger:** Schedule, weekly on Monday at 9am
**Connectors:** GitHub

```
Scan all pull requests merged in the past 7 days.

For each PR, identify any documentation files (README, docs/, wiki)
that reference modified functions, APIs, or configuration options.

If the documentation is outdated relative to the code changes,
open a PR with suggested updates. Group related doc updates into
a single PR when possible.

Title format: "docs: update references for [changed area]"

If no documentation drift is found, do nothing.
```

---

### 6. Dependency Audit

**Trigger:** Schedule, weekly on Wednesday at 6am
**Connectors:** GitHub

```
Audit project dependencies for security and freshness:

1. Run the package manager's audit command (npm audit, pip audit, etc.)
2. Check for dependencies with known CVEs
3. Identify packages more than 2 major versions behind
4. Flag any deprecated packages

If critical or high severity vulnerabilities are found:
- Open a GitHub issue titled "security: [package] CVE-XXXX"
- Include the CVE ID, affected version, and fixed version
- Tag it with "security" and "P1" labels

If packages are outdated but not vulnerable:
- Open a single PR that bumps non-breaking minor/patch versions
- Title: "chore: bump non-breaking dependency updates"

Do not bump major versions without explicit approval.
```

---

### 7. Stale Branch Cleanup

**Trigger:** Schedule, biweekly on Friday at 5pm
**Connectors:** GitHub

```
List all remote branches that:
1. Have not received a commit in 30+ days
2. Are not protected branches (main, develop, release/*)
3. Are not associated with an open PR

For each stale branch:
- Post a comment on the last commit asking if the branch is still needed
- If the branch has been inactive for 60+ days AND has no open PR,
  list it in a summary but do NOT delete it

Post the summary as a GitHub issue titled "housekeeping: stale branches review [date]"
with a table of branch name, last commit date, and author.
```

---

### 8. Daily Inbox Triage (Email)

**Trigger:** Schedule, daily at 7am
**Connectors:** Gmail, Slack

```
Fetch all unread emails received in the last 24 hours.

Classify each email into one of:
- URGENT: requires action today
- ACTION: requires action this week
- FYI: informational, no action needed
- NOISE: newsletters, promotions, automated notifications

Post a digest to #personal on Slack:
## Urgent (act today)
## Action required (this week)
## FYI
## Filtered out: [count] noise emails

For URGENT emails, include the sender, subject, and a one-line summary.
Do not reply to, forward, or delete any emails.
```

---

## `/loop` Patterns

### CI Monitor

```bash
/loop 5m check if the deployment finished and tell me what happened
```

### PR Babysitter

```bash
/loop check whether CI passed and address any review comments
```

### Build Watcher

```bash
/loop 3m check the build status — if it failed, diagnose and push a fix
```

### Custom `loop.md` (Project-Level)

Create `.claude/loop.md` to replace the built-in maintenance prompt:

```markdown
Check the `release/next` PR. If CI is red, pull the failing job log,
diagnose, and push a minimal fix. If new review comments have arrived,
address each one and resolve the thread. If everything is green and
quiet, say so in one line.
```

---

## Cron Expression Reference

| Expression | Meaning |
|-----------|---------|
| `*/5 * * * *` | Every 5 minutes |
| `0 * * * *` | Every hour on the hour |
| `0 9 * * *` | Daily at 9am local |
| `0 9 * * 1-5` | Weekdays at 9am local |
| `0 0 * * 0` | Weekly on Sunday at midnight |
| `0 9 1 * *` | First of each month at 9am |

Tip: avoid scheduling on `:00` or `:30` — the scheduler adds jitter to those times. Use odd minutes like `3 9 * * *` for precise timing.

---

## Prompt Design Best Practices

### The Goal-Output-Boundary Pattern

Every routine prompt should include three parts:

1. **Goal:** What to do and what data to read
2. **Output:** Exact format and where to deliver it
3. **Boundaries:** What NOT to do (prevents over-eager behavior)

```
# Goal
Scan PRs merged in the last 7 days for documentation drift.

# Output
Open a PR with suggested documentation updates.
Title format: "docs: update [area]"

# Boundaries
Do not modify source code. Do not merge anything. Do not
close issues. Only update documentation files.
```

### Self-Contained Prompts

Routines run in a clean cloud session with no conversation history. The prompt must include everything Claude needs:

- Repository context (which repo, which branch)
- Tool permissions (what connectors to use)
- Success criteria (how Claude knows it's done)
- Failure handling (what to do if something goes wrong)

### Testing Before Scheduling

Always run a routine manually first:

1. Click **Run now** on the routine detail page
2. Verify correct inputs were read
3. Check output went to the right place
4. Confirm no unintended side effects

---

## Trigger Combinations

A single routine can combine multiple triggers:

| Combo | Use Case |
|-------|----------|
| Schedule + GitHub | PR review runs nightly AND on each new PR |
| Schedule + API | Health check runs hourly AND after each deploy |
| GitHub + API | Code review on PR open AND from a deploy script |

---

## Common Pitfalls

| Pitfall | Fix |
|---------|-----|
| Prompt references "earlier in the conversation" | Routines have no history — make prompts self-contained |
| Routine pushes to protected branch | Default is `claude/`-prefixed branches only |
| Routine modifies too many things | Add explicit "do not" boundaries |
| Missing connector tools | Add connectors in the routine config, not just MCP |
| Network requests blocked | Check environment network access settings |
| One-shot fires at wrong time | Times are local — verify timezone conversion |

---

## Resources

- [Routines Documentation](https://code.claude.com/docs/en/routines)
- [Scheduled Tasks Guide](https://code.claude.com/docs/en/scheduled-tasks)
- [Desktop Scheduled Tasks](https://code.claude.com/docs/en/desktop-scheduled-tasks)
- [Cloud Environment Setup](https://code.claude.com/docs/en/claude-code-on-the-web#the-cloud-environment)
- [MCP Connectors](https://code.claude.com/docs/en/mcp)
- [GitHub Actions Integration](https://code.claude.com/docs/en/github-actions)
