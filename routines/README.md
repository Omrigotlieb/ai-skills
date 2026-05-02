# Claude Code Routines & Scheduled Tasks

Ready-to-use prompt templates for Claude Code [Routines](https://code.claude.com/docs/en/routines) — cloud agents that run on a schedule, on a GitHub trigger, or via API call.

> **Three automation tiers in Claude Code:**
> - **`/loop`** — session-scoped, runs while the conversation is open
> - **Desktop Scheduled Tasks** — persist across restarts, run while the Desktop app is open
> - **Cloud Routines** — run on Anthropic infrastructure 24/7 (`/schedule` in CLI or `claude.ai/code/routines`)

## Quick Navigation

- [Daily Standup Brief](#daily-standup-brief)
- [Dependency Audit](#dependency-audit)
- [Security Scan](#security-scan)
- [Docs Drift Detector](#docs-drift-detector)
- [Code Health Scan](#code-health-scan)
- [Test Coverage Monitor](#test-coverage-monitor)
- [Tech Debt Audit](#tech-debt-audit)
- [PR Review Bot](#pr-review-bot)
- [Changelog Generator](#changelog-generator)
- [Repo Health Check](#repo-health-check)
- [CI Failure Analyst](#ci-failure-analyst)
- [Stale TODO Janitor](#stale-todo-janitor)
- [Performance Regression Detector](#performance-regression-detector)
- [Feature Flag Cleanup](#feature-flag-cleanup)
- [Nightly Bug Fixer](#nightly-bug-fixer)
- [Morning Briefing](#morning-briefing)
- [Best Practices](#best-practices)

---

## Daily Standup Brief

**Schedule:** Daily at 9:00 AM  
**Connectors:** GitHub, Slack  
**Use case:** Replace manual standup prep with an automated triage of PRs, commits, and issues.

```
Read all open PRs and commits merged since yesterday in this repository.
Summarize:
1. What landed yesterday (merged PRs with one-line summaries)
2. What's in flight (open PRs, who's reviewing)
3. Anything blocked (PRs with failing CI or no reviewers assigned)

If no new activity since the last run, post "Nothing to triage" and exit.
Post the summary to #dev-standup in Slack.
```

**Why it works:** Surfaces blockers before the standup meeting and gives everyone a shared baseline without manual digging through GitHub.

---

## Dependency Audit

**Schedule:** Daily at 2:00 AM UTC  
**Connectors:** GitHub  
**Use case:** Catch vulnerable or outdated dependencies before they reach production.

```
Run the project's dependency audit command (npm audit / pip audit / cargo audit / etc.).
Filter results to severity high or critical.
For each finding:
  - Explain the risk in plain language
  - Determine if the project actually uses the vulnerable code path
  - Recommend: upgrade, patch, or replace
  - If a safe upgrade exists, open a PR on a claude/ branch with the update

Open a GitHub issue for each finding that cannot be auto-fixed.
Do not merge any PRs. Do not push to main. Only push to claude/ branches.
```

**Why it works:** Filters noise (low/moderate) and checks whether the vulnerable path is actually reachable, avoiding the "audit fatigue" that makes teams ignore alerts.

---

## Security Scan

**Schedule:** Every Sunday at 3:00 AM UTC  
**Connectors:** GitHub  
**Use case:** Weekly sweep for secrets, Dockerfile misconfigurations, and OWASP top-10 risks.

```
Perform a security audit of this repository:
1. Scan for secrets: API keys, tokens, passwords in config files or code
2. Check Dockerfiles: running as root, using :latest tags, exposing unnecessary ports
3. Review for OWASP top-10: SQL injection, XSS, auth flaws, insecure deserialization
4. Check for overly permissive CORS, missing rate limiting, missing input validation
5. Scan dependencies for known CVEs

For each finding, assign severity (Critical / High / Medium / Low) and provide
a specific remediation with code example.
Open a GitHub issue titled "Security Scan Report - [date]" with all findings.
```

**Why it works:** Catches the categories that automated scanners miss (logical auth flaws, CORS misconfiguration) by combining static analysis with semantic understanding.

---

## Docs Drift Detector

**Schedule:** Every Friday at 6:00 AM UTC  
**Connectors:** GitHub  
**Use case:** Catch documentation that fell out of sync with code changes.

```
Scan all pull requests merged in the past 7 days.
Identify any documentation files that reference modified functions, APIs,
or configuration options.
If the documentation is outdated relative to the code changes:
  - Open a PR on a claude/ branch with suggested updates
  - Include a summary of what changed and why the docs need updating

If no documentation drift is detected, post "Docs are up to date" and exit.
Do not merge any PRs. Only push to claude/ branches.
```

**Why it works:** Documentation rot is the #1 source of developer frustration. This routine catches it within a week of the causing change, when context is still fresh.

---

## Code Health Scan

**Schedule:** Every Monday at 2:00 AM UTC  
**Connectors:** GitHub  
**Use case:** Surface code smells, dead code, and complexity hotspots before they compound.

```
Run a comprehensive code quality scan:
1. Identify unused exports and dead code paths
2. Find duplicate code blocks (>10 lines)
3. Flag functions exceeding 50 lines or cyclomatic complexity > 10
4. Check for TODO/FIXME comments older than 30 days
5. Identify files with no test coverage

Rank findings by severity.
Open a single GitHub issue titled "Weekly Code Health Report - [date]"
with findings grouped by category.
If no findings, post "Code health is clean" and exit.
```

**Why it works:** Catches the gradual accumulation of complexity that code reviews miss because each individual PR looks fine.

---

## Test Coverage Monitor

**Schedule:** Daily at 11:00 PM UTC  
**Connectors:** GitHub  
**Use case:** Track coverage trends and catch regressions before they become permanent.

```
Run the full test suite with coverage enabled.
Compare coverage percentages against the previous run stored in
coverage-history.json (create it if it doesn't exist).
Flag:
- Any file where coverage dropped by more than 5%
- New files with 0% coverage
- Functions/methods with no test coverage that are part of the public API

If coverage dropped, open a GitHub issue with the specific files and
suggested test cases.
Update coverage-history.json on a claude/ branch.
```

**Why it works:** Coverage thresholds in CI are binary (pass/fail). This routine tracks trends and identifies exactly which files are sliding.

---

## Tech Debt Audit

**Schedule:** 1st of every month at 4:00 AM UTC  
**Connectors:** GitHub  
**Use case:** Monthly nine-dimension assessment that produces an actionable, file-cited report.

```
Audit this codebase across these dimensions:
1. Architectural decay (circular dependencies, god classes)
2. Consistency rot (mixed patterns, naming inconsistencies)
3. Type & contract debt (any types, missing interfaces)
4. Test debt (untested public APIs, flaky test patterns)
5. Dependency debt (outdated packages, unmaintained deps)
6. Performance hygiene (synchronous I/O, missing indexes)
7. Error handling (swallowed exceptions, missing error boundaries)
8. Security hygiene (hardcoded values, missing sanitization)
9. Documentation drift (stale comments, missing JSDoc)

For each dimension, cite specific files and line numbers.
Do NOT recommend rewrites. Do NOT pad categories with filler.
If a dimension is clean, say so and move on.
Commit the report as TECH_DEBT_AUDIT.md on a claude/ branch and open a PR.
```

**Why it works:** Monthly cadence prevents the report from becoming noise, and the nine-dimension framework ensures comprehensive coverage without scope creep.

**Source:** Inspired by [ksimback/tech-debt-skill](https://github.com/ksimback/tech-debt-skill).

---

## PR Review Bot

**Trigger:** GitHub `pull_request.opened`  
**Connectors:** GitHub  
**Use case:** Automated first-pass review so human reviewers can focus on design decisions.

```
Review this pull request against the following checklist:
1. Security: credential exposure, injection risks, auth bypass
2. Performance: N+1 queries, unbounded loops, missing pagination
3. Style: naming conventions, file organization, import ordering
4. Test coverage: are new code paths tested? Edge cases covered?
5. Breaking changes: API contract changes, schema migrations

Leave inline comments on specific lines where issues are found.
Add a summary comment categorizing findings as Blocking / Warning / Suggestion.
If no issues found, approve with a "LGTM" comment noting what was checked.
```

**Why it works:** Catches mechanical issues (security, performance, style) instantly, freeing human reviewers for architectural and design feedback.

---

## Changelog Generator

**Trigger:** GitHub `release.created` or manual  
**Connectors:** GitHub  
**Use case:** Draft user-facing release notes from PR history.

```
Generate release notes for the latest version.
Use PRs merged since the previous version tag.
Format as a user-facing changelog:
- Group by: Features / Bug Fixes / Breaking Changes / Performance
- Exclude internal refactoring and CI/build changes
- Write in user-facing language (not developer jargon)
- Include PR numbers and author attribution

Commit as CHANGELOG.md update on a claude/ branch and open a PR.
```

**Why it works:** Changelog writing is tedious and routinely skipped. Automating it ensures every release ships with notes.

---

## Repo Health Check

**Schedule:** Every Monday at 8:00 AM UTC  
**Connectors:** GitHub, Slack  
**Use case:** Weekly hygiene sweep for stale branches, stuck PRs, and CI rot.

```
Perform a repository health check:
1. Stale branches: list branches with no commits in >30 days
2. PR hygiene: open PRs older than 7 days without activity
3. CI health: check last 10 CI runs for flaky or consistently failing tests
4. Issue backlog: count open issues, flag any without labels or assignees
5. README accuracy: verify install commands actually work
6. License compliance: check all dependencies have compatible licenses

Post results to #engineering in Slack as a structured report.
Recommend specific actions for each finding.
```

**Why it works:** Small hygiene problems compound into major drag if left unaddressed. A weekly sweep keeps the repository in working order.

---

## CI Failure Analyst

**Schedule:** Daily at 7:00 AM UTC  
**Connectors:** GitHub, Slack  
**Use case:** Categorize CI failures so the team knows what to fix vs. what to ignore.

```
Analyze all CI failures from the past 24 hours.
For each failure:
  - Categorize as: flaky test / real failure / infra issue / timeout
  - Identify the likely commit or PR that caused it
  - For flaky tests: note how many times it has flaked in the past week

Post a summary to #ci-health in Slack:
- Real failures needing attention (with links)
- Flaky tests ranked by frequency
- Infrastructure issues (if any)

If no failures in the past 24 hours, post "CI is green" and exit.
```

**Why it works:** Teams waste hours investigating flaky tests that they've already seen. This routine classifies failures and tracks flake frequency.

---

## Stale TODO Janitor

**Schedule:** Every Monday at 6:00 AM UTC  
**Connectors:** GitHub  
**Use case:** Prevent TODO/FIXME comments from becoming permanent fixtures.

```
Scan the codebase for TODO, FIXME, HACK, and XXX comments.
For each one:
  - Determine the age using git blame
  - Check if it references an issue number and whether that issue is still open
  - Classify as: actionable / orphaned / outdated

For orphaned or outdated items (>90 days old with no linked issue):
  - Open a GitHub issue with the comment text, file location, and original author
  - Tag with "tech-debt" label

Post a summary: N total TODOs, N orphaned, N issues created.
```

**Why it works:** TODOs without tracking become invisible. This routine surfaces them as actual issues that can be prioritized.

---

## Performance Regression Detector

**Schedule:** Daily at 1:00 AM UTC  
**Connectors:** GitHub  
**Use case:** Catch performance regressions before they reach users.

```
Run the project's test suite and performance benchmarks.
Compare results against the baseline in performance-baseline.json
(create it if it doesn't exist).
Flag any test that:
  - Increased execution time by more than 20%
  - Reduced test coverage below the threshold
  - Introduced new flaky behavior (passed then failed on retry)

If regressions are found, open a GitHub issue with specific benchmarks
and the commits that likely caused the regression.
Update performance-baseline.json with current results on a claude/ branch.
```

**Why it works:** Performance regressions are invisible until they're severe. Nightly comparison against a baseline catches them early.

---

## Feature Flag Cleanup

**Trigger:** One-time, scheduled 2 weeks after a feature ships  
**Connectors:** GitHub  
**Use case:** Remove feature flags once the rollout is stable.

```
Check if the feature flag [FLAG_NAME] is still in the codebase.
If it is:
  - List all files that reference it
  - Determine if the flag is still gated or fully rolled out
  - If fully rolled out: open a PR removing the flag and all conditional paths
  - If still gated: report the current state and exit

Do not merge the PR. Only push to a claude/ branch.
```

**Why it works:** Feature flags left behind after rollout add permanent complexity. A scheduled cleanup prevents accumulation.

---

## Nightly Bug Fixer

**Schedule:** Daily at 2:00 AM  
**Connectors:** GitHub  
**Use case:** Make progress on the bug backlog overnight.

```
Pull the highest-priority open bug from GitHub issues (label: "bug",
sorted by reactions or priority label).
Attempt to reproduce and fix the bug:
1. Read the issue description and any linked error logs
2. Identify the root cause in the code
3. Implement a fix
4. Write a regression test
5. Open a draft PR linking the issue

If the bug cannot be reproduced or the fix is unclear:
  - Add a comment to the issue explaining what was tried
  - Do NOT open a PR

Do not merge any PRs. Only push to claude/ branches.
```

**Why it works:** Bug backlogs grow because fixing bugs competes with feature work. A nightly agent chips away at the backlog without occupying developer time.

---

## Morning Briefing

**Schedule:** Daily at 7:00 AM  
**Connectors:** Slack, GitHub  
**Use case:** Start the day with a structured overview of what matters.

```
Compile a morning briefing:
1. PRs that need my review (assigned to me or my team)
2. PRs I authored that have new comments or approvals
3. Issues assigned to me with approaching deadlines
4. CI status: any failing builds on main?
5. Mentions: any GitHub @mentions I haven't responded to

Format as a concise digest with links.
Post to my DM in Slack.

If nothing actionable, post "Clear morning - no blockers" and exit.
```

**Why it works:** Replaces the morning ritual of checking GitHub, Slack, and email separately. Surfaces only items that need attention.

---

## Best Practices

These patterns come from the community and Anthropic's own documentation:

### Prompt Design

1. **Handle empty states** — always include "If nothing to report, post X and exit" to avoid confusing empty outputs
2. **Specify output destinations** — "Post to #releases in Slack" or "Open a PR against the docs repo"
3. **Use negative constraints** — "Do not merge any PRs. Do not push to main. Only push to claude/ branches"
4. **Be explicit about success criteria** — "run npm audit, filter for severity high or critical"

### Operational

5. **Start with weekly cadences** and tighten to daily only after calibrating the prompt
6. **Review the first few outputs** carefully to calibrate prompt quality before trusting unattended
7. **Scope access narrowly** — only give the routine the repos, connectors, and network access it needs
8. **Design for failure** — routines can timeout, hit rate limits, or encounter unexpected states

### Limits

- Daily run caps: Pro = 5, Max = 15, Team/Enterprise = 25
- Outbound HTTP from cloud environment is restricted (use GitHub Actions as a bridge for custom webhooks)
- Routines can be created via `/schedule` in CLI, the Desktop app, or `claude.ai/code/routines`

---

## Resources

- [Automate work with routines — Claude Code Docs](https://code.claude.com/docs/en/routines)
- [Introducing routines in Claude Code](https://claude.com/blog/introducing-routines-in-claude-code)
- [anthropics/claude-code-action](https://github.com/anthropics/claude-code-action) — GitHub Actions integration
- [claude-code-workflows](https://github.com/OneRedOak/claude-code-workflows) — Community workflow patterns
- [ksimback/tech-debt-skill](https://github.com/ksimback/tech-debt-skill) — Tech debt audit skill
