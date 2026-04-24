# Nightly Maintenance Routine

**Schedule:** Nightly, midnight–2 AM · **Trigger:** Cron or scheduled task · **Requires:** GitHub CLI (`gh`), optionally Linear/Jira MCP

## What It Does

Runs background housekeeping while you sleep. Covers issue triage, test coverage gaps, dependency scanning, documentation drift, and optionally attempts automated bug fixes. You wake up to a status report and (sometimes) draft PRs ready for review.

## Setup

### As a Scheduled Task

```bash
claude schedule create \
  --name "nightly-maintenance" \
  --cron "0 0 * * 1-5" \
  --prompt "$(cat <<'EOF'
Run nightly maintenance for this repository.

## 1. Issue Triage
- Fetch issues opened in the last 24 hours
- Apply labels based on content (bug, feature, docs, question)
- Assign to code owners based on file paths mentioned
- Post a triage summary as a comment on each issue

## 2. Test Coverage
- Identify test files and the testing framework
- Find functions/methods with no corresponding test
- Generate tests matching the existing test suite style
- Open a draft PR titled "test: improve coverage for [area]"
- Only include tests that pass locally

## 3. Dependency Check
- Run `npm audit` (or equivalent for the project's package manager)
- Filter for severity: high and critical only
- For each vulnerability:
  - Check if an update is available
  - Check if the update has breaking changes
  - If safe to update, include in a draft PR
  - If breaking, document in the report

## 4. Documentation Drift
- Check PRs merged in the last 24 hours
- For each merged PR, identify documentation that references modified functions, APIs, or config
- If docs are outdated, open a draft PR with updates
- If uncertain, flag in the report for manual review

## 5. Optional: Bug Fix Attempt
- Pick the oldest open bug labeled "good-first-issue" or with low complexity
- Attempt a fix
- Open a draft PR if tests pass
- If fix attempt fails, add a comment to the issue with findings

## Output
Write a maintenance report to `reports/nightly/YYYY-MM-DD.md`:

### Triage
- Issues processed: X
- Labels applied: X
- Assigned: X

### Coverage
- New tests added: X
- Draft PR: #NNN (or "none needed")

### Dependencies
- Vulnerabilities found: X high, X critical
- Auto-fixable: X
- Draft PR: #NNN (or "none needed")

### Docs
- Outdated docs found: X
- Draft PR: #NNN (or "none needed")

### Bug Fix
- Attempted: [issue number] or "skipped"
- Result: [fixed / partial / failed]
- Draft PR: #NNN (or "none")
EOF
)"
```

## Module Breakdown

You don't have to run everything. Pick the modules that match your needs:

### Issue Triage Only

```bash
claude schedule create \
  --name "nightly-triage" \
  --cron "0 0 * * 1-5" \
  --prompt "Fetch issues opened today, apply labels, assign to code owners, and post a summary."
```

### Dependency Audit Only (Weekly)

```bash
claude schedule create \
  --name "weekly-deps" \
  --cron "0 2 * * 1" \
  --prompt "Run dependency audit. Report high/critical vulnerabilities. Open a draft PR for safe updates."
```

### Documentation Drift Only (Weekly)

```bash
claude schedule create \
  --name "weekly-docs-drift" \
  --cron "0 1 * * 1" \
  --prompt "Scan PRs merged in the past 7 days. Flag documentation referencing modified functions or APIs. Open update PRs where confident, report uncertain cases."
```

## Example Report

```markdown
# Nightly Maintenance — 2026-04-24

### Triage
- Issues processed: 3
- Labels applied: bug (2), enhancement (1)
- Assigned: @alex (payments), @sarah (auth), unassigned (1 — unclear ownership)

### Coverage
- New tests added: 4 (payments-service/handlers)
- Draft PR: #854 "test: add handler coverage for refund flow"
- Note: skipped async retry logic — needs integration test, not unit test

### Dependencies
- Vulnerabilities: 1 high (lodash prototype pollution), 0 critical
- lodash 4.17.20 → 4.17.21 is safe, non-breaking
- Draft PR: #855 "chore: bump lodash to fix CVE-2025-XXXX"

### Docs
- 1 merged PR (#852) changed the /api/auth/refresh endpoint
- API docs reference old response format
- Draft PR: #856 "docs: update auth refresh endpoint response format"

### Bug Fix
- Attempted: #841 "Login fails with special characters in password"
- Result: Fixed — the issue was unescaped regex in the validation layer
- Draft PR: #857 "fix: escape special characters in password validation"
```

## Safety

- **All changes go to draft PRs** — nothing merges without your review
- **Tests must pass** before opening any PR
- **Bug fixes are limited** to issues tagged low-complexity or good-first-issue
- **Dependency updates** skip major version bumps unless explicitly configured
- Add `--dry-run` to the prompt to generate reports without opening PRs

## Tips

- **Start with triage + deps** for the first week. Add coverage and docs-drift after you're comfortable with the output quality.
- **Review draft PRs in your morning briefing** — add "check nightly maintenance PRs" to your briefing prompt.
- **Tune issue labeling** after the first week — add project-specific label rules to improve accuracy.
- **The bug fix module is optional** and experimental — only enable it for repos with strong test coverage.
