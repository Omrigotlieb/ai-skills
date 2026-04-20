# Claude Code Routines and Scheduled Tasks

Production-ready routines, loop templates, and scheduled task patterns for automating your daily developer workflow with Claude Code.

> **Related:** For installable skill definitions, see [Automation Skills](../skills/automation/README.md). For copy-paste agent prompts, see [Agent Prompts](../prompts/agent-prompts.md). This page focuses on scheduling, loop configuration, and the recommended daily routine structure.

## Quick Navigation

- [Daily Routines](#daily-routines)
- [PR Management](#pr-management)
- [Code Quality](#code-quality)
- [Security and Dependencies](#security-and-dependencies)
- [Documentation](#documentation)
- [Loop Templates](#loop-templates)
- [Scheduled Task Setup](#scheduled-task-setup)

---

## Daily Routines

### Morning PR Digest

Run before standup to get a snapshot of open PRs:

```markdown
---
name: morning-pr-digest
description: Summarize open PRs by age, reviewer status, and merge readiness
schedule: "0 8 * * 1-5"
---

Review all open pull requests in this repository.

For each PR, report:
- Title, author, and age (days open)
- CI status (passing/failing/pending)
- Review status (approved/changes requested/awaiting review)
- Merge conflicts (yes/no)

Group by priority:
1. Ready to merge (approved + CI green)
2. Needs attention (failing CI or stale reviews)
3. In progress (recently updated, awaiting review)

Keep the report under 30 lines. Skip PRs opened today.
```

### Daily Issue Triage

Automatically label and categorize new issues:

```markdown
---
name: daily-issue-triage
description: Triage issues opened in the last 24 hours
schedule: "0 9 * * 1-5"
---

List issues opened in the last 24 hours using `gh issue list --state open`.

For each new issue:
1. Read the issue body and any linked code references
2. Suggest appropriate labels based on content (bug, feature, docs, etc.)
3. Identify which area of the codebase is affected
4. Flag urgent issues that mention crashes, data loss, or security

Output a summary grouped by suggested label. Do not modify issues directly.
```

### Morning Briefing (with MCP)

Requires email and calendar MCP servers:

```markdown
---
name: morning-briefing
description: Review emails, calendar, and repo activity for a daily briefing
schedule: "0 7 * * 1-5"
---

Compile a morning briefing covering:

1. Unread emails: sort into urgent / actionable / informational / skip
2. Today's calendar: list meetings with prep notes where relevant
3. Repo activity overnight: new PRs, merged PRs, failed CI runs

Draft replies for urgent emails. Keep the full briefing under 50 lines.
Format as a scannable list, not prose.
```

---

## PR Management

### PR Babysitter

The most useful loop for active development. Watches a PR through CI and review:

```markdown
---
name: babysit-pr
description: Monitor a PR through CI, reviews, and merge readiness
---

Check the current branch's open PR:

1. Run `gh pr view` to get current status
2. Run `gh pr checks` to see CI results
3. If CI is failing:
   - Pull the failing job log with `gh run view <id> --log-failed`
   - Diagnose the root cause
   - Push a minimal fix if confident, otherwise report
4. If review comments exist:
   - Read each unresolved comment
   - Triage: Fix (clear improvement) / Dismiss (disagree with reason) / Escalate (need human judgment)
   - Address fixable comments, push changes
5. If everything is green and approved:
   - Report "Ready to merge" and stop

Maximum 3 fix iterations before stopping and reporting status.
```

### Merge Conflict Detector

```markdown
---
name: conflict-detector
description: Detect merge conflicts on open PRs and report complexity
schedule: "0 12 * * 1-5"
---

For each open PR in this repository:
1. Check if it has merge conflicts with the base branch
2. If conflicts exist, report:
   - PR number and title
   - Files with conflicts
   - Complexity estimate (trivial/moderate/complex)

Do not attempt to resolve conflicts automatically.
Output a list sorted by conflict complexity.
```

---

## Code Quality

### Weekly Code Quality Report

```markdown
---
name: weekly-quality-report
description: Audit codebase for quality issues and technical debt
schedule: "0 0 * * 0"
---

Perform a weekly code quality audit:

1. Run linting and report any new violations since last week
2. Check test coverage if a coverage tool is configured
3. Identify files with the most churn (frequent changes) using `git log --since="1 week ago" --name-only`
4. Flag any TODO/FIXME/HACK comments added in the last week
5. Check for unused imports or dead exports if tooling supports it

Report findings grouped by severity:
- Critical: test coverage drops, lint errors in core modules
- Moderate: high-churn files without tests, stale TODOs
- Low: style nits, minor cleanup opportunities

Keep the report actionable. Skip anything that would take less than 5 minutes to fix.
```

### Nightly Test Runner

```markdown
---
name: nightly-tests
description: Run full test suite and report regressions
schedule: "0 2 * * *"
---

Run the full test suite for this project.

If any tests fail:
1. Identify which tests broke
2. Check `git log --since="1 day ago"` for recent changes that could have caused the failure
3. Correlate failing tests with changed files
4. Report: test name, error message, likely culprit commit

If all tests pass, report "All tests passing" in one line.
Do not attempt fixes. This is a monitoring routine.
```

---

## Security and Dependencies

### Weekly Dependency Audit

```markdown
---
name: dependency-audit
description: Audit dependencies for vulnerabilities and available updates
schedule: "0 9 * * 1"
---

Run the appropriate dependency audit for this project:
- Node.js: `npm audit` or `yarn audit`
- Python: `pip audit` or `safety check`
- Go: `govulncheck ./...`
- Rust: `cargo audit`

For each finding:
1. Severity (critical/high/moderate/low)
2. Package name and affected version
3. Fixed version if available
4. Whether the vulnerable code path is reachable

Group by severity. For critical/high issues with available fixes,
create a PR with the upgrade. For moderate/low, include in the report only.
```

### Nightly Dependency Upgrade Check

```markdown
---
name: dependency-upgrade
description: Check for non-breaking dependency upgrades and test them
schedule: "0 3 * * *"
---

Check for available non-major-version dependency upgrades.

For each upgradable package:
1. Apply the upgrade
2. Run the test suite
3. If tests pass, include in a single "dependency upgrades" PR
4. If tests fail, revert and note the failure

Create at most one PR per run. Include a changelog summary for each upgraded package.
Never upgrade major versions without human approval.
```

---

## Documentation

### Docs Drift Scanner

```markdown
---
name: docs-drift
description: Detect documentation that references changed APIs or interfaces
schedule: "0 10 * * 1"
---

Scan PRs merged since last Monday using `gh pr list --state merged --search "merged:>YYYY-MM-DD"`.

For each merged PR:
1. Identify changed function signatures, API endpoints, or config options
2. Search documentation files (README, docs/, wiki) for references to changed items
3. Flag any doc that references old signatures or removed options

Output a list of docs that need updating, with the specific outdated reference.
Do not modify docs. This is a detection routine.
```

### Changelog Generator

```markdown
---
name: changelog-update
description: Generate changelog entries from merged PRs
schedule: "0 17 * * 5"
---

Review all PRs merged this week using `gh pr list --state merged --search "merged:>YYYY-MM-DD"`.

Categorize each PR:
- Added: new features or capabilities
- Changed: modifications to existing behavior
- Fixed: bug fixes
- Removed: deprecated or removed features
- Security: security-related changes

Generate a changelog entry in Keep a Changelog format.
Output the entry for human review. Do not modify CHANGELOG.md directly.
```

---

## Loop Templates

### Default Loop (`.claude/loop.md`)

Place this file in your project to customize what `/loop` does between iterations:

```markdown
Check the current branch's open PR. If CI is red, pull the failing
job log, diagnose, and push a minimal fix. If new review comments
have arrived, address each one and resolve the thread. If everything
is green and quiet, say so in one line.
```

### Build Watcher Loop

For long-running builds:

```markdown
Check if the current build/CI run has completed.
If it failed, pull the log and diagnose the failure.
If it passed, report success and stop looping.
If still running, report progress and continue.
```

### Deploy Monitor Loop

```markdown
Check the latest deployment status.
If the deploy succeeded, run smoke tests against the deployed URL.
If smoke tests fail, report which checks failed and suggest rollback.
If the deploy is still in progress, report status and continue.
If the deploy failed, pull the deployment log and diagnose.
```

---

## Scheduled Task Setup

### Cloud Routines (survive laptop closure)

> **Note:** Cloud routines are available in Claude Code desktop and web apps. The exact CLI interface may vary by version. See [Claude Code Routines Documentation](https://code.claude.com/docs/en/routines) for current syntax.

Routines run on Anthropic's infrastructure and persist even when your machine is off. Minimum interval is 1 hour.

### Desktop Scheduled Tasks

> **Note:** Desktop scheduled tasks require the Claude desktop app. See [Scheduled Tasks Documentation](https://code.claude.com/docs/en/scheduled-tasks) for setup instructions.

Desktop tasks have access to local files and tools. Minimum interval is 1 minute. Tasks auto-expire after 7 days of inactivity.

### In-Session Loops

```bash
# Fixed interval loop (check every 5 minutes)
/loop 5m Check PR status and fix CI if needed

# Dynamic interval loop (Claude self-paces)
/loop Watch this PR until it merges or needs human intervention

# Custom loop behavior (reads from .claude/loop.md)
/loop
```

---

## The Daily Developer Schedule

A recommended routine configuration for a full day of AI-assisted development:

| Time | Routine | Type | Purpose |
|------|---------|------|---------|
| 7:30 AM | Morning briefing | Cloud | Email, calendar, overnight activity |
| 8:30 AM | PR digest | Cloud | Review readiness before standup |
| 9:00 AM | Issue triage | Cloud | Categorize overnight issues |
| During work | PR babysitter | Loop | CI monitoring, review response |
| 12:00 PM | Conflict check | Cloud | Detect merge conflicts early |
| 2:00 AM | Nightly tests | Cloud | Full regression suite |
| 3:00 AM | Dependency upgrades | Cloud | Safe non-breaking updates |
| Sunday midnight | Quality report | Cloud | Weekly debt and coverage check |
| Monday 9:00 AM | Dependency audit | Cloud | Security vulnerability scan |
| Monday 10:00 AM | Docs drift | Cloud | Stale documentation detection |
| Friday 5:00 PM | Changelog | Cloud | Weekly changelog draft |

### Governance Principles

1. **Create PRs, never merge** - humans approve all changes that ship
2. **Read issues, never respond** - triage and label, but let humans communicate
3. **Report, don't act** on anything ambiguous - flag for human judgment
4. **Silent when clean** - only notify when something actionable is found
5. **Maximum iterations** - always set a cap on fix attempts (usually 3)

---

## Resources

- [Claude Code Routines Documentation](https://code.claude.com/docs/en/routines)
- [Claude Code Scheduled Tasks](https://code.claude.com/docs/en/scheduled-tasks)
- [Babysitting PRs with Claude Code](https://www.solberg.is/babysit-pr)
- [Keeping Open Source Projects Alive with Claude](https://www.tag1.com/blog/keeping-open-source-projects-alive-with-claude/)
