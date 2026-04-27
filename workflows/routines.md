# Routines & Scheduled Tasks

Automated routines that run on a schedule so your codebase stays healthy without manual effort. Claude Code supports three scheduling tiers; pick the one that fits your setup.

## Scheduling Tiers

| Tier | Runs on | Machine required | Session required | Min interval |
|---|---|---|---|---|
| **Cloud Routines** | Anthropic cloud | No | No | 1 hour |
| **Desktop Scheduled Tasks** | Your machine | Yes | No | 1 minute |
| **`/loop` (in-session)** | Your machine | Yes | Yes | 1 minute |

Cloud Routines support three trigger types: **scheduled** (cron), **API** (HTTP POST), and **GitHub events** (PR opened, releases, etc.). A single routine can combine all three.

> Plan caps: Pro 5/day, Max 15/day, Team/Enterprise 25/day. One-off runs and webhook/API triggers do not count.

---

## Daily Routines

### Morning PR Digest

**Schedule:** Daily at 8:00 AM  
**Purpose:** Start the day knowing what landed, what's in flight, and what's stuck.

```
Read all open PRs and recent commits. Post a Slack message with:
- What landed yesterday
- What's in flight (open PRs with recent activity)
- Anything blocked or stale (PRs older than 3 days with no review)
Keep it under 10 lines. Do NOT approve or merge any PR.
```

**Trigger type:** Cloud Routine (scheduled) or Desktop Scheduled Task  
**Connectors:** GitHub, Slack

---

### Daily Security Scan

**Schedule:** Daily at 8:00 AM  
**Purpose:** Catch sensitive data, dependency vulnerabilities, and risky patterns before they reach production.

```
Scan all commits pushed in the last 24 hours for:
- Hardcoded secrets, API keys, or credentials
- New dependencies with known CVEs
- SQL injection, XSS, or command injection patterns

Create a GitHub issue listing findings by severity (critical/high/medium).
If nothing found, skip the issue. Do NOT modify any code.
```

**Trigger type:** Cloud Routine (scheduled)  
**Connectors:** GitHub

---

### Error Log Analysis

**Schedule:** Daily at 7:00 AM  
**Purpose:** Surface overnight errors before the team starts work.

```
Analyze application logs from the last 24 hours.
- Count ERROR and FATAL entries; compare to 7-day average
- Identify any new error types not seen before this week
- Flag error spikes (>2x the daily average)

Post a summary to #engineering-alerts. Include top 5 errors by frequency.
Do NOT open fix PRs automatically.
```

**Trigger type:** Cloud Routine (scheduled)  
**Connectors:** Logging service, Slack

---

### Documentation Sync Check

**Schedule:** Daily at 10:00 AM  
**Purpose:** Catch docs that have drifted from the code they describe.

```
Compare README.md and docs/ with the actual codebase.
Flag any documentation that:
- References functions, endpoints, or config keys that no longer exist
- Shows installation steps that don't match the current package.json/requirements
- Contains example code that would fail against the current API

Report findings as a checklist. Do NOT edit docs directly.
```

**Trigger type:** Cloud Routine (scheduled) or Desktop Scheduled Task  
**Connectors:** GitHub

---

## Event-Triggered Routines

### PR Code Review

**Trigger:** `pull_request.opened`  
**Purpose:** Immediate feedback on every new PR, applying your team's standards.

```
Review the PR carefully and post a comment with:
1. A one-line summary of what the PR changes
2. Any potential bugs, edge cases, or security concerns
3. Suggestions for improvement (if any)
4. A clear verdict: ready to merge, needs changes, or blocking issue

Apply the project's coding standards from CLAUDE.md.
Do NOT approve or merge the PR.
```

**Trigger type:** Cloud Routine (GitHub event)  
**Connectors:** GitHub

---

### Deploy Verification

**Trigger:** API endpoint called by CD pipeline after production deploy  
**Purpose:** Automated smoke test to catch deploy regressions.

```
Run smoke checks against the new build:
- Hit health check endpoints and verify 200 responses
- Scan error logs for new errors in the last 5 minutes
- Compare response times to pre-deploy baseline

Post go/no-go status to #releases. If critical failures detected,
include the error details and recent commit that likely caused it.
```

**Trigger type:** Cloud Routine (API trigger)  
**Connectors:** Monitoring service, Slack

---

### Alert Triage

**Trigger:** API endpoint called by monitoring when error threshold is crossed  
**Purpose:** Correlate alerts with recent changes and accelerate response.

```
Pull the stack trace from the alert payload.
Correlate with commits from the last 24 hours.
Identify the most likely causal commit.
Post analysis to #oncall with:
- Stack trace summary
- Suspected commit and author
- Suggested investigation steps

Do NOT open PRs or revert commits automatically.
```

