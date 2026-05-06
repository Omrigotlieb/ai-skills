# Routines & Scheduled Agents

Automated workflows that run on a schedule or in response to events, so your AI assistant works even when you don't. This page covers what to automate, when to run it, and how to set it up.

> Links last verified: 2026-05-06

---

## How Scheduling Works in Claude Code

Claude Code offers three scheduling layers, each with different tradeoffs:

| Layer | Runs where | Survives restarts | Best for |
|---|---|---|---|
| **Routines** (`/schedule` or [claude.ai/code/routines](https://claude.ai/code/routines)) | Anthropic cloud | Yes | Recurring jobs that must run regardless of laptop state |
| **Desktop scheduled tasks** | Local machine | Yes | Local automation tied to your machine |
| **`/loop`** (session-scoped) | Current session | No | Active monitoring during a work session |

Routines are available on Pro, Max, Team, and Enterprise plans. Current limit: 15 runs/day/account.

### Routine Anatomy

Each routine combines:
- **Prompt** — what the agent should do
- **Repository** — the GitHub repo to operate on
- **Trigger** — cron schedule, GitHub event (`pull_request.opened`, `issues.opened`), or API webhook
- **Connectors** — optional integrations (Slack, Linear, etc.)

---

## Daily Routines

### Morning Standup Digest

Scans open PRs, recent commits, and blocked items; posts a digest before standup.

**Schedule:** Weekdays, 15 minutes before standup (e.g., `45 8 * * 1-5`)

```
Read all open PRs and commits from the last 24 hours on this repo.

Post to #standup with:
- What landed yesterday (merged PRs with one-line summaries)
- What's in flight (open PRs with author and age)
- Anything stale (PRs open > 3 days with no review activity)

Keep the message under 20 lines. Use bullet points, not paragraphs.
```

**Why this works:** Replaces the manual "let me check GitHub" ritual. The time constraint (15 min before standup) means the digest is fresh when the team reads it.

---

### Nightly Issue Triage

Labels and assigns new GitHub issues, requests missing info, posts a summary.

**Schedule:** Daily overnight (e.g., `0 22 * * *`)
**Trigger alternative:** GitHub event `issues.opened` for real-time triage

```
Review all issues opened today that have no labels or assignees.

For each issue:
1. Apply appropriate labels based on content (bug, feature, docs, question)
2. Check CODEOWNERS and suggest an assignee
3. If the issue lacks reproduction steps or version info, post a comment
   asking for them
4. If the issue matches an existing open issue, link them

Post a summary to #triage with counts by label.
```

**Source:** [Builder.io Claude Code Routines tutorial](https://www.builder.io/blog/claude-code-routines)

---

### Support Ticket Digest

Clusters and summarizes the day's support tickets to surface trends.

**Schedule:** Daily end of business (e.g., `0 17 * * 1-5`)

```
Read the last 24 hours of support tickets.

Cluster by theme (authentication, billing, performance, etc.).
Identify anomalies: any spike in a category vs. the 7-day average?
Flag tickets that mention data loss or security.

Post a structured summary to #support-eng with:
- Top 3 themes with ticket counts
- Any anomalies
- Tickets requiring engineering escalation
```

**Source:** [Claude Code Routines: 8 Production Prompts](https://linas.substack.com/p/claude-code-routines-guide)

---

## Event-Triggered Routines

### PR Code Review

Automatically reviews every new PR for security, performance, and style issues.

**Trigger:** `pull_request.opened`

```
Review this pull request thoroughly.

Check for:
- Security: hardcoded secrets, injection risks, CVEs in new dependencies
- Performance: N+1 queries, missing indexes, synchronous ops in hot paths
- Code quality: naming, error handling, test coverage for new code

For each finding:
- Leave an inline comment at the specific line
- Include severity (critical/high/medium/low)
- Suggest a concrete fix, not just a description of the problem

Post a summary comment with pass/fail verdict and finding counts by severity.
```

**How it scales:** Cloudflare runs up to 7 specialized sub-reviewers (security, performance, compliance) per merge request, each with domain-specific prompts.

**Source:** [Cloudflare AI Code Review](https://blog.cloudflare.com/ai-code-review/)

---

### Deploy Verification

Fires when monitoring detects an error spike after a deploy.

**Trigger:** API webhook from monitoring (Datadog, PagerDuty, Sentry)

```
A deployment error spike was detected.

1. Pull the top 5 error stack traces from the last 30 minutes
2. Correlate with commits deployed in the last release
3. Identify the most likely culprit commit
4. Check if there's a quick rollback path or if a hotfix is needed

Post a go/no-go verdict to #deploys with:
- Root cause assessment (high/medium/low confidence)
- Recommended action (rollback, hotfix, or monitor)
- Links to relevant commits and error traces
```

---

## Session-Scoped Routines (`/loop`)

### PR Babysitter

Monitors your PR through CI and review, auto-fixing issues until it's green.

**Invocation:** `/loop 5m /babysit-pr`

```
Check the status of my open PR:

1. Are there any failing CI checks? If yes:
   - Read the failure logs
   - Identify the root cause
   - Fix the issue and push

2. Are there any unaddressed review comments? If yes:
   - Read each comment
   - Make the requested changes
   - Push and respond to the reviewer

3. Does the PR need a rebase? If yes:
   - Rebase onto the base branch
   - Resolve any conflicts
   - Push

4. Is everything green and approved? If yes:
   - Report "PR is ready to merge" and stop the loop

5. If none of the above, report current status and continue monitoring.

Maximum 5 fix iterations before escalating to the developer.
```

**Origin:** Boris Cherny (Anthropic) popularized this pattern. Community SKILL.md versions exist as gists by [tilomitra](https://gist.github.com/tilomitra/e0dca29b3a63b5b5aba62c1baeaa27b4) and [gabrielshanahan](https://gist.github.com/gabrielshanahan/6c2f1a5e40e33040b306b375b42ffc5e).

---

### CI Babysitter

Watches GitHub Actions, pulls failed job logs, fixes and pushes until green.

**Invocation:** `/loop 5m`

```
Check the latest GitHub Actions run on this branch.

If any jobs failed:
1. Pull the failed job logs
2. Identify the root cause
3. Fix the issue locally
4. Push the fix
5. Wait for the new run to start

If all jobs passed: report success and stop.
If the same job has failed 3 times: stop and report the persistent failure.
```

**Source:** [CI Babysitter Guide (neonwatty.com)](https://neonwatty.com/posts/claude-code-ci-babysitter/)

---

## Weekly Routines

### Dependency Audit

Checks for vulnerable or outdated packages and opens a PR with updates.

**Schedule:** Weekly, Sunday night (e.g., `0 2 * * 0`)

```
Run a dependency audit for this project.

1. Check for known vulnerabilities (npm audit / pip-audit / cargo audit)
2. List outdated packages with current vs. latest version
3. For each vulnerability:
   - Severity level
   - Whether an upgrade path exists
   - Breaking change risk (major version bump = flag it)

4. Create a branch and PR with:
   - Safe patch/minor updates applied
   - Major updates listed in the PR description with migration notes
   - Updated lockfile

Title the PR "chore(deps): weekly dependency update [automated]"
```

---

### Documentation Drift Detection

Catches stale API references and outdated docs before users find them.

**Schedule:** Weekly, Monday morning (e.g., `0 9 * * 1`)

```
Scan PRs merged in the last 7 days.

For each PR that modified a public API (added/changed/removed endpoints,
function signatures, or CLI flags):
1. Check if the corresponding docs are up to date
2. Check if README sections reference the changed code
3. Check if inline doc comments match the current implementation

If any docs are stale:
- Open a PR with suggested updates
- Title: "docs: fix drift detected in [area]"
- List which PRs caused the drift
```

**Source:** [GitHub Agentic Workflows — Documentation](https://github.github.io/gh-aw/blog/2026-01-13-meet-the-workflows-documentation/)

---

### Tech Debt Scan

Surfaces TODO/FIXME comments, dead code, and complexity hotspots.

**Schedule:** Weekly, Monday morning (e.g., `0 6 * * 1`)

```
Scan the codebase for tech debt signals:

1. TODO/FIXME/HACK/XXX comments — list with file, line, and age
   (how many commits ago was it added?)
2. Functions over 100 lines
3. Files with cyclomatic complexity in the top 10%
4. Dead exports (exported but never imported elsewhere)
5. Duplicate code blocks (>10 lines of near-identical code)

Cluster findings by area (auth, API, database, frontend, etc.).
Prioritize by impact: "this blocks feature X" > "this is ugly."

Post the report to #tech-debt or create a GitHub issue labeled "tech-debt."
```

---

### Security Sweep

Proactive security scan beyond dependency audits.

**Schedule:** Weekly or daily (e.g., `0 3 * * 1`)

```
Run a security review of the codebase:

1. Scan for hardcoded secrets, API keys, or tokens (check .env.example
   against actual environment variable usage)
2. Check for SQL injection, XSS, and command injection patterns
3. Review authentication and authorization code for common flaws
4. Check that sensitive endpoints have rate limiting
5. Verify CORS configuration is restrictive

Report findings with:
- Severity (critical/high/medium/low)
- File and line number
- Suggested fix
- OWASP category

If any critical findings: create a GitHub issue labeled "security" and
assign the security team.
```

---

## Scheduling Tools (Community)

When you need more control than native routines provide:

| Tool | What it does | Link |
|---|---|---|
| **claude-code-scheduler** | JSON config in `.claude/schedules.json`, cron expressions, git worktree isolation | [jshchnz/claude-code-scheduler](https://github.com/jshchnz/claude-code-scheduler) |
| **claudecron** | MCP server with cron, hook-event, and file-watch triggers; SQLite state | [phildougherty/claudecron](https://github.com/phildougherty/claudecron) |
| **claude-tasks** | Go TUI with second-granularity cron, Discord/Slack webhooks | [kylemclaren/claude-tasks](https://github.com/kylemclaren/claude-tasks) |
| **outworked** | Agent framework with built-in `create_trigger` scheduling | [outworked/outworked](https://github.com/outworked/outworked) |

---

## Building Your Own Routine

### As a Skill

Create `.claude/skills/my-routine/SKILL.md`:

```yaml
---
name: my-routine
description: Describe what this routine does and when it triggers
---

# My Routine

## When to Use
- Triggered by /schedule with cron "0 9 * * 1-5"
- Or manually via /my-routine

## Instructions
1. Step one...
2. Step two...
3. Post results to #channel

## Success Criteria
- All checks pass
- Summary posted within 5 minutes
- No false positives in the last 7 days
```

### As a Native Routine

Via CLI:
```bash
claude schedule create \
  --name "morning-digest" \
  --repo "owner/repo" \
  --cron "45 8 * * 1-5" \
  --prompt "Review open PRs and post digest to #standup"
```

Via web: [claude.ai/code/routines](https://claude.ai/code/routines) — configure prompt, repo, trigger, and connectors through the UI.

### Prompt Writing Tips

From community experience, effective routine prompts share these traits:

1. **Explicit success criteria** — not "review PRs" but "review open PRs against /auth, check for SQL injection, leave inline comments with severity labels"
2. **Structured output** — tell the agent exactly what format to post (bullet points, table, pass/fail)
3. **Bounded scope** — "last 24 hours" or "files changed in this PR," not "the whole codebase"
4. **Escalation rules** — "if you can't fix it in 3 attempts, stop and report"
5. **Idempotency** — routines may run twice; the prompt should handle duplicate runs gracefully

---

## Sample Daily Schedule

A complete developer automation schedule combining the routines above:

| Time | Routine | Type | Purpose |
|---|---|---|---|
| 7:00 AM | Tech debt scan | Weekly (Mon) | Surface accumulated debt |
| 8:45 AM | Morning standup digest | Daily | Prep the team for standup |
| On PR open | PR code review | Event | Catch issues before human review |
| On issue open | Issue triage | Event | Label and assign automatically |
| 5:00 PM | Support ticket digest | Daily | Surface support trends |
| 10:00 PM | Nightly issue triage | Daily | Clean up unlabeled issues |
| 2:00 AM Sun | Dependency audit | Weekly | Keep deps secure and current |
| 3:00 AM Mon | Security sweep | Weekly | Proactive vulnerability detection |
| 9:00 AM Mon | Docs drift detection | Weekly | Catch stale documentation |
| As needed | PR babysitter | `/loop` session | Shepherd PRs to merge |

---

## Resources

- [Claude Code Routines Documentation](https://code.claude.com/docs/en/routines)
- [Claude Code Scheduled Tasks](https://code.claude.com/docs/en/scheduled-tasks)
- [Claude Code Routines: 5 Setups That Work While You Sleep](https://alirezarezvani.medium.com/claude-code-routines-5-setups-that-work-while-you-sleep-ee779b5e6924)
- [Claude Code Routines: 8 Production Prompts](https://linas.substack.com/p/claude-code-routines-guide)
- [Builder.io: Claude Code Routines Tutorial](https://www.builder.io/blog/claude-code-routines)
- [CI Babysitter Guide](https://neonwatty.com/posts/claude-code-ci-babysitter/)
- [Cloudflare AI Code Review](https://blog.cloudflare.com/ai-code-review/)
- [GitHub Agentic Workflows](https://github.github.io/gh-aw/)
