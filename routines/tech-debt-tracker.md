# Tech Debt Tracker

**Trigger:** Schedule | **Frequency:** Daily | **Category:** Self-Improvement

Three-component system that scans for tech debt signals, prioritizes them using cost-of-delay frameworks, and tracks trends over time. Makes tech debt visible and quantified rather than a vague concern.

## Setup

```bash
claude /schedule create \
  --name "tech-debt-tracker" \
  --cron "0 6 * * 1-5" \
  --prompt "$(cat <<'EOF'
You are tracking tech debt across the codebase.

## Component 1: Debt Scanner
Identify new tech debt signals since yesterday:
- New TODO/FIXME/HACK/WORKAROUND comments added
- Functions that exceeded 50 lines
- Files that exceeded 500 lines
- New suppressed linter warnings (noqa, eslint-disable, @ts-ignore)
- Test files with skipped tests (.skip, @pytest.mark.skip)
- Catch-all error handlers (catch(e) {}, except Exception)

## Component 2: Debt Prioritizer
For each debt item found, estimate:
- **Impact:** How much does this slow down current development? (1-5)
- **Spread risk:** Will this pattern likely be copied elsewhere? (1-5)
- **Fix cost:** How many hours to resolve? (estimate)
- **Priority score:** (Impact + Spread risk) / Fix cost

## Component 3: Debt Dashboard
Compare to yesterday's scan and report:

### Tech Debt Report - <date>

**Trend:** [improving / stable / accumulating]

| Metric | Today | Yesterday | Delta |
|---|---|---|---|
| TODO/FIXME count | | | |
| Suppressed warnings | | | |
| Skipped tests | | | |
| God files (>500 lines) | | | |
| Long functions (>50 lines) | | | |

**New debt items (ranked by priority):**
1. [item] - Impact: X, Spread: Y, Fix cost: Zh - in [file:line]
2. [item] ...

**Resolved since yesterday:**
- [items removed or fixed]

## Constraints
- Only report NEW debt since the last scan. Do not re-report known items.
- Store the current scan results in .tech-debt-state.json for comparison.
- Keep the report under 30 lines. Link to files rather than quoting code.
EOF
)"
```

## Cost-of-Delay Framework

The prioritizer uses a simple formula to rank debt items:

```
Priority = (Impact + Spread Risk) / Fix Cost
```

| Score | Meaning | Action |
|---|---|---|
| > 3.0 | High priority, cheap fix | Fix this week |
| 1.0 - 3.0 | Moderate | Schedule for next sprint |
| < 1.0 | Low priority or expensive | Track but defer |

## Customization

- **Thresholds:** Adjust line count limits (50/500) for your language and style
- **Signals:** Add or remove debt signals for your stack (e.g., `# type: ignore` for Python)
- **State file:** Track in git for history, or in `.gitignore` for local-only tracking
- **Output:** Post high-priority items to Slack, keep the full report in a file

## Related

- [Nightly Bug Hunter](nightly-bug-hunter.md) for automated bug fixing
- [Architecture Review](architecture-review.md) for structural analysis
- [Weekly Quality Dashboard](weekly-quality-dashboard.md) for aggregate metrics
