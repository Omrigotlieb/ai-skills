# Claude Code Routines & Scheduled Agents

Routines are scheduled agents that run autonomously on a cron schedule or at a specific time. They handle recurring maintenance, monitoring, and housekeeping tasks so you can focus on feature work.

> **Feature:** `/schedule` command | **Docs:** [Routines Documentation](https://code.claude.com/docs/en/routines)

## Quick Start

```bash
# Create a routine interactively
/schedule

# Or describe what you want
"Schedule a weekly dependency audit every Monday at 9am"
```

Claude Code creates a remote agent that runs on the specified schedule, executes its prompt against your repository, and can open PRs, post to Slack, or send email summaries.

---

## How Routines Work

1. **You describe the task** — what to do, when, and how to report results
2. **Claude creates a scheduled agent** — runs remotely on Anthropic's infrastructure
3. **The agent executes on schedule** — clones your repo, runs the prompt, takes action
4. **You get notified** — via email, Slack, PR, or however the routine is configured

### Key Properties

| Property | Description |
|----------|-------------|
| **Schedule** | Cron expression or one-time datetime |
| **Prompt** | Instructions for the agent |
| **Repository** | Git repo the agent operates on |
| **Permissions** | What the agent can do (read, write, PR, push) |
| **Notifications** | How results are delivered |

---

## Routine Catalog

### Daily Routines

#### Morning Standup Digest
Generate a daily summary of repository activity, open PRs, and CI status.

**Schedule:** `0 8 * * 1-5` (weekdays at 8am)

```
Review the repository and create a morning digest:

1. List PRs opened, merged, or updated in the last 24 hours
2. Summarize any CI/CD failures on main
3. List open issues labeled "urgent" or "bug"
4. Note any dependency security advisories from Dependabot or Renovate
5. Check for stale PRs (open > 7 days with no review)

Format as a concise Slack-ready message with sections. Send to #engineering-standup.
```

**Why this works:** Eliminates the 10 minutes every morning spent checking GitHub notifications, CI dashboards, and PR queues. The team gets a single digestible update.

---

#### PR Review Reminder
Nudge reviewers on PRs that have been waiting too long.

**Schedule:** `0 10 * * 1-5` (weekdays at 10am)

```
Check all open pull requests in this repository:

1. Find PRs with no review activity in the last 48 hours
2. For each, identify the requested reviewers
3. Post a polite reminder comment tagging the reviewers
4. If a PR has been open > 5 business days, escalate by also commenting with "@team-lead"

Do NOT comment on draft PRs or PRs labeled "on-hold".
```

---

#### Flaky Test Monitor
Track and report on flaky tests before they erode CI trust.

**Schedule:** `0 9 * * 1-5` (weekdays at 9am)

```
Analyze CI runs from the last 24 hours:

1. Identify tests that passed on retry but failed initially
2. Group by test file and count failure frequency
3. If any test has failed > 3 times this week, open an issue titled "Flaky test: [test name]"
4. Include the failure logs and a suggested investigation path

Label issues with "flaky-test" and "tech-debt".
```

---

### Weekly Routines

#### Dependency Audit
Keep dependencies current and secure.

**Schedule:** `0 9 * * 1` (Monday at 9am)

```
Audit project dependencies:

1. Run the package manager's audit command (npm audit / pip audit / cargo audit)
2. List all vulnerabilities by severity (critical, high, medium, low)
3. For critical and high: check if a patched version exists and is compatible
4. For outdated dependencies (> 2 major versions behind): note the migration effort
5. If safe updates are available, open a PR that bumps patch/minor versions

Title the PR "chore: weekly dependency updates [date]".
Include a summary table of what was updated and why.
Do NOT bump major versions without flagging them for manual review.
```

**Why this works:** Most teams neglect dependency updates until a security advisory forces them. A weekly routine keeps the backlog small and catches vulnerabilities early.

---

#### Dead Code & TODO Sweep
Surface technical debt before it compounds.

**Schedule:** `0 10 * * 3` (Wednesday at 10am)

```
Scan the codebase for technical debt indicators:

1. Find TODO, FIXME, HACK, and XXX comments
2. Check if any reference issues that have been closed
3. Look for unused exports (functions, types, constants exported but never imported)
4. Find files not modified in the last 6 months that are still imported
5. Check for commented-out code blocks > 5 lines

Create a summary report. If actionable items are found, open a single issue titled
"Tech debt sweep [date]" with a prioritized list.
Do NOT open PRs to fix these — just surface them for the team.
```

---

#### Changelog & Release Notes Draft
Prepare release communication automatically.

**Schedule:** `0 14 * * 5` (Friday at 2pm)

```
Prepare a draft changelog for this week's changes:

1. Gather all commits merged to main since last Friday
2. Group by conventional commit type (feat, fix, chore, docs, refactor)
3. Write user-facing release notes for features and fixes
4. Flag any breaking changes prominently
5. Note any new dependencies added

Create a draft PR adding the entry to CHANGELOG.md.
Title: "docs: changelog for week of [date]"
```

---

#### Documentation Freshness Check
Prevent docs from rotting silently.

**Schedule:** `0 11 * * 2` (Tuesday at 11am)

```
Check documentation freshness:

1. Compare README.md setup instructions against actual project config
2. Verify that documented API endpoints match the route definitions in code
3. Check that documented environment variables match what the code reads
4. Look for references to renamed or deleted files/functions
5. Verify external links are not returning 404

If stale docs are found, open a PR with fixes for straightforward issues.
For ambiguous cases, open an issue describing what looks outdated.
```

---

### Bi-Weekly / Monthly Routines

#### Security Posture Review
Comprehensive security check beyond dependency scanning.

**Schedule:** `0 9 1,15 * *` (1st and 15th of each month at 9am)

```
Perform a security posture review:

1. Check for hardcoded secrets, API keys, or tokens (scan all file types)
2. Review .env.example — are all required vars documented?
3. Audit authentication and authorization middleware for common issues
4. Check that CORS, CSP, and other security headers are configured
5. Review database queries for SQL injection potential
6. Check that user input validation exists at API boundaries

Open an issue with findings organized by severity.
Title: "Security review [date]"
Label: "security"
```

---

#### Architecture Drift Check
Detect when the code diverges from intended architecture.

**Schedule:** `0 10 1 * *` (first of each month at 10am)

```
Check for architecture drift:

1. Verify the dependency graph matches the intended layer structure
   (e.g., controllers → services → repositories, no reverse dependencies)
2. Look for circular imports
3. Check that new files follow the established directory conventions
4. Identify modules that have grown unusually large (> 500 lines)
5. Flag any new direct database access outside the data layer

Create a summary report as a GitHub issue.
Title: "Architecture review [date]"
```

---

#### Feature Flag Cleanup
Remove stale feature flags that were fully rolled out.

**Schedule:** `0 10 1 * *` (first of each month at 10am)

```
Audit feature flags in the codebase:

1. Find all feature flag references (check for common patterns: isEnabled, featureFlag,
   LaunchDarkly, Unleash, environment-based toggles)
2. For each flag, check if it's always returning the same value in production config
3. If a flag has been fully enabled for > 30 days, open a PR to remove it and
   the dead code path
4. If a flag has been fully disabled for > 30 days, flag it for deletion review

Title PRs: "chore: remove fully-rolled-out flag [flag-name]"
```

---

#### Performance Baseline Comparison
Track performance trends over time.

**Schedule:** `0 6 * * 1` (Monday at 6am)

```
Run performance baseline checks:

1. Execute the project's benchmark suite (if one exists)
2. Compare results against the last recorded baseline
3. Flag any metric that regressed > 10% from the previous week
4. If no benchmark suite exists, analyze bundle size (for frontend) or
   startup time (for backend) as proxy metrics
5. Update the baseline file with current results

If regressions are found, open an issue with before/after comparison.
Title: "Performance regression detected [date]"
```

---

### One-Time Routines

These are triggered once for specific events, not on a recurring schedule.

#### Post-Release Soak Check
Verify a release is healthy after deployment.

**Schedule:** One-time, 2 hours after deploy

```
Check the health of the latest release:

1. Verify the deployment succeeded (check CI/CD status)
2. Review error rates in the last 2 hours vs. the prior 2-hour window
3. Check for any new error types appearing in logs
4. Verify key API endpoints are responding with expected status codes
5. Check that database migration completed successfully

Send a summary email. If error rates increased > 20%, flag as urgent.
```

---

#### Migration Verification
Confirm a database migration landed correctly.

**Schedule:** One-time, 1 hour after migration

```
Verify the database migration completed correctly:

1. Check that all new tables/columns exist with correct types
2. Verify indexes were created as specified
3. Confirm data backfill completed (if applicable)
4. Run a sample of queries that exercise the new schema
5. Check for any orphaned data or constraint violations

Report results via email. Flag any discrepancies as critical.
```

---

## Building Effective Routine Prompts

### Structure

Every good routine prompt follows this pattern:

```
[What to check/do — numbered steps]
[How to report results — format and channel]
[Guard rails — what NOT to do]
```

### Tips

1. **Be specific about actions** — "open a PR" vs. "fix the issue" vs. "open an issue" vs. "send a message"
2. **Set boundaries** — always include what the routine should NOT do
3. **Specify output format** — Slack message, email, PR, issue, or report file
4. **Include severity thresholds** — "flag if > 10% regression" is better than "flag if slow"
5. **Reference specific files** — "check `src/config/flags.ts`" beats "find feature flags"
6. **Test manually first** — run the prompt once interactively before scheduling

### Anti-Patterns

| Anti-Pattern | Problem | Fix |
|---|---|---|
| "Fix all bugs" | Unbounded scope, risky changes | "Open issues for bugs found" |
| "Update everything" | Major version bumps break things | "Bump patch/minor only, flag major" |
| "Refactor the codebase" | Too broad, no clear completion | "Identify top 5 refactor targets" |
| No guard rails | Agent might push breaking changes | Always include "Do NOT merge without review" |
| Vague schedule | Runs too often or too rarely | Match cadence to how fast the signal changes |

---

## Managing Routines

```bash
# List all active routines
/schedule list

# Update an existing routine
/schedule update <routine-id>

# Pause a routine
/schedule pause <routine-id>

# Delete a routine
/schedule delete <routine-id>

# Run a routine immediately (for testing)
/schedule run <routine-id>
```

---

## Composing a Daily Schedule

Here's a battle-tested daily schedule combining multiple routines:

| Time | Routine | Purpose |
|------|---------|---------|
| **6:00 AM** | Performance baseline | Catch regressions before the team arrives |
| **8:00 AM** | Standup digest | Morning overview of repo activity |
| **9:00 AM** | Flaky test monitor | Surface CI reliability issues |
| **10:00 AM** | PR review reminder | Keep reviews moving |
| **2:00 PM** | Stale branch cleanup | Housekeeping |
| **Monday 9 AM** | Dependency audit | Start the week with a clean bill of health |
| **Tuesday 11 AM** | Docs freshness check | Catch documentation rot |
| **Wednesday 10 AM** | Dead code & TODO sweep | Surface tech debt mid-week |
| **Friday 2 PM** | Changelog draft | End the week with release notes ready |
| **1st of month** | Security posture review | Monthly deep security scan |
| **1st of month** | Architecture drift check | Monthly structure validation |
| **1st of month** | Feature flag cleanup | Remove stale flags |

### Starter Kit

Start with just three routines and add more as you see value:

1. **Morning standup digest** — immediate daily value
2. **Weekly dependency audit** — catches security issues early
3. **PR review reminder** — keeps the team shipping

---

## Community Routine Ideas

Collected from GitHub discussions, Reddit r/ClaudeAI, and practitioner blogs:

| Routine | Source | Schedule |
|---------|--------|----------|
| Auto-label new issues based on content | GitHub community | On issue creation |
| Weekly metrics dashboard generation | r/ClaudeAI | Weekly |
| Sprint retrospective data gathering | Agile teams | Bi-weekly |
| License compliance scanning | OSS maintainers | Monthly |
| API contract drift detection | Backend teams | Weekly |
| Accessibility audit on UI changes | Frontend teams | On PR to UI dirs |
| Infrastructure cost anomaly detection | DevOps teams | Daily |
| Onboarding doc verification | Growing teams | Monthly |
| Competitive feature tracking | Product teams | Weekly |
| Release readiness checklist | Release managers | Before each release |

---

## Resources

### Official
- [Routines Documentation](https://code.claude.com/docs/en/routines)
- [Scheduled Tasks Guide](https://code.claude.com/docs/en/scheduled-tasks)
- [Claude Code Best Practices](https://www.anthropic.com/engineering/claude-code-best-practices)

### Community
- [r/ClaudeAI](https://reddit.com/r/ClaudeAI) — Community discussions on automation
- [awesome-claude-code](https://github.com/hesreallyhim/awesome-claude-code) — Curated tools and patterns
- [claude-code-workflows](https://github.com/OneRedOak/claude-code-workflows) — Workflow automation patterns
