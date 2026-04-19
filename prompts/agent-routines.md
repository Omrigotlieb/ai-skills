# Agent Routine Prompt Templates

Copy-ready prompt templates for Claude Code routines and scheduled agents. Each template is tested for autonomous execution — no human in the loop.

> See [Daily Routines Guide](../workflows/daily-routines.md) for the daily schedule overview, setup guide, and trigger configuration. This file focuses on copy-ready prompts; the guide covers strategy and scheduling context.

## Quick Navigation

- [Morning Routines](#morning-routines)
- [Code Quality](#code-quality)
- [DevOps and Infrastructure](#devops-and-infrastructure)
- [Communication](#communication)
- [Maintenance](#maintenance)
- [Prompt Writing Patterns](#prompt-writing-patterns)

---

## Morning Routines

### Daily Standup Digest

**Trigger:** Schedule, weekdays at 8:30 AM
**Connectors:** Slack, GitHub

```
Compile a standup digest for the team:

1. List all PRs merged since yesterday 5 PM with one-line summaries
2. List all PRs currently awaiting review, sorted by age
3. List new issues opened in the last 24 hours with labels and assignees
4. Check CI status on the main branch

Post to #standup in Slack with this format:

**Merged Yesterday**
- PR #123: Added user auth (by @alice)

**Awaiting Review**
- PR #456: Fix payment flow (by @bob, open 2 days) ⚠️

**New Issues**
- #789: Login timeout on mobile [bug, P1] → @carol

**CI Status**: ✅ Passing / ❌ Failing (link to failing workflow)

If nothing happened overnight, post: "Quiet night — no changes since yesterday."
```

---

### Overnight Activity Report

**Trigger:** Schedule, daily at 7:00 AM
**Connectors:** Slack, monitoring tool

```
Generate an overnight activity report covering 6 PM yesterday to 7 AM today:

Check:
1. Commits pushed to any branch
2. CI/CD pipeline runs and their results
3. Error rate changes in monitoring (if connected)
4. New issues or comments on existing issues

Produce a brief report:
- Total commits: X across Y branches
- CI: X passed, Y failed (list failures)
- Errors: any new error patterns vs baseline
- Issues: new issues or notable comments

Post to #dev-morning in Slack. Keep it under 20 lines.
If nothing happened: "All quiet overnight."
```

---

## Code Quality

### PR Review Checklist

**Trigger:** GitHub `pull_request.opened`, filter: `is_draft = false`
**Connectors:** GitHub

```
Review this pull request systematically:

**Pass 1 — Security**
- Scan for hardcoded secrets, tokens, API keys
- Check for injection vulnerabilities (SQL, XSS, command)
- Verify input validation on public endpoints
- Check authentication/authorization on new endpoints

**Pass 2 — Correctness**
- Verify edge case handling (null, empty, boundary values)
- Check error handling (are errors caught and handled appropriately?)
- Verify test coverage for new code paths
- Check for race conditions in concurrent code

**Pass 3 — Quality**
- Flag dead code, unused imports, debug statements
- Check naming consistency with the rest of the codebase
- Identify overly complex functions (>50 lines, >3 nesting levels)
- Look for duplicated logic that should be extracted

For each finding, leave an inline comment:
- **[Critical]** Must fix before merge
- **[Warning]** Should fix, but not a blocker
- **[Suggestion]** Nice to have improvement

Add a summary comment at the end:
"Reviewed X files, Y lines changed. Found: Z critical, W warnings, V suggestions."
If clean: "LGTM — no issues found."

Skip files: package-lock.json, yarn.lock, generated files, vendor/.
```

---

### Test Coverage Check

**Trigger:** GitHub `pull_request.synchronized`
**Connectors:** GitHub

```
Analyze test coverage for the changes in this PR:

1. Identify all new or modified functions/methods
2. Check if each has corresponding test coverage
3. For functions without tests, assess:
   - Is this a pure function? → should have unit tests
   - Does it handle I/O? → should have integration tests
   - Is it a thin wrapper? → test may be optional

Report:
- Functions with tests: list them ✅
- Functions missing tests: list them with recommended test type ❌
- Coverage assessment: "Adequate" / "Needs improvement" / "Insufficient"

If tests are missing for critical paths (auth, payment, data mutation):
leave a comment: "[Critical] Missing test coverage for {function} — this handles {sensitive area}."

If all new code has tests: "Test coverage looks good for this change."
```

---

## DevOps and Infrastructure

### Nightly Dependency Update

**Trigger:** Schedule, daily at 3:00 AM
**Connectors:** GitHub

```
Check dependencies for security vulnerabilities and available updates:

Step 1 — Security audit
Run the appropriate audit command for this project:
- Node.js: npm audit
- Python: pip audit or safety check
- Ruby: bundle audit
- Go: govulncheck
- Rust: cargo audit

Step 2 — Handle vulnerabilities
For Critical/High vulnerabilities:
- Create branch: claude/security-{YYYY-MM-DD}
- Update the affected package to the patched version
- Run the full test suite
- If tests pass: open a PR titled "Security: fix {CVE} in {package}"
- If tests fail: revert and note in the report

Step 3 — Check for updates
List outdated dependencies, grouped by:
- Patch updates: safe to auto-update
- Minor updates: likely safe, review changelog
- Major updates: manual review needed (list only, don't update)

Step 4 — Report
Post to #dev-ops in Slack:
- Security PRs created (if any)
- Patch updates applied (if any)
- Major updates available (for manual review)
- "All clear" if nothing to report

Never update major versions automatically.
Always run tests before opening any PR.
If the test suite takes longer than 15 minutes, note it in the report and proceed.
```

---

### CI Failure Investigator

**Trigger:** API (called by CI pipeline on failure)
**Connectors:** Slack

```
A CI pipeline has failed. The failure details are provided as context.

Investigation:
1. Parse the error output to identify the failing step
2. Determine the failure category:
   - Test failure: which test, what assertion
   - Build failure: which file, what error
   - Lint failure: which rule, which files
   - Infrastructure: timeout, OOM, network
3. Check git log for the most recent commit that could have caused this
4. Read the relevant code to understand the failure

Report to #ci-alerts in Slack:
- **Pipeline**: {name}
- **Failed step**: {step name}
- **Category**: {test/build/lint/infra}
- **Likely cause**: {one-line explanation}
- **Relevant commit**: {hash} by {author}
- **Suggested fix**: {brief recommendation}

If the failure is infrastructure-related (timeout, OOM):
note "Infrastructure issue — retry may resolve" and don't assign blame.

If the failure is clearly a code issue:
tag the commit author in the Slack message.
```

---

### Deploy Smoke Test

**Trigger:** API (called by deploy pipeline)
**Connectors:** Slack

```
A deployment just completed. Run post-deploy verification:

1. Check the health endpoint returns 200
2. Run the smoke test suite if one exists
3. Compare error rates in the last 5 minutes against the 1-hour pre-deploy baseline
4. Check for new error patterns in logs

Assessment:
- **GO**: Health check passes, smoke tests pass, error rate stable
- **WATCH**: Health check passes but error rate elevated 10-25%
- **NO-GO**: Health check fails, smoke tests fail, or error rate >25% increase

Post to #releases in Slack:
"Deploy verification: {GO/WATCH/NO-GO}
- Health: {pass/fail}
- Smoke tests: {X/Y passed}
- Error rate: {current} vs {baseline} ({change%})
- New errors: {none / list}"

If NO-GO: include rollback recommendation but do NOT execute rollback.
If WATCH: schedule a follow-up check in 30 minutes.
```

---

## Communication

### Weekly Changelog Generator

**Trigger:** Schedule, Friday at 3:00 PM
**Connectors:** Slack

```
Generate a weekly changelog from this week's merged PRs:

1. List all PRs merged to main since last Friday
2. Categorize each as: Feature, Fix, Improvement, Docs, Chore
3. Write a human-readable summary for each (not the PR title — the user impact)

Format:
## Week of {date}

### Features
- **User avatars**: Users can now upload and crop profile photos (#234)

### Fixes
- **Login timeout**: Fixed session expiry causing logout during long forms (#245)

### Improvements
- **Search speed**: Search results now load 40% faster (#251)

### Docs
- **API guide**: Updated authentication examples for v3 (#260)

### Chore
- **Dependencies**: Updated React to 19.1, Next.js to 15.3 (#262)

Post to #changelog in Slack.
Skip PRs labeled "internal" or "chore" from the user-facing sections.
If no PRs merged this week: "No changes shipped this week."
```

---

### Issue Digest for Product Team

**Trigger:** Schedule, weekdays at 10:00 AM
**Connectors:** Slack

```
Create a daily issue digest for the product team:

1. New bug reports (last 24 hours): title, severity, affected area
2. Feature requests (last 24 hours): title, votes/reactions if available
3. Issues closed (last 24 hours): title, resolution type (fixed, won't fix, duplicate)
4. Issues by age: count of issues open >7 days, >30 days, >90 days

Format as a concise digest. Use plain language — this audience is non-technical.
Replace technical terms: "API endpoint" → "server connection", "race condition" → "timing conflict".

Post to #product-updates in Slack.
Keep the total under 30 lines.
```

---

## Maintenance

### Stale Branch Cleanup

**Trigger:** Schedule, weekly Sunday at 2:00 AM
**Connectors:** GitHub

```
Clean up stale branches:

1. List all remote branches except: main, master, develop, staging, release/*
2. For each branch check:
   - Days since last commit
   - Whether it has an open PR
   - Whether it was merged to main

Actions:
- Merged + no open PR → delete
- No commits in 30+ days + no open PR → delete
- Has open PR → skip (regardless of age)
- Protected branch → skip

Report:
- Deleted: list with last commit date
- Skipped (has open PR): list
- Skipped (recent activity): list

Never delete branches with open PRs.
Never delete branches named main, master, develop, staging, or matching release/*.
```

---

### Database Migration Check

**Trigger:** GitHub `pull_request.opened`, filter: title contains "migration" OR files match `**/migrations/**`
**Connectors:** GitHub

```
This PR contains database migrations. Review them for safety:

1. **Reversibility**: Can each migration be rolled back? Is there a down migration?
2. **Locking**: Will any operation lock tables in production?
   - Adding NOT NULL without default → locks table
   - Adding index without CONCURRENTLY → locks table (Postgres)
   - Renaming columns → may break running queries
3. **Data safety**: Could any operation lose data?
   - DROP COLUMN: is the data backed up or unused?
   - ALTER TYPE: could values be truncated?
4. **Performance**: On large tables (>1M rows), flag operations that may be slow
5. **Compatibility**: Can the migration run alongside the current code version?

For each concern, leave an inline comment with severity:
- [Critical]: Will cause downtime or data loss
- [Warning]: May cause issues under load
- [Info]: Worth knowing but safe

Summary comment:
"Migration review: {safe to run / needs changes / needs DBA review}"
```

---

## Prompt Writing Patterns

### The Autonomous Prompt Template

Every routine prompt should follow this structure:

```
[WHAT] — One sentence describing the job

[STEPS] — Numbered list of specific actions

[CRITERIA] — How to evaluate results (pass/fail, thresholds)

[OUTPUT] — Where to post and in what format

[BOUNDARIES] — What the routine must NOT do

[EMPTY CASE] — What to do when there's nothing to process
```

### Example: Applying the Template

```
[WHAT] Check for and fix security vulnerabilities in project dependencies.

[STEPS]
1. Run npm audit (or equivalent for the project type)
2. Parse results for Critical and High severity issues
3. For each: attempt to update the package, run tests

[CRITERIA]
- Success: vulnerability fixed, tests pass
- Partial: vulnerability fixed but tests fail → revert
- Skip: no fix available → log for manual review

[OUTPUT] Post summary to #security in Slack. Open PRs for successful fixes.

[BOUNDARIES] Never update major versions. Never skip tests. Never push to main.

[EMPTY CASE] If no vulnerabilities found: "Security audit clean — no action needed."
```

### Anti-Patterns

| Pattern | Problem | Fix |
|---------|---------|-----|
| `Review the code` | Too vague for autonomous execution | Specify exactly what to check with pass/fail criteria |
| `Fix any issues you find` | Unbounded scope, unpredictable changes | List specific issue types and actions for each |
| `Post a summary` | Where? In what format? | Specify channel, format, and max length |
| No empty case handling | Routine may error or produce confusing output | Always include "if nothing to do" clause |
| Multiple unrelated jobs | Hard to debug, hard to schedule optimally | One routine, one job |

---

## Resources

- [Claude Code Routines Documentation](https://code.claude.com/docs/en/routines)
- [Scheduled Tasks (local)](https://code.claude.com/docs/en/scheduled-tasks)
- [Prompting Best Practices](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices)
- [Daily Routines Guide](../workflows/daily-routines.md)
