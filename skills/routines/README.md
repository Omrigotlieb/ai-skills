# Routines & Scheduled Agents

Patterns for automating recurring developer workflows with Claude Code. These routines run on cron schedules or in response to events, handling tasks that would otherwise eat into focused development time.

> **Sources:** [Claude Code docs](https://code.claude.com/docs/en/routines), [GitHub Agentic Workflows](https://github.blog/ai-and-ml/automate-repository-tasks-with-github-agentic-workflows/), community patterns from Reddit r/ClaudeAI, DEV Community, and practitioner write-ups.

---

## Why Routines Matter

Most developer overhead comes from dozens of small recurring tasks: checking CI, triaging email, reviewing PRs, scanning for stale docs. Routines automate the predictable parts so you can focus on the unpredictable ones.

## Three Scheduling Tiers

Claude Code offers three levels of automation, each suited to different use cases:

| Feature | Cloud Routines | Desktop Tasks | /loop |
|---------|----------------|---------------|-------|
| Runs on | Anthropic cloud | Your machine | Your machine |
| Requires machine on | No | Yes | Yes |
| Requires open session | No | No | Yes |
| Local file access | No (fresh clone) | Yes | Yes |
| Min interval | 1 hour | 1 minute | 1 minute |
| Permission prompts | No (autonomous) | Configurable | Inherits from session |

### Cloud Routines (unattended, reliable)

```bash
# Create via CLI
/schedule daily PR review at 9am

# Or with explicit cron
claude schedule create --name "morning-briefing" --cron "0 7 * * 1-5" --prompt "..."

# Manage
/schedule list
/schedule run morning-briefing
```

Routines run on Anthropic's infrastructure -- they work when your laptop is closed. Three trigger types: **scheduled** (cron), **API** (HTTP POST webhook), and **GitHub** (PR or release events).

### Desktop Scheduled Tasks (local, persistent)

Tasks stored at `~/.claude/scheduled-tasks/<name>/SKILL.md`. Run on your machine with full local file access. Persist across app restarts.

### Session /loop (quick polling)

```bash
/loop 5m check CI status for PR #123 and fix any failures
/loop check the deploy          # Claude picks interval dynamically
/loop                           # runs built-in maintenance or custom loop.md
/loop 20m /babysit-pr 1234      # run a command repeatedly
```

Auto-expires after 7 days. Max 50 concurrent tasks per session.

### Custom Default Loop via loop.md

Place at `.claude/loop.md` (project) or `~/.claude/loop.md` (user). When you run bare `/loop` with no prompt, this replaces the built-in maintenance prompt:

```markdown
# .claude/loop.md
Check the `release/next` PR. If CI is red, pull the failing job log,
diagnose, and push a minimal fix. If new review comments have arrived,
address each one and resolve the thread. If everything is green and
quiet, say so in one line.
```

### Recommended Intervals

| Urgency | Interval | Use Case |
|---------|----------|----------|
| Urgent | 2-5m | Post-deployment regression testing, service health checks |
| Important | 10-15m | CI monitoring, PR comment follow-ups |
| Routine | 30m-2h | Code quality, security scans, log trends |
| Low Frequency | 24h+ | Dependency audits, daily reports, branch cleanup |

---

## Routine Catalog

### Daily Routines

| Routine | Schedule | Description | Link |
|---------|----------|-------------|------|
| **Morning Briefing** | Weekdays 7 AM | Aggregates email, calendar, GitHub, Slack into a prioritized summary | [View](morning-briefing.md) |
| **Standup Generator** | Weekdays 8:45 AM | Builds standup update from git log and issue tracker | [View](standup-generator.md) |
| **End-of-Day Wrap-Up** | Weekdays 5 PM | Summarizes work, captures decisions, sets tomorrow's priorities | [View](end-of-day-wrapup.md) |

### Continuous Routines

| Routine | Trigger | Description | Link |
|---------|---------|-------------|------|
| **PR Review Automation** | PR opened/updated | Reviews PRs for logic errors, security, performance | [View](pr-review-automation.md) |
| **Codebase Guardian** | Daily or on push | Monitors code quality, test coverage, and technical debt | [View](codebase-guardian.md) |

### Weekly Routines

| Routine | Schedule | Description | Link |
|---------|----------|-------------|------|
| **Repository Health Check** | Monday 7 AM | Audits dependencies, stale PRs, branches, coverage, CI reliability | [View](weekly-health-check.md) |
| **Security Scan** | Monday 7 AM | Scans for vulnerabilities, exposed secrets, dependency CVEs | [View](security-scan.md) |

---

## Prompt Patterns for Routines

### The Heartbeat Pattern (Silent Unless Wrong)

Best for monitoring routines. Prevents notification fatigue.

```markdown
Check [sources]. ONLY output if something requires human attention.
If everything is normal, produce no output.
```

### The Structured Triage Pattern

Forces categorized decision-making instead of blind action.

```markdown
For each finding, categorize:
| Verdict | Criteria | Action |
|---------|----------|--------|
| Fix | Clear issue, clear fix | Apply and explain |
| Dismiss | False positive or style | Explain why |
| Escalate | Needs human judgment | Flag with context |
```

### The Authority-Framing Pattern

Improves output quality by setting the review perspective.

```markdown
Review this as a [senior engineer / security auditor / performance specialist].
Focus on [specific concerns]. Ignore [specific non-concerns].
```

### The Five-Element Spec

Ensures routine prompts are complete and unambiguous.

```markdown
Context: [what the agent knows and has access to]
Task: [what to do]
Constraints: [boundaries and limitations]
Edge Cases: [what to handle gracefully]
Acceptance Criteria: [what success looks like]
```

---

## Getting Started

### Starter Pack: 3 Routines That Cover 80% of Value

1. **Morning Briefing** (daily, 7 AM) -- know what matters before you open your laptop
2. **PR Review** (on PR opened) -- catch issues before they reach main
3. **Weekly Health Check** (Monday, 7 AM) -- prevent slow decay of repo hygiene

### Implementation Steps

1. Pick one routine from the starter pack
2. Copy the prompt template from its detail page
3. Customize sources and output format for your project
4. Set up the schedule: `claude schedule create --name "..." --cron "..." --prompt "..."`
5. Run it manually first to verify output quality
6. Iterate on the prompt based on the first few runs
7. Add the next routine once the first is stable

---

## Event-Driven Patterns

### PR Babysitting (Loop Pattern)

Watches a PR from push through merge, handling CI and review feedback iteratively. One of the most popular community patterns.

**Trigger:** Manual via `/loop` after pushing a PR

```markdown
Monitor PR #[number] and iterate until merged or escalated:

1. Check CI status
2. If CI fails: read logs, diagnose, apply fix, push
3. Check for new review comments
4. For each comment, triage:
   | Verdict | Criteria | Action |
   |---------|----------|--------|
   | Fix | Valid issue, clear fix | Apply fix, push |
   | Dismiss | Style preference or false positive | Reply explaining why |
   | Escalate | Architectural concern, needs discussion | Flag for human |
5. If all checks pass and approved: report ready to merge

Max 3 fix iterations per cycle. If still failing after 3, escalate.
Do NOT merge automatically.
```

*Source: [PR Babysitting Pattern](https://www.solberg.is/babysit-pr)*

### Issue Triage

Auto-labels and routes new issues.

**Trigger:** `issues.opened`

```markdown
For each new issue:

1. Read the title and body
2. Apply labels based on content:
   - bug / feature / question / documentation
   - Area labels based on files/components mentioned
   - Priority: P0 (crash/data loss), P1 (broken feature), P2 (degraded), P3 (nice-to-have)
3. If the issue lacks reproduction steps for a bug, comment asking for them
4. If the issue references a specific file or module, suggest an assignee based on git blame

Do NOT close issues automatically. Labeling and routing only.
```

### Deploy Verification

Runs smoke checks after a deployment.

**Trigger:** Post-deploy webhook

```markdown
After deployment to [environment]:

1. Run smoke tests against the deployed endpoint
2. Check error logs for new error patterns (last 5 minutes vs baseline)
3. Verify key metrics are within normal range
4. Check for any rollback indicators

**Status:** GO / NO-GO / WATCH

If NO-GO: describe the issue and suggest whether to rollback or hotfix.
If WATCH: describe what looks unusual and set a 15-minute re-check.
```

---

## Advanced Patterns

### Model Routing for Cost

Route tasks to appropriate model tiers to balance cost and quality:

- **Haiku** for monitoring heartbeats (CI checks, log scanning)
- **Sonnet** for analysis and triage (PR review, issue classification)
- **Opus** for high-stakes decisions (security review, architecture changes)

### The Executive Cabinet

Run multiple specialized agents that each own a domain (Security Lead, Docs Lead, Performance Lead). A router agent triages incoming tasks to the right specialist.

*Source: [DEV Community -- AI Agents for Side Projects](https://dev.to/razbakov/i-built-an-executive-team-of-6-ai-agents-to-manage-my-15-side-projects-4k0i)*

### Self-Improving Meta-Routine

A weekly routine that audits the agent's own effectiveness: token usage, false positive rate, and response quality. Proposes one workflow improvement per week.

```markdown
Review this week's routine outputs:

1. Which routine generated the most noise vs signal?
2. Which findings were dismissed by humans? (false positives)
3. Which issues were missed that humans caught manually?
4. Token usage per routine -- any optimization opportunities?

Propose ONE specific improvement to the worst-performing routine.
```

---

## Prompt Writing Best Practices for Routines

1. **Be explicit about success criteria** -- instead of "check for issues," write "run npm audit, filter for severity high or critical, and open a GitHub issue for each finding"
2. **Tell Claude what NOT to do** -- "Do not merge any PRs. Do not push to main. Only push to claude/ branches"
3. **Define alert conditions** -- notify only on anomalies to avoid information overload
4. **Specify action plans** -- "Open a PR directly if it is fixable"
5. **Limit scope** -- "Scan the src/ directory" instead of "Scan all files"
6. **Set termination conditions** -- "Stop after 3 consecutive passes"
7. **Add error handling** -- "If npm audit fails to run, create a GitHub issue describing the error instead of silently exiting"
8. **Start with one routine** for your most repetitive task. Run it for two weeks. Calibrate the prompt. Then add a second.

---

## Resources

### Official
- [Claude Code Routines Documentation](https://code.claude.com/docs/en/routines)
- [Claude Code Scheduled Tasks](https://code.claude.com/docs/en/scheduled-tasks)
- [Build a Daily Briefing](https://claude.com/resources/use-cases/build-a-daily-briefing-across-your-tools)
- [anthropics/claude-code-security-review](https://github.com/anthropics/claude-code-security-review) -- GitHub Action for automated PR security review

### Community Routine Collections
- [PR Babysitting Pattern](https://www.solberg.is/babysit-pr) -- Loop-based PR management
- [babysit-pr skill](https://gist.github.com/tilomitra/e0dca29b3a63b5b5aba62c1baeaa27b4) -- Full implementation by Tilo Mitra
- [OpenClaw 25 Real Workflows](https://gist.github.com/alirezarezvani/bb68f4f7444fcab00beb6ded31eeb028) -- Practitioner routine prompts
- [20 Loop Prompts Collection](https://help.apiyi.com/en/claude-code-loop-useful-prompts-collection-automation-guide-en.html) -- Field-tested /loop prompts
- [5 Production Workflows + MCP Setup](https://www.arcade.dev/blog/claude-code-routines-mcp-setup/) -- Enterprise-grade patterns from Arcade
- [8 Production Prompts](https://linas.substack.com/p/claude-code-routines-guide) -- Linas Substack guide

### Scheduling Tools
- [claude-code-scheduler](https://github.com/jshchnz/claude-code-scheduler) -- Natural language scheduling plugin with OS-native cron
- [claudecron](https://github.com/phildougherty/claudecron) -- MCP server with file-watch, dependency, and hook triggers
- [claude-tasks](https://github.com/kylemclaren/claude-tasks) -- Go-based TUI scheduler with Discord/Slack webhooks

### Real-World Implementations
- [claude-skills-weekly](https://github.com/er1chu/claude-skills-weekly) -- Monday/daily/Friday productivity system with launchd
- [routine-templates](https://github.com/Fisher521/routine-templates) -- 5 production-grade prompt templates
- [GitHub Agentic Workflows](https://github.blog/ai-and-ml/automate-repository-tasks-with-github-agentic-workflows/) -- GitHub-native automation

### Related Sections in This Repo
- [Workflows](../../workflows/README.md) -- Manual workflow patterns
- [Hooks](../../hooks/README.md) -- Event-driven automation via hooks
- [Tips](../../tips/README.md) -- General productivity patterns
