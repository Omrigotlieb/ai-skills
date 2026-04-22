# Routines & Scheduled Agents for Claude Code

Skills and prompt templates for automated routines, scheduled tasks, and daily agent workflows. These patterns help you put Claude Code on autopilot for recurring work.

> **New in 2026:** Claude Code Routines run on Anthropic-managed cloud infrastructure with schedule, API, and GitHub event triggers. Create them at [claude.ai/code/routines](https://claude.ai/code/routines) or via `/schedule` in the CLI.

---

## Quick Start

1. Pick a routine template below
2. Customize the prompt for your project
3. Set up triggers (schedule, API, or GitHub event)
4. Test with "Run now" before relying on the schedule

---

## Routine Trigger Types

| Trigger | When to Use | Example |
|---------|-------------|---------|
| **Scheduled** | Recurring cadence (hourly, daily, weekly) | Nightly backlog triage |
| **API** | On-demand via HTTP POST | Post-deploy verification |
| **GitHub** | Repository events (PR opened, release created) | Automated code review |

A single routine can combine multiple triggers.

---

## Morning Brief & Daily Digest

Start each day with an automated summary of what happened overnight.

```markdown
---
name: morning-brief
description: Daily morning briefing with overnight activity summary
---

# Morning Brief

## Prompt

Prepare a morning brief covering the last 24 hours:

1. **Git Activity**: List all commits pushed since yesterday. Group by author.
   Highlight any commits to main/production branches.

2. **Open PRs**: List all open pull requests with their status:
   - CI pass/fail
   - Review status (approved, changes requested, pending)
   - Days open

3. **Issues & Bugs**: Summarize new issues opened in the last 24 hours.
   Flag any labeled "critical" or "urgent".

4. **Deploy Status**: Check the latest deploy. Report whether it succeeded
   or failed. If failed, include the error summary.

5. **Action Items**: Based on the above, list the top 3 things that need
   attention today, ranked by urgency.

Format the output as a concise Slack message. Post to #team-standup.
If nothing notable happened overnight, post "All clear — no overnight changes."
```

**Trigger:** Schedule — daily at 8:00 AM on weekdays
**Connectors:** GitHub, Slack

---

## Backlog Triage

Keep your issue tracker clean and categorized without manual effort.

```markdown
---
name: backlog-triage
description: Nightly issue triage with labeling and assignment
---

# Backlog Triage

## Prompt

Triage all issues opened in the last 24 hours:

1. **Read** each new issue title, body, and any linked code references.

2. **Label** each issue:
   - By type: bug, feature, enhancement, question, documentation
   - By area: match file paths mentioned to CODEOWNERS areas
   - By priority: critical (production broken), high (blocking work),
     medium (should fix this sprint), low (nice to have)

3. **Assign** to the team member who owns the relevant code area
   based on CODEOWNERS. If no clear owner, assign to the team lead.

4. **Post a summary** to #dev-standup on Slack:
   - New issues count by priority
   - Issues assigned vs. needing manual triage
   - Any critical issues that need immediate attention

5. If no new issues were opened, post:
   "No new issues in the last 24 hours. Backlog is current."
```

**Trigger:** Schedule — every weeknight at 10:00 PM
**Connectors:** GitHub, Slack, Linear (optional)

---

## Documentation Drift Detection

Catch when code changes make documentation outdated.

```markdown
---
name: docs-drift
description: Weekly scan for documentation that has drifted from code
---

# Documentation Drift Detection

## Prompt

Scan all pull requests merged in the past 7 days and check for documentation drift:

1. For each merged PR, identify modified functions, API endpoints,
   configuration options, CLI flags, and environment variables.

2. Search documentation files (README.md, docs/, wiki/, any .md files)
   for references to the modified items.

3. For each stale reference found:
   - Note the doc file, line number, and what changed
   - Draft an updated version of the relevant section

4. If stale references are found, open a pull request titled
   "docs: update references drifted by recent changes" with:
   - A summary of what drifted and why
   - The corrected documentation

5. If no drift detected, log: "Weekly docs check — all documentation
   is current with merged code changes."
```

**Trigger:** Schedule — weekly on Monday at 9:00 AM
**Connectors:** GitHub

---

## PR Code Review

Automated first-pass review on every new pull request.

```markdown
---
name: pr-review
description: Automated code review on new pull requests
---

# PR Code Review

## Prompt

Review this pull request against the team's standards:

1. **Security**: Check for SQL injection, XSS, command injection,
   hardcoded secrets, and OWASP Top 10 vulnerabilities.
   Severity labels: critical, warning, info.

2. **Performance**: Flag N+1 queries, missing indexes on new DB columns,
   unbounded loops, large allocations in hot paths.

3. **Testing**: Verify new code has corresponding tests. Flag untested
   branches and edge cases. Check that test names describe behavior.

4. **Style**: Check against project conventions in CLAUDE.md.
   Only flag clear violations, not nitpicks.

5. **Summary**: Add a top-level review comment with:
   - Pass/fail status (fail if any critical security issues)
   - Count of findings by category and severity
   - One-line summary of the change's purpose

Leave inline comments on specific lines. Be direct and constructive.
Do not comment on things that are fine.
```

**Trigger:** GitHub — `pull_request.opened`, filter: `is_draft = false`
**Connectors:** GitHub

---

## Deploy Verification

Smoke-test production after every deploy.

```markdown
---
name: deploy-verify
description: Post-deploy smoke test and regression check
---

# Deploy Verification

## Prompt

Run post-deploy verification:

1. **Health Check**: Hit the /health endpoint. Confirm HTTP 200 and
   response time under 500ms.

2. **Error Scan**: Pull error logs from the last 15 minutes.
   Compare error rate to the 24-hour baseline. Flag if error rate
   increased by more than 20%.

3. **Recent Commits**: List commits included in this deploy.
   For each, check if the related tests passed in CI.

4. **Regression Check**: If error rate spiked, correlate new errors
   with the deployed commits. Identify the most likely culprit.

5. **Report**: Post to #releases:
   - Deploy status: healthy / degraded / failing
   - Error rate: current vs. baseline
   - Commits included
   - If degraded/failing: suspected cause and recommended action

If the deploy is failing, also open a GitHub issue titled
"Production regression after deploy [timestamp]" with the analysis.
```

**Trigger:** API — called from your CD pipeline after deploy completes
**Connectors:** GitHub, Slack

---

## Dependency Update & Security Audit

Keep dependencies fresh and vulnerabilities patched.

```markdown
---
name: dependency-audit
description: Weekly dependency update and security vulnerability scan
---

# Dependency Update & Security Audit

## Prompt

Audit project dependencies:

1. **Vulnerability Scan**: Run the project's dependency audit command
   (npm audit, pip audit, cargo audit, etc.). List all known
   vulnerabilities with severity.

2. **Outdated Packages**: List dependencies more than 2 major versions
   behind or with known deprecation notices.

3. **Update Strategy**: For each vulnerability or major outdated package:
   - Check if updating breaks any tests
   - If safe, create an update PR with the change
   - If breaking, document what needs manual attention

4. **Summary**: Post to #engineering:
   - Vulnerabilities found (critical/high/medium/low)
   - Packages updated automatically
   - Packages needing manual intervention
   - Link to any opened PRs

If no vulnerabilities and all packages are current, post:
"Weekly dependency audit — all clear, no action needed."
```

**Trigger:** Schedule — weekly on Wednesday at 6:00 AM
**Connectors:** GitHub, Slack

---

## Daily Research Digest

Automated research on topics relevant to your project.

```markdown
---
name: research-digest
description: Daily research digest on specified topics
---

# Daily Research Digest

## Prompt

Research the following topics and create a daily digest:

Topics: [AI/ML developments, JavaScript ecosystem, security advisories]

For each topic:
1. Search for notable developments in the last 24 hours
2. Filter for items relevant to our tech stack
3. Summarize each finding in 2-3 sentences

Format the digest as:
- **Executive Summary** (3-4 sentences, most important items)
- **Key Findings** (5-7 bullet points with source links)
- **Action Items** (anything that requires team attention)

Email the digest to [team-lead@company.com].
If nothing notable was found, send a one-line "No significant updates today."
```

**Trigger:** Schedule — daily at 7:00 AM
**Connectors:** Gmail or Slack

---

## Release Notes Generator

Automatically generate release notes when a release is published.

```markdown
---
name: release-notes
description: Generate release notes from merged PRs on release publish
---

# Release Notes Generator

## Prompt

Generate release notes for this release:

1. List all PRs merged since the previous release tag.

2. Categorize each PR:
   - Features (new functionality)
   - Fixes (bug fixes)
   - Performance (speed/efficiency improvements)
   - Breaking Changes (anything requiring user migration)
   - Internal (refactoring, CI, dependencies)

3. For each entry, write a one-line user-facing description.
   Use the PR title as a starting point but rewrite for clarity.
   Link to the PR number.

4. If there are breaking changes, add a **Migration Guide** section
   with step-by-step upgrade instructions.

5. Update the release body on GitHub with the generated notes.
```

**Trigger:** GitHub — `release.published`
**Connectors:** GitHub

---

## Stale Branch Cleanup

Keep the repository tidy by flagging abandoned branches.

```markdown
---
name: stale-branch-cleanup
description: Weekly cleanup of stale branches with no recent activity
---

# Stale Branch Cleanup

## Prompt

Audit repository branches for staleness:

1. List all remote branches except main, master, develop, and
   release/* branches.

2. For each branch, check:
   - Last commit date
   - Whether it has an open PR
   - Whether it has been merged

3. Categorize:
   - **Merged & deletable**: branch was merged, PR is closed
   - **Stale**: no commits in 30+ days, no open PR
   - **Active**: recent commits or open PR

4. For merged & deletable branches: delete them automatically.

5. For stale branches: open a single issue titled
   "Stale branches — [date]" listing each branch, its last author,
   and last commit date. Tag the authors for review.

6. Post summary to #engineering:
   - Branches deleted (count)
   - Stale branches flagged (count)
   - Link to the issue if any were flagged
```

**Trigger:** Schedule — weekly on Friday at 5:00 PM
**Connectors:** GitHub, Slack

---

## Prompt Writing Best Practices for Routines

Routines run autonomously with no interactive approval. Prompt quality determines outcome quality.

### Do

- **Be explicit about success criteria.** "Review open PRs against the /auth module, check for SQL injection, leave inline comments with severity labels, and add a summary comment with pass/fail" is better than "review PRs."
- **Specify the output format.** Where does the result go? Slack message, GitHub PR, issue, email?
- **Handle the empty case.** What should happen when there's nothing to do? Always include a "nothing to report" path.
- **Include severity or priority logic.** Tell the routine how to rank findings so output is actionable.
- **Use concrete thresholds.** "Flag if error rate increased by more than 20%" beats "flag if errors increased."

### Don't

- **Don't use vague instructions.** "Check for errors" produces inconsistent results.
- **Don't skip the output step.** A routine that analyzes but doesn't report is wasted compute.
- **Don't assume context.** The routine starts fresh each run. Include all necessary context in the prompt.
- **Don't forget edge cases.** What if no PRs were merged? No issues opened? The endpoint is down?

---

## Routine Setup Checklist

Before going live with any routine:

- [ ] Test the prompt with "Run now" at least twice
- [ ] Verify connectors are authorized (GitHub, Slack, etc.)
- [ ] Set appropriate network access (custom allowlist preferred)
- [ ] Add environment variables for any API keys needed
- [ ] Confirm the output destination exists (Slack channel, email, etc.)
- [ ] Set up a way to monitor routine failures (check the runs list)
- [ ] Start with a conservative schedule, then increase frequency

---

## Sample Automated Day Schedule

A complete daily automation setup combining multiple routines:

| Time | Routine | Trigger | Output |
|------|---------|---------|--------|
| 7:00 AM | Research Digest | Schedule | Email digest |
| 8:00 AM | Morning Brief | Schedule | Slack #team-standup |
| 10:00 PM | Backlog Triage | Schedule | Slack #dev-standup |
| On PR open | PR Code Review | GitHub event | PR inline comments |
| On deploy | Deploy Verification | API trigger | Slack #releases |
| Monday 9 AM | Docs Drift Detection | Schedule | GitHub PR |
| Wednesday 6 AM | Dependency Audit | Schedule | Slack #engineering |
| Friday 5 PM | Stale Branch Cleanup | Schedule | GitHub issue |
| On release | Release Notes | GitHub event | GitHub release body |

---

## Community Tools & Plugins for Scheduling

| Tool | Description | Link |
|------|-------------|------|
| **claude-code-scheduler** | Cross-platform scheduler (macOS/Linux/Windows) | [GitHub](https://github.com/jshchnz/claude-code-scheduler) |
| **claude-mcp-scheduler** | Cron-based remote agent prompting with local MCP tools | [GitHub](https://github.com/tonybentley/claude-mcp-scheduler) |
| **comfy-claude-prompt-library** | Collection of Claude Code commands and memories for agentic coding | [GitHub](https://github.com/Comfy-Org/comfy-claude-prompt-library) |

For more scheduling-related plugins (jarvis, discoclaw, AgentSys, ORCH, background-timer, and others), browse the [awesome-claude-code-toolkit](https://github.com/rohitg00/awesome-claude-code-toolkit) plugin catalog.

---

## Further Reading

- [Claude Code Routines docs](https://code.claude.com/docs/en/routines)
- [Scheduled tasks (local)](https://code.claude.com/docs/en/scheduled-tasks)
- [Desktop scheduled tasks](https://code.claude.com/docs/en/desktop-scheduled-tasks)
- [MCP connectors](https://code.claude.com/docs/en/mcp)
- [Claude Code on the web](https://code.claude.com/docs/en/claude-code-on-the-web)
- [awesome-claude-code](https://github.com/hesreallyhim/awesome-claude-code) — Curated skill, hook, and plugin list
- [awesome-claude-code-toolkit](https://github.com/rohitg00/awesome-claude-code-toolkit) — 135 agents, 35+ skills, 176+ plugins
