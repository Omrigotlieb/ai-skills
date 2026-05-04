# Claude Code Routines & Scheduled Agents

Routines let Claude Code run prompts automatically — on a schedule, via API, or in response to GitHub events — without you being at the keyboard. This guide covers all three scheduling tiers, ready-to-use routine prompts, and best practices from the community.

> **Requires:** Claude Code Desktop or CLI on a paid plan (Pro, Max, Team, Enterprise)

## Three Scheduling Tiers

| Method | Where it runs | Needs machine awake? | Setup | Best for |
|--------|--------------|----------------------|-------|----------|
| **`/loop`** | Local session | Yes | `/loop 5m <prompt>` | Polling within an active session (deploy status, CI checks) |
| **Desktop scheduled task** | Local machine | Yes (skips if asleep) | Sidebar → Schedule → New local task | Personal recurring tasks on your dev machine |
| **Cloud routine** | Anthropic infra | No | `/schedule` or [claude.ai/code/routines](https://claude.ai/code/routines) | Team-wide automation that must run reliably |

### Usage Limits (Cloud Routines)

| Plan | Runs per day |
|------|-------------|
| Pro | 5 |
| Max | 15 |
| Team / Enterprise | 25 |

---

## Cloud Routines

Cloud routines run on Anthropic's infrastructure with your laptop closed. They have three trigger types:

### Schedule Triggers

Cron-based (minimum 1-hour interval). Natural language input is converted automatically.

```
Every weekday at 9am        →  0 9 * * 1-5
Every Monday at 8am         →  0 8 * * 1
Every 2 hours               →  0 */2 * * *
First day of month at noon  →  0 12 1 * *
```

### API Triggers

Fire a routine via HTTP POST with a bearer token. Useful for chaining with CI/CD, Zapier, or n8n.

### GitHub Event Triggers

React to pull requests (opened, updated, merged) and releases. Attach connectors for Slack, Linear, or Google Drive output.

### Creating a Routine

**CLI:**
```bash
# Interactive setup
/schedule

# Or the schedule skill directly
claude schedule create
```

**Web UI:**
Visit [claude.ai/code/routines](https://claude.ai/code/routines) → New Routine → configure prompt, repo, trigger, and connectors.

**Desktop:**
Sidebar → Scheduled Tasks → New → choose local or cloud.

---

## Ready-to-Use Routine Prompts

### Morning Standup Prep

**Trigger:** Daily, 8:30am weekdays
**Connectors:** GitHub, Slack

```
Review overnight activity for this repository:
1. List PRs merged since yesterday 5pm
2. List PRs still awaiting review with CI status
3. Summarize new issues opened overnight
4. Flag any failed CI runs on main branch

Post a concise digest to #eng-standup. Format:
- 🟢 Merged: [count] PRs
- 🔍 Awaiting review: [list with CI status]
- 🆕 New issues: [list with labels]
- 🔴 CI failures: [list or "none"]
```

### Nightly Issue Triage

**Trigger:** Daily, 11pm
**Connectors:** GitHub

```
Scan all issues opened today that are unlabeled:
1. Read the issue title and body
2. Apply the most appropriate label (bug, enhancement, question, documentation)
3. If the issue mentions a specific file or module, assign it to the CODEOWNERS for that path
4. If the issue is a duplicate of an existing open issue, comment with a link and add the "duplicate" label

Do not close any issues. Only label and assign.
```

### Weekly Dependency Audit

**Trigger:** Every Monday at 7am
**Connectors:** GitHub

```
Audit dependencies for security and freshness:
1. Run the project's dependency audit command (npm audit / pip audit / cargo audit)
2. Check for outdated packages with known CVEs
3. If vulnerabilities are found, create a single PR titled "chore: fix dependency vulnerabilities [automated]"
   - Update only packages with security advisories
   - Do not bump major versions
   - Include audit output in PR description
4. If no vulnerabilities, do nothing

Post results to #security-alerts if any CVEs found.
```

### Overnight PR Review

**Trigger:** Daily, midnight
**Connectors:** GitHub

```
Review all open PRs labeled "needs-review":
1. For each PR, check:
   - Logic correctness and edge cases
   - Security implications (SQL injection, XSS, auth bypass)
   - Test coverage for new code paths
   - Performance concerns (N+1 queries, memory leaks, blocking calls)
2. Leave inline comments on specific lines where issues are found
3. Use severity labels: 🔴 Critical, 🟡 Warning, 🔵 Suggestion
4. Post a summary comment with an overall verdict:
   - ✅ Ready to merge
   - ⚠️ Needs attention (list issues)
   - 🚫 Needs work (list blockers)
```

### Docs-Drift Detection

**Trigger:** Weekly, Friday at 3pm
**Connectors:** GitHub

```
Detect documentation that has drifted from the code:
1. List all PRs merged this week that changed files in src/
2. For each changed module, check if corresponding docs (README, API docs, docstrings) reference the changed functions or APIs
3. If docs reference functions that were renamed, removed, or had signature changes, open a PR updating the docs
4. Title: "docs: sync documentation with code changes [automated]"
5. Include a table in the PR body: file changed | doc affected | what drifted
```

### Deploy Verification

**Trigger:** GitHub event (release published)
**Connectors:** GitHub, Slack

```
Post-deploy smoke check for the release:
1. Wait 2 minutes for deployment to propagate
2. Check health endpoint returns 200
3. Scan application logs for new error patterns in the last 5 minutes
4. Compare error rate to the 1-hour baseline before deploy
5. Report to #deploys:
   - ✅ Deploy healthy — no new errors detected
   - ⚠️ Elevated errors — [details]
   - 🔴 Health check failed — [details]
```

### PR Babysitting

**Trigger:** `/loop 5m` (session-scoped)

```
Monitor my open PR until it's ready:
1. Check CI status for PR #[number]
2. If all checks pass and no review comments are unresolved:
   - Post "CI green, ready for merge" and stop
3. If a check fails:
   - Read the failure log
   - Attempt a fix and push
   - Continue monitoring
4. If a reviewer leaves comments:
   - Summarize the feedback and stop (I'll handle it)
```

### Code Quality Nightly Report

**Trigger:** Daily, 2am
**Connectors:** GitHub, Slack

```
Run a code quality audit:
1. Run the project linter and type checker
2. Check test coverage — flag any files below 60% coverage
3. Scan for TODO/FIXME comments added in the last 7 days
4. Check for large files (>500 lines) added recently
5. Post a summary to #code-quality:
   - Lint issues: [count]
   - Type errors: [count]
   - Low-coverage files: [list]
   - New TODOs: [list with file:line]
```

### Changelog Draft

**Trigger:** GitHub event (release created) or weekly
**Connectors:** GitHub

```
Generate a changelog draft from merged PRs:
1. Collect all PRs merged since the last release tag
2. Group by conventional commit prefix:
   - feat: → Features
   - fix: → Bug Fixes
   - perf: → Performance
   - docs: → Documentation
   - Other → Maintenance
3. For each entry: one-line summary with PR link and author
4. Create a draft release with the generated notes
5. Do not publish — leave as draft for human review
```

---

## Multi-Agent Routine Patterns

### Split-and-Merge Review

Spawn specialized sub-agents for parallel analysis, then merge results:

```
Review this codebase change with a multi-agent team.

Spawn three parallel reviewers:
1. Security reviewer — focus on auth, injection, data exposure
2. Performance reviewer — focus on queries, caching, algorithmic complexity
3. Test coverage reviewer — focus on missing tests, edge cases, assertions

Each reviewer should return:
- Severity-ranked findings (Critical / Warning / Info)
- Specific file:line references

After all complete, merge findings into a single report sorted by severity.
Verdict: Ready to Merge | Needs Attention | Needs Work
```

### Sequential Pipeline

Chain agents where each builds on the previous output:

```
1. Analyze → understand the feature request and existing code
2. Design → propose architecture with file-level changes
3. Plan → break design into ordered, testable tasks
4. Implement → execute tasks one at a time with tests
5. Verify → run full test suite and review own changes
```

### Headless Batch Processing

For CI/CD integration using `claude -p`:

```bash
# Run headless — no interactive session
claude -p "Review the diff in this PR for security issues. \
  Output JSON: {issues: [{severity, file, line, description}]}" \
  --output-format json
```

---

## Best Practices

### Prompt Design for Routines

1. **One job per routine** — don't combine triage + audit + reporting
2. **Be explicit about output** — say where results go (Slack channel, PR comment, file)
3. **Define the "do nothing" case** — tell the agent what to do when there's nothing to report
4. **Set boundaries** — "do not close issues", "do not merge", "leave as draft"
5. **Include format specs** — structured output makes results scannable

### Operational Hygiene

1. **Set timeouts** — 15 minutes per routine is a good ceiling; split longer tasks
2. **Budget per agent** — a bug in an hourly routine can drain API budget overnight
3. **Use the right model tier** — Sonnet for triage/formatting, Opus for complex reasoning
4. **Log every execution** — maintain an audit trail for when an agent makes a bad call at 3am
5. **File-based state** — store inter-run state in repo files so humans can inspect and agents can resume

### Choosing the Right Tier

| If you need... | Use |
|---------------|-----|
| Quick polling during active work | `/loop` |
| Personal daily task on your machine | Desktop scheduled task |
| Team-wide automation, laptop-independent | Cloud routine |
| CI/CD integration | API trigger or `claude -p` in GitHub Actions |
| React to PRs/releases | GitHub event trigger |

---

## Resources

### Official
- [Automate work with routines — Claude Code Docs](https://code.claude.com/docs/en/routines)
- [Desktop scheduled tasks — Claude Code Docs](https://code.claude.com/docs/en/scheduled-tasks)
- [Common workflows — Claude Code Docs](https://code.claude.com/docs/en/common-workflows)
- [Best practices — Claude Code Docs](https://code.claude.com/docs/en/best-practices)

### Anthropic Engineering
- [Effective context engineering for AI agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)
- [Effective harnesses for long-running agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents)
- [2026 Agentic Coding Trends Report](https://resources.anthropic.com/2026-agentic-coding-trends-report)

### Community Guides
- [Claude Code Routines Practical Guide — builder.io](https://www.builder.io/blog/claude-code-routines)
- [Claude Code Routines in Practice — ShareUHack](https://www.shareuhack.com/en/posts/claude-code-routines-2026)
- [8 Routine Prompts + What Breaks — Linas Substack](https://linas.substack.com/p/claude-code-routines-guide)
- [5 Setups That Work While You Sleep — Medium](https://alirezarezvani.medium.com/claude-code-routines-5-setups-that-work-while-you-sleep-ee779b5e6924)
- [9 Parallel Agents for Code Review — hamy.xyz](https://hamy.xyz/blog/2026-02_code-reviews-claude-subagents)
- [Stop Confusing /schedule, /loop, and Cron — wmedia.es](https://wmedia.es/en/tips/claude-code-schedule-vs-loop-vs-cron)

### Tools
- [tonybentley/claude-mcp-scheduler](https://github.com/tonybentley/claude-mcp-scheduler) — Self-hosted scheduling via Claude API + MCP
- [jshchnz/claude-code-scheduler](https://github.com/jshchnz/claude-code-scheduler) — Lightweight cron wrapper for `claude -p`
