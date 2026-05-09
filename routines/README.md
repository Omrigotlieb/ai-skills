# Claude Code Routines & Scheduled Automation

Production-ready routine prompts and scheduling patterns for Claude Code. Routines run autonomously on Anthropic's cloud infrastructure — they keep working when your laptop is closed.

> **Released:** April 2026 | **Docs:** [Official Routines Reference](https://code.claude.com/docs/en/routines) | Links last verified: 2026-05-09

## Quick Start

Create a routine from the CLI or the web:

```bash
# Conversational creation
/schedule

# One-liner
/schedule daily PR review at 9am

# One-off future task
/schedule tomorrow at 9am, summarize yesterday's merged PRs

# Manage existing routines
/schedule list
/schedule update
/schedule run
```

Or create at [claude.ai/code/routines](https://claude.ai/code/routines).

---

## Trigger Types

A single routine can combine multiple triggers.

| Trigger | Fires when | Example |
|---------|-----------|---------|
| **Schedule** | Recurring cadence (hourly, daily, weekly) or one-off timestamp | Nightly at 11pm, weekdays at 9am |
| **API** | HTTP POST to a per-routine endpoint | Deploy pipeline calls after push |
| **GitHub** | Repository events (PR opened, release published) | Every new pull request |

---

## Production Routine Prompts

### Daily Routines

#### 1. Morning Standup Brief

**Trigger:** Schedule — weekdays at 8:30am
**Connectors:** Slack

```
Read all open PRs and recent commits in the repository.
Post a Slack message to #standup with:
- What landed yesterday (merged PRs, key commits)
- What's in flight (open PRs with author and age)
- Anything blocked or stale (PRs older than 3 days with no review activity)

Keep the message under 10 lines. Use bullet points. Tag PR authors when something is stale.
```

---

#### 2. Issue Triage & Backlog Grooming

**Trigger:** Schedule — every weeknight at 10pm
**Connectors:** Slack or Linear

```
Read all GitHub issues opened since the last run of this routine.

For each new issue:
1. Analyze the title and body to determine the affected module
2. Apply appropriate labels (bug, feature, docs, security, performance)
3. Estimate priority (P0-P3) based on: severity keywords, affected components, reporter history
4. Assign to the team member who owns that code area based on CODEOWNERS

Post a triage summary to #engineering-triage in Slack:
- Count of new issues by label
- Any P0/P1 items that need immediate attention
- Issues that couldn't be auto-classified (need human review)
```

---

#### 3. Daily Security and Dependency Scan

**Trigger:** Schedule — weekdays at 7am
**Connectors:** Slack

```
Run the project's dependency audit command (npm audit / pip audit / cargo audit).

For each vulnerability found:
1. Check if it has a fix available
2. Assess whether the vulnerable code path is reachable in this project
3. If a fix exists and the update is non-breaking, create a PR with the fix

Post a summary to #security:
- Total vulnerabilities by severity (critical, high, medium, low)
- PRs created for auto-fixable issues
- Manual review needed for breaking changes

If no vulnerabilities found, post "All clear" with the date.
```

---

### Weekly Routines

#### 4. Documentation Drift Detection

**Trigger:** Schedule — Monday at 9am
**Connectors:** None required

```
Scan all PRs merged to main since last Monday.

For each merged PR:
1. Identify functions, APIs, or config that changed
2. Check if corresponding documentation references those same identifiers
3. Flag any docs file that references a function signature, endpoint, or config key that was modified but the doc was not updated

For each stale doc found:
- Open a PR against the docs with a proposed update
- Include a link to the PR that introduced the change
- Add the label "docs-drift"

If no drift detected, skip PR creation.
```

---

#### 5. Stale Branch Cleanup Report

**Trigger:** Schedule — Friday at 4pm
**Connectors:** Slack

```
List all remote branches that:
- Have not received a commit in the last 30 days
- Are not protected branches (main, develop, release/*)
- Are not currently associated with an open PR

Post a report to #engineering:
- Branch name, last commit date, and author
- Total count of stale branches
- Estimated repo size savings if cleaned up

Do NOT delete any branches. This is a report only.
```

---

#### 6. Weekly Test Health Report

**Trigger:** Schedule — Sunday at 8pm
**Connectors:** Slack

```
Run the full test suite and collect results.

Generate a health report:
1. Total tests: passed, failed, skipped
2. Test duration trend (compare with last week if a previous report exists in the repo)
3. Flaky tests: any test that passed on retry but failed initially
4. Coverage delta: files with decreased coverage compared to main

Post to #engineering with:
- Overall health score (green/yellow/red)
- Top 3 issues to address this week
- Link to full report if saved as an artifact
```

---

### Event-Driven Routines

#### 7. PR Code Review Bot

**Trigger:** GitHub — `pull_request.opened`
**Filter:** `is_draft` = false

```
A pull request was just opened on this repository. Review it carefully.

Check for:
1. Security: SQL injection, XSS, hardcoded secrets, unsafe deserialization
2. Performance: N+1 queries, unbounded loops, missing indexes, large allocations
3. Correctness: Off-by-one errors, null handling, race conditions, error propagation
4. Style: Naming conventions, file organization, consistency with existing patterns

Post a review comment on the PR with:
- One-line summary of what the PR changes
- Issues found, grouped by severity (blocking, warning, suggestion)
- A clear verdict: "Ready to merge", "Needs changes", or "Blocking issue"

If the PR is clean, say so briefly. Don't invent issues to seem thorough.
```

---

#### 8. Deploy Verification

**Trigger:** API — called by CD pipeline after production deploy
**Connectors:** Slack

```
A production deploy just completed. The deploy details are in the text field.

Verify the deploy:
1. Run smoke tests against the deployed endpoints (if test commands exist)
2. Check application logs for new errors in the last 5 minutes
3. Compare error rates before and after the deploy window
4. Verify that the deployed version matches the expected commit SHA

Post to #releases:
- GO: if all checks pass, with a summary of what shipped
- NO-GO: if any check fails, with specific failure details and rollback recommendation

Tag @oncall if NO-GO.
```

---

#### 9. Release Notes Generator

**Trigger:** GitHub — `release.published`

```
A new release was just published. Generate user-facing release notes.

Steps:
1. Collect all merged PRs between this release tag and the previous one
2. Categorize changes: Features, Bug Fixes, Performance, Breaking Changes, Dependencies
3. Write a concise description for each change in plain language (not commit messages)
4. Highlight breaking changes with migration instructions

Update the release body on GitHub with the generated notes.
Format with markdown headers and bullet points.
```

---

### Specialized Routines

#### 10. Competitor / Industry Monitor

**Trigger:** Schedule — weekdays at 8am
**Connectors:** Slack

```
Search for recent news, blog posts, and announcements related to:
- [Your product category]
- [Key competitors by name]
- [Relevant technology trends]

Summarize the top 5 most relevant items:
- Title and source
- One-sentence summary
- Relevance to our product/roadmap
- Suggested action (if any)

Post to #product-intel. Skip items older than 48 hours.
```

---

#### 11. On-Call Alert Triage

**Trigger:** API — called by monitoring system (PagerDuty, Datadog, Sentry)

```
An alert just fired. The alert body is in the text field.

Triage steps:
1. Parse the alert for service name, error type, and affected endpoints
2. Search recent commits (last 48 hours) for changes to the affected service
3. Check if this error pattern has appeared before in the repository's issue tracker
4. If a likely root cause commit is found, draft a revert PR

Post findings to #oncall:
- Alert summary
- Likely root cause (with confidence: high/medium/low)
- Recent commits that may be related
- Recommended action: revert, hotfix, or monitor
- Link to draft PR if created
```

---

#### 12. Library Port / SDK Sync

**Trigger:** GitHub — `pull_request.closed` (filtered to merged PRs)
**Repos:** Source SDK + Target SDK

```
A PR was just merged into the source SDK repository.

Port the change to the target SDK:
1. Analyze what the merged PR changed (API surface, behavior, tests)
2. Find the equivalent code in the target SDK repository
3. Implement the same change adapted to the target language's idioms
4. Port or create equivalent tests
5. Open a PR in the target SDK with:
   - Reference to the source PR
   - Description of what was ported and any adaptation decisions
   - Label: "auto-port"
```

---

## Writing Effective Routine Prompts

### The Prompt is Everything

Routines run autonomously with no human in the loop. The prompt must be **self-contained and explicit**.

| Do | Don't |
|----|-------|
| Specify exact output format | Say "summarize as appropriate" |
| Name the Slack channel or connector target | Say "post somewhere visible" |
| Define success criteria | Assume Claude knows what "done" means |
| List the steps in order | Give vague high-level goals |
| Set scope boundaries | Leave open-ended exploration |

### Prompt Structure Template

```
[CONTEXT] What just happened or what state to check
[STEPS] Numbered actions to take, in order
[OUTPUT] Exact format and destination for results
[EDGE CASES] What to do when things are ambiguous
[CONSTRAINTS] What NOT to do (don't delete, don't push to main, etc.)
```

### Security Considerations

- Routines execute under **your** GitHub identity — commits and PRs carry your name
- By default, Claude can only push to `claude/`-prefixed branches
- Remove connectors the routine doesn't need
- Be cautious with routines that process external input (support tickets, emails) — prompt injection risk
- Review routine outputs for the first few runs before trusting them fully

---

## Scheduling Best Practices

| Pattern | Cadence | Why |
|---------|---------|-----|
| Standup brief | Weekdays 8:30am | Ready before first meeting |
| Issue triage | Nightly 10pm | Clean backlog every morning |
| Security scan | Weekdays 7am | Start the day with a clean bill |
| Docs drift | Monday 9am | Catch weekend merges early |
| Stale branches | Friday 4pm | End-of-week cleanup |
| Test health | Sunday 8pm | Monday morning readiness |

### Usage Limits

| Plan | Daily routine runs |
|------|-------------------|
| Pro | 5 |
| Max | 15 |
| Team | 25 |
| Enterprise | 25 |

One-off scheduled runs do not count against the daily cap.

---

## Local Alternatives

Not everything needs cloud routines. For tasks tied to your machine:

| Method | Runs where | Best for |
|--------|-----------|----------|
| **Cloud routines** | Anthropic infrastructure | Unattended, scheduled, event-driven |
| **Desktop scheduled tasks** | Your machine (Desktop app) | Local file access, personal automation |
| **`/loop` in CLI** | Active CLI session | Polling, monitoring during a session |
| **Headless mode** | Your machine via cron | CI/CD integration, batch processing |

```bash
# Headless mode example (local cron)
claude -p "Review src/ for TODO comments and list them" --output-format json

# /loop for active monitoring
/loop 5m check if the build passed
```

---

## Starter Kit: Your First Week of Routines

**Day 1:** Set up the [Daily Standup Brief](#1-morning-standup-brief) — low risk, immediate value.

**Day 2:** Add [PR Code Review Bot](#7-pr-code-review-bot) — catches issues before human review.

**Day 3:** Enable [Documentation Drift Detection](#4-documentation-drift-detection) — prevents stale docs.

**Day 4:** Configure [Daily Security Scan](#3-daily-security-and-dependency-scan) — automated vulnerability monitoring.

**Day 5:** Add [Deploy Verification](#8-deploy-verification) — post-deploy confidence.

Review outputs from each routine before adding the next. Calibrate prompts based on results.

---

## Resources

### Official
- [Routines Documentation](https://code.claude.com/docs/en/routines)
- [Introducing Routines Blog](https://claude.com/blog/introducing-routines-in-claude-code)
- [Scheduled Tasks (local)](https://code.claude.com/docs/en/scheduled-tasks)
- [Desktop Scheduled Tasks](https://code.claude.com/docs/en/desktop-scheduled-tasks)

### Guides
- [Routines Practical Guide (Nimbalyst)](https://nimbalyst.com/blog/claude-code-routines-practical-guide/)
- [Routines Tutorial (AyyazTech)](https://www.ayyaztech.com/blog/claude-code-routines-tutorial)
- [8 Production Prompts (Substack)](https://linas.substack.com/p/claude-code-routines-guide)
- [5 Setups That Work While You Sleep (Medium)](https://alirezarezvani.medium.com/claude-code-routines-5-setups-that-work-while-you-sleep-ee779b5e6924)
- [Daily Briefing Across Tools](https://claude.com/resources/use-cases/build-a-daily-briefing-across-your-tools)

### Tools
- [claude-code-scheduler (GitHub)](https://github.com/jshchnz/claude-code-scheduler) — Local scheduling with natural language
- [claude-scheduler (GitHub)](https://github.com/gruckion/claude-scheduler) — Fire-and-forget with notifications
- [claude-mcp-scheduler (GitHub)](https://github.com/tonybentley/claude-mcp-scheduler) — Cron + MCP integration
- [awesome-claude-code-workflows (GitHub)](https://github.com/ithiria894/awesome-claude-code-workflows) — Workflow recipes

### Prompt Engineering for Agents
- [AI Agent Prompt Patterns (Paxrel)](https://paxrel.com/blog-ai-agent-prompts) — 10 patterns that work
- [Anthropic Best Practices](https://www.anthropic.com/engineering/claude-code-best-practices)
