# Rotating Health Scan

**Trigger:** Schedule | **Frequency:** Nightly | **Category:** Security

Each night, picks a different module or directory and runs a deep health check: static analysis, dependency cycle detection, coupling metrics, and dead code identification. The rotation distributes scanning cost across days and prevents alert fatigue.

## Setup

```bash
claude /schedule create \
  --name "rotating-health-scan" \
  --cron "0 3 * * *" \
  --prompt "$(cat <<'EOF'
You are running a rotating deep health scan.

## Task
1. Determine which module to scan:
   - Read the rotation state file (.health-scan-state.json) to find the last scanned directory
   - Pick the next directory in alphabetical order from the top-level source directories
   - If all directories have been scanned this cycle, start over

2. Run deep analysis on the selected module:
   - **Static Analysis:** Identify code smells, overly complex functions, unreachable code
   - **Dependency Cycles:** Map internal imports and flag circular dependencies
   - **Coupling Metrics:** Measure afferent and efferent coupling for each file
   - **Dead Code:** Identify exported functions/classes with no internal callers
   - **Security Patterns:** Check for unsafe patterns specific to this module's domain

3. Compare to the previous scan of this module (if available in git history)

4. Update the rotation state file with the current scan date and module

## Output
- Open a GitHub issue titled "[Health] <module> scan - <date>" with:
  - Top 5 findings ranked by severity
  - Comparison to previous scan (new issues, resolved issues)
  - Suggested refactoring actions
- If no issues found, update the state file and log "Module <name> is healthy"

## Constraints
- Scan ONE module per night. Do not attempt full-codebase scans.
- Do not auto-fix anything. Report only.
- If the module has more than 100 files, focus on the top-level files and flag that a deeper scan is needed.
EOF
)"
```

## Rotation Strategy

For a project with directories `api/`, `auth/`, `core/`, `ui/`, `workers/`:

| Night | Module | Next |
|---|---|---|
| Monday | `api/` | `auth/` |
| Tuesday | `auth/` | `core/` |
| Wednesday | `core/` | `ui/` |
| Thursday | `ui/` | `workers/` |
| Friday | `workers/` | `api/` (restart) |

Each module gets a deep scan once per cycle. A 5-module project completes a full rotation weekly.

## Customization

- **Scope:** Exclude vendor, generated, or test directories from the rotation
- **Depth:** Adjust the 100-file threshold for large modules
- **State:** Use a git-tracked JSON file or a project-level config for rotation state
- **Frequency:** Run weekly for stable projects, nightly for active development

## Related

- [Dependency Audit](dependency-audit.md) for supply chain vulnerability scanning
- [Security Diff Review](security-diff-review.md) for per-PR security checks
- [Weekly Quality Dashboard](weekly-quality-dashboard.md) for aggregate code health metrics
