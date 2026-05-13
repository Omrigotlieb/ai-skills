# Claude Code Routines

Production-ready routine prompts for Claude Code's cloud automation. Routines run autonomously on Anthropic's infrastructure — no laptop required.

> **Feature status:** Research preview (April 2026) | **Docs:** [Official Routines Guide](https://code.claude.com/docs/en/routines)

## What Are Routines?

A routine is a saved Claude Code configuration — a prompt, one or more repositories, and a set of connectors — packaged once and run automatically on Anthropic-managed cloud infrastructure.

**Three trigger types:**
- **Scheduled** — recurring (hourly, daily, weekly) or one-off at a future time
- **API** — HTTP POST to a per-routine endpoint with a bearer token
- **GitHub** — repository events like `pull_request.opened` or `release.published`

A single routine can combine triggers. A PR review routine can run nightly, trigger from a deploy script, and react to every new PR.

**Plan limits:** Routines have a daily run cap per account (varies by plan). Check your current allowance at [claude.ai/code/routines](https://claude.ai/code/routines). One-off runs are exempt from the daily cap.

---

## Quick Start

### From the web
Visit [claude.ai/code/routines](https://claude.ai/code/routines) and click **New routine**.

### From the CLI
```bash
/schedule daily PR review at 9am
/schedule in 2 weeks, open a cleanup PR that removes the feature flag
/schedule list           # see all routines
/schedule update         # change one
/schedule run            # trigger immediately
```

> `/schedule` creates scheduled (time-based) routines only. To add API or GitHub event triggers, edit the routine at [claude.ai/code/routines](https://claude.ai/code/routines).

---

## Writing Effective Routine Prompts

The prompt is the most important part. Since routines run autonomously, every prompt must be self-contained.

### The SCOPE Framework

| Element | Purpose | Example |
|---------|---------|---------|
| **S**pecify | What exactly to do | "Scan all PRs merged in the past 7 days" |
| **C**ontext | What repo/files/tools are involved | "In the docs/ directory of the main repo" |
| **O**utput | What deliverable to produce | "Open a PR with suggested updates" |
| **P**ost | Where to report results | "Post a summary to the #engineering Slack channel" |
| **E**dge cases | What to do when things are ambiguous | "If no outdated docs are found, post a short all-clear message" |

### Rules of Thumb

1. **Be explicit, not vague.** "Pull the last 24 hours of error logs, summarize the top 5 errors by frequency, and write the report to `/reports/daily-errors-YYYY-MM-DD.md`" beats "check for errors."
2. **Define success.** The routine can't ask you questions — tell it what "done" looks like.
3. **Scope connectors.** Remove connectors the routine doesn't need.
4. **Watch the first runs.** Open the sessions, read what Claude did, adjust the prompt.
5. **Start with one.** Calibrate before adding more routines.

---

## Routine Templates

### Daily Routines

#### 1. Morning Standup Report

**Trigger:** Scheduled — weekdays at 8:30 AM  
**Connectors:** GitHub, Slack

```
Generate a morning development standup report.

Gather:
1. PRs merged since yesterday's report
2. PRs currently open and awaiting review (flag any older than 48 hours)
3. New issues opened in the last 24 hours
4. CI/CD pipeline status — any failing builds on main

Format as a Slack message with sections:
- "Shipped Yesterday" — list merged PRs with one-line summaries
- "Needs Review" — open PRs sorted by age, oldest first
- "New Issues" — new issues with labels and assignees (or "unassigned" if none)
- "Build Status" — green/red for each CI workflow on main

Post to #engineering-standup. If nothing noteworthy happened, post a short all-clear message instead of an empty report.
```

---

#### 2. Issue Triage Bot

**Trigger:** Scheduled — nightly at 11 PM  
**Connectors:** GitHub, Slack (or Linear)

```
Triage all GitHub issues opened today that have no labels.

For each unlabeled issue:
1. Read the title and body
2. Scan the repository code to identify which modules or directories are affected
3. Apply labels:
   - Area label (e.g., "area:auth", "area:api", "area:frontend") based on affected code
   - Type label ("bug", "feature", "question", "docs") based on content
   - Priority label ("P0-critical", "P1-high", "P2-medium", "P3-low") based on severity signals
4. If the issue mentions a specific error or stack trace, add a comment with the likely root cause and affected files

After processing all issues, post a summary to #triage-log:
- Total issues triaged
- Breakdown by priority
- Any P0/P1 issues that need immediate attention

If no new unlabeled issues exist, skip the Slack message.
```

---

#### 3. Dependency Vulnerability Check

**Trigger:** Scheduled — daily at 6 AM  
**Connectors:** GitHub

```
Run a daily dependency security check across all package manifests in the repository.

Steps:
1. Identify all dependency files (package.json, requirements.txt, go.mod, Cargo.toml, Gemfile)
2. Check each for known vulnerabilities using the lockfile and advisory databases
3. For any vulnerabilities found:
   - Classify severity (critical, high, medium, low)
   - Check if a patched version exists
   - If a patch exists and the update is semver-compatible (patch or minor), open a PR with the update
   - If the update is a major version bump, open an issue instead describing the vulnerability and required migration

Group related updates into a single PR where possible. Title PRs as:
"security: patch [package] from [old] to [new] (fixes [CVE])"

If no vulnerabilities are found, do nothing — don't create empty PRs or issues.
```

---

### Weekly Routines

#### 4. Documentation Drift Detection

**Trigger:** Scheduled — Mondays at 9 AM  
**Connectors:** GitHub

```
Scan all pull requests merged in the past 7 days. For each PR:

1. Identify which functions, APIs, CLI flags, configuration options, or environment variables were added, changed, or removed
2. Search documentation files (README.md, docs/, wiki pages, any .md files) for references to those changed items
3. If documentation references an API or option that was modified, check whether the documentation reflects the new behavior

For each piece of outdated documentation found:
- Open a single PR (not one per doc) titled "docs: update references for week of YYYY-MM-DD"
- Include clear descriptions of what changed and why the doc needs updating
- Group changes by the PR that caused them

If no documentation drift is detected, do nothing.
```

---

#### 5. Stale Issue Cleanup

**Trigger:** Scheduled — Fridays at 5 PM  
**Connectors:** GitHub

```
Find GitHub issues that have gone stale and need attention.

Definition of stale:
- No comments or updates in the past 30 days
- Not labeled "long-term" or "backlog"
- Not assigned to a milestone

For each stale issue:
1. Add the label "stale"
2. Post a comment: "This issue has had no activity for 30 days. It will be closed in 14 days if there are no further updates. Remove the 'stale' label to keep it open."

For issues already labeled "stale" with no activity in 14 additional days:
1. Close the issue
2. Add a closing comment: "Closed due to inactivity. Reopen if this is still relevant."

Post a summary to #project-management:
- Number of issues marked stale
- Number of issues closed
- Any issues that were un-staled (someone removed the label since last run)
```

---

#### 6. PR Aging Report

**Trigger:** Scheduled — Fridays at 4 PM  
**Connectors:** GitHub, Slack

```
Generate a weekly PR aging report for open pull requests.

For each open PR:
1. Calculate age since creation
2. Identify the current review status (approved, changes requested, pending review, no reviewers assigned)
3. Check CI status

Organize into tiers:
- "Critical" (>7 days, no approval): list with assignee and blockers
- "Aging" (3-7 days): list with current status
- "On Track" (<3 days): count only, don't list individually

Format as a Slack message to #engineering with:
- Total open PRs
- Critical PRs requiring attention (with @mentions of assignees)
- Aging PRs summary
- On-track count

If all PRs are on track, post a brief celebratory message instead.
```

---

### Event-Driven Routines

#### 7. PR Code Review

**Trigger:** GitHub — `pull_request.opened`  
**Connectors:** GitHub

```
Review this pull request using the team's code review checklist.

For each changed file, check:

1. **Correctness**: Logic errors, off-by-one mistakes, race conditions, null safety
2. **Security**: SQL injection, XSS, hardcoded secrets, insecure deserialization, auth bypasses
3. **Performance**: N+1 queries, unnecessary allocations, missing indexes, blocking I/O in async paths
4. **Tests**: Are new code paths tested? Are edge cases covered? Do existing tests still apply?
5. **Readability**: Unclear naming, overly complex logic, missing context for non-obvious decisions

Leave inline comments only for issues that matter — skip style nitpicks already caught by linters. Each comment should explain the problem and suggest a fix.

Post a summary comment on the PR:
- Overall assessment (approve / request changes / comment only)
- Key findings grouped by severity
- A one-sentence summary of what the PR does

Do not approve PRs automatically — always use "comment" status so a human makes the final call.
```

---

#### 8. Deploy Verification

**Trigger:** API (called by CD pipeline after deploy)  
**Connectors:** GitHub, Slack

```
Verify the production deployment is healthy.

The API trigger text contains the deploy metadata (commit SHA, environment, deployer).

Steps:
1. Identify what changed in this deploy by reading the commits since the last tagged release
2. For each changed area, verify:
   - The relevant API endpoints return 200 status (if endpoint URLs are documented in the repo)
   - No new error patterns appear in recent logs (check error monitoring connector if available)
   - Database migrations (if any) completed without errors
3. Check the CI status of the deployed commit

Post to #deploys:
- "Deploy Verified" or "Deploy Needs Attention"
- What was deployed (PR titles and authors)
- Any issues found during verification
- Suggested rollback steps if critical issues are detected

If verification passes cleanly, keep the message brief. Only include detailed analysis when issues are found.
```

---

#### 9. Release Notes Generator

**Trigger:** GitHub — `release.created`  
**Connectors:** GitHub

```
Generate customer-facing release notes for this release.

Steps:
1. Find all PRs merged between this release tag and the previous one
2. For each PR, extract:
   - The user-visible change (ignore internal refactors, CI changes, dependency bumps)
   - The category: "New Features", "Improvements", "Bug Fixes", "Breaking Changes"
3. If the PR links to an issue or ticket, include the reference

Write the release notes in this format:
## What's New
- [Feature description] (#PR)

## Improvements
- [Improvement description] (#PR)

## Bug Fixes
- [Fix description] (#PR)

## Breaking Changes
- [Change description and migration steps] (#PR)

Omit empty sections. Use plain language — write for users, not developers.
Update the release body on GitHub with the generated notes.
```

---

#### 10. Alert Triage and Fix

**Trigger:** API (called by monitoring/alerting system)  
**Connectors:** GitHub

```
An alert has fired. The alert body is in the trigger text.

Steps:
1. Parse the alert for: error message, stack trace, affected service, and timestamp
2. Search the repository for the code referenced in the stack trace
3. Review recent commits (last 48 hours) that touched the affected files
4. Correlate: did a recent change introduce this error?

If a likely root cause is found:
- Open a draft PR with a proposed fix
- Title: "fix: [brief description] (triggered by [alert name])"
- In the PR description, link the alert, explain the root cause, and describe the fix
- Request review from the author of the commit that likely introduced the issue

If no clear root cause is found:
- Open an issue titled "Investigate: [alert name]"
- Include the full alert context, affected code paths, and recent commits for manual investigation
- Label it "P1-high" and "needs-investigation"
```

---

### Maintenance Routines

#### 11. Weekly Code Quality Sweep

**Trigger:** Scheduled — Sundays at 2 AM  
**Connectors:** GitHub

```
Run a weekly code quality sweep on the repository.

Check for:
1. TODO/FIXME/HACK comments older than 30 days (check git blame dates)
2. Dead code: exported functions or classes with zero internal references
3. Unused dependencies in package manifests
4. Files exceeding 500 lines that could benefit from splitting
5. Test files with skipped/pending tests (.skip, .todo, xit, xdescribe)

For each finding, assess whether it's actionable:
- If the fix is safe and mechanical (removing unused imports, deleting dead exports), include it in a single cleanup PR titled "chore: weekly code quality sweep YYYY-MM-DD"
- If the fix requires judgment (splitting a large file, resolving a TODO), open an issue instead

Keep the PR under 200 lines of changes. If more cleanup is needed, prioritize by impact and defer the rest to next week.
```

---

#### 12. Changelog Generator

**Trigger:** Scheduled — Mondays at 8 AM  
**Connectors:** GitHub

```
Generate a changelog entry for the past week's changes.

Steps:
1. List all PRs merged to main since the last CHANGELOG.md entry
2. Categorize each PR:
   - "Added" — new features
   - "Changed" — modifications to existing features
   - "Fixed" — bug fixes
   - "Removed" — removed features or deprecated items
   - "Security" — security-related changes
3. Skip PRs that are purely internal (CI config, code formatting, dependency bumps unless security-related)

Format following Keep a Changelog (keepachangelog.com):

## [Unreleased] - YYYY-MM-DD
### Added
- Description (#PR)
### Fixed
- Description (#PR)

Open a PR titled "docs: changelog for week of YYYY-MM-DD" adding the new entry at the top of CHANGELOG.md. If no user-facing changes were merged, do nothing.
```

---

## Connector Setup

Routines access external services through MCP connectors configured at [claude.ai/customize/connectors](https://claude.ai/customize/connectors).

| Connector | Common Uses | Setup |
|-----------|-------------|-------|
| **GitHub** | PR review, issue triage, release notes | Connected via `/web-setup` or OAuth |
| **Slack** | Standup reports, deploy notifications, triage summaries | Add via Connectors settings |
| **Linear** | Issue creation, status updates, sprint tracking | Add via Connectors settings |
| **Sentry** | Error monitoring, alert triage | Add via Connectors settings |
| **Google Drive** | Report generation, document updates | Add via Connectors settings |

For services without a connector, declare an MCP server in `.mcp.json` in the repository so it's available when the repo is cloned.

---

## Configuration Tips

### Branch Permissions
By default, routines can only push to `claude/`-prefixed branches. Enable **Allow unrestricted branch pushes** per repository if the routine needs to push to other branches.

### Environment Variables
Store API keys and tokens in the environment's variable section, not in the prompt. The routine inherits these on every run.

### Network Access
The default environment allows common package registries and cloud APIs. If your routine needs to reach custom domains, set network access to **Custom** and add your domains.

### Monitoring Runs
- Each run creates a session at [claude.ai/code](https://claude.ai/code)
- Green status means the session ran without infrastructure errors — it does not mean the task succeeded
- Always open the first few runs to verify the prompt produces correct results

---

## Composing Routines

### Daily Schedule Example

| Time | Routine | Trigger |
|------|---------|---------|
| 6:00 AM | Dependency vulnerability check | Scheduled |
| 8:30 AM | Morning standup report | Scheduled |
| 11:00 PM | Issue triage | Scheduled |

### Weekly Schedule Example

| Day | Routine | Trigger |
|-----|---------|---------|
| Monday 8 AM | Changelog generator | Scheduled |
| Monday 9 AM | Documentation drift detection | Scheduled |
| Friday 4 PM | PR aging report | Scheduled |
| Friday 5 PM | Stale issue cleanup | Scheduled |
| Sunday 2 AM | Code quality sweep | Scheduled |

### Event-Driven Layer

Run these alongside scheduled routines:

| Event | Routine |
|-------|---------|
| PR opened | Code review |
| Release created | Release notes |
| Deploy completed | Deploy verification |
| Alert fired | Alert triage |

---

## Anti-Patterns

| Mistake | Why It Fails | Fix |
|---------|--------------|-----|
| Vague prompt ("review code") | Inconsistent, shallow results | Specify exact checklist and output format |
| No success criteria | Can't tell if the routine worked | Define what "done" looks like |
| Too many connectors | Wider attack surface, slower runs | Remove unused connectors |
| Runs too frequently | Wastes quota, produces noise | Match cadence to value — daily or weekly is usually enough |
| No output destination | Results sit in session logs unseen | Always post to Slack, open a PR, or write a file |
| Prompt references external context | Routine runs in a clean session with no memory | Make every prompt fully self-contained |

---

## Community Resources

### Routine Template Libraries
- [phillipatkins/claude-code-routines](https://github.com/phillipatkins/claude-code-routines) — 13 ready-to-use templates installable via `npx`
- [wshobson/agents](https://github.com/wshobson/agents) — 185 specialized agents across 80 plugins with orchestration patterns
- [jordanpartridge/claude-code-agents](https://github.com/jordanpartridge/claude-code-agents) — GitHub workflow automation agents
- [ChrisWiles/claude-code-showcase](https://github.com/ChrisWiles/claude-code-showcase) — Full project configuration with hooks, skills, agents, and GitHub Actions

### Guides
- [Official Routines Documentation](https://code.claude.com/docs/en/routines)
- [Claude Code Routines: Practical Guide](https://nimbalyst.com/blog/claude-code-routines-practical-guide/)
- [Introducing Routines in Claude Code](https://claude.com/blog/introducing-routines-in-claude-code)
- [Claude Directory Routines Guide](https://www.claudedirectory.org/blog/claude-code-routines-guide)

### Related Features
- [`/loop` and in-session scheduling](https://code.claude.com/docs/en/scheduled-tasks) — local recurring tasks within an open CLI session
- [Desktop scheduled tasks](https://code.claude.com/docs/en/desktop-scheduled-tasks) — local scheduled tasks that run on your machine
- [GitHub Actions](https://code.claude.com/docs/en/github-actions) — CI/CD integration for repository events
