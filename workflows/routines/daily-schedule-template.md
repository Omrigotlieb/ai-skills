# Daily Schedule Template

A recommended daily routine schedule for development teams. Copy and adapt to your needs.

## Recommended Schedule

| Time | Routine | Purpose |
|------|---------|---------|
| 6:00 AM | Dependency audit | Check for vulnerabilities before team arrives |
| 7:00 AM | Morning brief | Prepare daily context (PRs, issues, mentions) |
| 8:30 AM | Standup post | Auto-post development status to Slack |
| 9:00 AM | Inbox triage | Label and route overnight issues |
| 12:00 PM | Stale PR reminder | Nudge reviews older than 24h |
| 5:00 PM | End-of-day summary | What shipped, what's pending |
| 11:00 PM | Stale issue cleanup | Flag abandoned issues |
| 2:00 AM | Security scan | Nightly vulnerability audit |

## Weekly Additions

| Day | Time | Routine | Purpose |
|-----|------|---------|---------|
| Monday | 6:00 AM | Dependency updates | Open PRs for outdated packages |
| Wednesday | 10:00 AM | Docs drift scan | Find stale documentation |
| Friday | 5:00 PM | Changelog generation | Weekly changelog from merged PRs |
| Sunday | 10:00 PM | Full docs audit | Deep documentation freshness check |

## Event-Triggered (Always On)

| Trigger | Routine | Purpose |
|---------|---------|---------|
| PR opened | Automated review | Security, perf, style checks |
| Issue opened | Triage bot | Label, prioritize, detect duplicates |
| Deploy completed | Verification | Smoke tests and health checks |
| Alert fired | Alert triage | Correlate with recent changes |

## Setup Checklist

1. **Start with read-only routines** — standup brief and morning prep
2. **Add labeling routines** — issue triage, stale detection
3. **Enable PR review** — automated code review on PR open
4. **Add write routines** — dependency PRs, changelog generation
5. **Wire up event triggers** — deploy verification, alert triage

## CLI Quick Commands

```bash
# Create a recurring routine
/schedule daily standup brief at 8:30am

# Create a one-off
/schedule tomorrow at 9am, summarize yesterday's merged PRs

# List all routines
/schedule list

# Update a routine's schedule
/schedule update

# Trigger immediately
/schedule run
```

## Budget Planning

| Plan | Daily runs | Recommended allocation |
|------|-----------|----------------------|
| Pro | 5/day | 2 scheduled + 3 event-triggered |
| Max | 15/day | 5 scheduled + 10 event-triggered |
| Team | 25/day | 8 scheduled + 17 event-triggered |

One-off runs don't count against the daily cap.

## Starter Kit: Minimum Viable Automation

If you're just getting started, these three routines provide the highest ROI:

### 1. Morning Brief (read-only, low risk)

```
/schedule weekdays at 8am

Prompt: Read all PRs merged yesterday and all currently open PRs.
Post to #standup:
- What shipped (merged PRs with authors)
- What needs review (open PRs > 12h without review)
- CI status (green/red)
Keep under 10 lines.
```

### 2. PR Review (on PR open, medium value)

```
Trigger: pull_request.opened

Prompt: Review this PR for correctness, security, and performance.
Leave inline comments for issues found. Post a summary comment
with APPROVE/REQUEST_CHANGES verdict. Max 8 inline comments.
Don't nitpick formatting if a linter covers it.
```

### 3. Stale Issue Cleanup (nightly, maintenance)

```
/schedule daily at 11pm

Prompt: Find issues with no activity in 30 days.
Skip pinned issues and anything labeled "keep-open".
Apply "stale" label and comment asking if still relevant.
Close issues stale for 14+ days after labeling.
Post count to #project-maintenance.
Max 10 closures per night.
```

These three cover awareness, quality, and hygiene — the foundation of an automated development workflow.
