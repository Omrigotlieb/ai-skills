# GitHub Actions Routine Examples

Copy-paste workflow templates for running Claude Code routines as GitHub Actions. These use the official `anthropics/claude-code-action` action.

---

## Weekly Code Quality Review

Runs every Sunday, reviews random directories, and opens a PR with any fixes.

```yaml
# .github/workflows/weekly-code-quality.yml
name: Weekly Code Quality Review

on:
  schedule:
    - cron: '0 9 * * 0'  # Sundays at 9am UTC
  workflow_dispatch:       # Manual trigger

jobs:
  code-quality:
    runs-on: ubuntu-latest
    timeout-minutes: 30
    permissions:
      contents: write
      pull-requests: write

    steps:
      - uses: actions/checkout@v4

      - uses: anthropics/claude-code-action@v1
        with:
          anthropic_api_key: ${{ secrets.ANTHROPIC_API_KEY }}
          model: claude-sonnet-4-6
          max_turns: 20
          prompt: |
            Weekly Code Quality Review

            1. Scan all source files for:
               - Unused imports
               - Functions over 50 lines
               - Commented-out code blocks (>5 lines)
               - TODO/FIXME comments (list, don't fix)
            2. Fix only mechanical issues (unused imports, formatting)
            3. Don't change logic or behavior
            4. Commit fixes with message "chore: weekly code cleanup"
            5. Summarize findings in a comment

            Skip: node_modules/, vendor/, dist/, *.min.js, generated/
```

---

## Biweekly Dependency Audit

Runs on the 1st and 15th of each month. Only invokes Claude when issues exist.

```yaml
# .github/workflows/dependency-audit.yml
name: Dependency Audit

on:
  schedule:
    - cron: '0 10 1,15 * *'  # 1st and 15th at 10am UTC
  workflow_dispatch:

jobs:
  audit:
    runs-on: ubuntu-latest
    timeout-minutes: 45

    permissions:
      contents: write
      pull-requests: write

    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-node@v4
        with:
          node-version: '20'

      - name: Check for issues
        id: check
        run: |
          npm ci
          OUTDATED=$(npm outdated --json 2>/dev/null || echo '{}')
          AUDIT=$(npm audit --json 2>/dev/null || echo '{}')
          HAS_ISSUES=$(node -e "
            const o = JSON.parse(process.argv[1]);
            const a = JSON.parse(process.argv[2]);
            console.log(Object.keys(o).length > 0 || (a.vulnerabilities && Object.keys(a.vulnerabilities).length > 0) ? 'true' : 'false');
          " "$OUTDATED" "$AUDIT")
          echo "has_issues=$HAS_ISSUES" >> "$GITHUB_OUTPUT"

      - name: Run Claude analysis
        if: steps.check.outputs.has_issues == 'true'
        uses: anthropics/claude-code-action@v1
        with:
          anthropic_api_key: ${{ secrets.ANTHROPIC_API_KEY }}
          model: claude-sonnet-4-6
          max_turns: 40
          timeout_minutes: 45
          prompt: |
            Dependency Audit

            1. Run: npm outdated
            2. Run: npm audit
            3. Analyze outdated packages and security issues
            4. Update packages conservatively:
               - Apply all patch updates
               - Apply minor updates only for packages with no breaking changes
               - Never apply major updates automatically
            5. Run: npm test
            6. If tests pass: commit and create a PR
            7. If tests fail: revert the failing update and note it in the PR description

            PR title: "chore(deps): dependency audit YYYY-MM-DD"
            Include in the PR body:
            - Packages updated (with version changes)
            - Security issues resolved
            - Packages skipped (with reasons)
```

---

## Monthly Documentation Sync

Verifies docs match the codebase after a month of changes.

```yaml
# .github/workflows/docs-sync.yml
name: Monthly Documentation Sync

on:
  schedule:
    - cron: '0 10 1 * *'  # 1st of month at 10am UTC
  workflow_dispatch:

jobs:
  docs-sync:
    runs-on: ubuntu-latest
    timeout-minutes: 30

    permissions:
      contents: write
      pull-requests: write

    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0  # Full history for log analysis

      - uses: anthropics/claude-code-action@v1
        with:
          anthropic_api_key: ${{ secrets.ANTHROPIC_API_KEY }}
          model: claude-sonnet-4-6
          max_turns: 30
          prompt: |
            Monthly Documentation Sync

            1. Run: git log --since="1 month ago" --oneline --name-only
            2. Identify source files that changed
            3. For each changed source file, check if related docs exist
            4. If docs exist, verify they still match the code:
               - Function signatures match
               - Configuration options are current
               - Examples still work
               - CLI flags are accurate
            5. If docs are outdated, update them
            6. If new public APIs lack docs, create stubs
            7. Commit and create PR

            PR title: "docs: monthly sync YYYY-MM-DD"
            Skip: CHANGELOG.md, package.json, lock files
```

