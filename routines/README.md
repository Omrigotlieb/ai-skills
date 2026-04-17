# Claude Code Routines & Scheduled Tasks

Automate your daily developer workflow with Claude Code's three scheduling tiers. This guide covers practical routine templates, daily schedule patterns, and prompt-writing best practices drawn from official docs, community patterns, and real-world usage.

> **Latest Update:** April 2026 - Added routines guide with 10 routine templates, 3 loop.md templates, and event-driven examples

## Quick Navigation

- [Scheduling Options](#scheduling-options)
- [Daily Schedule Patterns](#daily-schedule-patterns)
- [Routine Templates](#routine-templates)
- [Prompt Writing Best Practices](#prompt-writing-best-practices)
- [Setup Guide](#setup-guide)
- [loop.md Templates](#loopmd-templates)

---

## Scheduling Options

Claude Code offers three ways to schedule recurring work, each with different trade-offs:

| | Cloud Routines | Desktop Scheduled Tasks | `/loop` (In-Session) |
|---|---|---|---|
| **Runs on** | Anthropic cloud | Your machine | Your machine |
| **Requires machine on** | No | Yes | Yes |
| **Requires open session** | No | No | Yes |
| **Persistent** | Yes | Yes | Session-scoped (7-day expiry) |
| **Local file access** | No (fresh clone) | Yes | Yes |
| **MCP servers** | Connectors per task | Config files + connectors | Inherits from session |
| **Min interval** | 1 hour | 1 minute | 1 minute |
| **Daily limits** | Pro: 5, Max: 15, Team: 25 | Unlimited | Unlimited |

### When to Use What

- **Cloud Routines**: Work that must run reliably without your machine (daily digests, PR reviews, backlog triage)
- **Desktop Scheduled Tasks**: Work that needs local files, tools, or MCP servers (local builds, file watchers, project-specific automation)
- **`/loop`**: Quick polling during a session (deployment monitoring, CI babysitting, build checks)

---

## Daily Schedule Patterns

### The Developer Daily (Recommended Starting Point)

A battle-tested daily schedule combining the highest-value automations. Most routines require **GitHub** and **Slack** connectors; see the [MCP Servers guide](../mcp-servers/README.md) for setup.

| Time | Routine | Type | Purpose |
|---|---|---|---|
| **7:00 AM** | Morning Briefing | Cloud/Desktop | Summarize overnight activity: PRs merged, issues opened, CI failures, Slack threads |
| **9:00 AM** | Standup Prep | Cloud | Generate standup notes from git activity and issue tracker |
| **12:00 PM** | PR Review Digest | Cloud | Review open PRs, flag stale ones, summarize review status |
| **3:00 PM** | Dependency Check | Desktop | Scan for security advisories and outdated packages |
| **6:00 PM** | End-of-Day Summary | Cloud | Compile daily progress, update project docs, draft tomorrow's priorities |
| **10:00 PM** | Nightly Maintenance | Cloud | Run backlog triage, detect docs drift, clean up stale branches |

### The Team Lead Daily

Optimized for engineering managers and tech leads:

| Time | Routine | Type | Purpose |
|---|---|---|---|
| **7:30 AM** | Team Activity Digest | Cloud | PR velocity, blocker summary, review bottlenecks across team repos |
| **9:00 AM** | Sprint Health Check | Cloud | Track sprint burndown, flag at-risk items, generate standup agenda |
| **2:00 PM** | Code Quality Pulse | Cloud | Run linting/type-check across repos, track tech debt trends |
| **5:00 PM** | Weekly Prep (Fri) | Cloud | Compile weekly metrics, draft retro notes, plan next sprint highlights |

### The Open Source Maintainer

For managing community-driven projects:

| Time | Routine | Type | Purpose |
|---|---|---|---|
| **8:00 AM** | Triage New Issues | Cloud | Label, assign, and respond to overnight issues |
| **10:00 AM** | Community PR Review | Cloud | Review fork-based PRs with security focus, leave actionable feedback |
| **4:00 PM** | Release Readiness | Cloud | Check changelog completeness, test matrix status, version bumps |

---

## Routine Templates

Ready-to-use prompt templates organized by category. Each template is designed for autonomous execution.

### Morning Briefing

**Trigger:** Schedule - Daily at 7:00 AM
**Connectors:** GitHub, Slack

```
Compile a morning briefing for the team. Check:

1. PRs merged since yesterday 5pm: list each with title, author, and one-line summary
2. PRs awaiting review for >24 hours: flag with reviewer names
3. CI failures on main branch: include job name and failing step
4. New issues opened overnight: group by label (bug, feature, question)

Format as a Slack message with sections. Post to #dev-standup.
If nothing noteworthy happened, post "All clear overnight" and exit.
```

[Full template](templates/morning-briefing.md)

### Standup Prep

**Trigger:** Schedule - Weekdays at 9:00 AM
**Connectors:** GitHub, Linear/Jira

```
Generate my standup notes for today.

Yesterday:
- List my merged PRs with one-line descriptions
- List issues I commented on or closed
- Note any PR reviews I completed

Today:
- List my open PRs and their status (needs review, changes requested, approved)
- List issues assigned to me sorted by priority
- Flag any blockers (failed CI, pending reviews >48h, dependency issues)

Blockers:
- Check if any of my PRs have failing CI
- Check if any assigned issues are blocked by other issues

Format as bullet points, keep it under 15 lines. Post to #standup or print to console.
```

[Full template](templates/standup-prep.md)

### PR Review Automation

**Trigger:** GitHub - `pull_request.opened` (or Schedule - Daily at noon)
**Connectors:** GitHub

```
Review this pull request thoroughly. Apply the following checklist:

Security:
- Check for SQL injection, XSS, command injection, and path traversal
- Verify authentication/authorization on new endpoints
- Flag hardcoded secrets or credentials
- Check for proper input validation at system boundaries

Performance:
- Flag N+1 queries or missing database indexes
- Check for unbounded loops or memory allocations
- Identify missing pagination on list endpoints

Code Quality:
- Verify error handling covers failure modes
- Check test coverage for new code paths
- Flag dead code or unused imports
- Verify naming consistency with existing codebase

Leave inline comments with severity labels: [critical], [warning], [suggestion].
Add a summary comment with pass/fail status and a one-paragraph assessment.
Create draft PRs only. Never merge. Never push to main.
```

[Full template](templates/pr-review.md)

### Backlog Triage

**Trigger:** Schedule - Weeknights at 10:00 PM
**Connectors:** GitHub, Slack

```
Triage issues opened today in this repository.

For each new issue:
1. Apply labels based on content: bug, feature, documentation, question, good-first-issue
2. Assign to the team member who owns that area of code (check CODEOWNERS or recent git blame)
3. Add priority label: P0 (broken for users), P1 (important), P2 (nice to have)
4. If it's a bug, check if a related PR already exists

After processing all issues:
- Post a summary to #triage with counts by label and priority
- Flag any P0 issues that need immediate attention

If no new issues exist, post "No new issues today" and exit.
```

[Full template](templates/backlog-triage.md)

### Dependency & Security Audit

**Trigger:** Schedule - Daily at 3:00 PM (or Weekly)
**Connectors:** GitHub

```
Run a dependency health check on this repository.

1. Check for known security vulnerabilities:
   - Run the package manager's audit command (npm audit, pip-audit, cargo audit, etc.)
   - Flag any critical or high severity issues with CVE links

2. Check for outdated dependencies:
   - List packages more than 2 major versions behind
   - Note any dependencies with deprecation warnings

3. License compliance:
   - Flag any new dependencies with copyleft licenses (GPL, AGPL)
   - Note any dependencies without a license

If critical vulnerabilities are found:
- Open a draft PR with the fix if it's a simple version bump
- Otherwise, create an issue with remediation steps

Post results summary to #security or print to console.
```

[Full template](templates/dependency-audit.md)

### Deploy Verification

**Trigger:** API (called from CD pipeline)
**Connectors:** GitHub, Slack

```
A production deployment just completed. Verify it succeeded.

The deployment context is provided in the API trigger payload.

1. Health checks:
   - Verify the application responds on its health endpoint
   - Check that the version endpoint reports the expected version

2. Error monitoring:
   - Check error logs for the last 15 minutes for new error patterns
   - Compare error rate to pre-deploy baseline

3. Smoke tests:
   - Run the critical path smoke test suite
   - Verify key API endpoints return expected status codes

Post results to #deploys:
- GREEN: "Deploy verified. No regressions detected."
- YELLOW: "Deploy warning: [specific concern]. Monitoring."
- RED: "Deploy issue detected: [details]. Consider rollback."

If RED, also post to #oncall with the specific failure details.
```

[Full template](templates/deploy-verification.md)

### Docs Drift Detection

**Trigger:** Schedule - Weekly (Mondays at 8:00 AM)
**Connectors:** GitHub

```
Scan for documentation that has drifted from the code.

1. Find all PRs merged in the last 7 days that changed:
   - API endpoints or route definitions
   - Configuration options or environment variables
   - Public function signatures or class interfaces
   - Database schema or migration files

2. For each changed area, check if corresponding documentation exists and is up to date:
   - README.md sections referencing changed code
   - API documentation (OpenAPI specs, doc comments)
   - Configuration guides
   - Architecture decision records (ADRs)

3. For each drift found:
   - Open a documentation update PR with the suggested change
   - Reference the original PR that caused the drift

If no drift is detected, report "Documentation is in sync" and exit.
```

[Full template](templates/docs-drift.md)

### End-of-Day Summary

**Trigger:** Schedule - Weekdays at 6:00 PM
**Connectors:** GitHub, Slack

```
Compile my end-of-day development summary.

Activity:
- List all commits I pushed today with one-line messages
- List PRs I opened, reviewed, or merged
- List issues I closed or commented on

Progress:
- Summarize what was accomplished in 2-3 sentences
- Note any items that took longer than expected and why

Tomorrow:
- List my open PRs that need attention (failing CI, review comments)
- List highest-priority assigned issues for tomorrow
- Flag any upcoming deadlines within 3 days

Format as a clean summary. Keep it under 20 lines.
If this is Friday, also include a weekly highlights section.
```

[Full template](templates/end-of-day.md)

### Alert Triage

**Trigger:** API (called from monitoring/alerting system)
**Connectors:** GitHub, Slack

```
An alert has fired. The alert payload is included in the trigger text.

Triage steps:
1. Parse the alert to identify: service name, error type, affected endpoint, and severity
2. Search recent commits (last 48 hours) for changes to the affected service
3. If a recent commit correlates with the error:
   - Identify the specific change that likely caused it
   - Draft a revert or fix PR
   - Post to #oncall: "Alert [name] likely caused by [commit]. Draft fix: [PR link]"
4. If no recent commit correlates:
   - Check if this is a known/recurring alert pattern
   - Post to #oncall: "Alert [name] - no recent code change found. Likely infrastructure or external dependency."

Never merge fix PRs automatically. Always create as draft for human review.
```

[Full template](templates/alert-triage.md)

### Stale Branch Cleanup

**Trigger:** Schedule - Weekly (Sundays at 11:00 PM)
**Connectors:** GitHub

```
Clean up stale branches in this repository.

1. List all remote branches not updated in the last 30 days
2. Exclude: main, master, develop, release/*, and any branch with an open PR
3. For branches with no open PR and no activity in 30+ days:
   - Check if the branch was merged (if so, safe to delete)
   - If merged: delete the remote branch
   - If not merged: create an issue tagging the branch author asking if it's still needed

4. Report:
   - Branches deleted (merged and stale)
   - Branches flagged for author review
   - Protected branches skipped

Post summary to #dev-ops or print to console.
```

[Full template](templates/stale-branch-cleanup.md)

---

## Prompt Writing Best Practices

Writing effective routine prompts requires a different mindset than interactive prompts. Routines run autonomously without human approval, so clarity and safety boundaries are critical.

### The SCORE Framework

Structure every routine prompt with these five elements:

| Element | Purpose | Example |
|---|---|---|
| **S**cope | What to examine or act on | "Review open PRs against the /auth module" |
| **C**riteria | Success/failure conditions | "Flag SQL injection, missing validation, hardcoded secrets" |
| **O**utput | Where and how to report | "Post to #security-reviews with severity labels" |
| **R**estrictions | Safety boundaries | "Create draft PRs only. Never merge. Never push to main" |
| **E**dge cases | What to do when nothing matches | "If no new issues exist, post status and exit" |

### Do's and Don'ts

**Do:**
- Be explicit about success criteria ("flag PRs older than 48 hours" not "flag old PRs")
- Specify output destinations (Slack channel, PR comment, console)
- Include edge case handling ("if no results, post status and exit")
- Set clear safety boundaries ("never merge", "draft PRs only")
- Use action verbs ("scan", "flag", "post", "open") not vague language ("look at", "check out")

**Don't:**
- Leave outputs ambiguous ("report the results" - where?)
- Assume human intervention ("ask the team" - no one is watching)
- Use relative time without anchoring ("check recent PRs" - how recent?)
- Skip the empty-result case (routines that find nothing should still report)
- Combine too many unrelated tasks (split into separate routines)

### Prompt Length Guidelines

| Routine Complexity | Recommended Length | Example |
|---|---|---|
| Simple check | 5-10 lines | Health check, single metric |
| Standard workflow | 15-30 lines | PR review, issue triage |
| Complex pipeline | 30-50 lines | Multi-step deploy verification |

Keep prompts under 50 lines. If you need more, the routine should probably be split.

---

## Setup Guide

### Cloud Routines (Recommended for Teams)

```bash
# Create from CLI
/schedule daily morning briefing at 7am

# List all routines
/schedule list

# Trigger manually
/schedule run <routine-name>

# Update
/schedule update <routine-name>
```

Or create at [claude.ai/code/routines](https://claude.ai/code/routines) with full trigger configuration (schedule, API, GitHub webhooks).

### Desktop Scheduled Tasks

Desktop tasks run locally on your machine with full access to local files, MCP servers, and tools configured in your project.

**Setup:**
1. Open the Claude Code desktop app
2. Go to the **Schedule** page
3. Click **New Task** > **New Local Task**
4. Configure the task name, prompt, interval, and permission mode
5. Tasks persist across app restarts and run even when no session is open

Desktop tasks are ideal for routines that need local file access (running tests, scanning local repos, interacting with local databases) or that use MCP servers not available as cloud connectors.

See the [official Desktop Scheduled Tasks docs](https://code.claude.com/docs/en/desktop-scheduled-tasks) for the full configuration guide.

### `/loop` for In-Session Polling

```bash
# Fixed interval with prompt
/loop 5m check if the deployment finished

# Claude chooses interval dynamically
/loop check whether CI passed and address any review comments

# Run a command on repeat
/loop 20m /review-pr 1234

# Built-in maintenance (continues unfinished work, tends to PRs)
/loop
```

### Custom `loop.md` for Default Behavior

Create `.claude/loop.md` in your project to customize what bare `/loop` does:

```markdown
Check the current branch's PR:
1. If CI is red, pull the failing job log, diagnose, and push a fix
2. If new review comments arrived, address each one and resolve the thread
3. If everything is green and quiet, say so in one line
```

---

## loop.md Templates

### The PR Babysitter

```markdown
# .claude/loop.md - PR Babysitter

Check the current branch's pull request.

If CI is failing:
- Pull the failing job log
- Diagnose the root cause
- Push a minimal fix targeting only the failure

If new review comments exist:
- Address each comment with a code change or explanation
- Resolve the thread after addressing

If merge conflicts exist:
- Rebase on the target branch and resolve conflicts
- Push the resolved branch

If everything is green with no pending comments:
- Report "PR is healthy" in one line
```

### The Build Guardian

```markdown
# .claude/loop.md - Build Guardian

Monitor the health of the main branch.

If the latest CI run on main failed:
- Identify the failing step and pull its log
- Check which commit introduced the failure
- If it's a simple fix (typo, missing import, config issue), push a fix to a new branch and open a PR
- If it's complex, create an issue with diagnosis and tag the commit author

If all CI is green:
- Report "main is healthy" in one line
```

### The Release Watcher

```markdown
# .claude/loop.md - Release Watcher

Monitor the release branch for readiness.

Check:
1. All required checks are passing
2. No unresolved review comments on the release PR
3. CHANGELOG.md is updated with all merged PRs since last release
4. Version numbers are bumped consistently across package files

If any check fails, report what needs attention.
If all checks pass, report "Release branch is ready for merge."
```

---

## Event-Driven Routines (GitHub Triggers)

Beyond schedules, routines can react to repository events:

### On PR Opened
```
Trigger: pull_request.opened
Filter: base branch = main, is draft = false

Run the team's code review checklist. Leave inline comments
for security, performance, and style issues. Add a summary
comment with pass/fail status.
```

### On PR Merged to Main
```
Trigger: pull_request.closed (merged = true)
Filter: base branch = main

Check if the merged PR changes any public API surface.
If so, verify that API documentation is updated.
If documentation is stale, open an update PR against docs/.
```

### On Release Published
```
Trigger: release.published

Verify the release:
1. Check that the release tag matches package version
2. Verify CHANGELOG has an entry for this version
3. Run smoke tests against the published package
4. Post release announcement to #releases with highlights
```

### On Issue Labeled "urgent"
```
Trigger: issues.labeled
Filter: label = urgent

When an issue is labeled urgent:
1. Check if it's reproducible from the description
2. Search for related code and recent changes
3. Draft a fix if the issue is clear-cut
4. Post to #urgent with triage summary and estimated complexity
```

---

## Combining Routines into a System

The real power of routines comes from combining them into a coherent automation system:

```
Morning (7 AM)          Afternoon (3 PM)         Evening (10 PM)
+------------------+    +------------------+    +------------------+
| Morning Briefing |    | Dependency Audit |    | Backlog Triage   |
| Standup Prep     |    | PR Review Digest |    | Stale Branches   |
+------------------+    +------------------+    | Docs Drift       |
                                                 +------------------+

Event-Driven (Always On)
+-------------------+  +------------------+  +-------------------+
| PR Review on Open |  | Deploy Verify    |  | Alert Triage      |
| (GitHub trigger)  |  | (API trigger)    |  | (API trigger)     |
+-------------------+  +------------------+  +-------------------+
```

Start with 2-3 routines and expand as you validate their value. The Morning Briefing and PR Review are the highest-impact starting points for most teams.

---

## Resources

- [Official Docs: Routines](https://code.claude.com/docs/en/routines)
- [Official Docs: Scheduled Tasks & /loop](https://code.claude.com/docs/en/scheduled-tasks)
- [Official Docs: Desktop Scheduled Tasks](https://code.claude.com/docs/en/desktop-scheduled-tasks)
- [Workflows Guide](../workflows/README.md) - Complementary manual workflow patterns
- [Hooks Guide](../hooks/README.md) - Event-driven automation within sessions
- [MCP Servers](../mcp-servers/README.md) - External tool integrations for routines
