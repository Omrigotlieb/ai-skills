# Routines & Scheduled Tasks for Claude Code

Skills and patterns for automating recurring workflows with Claude Code. These routines run on schedules or in response to events, handling tasks that would otherwise eat into focused development time.

> **Sources:** Patterns collected from Anthropic docs, GitHub Agentic Workflows, community workflows (OpenClaw, awesome-continuous-ai), and practitioner write-ups from Reddit and DEV Community.

---

## Why Routines Matter

Most developer time lost to overhead is not from any single task but from dozens of small recurring ones: checking CI, triaging email, reviewing PRs, scanning for stale docs. Routines automate the predictable parts so you can focus on the unpredictable ones.

## How Routines Work in Claude Code

Claude Code supports scheduled tasks and event-driven routines:

```bash
# Create a scheduled task
claude schedule create --name "morning-briefing" --cron "0 7 * * 1-5" --prompt "..."

# Trigger-based (GitHub events)
# Configured via Claude Code Routines with GitHub/API triggers
```

**Trigger types:**
- **Cron schedule** -- runs at fixed times (e.g., `0 7 * * 1-5` for weekday 7 AM)
- **GitHub events** -- `pull_request.opened`, `issues.opened`, `push`, `pull_request.closed`
- **API triggers** -- webhook endpoints that fire routines from monitoring tools
- **Loop-based** -- `/loop` patterns that poll until a condition is met

---

## Routine Categories

