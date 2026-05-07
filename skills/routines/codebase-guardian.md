# Codebase Guardian Routine

Monitors code quality, technical debt, and test coverage trends. Catches the slow decay that compounds over months -- growing complexity, declining coverage, proliferating TODO comments.

---

## Overview

| Property | Value |
|----------|-------|
| **Schedule** | `0 8 * * 1-5` (weekdays at 8 AM) or on push to main |
| **Duration** | 1-3 minutes |
| **Sources** | Source code, test suite, git log |

## Setup

Create via `/schedule` in Claude Code: `/schedule weekdays at 8am: codebase quality check`

Or create at `claude.ai/code/routines` with cron `0 8 * * 1-5` and the prompt below.

### Daily Quality Check

Use this prompt:

```markdown
Run a daily code quality check. ONLY report if something needs attention.

## Checks

### 1. Test Coverage
- Run the test suite and report coverage percentage
- Flag any files added in the last 24 hours with 0% test coverage
- Flag if overall coverage dropped by more than 2% since yesterday

### 2. Code Complexity
- Check files modified in the last 24 hours
- Flag functions with cyclomatic complexity > 15
- Flag functions longer than 100 lines
- Flag files with more than 500 lines

### 3. TODO/FIXME Tracking
- Scan for TODO, FIXME, HACK, and XXX comments
- Flag any that have been pending for more than 14 days (check git blame)
- Count total vs last check -- is the count growing?

### 4. Dead Code Detection
- Check for exported functions/classes with zero internal references
- Check for files not imported anywhere
- Flag unused dependencies (installed but never imported)

### 5. Build Health
- Run the build and report any warnings
- Flag new TypeScript/compiler warnings introduced in the last 24 hours

## Output Rules
- If everything is clean, produce no output (heartbeat pattern)
- Only report findings that are actionable
- Group by severity: needs-fix-today / fix-this-week / awareness

## Output Format (only if issues found)

### Codebase Guardian -- [date]

#### Fix Today
- [issue with file:line and specific recommendation]

#### Fix This Week
- [issue with context]

#### Trends
- Coverage: [X%] ([up/down/stable])
- TODO count: [N] ([up/down/stable])
- Build warnings: [N] ([up/down/stable])
```

### Loop-Based Variants

For active development sessions:

**Test coverage watch:**
```
/loop 1h Run a test coverage check. If overall coverage drops below 80%
or if any new files are missing tests, list the specific files and
provide recommendations.
```

**Complexity monitor:**
```
/loop 2h Check recently modified files in src/. If any function has
cyclomatic complexity exceeding 15 or is longer than 100 lines,
suggest a refactor with a concrete approach.
```

**TODO tracker:**
```
/loop 2h Scan all TODO and FIXME comments in the code, sort them
by age (git blame), and flag any items pending for more than 7 days.
```

**Lint auto-fix:**
```
/loop 30m Run eslint src/ --fix. If there are errors that cannot be
automatically fixed, summarize the error types and their locations.
```

## Weekly Deep Dive

For a more thorough analysis, run a weekly version:

```markdown
Run a deep code quality analysis for the past week.

## Checks (in addition to daily checks)

### Architecture Health
- Are there circular dependencies between modules?
- Are there modules with too many inbound dependencies (fan-in > 10)?
- Are there "god files" that keep growing? (files modified in >5 PRs this week)

### API Surface
- List any new public API endpoints or exported functions added this week
- Do they have documentation/doc comments?
- Do they have corresponding test files?

### Dependency Health
- Any new dependencies added this week? List with license and purpose
- Any dependencies with known CVEs? (cross-reference with npm/pip audit)

### Pattern Violations
- Check for patterns that differ from established conventions in the codebase
- Flag any direct database access outside of the data layer
- Flag any hardcoded URLs or magic numbers

## Output

### Weekly Code Quality Report

**Quality Score: [A/B/C/D/F]**

Scoring:
- A: No issues, stable or improving trends
- B: Minor issues only, no regressions
- C: Some issues need attention this week
- D: Multiple concerning trends
- F: Critical issues require immediate action

#### Issues
- [categorized findings]

#### Trends (vs last week)
| Metric | This Week | Last Week | Trend |
|--------|-----------|-----------|-------|
| Coverage | ... | ... | ... |
| TODO count | ... | ... | ... |
| Build warnings | ... | ... | ... |
| Avg function complexity | ... | ... | ... |
| Files > 500 lines | ... | ... | ... |
```

## Customization

### Project-Specific Rules

Add rules that match your team's conventions:

```markdown
## Custom Rules
- All React components must have PropTypes or TypeScript interfaces
- All API routes must have request validation middleware
- All database queries must go through the repository pattern
- No console.log in production code (use the logger utility)
- All async functions must have error handling
```

### Auto-Fix Mode

For low-risk fixes, enable automatic remediation:

```markdown
## Auto-Fix (low-risk only)
- Remove unused imports automatically
- Fix linting errors that have auto-fix rules
- Add missing semicolons / trailing commas
- Push fixes in a PR titled "[Guardian] Auto-fix: [description]"
- Do NOT auto-fix logic, rename variables, or restructure code
```

## Example Output

```
### Codebase Guardian -- 2026-05-07

#### Fix Today
- `src/services/payment.ts:234` -- Function processRefund is 142 lines long
  and has cyclomatic complexity of 22. Extract validation and notification
  logic into separate functions.

#### Fix This Week
- `src/utils/helpers.ts` -- 3 exported functions with zero references:
  formatCurrency, slugify, debounce. Verify unused and remove.
- `src/api/orders.ts:67` -- TODO added 21 days ago: "handle partial refunds"
  Either implement or create an issue to track it.

#### Trends
- Coverage: 84% (down 1% from yesterday -- new file src/services/shipping.ts has 0% coverage)
- TODO count: 23 (up 2 this week)
- Build warnings: 5 (stable)
```
