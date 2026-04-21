# Weekly Repository Health Check Routine

A comprehensive weekly audit that catches slow-burning issues before they become emergencies: stale PRs, dependency vulnerabilities, documentation drift, and declining test coverage.

---

## Overview

| Property | Value |
|----------|-------|
| **Schedule** | `0 7 * * 1` (Monday at 7 AM) |
| **Duration** | 2-5 minutes depending on repo size |
| **Impact** | Prevents the gradual decay of repo hygiene that compounds over months |
| **Sources** | Git history, package manager, CI, GitHub API |

## Setup

### Basic Health Check

```bash
claude schedule create \
  --name "weekly-health-check" \
  --cron "0 7 * * 1" \
  --prompt "$(cat <<'EOF'
Run a weekly health check on this repository and produce a report.

## Checks

### 1. Dependency Health
- Run the package manager's audit command (npm audit / pip audit / cargo audit)
- List packages with known vulnerabilities, grouped by severity
- List packages more than 1 major version behind latest
- Identify any dependencies that appear in package.json/requirements.txt but are never imported

### 2. Stale PRs
- List open PRs with no activity in the last 7 days
- For each: title, author, days since last activity, review status
- Flag PRs that are approved but not merged

### 3. Branch Hygiene
- List branches with no commits in 30+ days
- List branches that have been merged but not deleted
- Count total open branches

### 4. Test Coverage
- Run the test suite and report coverage percentage
- Compare to last known coverage if available
- List files with 0% coverage that contain business logic

### 5. CI Reliability
- Check the last 10 CI runs on main: how many passed vs failed?
- If any tests are flaky (pass/fail inconsistently), list them
- Report average build time

### 6. Documentation
- List any README.md files that reference functions or APIs that no longer exist
- Check if CHANGELOG.md was updated with this week's merged PRs
- Verify that any new public exports have JSDoc/docstring comments

## Output Format

### Repository Health Report -- Week of [date]

**Health Score: [A/B/C/D/F]**

Scoring:
- A: No critical issues, <3 medium issues
- B: No critical issues, 3-5 medium issues
- C: 1 critical issue OR >5 medium issues
- D: 2-3 critical issues
- F: >3 critical issues

#### Critical (fix this week)
- [issue with specific file/package and remediation]

#### Recommended (fix soon)
- [issue with context]

#### Informational
- [trends and observations]

#### Metrics
| Metric | This Week | Last Week | Trend |
|--------|-----------|-----------|-------|
| Open PRs | ... | ... | ... |
| Test coverage | ... | ... | ... |
| Build time | ... | ... | ... |
| Vulnerabilities | ... | ... | ... |
| Stale branches | ... | ... | ... |
EOF
)"
```

### Dependency-Focused Check

For projects where dependency management is the primary concern:

```bash
claude schedule create \
  --name "dependency-audit" \
  --cron "0 7 * * 1" \
  --prompt "$(cat <<'EOF'
Run a thorough dependency audit.

## Checks

### Vulnerabilities
- Run npm audit / pip audit / cargo audit
- For each vulnerability:
  - Package name and current version
  - Vulnerability description and CVE ID
  - Fixed version (if available)
  - Is it a direct or transitive dependency?
  - Suggested remediation (upgrade, replace, or accept risk)

### Outdated Packages
- List packages where a newer major version exists
- For each: current version, latest version, breaking changes summary
- Prioritize by: security fixes > bug fixes > features

### Unused Dependencies
- Cross-reference installed packages against import/require statements
- List packages that appear installed but never imported
- Estimate size savings from removing unused packages

### License Compliance
- List all dependency licenses
- Flag any copyleft licenses (GPL, AGPL) in a permissively-licensed project
- Flag any dependencies with no license specified

## Output
### Action Required
- [packages to upgrade urgently with commands]

### Upgrade When Convenient
- [packages to upgrade with migration notes]

### Remove
- [unused packages with removal commands]

### License Issues
- [any compliance concerns]
EOF
)"
```

## Notification & Delivery

### Slack Summary

```markdown
After generating the report, post a summary to #engineering-health:

**Weekly Health: [score]**
- Critical issues: [count]
- Stale PRs: [count]
- Vulnerabilities: [critical/high/medium/low counts]
- Coverage: [percentage] ([trend])

[Link to full report if stored somewhere]
```

### Email Report

```markdown
After generating the report, email it to the engineering team with subject:
"[Repo Name] Weekly Health Report -- [date] -- Grade: [score]"
```

### Auto-Create Issues

```markdown
For each Critical finding, check if a GitHub issue already exists.
If not, create one with:
- Title: "[Health Check] [brief description]"
- Label: "health-check", "priority:high"
- Body: finding details and suggested remediation
- Assign to the most recent committer in the affected area
```

## Customization

### Adjusting Thresholds

```markdown
## Custom Thresholds
- Stale PR threshold: 5 days (default: 7)
- Stale branch threshold: 14 days (default: 30)
- Coverage warning below: 85% (default: 80%)
- Build time warning above: 10 minutes (default: 15)
```

### Adding Project-Specific Checks

```markdown
## Additional Checks
- Verify that all API endpoints have corresponding OpenAPI spec entries
- Check that all environment variables in .env.example exist in CI config
- Ensure all database migrations are reversible
- Verify that Docker images build successfully
```

### For Monorepos

```markdown
## Monorepo Mode
Run health checks independently for each package/workspace:
- Report per-package scores
- Highlight cross-package dependency issues
- Flag packages that haven't been updated in 60+ days
```

## Trend Tracking

Store weekly metrics to track trends over time:

```markdown
After generating the report, append this week's metrics to
.github/health-metrics.json in the format:
{
  "date": "YYYY-MM-DD",
  "score": "A",
  "open_prs": 5,
  "coverage": 87.3,
  "build_time_seconds": 145,
  "vulnerabilities": {"critical": 0, "high": 1, "medium": 3, "low": 8},
  "stale_branches": 12
}
```

## Example Output

```
### Repository Health Report -- Week of 2026-04-20

**Health Score: B**

#### Critical (fix this week)
(none)

#### Recommended (fix soon)
- `express` 4.18.2 -> 5.0.1: security fix for CVE-2026-1234 (path traversal).
  Run: `npm install express@5.0.1`. Breaking change: `req.host` no longer includes port.
- PR #198 "Add caching layer" has been open 12 days with no review.
  Author: @alex. Reviewer requested: @sarah.
- Test coverage dropped from 87% to 83% this week.
  Files with 0% coverage added: `src/services/notifications.ts`

#### Informational
- 8 branches merged but not deleted (cleanup with `git remote prune origin`)
- Average build time: 2m 34s (stable)
- 3 flaky tests identified in payment module (pass rate: 94%)

#### Metrics
| Metric | This Week | Last Week | Trend |
|--------|-----------|-----------|-------|
| Open PRs | 7 | 5 | +2 |
| Test coverage | 83% | 87% | -4% |
| Build time | 2m 34s | 2m 28s | stable |
| Vulnerabilities | 0/1/3/8 | 0/0/3/8 | +1 high |
| Stale branches | 8 | 6 | +2 |
```