| Category | Routines | Description | Link |
|----------|----------|-------------|------|
| **Morning** | 3 | Start-of-day briefings and triage | [View](#morning-routines) |
| **Continuous** | 4 | Always-on monitoring and review | [View](#continuous-routines) |
| **End-of-Day** | 2 | Wrap-up and handoff | [View](#end-of-day-routines) |
| **Weekly** | 4 | Health checks and audits | [View](#weekly-routines) |
| **Event-Driven** | 3 | React to repo/infrastructure events | [View](#event-driven-routines) |

---

## Morning Routines

### Morning Briefing

The single most adopted routine across all sources. Aggregates signals from email, calendar, GitHub, and Slack into a prioritized summary.

**Schedule:** Weekdays at 7-9 AM
**Impact:** Developers report going from 45 minutes of dashboard-checking to 3 minutes of reading a summary.

```markdown
# Morning Briefing Routine

Scan the following sources from the last 24 hours and produce a prioritized morning briefing:

## Sources
- Email: flag replies needed, deadline mentions, urgent threads
- Calendar: today's meetings, conflicts, prep needed
- GitHub: open PRs needing my review, failing CI, new issues assigned to me
- Slack: unread mentions, threads I'm tagged in

## Output Format
### Needs Action (do today)
- [item with source and one-line context]

### Awareness (no action needed yet)
- [item]

### Today's Schedule
- [time] [meeting] -- [one-line prep note]

## Rules
- Skip newsletters, automated notifications, and anything purely informational
- Flag anything with a deadline within 48 hours
- Keep each item to one line
```

See [morning-briefing.md](morning-briefing.md) for the full implementation guide.

---

### Email Triage

Classifies incoming email and drafts replies without sending.

**Schedule:** Every 30 minutes or once at 7 AM
**Key principle:** Never auto-send. Draft only.

```markdown
# Email Triage Routine

Fetch unread emails from the last cycle. For each:

1. Classify as: URGENT / ACTION-REQUIRED / FYI / NEWSLETTER
2. For URGENT and ACTION-REQUIRED:
   - Draft a reply (do NOT send)
   - Flag the thread
3. For FYI: summarize in one line
4. For NEWSLETTER: archive silently

Output a summary grouped by category. Include draft reply previews for urgent items.
```

---

### Standup Generator

Builds a standup update from git history and issue tracker activity.

**Schedule:** Weekdays at 8:45 AM (before standup)

```markdown
# Standup Generator

Generate my standup update from yesterday's activity.

## Sources
- Git log: commits by me since yesterday
- GitHub: PRs I opened, reviewed, or merged
- Issues: status changes on issues assigned to me

## Output Format
**Yesterday:** [2-3 bullet points of what was accomplished]
**Today:** [2-3 bullet points based on open PRs and assigned issues]
**Blockers:** [any PRs waiting on review > 24h, failing CI, unresolved questions]

Keep it under 100 words. Use past tense for yesterday, future tense for today.
```

---

## Continuous Routines

### Automated PR Review

Reviews pull requests on open/update events. The most impactful continuous routine for team code quality.

**Trigger:** `pull_request.opened` or `pull_request.synchronize`
**Key pattern:** Review as a senior engineer, not a linter.

```markdown
# PR Review Routine

Review this pull request as a senior engineer. Focus on:

1. **Logic errors** -- incorrect conditions, off-by-ones, race conditions
2. **Edge cases** -- null/empty inputs, boundary values, error paths
3. **Security** -- injection, auth bypass, data exposure
4. **Performance** -- N+1 queries, unbounded loops, missing indexes
5. **Maintainability** -- unclear names, missing abstractions, dead code

## Rules
- Ignore purely stylistic preferences (formatting, import order)
- For each issue, explain WHY it matters and suggest a concrete fix
- Rate severity: Critical / High / Medium / Low
- If the PR is clean, say so briefly -- don't manufacture feedback

## Output
Post inline comments on specific lines. End with a summary verdict:
APPROVE / REQUEST CHANGES / COMMENT
```

See [pr-review-automation.md](pr-review-automation.md) for advanced patterns including the "Review Council" multi-pass approach.

---

### CI/CD Watch

Monitors build health and alerts only when something needs attention.

**Schedule:** Every 30 minutes during work hours
**Key principle:** Silent unless something is wrong (heartbeat pattern).

```markdown
# CI/CD Watch Routine

Check the following and ONLY report if action is needed:

1. PRs with failing CI -- include error summary and likely cause
2. PRs waiting for review > 24 hours -- mention reviewer
3. PRs with unresolved review comments > 48 hours
4. Deployments that failed in the last cycle

If everything is green, output nothing. Do not notify for passing builds.
```

---

### Issue Triage

Auto-labels and routes new issues.

**Trigger:** `issues.opened`

```markdown
# Issue Triage Routine

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

---

### PR Babysitting (Loop Pattern)

Watches a PR from push through merge, handling CI and review feedback iteratively.

**Trigger:** Manual via `/loop` after pushing a PR

```markdown
# PR Babysitting Loop

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

---

## End-of-Day Routines

### Day Wrap-Up

Summarizes the day's work and prepares tomorrow's priorities.

**Schedule:** Weekdays at 5-6 PM

```markdown
# Day Wrap-Up Routine

Generate an end-of-day summary:

## Accomplished Today
- [From git log, PR activity, and issue updates]

## Decisions Made
- [Any architectural or design decisions from PR comments, issues, or commits]

## Open Items
- [PRs still in review]
- [Issues started but not finished]
- [Questions asked but not answered]

## Tomorrow's Priorities
1. [Highest-impact item based on deadlines and dependencies]
2. [Next item]
3. [Next item]

Keep the summary under 200 words. Focus on outcomes, not activity.
```

See [end-of-day-wrapup.md](end-of-day-wrapup.md) for the full guide.

---

### Commit Summary

Generates a human-readable changelog from the day's commits.

**Schedule:** Weekdays at 6 PM

```markdown
# Commit Summary Routine

Summarize today's commits into a readable changelog:

1. Group commits by feature/area
2. Collapse fixup/WIP commits into their parent feature
3. Write one line per logical change
4. Note any breaking changes or API modifications

Format as a bulleted list, not raw commit messages.
```

---

## Weekly Routines

### Repository Health Check

Comprehensive weekly audit of repo hygiene.

**Schedule:** Monday at 7 AM

```markdown
# Weekly Repository Health Check

Audit the repository and produce a health report:

## Checks
1. **Dependency health** -- outdated packages, known vulnerabilities (npm audit / pip audit)
2. **Stale PRs** -- open > 7 days with no activity
3. **Stale branches** -- branches with no commits in 30+ days
4. **Test coverage** -- current percentage, trend vs last week
5. **CI reliability** -- flaky test rate, average build time
6. **Documentation drift** -- APIs changed in merged PRs that touch files without matching doc updates

## Output
### Health Score: [A/B/C/D/F]

**Action Items (prioritized):**
1. [Most urgent item]
2. [Next item]
...

**Trends:**
- Coverage: [up/down/stable] at [X%]
- Build time: [Xs average]
- Open PRs: [N] (was [M] last week)
```

See [weekly-health-check.md](weekly-health-check.md) for the full implementation.

---

### Documentation Drift Detection

Finds docs that have fallen out of sync with code changes.

**Schedule:** Weekly (Friday)

```markdown
# Documentation Drift Detection

Scan PRs merged this week. For each:

1. Identify changed public APIs, function signatures, config options
2. Search for documentation that references the changed items
3. If docs exist but don't reflect the change, open a PR updating them
4. If no docs exist for a new public API, flag it

Output a list of documentation gaps with file paths and specific mismatches.
```

---

### Dependency Audit

Checks for security vulnerabilities and outdated packages.

**Schedule:** Monday at 7 AM

```markdown
# Dependency Audit Routine

Run a full dependency audit:

1. Check for known vulnerabilities (CVEs)
2. List packages more than 2 major versions behind
3. Identify unused dependencies (installed but not imported)
4. Check license compatibility

## Output
### Critical (fix this week)
- [package]: [vulnerability description]

### Update Recommended
- [package]: [current] -> [latest] ([breaking changes summary])

### Cleanup
- [unused packages that can be removed]
```

---

### Team Digest

Weekly summary of team activity for async teams.

**Schedule:** Monday at 8 AM

```markdown
# Weekly Team Digest

Compile a team activity digest for the past week:

## By Area
- [Area 1]: [what shipped, what's in progress]
- [Area 2]: [what shipped, what's in progress]

## Key Metrics
- PRs merged: [N]
- Issues closed: [N]
- Issues opened: [N]
- Average PR review time: [X hours]

## Highlights
- [Notable accomplishments]
- [Important decisions made in PR discussions]

## Coming Up
- [PRs likely to merge this week]
- [Upcoming deadlines]

Keep it scannable. Use bullet points, not paragraphs.
```

---

## Event-Driven Routines

### Deploy Verification

Runs smoke checks after a deployment.

**Trigger:** Post-deploy webhook

```markdown
# Deploy Verification Routine

After deployment to [environment]:

1. Run smoke tests against the deployed endpoint
2. Check error logs for new error patterns (last 5 minutes vs baseline)
3. Verify key metrics are within normal range
4. Check for any rollback indicators

## Output
**Status:** GO / NO-GO / WATCH

If NO-GO: describe the issue and suggest whether to rollback or hotfix.
If WATCH: describe what looks unusual and set a 15-minute re-check.
```

---

### Alert Triage

Correlates production alerts with recent changes.

**Trigger:** API webhook from monitoring tool

```markdown
# Alert Triage Routine

An alert has fired: [alert details]

1. Parse the stack trace or error message
2. Search git log for recent commits touching the affected files
3. Check if any PRs were merged in the last 24 hours that could cause this
4. Assess impact: how many users affected, is there a workaround?

## Output
**Likely cause:** [commit/PR with explanation]
**Impact:** [scope and severity]
**Suggested action:** [rollback / hotfix / monitor]

If a fix is straightforward, open a draft PR with the proposed change.
```

---

### Library Port

Automatically ports changes across parallel SDKs or packages.

**Trigger:** `pull_request.closed` (merged) in source repo

```markdown
# Library Port Routine

A PR was merged in [source SDK]. Port the changes:

1. Read the merged PR diff
2. Identify the equivalent files in [target SDK]
3. Apply the logical change (not a literal diff -- adapt to target language idioms)
4. Run the target SDK's test suite
5. Open a PR in the target repo with a reference to the source PR

If the port requires architectural decisions, flag for human review instead of guessing.
```

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

## Novel Approaches Worth Exploring

### The Executive Cabinet

Run multiple specialized agents (CTO, Security Lead, Docs Lead) that each own a domain. A router agent triages incoming tasks to the right specialist. Uses tmux for parallel sessions and git worktrees for isolation.

*Source: [DEV Community -- 6 AI Agents for 15 Side Projects](https://dev.to/razbakov/i-built-an-executive-team-of-6-ai-agents-to-manage-my-15-side-projects-4k0i)*

### Self-Improving Agent

A weekly meta-routine that audits the agent's own effectiveness: token efficiency, memory hygiene, response quality. Proposes one workflow improvement per week.

### Model Routing for Cost

Route tasks to appropriate model tiers: Haiku for monitoring heartbeats, Sonnet for analysis, Opus for high-stakes decisions. Dramatically reduces API costs while maintaining quality where it matters.

---

## Getting Started

### Starter Pack: 3 Routines That Cover 80% of Value

1. **Morning Briefing** (daily, 7 AM) -- know what matters before you open your laptop
2. **PR Review** (on PR opened) -- catch issues before they reach main
3. **Weekly Health Check** (Monday, 7 AM) -- prevent slow decay of repo hygiene

### Implementation Steps

1. Pick one routine from the starter pack
2. Copy the prompt template above
3. Customize sources and output format for your project
4. Set up the schedule: `claude schedule create --name "..." --cron "..." --prompt "..."`
5. Run it manually first to verify output quality
6. Iterate on the prompt based on the first few runs
7. Add the next routine once the first is stable

---

## Resources

### Official
- [Claude Code Routines Documentation](https://code.claude.com/docs/en/routines)
- [Claude Code Scheduled Tasks](https://code.claude.com/docs/en/scheduled-tasks)

### Community
- [awesome-continuous-ai](https://github.com/githubnext/awesome-continuous-ai) -- Curated patterns for continuous AI workflows
- [OpenClaw 25 Workflows](https://gist.github.com/alirezarezvani/bb68f4f7444fcab00beb6ded31eeb028) -- Real-world routine prompts
- [OpenClaw 20 Real Workflows After 50 Days](https://gist.github.com/velvet-shark/b4c6724c391f612c4de4e9a07b0a74b6) -- Practitioner experience reports
- [PR Babysitting Pattern](https://www.solberg.is/babysit-pr) -- Detailed loop-based PR management
- [GitHub Agentic Workflows](https://github.blog/ai-and-ml/automate-repository-tasks-with-github-agentic-workflows/) -- GitHub-native automation

### Related Sections in This Repo
- [Workflows](../../workflows/README.md) -- Manual workflow patterns
- [Hooks](../../hooks/README.md) -- Event-driven automation via hooks
- [Tips](../../tips/README.md) -- General productivity patterns
