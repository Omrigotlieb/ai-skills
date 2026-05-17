# Claude Code Routines & Scheduled Agents

Production-ready routine templates for Claude Code. These run autonomously on Anthropic's cloud infrastructure and keep working when your laptop is closed.

> Links last verified: 2026-05-17

## What Are Routines?

A routine is a saved Claude Code configuration: a prompt, one or more repositories, and a set of connectors, packaged once and run automatically. Routines execute on Anthropic-managed cloud infrastructure, so they keep working when your laptop is closed.

**Trigger types:**
- **Scheduled** — recurring cadence (hourly, daily, weekdays, weekly) or one-off
- **API** — HTTP POST to a per-routine endpoint
- **GitHub** — react to repository events (PRs, releases)

**Create from CLI:** `/schedule daily PR review at 9am`

**Quick-start:** See the [Daily Schedule Template](daily-schedule-template.md) for a ready-made routine timetable.

## Quick Navigation

| Category | Routines |
|----------|----------|
| [Daily Operations](#daily-operations) | Standup brief, morning prep, inbox triage |
| [Code Quality](#code-quality) | PR review, security scan, dependency updates |
| [Documentation](#documentation) | Docs drift, changelog, release notes |
| [Project Management](#project-management) | Issue triage, stale cleanup, backlog grooming |
| [Monitoring](#monitoring) | Deploy verification, alert triage, health checks |

---

## Writing Effective Routine Prompts

Routines run autonomously with no human in the loop. Write prompts like instructions for a contractor.

### The 5 Rules

1. **Be explicit about success** — state what "done" looks like
2. **Specify outputs** — where results go (Slack channel, PR, issue)
3. **Set boundaries** — what NOT to touch, max scope
4. **Include verification** — how to confirm the work is correct
5. **Handle failure** — what to do when something goes wrong

### Bad vs Good

```
Bad:  "Check for issues"
Good: "Read all GitHub issues opened today in {repo}. Apply a label from
       [bug, feature, docs, question, needs-triage] to each. Assign based
       on which files it references. Post a summary to #dev-standup with
       the count and breakdown by label."
```

### Prompt Structure Template

```
## Goal
[One sentence: what this routine achieves]

## Context
[Repository, services involved, what changed since last run]

## Steps
1. [Specific action with tool/connector to use]
2. [Next action]
3. [Verification step]

## Output
[Where results go: Slack channel, PR, file, issue]

## Constraints
- [What NOT to do]
- [Scope limits]
- [Time/resource bounds]

## On Failure
[What to do if a step fails — post to channel, open issue, skip]
```

---

## Daily Operations

### Morning Standup Brief

**Schedule:** Weekdays at 8:30 AM  
**Connectors:** GitHub, Slack

```
## Goal
Post a concise development standup to #dev-standup every weekday morning.

## Steps
1. Read all commits merged to main since yesterday 8:30 AM
2. List all currently open PRs with their age and review status
3. Identify anything blocked or stale (PRs open > 3 days with no review)
4. Check CI status for main branch

## Output
Post a single Slack message to #dev-standup formatted as:

**Shipped yesterday:**
- [list of merged PRs with author]

**In flight:**
- [open PRs with age and status]

**Needs attention:**
- [stale/blocked items]

**CI:** [green/red with link if failing]

## Constraints
- Keep under 15 lines
- Use bullet points, no prose
- Don't tag people unless something is blocked > 5 days
```

### Morning Meeting Prep

**Schedule:** Weekdays at 7:00 AM  
**Connectors:** GitHub, Slack, Linear/Jira (if available)

```
## Goal
Prepare a daily brief summarizing what I need to know before my first meeting.

## Steps
1. Scan PRs that were opened, updated, or merged in the last 24 hours
2. Read any GitHub issues assigned to me or mentioning my username
3. Check for failed CI runs on branches I contributed to
4. Summarize any Slack threads in #engineering where I was mentioned

## Output
Write a markdown file to /reports/daily-brief-YYYY-MM-DD.md with sections:
- Action items (things needing my response)
- Updates (FYI items)
- Risks (failing builds, stale PRs)

## Constraints
- Prioritize by urgency: action items first
- Each item should be one line with a link
- Maximum 20 items total
```

### Daily Inbox Triage

**Schedule:** Weekdays at 9:00 AM  
**Connectors:** GitHub, Linear

```
## Goal
Triage all new issues and PRs that arrived overnight, applying labels and routing.

## Steps
1. Read all GitHub issues opened since last run
2. For each issue:
   - Analyze content against codebase to determine affected area
   - Apply label from: [bug, feature, docs, question, needs-triage]
   - Apply area label from: [frontend, backend, infra, api, auth]
   - Estimate priority (P0-P3) based on severity and affected users
3. For PRs missing reviewers > 12 hours:
   - Suggest reviewer based on file ownership (git blame)

## Output
Post summary to #dev-triage:
- New issues: [count] ([breakdown by label])
- PRs needing reviewers: [list]

## Constraints
- Never auto-assign P0 issues — just flag them loudly
- Don't re-label issues that already have labels
- Skip issues from bots
```

---

## Code Quality

### Automated PR Review

**Trigger:** GitHub `pull_request.opened`  
**Connectors:** GitHub

```
## Goal
Review every new PR with a structured checklist and leave actionable feedback.

## Steps
1. Read the full diff of the PR
2. Analyze against this checklist:
   - Correctness: logic errors, off-by-one, null handling
   - Security: injection, auth bypass, secrets in code
   - Performance: N+1 queries, unbounded loops, missing indexes
   - Tests: new code has test coverage, edge cases covered
   - Readability: naming, complexity, dead code
3. For each finding, leave an inline comment at the relevant line
4. Post a summary comment with:
   - Verdict: APPROVE / REQUEST_CHANGES / COMMENT
   - Critical issues (must fix)
   - Suggestions (nice to have)

## Constraints
- Be specific: reference exact lines and suggest fixes
- Don't nitpick style if a linter handles it
- If no issues found, approve with a brief positive note
- Maximum 10 inline comments per review
```

### Nightly Security Audit

**Schedule:** Daily at 2:00 AM  
**Connectors:** GitHub

```
## Goal
Scan the repository for security vulnerabilities and report findings.

## Steps
1. Check dependency manifests (package.json, requirements.txt, go.mod)
   for known CVEs using available audit tools
2. Grep for patterns indicating hardcoded secrets:
   - API keys, tokens, passwords in source files
   - .env files committed to repo
   - Private keys or certificates
3. Scan for OWASP Top 10 patterns:
   - SQL string concatenation (potential injection)
   - Unescaped user input in templates (XSS)
   - Missing auth checks on endpoints
   - Insecure deserialization
4. Review recent changes (last 24h) for security regressions

## Output
If findings exist:
- Open a GitHub issue titled "Security Audit [DATE]: [count] findings"
- Label: security, priority based on severity
- List each finding with file, line, severity, and remediation

If clean:
- Post to #security: "Nightly audit passed. No new findings."

## Constraints
- Only report HIGH and CRITICAL findings as issues
- LOW findings go in the Slack summary only
- Never commit fixes automatically — report only
- Don't duplicate issues already open for the same finding
```

### Weekly Dependency Update

**Schedule:** Mondays at 6:00 AM  
**Connectors:** GitHub

```
## Goal
Check for outdated dependencies and open grouped PRs by risk level.

## Steps
1. Run dependency audit for all package manifests
2. Categorize updates:
   - Patch updates (low risk): group into single PR
   - Minor updates (medium risk): one PR per package
   - Major updates (high risk): one PR with migration notes
3. For each PR:
   - Update the dependency
   - Run tests to verify nothing breaks
   - Add a description noting what changed and any breaking changes

## Output
- Open PRs with clear titles: "deps: bump [package] from X to Y"
- Post summary to #dependencies with PR links grouped by risk

## Constraints
- Skip devDependencies unless they have security advisories
- Don't bump dependencies with open breaking-change issues
- Maximum 5 PRs per run to avoid review fatigue
- If tests fail after update, don't open the PR — report to Slack instead
```

---

## Documentation

### Docs Drift Detection

**Schedule:** Weekly (Sundays at 10:00 PM)  
**Connectors:** GitHub

```
## Goal
Find documentation that has fallen out of sync with code changes.

## Steps
1. List all PRs merged in the past 7 days
2. For each merged PR, identify:
   - Functions, APIs, or config options that were modified
   - Corresponding documentation files (README, docs/, wiki)
3. Compare documentation against current code:
   - Are function signatures still accurate?
   - Are config examples still valid?
   - Are removed features still documented?
4. For each stale doc, open a PR with suggested updates

## Output
Open PRs titled: "docs: update [file] to reflect [change]"
Post summary to #docs: "[count] docs need updating, PRs opened"

## Constraints
- Only flag documentation that is provably wrong (not just incomplete)
- Don't rewrite entire docs — make minimal targeted fixes
- Skip auto-generated API docs (they regenerate on build)
```

### Changelog Generation

**Schedule:** Fridays at 5:00 PM  
**Connectors:** GitHub

```
## Goal
Generate a weekly changelog from merged PRs, grouped by category.

## Steps
1. List all PRs merged since last Friday
2. Categorize each by conventional commit type:
   - feat: New features
   - fix: Bug fixes
   - perf: Performance improvements
   - docs: Documentation
   - chore: Maintenance
3. Write CHANGELOG entry with:
   - Date range
   - Grouped items with PR links
   - Contributors credited

## Output
Open a PR updating CHANGELOG.md with the new entry prepended.

## Constraints
- Use PR title as the entry (it should be descriptive)
- Skip dependabot/renovate PRs unless they fix CVEs
- Credit each contributor once in a "Contributors" section
- Don't include internal/draft PRs that were merged accidentally
```

---

## Project Management

### Issue Triage Bot

**Trigger:** GitHub `issues.opened`  
**Connectors:** GitHub

```
## Goal
Auto-triage new bug reports: identify likely cause, apply labels, detect duplicates.

## Steps
1. Read the new issue content
2. Search existing open issues for potential duplicates:
   - Similar title
   - Same error messages
   - Same affected component
3. If duplicate found: comment linking to original, apply "duplicate" label
4. If not duplicate:
   - Identify affected component from description and stack traces
   - Apply area label based on file paths mentioned
   - Estimate severity from impact description
   - Apply priority label (P0-P3)

## Output
- Labels applied to the issue
- Comment with: "Triaged: [area], [priority]. Similar: [links if any]"

## Constraints
- Never close issues automatically
- If uncertain about priority, default to P2 and apply "needs-triage"
- Don't triage issues from maintainers (they self-label)
```

### Stale Issue Cleanup

**Schedule:** Daily at 11:00 PM  
**Connectors:** GitHub

```
## Goal
Keep the issue tracker clean by flagging and closing abandoned issues.

## Steps
1. Find issues with no activity in 30 days
2. Exclude: pinned issues, P0/P1 issues, issues with "keep-open" label
3. For issues inactive 30 days: apply "stale" label and comment asking
   if the issue is still relevant
4. For issues inactive 44 days (14 days after stale label): close with
   a comment explaining they can be reopened

## Output
- Post to #project: "Stale cleanup: [X] labeled stale, [Y] closed"

## Constraints
- Never close issues with recent linked PRs
- Don't close issues that have upvotes/reactions in last 60 days
- Respect "keep-open" label absolutely
- Maximum 10 closures per run
```

---

## Monitoring

### Post-Deploy Verification

**Trigger:** API (called from CD pipeline)  
**Connectors:** GitHub, Slack

```
## Goal
Verify a production deployment is healthy and report status.

## Steps
1. Parse the deployment context from the API trigger text
2. Wait 2 minutes for deployment to stabilize
3. Run verification checks:
   - Health endpoint responds 200
   - Response time < 500ms for key endpoints
   - No new error patterns in logs (last 5 minutes vs baseline)
   - Key user flows complete without error
4. Compare error rates: current 5-min window vs same window yesterday

## Output
Post to #releases:
- PASS: "Deploy [version] verified. All checks green."
- FAIL: "Deploy [version] FAILED verification: [specific failures]"

If FAIL, also open an issue with full diagnostic details.

## Constraints
- Give deployment 2 minutes before checking (cold start)
- Only compare against same time window to account for traffic patterns
- Don't trigger rollback automatically — just report
```

### Alert Triage Agent

**Trigger:** API (called from monitoring/alerting system)  
**Connectors:** GitHub, Slack

```
## Goal
When an alert fires, correlate it with recent changes and suggest a fix.

## Steps
1. Parse the alert from the trigger text (service, error, threshold)
2. Find commits deployed in the last 6 hours
3. For each recent commit:
   - Check if modified files relate to the alerting service
   - Look for patterns that could cause the reported error
4. If probable cause found:
   - Open a draft PR with a proposed fix
   - Link to the alert and explain the correlation
5. If no cause found:
   - Post analysis to #oncall with what was checked

## Output
- Draft PR with fix (if cause identified)
- Slack message to #oncall with analysis either way

## Constraints
- Draft PRs only — never merge automatically
- If multiple possible causes, list them ranked by likelihood
- Don't modify config files without explicit patterns
- Maximum investigation time: 10 minutes worth of analysis
```

---

## Multi-Agent Patterns

### Task Board Architecture

For teams running multiple routines, use a shared task board pattern:

```
## Task States
TODO → IN_PROGRESS → DONE → VERIFIED → ARCHIVED

## Agent Roles
- Idea/Triage agent: creates and prioritizes tasks
- Developer agent: implements tasks
- Reviewer agent: validates implementations
- Supervisor agent: monitors health and progress

## Collaboration
Agents communicate through a shared markdown task file committed to the repo.
Each agent runs on its own cron schedule (every 2 hours offset by 15 min).
```

### Chaining Routines

Use API triggers to chain routines:

```
Routine A (scheduled nightly): Run security scan
  → On findings, call Routine B's API endpoint

Routine B (API triggered): Create fix PRs
  → On PR created, Routine C auto-triggered by GitHub event

Routine C (GitHub PR opened): Review the fix PR
```

---

## Best Practices

### Start Small

1. Begin with read-only routines (standup brief, reports)
2. Graduate to labeling and commenting
3. Then move to PR creation
4. Last: approval and merge (requires high trust)

### Prompt Engineering for Autonomy

| Principle | Example |
|-----------|---------|
| Explicit success criteria | "Post exactly one message with these sections..." |
| Bounded scope | "Only check files modified in the last 24 hours" |
| Failure handling | "If audit tool is unavailable, post to #alerts and exit" |
| Idempotency | "Skip issues that already have a triage label" |
| Rate limiting | "Maximum 5 PRs per run" |

### Common Pitfalls

1. **Vague prompts** — "check things" produces random results
2. **No output destination** — routine runs but results vanish
3. **Missing idempotency** — routine creates duplicates on re-run
4. **Overly broad scope** — routine times out analyzing entire repo
5. **No failure path** — silent failures with no notification
6. **Network assumptions** — cloud routines have proxy restrictions; use MCP connectors for external services

### Lessons from Production

- Connectors require explicit loading in routines (they aren't auto-available)
- Cloud routines operate behind a network proxy; use MCP connectors for non-GitHub traffic
- Scheduled triggers are more reliable than API triggers for connector availability
- Test manually first: verify correct input reading, output location, and completion signals
- Treat prompts like production code: version them, test them, iterate

---

## Resources

- [Official Routines Documentation](https://code.claude.com/docs/en/routines)
- [Desktop Scheduled Tasks](https://code.claude.com/docs/en/desktop-scheduled-tasks) (local alternative that runs on your machine)
- [Introducing Routines (Blog)](https://claude.com/blog/introducing-routines-in-claude-code)
- [claude-code-routines templates](https://github.com/phillipatkins/claude-code-routines)
- [claude-routines-and-agents-pm-pack](https://github.com/aakashg/claude-routines-and-agents-pm-pack)
- [techtools-claude-code-cron-loop](https://github.com/TaraJura/techtools-claude-code-cron-loop)
- [claudecron MCP server](https://github.com/phildougherty/claudecron)
- [Builder.io Routines Tutorial](https://www.builder.io/blog/claude-code-routines)
- [Nimbalyst Practical Guide](https://nimbalyst.com/blog/claude-code-routines-practical-guide/)