**Trigger type:** Cloud Routine (API trigger)  
**Connectors:** Monitoring service, GitHub, Slack

---

## Weekly Routines

### Dependency Update Check

**Schedule:** Every Monday at 7:00 AM  
**Purpose:** Stay current on dependencies without surprise breakage.

```
Check for outdated packages in the project.
For each outdated dependency:
- Note the current vs latest version
- Flag whether it's a major/minor/patch bump
- Check for known security advisories
- Note breaking changes from the changelog

Post a summary to #engineering. For security-critical updates,
open a GitHub issue with the "security" label.
Do NOT auto-upgrade or open PRs.
```

**Trigger type:** Cloud Routine (scheduled)  
**Connectors:** GitHub, Slack

---

### Stale Branch Cleanup

**Schedule:** Every Friday at 5:00 PM  
**Purpose:** Keep the repository tidy by surfacing abandoned work.

```
List all branches in the repository.
Identify:
- Branches already merged to main (safe to delete)
- Unmerged branches with no commits in 30+ days

For merged branches: delete them.
For stale unmerged branches: open a GitHub issue tagging the branch author,
asking whether the work should be continued or the branch deleted.
```

**Trigger type:** Cloud Routine (scheduled) or Desktop Scheduled Task  
**Connectors:** GitHub

---

### Code Complexity Trend

**Schedule:** Every Monday at 8:00 AM  
**Purpose:** Catch architectural drift before it becomes tech debt.

```
Analyze the codebase for complexity trends:
- Identify files with the highest cyclomatic complexity
- Compare this week's metrics to last week's
- Flag any file where complexity increased by >20%
- List the top 5 most complex functions

Post the report to #engineering. Do NOT refactor anything.
```

**Trigger type:** Cloud Routine (scheduled)  
**Connectors:** GitHub, Slack

---

### Weekly Changelog Generation

**Schedule:** Every Friday at 4:00 PM  
**Purpose:** Automated release notes from the week's merged PRs.

```
Read all PRs merged to main this week.
Categorize each into: Feature, Fix, Chore, Docs.
Generate a formatted changelog entry following Keep a Changelog format.

Post the draft to #releases for review. Do NOT commit to the repository.
```

**Trigger type:** Cloud Routine (scheduled)  
**Connectors:** GitHub, Slack

---

### Test Coverage Report

**Schedule:** Every Monday at 9:00 AM  
**Purpose:** Track coverage trends and prevent regression.

```
Run the test suite with coverage enabled.
Compare coverage to last week's baseline.
Flag:
- Any module that dropped below 80% coverage
- New files with zero test coverage
- Coverage trend (improving/declining/stable)

Post results to #engineering with the coverage delta.
```

**Trigger type:** Desktop Scheduled Task  
**Connectors:** GitHub, Slack

---

## The `/loop` Pattern

For in-session maintenance, the `/loop` command runs a repeating task while you work. Customize it with a `.claude/loop.md` file.

### Default behavior (no loop.md)

- Continues unfinished work from the conversation
- Tends the current branch's PR: review comments, failed CI, merge conflicts
- Runs cleanup passes when nothing else is pending

### Custom loop.md example

Place at `.claude/loop.md` (project) or `~/.claude/loop.md` (user):

```markdown
Check the `release/next` PR. If CI is red, pull the failing job log,
diagnose, and push a minimal fix. If new review comments have arrived,
address each one and resolve the thread. If everything is green and
quiet, say so in one line.
```

### Babysit PRs loop

```
/loop 5m Review all open PRs on this repo. For each:
- Check CI status
- Respond to new review comments
- Flag merge conflicts
Report only changes since last check.
```

---

## Writing Effective Routine Prompts

### Do

- **Be explicit about outputs.** "Post a Slack message to #channel" beats "notify the team."
- **Include guardrails.** Every routine should state what it must NOT do: "Do NOT merge," "Do NOT edit files."
- **Specify scope.** "Commits from the last 24 hours" is better than "recent commits."
- **Define thresholds.** "Flag if >2x daily average" prevents noise on normal fluctuations.
- **State the format.** "Bulleted list under 10 lines" keeps outputs consistent.

### Don't

- Don't omit "Do NOT" boundaries — routines run autonomously and will take any action the prompt allows.
- Don't use vague time references — "yesterday" is ambiguous across timezones; prefer "last 24 hours."
- Don't skip the connector list — routines need explicit access to each service they touch.
- Don't assume context — the routine starts fresh each run with no memory of previous executions.

---

## Resources

- [Cloud Routines documentation](https://code.claude.com/docs/en/routines)
- [Desktop Scheduled Tasks documentation](https://code.claude.com/docs/en/desktop-scheduled-tasks)
- [Scheduled Tasks overview](https://code.claude.com/docs/en/scheduled-tasks)
