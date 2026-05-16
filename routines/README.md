# Claude Code Routines & Scheduled Agent Prompts

Production-ready routines, scheduled tasks, and agent prompt templates for Claude Code automation. Routines run on Anthropic cloud infrastructure, so they keep working when your laptop is closed.

> Links last verified: 2026-05-16

---

## What Are Routines?

Routines (launched April 14, 2026 in research preview) let you define a prompt, point it at a GitHub repository, attach a trigger, and let Claude execute autonomously. Three trigger types:

| Trigger | How It Fires | Best For |
|---------|-------------|----------|
| **Schedule** | Cron-based (hourly, daily, weekdays, weekly) | Recurring maintenance, reports |
| **API** | HTTP POST to a per-routine endpoint | Deploy pipelines, alerts, on-demand |
| **GitHub** | Repository events (PR opened, release published) | Code review, backports, triage |

**Daily run limits** vary by plan. Check your current cap at [claude.ai/settings/usage](https://claude.ai/settings/usage). One-off runs are exempt from caps.

---

## Quick Start

### From the Web
1. Visit [claude.ai/code/routines](https://claude.ai/code/routines)
2. Click **New routine**
3. Write prompt, select repo, pick trigger
4. Click **Create**

### From the CLI
```bash
/schedule daily PR review at 9am
/schedule list
/schedule run
```

### From Desktop App
**Routines** in sidebar > **New routine** > **Remote**

---

## Compare Scheduling Options

| | Cloud Routines | Desktop Scheduled Tasks | `/loop` |
|---|---|---|---|
| Runs on | Anthropic cloud | Your machine | Your machine |
| Requires machine on | No | Yes | Yes |
| Requires open session | No | No | Yes |
| Persistent across restarts | Yes | Yes | Restored on `--resume` |
| Access to local files | No (fresh clone) | Yes | Yes |
| MCP servers | Connectors configured per task | Config files and connectors | Inherits from session |
| Permission prompts | No (runs autonomously) | Configurable per task | Inherits from session |
| Minimum interval | 1 hour | 1 minute | 1 minute |

---

## Production-Ready Routine Catalog

### Development Workflows

#### 1. Nightly Issue Triage
**Trigger:** Schedule (daily, 7am)
**Value:** Team starts the day with a groomed queue instead of raw inbox.

```
Read all GitHub issues opened in this repo in the last 24 hours.

For each issue:
1. Apply one label from: [bug, feature, docs, infra, perf, question, needs-triage]
2. Set a priority label from: [p0-critical, p1-high, p2-medium, p3-low]
3. Assign to the relevant owner based on which files or directories the issue references

Post a summary to the #dev-standup Slack channel with:
- Total new issues count
- Breakdown by label and priority
- Any p0/p1 items highlighted at the top

Execute these steps immediately.
```

---

#### 2. Automated PR Code Review
**Trigger:** GitHub event (pull_request.opened)
**Value:** Catches mechanical issues before human reviewers see the PR.

```
Review this pull request against the team's code review checklist.

Check for:
- Security: hardcoded secrets, unvalidated inputs, SQL injection, XSS, dependency CVEs
- Performance: N+1 queries, missing indexes, synchronous operations that should be async
- Code style: linting compliance, naming conventions, clarity
- Testing: new code paths without test coverage, missing edge cases
- Breaking changes: API contract changes, migration requirements

For each issue found:
1. Leave an inline comment on the specific line
2. Rate severity: [critical, warning, suggestion]
3. Include a concrete fix suggestion

Post a summary comment with:
- Overall assessment: [approve, request-changes, needs-discussion]
- Count of issues by severity
- One-sentence summary of the most important finding

Execute these steps immediately.
```

**Filter tip:** Set `is_draft = false` to skip draft PRs.

---

#### 3. Friday Changelog Generator
**Trigger:** Schedule (weekly, Friday 4pm)
**Value:** Ships a human-readable changelog without manual writing.

```
Read all pull requests merged to main this week.

Group them by type:
- Features: new user-facing functionality
- Fixes: bug fixes
- Infrastructure: CI/CD, tooling, dependency changes
- Docs: documentation updates

For each entry, write a plain-English one-liner (not the PR title verbatim).

Open a PR that appends this week's section to CHANGELOG.md using the format:
## [Unreleased] - YYYY-MM-DD
### Features
- Description (PR #number)
### Fixes
- Description (PR #number)

Execute these steps immediately.
```

---

#### 4. Documentation Drift Detection
**Trigger:** Schedule (weekly) or GitHub event (pull_request.closed, filtered to merged)
**Value:** Catches stale docs before users hit outdated information.

```
Scan all pull requests merged to main since the last run.

For each PR, check whether any documentation files (README.md, docs/,
wiki, API references) reference functions, APIs, configuration options,
or CLI flags that were modified in the PR.

If documentation is outdated relative to code changes:
1. Open a PR with suggested documentation updates
2. Tag the PR with "docs-drift"
3. Reference the original PR that caused the drift

Post a summary to #docs-channel with:
- Number of drift issues found
- Links to opened PRs

Execute these steps immediately.
```

---

#### 5. Dependency Health Report
**Trigger:** Schedule (weekly, Monday 8am)
**Value:** Stays ahead of security vulnerabilities and version lag.

```
Analyze the project's dependency files (package.json, requirements.txt,
go.mod, Cargo.toml, or equivalent).

For each dependency:
1. Check if a newer version is available
2. Categorize the upgrade: [patch, minor, major]
3. Flag any known security vulnerabilities (CVEs)

For patch and minor upgrades with no breaking changes:
- Run the test suite with the upgrade applied
- If tests pass, open a PR with the upgrade
- If tests fail, add to the report as "needs manual review"

Post a dependency health report to #engineering with:
- Security vulnerabilities requiring immediate attention
- Safe upgrades applied (with PR links)
- Major upgrades requiring manual review
- Overall health score (% of dependencies up-to-date)

Execute these steps immediately.
```

---

#### 6. Deploy Verification
**Trigger:** API (called from CD pipeline after each deploy)
**Value:** Automated smoke test and go/no-go decision.

```
A new deployment just completed. The deploy context is provided in the
trigger payload.

Run verification:
1. Check the health endpoint returns 200
2. Run the smoke test suite
3. Scan error logs from the last 10 minutes for new error patterns
4. Compare error rates to the pre-deploy baseline

If any check fails:
- Post a "NO-GO" alert to #releases with specific failures
- Open an issue with the failure details and recent commit references

If all checks pass:
- Post a "GO" confirmation to #releases with:
  - Deploy version/commit
  - Smoke test results
  - Error rate comparison

Execute these steps immediately.
```

---

#### 7. Stale Branch Sweeper
**Trigger:** Schedule (weekly)
**Value:** Keeps the repo clean without accidentally deleting active work.

```
List all branches in this repository.

Identify branches that meet ALL of these criteria:
- No commits in the last 30 days
- Not the default branch (main/master)
- Not referenced by any open pull request
- Not a release or production branch

For each stale branch, collect:
- Last commit date and author
- Whether it was ever part of a merged PR

Post a report to #engineering with:
- List of stale branches grouped by author
- Recommended action for each (safe to delete / check with author)
- Do NOT auto-delete any branches

Execute these steps immediately.
```

---

### Reporting & Intelligence

#### 8. Morning Engineering Brief
**Trigger:** Schedule (daily, 7am weekdays)
**Value:** Start the day informed without triaging multiple tools.

```
Prepare a morning engineering briefing covering the last 24 hours.

Gather:
1. GitHub: new issues, merged PRs, failed CI runs, open review requests
2. Slack (#incidents, #engineering): any overnight incidents or escalations
3. Open PRs waiting for review longer than 24 hours

Format as a concise briefing:

MORNING BRIEF - [date]

URGENT (action needed today):
- [items requiring immediate attention]

OVERNIGHT SUMMARY:
- PRs merged: [count] ([list key ones])
- New issues: [count] ([any p0/p1 highlighted])
- CI status: [green/red with details if red]

REVIEW QUEUE:
- [PRs waiting for review with age]

Post to #dev-standup.

Execute these steps immediately.
```

---

#### 9. Weekly User Sentiment Analysis
**Trigger:** Schedule (weekly, Monday 9am)
**Value:** Prioritize off real user pain, not the loudest ticket.

```
Analyze all support tickets and user feedback from the past 7 days.

Cluster feedback by:
1. Feature area / component
2. Sentiment (positive, neutral, negative, frustrated)
3. Frequency of similar reports

Produce a report with:

TOP 5 ISSUES BY VOLUME:
- [Issue]: [count] reports, [avg sentiment], [sample quote]

TRENDING (new this week):
- [Emerging patterns not seen in prior weeks]

POSITIVE SIGNALS:
- [Features getting praise]

RECOMMENDED PRIORITIES:
- Based on volume x severity, suggest top 3 engineering priorities

Post to #product-engineering.

Execute these steps immediately.
```

---

#### 10. Competitor Pricing Monitor
**Trigger:** Schedule (daily or weekly)
**Value:** Detect pricing changes before sales discovers them in a deal.
**Network access:** Requires "Full" or "Custom" (with competitor domains allowlisted) — the default "Trusted" environment blocks arbitrary domains.

```
Check the pricing pages for the following competitors:
- [Competitor A URL]
- [Competitor B URL]
- [Competitor C URL]

For each competitor, record:
- Plan names and prices
- Feature differences from last check
- Any new plans or discontinued plans

Compare against our stored baseline (in competitor-pricing.json
in this repo).

If ANY changes detected:
1. Update competitor-pricing.json with new data
2. Open a PR with the changes
3. Post an alert to #competitive-intel with:
   - What changed
   - Which competitor
   - Potential impact on our positioning

If no changes: post a brief "no changes detected" confirmation.

Execute these steps immediately.
```

---

### Operations & Incident Response

#### 11. Alert Triage Agent
**Trigger:** API (called from monitoring/alerting system)
**Value:** Reduces on-call triage time from minutes to seconds.

```
An alert has fired. The alert details are in the trigger payload.

Triage steps:
1. Parse the alert: extract service name, error type, and stack trace
2. Search recent commits (last 48 hours) for changes to affected files
3. Check if this error pattern has occurred before (search closed issues)
4. Correlate with any recent deployments

If a likely root cause is identified:
- Open a draft PR with a proposed fix
- Link the PR to the alert details
- Post to #incidents with: alert summary, likely cause, PR link

If root cause is unclear:
- Open an issue with gathered context
- Tag the on-call engineer
- Post to #incidents with: alert summary, investigation findings, issue link

Execute these steps immediately.
```

---

#### 12. Post-Incident Review Prep
**Trigger:** API or schedule (after incident resolution)
**Value:** Automates the tedious data gathering for postmortems.

```
Prepare a post-incident review document for the most recent incident.

Gather:
1. Timeline: commits, deploys, alerts, and Slack messages in #incidents
   from the last 48 hours
2. Impact: affected services, error rates, duration
3. Resolution: which commit/deploy fixed it

Generate a structured document:

## Incident Review - [date]

### Timeline
- [timestamp]: [event]

### Root Cause
[Analysis based on code changes and error patterns]

### Impact
- Duration: [time]
- Services affected: [list]
- User impact: [description]

### What Went Well
- [items]

### What Could Improve
- [items]

### Action Items
- [ ] [Specific follow-up task with suggested owner]

Open a PR adding this document to docs/incidents/.

Execute these steps immediately.
```

---

## Local Scheduled Tasks

For tasks that need local file access or run within an active session.

### loop.md Templates

Place in `.claude/loop.md` (project-level) or `~/.claude/loop.md` (user-level). The project-level file takes precedence when both exist. Content beyond 25,000 bytes is truncated. These templates omit the "Execute these steps immediately" closing used in cloud routines because `/loop` is interactive and does not need it.

#### Release Branch Guardian
```markdown
Check the `release/next` PR. If CI is red, pull the failing job log,
diagnose, and push a minimal fix. If new review comments have arrived,
address each one and resolve the thread. If everything is green and
quiet, say so in one line.
```

#### PR Babysitter
```markdown
Check all open PRs I authored. For each:
1. If CI failed, diagnose and push a fix
2. If review comments arrived, address them
3. If approved and CI green, report ready to merge
Summarize status of all PRs in one paragraph.
```

### In-Session Reminders

Use natural language directly in a session. Claude schedules a single-fire task:

```
remind me at 3pm to push the release branch
in 45 minutes, check whether the integration tests passed
```

### Cloud One-Off Runs

Use `/schedule` for one-off runs on Anthropic cloud (fires once, then auto-disables):

```bash
/schedule tomorrow at 9am, summarize yesterday's merged PRs
/schedule in 2 weeks, open a cleanup PR that removes the feature flag
```

---

## Prompt Engineering for Routines

Routines run without human approval, so the prompt carries the full cognitive load.

### The Five Rules

1. **Specify what "done" looks like.** A Slack message, a draft PR, a labeled issue. Not "review the code."
2. **Name which connectors to use.** "Post to #dev-standup via Slack" not "notify the team."
3. **Define the label/category taxonomy.** Provide the exact set of labels, not "appropriate labels."
4. **End with "Execute these steps immediately."** Prevents Claude from narrating instead of acting.
5. **Handle the empty case.** What should happen when there are no new issues, no failing tests, no drift?

### Anti-Patterns

| Anti-Pattern | Problem | Fix |
|---|---|---|
| "Check for issues" | Too vague, no defined output | Specify exact checks and output format |
| No output destination | Routine runs but nobody sees results | Always specify Slack channel, PR, or issue |
| Assuming repo structure | Fails on repos with different layouts | Reference specific file paths or use discovery |
| No error handling | Silent failure on edge cases | Define what to do when checks fail |
| "Use best judgment" | Unpredictable behavior across runs | Provide explicit decision criteria |

---

## GitHub Trigger Filters

Fine-tune which events fire your routine:

| Filter | Operator Options | Example |
|--------|-----------------|---------|
| Author | equals, contains | `author equals dependabot[bot]` |
| Title | contains, matches regex | `title matches .*hotfix.*` |
| Base branch | equals | `base_branch equals main` |
| Head branch | contains | `head_branch contains auth-provider` |
| Labels | is one of | `labels is one of [needs-review, ready]` |
| Is draft | equals | `is_draft equals false` |

**Regex tip:** `matches regex` tests the *entire* field value, not a substring. Use `.*hotfix.*` not `hotfix`.

---

## Connector Setup

Routines can use MCP connectors for external services:

| Connector | Common Use |
|-----------|-----------|
| **Slack** | Post summaries, alerts, reports to channels |
| **Linear** | Create/update issues, manage projects |
| **GitHub** | Clone repos, open PRs, manage issues (built-in) |
| **Google Calendar** | Read schedules for meeting prep routines |
| **Gmail** | Read/draft emails for digest routines |

Manage at [claude.ai/customize/connectors](https://claude.ai/customize/connectors).

---

## Resources

### Official
- [Routines Documentation](https://code.claude.com/docs/en/routines)
- [Scheduled Tasks (In-Session)](https://code.claude.com/docs/en/scheduled-tasks)
- [Desktop Scheduled Tasks](https://code.claude.com/docs/en/desktop-scheduled-tasks)
- [Introducing Routines Blog](https://claude.com/blog/introducing-routines-in-claude-code)

### Community
- [claude-routines-and-agents-pm-pack](https://github.com/aakashg/claude-routines-and-agents-pm-pack) - 9 production-ready prompts with sample outputs
- [awesome-claude-code-toolkit](https://github.com/rohitg00/awesome-claude-code-toolkit) - 135 agents, 35 skills, comprehensive toolkit
- [awesome-claude-code](https://github.com/hesreallyhim/awesome-claude-code) - Curated skills, hooks, and plugins
- [awesome-claude-code-subagents](https://github.com/VoltAgent/awesome-claude-code-subagents) - 100+ specialized subagents
- [claude-code-prompts](https://github.com/repowise-dev/claude-code-prompts) - Agent delegation and multi-agent coordination

### Guides
- [7 Routines That Save Hours](https://dev.to/muhammad_moeed/7-claude-code-routines-that-actually-save-me-hours-each-week-562l)
- [Routines Tutorial (Builder.io)](https://www.builder.io/blog/claude-code-routines)
- [Routines Guide (Better Stack)](https://betterstack.com/community/guides/ai/claude-code-routines/)
- [Production Workflows + MCP Setup](https://www.arcade.dev/blog/claude-code-routines-mcp-setup/)
