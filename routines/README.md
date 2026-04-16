# Claude Code Routines & Daily Schedules

Production-ready routine prompts for automating daily development work with Claude Code.

A **routine** is a saved Claude Code configuration (prompt + repositories + connectors) that runs autonomously on a schedule, from an API call, or in response to a GitHub event. Routines execute on Anthropic-managed cloud infrastructure, so they keep working when your laptop is closed.

> **Shipped:** April 14, 2026 (research preview). Available on Pro, Max, Team, and Enterprise plans with Claude Code on the web enabled.

## Quick Navigation

- [How Routines Work](#how-routines-work)
- [Daily Schedule Examples](#daily-schedule-examples)
- [Morning Routines](#morning-routines)
- [Mid-Day Routines](#mid-day-routines)
- [End-of-Day Routines](#end-of-day-routines)
- [Nightly Routines](#nightly-routines)
- [Weekly Routines](#weekly-routines)
- [GitHub Event Routines](#github-event-routines)
- [API-Triggered Routines](#api-triggered-routines)
- [Prompt Quality Checklist](#prompt-quality-checklist)
  - [Anti-Patterns](#anti-patterns)
- [Usage Limits](#usage-limits)
- [Routines vs. /loop vs. Desktop Scheduled Tasks](#routines-vs-loop-vs-desktop-scheduled-tasks)

---

## How Routines Work

Three ways to run a routine:

| Trigger | When it runs | Best for |
|---------|--------------|----------|
| **Scheduled** | Hourly, daily, weekly cadence (minimum 1 hour) | Recurring chores: standup digests, backlog triage, docs drift |
| **API** | HTTP POST to a per-routine endpoint with a bearer token | Alert triage, deploy verification, webhook-style work |
| **GitHub** | Automatically on `pull_request.*` or `release.*` events | PR review, cross-SDK porting, release gating |

A single routine can combine triggers. Create routines at [claude.ai/code/routines](https://claude.ai/code/routines) or from the CLI with `/schedule`.

### Prompt-First Discipline

Routines run autonomously with no approval prompts mid-session. **Prompt quality drives outcome quality.** Every prompt in this guide follows four principles:

1. **Explicit success criteria** — spell out what "done" looks like
2. **Hard boundaries** — what the routine must never do
3. **Concrete output** — one specific destination (Slack channel, label, PR template)
4. **Failure handling** — how to surface problems instead of hiding them

---

## Daily Schedule Examples

A realistic day using Claude Code routines:

| Time | Routine | Trigger | Outcome |
|------|---------|---------|---------|
| 08:00 | Morning standup digest | Daily | Slack summary of overnight PRs, issues, deploys |
| 09:00 | Backlog triage | Daily | Fresh issues labeled, assigned, prioritized |
| 11:00 | Dependency & security scan | Daily | Draft PRs for vulnerable or outdated deps |
| 14:00 | CI failure watchdog | Hourly | Flaky vs. real failure triage posted to #build |
| 17:00 | End-of-day recap | Daily | Personal summary of commits, PRs, open threads |
| 23:00 | Nightly bug fixer | Daily | Top Linear bug attempted, draft PR for review |
| Sat 06:00 | Docs drift sweep | Weekly | Docs PRs opened for APIs that changed this week |

Each example below includes a complete prompt you can paste into `/schedule`.

---

## Morning Routines

### Morning Standup Digest

Runs daily at 08:00 local time. Posts a single Slack summary so the team starts the day with shared context instead of checking ten tabs.

**Prompt:**

```
You are preparing the engineering morning digest. Today's run covers the last 24 hours.

Scope:
- This repository's default branch
- Issues opened or updated in the linked Linear project
- Open pull requests on this repository

Steps:
1. List merged PRs in the last 24h with title, author, and one-line impact summary.
2. List open PRs older than 48h that are not draft, grouped by "needs review" vs "needs changes".
3. List Linear issues moved to Blocked or reopened in the last 24h.
4. List production deploys from the GitHub Deployments API in the last 24h.

Output:
- Post a single message to the #eng-standup Slack channel.
- Use this exact structure with H3 headers: "Merged", "Needs Review", "Blocked", "Deploys".
- Keep each line under 120 characters.
- If a section is empty, write "None" under it. Do not omit the section.

Boundaries:
- Do not merge, close, or comment on any PR or issue.
- Do not push any branches.
- If any API call fails, post a message noting which section is incomplete and why.
```

**Trigger:** Schedule, daily at 08:00 local

---

### Backlog Triage

Runs daily at 09:00. Reads issues opened since the last run, labels them by area, assigns based on CODEOWNERS, and posts a groomed queue.

**Prompt:**

```
You are triaging new issues opened in the linked Linear project since the last run of this routine.

Steps:
1. Read issues with status "Backlog" or "Triage" created in the last 24h.
2. For each issue:
   - Infer the affected area from referenced files, stack traces, or keywords.
   - Apply labels from this allowlist only: bug, feature, docs, perf, security, infra, ux.
   - Set priority: P0 for data loss or auth bypass; P1 for user-visible regression; P2 otherwise.
   - If the issue references a file path, assign the CODEOWNERS owner for that path.
   - If you cannot determine an area with confidence, apply the "needs-human-triage" label and skip assignment.

Output:
- After triage, post a markdown summary to #backlog-triage listing counts by label and any "needs-human-triage" issues with links.

Boundaries:
- Never close or delete issues.
- Never comment on issues.
- Never assign a human owner you cannot resolve from CODEOWNERS.
- If Linear or the repository is unavailable, post a failure notice to #backlog-triage and exit.
```

**Trigger:** Schedule, daily at 09:00 local

---

### Dependency & Security Scan

Runs daily at 11:00. Checks for outdated or vulnerable dependencies and opens targeted draft PRs.

**Prompt:**

```
You are scanning this repository for outdated and vulnerable dependencies.

Steps:
1. Run the project's dependency audit (detect npm, pip, cargo, or go.mod and use the matching tool).
2. Group findings into: critical CVE, high CVE, outdated major, outdated minor.
3. For each critical or high CVE:
   - Check the advisory's suggested fixed version.
   - If a non-breaking upgrade exists, open a draft PR on a claude/deps-<package> branch with only the version bump and changelog excerpt in the PR body.
   - If the upgrade requires code changes, open an issue with the CVE link and affected call sites.
4. For outdated minor versions, batch into a single draft PR titled "chore(deps): routine minor updates" — no more than 10 packages per PR.

Output:
- PR bodies must include: CVE ID (if any), current version, target version, link to changelog, list of affected files.
- After the run, post a one-line summary to #security-ops: "N critical, N high, N minor PRs opened."

Boundaries:
- Draft PRs only. Never merge.
- Never bump a major version automatically — open an issue instead.
- Never touch lockfiles outside of the dependency range you are upgrading.
- Skip any package listed in .claude/deps-skip.txt if that file exists.
```

**Trigger:** Schedule, daily at 11:00 local

---

## Mid-Day Routines

### CI Failure Watchdog

Runs hourly during work hours. Distinguishes flaky tests from real regressions so the team stops ignoring the #build channel.

**Prompt:**

```
You are triaging CI failures on the default branch.

Steps:
1. List failed workflow runs on the default branch in the last hour.
2. For each failure:
   - Fetch the failing job logs.
   - Extract the failing test name and error message.
   - Search the last 20 runs of the same job for the same test name.
   - Classify as FLAKY (passed >80% of recent runs) or REAL (consistent failure).
3. For REAL failures:
   - Identify the PR or commit that introduced the failure using git blame on the changed test or the last file edited.
   - Open a GitHub issue titled "CI failure: <test name> on <commit sha>" with the log excerpt, suspect commit, and suspect author.
4. For FLAKY failures:
   - Post a one-line note to #build-flakes with the test name and link.
   - Do not open an issue.

Output:
- Post a summary to #build: "N real failures (issues opened), N flaky (logged)."
- If zero failures, post nothing. Silence is fine here.

Boundaries:
- Do not re-run any workflow.
- Do not revert any commit.
- Do not push any branches.
- If you cannot identify a suspect commit, label the issue "unknown-blame" and stop.
```

**Trigger:** Schedule, hourly between 09:00 and 18:00 local

---

### Slow Query Sweep

Runs mid-afternoon against production logs or an APM connector to catch performance regressions before the end of the day.

**Prompt:**

```
You are identifying slow database queries from the last 4 hours of production traffic.

Steps:
1. Query the APM connector for the 10 slowest database spans (p95) in the last 4 hours.
2. For each slow query:
   - Identify the calling service and endpoint.
   - Check git log for recent changes to that endpoint (last 7 days).
   - Flag as REGRESSION if the query was not in the previous day's top 10 but is now.
3. For any REGRESSION:
   - Open an issue with the query, p95 latency, calling endpoint, and suspect commit.
   - Apply labels: perf, regression, P1.

Output:
- Post a markdown table to #perf: rank, query (redacted of PII), p95, classification.

Boundaries:
- Never execute any query against the production database. APM read-only access only.
- Redact all literal values in queries (replace with "?") before posting.
- Do not include any row-level data, even in issue bodies.
```

**Trigger:** Schedule, daily at 14:00 local

---

## End-of-Day Routines

### Personal End-of-Day Recap

Runs at 17:00. Gives the developer a clean handoff summary they can paste into a standup doc or Slack DM.

**Prompt:**

```
You are summarizing my activity today on this repository.

Scope:
- Commits I authored on any branch in the last 8 hours.
- PRs I opened, updated, or reviewed today.
- Issues I commented on or closed today.

Steps:
1. Group my commits by branch, with a one-line summary per branch.
2. List PRs I opened today with status (draft, ready, merged).
3. List PRs I reviewed with outcome (approved, changes requested, commented).
4. List any CI failures on my branches as of end of day.
5. Identify open threads: review comments waiting on me, failing tests, unmerged PRs older than 24h.

Output:
- Write the result to a markdown file at handoffs/YYYY-MM-DD.md in a claude/daily-recap branch.
- Include H2 sections: "Shipped", "In Progress", "Reviewed", "Open Threads".
- Keep it under 40 lines. Bullets only.

Boundaries:
- Never include commit diffs or code snippets.
- Never merge or close anything.
- Do not overwrite an existing file with the same date — append a timestamp suffix instead.
```

**Trigger:** Schedule, weekdays at 17:00 local

---

### Stale PR Nudge

Runs at 18:00. Identifies PRs stuck waiting on review or changes and nudges the right person without turning into spam.

**Prompt:**

```
You are identifying stale pull requests on this repository.

Criteria:
- "Stale waiting on review": open >48h, no review comments, not draft.
- "Stale waiting on author": open >72h, last activity was a review requesting changes, PR author has not pushed since.

Steps:
1. Walk open PRs and classify into the two buckets above.
2. For "waiting on review", identify assigned reviewers; if none, use CODEOWNERS for the most-changed file.
3. Compose one Slack message per stale PR.

Output:
- Send a single batched message to #pr-nudges with sections "Waiting on Review" and "Waiting on Author".
- Under each, list PRs as: "<PR title> — @reviewer — <PR link>".
- If both buckets are empty, send nothing.

Boundaries:
- Do not @-mention a person more than once per day, even across multiple stale PRs.
- Do not DM anyone directly — batched channel message only.
- Never close a PR for staleness.
```

**Trigger:** Schedule, weekdays at 18:00 local

---

## Nightly Routines

### Nightly Bug Fixer

The headline routine from the 2026 launch. Pulls the top bug from Linear, attempts a fix, opens a draft PR for morning review.

**Prompt:**

```
You are attempting a fix for the highest-priority unassigned bug in the linked Linear project.

Steps:
1. Find the top Linear issue matching: status in (Backlog, Todo), label "bug", priority P0 or P1, no assignee.
2. If none, exit and post "No candidate bug tonight" to #nightly-fixer.
3. Read the issue description, acceptance criteria, and any linked stack traces.
4. Investigate the affected code. Use grep and read files — do not run tests against production-connected services.
5. Propose and implement a minimal fix on a claude/fix-<issue-id> branch.
6. Add or update at least one test that would have caught this bug.
7. Run the full test suite. If it fails, do not open a PR — update the Linear issue with a comment explaining what you tried and what blocked you.
8. If tests pass, open a draft PR titled "fix: <issue title> (<issue id>)" linked to the Linear issue.

PR body must include:
- Linear issue link
- Root cause (2-3 sentences)
- What changed (bulleted file list)
- Test added (name and what it asserts)
- What you are unsure about (at least one item)

Boundaries:
- Draft PRs only.
- Never mark the Linear issue as Done — leave it In Review.
- Never push to any branch not prefixed with claude/fix-.
- Never touch migration files, CI config, or infrastructure as code.
- If the fix would require changes outside the affected module, stop and comment on the issue instead.
```

**Trigger:** Schedule, daily at 23:00 local

---

### Overnight Test Flake Quarantine

Catches tests that flaked >3 times in 24h and temporarily quarantines them with an owner-assigned follow-up.

**Prompt:**

```
You are quarantining flaky tests based on the last 24 hours of CI runs on the default branch.

Steps:
1. Query workflow runs on the default branch from the last 24h.
2. For each test that failed and later passed in the same or subsequent run on the same commit, increment a flake count.
3. For any test with flake count >= 3:
   - Add the appropriate skip or quarantine marker (detect the test framework: pytest, jest, go test).
   - Add a TODO comment above the marker with the test name, flake count, and a link to this routine's session.
   - Open an issue titled "Flaky: <test name>" with owner inferred from git blame of the test file.

Output:
- Open one claude/quarantine-<date> branch with all quarantine changes.
- Open one PR titled "test: quarantine flaky tests <date>" summarizing quarantined tests in a table.

Boundaries:
- Never quarantine more than 5 tests per run — if more qualify, quarantine the top 5 by flake count and log the rest.
- Never touch tests under paths listed in .claude/no-quarantine.txt.
- Draft PR only.
```

**Trigger:** Schedule, daily at 02:00 local

---

## Weekly Routines

### Docs Drift Sweep

Weekly routine from the Anthropic launch examples. Catches stale docs before they mislead readers.

**Prompt:**

```
You are identifying documentation that references code that has changed this week.

Steps:
1. List merged PRs on the default branch in the last 7 days.
2. For each PR, extract the list of changed public symbols (exported functions, classes, API routes, CLI flags).
3. Grep the docs/ directory and README.md for each symbol.
4. For every match in a docs file, verify the doc's described behavior still matches the current code.
5. Group mismatches by docs file.

Output:
- For each docs file with mismatches, open a draft PR on claude/docs-drift-<file>.
- PR body: list each symbol, the behavior described in docs, the new behavior, and a suggested edit.
- Post a summary to #docs-drift: "N docs files need updates, N PRs opened."

Boundaries:
- Draft PRs only.
- Do not rewrite prose wholesale — include a targeted diff per mismatched symbol.
- If no mismatches found, post "Docs are in sync this week" to #docs-drift.
- Do not touch CHANGELOG.md or release notes.
```

**Trigger:** Schedule, weekly on Saturday at 06:00 local

---

### Weekly Codebase Health Report

Runs Monday morning. Summarizes technical debt signals without prescribing fixes.

**Prompt:**

```
You are producing a weekly codebase health report.

Measure the following for the last 7 days:
1. Lines added vs removed on the default branch.
2. Number of TODOs, FIXMEs, and HACKs added vs removed (via git diff search).
3. Test coverage delta if a coverage report exists at coverage/summary.json.
4. Number of files with >500 lines that grew this week.
5. Top 5 files by churn (distinct commits).
6. Dead code candidates: exported symbols that are never imported elsewhere in the repo.

Output:
- Post a markdown report to #eng-weekly with one H3 per metric.
- For each metric, include a trend arrow vs the previous week (store previous values in a claude/health-history.json file in the repo on a claude/health-report branch).
- Commit the updated history file on the same branch and open a draft PR titled "chore: weekly health history <date>".

Boundaries:
- This is observational. Do not open issues or propose fixes.
- Never modify any file other than claude/health-history.json.
- If the history file is missing, create it with only this week's data and skip the trend arrows.
```

**Trigger:** Schedule, weekly on Monday at 07:00 local

---

## GitHub Event Routines

### On-Open Pull Request Review

Fires on `pull_request.opened` and `pull_request.synchronize`. Leaves inline feedback so human reviewers focus on design.

**Prompt:**

```
You are performing a first-pass review on a pull request.

Scope:
- Only the files changed in this PR.
- Use the team review checklist in docs/REVIEW-CHECKLIST.md if present; otherwise use the default below.

Default checklist:
- Security: SQL injection, XSS, path traversal, unchecked auth, secrets in code.
- Correctness: off-by-one errors, unhandled null, missing await, wrong comparison operator.
- Tests: any new public function lacking a test; any test that tests implementation instead of behavior.
- Style: only if a project linter rule is violated. Ignore personal style preferences.

Steps:
1. For each changed file, walk the hunks and apply the checklist.
2. Leave inline comments with severity prefix: [CRITICAL], [HIGH], [MEDIUM], [LOW].
3. Add a single summary comment at the bottom with counts by severity and an overall verdict: APPROVE, REQUEST_CHANGES, or COMMENT.

Output:
- Inline comments on exact lines.
- One summary comment.

Boundaries:
- Never approve a PR with any [CRITICAL] or [HIGH] finding — use REQUEST_CHANGES.
- Never merge the PR under any circumstances.
- Never leave more than 15 inline comments — if the PR has more issues, list the extras in the summary comment.
- Do not comment on formatting unless a linter rule is violated.
- Skip PRs with the label "skip-ai-review".
```

**Trigger:** GitHub, `pull_request.opened` and `pull_request.synchronize`, filter: `is draft = false`

---

### Bespoke Module Guard

Fires on any PR touching a sensitive module (auth, billing, payments). Posts a heads-up to the domain channel before a human reviewer looks.

**Prompt:**

```
You are watching for pull requests that touch security-sensitive modules.

Scope:
- This PR's changed files.

Steps:
1. Check if any changed file is under src/auth/, src/billing/, or src/payments/. Adjust these paths for your repo layout.
2. If not, exit silently.
3. If yes:
   - Summarize what changed: files touched, functions added or removed, new external calls.
   - Identify any changes to authentication checks, permission gates, or money math.
   - Post a message to #sensitive-changes tagging the module's owner from CODEOWNERS.

Message format:
- Title: "Sensitive-module PR: <PR title>"
- Link to PR
- Summary (5 bullets max)
- Specific concerns (e.g., "removes a permission check on line 47")
- "Full review required before merge"

Boundaries:
- Do not request changes or approve.
- Do not leave inline comments — channel post only.
- If the PR is from a bot (dependabot, renovate), skip.
```

**Trigger:** GitHub, `pull_request.opened`, filter: none (the routine filters by path itself)

---

## API-Triggered Routines

### Alert-to-Draft-PR

Pointed at by Datadog, Sentry, or any alerting tool via its HTTP webhook. Turns a page into a draft fix on a claude/ branch.

**Prompt:**

```
You are responding to an incoming production alert passed in the `text` field of the trigger payload.

Steps:
1. Parse the alert body. Extract: service name, error message, stack trace, timestamp.
2. In this repository, find the file and line matching the top of the stack trace.
3. Check git log for commits touching that file in the last 14 days. Identify the likely regression commit.
4. Investigate the code around the failing line. Read related tests.
5. Propose a minimal fix on a claude/alert-<timestamp> branch.
6. Add a regression test that fails without the fix.
7. Run the test suite. If it passes, open a draft PR. If it fails, post a comment on the alert's incident thread explaining what blocked you.

PR body must include:
- Alert ID and link
- Stack trace excerpt
- Suspect commit SHA and author
- Proposed fix summary
- Test added
- Confidence: HIGH / MEDIUM / LOW with one sentence why

Boundaries:
- Draft PRs only.
- Never deploy or hotfix.
- Never revert a commit automatically — open an issue instead if revert seems warranted.
- If the alert lacks a stack trace, post "Need stack trace to proceed" to the incident thread and exit.
```

**Trigger:** API endpoint called by alerting tool webhook

---

### Deploy Verification Gate

Called by the CD pipeline after a production deploy. Smoke-checks the new build and posts a go/no-go.

**Prompt:**

```
You are verifying a production deploy. The trigger payload contains the deploy ID in `text`.

Steps:
1. Parse the deploy ID.
2. Hit the health endpoint documented in docs/DEPLOY.md (default: /healthz).
3. Run the smoke test suite tagged @smoke (pytest -m smoke, jest --grep @smoke, or go test -tags smoke — detect by repo).
4. Query the APM connector for error rate on the deployed service in the 5 minutes after deploy. Compare to the baseline in the 1 hour before deploy.
5. Scan the last 5 minutes of logs for any new ERROR-level entries.

Decision:
- GO if: health check passes, smoke tests pass, error rate increase <20%, no new ERROR patterns.
- NO_GO otherwise.

Output:
- Post a message to #releases with:
  - Decision: GO or NO_GO (with a clear emoji or marker)
  - Deploy ID
  - Health check result
  - Smoke test summary
  - Error rate delta
  - New ERROR patterns (if any)

Boundaries:
- Never roll back automatically.
- If NO_GO, also @mention the on-call engineer in the message.
- Never modify infrastructure.
- Complete within 5 minutes — if any check times out, mark NO_GO with reason "verification timeout".
```

**Trigger:** API endpoint called from CD pipeline

---

## Prompt Quality Checklist

Before saving a routine, verify the prompt answers all five:

- [ ] **Scope**: What data sources, repos, or channels does the routine read?
- [ ] **Steps**: Numbered, each step single-purpose, no ambiguous "as appropriate" language?
- [ ] **Output**: Exact destination, exact format, counts of sections required?
- [ ] **Boundaries**: What the routine must never do (merge, delete, escalate, push to main)?
- [ ] **Failure mode**: How does the routine surface partial success or full failure?

**Rule of thumb:** If a prompt reads like a ticket you would hand to a new hire with no Slack access, it is ready.

### Anti-Patterns

| Bad | Why | Better |
|-----|-----|--------|
| "Review PRs" | No scope, no criteria, no output | See [On-Open PR Review](#on-open-pull-request-review) |
| "Check for bugs" | Infinitely recursive, no success criteria | "Run the failing test list from the last 24h and classify each as flaky or real" |
| "Fix the issue" | No boundary — could rewrite the repo | "Propose a minimal fix on claude/fix-<id>, draft PR only, never touch migrations" |
| "Summarize yesterday" | No output destination, no format | "Post H2-sectioned markdown to #eng-standup with Merged/Needs Review/Blocked/Deploys" |

---

## Usage Limits

Each account has a daily cap on how many routine runs can start, and routines also count against standard subscription token usage. The per-plan numbers are not published in the docs and can change during the research preview — check your current allowance at [claude.ai/code/routines](https://claude.ai/code/routines) or [claude.ai/settings/usage](https://claude.ai/settings/usage). Organizations with extra usage enabled can continue on metered overage when the daily cap is hit.

Minimum schedule interval: **1 hour**. For sub-hour polling, use `/loop` inside an active session instead.

---

## Routines vs. `/loop` vs. Desktop Scheduled Tasks

| Mechanism | Runs where | Survives laptop closed | Minimum interval | Best for |
|-----------|------------|------------------------|------------------|----------|
| **Routines** | Anthropic cloud | Yes | 1 hour | Production daily/weekly automation |
| **Desktop scheduled tasks** | Your machine | No (needs machine on) | 1 minute | Local-file-aware automation |
| **`/loop`** | Active session | No (needs session open) | Seconds | In-session polling and pacing |

Use routines as the default. Drop to desktop tasks when the automation needs local files or tools. Use `/loop` only for tight polling inside an active session.

---

## Resources

### Official
- [Automate work with routines](https://code.claude.com/docs/en/routines) — canonical docs
- [Introducing routines in Claude Code](https://claude.com/blog/introducing-routines-in-claude-code) — launch post with use cases
- [Run prompts on a schedule](https://code.claude.com/docs/en/scheduled-tasks) — `/schedule` and `/loop`
- [Desktop scheduled tasks](https://code.claude.com/docs/en/desktop-scheduled-tasks) — local alternative

### Practitioner Guides
- [Claude Code Routines: Put Your AI Agent on Cloud Autopilot](https://claudefa.st/blog/guide/development/routines-guide)
- [5 Claude Code Agentic Workflow Patterns](https://www.mindstudio.ai/blog/claude-code-agentic-workflow-patterns) — sequential, operator, split-and-merge, agent teams, headless
- [Put Claude on Autopilot: Scheduled Tasks with /loop and /schedule](https://medium.com/@richardhightower/put-claude-on-autopilot-scheduled-tasks-with-loop-and-schedule-built-in-skills-43f3be5ac1ec)
- [Claude Code routines: Automate dev workflows](https://dev.to/onsen/claude-code-routines-automate-dev-workflows-4ijn)

### Related Sections in This Repo
- [Workflows](../workflows/README.md) — interactive workflows for planning, review, debugging
- [Prompts](../prompts/README.md) — prompt patterns for interactive sessions
- [Hooks](../hooks/README.md) — event-driven automation inside a session
- [MCP Servers](../mcp-servers/README.md) — connectors routines can call
