# Architecture Review

**Trigger:** Schedule | **Frequency:** Weekly | **Category:** Self-Improvement

Identifies module boundary confusion, tight coupling, unnecessary abstractions, and structural drift. Run weekly or after development surges to keep the codebase navigable and agent-friendly.

## Setup

```bash
claude /schedule create \
  --name "architecture-review" \
  --cron "0 9 * * 1" \
  --prompt "$(cat <<'EOF'
You are running a weekly architecture review.

## Task
1. Module Boundaries:
   - Map the dependency graph between top-level modules/packages
   - Identify cross-module imports that violate intended boundaries
   - Flag modules that import from more than 5 other modules (high efferent coupling)
   - Flag modules imported by more than 8 others (high afferent coupling)

2. Abstraction Quality:
   - Identify wrapper functions/classes that add no value (pass-through abstractions)
   - Find interfaces with only one implementation (premature abstraction)
   - Detect god objects (classes with 10+ methods or files with 500+ lines)

3. Structural Drift:
   - Compare the current module structure to CLAUDE.md or ARCHITECTURE.md descriptions
   - Identify new modules/directories not documented in architecture docs
   - Flag naming inconsistencies between the documented architecture and actual structure

4. Change Hotspots:
   - Identify files changed most frequently in the last 30 days (git log analysis)
   - Cross-reference hotspots with complexity metrics
   - Flag files that are both high-churn AND high-complexity (refactoring candidates)

## Output
Generate a Markdown report:

### Architecture Review - Week of <date>

**Health:** [healthy / attention needed / action required]

#### Boundary Violations
| From | To | Type | Suggestion |
|---|---|---|---|

#### Abstraction Issues
- [list with file paths and recommendations]

#### Hotspots (High Churn + High Complexity)
| File | Commits (30d) | Complexity | Recommendation |
|---|---|---|---|

#### Recommendations
1. [Top priority structural improvement]
2. [Second priority]
3. [Third priority]

## Constraints
- Focus on structural issues, not code style or formatting.
- Recommend refactoring only when the cost of the current structure is clear.
- Do not auto-refactor. Report only.
EOF
)"
```

## Why This Matters

Code quality degrades faster than it improves. Regular architecture reviews catch structural decay early, when fixes are small. Without them:

- **Module boundaries blur** as quick-fix cross-module imports accumulate
- **Abstractions fossilize** as one-implementation interfaces outlive their purpose
- **Change hotspots grow** as complex files attract more changes that increase complexity

## Customization

- **Coupling thresholds:** Adjust the 5-import and 8-imported thresholds for your project size
- **File size threshold:** Change the 500-line god-object threshold for your language/style
- **Hotspot window:** Use 7 days instead of 30 for fast-moving projects
- **Output:** Post to a team channel or commit to a `docs/reviews/` directory

## Related

- [Weekly Quality Dashboard](weekly-quality-dashboard.md) for code-level metrics
- [Tech Debt Tracker](tech-debt-tracker.md) for daily debt monitoring
