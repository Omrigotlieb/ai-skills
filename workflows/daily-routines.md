# Daily Routines and Scheduled Automation

Practical patterns for automating recurring development work with Claude Code. These routines run unattended on a schedule, via API triggers, or in response to GitHub events. For copy-ready prompt templates, see [Agent Routine Prompt Templates](../prompts/agent-routines.md).

> **As of April 2026**: Claude Code Routines are in research preview. Routines run on Anthropic's cloud infrastructure and survive machine shutdowns. Behavior, limits, and API surface may change.

## Quick Navigation

- [Morning Routines](#morning-routines)
- [Continuous Routines](#continuous-routines)
- [Evening and Nightly Routines](#evening-and-nightly-routines)
- [Weekly Routines](#weekly-routines)
- [Routine Prompt Best Practices](#routine-prompt-best-practices)
- [Setup Guide](#setup-guide)
- [Trigger Types](#trigger-types)

---

## A Developer's Daily Schedule

A recommended daily automation schedule combining scheduled routines, GitHub-triggered routines, and API-triggered routines.

| Time | Routine | Trigger | What It Does |
|------|---------|---------|-------------|
| 2:30 AM | Memory consolidation | Schedule | Processes logs, cleans stale branches, archives old sessions |
| 3:00 AM | Dependency audit | Schedule | Checks for outdated or vulnerable dependencies, opens PRs |
| 7:00 AM | Morning briefing | Schedule | Summarizes overnight activity, open PRs, failing CI, unresolved alerts |
| 9:00 AM | Backlog grooming | Schedule | Labels new issues, assigns owners, posts standup digest |
| On PR open | Code review | GitHub | Runs team checklist, leaves inline comments, flags security issues |
| On deploy | Deploy verification | API | Smoke tests, error log scan, go/no-go post to release channel |
| 5:00 PM | End-of-day digest | Schedule | Summarizes the day: merged PRs, open blockers, tomorrow priorities |
| Friday 4 PM | Docs drift check | Schedule (weekly) | Scans merged PRs, flags stale docs, opens update PRs |

---

## Morning Routines

### Morning Briefing (7:00 AM)

A digest that lands before you open your laptop.

**Prompt:**
```
Review all activity in this repository since 5 PM yesterday (local time).

Produce a morning briefing that includes:

1. **Merged PRs**: list each with a one-line summary
2. **Open PRs**: list each with author, age, and review status
3. **Failing CI**: list any workflows that failed overnight with the failing step
4. **New issues**: list issues opened since yesterday with labels
5. **Unresolved alerts**: check connected monitoring for any open incidents

Format as a clean markdown summary. Post to #dev-morning in Slack.

If there is no activity to report, post "All quiet overnight — nothing to review."
```

**Setup:** Schedule trigger, daily at 7:00 AM. Connect Slack and your monitoring tool.

---

### Backlog Grooming (9:00 AM weekdays)

Automates the busywork of issue triage so standup starts with a clean queue.

**Prompt:**
```
Read every issue opened in the last 24 hours in this repository.

For each issue:
1. Apply labels based on files referenced in the issue body (use CODEOWNERS for area mapping)
2. Assign an owner based on the code area
3. Set priority based on: P0 if "critical" or "production" appears, P1 if "bug", P2 otherwise

After processing all issues, post a markdown summary to #team-standup in Slack:
- **New issues triaged**: count and list
- **Assigned to each person**: grouped list
- **Issues needing manual triage**: any that couldn't be auto-assigned

If no new issues were opened since the last run, post "No new issues to triage today" and exit.
```

**Setup:** Schedule trigger, weekdays at 9:00 AM. Connect your issue tracker (Linear, GitHub Issues) and Slack.

---

## Continuous Routines

### Automated Code Review (on every PR)

Applies your team's review standards before a human reviewer looks at the PR.

**Prompt:**
```
Review this pull request against the following checklist:

**Security**
- [ ] No hardcoded secrets, tokens, or credentials
- [ ] No SQL injection, XSS, or command injection vectors
- [ ] Input validation on all user-facing endpoints

**Quality**
- [ ] Tests added for new functionality
- [ ] No unhandled error paths
- [ ] No console.log or debug statements left in

**Performance**
- [ ] No N+1 query patterns
- [ ] No unnecessary blocking operations
- [ ] Large data sets are paginated

**Style**
- [ ] Follows existing code patterns in the module
- [ ] No commented-out code blocks
- [ ] Naming conventions match the codebase

For each issue found:
1. Leave an inline comment at the exact location with severity (Critical / Warning / Suggestion)
2. Explain the issue and suggest a fix

After reviewing all files, add a summary comment:
- Total issues found by severity
- Overall assessment: "Approve", "Request Changes", or "Needs Discussion"
- If no issues: "LGTM — ready to merge"

Never approve PRs with Critical issues. Draft PRs should be skipped.
```

**Setup:** GitHub trigger on `pull_request.opened`, filter `is_draft = false`.

---

### Alert Triage (on monitoring alert)

Turns raw alerts into actionable draft PRs.

**Prompt:**
```
An alert has been triggered. The alert details are provided as context.

Investigation steps:
1. Parse the stack trace and identify the failing code path
2. Run git log to find commits touching the affected files in the last 48 hours
3. Identify the most likely root cause commit
4. Read the affected code and understand the failure

If a fix is identifiable:
- Create a branch named claude/fix-{alert-id}
- Implement the fix with a test that reproduces the failure
- Open a draft PR linking back to the alert
- Post to #on-call in Slack: "Draft fix for [alert]: [PR link]"

If the cause is unclear:
- Post to #on-call in Slack: "Alert [alert] triaged — likely related to [commit]. Needs manual investigation."
- Include the narrowed-down file paths and the analysis

Never push directly to main. Always use draft PRs.
```

**Setup:** API trigger. Wire your monitoring tool (Datadog, Sentry, PagerDuty) to POST to the routine's endpoint with the alert body in the `text` field.

---

### Deploy Verification (post-deploy)

Automated smoke check after every production deployment.

**Prompt:**
```
A production deployment just completed. Run verification:

1. **Smoke tests**: Run the smoke test suite against the production URL
2. **Error scan**: Check error logs from the last 10 minutes for new error patterns
3. **Metric comparison**: Compare error rate and p99 latency to the 1-hour pre-deploy baseline

Assessment criteria:
- GO: No new errors, metrics within 10% of baseline, all smoke tests pass
- WATCH: Minor metric degradation (10-25%) but no new errors — monitor for 30 minutes
- NO-GO: New errors detected, smoke test failures, or metrics degraded more than 25%

Post the assessment to #releases in Slack with:
- Deploy status: GO / WATCH / NO-GO
- Summary of findings
- If NO-GO: specific errors and recommended rollback steps

Do not trigger rollbacks automatically. Post the recommendation and let a human decide.
```

**Setup:** API trigger. Call from your CD pipeline after deploy completes.

---

## Evening and Nightly Routines

### End-of-Day Digest (5:00 PM)

Summarizes the day and sets up tomorrow.

**Prompt:**
```
Compile a daily development digest for this repository:

1. **Merged today**: list all PRs merged since 9 AM with one-line summaries
2. **Still open**: list PRs still awaiting review, sorted by age (oldest first)
3. **Blockers**: list any issues labeled "blocked" or "needs-decision"
4. **CI status**: current state of main branch CI — passing or failing
5. **Tomorrow's priorities**: based on issue priority labels, list the top 3 items

Format as a clean markdown digest. Post to #dev-daily in Slack.
```

---

### Nightly Dependency Audit (3:00 AM)

Catches vulnerable or outdated dependencies before they become a problem.

**Prompt:**
```
Audit dependencies in this repository for security and freshness:

1. Run the appropriate security audit command (npm audit, pip audit, cargo audit, etc.)
2. Check for outdated dependencies (npm outdated, pip list --outdated, etc.)

For vulnerabilities:
- If Critical or High severity: create a branch claude/security-{date}, update the affected package, run tests, and open a PR titled "Security: update {package} to fix {CVE}"
- If Medium or Low: log them but don't create PRs

For outdated dependencies:
- If a minor/patch update is available and tests pass: create a branch claude/deps-{date}, update the package, and open a PR
- Never auto-upgrade major versions — log them for manual review

After the audit, post a summary to #dev-ops in Slack:
- Vulnerabilities found and PRs created
- Outdated packages (major versions needing manual review)
- If everything is current: "All dependencies up to date, no vulnerabilities found"

Run tests after every dependency change. If tests fail, revert the change and note it in the summary.
```

---

### Branch Cleanup (2:30 AM)

Keeps the repo tidy by archiving stale branches.

**Prompt:**
```
Clean up stale branches in this repository:

1. List all remote branches except main, master, develop, and release/*
2. For each branch, check:
   - Last commit date
   - Whether it has an associated open PR
   - Whether it has been merged to main

Actions:
- Branches merged to main with no open PR: delete the remote branch
- Branches with no commits in 30+ days and no open PR: delete the remote branch
- Branches with open PRs: skip entirely

After cleanup, post to #dev-ops:
- Branches deleted (with last commit dates)
- Branches skipped (with reasons)
- If nothing to clean: "All branches are active"

Never delete branches with open PRs. Never delete protected branches.
```

---

## Weekly Routines

### Documentation Drift Check (Friday 4:00 PM)

Keeps docs synchronized with code changes.

**Prompt:**
```
Scan all PRs merged to main since last Friday:

1. For each merged PR, identify if it changed:
   - Public API endpoints or function signatures
   - Configuration options or environment variables
   - Database schema or migration files
   - CLI commands or flags

2. For each change found, check if the corresponding documentation is updated:
   - README.md sections
   - API documentation
   - Configuration guides
   - Migration guides

3. For each documentation gap:
   - Create a branch claude/docs-update-{date}
   - Write the documentation update
   - Open a PR titled "Docs: update {section} for {change}"

Post a summary to #dev-docs:
- PRs scanned: count
- Documentation gaps found: count and list
- Update PRs created: list with links
- If everything is current: "All documentation is in sync with code changes"
```

---

### Weekly Security Review (Sunday 2:00 AM)

A deeper security pass that runs weekly.

**Prompt:**
```
Perform a weekly security review of this repository:

1. **Dependency scan**: Full audit of all dependencies for known vulnerabilities
2. **Secret scan**: Search the codebase for accidentally committed secrets, API keys, or tokens
3. **Permission review**: Check file permissions for anything world-readable that shouldn't be
4. **OWASP check**: Scan for common web vulnerabilities in any HTTP-handling code:
   - SQL injection
   - XSS
   - CSRF
   - Insecure deserialization
   - Broken authentication patterns

For each finding:
- Severity: Critical / High / Medium / Low
- Location: file:line
- Description: what the issue is
- Recommendation: how to fix it

If Critical issues found: open a PR with the fix and post to #security
If High issues found: open an issue and post to #security
Medium/Low: include in the weekly report only

Post the full report to #security-weekly in Slack.
```

---

## Routine Prompt Best Practices

### The Four Rules

1. **One routine, one job.** A routine that reviews PRs should not also update dependencies. Split them.

2. **Explicit success criteria.** Bad: "review PRs." Good: "review open PRs against the /auth module, check for SQL injection vulnerabilities and missing input validation, leave inline comments with severity labels."

3. **Define boundaries.** Always specify what the routine is NOT allowed to do: "Create draft PRs only. Never merge. Never push to main."

4. **Handle the empty case.** Specify what to do when there's nothing to process: "If no new issues were opened since the last run, post a 'nothing to triage' message to #dev-standup and exit."

### Prompt Structure Template

```
[What to do — specific, measurable action]

[Step-by-step process with numbered steps]

[Success criteria — what "done" looks like]

[Boundaries — what NOT to do]

[Output — where to post results and in what format]

[Empty case — what to do when there's nothing to process]
```

### Common Mistakes

| Mistake | Why It Fails | Fix |
|---------|-------------|-----|
| Vague prompt | "Check the repo" gives inconsistent results | List specific checks with pass/fail criteria |
| No output destination | Results are lost in a session log | Always specify Slack channel, PR, or issue |
| No boundary setting | Routine might merge, push to main, or delete branches | Explicitly forbid destructive actions |
| Ignoring empty state | Routine errors or produces confusing output when idle | Add an "if nothing to do" clause |
| Too broad scope | Single routine doing 5 different jobs | Split into focused routines |

---

## Setup Guide

### Creating a Routine

**Web (recommended for first-time setup):**
1. Go to [claude.ai/code/routines](https://claude.ai/code/routines)
2. Click **New routine**
3. Name it, write the prompt, select repos, pick a trigger
4. Review connectors (Slack, Linear, etc.) and remove ones not needed
5. Click **Create**

**CLI:**
```bash
# Create a scheduled routine
/schedule daily PR review at 9am

# List routines
/schedule list

# Update a routine
/schedule update

# Run immediately
/schedule run
```

**Desktop app:**
Schedule page > New task > New remote task

### Requirements

- Paid Claude subscription (Pro, Max, Team, or Enterprise)
- Claude Code on the web enabled
- GitHub connected (for repo access)
- Relevant connectors configured (Slack, Linear, etc.)

### Usage Limits

As of April 2026 (check the link below for current limits):

| Plan | Daily Routine Runs |
|------|-------------------|
| Pro | 5 |
| Max | 15 |
| Team | 25 |
| Enterprise | 25 |

Check current usage at [claude.ai/settings/usage](https://claude.ai/settings/usage).

---

## Trigger Types

### Schedule Triggers

Run on a recurring cadence. Presets: hourly, daily, weekdays, weekly. Custom cron expressions available via `/schedule update` (minimum interval: 1 hour).

Best time slots for overnight routines: 2:00-4:00 AM local time. This avoids peak usage and gives maximum distance from evening and morning activity.

### API Triggers

Each routine gets a dedicated HTTP endpoint with bearer token authentication. Wire monitoring, deploy pipelines, or internal tools to POST to the endpoint.

```bash
curl -X POST https://api.anthropic.com/v1/claude_code/routines/{routine_id}/fire \
  -H "Authorization: Bearer {token}" \
  -H "anthropic-beta: experimental-cc-routine-2026-04-01" \
  -H "anthropic-version: 2023-06-01" \
  -H "Content-Type: application/json" \
  -d '{"text": "Deploy completed for v2.3.1"}'
```

### GitHub Triggers

React to repository events: PR opened, PR merged, release published, etc. Filter by author, branch, labels, draft status, and more.

Example filter combinations:
- **Auth module review**: base branch `main`, head branch contains `auth-provider`
- **Ready-for-review only**: is draft is `false`
- **Label-gated**: labels include `needs-review`
- **External contributors**: fork is `true`

---

## Starter Kit: Your First Three Routines

If you're new to routines, start with these three and expand from there:

### 1. Daily PR Summary (lowest risk, highest visibility)

**Schedule:** Daily at 9:00 AM
**Prompt:** Review all open PRs. For each: one-line summary, age, review status, any failing checks. Post to #dev-morning in Slack.

### 2. Nightly Dependency Check (low risk, high value)

**Schedule:** Daily at 3:00 AM
**Prompt:** Run security audit on all dependencies. For critical/high vulns, open a PR with the fix. Post summary to #dev-ops.

### 3. PR Review Bot (medium risk, high value)

**Trigger:** GitHub `pull_request.opened`, filter `is_draft = false`
**Prompt:** Apply the team review checklist (security, tests, style). Leave inline comments. Add summary comment.

---

## Resources

- [Official Routines Documentation](https://code.claude.com/docs/en/routines)
- [Scheduled Tasks (local)](https://code.claude.com/docs/en/scheduled-tasks)
- [Desktop Scheduled Tasks](https://code.claude.com/docs/en/desktop-scheduled-tasks)
- [MCP Connectors](https://code.claude.com/docs/en/mcp)
- [claude-code-scheduler](https://github.com/jshchnz/claude-code-scheduler)
- [claude-code-workflows](https://github.com/shinpr/claude-code-workflows)
