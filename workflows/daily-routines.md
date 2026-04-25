# Daily Routines for Claude Code

Automated routines that run on a schedule to keep your codebase, team, and workflow healthy. Each routine includes a copy-ready prompt, recommended schedule, and required connectors.

> **Scheduling surfaces:** Cloud Routines (runs on Anthropic's cloud, no machine needed), Desktop Scheduled Tasks (local, requires app open), and `/loop` (in-session polling). See [official docs](https://code.claude.com/docs/en/routines) for setup.

## Quick Navigation

- [Recommended Daily Schedule](#recommended-daily-schedule)
- [Morning Routines](#morning-routines)
- [Continuous Routines](#continuous-routines)
- [Evening Routines](#evening-routines)
- [Weekly Routines](#weekly-routines)
- [Event-Driven Routines](#event-driven-routines)
- [Writing Good Routine Prompts](#writing-good-routine-prompts)

---

## Recommended Daily Schedule

| Time | Routine | Trigger | Purpose |
|------|---------|---------|---------|
| 2:00 AM | [Dependency Audit](#dependency-audit) | Schedule | Check for CVEs, open issues for critical vulnerabilities |
| 2:30 AM | [Branch Cleanup](#branch-cleanup) | Schedule | Delete merged and stale branches |
| 3:00 AM | [Security Scan](#security-scan) | Schedule | Scan for secrets, container issues, dependency vulns |
| 7:00 AM | [Morning Briefing](#morning-briefing) | Schedule | Pull calendar, Slack, email into one structured overview |
| 9:00 AM | [Backlog Triage](#backlog-triage) | Schedule | Label, assign, and summarize new issues |
| On PR | [Automated Code Review](#automated-code-review) | GitHub event | Run team checklist, leave inline comments |
| On deploy | [Deploy Verification](#deploy-verification) | API trigger | Smoke tests, error scan, go/no-go verdict |
| 5:00 PM | [End-of-Day Digest](#end-of-day-digest) | Schedule | Summarize merges, blockers, tomorrow's priorities |
| Friday 4 PM | [Documentation Drift Check](#documentation-drift-check) | Schedule (weekly) | Find code/docs mismatches |
| Monday 9 AM | [Weekly Report](#weekly-report) | Schedule (weekly) | PR stats, velocity, incident summary |

---

## Morning Routines

### Morning Briefing

**Schedule:** Weekdays at 7:00 AM
**Connectors:** Gmail, Google Calendar, Slack, Notion (optional)

The single most impactful routine to start with. Pulls from multiple sources into one structured overview so you start the day with full context.

```
I need my morning briefing. Pull from Slack and email, check my calendar,
and visit my team dashboard.

Structure it as:
- Urgent items: anything red or trending down
- Slack threads where I'm mentioned — read the full threads for context
- Threads I'm not in but should know about based on my current projects
- Today's calendar: for each meeting, one sentence on what it's about
  and one thing I should prepare
- Tasks due this week and anything blocking them

For urgent items, pull deeper context: who's involved, what's been
discussed, what's still unresolved.

If nothing is urgent, say so in one line and skip to the schedule.
```

**Source:** [Anthropic — Build a daily briefing](https://claude.com/resources/use-cases/build-a-daily-briefing-across-your-tools)

---

### Backlog Triage

**Schedule:** Weekdays at 9:00 AM
**Connectors:** GitHub, Slack

```
Read all GitHub issues opened since this routine last ran in {org}/{repo}.

For each issue:
1. Apply one label from [bug, feature, docs, question, needs-triage]
2. Assign based on files referenced and our CODEOWNERS file
3. If the issue is unclear, comment asking the author for reproduction steps

Post a summary to #dev-standup with count and breakdown by label.
Use bullet points. If zero issues were filed, post a single line saying so.
```

---

## Continuous Routines

### Automated Code Review

**Trigger:** GitHub event — `pull_request.opened`
**Connectors:** GitHub (Claude GitHub App)

The highest-ROI event-driven routine. Shifts human reviewers from mechanical checks to design decisions.

```
Review this pull request against our team standards.

Check for:
- Security: hardcoded secrets, SQL injection, unvalidated inputs,
  new dependency CVEs
- Performance: N+1 queries, missing indexes, synchronous operations
  that should be async, unbounded loops
- Style: linting compliance, naming consistency, dead code,
  TODOs without issue links
- Tests: coverage for new code paths, edge cases, error paths

Leave an inline comment on each specific issue found. Give the line
number and the specific fix, not vague observations.

Add a summary comment with:
- pass/fail status
- count of issues by severity (critical/high/medium/low)
- one sentence on the overall quality

Do not approve or merge. Only comment.
```

**Source:** [Builder.io — Claude Code Routines Tutorial](https://www.builder.io/blog/claude-code-routines)

---

### Deploy Verification

**Trigger:** API (called from CD pipeline after deploy)
**Connectors:** GitHub, Slack, monitoring/logging access

```
A deploy just completed. Verify it:

1. Run smoke tests from tests/smoke/
2. Check production logs for new error patterns in the last 10 minutes
3. Compare error rates before and after deploy
4. Check response times for key endpoints

Post results to #deploys with a go/no-go verdict.

If failures found, open GitHub issues tagged @oncall with:
- the stack trace
- correlated recent commits
- suggested rollback steps

If everything is clean, post a single green-status message.
```

Fire via API:
```bash
curl -X POST https://api.anthropic.com/v1/claude_code/routines/{trigger_id}/fire \
  -H "Authorization: Bearer $ANTHROPIC_API_KEY" \
  -H "anthropic-beta: experimental-cc-routine-2026-04-01" \
  -H "anthropic-version: 2023-06-01" \
  -H "Content-Type: application/json" \
  -d '{"text": "Deploy v2.4.1 completed. Environment: production."}'
```

---

### Stale PR Detection

**Trigger:** Schedule (daily) or every 3 hours
**Connectors:** GitHub, Slack

```
Fetch open pull requests in {org}.

For PRs open more than 3 days with no reviewer activity:
- List PR title, author, days open, and requested reviewers
- Post to #code-review on Slack

For PRs open more than 7 days:
- Add a comment on the PR asking for a status update

Keep the Slack message concise. Use bullet points.
If all PRs are actively reviewed, post one line saying so.
```

---

## Evening Routines

### End-of-Day Digest

**Schedule:** Weekdays at 5:00 PM
**Connectors:** GitHub, Slack

```
Compile today's engineering digest:

1. PRs merged today — list titles, authors, and key changes
2. Issues closed — count and notable ones
3. New issues opened — flag any critical/urgent
4. Deploys — count and any incidents
5. Blockers — anything stalled or waiting on external input
6. Tomorrow's priorities — based on sprint board and due dates

Post to #engineering-daily. Format for Slack: bullet points,
no horizontal rules (they cause rendering errors).
If it was a quiet day, say so in two lines.
```

---

### Dependency Audit

**Schedule:** Daily at 2:00 AM UTC
**Connectors:** GitHub

```
Run dependency audits on all package manifests in this repository.

For each vulnerability with severity high or critical:
1. Check if a tracking issue already exists
2. If not, open a GitHub issue with: CVE ID, affected package,
   current version, fixed version, and upgrade path
3. Label all issues "security" and "dependencies"

For moderate vulnerabilities, add them to a single summary issue
updated weekly.

Do not merge any PRs. Do not push to main. Only push to claude/ branches.
```

**Source:** [ComputingForGeeks — Setup Guide](https://computingforgeeks.com/claude-code-routines-setup/)

---

### Security Scan

**Schedule:** Daily at 3:00 AM UTC
**Connectors:** GitHub, Docker access (optional)

```
Run a comprehensive security sweep:

1. Dependency audit: check for known CVEs in all package manifests
2. Secrets scan: search for API keys, tokens, passwords, and
   connection strings in source files (not .env.example)
3. Container scan: check Dockerfiles for running as root,
   using :latest tags, or exposing unnecessary ports
4. Permission review: flag any files with overly broad permissions

Open GitHub issues with remediation steps for high/critical findings.
Label all issues "security".

Do not push to main. Only push to claude/ branches.
```

---

### Branch Cleanup

**Schedule:** Daily at 2:30 AM
**Connectors:** GitHub

```
Clean up stale branches:

1. List branches merged to main more than 7 days ago — delete them
2. List branches with no commits in the last 30 days — report but
   don't delete (they may be someone's WIP)
3. Report branch count before and after cleanup

Post results to #engineering-ops.
Do not delete branches with open PRs.
Do not delete protected branches.
```

---

## Weekly Routines

### Documentation Drift Check

**Schedule:** Fridays at 4:00 PM
**Connectors:** GitHub

```
Scan all PRs merged since last Monday.

For each PR that changed files in src/api/ or src/config/:
1. Check if corresponding docs in docs/ or README.md were also updated
2. If documentation is stale relative to the code changes,
   open a PR on a claude/ branch with suggested updates

List all stale docs found and their corresponding code changes.
Do not merge any PRs. Do not push to main.
```

---

### Weekly Report

**Schedule:** Fridays at 4:00 PM (or Mondays at 9:00 AM)
**Connectors:** GitHub, Slack

```
Compile the weekly engineering report:

- PRs merged: count, authors, average review time
- Issues closed vs opened: net change
- Deployment count and any incidents
- Test coverage delta (if CI reports coverage)
- Top 3 contributors by PR count

Format as a Slack-friendly summary. Post to #engineering-weekly.
Keep it under 20 lines.
```

---

### Tech Debt Tracking

**Schedule:** Weekly (Mondays)
**Connectors:** GitHub

```
Scan the codebase for TODO, FIXME, HACK, and XXX comments.

For each one added in the last 7 days (check git blame):
1. Create a GitHub issue with file path, line number, comment text,
   and the author who added it
2. Label with "tech-debt"

For existing TODOs older than 90 days:
- Add a comment to their tracking issue asking if still relevant

Post a summary to #engineering with total count by age bracket:
<7 days, 7-30 days, 30-90 days, >90 days.
```

---

### Feature Flag Cleanup

**Schedule:** Weekly or one-off (2 weeks after rollout)
**Connectors:** GitHub, feature flag service

```
Check for feature flags that have been at 100% rollout for more than
14 days.

For each one:
1. Open a cleanup PR that removes the flag, all conditional branches,
   and the flag definition
2. Update tests that reference the flag
3. Push to a claude/ branch

Do not merge. Do not push to main.
```

---

## Event-Driven Routines

### Release Notes Generation

**Trigger:** GitHub event — `release.published`
**Connectors:** GitHub

```
A new release was just tagged.

1. Summarize all commits and merged PRs since the last release tag
2. Group by category: Features, Bug Fixes, Performance,
   Documentation, Breaking Changes
3. Write user-facing release notes in markdown
4. Update CHANGELOG.md

Push to a claude/ branch. Do not merge.
```

---

### Error Log Monitoring

**Trigger:** Schedule (hourly) or API
**Connectors:** Logging service, GitHub, Sentry (optional)

```
Check error logs from the last hour.

1. Filter out known false positives and transient errors
2. For each new error pattern:
   - Correlate with recent commits
   - Identify likely root cause
   - Open a draft PR with a proposed fix if straightforward
3. If error rate exceeds baseline by 2x, post an alert to #incidents

Do not merge any PRs.
```

---

### Nightly Bug Fix Attempt

**Trigger:** Schedule — 2:00 AM
**Connectors:** GitHub Issues or Linear, GitHub

```
Pull the top bug from the issue tracker sorted by priority.

1. Attempt to reproduce and understand the bug
2. If the fix is straightforward (touches fewer than 3 files,
   no auth/billing code), open a draft PR with tests
3. If complex, add a comment on the issue with your analysis
   and proposed approach

Do not merge anything. Do not touch auth or billing code.
Bias toward analysis over action.
```

---

## Writing Good Routine Prompts

### Principles

1. **One routine, one job.** Don't combine a security scan with a performance audit.

2. **Explicit success criteria.** "Post a summary to #channel" is better than "report results."

3. **Define boundaries.** Always include what NOT to do:
   ```
   Do not merge any PRs.
   Do not push to main.
   Only push to claude/ branches.
   Do not delete any files.
   ```

4. **Handle the empty case.** Every routine should know what to do when there's nothing to report:
   ```
   If zero issues were filed today, post a single line saying so.
   ```

5. **Be stateless.** Each run starts fresh with no memory of previous executions. Don't assume context from prior runs.

6. **Name specific connectors.** Don't assume Claude knows your workspace. Spell out channel names, repo paths, and label sets.

7. **Use worktree isolation** for routines that touch code to prevent interference with manual work.

8. **Avoid Slack formatting pitfalls.** Use bullet points. Avoid horizontal rules (`---`) which cause `invalid_blocks` errors.

### Start Small

Start with one routine. Run it for two weeks. Calibrate the prompt based on results. Then add a second. Don't roll out ten routines on day one — you'll spend more time tuning prompts than saving time.

### Recommended First Routine

Pick one based on your biggest pain point:

- **Lots of context switching?** → Morning Briefing
- **PR reviews are a bottleneck?** → Automated Code Review
- **Security concerns?** → Dependency Audit
- **Stale branches everywhere?** → Branch Cleanup

---

## Resources

- [Anthropic — Introducing Routines](https://claude.com/blog/introducing-routines-in-claude-code)
- [Anthropic — Routines Docs](https://code.claude.com/docs/en/routines)
- [Anthropic — Scheduled Tasks Docs](https://code.claude.com/docs/en/scheduled-tasks)
- [Anthropic — Desktop Scheduled Tasks](https://code.claude.com/docs/en/desktop-scheduled-tasks)
- [Anthropic — Build a Daily Briefing](https://claude.com/resources/use-cases/build-a-daily-briefing-across-your-tools)
- [Builder.io — Claude Code Routines Tutorial](https://www.builder.io/blog/claude-code-routines)
- [ComputingForGeeks — Setup Guide](https://computingforgeeks.com/claude-code-routines-setup/)
