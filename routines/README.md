# Routines & Scheduled Tasks

Routines are recurring AI agent tasks that run on a schedule, on events, or in continuous loops. They turn idle compute into productive work: security scans at 2am, morning briefings at 8am, PR monitoring while you sleep.

This guide covers the best routines discovered across the Claude Code ecosystem, organized by when and why you would use them.

## How Routines Work

Claude Code supports three triggering mechanisms:

| Mechanism | Setup | Best For |
|---|---|---|
| **Scheduled tasks** (`/schedule`) | Cron expression + prompt | Nightly scans, morning reports, weekly reviews |
| **Loop mode** (`/loop` or `loop.md`) | Interval or dynamic pacing | PR monitoring, CI babysitting, maintenance |
| **API triggers** | HTTP endpoint + prompt | Post-deploy checks, alert triage, webhook responses |

### Quick Start

```bash
# Schedule a nightly dependency audit
claude /schedule create --cron "0 2 * * *" --prompt "Run dependency audit..."

# Start a PR monitoring loop
claude /loop 5m "Check CI status, address review comments, report"

# Dynamic-paced maintenance loop
claude /loop
```

## Routine Catalog

### Security & Compliance

| Routine | Trigger | Frequency | Guide |
|---|---|---|---|
| [Dependency Audit](dependency-audit.md) | Schedule | Nightly 2am | Scan for CVEs, outdated packages, breaking changes |
| [Security Diff Review](security-diff-review.md) | GitHub webhook | Per PR | Detect secrets, injection flaws, auth bypasses |
| [Rotating Health Scan](rotating-health-scan.md) | Schedule | Nightly | Deep SAST scan of one module per night |

### Code Review & Quality

| Routine | Trigger | Frequency | Guide |
|---|---|---|---|
| [PR Auto-Review](pr-auto-review.md) | GitHub webhook | Per PR | Multi-dimensional review with parallel agents |
| [Weekly Quality Dashboard](weekly-quality-dashboard.md) | Schedule | Monday 9am | Complexity trends, coverage, tech debt metrics |

### Operations & Monitoring

| Routine | Trigger | Frequency | Guide |
|---|---|---|---|
| [Deploy Verification](deploy-verification.md) | API trigger | Per deploy | Smoke tests, error log scan, go/no-go |
| [Nightly Bug Hunter](nightly-bug-hunter.md) | Schedule | Nightly 2:30am | Pull top bug from tracker, attempt fix, open draft PR |
| [PR Branch Monitor](pr-branch-monitor.md) | Loop | Dynamic | Fix CI, address comments, report status |

### Documentation & Knowledge

| Routine | Trigger | Frequency | Guide |
|---|---|---|---|
| [Docs Drift Detector](docs-drift-detector.md) | Schedule | Weekly | Find stale docs after API changes |
| [Memory Consolidation](memory-consolidation.md) | Schedule | Nightly | Merge, prune, and index agent memory files |
| [Knowledge Base Updater](knowledge-base-updater.md) | End of session | Daily | Append learnings to CLAUDE.md / AGENTS.md |

### Morning Briefings & Standup

| Routine | Trigger | Frequency | Guide |
|---|---|---|---|
| [Morning Briefing](morning-briefing.md) | Schedule | Daily 8am | CI status, new issues, review requests, deadlines |
| [Standup Summary](standup-summary.md) | Schedule | Daily | Aggregate commits, PRs, issues per developer |

### Self-Improvement

| Routine | Trigger | Frequency | Guide |
|---|---|---|---|
| [Architecture Review](architecture-review.md) | Schedule | Weekly | Module boundaries, coupling, DRY/KISS violations |
| [Tech Debt Tracker](tech-debt-tracker.md) | Schedule | Daily | Scan, prioritize, and report tech debt |

## Building Your Daily Schedule

A practical daily schedule combining the routines above:

```
 2:00 AM  Dependency Audit        - scan for vulnerabilities overnight
 2:30 AM  Nightly Bug Hunter      - attempt top-priority bug fix
 3:00 AM  Rotating Health Scan    - deep scan one module
 5:00 AM  Memory Consolidation    - prune and merge memory files
 6:00 AM  Tech Debt Tracker       - scan and prioritize tech debt (weekdays)
 8:00 AM  Morning Briefing        - deliver daily status report (weekdays)
 8:15 AM  Standup Summary         - generate per-developer summaries (weekdays)
 9:00 AM  (Monday) Quality Dashboard    - weekly code health report
 9:15 AM  (Monday) Architecture Review  - weekly structure review
 9:30 AM  (Monday) Docs Drift Detector  - find stale documentation
 6:00 PM  Knowledge Base Updater  - capture daily learnings to CLAUDE.md (weekdays)
          (continuous) PR Branch Monitor - loop during active PRs
          (per event) Deploy Verification - after each production deploy
          (per event) Security Diff Review - on every new PR
          (per event) PR Auto-Review - multi-dimensional review on new PRs
```

## Writing Your Own Routines

### Prompt Structure

Good routine prompts follow this pattern:

```markdown
## Context
You are running as a scheduled routine for [project name].
The repository is at [path]. The main branch is [branch].

## Task
1. [Specific check or action]
2. [Specific check or action]
3. [Decision criteria]

## Output
- If [condition]: [action, e.g., open issue, send notification]
- If [condition]: [action, e.g., log and skip]
- Always: [summary action, e.g., post to Slack]
```

### Tips

- **Be specific about outputs.** "Report findings" is vague. "Open a GitHub issue titled `[Security] CVE-XXXX in package Y`" is actionable.
- **Set clear boundaries.** "Fix any bugs you find" is dangerous. "Open a draft PR with the fix and request review" is safe.
- **Include failure modes.** What should the routine do when the repo is in a broken state, or the API is down?
- **Use dynamic pacing for loops.** Check frequently when CI is active, back off when idle. The `/loop` command with no interval does this automatically.

## Key Resources

| Resource | Description |
|---|---|
| [Claude Code Routines Docs](https://code.claude.com/docs/en/routines) | Official documentation for scheduled tasks and routines |
| [Claude Code Scheduled Tasks](https://code.claude.com/docs/en/scheduled-tasks) | Setup guide for cron-based and API-triggered tasks |
| [VoltAgent/awesome-agent-skills](https://github.com/VoltAgent/awesome-agent-skills) | 1000+ agent skills across platforms |
| [wshobson/agents](https://github.com/wshobson/agents) | 184 agents with orchestration patterns |
| [alirezarezvani/claude-skills](https://github.com/alirezarezvani/claude-skills) | 232+ Claude Code skills including tech debt tracking |
| [hamelsmu/claude-review-loop](https://github.com/hamelsmu/claude-review-loop) | Cross-model review automation pattern |
