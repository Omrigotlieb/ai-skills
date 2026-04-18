# Weekly Quality Dashboard

**Trigger:** Schedule | **Frequency:** Monday at 9am | **Category:** Code Review

Generates a weekly code health report covering complexity trends, test coverage changes, tech debt metrics, and refactoring priorities. Gives teams a longitudinal view of code quality without manual metric collection.

## Setup

```bash
claude /schedule create \
  --name "weekly-quality-dashboard" \
  --cron "0 9 * * 1" \
  --prompt "$(cat <<'EOF'
You are generating a weekly code quality dashboard.

## Task
1. Complexity Analysis:
   - Identify the 10 most complex functions/methods (by cyclomatic complexity)
   - Compare to last week's report (if available in git history)
   - Flag any function that increased in complexity this week

2. Test Coverage:
   - Run the test suite with coverage reporting
   - Compare coverage percentages to the previous week
   - Identify files with the lowest coverage that were modified this week

3. Tech Debt Signals:
   - Count TODO/FIXME/HACK comments and compare to last week
   - Identify files with the most churn (most commits) this week
   - Flag any files over 500 lines that grew this week

4. Code Duplication:
   - Identify blocks of similar code (potential extraction candidates)
   - Compare to last week's duplication count

5. Dependencies:
   - Count total dependencies and compare to last week
   - Flag any newly added dependencies

## Output Format
Generate a Markdown report:

### Code Quality Dashboard - Week of <date>

**Overall Health:** [improving/stable/declining]

#### Complexity Hotspots
| File | Function | Complexity | Trend |
|---|---|---|---|

#### Coverage
- **Total:** X% ([+/-]Y% from last week)
- **Lowest coverage modified files:** [list]

#### Tech Debt
- **TODO/FIXME count:** X ([+/-]Y from last week)
- **High-churn files:** [list]

#### Recommendations
1. [Top priority refactoring suggestion]
2. [Test coverage improvement suggestion]
3. [Dependency cleanup suggestion]

## Constraints
- If test suite takes more than 5 minutes, skip coverage and note it.
- Compare to previous reports stored in git history when possible.
- Keep the report actionable. Every metric should have a "so what" recommendation.
EOF
)"
```

## Customization

- **Language tools:** Use `radon` for Python complexity, `eslint` metrics for JavaScript, `go vet` for Go
- **Thresholds:** Adjust the 500-line file size threshold and complexity warnings for your standards
- **Delivery:** Post to Slack, email, or commit the report to a `docs/reports/` directory
- **Frequency:** Run daily for fast-moving projects, biweekly for stable ones

## Related

- [Architecture Review](architecture-review.md) for deeper structural analysis
- [Tech Debt Tracker](tech-debt-tracker.md) for daily debt monitoring
