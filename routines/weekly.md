# Weekly Routines

Routines that run once per week to catch systemic issues and maintain long-term codebase health.

---

## Code Quality Review

**Schedule:** Sundays at 9:00pm  
**Purpose:** Catch tech debt and code smells before they accumulate.

```
Weekly Code Quality Review

1. Scan the codebase for:
   - Functions longer than 50 lines
   - Files longer than 500 lines
   - Cyclomatic complexity hotspots
   - Duplicated code blocks (>10 lines identical)
   - Unused exports and dead code paths
2. Find all TODO, FIXME, HACK, and XXX comments
   - List by file with line numbers
   - Identify the top 3 priority items based on surrounding code risk
3. Check for commented-out code blocks (>5 lines)
4. Review import hygiene: unused imports across the project

Output format: Markdown report at reports/code-quality-YYYY-MM-DD.md
Structure:
- Executive summary (1-2 sentences)
- Hotspots table (file, issue, severity)
- TODO/FIXME inventory (top 10 by priority)
- Recommended actions (up to 5)

Skip: vendor/, node_modules/, generated/, *.min.js
```

### Auto-Fix Variant

```
Weekly Code Cleanup (with auto-fix)

1. Remove unused imports across all source files
2. Remove commented-out code blocks (>5 lines)
3. Run the project formatter and linter
4. Commit each category of fix separately with clear messages
5. Open a single PR titled "chore: weekly code cleanup YYYY-MM-DD"

Skip: Don't modify files with uncommitted changes.
Constraint: Only make changes that are purely mechanical (formatting, unused imports).
Never change logic or behavior.
```

---

## Dependency Audit

**Schedule:** Thursdays at 10:00am  
**Purpose:** Keep dependencies current and free of known vulnerabilities.

```
Weekly Dependency Health Check

1. Run: npm outdated --json (or pip list --outdated, cargo outdated, etc.)
2. Run: npm audit --json (or equivalent for your package manager)
3. Categorize updates:
   - Patch updates (safe to auto-apply)
   - Minor updates (review changelog)
   - Major updates (breaking changes, needs planning)
4. For any CVE with severity High or Critical:
   - Describe the vulnerability
   - Check if our code uses the affected API
   - Recommend: update, patch, or replace
5. Produce a summary report

Output format: Markdown report
Sections:
- Security alerts (Critical/High first)
- Available updates table (package, current, latest, type)
- Recommended actions
- Packages safe to auto-update

Skip conditions: Don't run if no lock file changes in the past week.
```

### Conservative Auto-Update Variant

```
Dependency Patch Update

1. Run: npm outdated --json
2. Update only patch versions (e.g., 1.2.3 -> 1.2.5)
3. Run: npm test
4. If tests pass: commit and open PR titled "chore(deps): patch updates YYYY-MM-DD"
5. If tests fail: revert changes, report which packages caused failures

Never update major or minor versions automatically.
```

---

## Documentation Drift Detection

**Schedule:** Mondays at 9:00am  
**Purpose:** Catch docs that have fallen out of sync with the code.

```
Documentation Drift Detection

1. List PRs merged to main in the past 7 days
2. For each PR, identify:
   - Functions or APIs that were added, renamed, or removed
   - Configuration options that changed
   - CLI flags or commands that changed
3. Cross-reference against documentation files (docs/, README.md, *.md)
4. Flag any doc that references a function, API, or config that was modified

Output format: Markdown report
Sections:
- PRs reviewed (count, titles)
- Drift detected (doc file, what changed, what the doc still says)
- No drift detected (doc file, confirmed current)
- Suggested updates (specific text replacements)

Skip conditions: Don't run if no PRs were merged this week.
```

---

## Security Vulnerability Scan

**Schedule:** Mondays at 10:00am  
**Purpose:** Weekly security posture check beyond dependency audits.

```
Weekly Security Scan

1. Dependency vulnerabilities:
   - Run: npm audit (or equivalent)
   - Flag Critical and High severity issues
2. Secrets detection:
   - Scan for hardcoded API keys, passwords, tokens, and connection strings
   - Check: .env files committed to git, config files, test fixtures
   - Patterns: API_KEY, SECRET, PASSWORD, TOKEN, Bearer, sk-, pk_
3. Code pattern review:
   - SQL string concatenation (injection risk)
   - eval() or Function() usage
   - Unsanitized user input in templates (XSS risk)
   - Insecure HTTP URLs for API calls
   - Disabled TLS verification
4. Permission and access:
   - Files with overly broad permissions (777, world-writable)
   - .env or credentials files without .gitignore coverage

Output format: Markdown report
Sections:
- Critical findings (act immediately)
- High findings (fix this sprint)
- Medium findings (schedule for next sprint)
- Informational (note for future reference)

Each finding: severity, file:line, description, remediation.
```

---

## Friday Wrap-Up

**Schedule:** Fridays at 4:30pm  
**Purpose:** Close out the week and set up next week.

```
Friday Wrap-Up

1. Scan git log for this week's activity:
   - Commits by author and day
   - PRs merged, opened, and still in review
   - Issues closed and opened
2. Identify incomplete work:
   - Open PRs with no review activity
   - Issues started but not closed
   - Branches with commits but no PR
3. Generate carry-forward list for next week
4. Summarize wins (PRs merged, issues resolved)
5. Note any blockers that persisted through the week

Output format: Markdown weekly summary
Sections:
- This week's wins
- Carry-forward items
- Blockers
- Stats (commits, PRs, issues)
```

---

## Monday Setup

**Schedule:** Mondays at 7:00am  
**Purpose:** Prepare the workspace for a productive week.

```
Monday Setup

1. Create weekly folder: notes/YYYY/w##-MM-DD/
2. Pull latest from main on all active branches
3. Check CI status across open PRs
4. Review calendar for the week to identify:
   - Deep work windows (2+ hour blocks with no meetings)
   - Meeting-heavy days (adjust expectations)
5. Pull carry-forward items from last Friday's wrap-up
6. Generate a prioritized task list for the week

Output format: Markdown file at notes/YYYY/w##-MM-DD/plan.md
```

---

## Tech Debt Tracker

**Schedule:** Wednesdays at 3:00pm  
**Purpose:** Quantify and prioritize technical debt.

```
Tech Debt Assessment

For each source file, compute a debt score:
  Score = (Change Frequency x Bug Density x Complexity) / Test Coverage

Where:
- Change Frequency: number of commits touching this file in the last 90 days
- Bug Density: number of bug-fix commits touching this file in the last 90 days
- Complexity: lines of code / number of functions (rough proxy)
- Test Coverage: 1 if test file exists for this module, 0.5 if partial, 0.1 if none

Output:
- Top 10 files by debt score
- Trend vs. last week (if prior report exists)
- Recommended refactoring targets (files with high score AND high change frequency)

Write to: reports/tech-debt-YYYY-MM-DD.md
```

---

## Tips

- **Stagger schedules**: Don't run all weekly routines on Monday. Spread them across the week to avoid notification overload and stay within daily run limits.
- **Reports directory**: Create a `reports/` directory and add it to `.gitignore` for local routine output, or commit it for team visibility.
- **Progressive rollout**: Start with one or two routines. Add more once you've tuned the prompts to your codebase.
- **Combine with hooks**: Use a `SessionStart` hook to surface the latest weekly report when you open Claude Code on Monday morning.
