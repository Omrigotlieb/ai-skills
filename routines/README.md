# Claude Code Routines & Scheduled Tasks

Routines are autonomous agents that run on a schedule, in response to events, or via API triggers. Unlike interactive workflows (which require you at the keyboard), routines execute unattended and report results through connectors like Slack, GitHub, or email.

This guide covers the three automation tiers, battle-tested routine patterns, and the repositories worth following.

> Links last verified: 2026-05-03

## Quick Navigation

- [Automation Tiers](#automation-tiers)
- [Daily Standup & Briefing](#daily-standup--briefing)
- [Code Review Automation](#code-review-automation)
- [Repository Health](#repository-health)
- [Dependency & Security](#dependency--security)
- [Documentation Maintenance](#documentation-maintenance)
- [PR Management](#pr-management)
- [Notification Triage](#notification-triage)
- [Deploy & Operations](#deploy--operations)
- [Memory & Knowledge](#memory--knowledge)
- [Creative & Unusual](#creative--unusual)
- [Best Practices](#best-practices)
- [Repositories & Resources](#repositories--resources)

---

## Automation Tiers

Claude Code offers three levels of automation. Pick the one that matches your needs:

| Tier | Where It Runs | Trigger Types | Requires Machine On? |
|------|--------------|---------------|---------------------|
| **Cloud Routines** | Anthropic infrastructure | Cron, API (HTTP POST), GitHub events | No |
| **Desktop Scheduled Tasks** | Local machine (Desktop app) | Cron | Yes (app must be open) |
| **Session `/loop`** | Current CLI session | Interval or self-paced | Yes (session must be active) |

### Cloud Routines

The most powerful tier. Created at `claude.ai/code/routines` or via `/schedule` in the CLI.

```bash
# Create a routine from the CLI
/schedule

# Or use the web UI
# claude.ai/code/routines
```

**Trigger types:**
- **Scheduled** -- Cron expressions (e.g., `0 9 * * 1-5` for weekday mornings)
- **API** -- HTTP POST endpoint; wire it to monitoring tools, CI/CD, or webhooks
- **GitHub events** -- `pull_request.opened`, `issues.opened`, `push`, etc.

**Limits (per day):**
- Pro: 5 | Max: 15 | Team/Enterprise: 25
- One-off "run now" executions don't count against daily caps

### Desktop Scheduled Tasks

Run locally via the Claude Desktop app. Persistent across restarts but require the app to be open.

### Session `/loop`

Temporary, session-bound loops. Good for monitoring a build, polling for a condition, or running periodic checks during active development.

```bash
# Check build status every 5 minutes
/loop 5m check if the build passed and report any failures

# Self-paced (model decides interval)
/loop monitor the deploy and notify me when it stabilizes
```

---

## Daily Standup & Briefing

### Morning Standup Brief

Post a daily summary of repository activity to Slack.

**Trigger:** Schedule (daily at 9:00 AM, weekdays)
**Connectors:** GitHub, Slack

```
Read all open PRs and recent commits in the repository. Post a Slack
message to #standup with:
- What landed yesterday
- What's in flight (open PRs)
- Anything blocked or stale (PRs older than 3 days)
Keep it under 10 lines with bullet points.
```

### Morning Check-In Brief

A broader daily briefing that includes calendar, email, and tasks.

**Trigger:** Schedule (daily, early morning)
**Connectors:** Calendar, Email, Slack

```
Check today's calendar events with attendees and prep signals. Scan
unread mail and chat from key contacts. Identify the single most
critical task for today. Generate a scannable brief with:
- Today's meetings (with context on attendees)
- Action items from overnight messages
- Top priority for the day
```

### Periodic Catch-Up Heartbeat

Runs every few hours. Only surfaces actionable items.

**Trigger:** Schedule (every 2-3 hours)
**Principle:** Silence is the default. Only surface something if it's actionable, time-sensitive, or the agent can handle it autonomously.

```
Scan connected tools (GitHub, Slack, email) for new activity.
Triage into: assistant-can-act / user-should-act / FYI / suppress.
Report max 3 bullets. If nothing is actionable, stay silent.
```

---

## Code Review Automation

### PR Auto-Reviewer (GitHub-Triggered)

Automatically review every new PR.

**Trigger:** GitHub event (`pull_request.opened`)

```
A pull request was just opened on this repository. Review it carefully
and post a comment on the PR with:
1. A one-line summary of what the PR changes
2. Any potential bugs, edge cases, or security concerns
3. Suggestions for improvement (if any)
4. A clear verdict: ready to merge, needs changes, or blocking issue
```

**Tip:** Add an author filter to your own GitHub username to avoid burning quota on every contributor's PRs.

### Team Checklist Review (GitHub-Triggered)

Enforce team-specific review standards.

**Trigger:** GitHub event (`pull_request.opened`)

```
Review this PR against our team checklist:

## Security
- Hardcoded secrets, API keys, or credentials in the diff?
- Unvalidated user inputs enabling injection attacks?
- New dependencies with known CVEs?

## Performance
- N+1 query patterns in ORM calls?
- Missing database indexes for new query patterns?
- Large synchronous operations that should be async?

## Code Style
- Consistent naming with the rest of the codebase?
- Functions named clearly enough to be self-documenting?

Leave inline comments on specific issues with line numbers and fixes.
Post a summary comment with pass/fail for each category.
```

### CI Test Failure Analysis

Diagnose CI failures automatically.

**Trigger:** GitHub Action (`workflow_run` on test failure)

```
The CI test suite just failed. Analyze the failure:
1. Identify which tests failed and their error messages
2. Trace the root cause to a specific file and line
3. Suggest a fix with code
4. Check if the failure is flaky (has it passed recently?)
Post findings as a PR comment.
```

---

## Repository Health

### Nightly Issue Triage

Classify and assign new issues automatically.

**Trigger:** Schedule (nightly)
**Connectors:** GitHub, Slack

```
Read all GitHub issues opened today. For each issue:
- Apply the appropriate label: bug, feature, docs, question, needs-triage
- Assign to the relevant owner based on CODEOWNERS
- If unclear or missing reproduction steps, comment requesting more info

Post a summary to #dev-standup:
- Total issues processed
- Breakdown by label
- Issues needing human attention

If zero issues were filed, post: "No new issues today."
```

### Weekly Tech Debt Scan

Surface TODOs and FIXMEs before they accumulate.

**Trigger:** Schedule (weekly, e.g., Friday at 2pm)

```
Find all TODO, FIXME, HACK, and XXX comments in the codebase.
List by file with line numbers. Identify the 3 highest-priority
items based on surrounding code complexity and recency.
```

### Dead Code Detection

Find unused code that can be removed.

**Trigger:** Schedule (weekly or biweekly)

```
Scan the codebase for dead code:
- Unused functions and methods
- Unreachable branches
- Commented-out code blocks
- Unused imports

Report findings grouped by file. Flag only high-confidence results.
```

---

## Dependency & Security

### Nightly Dependency Audit

Catch vulnerabilities before they reach production.

**Trigger:** Schedule (daily at 2am UTC)
**Connectors:** GitHub

```
Run npm audit (or pip-audit, cargo audit) on all package manifests.
For each vulnerability with severity high or critical:
- Check if a GitHub issue already exists
- If not, open one with: CVE ID, affected package, current version,
  fixed version, and remediation steps
Label all issues "security" and "dependencies".
```

### Weekly Security Audit

Broader security scan beyond just dependencies.

**Trigger:** Schedule (weekly, e.g., Monday at 10am)

```
Perform a security audit:
1. Check for outdated dependencies with known CVEs
2. Scan for hardcoded secrets or API keys in committed files
3. Review Dockerfiles for running as root, using :latest tags,
   or exposing unnecessary ports
4. Flag any unsafe patterns (eval, dangerouslySetInnerHTML, etc.)
Open GitHub issues for high/critical findings with remediation steps.
```

---

## Documentation Maintenance

### Weekly Docs Drift Detection

Catch documentation that falls behind the code.

**Trigger:** Schedule (weekly, e.g., Monday at 9am)
**Connectors:** GitHub

```
Scan all PRs merged in the past 7 days. For each PR, check if any
documentation files (README, docs/, wiki) reference the modified
functions, APIs, or configuration options.

If documentation is outdated relative to code changes, open a PR
with suggested updates.
```

### Changelog Generation

Auto-generate changelogs when versions are tagged.

**Trigger:** GitHub event (`push` on tags matching `v*`)

```
A new version tag was pushed. Generate a formatted changelog from
all commits since the previous tag. Categorize into:
- Features
- Bug Fixes
- Breaking Changes
- Documentation

Open a PR adding the changelog entry.
```

---

## PR Management

### Stale PR Detection

Keep the PR queue clean.

**Trigger:** Schedule (daily)

```
List every open PR. Flag any that:
- Have been open for more than 2 weeks
- Have unresolved review comments older than 3 days
- Have failing CI checks with no recent activity
- Have merge conflicts

Post a summary to the team channel with action items.
```

### Cross-SDK Port (Library Maintainers)

Automatically port changes across language SDKs.

**Trigger:** GitHub event (`pull_request.closed`, filtered to merged PRs)

```
A PR was just merged to the Python SDK. Port the equivalent changes
to the TypeScript SDK:
1. Identify the corresponding files and patterns
2. Translate the implementation
3. Run tests
4. Open a draft PR with the ported changes
```

---

## Notification Triage

### Alert Triage

Route monitoring alerts to the right people with context.

**Trigger:** API (HTTP POST from monitoring tool)

```
Read the alert payload. Find the owning service by matching the
alert source to CODEOWNERS. Post a triage summary to #oncall with:
- Alert severity and source
- Affected service and owner
- Recent commits that may be related
- Proposed first step for investigation
```

### Email Triage

Classify and draft responses to incoming email.

**Trigger:** Schedule (daily, before workday starts)
**Connectors:** Email

```
Read unread emails from the past 24 hours. For each:
- Classify urgency: immediate / today / this week / FYI
- Determine intent: question, request, FYI, action-needed
- Draft a reply for urgent items
Queue drafts for review. Summarize the inbox state.
```

---

## Deploy & Operations

### Post-Deploy Verification

Verify deployments are healthy.

**Trigger:** API (POST from CD pipeline after deploy)
**Connectors:** GitHub, Slack

```
A deploy just completed. Verify it's healthy:
1. Run smoke tests from tests/smoke/ against the production URL
2. Check application logs for new error patterns in past 10 minutes
3. Compare key metrics (latency, error rate) to pre-deploy baseline

Post results to #deploys. For failing tests, open a GitHub issue
with details and tag @oncall.
```

### Nightly Bug Fix Attempt

Let the agent take a crack at top bugs overnight.

**Trigger:** Schedule (daily at 2am)
**Connectors:** GitHub (or Linear/Jira)

```
Pull the top bug from the issue tracker (by priority or votes).
Attempt a fix:
1. Reproduce the issue from the description
2. Trace the root cause
3. Implement a fix with tests
4. Open a draft PR for human review

If the fix isn't confident, comment on the issue with findings instead.
```

---

## Memory & Knowledge

### Dream Memory Consolidation

Consolidate conversation learnings into persistent memory during idle periods.

**Trigger:** After 24+ hours of inactivity (or nightly)

```
Scan recent session transcripts for:
- Corrections and feedback the user gave
- Decisions and their rationale
- Recurring themes or preferences
- New facts about the project or codebase

Integrate findings into memory. Resolve contradictions with existing
memories. Prune outdated entries. Rebuild the memory index.
```

### Weekly Research Digest

Stay current on topics relevant to the project.

**Trigger:** Schedule (weekly)

```
Scan for new developments in [topics relevant to this project].
Compare against prior coverage. Synthesize new findings into a
structured brief with:
- Key developments this week
- Relevance to our project
- Recommended actions (if any)
```

---

## Creative & Unusual

### Meeting Prep Agent

Prepare for tomorrow's meetings while you sleep.

**Trigger:** Schedule (daily, evening)
**Connectors:** Calendar, Email

```
Check tomorrow's calendar. For each meeting:
- Look up attendees and their recent activity
- Pull relevant documents or PRs
- Prepare talking points or agenda items
- Flag any prep work needed

Post the briefing to a personal channel or note.
```

### Spec-to-Stub Conversion

Turn issues into code scaffolds automatically.

**Trigger:** GitHub event (issue labeled `ai-scaffold`)

```
An issue was just labeled for scaffolding. Convert it into code:
1. Parse the requirements from the issue body
2. Identify the right files and patterns from the existing codebase
3. Generate stubs with TODOs for each requirement
4. Open a draft PR with the scaffold

Follow existing code patterns for naming, structure, and testing.
```

### Routine Chaining

Chain multiple routines for complex workflows.

**Example chain:**
1. Morning email triage identifies a lead
2. Writes lead info to a shared file
3. Second routine generates a proposal draft
4. Third routine (end-of-day) checks if proposal was sent and adds CRM follow-up

Each routine reads from and writes to shared state (files, issues, or database).

---

## Best Practices

### Writing Effective Routine Prompts

**Be specific about outputs.** Bad: "Check for issues." Good: specify labels, owner assignment logic, connector targets, and what "done" looks like (a Slack message, a draft PR, a labeled issue).

**Include guard rails.** Tell the routine what NOT to do: "Do not merge PRs automatically," "Do not send messages without drafting first," "Only open issues for high/critical severity."

**Specify connectors explicitly.** Name the Slack channel, GitHub repo, or email address. Routines don't inherit your context the way interactive sessions do.

### Testing and Iteration

1. **Always "Run now" before scheduling.** Verify behavior manually before setting a cron schedule.
2. **Start with dry runs.** Have the routine report what it would do before giving it write permissions.
3. **Expect prompt evolution.** Claude optimizes the prompt after the first run based on what it learned. Review the rewritten prompt.

### Quota and Cost Management

- One-off "Run now" executions don't count against daily routine caps
- Use author filters on GitHub triggers to avoid burning quota on every contributor's PRs
- Routines use your identity -- commits, Slack messages, and PR actions appear as you, not a bot
- Consider cost: a PR review routine on a busy repo can consume significant quota

### Choosing the Right Tier

| Scenario | Recommended Tier |
|----------|-----------------|
| Nightly security scans | Cloud Routine (scheduled) |
| PR review on every push | Cloud Routine (GitHub event) |
| Post-deploy smoke test | Cloud Routine (API trigger) |
| Monitor a running build | Session `/loop` |
| Daily local file cleanup | Desktop Scheduled Task |
| One-time future task | Cloud Routine (one-off schedule) |

---

## Repositories & Resources

### Official

- [Routines Documentation](https://code.claude.com/docs/en/routines) -- Setup, triggers, connectors, limits
- [Scheduled Tasks Documentation](https://code.claude.com/docs/en/scheduled-tasks) -- Desktop-based scheduling
- [claude-code-action](https://github.com/anthropics/claude-code-action) -- GitHub Action for PR review and issue automation
- [claude-code-security-review](https://github.com/anthropics/claude-code-security-review) -- AI-powered SAST as a GitHub Action

### Community

| Repository | Focus |
|---|---|
| [Piebald-AI/claude-code-system-prompts](https://github.com/Piebald-AI/claude-code-system-prompts) | System prompts including morning-checkin, catch-up, dream skills |
| [jshchnz/claude-code-scheduler](https://github.com/jshchnz/claude-code-scheduler) | OS-native scheduler with natural language scheduling |
| [grandamenium/dream-skill](https://github.com/grandamenium/dream-skill) | Memory consolidation replicating auto-dream |
| [wanshuiyin/Auto-claude-code-research-in-sleep](https://github.com/wanshuiyin/Auto-claude-code-research-in-sleep) | Autonomous research pipelines with cross-model review |
| [alirezarezvani/claude-skills](https://github.com/alirezarezvani/claude-skills) | 232+ skills for Claude Code, Codex, Gemini CLI |
| [ComposioHQ/awesome-claude-skills](https://github.com/ComposioHQ/awesome-claude-skills) | Curated directory with 78 SaaS integrations |

### Tutorials

- [Builder.io: Claude Code Routines](https://www.builder.io/blog/claude-code-routines) -- Practical examples with connectors
- [AyyazTech: Routines Tutorial](https://www.ayyaztech.com/blog/claude-code-routines-tutorial) -- Step-by-step setup guide
- [ComputingForGeeks: Setup Guide](https://computingforgeeks.com/claude-code-routines-setup/) -- Infrastructure-focused setup
