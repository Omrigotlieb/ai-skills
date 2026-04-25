# Agent Prompts for Claude Code

Copy-ready prompt templates for common agent patterns. Each prompt is designed to be used as a scheduled routine, slash command, or direct instruction.

> Links last verified: 2026-04-25

## Quick Navigation

- [Development Agents](#development-agents)
- [Operations Agents](#operations-agents)
- [Communication Agents](#communication-agents)
- [Research Agents](#research-agents)
- [Prompt Engineering Tips](#prompt-engineering-tips)

---

## Development Agents

### Codebase Health Auditor

Runs a multi-dimensional audit across your codebase and produces a scorecard.

```
Audit this codebase across the following dimensions. Score each 1-5
and provide specific findings:

1. Test coverage: run tests, check coverage reports, identify
   untested critical paths
2. Type safety: look for any types, type assertions, and
   missing return types
3. Error handling: find swallowed errors, missing try/catch,
   unhandled promise rejections
4. Dead code: identify unused exports, unreachable branches,
   commented-out code
5. Dependency health: outdated packages, unused dependencies,
   duplicate packages
6. API consistency: inconsistent naming, missing validation,
   undocumented endpoints

Output a markdown scorecard with:
- Overall score (average of dimensions)
- Top 3 most urgent items to fix
- Estimated effort for each (S/M/L)

Do not fix anything. Report only.
```

---

### Test Gap Finder

Identifies code paths without test coverage and generates the missing tests.

```
Analyze test coverage for this repository.

1. Identify all public functions and API endpoints
2. Cross-reference with existing test files
3. List untested code paths, sorted by risk:
   - High risk: auth, payments, data mutations
   - Medium risk: business logic, transformations
   - Low risk: utilities, formatting, constants

For the top 5 high-risk gaps:
- Write tests following existing test patterns in the repo
- Use the same test framework and assertion style
- Include happy path, error path, and one edge case per function

Put new tests next to existing test files. Follow the naming
convention already in use.
```

---

### Migration Assistant

Helps plan and execute database or API migrations safely.

```
I need to migrate {describe change}.

Before writing any code:
1. Identify all files that reference the affected tables/endpoints
2. Map the dependency graph of affected components
3. Check for any running queries or jobs that touch this data
4. Propose a migration plan with:
   - Steps in order
   - Rollback strategy for each step
   - Expected downtime (if any)
   - Data validation queries to run before and after

Wait for my approval before implementing any step.
```

---

### Performance Profiler

Systematic performance analysis with actionable recommendations.

```
Profile the performance of this application:

1. Identify the 5 slowest operations by analyzing:
   - Database queries (look for N+1, missing indexes, full scans)
   - API endpoints (response time, payload size)
   - Frontend renders (unnecessary re-renders, large bundles)
   - File I/O (synchronous reads, unbuffered writes)

2. For each slow operation, provide:
   - Current estimated latency
   - Root cause
   - Specific fix with code diff
   - Expected improvement

3. Check bundle size and suggest code splitting opportunities

Report findings sorted by impact (biggest improvement first).
Do not implement fixes — report only.
```

---

### SDK/Library Porter

When a change lands in one SDK, ports it to a parallel SDK in another language.

```
A PR was just merged in the {source_language} SDK repository.

Port the change to the {target_language} SDK repository:
1. Understand the intent and behavior of the original change
2. Implement the equivalent in idiomatic {target_language}
3. Maintain the same public API semantics
4. Write tests that mirror the original test coverage
5. Update documentation to match

Open a draft PR with a reference to the original PR.
Do not merge.
```

---

## Operations Agents

### Incident Responder

First-pass incident analysis when an alert fires.

```
An alert fired: {alert_description}

Investigate immediately:
1. Check error logs for the last 30 minutes — identify the error
   pattern and frequency
2. Correlate with recent deploys (last 24 hours)
3. Check if this is a known issue (search existing GitHub issues)
4. Assess blast radius: which users/services are affected?

Produce an incident report:
- Severity: P0/P1/P2/P3
- Impact: what's broken and for whom
- Likely root cause: with evidence
- Recommended action: rollback, hotfix, or monitor
- Timeline: when it started, when detected

Post to #incidents on Slack. Do not take any remediation action
without human approval.
```

---

### Infrastructure Health Check

Verifies system health across multiple dimensions.

```
Run an infrastructure health check:

1. Database: verify connectivity, check for long-running queries
   (>30s), verify table availability, check disk usage
2. API endpoints: hit each health check endpoint, flag any
   with response time >500ms
3. Queue depth: check message queues for backlog >1000
4. Disk space: flag any volume below 20% free
5. Certificate expiry: flag any SSL cert expiring within 30 days

Report format:
- GREEN: all checks pass
- YELLOW: non-critical issues found (list them)
- RED: critical issues (list them with remediation steps)

Post to #infrastructure-alerts.
```

---

### Cost Monitor

Tracks cloud spending and flags anomalies.

```
Review cloud spending for the last 7 days:

1. Compare daily spend against the 30-day average
2. Flag any service with >20% cost increase
3. Identify unused resources:
   - Unattached volumes
   - Idle load balancers
   - Oversized instances (CPU <10% average)
4. Estimate monthly savings if unused resources are cleaned up

Post a summary to #engineering-ops with:
- This week's total spend vs last week
- Top 3 cost drivers
- Savings opportunities with estimated dollar amounts
```

---

## Communication Agents

### Email Triage

Classifies and drafts responses for unread email.

```
Connect to Gmail. Fetch all unread emails from the last 24 hours.

Classify each as:
- URGENT: needs response today
- ACTION: needs response this week
- FYI: informational, no response needed
- NOISE: newsletters, promos, automated notifications

For URGENT emails:
- Draft a reply (don't send)
- Flag the key decision or question being asked

For ACTION emails:
- Create a one-line task summary

Output a structured summary:
- Count per category
- URGENT items with drafted replies
- ACTION items as a task list

Apply labels but do not send any replies.
```

---

### Meeting Prep Agent

Prepares context and talking points before meetings.

```
I have a meeting about {topic} in {time}.

Prepare me:
1. Context: summarize relevant recent activity
   - PRs merged related to this topic
   - Issues discussed in the last week
   - Slack threads mentioning this topic
2. Status: what's done, what's in progress, what's blocked
3. Talking points: 3-5 bullet points I should raise
4. Questions: 2-3 questions I should be prepared to answer
5. Data: any metrics or numbers I might need

Keep the entire prep under 1 page. Lead with the most important item.
```

---

### Standup Report Generator

Generates standup updates from git activity.

```
Generate my standup report for today.

Pull from:
- Git commits I authored yesterday and today
- PRs I opened, reviewed, or merged
- Issues I commented on or closed
- Any CI failures on my branches

Format as:
**Yesterday:**
- [completed items from git activity]

**Today:**
- [items in progress based on open PRs and assigned issues]

**Blockers:**
- [any failing CI, stale reviews, or dependency issues]

Keep each section to 3 items max. Be specific, not vague.
If there's nothing for a section, say "None."
```

---

## Research Agents

### Competitor Monitor

Tracks competitor activity across public channels.

```
Check the following competitors for new public activity in the last
7 days: {list competitors}

For each, check:
- Blog posts and announcements
- GitHub releases and changelogs
- Social media (LinkedIn company page, Twitter/X)
- Job postings (new roles that signal strategy shifts)

Summarize as:
- 3 bullet points per competitor
- Flag separately: pricing changes, product launches, major hires

Post to #competitive-intel on Slack.
If a competitor had no notable activity, say so in one line.
```

---

### Technology Radar

Evaluates new tools and libraries against your stack.

```
Research {technology/library} for potential adoption:

1. What problem does it solve that we currently handle with {current approach}?
2. Maturity: GitHub stars, release cadence, bus factor, last commit date
3. Compatibility: works with our stack ({list stack})?
4. Migration effort: estimate in days for our codebase size
5. Risks: lock-in, license, community health
6. Alternatives: 2-3 other options with brief trade-off comparison

Recommendation: adopt, trial, assess, or hold — with one-sentence rationale.
Do not install or modify any code.
```

---

### Dependency Landscape Report

Monthly overview of your dependency ecosystem health.

```
Generate a dependency landscape report:

1. Total dependency count (direct vs transitive)
2. Outdated packages: list those >2 major versions behind
3. Security: packages with known CVEs (high/critical)
4. License audit: flag any copyleft or unknown licenses
5. Maintenance risk: packages with no commits in >12 months
6. Duplication: packages that serve the same purpose

Prioritize the report by risk:
- P0: security vulnerabilities with known exploits
- P1: unmaintained packages in critical paths
- P2: outdated packages with breaking changes ahead
- P3: cleanup opportunities

Output as markdown. Do not modify any files.
```

---

## Prompt Engineering Tips

### The TCRO Framework

Structure prompts with four components:

| Component | Purpose | Example |
|-----------|---------|---------|
| **T**ask | What to do | "Review this PR for security issues" |
| **C**ontext | Background info | "This is a payments service handling PII" |
| **R**equirements | Constraints and boundaries | "Do not approve or merge. Only comment." |
| **O**utput | Expected format | "List issues with severity, location, and fix" |

### Negative Constraints Matter

Always tell the agent what NOT to do. Routines run unattended — explicit boundaries prevent surprises:

```
Do not merge any PRs.
Do not push to main.
Do not delete any files.
Do not send messages to external services.
Only push to claude/ branches.
```

### Handle Empty Results

Every prompt should define behavior when there's nothing to report:

```
If no issues were found, post a single line confirming all clear.
```

### Be Specific About Output Destination

Don't say "report results." Say where:

```
Post to #engineering-daily on Slack.
Open a GitHub issue labeled "security".
Send an email summary to team@example.com.
Write results to reports/weekly-digest.md.
```

### Stateless by Design

Each routine run starts fresh. Don't reference "last time" or "the previous run" — instead use time windows:

```
# Bad
Check for new issues since last run.

# Good
Check for issues opened in the last 24 hours.
```

---

## Resources

- [Daily Routines Guide](daily-routines.md) — scheduled routines with cron timing
- [Anthropic — Routines Docs](https://code.claude.com/docs/en/routines)
- [Anthropic — Scheduled Tasks](https://code.claude.com/docs/en/scheduled-tasks)
- [Prompts Guide](../prompts/README.md) — general prompt templates and the TCRO framework
- [levnikolaevich/claude-code-skills](https://github.com/levnikolaevich/claude-code-skills) — community skills collection
- [glebis/claude-skills](https://github.com/glebis/claude-skills) — skills including workflow helpers
- [ComposioHQ/awesome-claude-skills](https://github.com/ComposioHQ/awesome-claude-skills) — curated skill catalog