---

## PR Review on Open

Automated code review for every new PR.

```yaml
# .github/workflows/pr-review.yml
name: Automated PR Review

on:
  pull_request:
    types: [opened, synchronize]

jobs:
  review:
    runs-on: ubuntu-latest
    timeout-minutes: 15

    permissions:
      contents: read
      pull-requests: write

    steps:
      - uses: actions/checkout@v4

      - uses: anthropics/claude-code-action@v1
        with:
          anthropic_api_key: ${{ secrets.ANTHROPIC_API_KEY }}
          model: claude-sonnet-4-6
          max_turns: 15
          prompt: |
            Review this pull request.

            Checklist:
            1. Logic correctness and edge cases
            2. Security issues (injection, auth, data exposure)
            3. Error handling completeness
            4. Performance concerns (N+1, unbounded loops)
            5. Test coverage for new code paths
            6. Style consistency with existing codebase

            Read CLAUDE.md and REVIEW.md if they exist for project-specific rules.

            Post inline comments for specific issues.
            Post a summary comment with overall assessment.

            Be constructive. Don't flag style issues handled by linters.
            Focus on logic, security, and correctness.
```

---

## Weekly Security Scan

```yaml
# .github/workflows/security-scan.yml
name: Weekly Security Scan

on:
  schedule:
    - cron: '0 10 * * 1'  # Mondays at 10am UTC
  workflow_dispatch:

jobs:
  security:
    runs-on: ubuntu-latest
    timeout-minutes: 30

    permissions:
      contents: read
      issues: write

    steps:
      - uses: actions/checkout@v4

      - uses: anthropics/claude-code-action@v1
        with:
          anthropic_api_key: ${{ secrets.ANTHROPIC_API_KEY }}
          model: claude-sonnet-4-6
          max_turns: 25
          prompt: |
            Weekly Security Scan

            1. Check dependencies for known CVEs:
               - Run: npm audit (or equivalent)
               - Flag Critical and High severity
            2. Scan source code for:
               - Hardcoded secrets (API keys, passwords, tokens)
               - SQL string concatenation
               - eval() or Function() usage
               - Unsanitized user input in templates
               - HTTP URLs for API calls (should be HTTPS)
            3. Check configuration:
               - .env files not in .gitignore
               - Overly permissive CORS settings
               - Debug mode enabled in production config

            Output: Create a GitHub issue titled "Security scan: YYYY-MM-DD"
            Label: security
            Include severity, file:line, description, and remediation for each finding.
            If no issues found, don't create an issue.
```

---

## Cost Estimates

Approximate costs per run using `claude-sonnet-4-6`. Estimates assume a ~50k-line codebase; costs scale with repository size and number of files analyzed:

| Routine | Frequency | Est. cost/run | Monthly cost |
|---------|-----------|--------------|--------------|
| Code Quality | Weekly | $1-5 | $4-20 |
| Dependency Audit | Biweekly | $0.20-1.00 | $0.40-2.00 |
| Docs Sync | Monthly | $0.50-2.00 | $0.50-2.00 |
| PR Review | Per PR | $0.10-0.50 | Varies |
| Security Scan | Weekly | $0.50-2.00 | $2-8 |

---

## Tips

- **Secrets**: Store your `ANTHROPIC_API_KEY` in GitHub repository secrets. Never commit it.
- **Model choice**: Use `claude-sonnet-4-6` for routine tasks (cost-effective). Reserve `claude-opus-4-6` for complex reviews requiring deep reasoning.
- **Timeouts**: Set generous timeouts (30-45 min) for routines that modify code. Set shorter timeouts (15 min) for read-only reviews.
- **Manual trigger**: Always include `workflow_dispatch` so you can test routines without waiting for the schedule.
- **Branch protection**: Ensure the GitHub Actions bot can push to branches and create PRs. You may need to adjust branch protection rules.
- **Conditional runs**: Gate Claude invocation behind a check step (like the dependency audit example) to avoid burning API credits when there's nothing to do.
