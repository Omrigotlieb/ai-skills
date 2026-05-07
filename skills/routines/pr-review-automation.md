# Automated PR Review Routine

Reviews pull requests for logic errors, security issues, and edge cases -- acting as a senior engineer, not a linter.

---

## Overview

| Property | Value |
|----------|-------|
| **Trigger** | `pull_request.opened`, `pull_request.synchronize`, or daily cron |
| **Duration** | 1-3 minutes per review |
| **Key principle** | Review like a senior engineer, not a linter |

## Setup

### Single-Pass Review

```bash
claude schedule create \
  --name "pr-review" \
  --cron "0 8 * * 1-5" \
  --prompt "$(cat <<'EOF'
Review open pull requests. Focus on issues that matter:

## Review Checklist
1. **Logic errors** -- incorrect conditions, off-by-one, race conditions, null handling
2. **Edge cases** -- empty inputs, boundary values, concurrent access, error paths
3. **Security** -- injection, auth bypass, data exposure, secrets in code
4. **Performance** -- N+1 queries, unbounded collections, missing indexes, expensive loops
5. **Breaking changes** -- API contract changes, config format changes, migration needs

## Rules
- Ignore formatting, import order, and naming style (that is what linters are for)
- Only comment when you have a specific concern with a specific fix
- Rate each finding: Critical / High / Medium / Low
- If the PR is clean, approve with a brief note -- do not manufacture feedback
- For each issue, explain the impact (what breaks, what leaks, what slows down)

## Output
Post inline comments on the relevant lines.
End with a summary comment:
- **Verdict:** APPROVE / REQUEST CHANGES / COMMENT
- **Risk areas:** [list any files or patterns that deserve extra human attention]
- **Test coverage:** [note if new code paths lack tests]
EOF
)"
```

### Multi-Pass Review Council

Run multiple focused reviews from different expert perspectives. Each pass catches different classes of issues.

```markdown
Run three sequential review passes on this PR:

## Pass 1: Security Review
Assume this code was written by a junior developer unfamiliar with security.
Look for: injection (SQL, command, XSS), auth/authz gaps, data exposure,
secrets in code, SSRF, path traversal, insecure deserialization.
Rate: Critical / High only. Skip Medium/Low for this pass.

## Pass 2: Performance Review
Focus on: database query patterns (N+1, missing indexes, full table scans),
memory allocation (unbounded collections, large objects in loops),
concurrency (race conditions, deadlocks, thread safety),
caching opportunities (repeated expensive computations).

## Pass 3: Architecture Review
Focus on: does this change fit the existing patterns in this codebase?
Are there existing utilities being reinvented? Is the abstraction level right?
Will this be maintainable in 6 months by someone who didn't write it?
Are there implicit dependencies that should be explicit?

## Output
Combine findings from all three passes. Deduplicate if the same issue
was caught by multiple passes. Present as a single review with sections.
```

## Filter Configuration

Not every PR needs a full review. Match review depth to change risk.

### By File Path

```yaml
# High-risk paths: full review council
high_risk:
  paths:
    - "src/auth/**"
    - "src/payments/**"
    - "migrations/**"
    - "infrastructure/**"
  review: council

# Standard paths: single-pass review
standard:
  paths:
    - "src/**"
  review: single

# Low-risk paths: quick scan only
low_risk:
  paths:
    - "docs/**"
    - "*.md"
    - "tests/**"
  review: quick
```

### By PR Metadata

```markdown
## Filter Rules
- Skip draft PRs (review when marked ready)
- Skip PRs labeled "skip-ai-review" or "trivial"
- Skip PRs from bots (dependabot, renovate) unless they touch lock files
- Always review PRs labeled "security" or "breaking-change" with full council
- PRs with > 500 lines changed: flag as "needs splitting" before reviewing
```

## The Review Feedback Triage Pattern

For handling review feedback on your own PRs:

```markdown
For each review comment on this PR:

| Finding | Verdict | Reasoning | Action |
|---------|---------|-----------|--------|
| [comment] | Fix | [why it is valid] | [specific change] |
| [comment] | Dismiss | [why it is not applicable] | Reply with explanation |
| [comment] | Escalate | [why it needs discussion] | Flag for human decision |

## Rules
- Fix: clear issue with clear fix. Apply the fix and push.
- Dismiss: style preference, false positive, or misunderstanding of context. Reply politely.
- Escalate: architectural concern, tradeoff decision, or disagreement. Do not resolve unilaterally.
- Maximum 3 fix iterations per review cycle. If still getting changes-requested after 3, escalate.
```

## Anti-Patterns to Avoid

1. **The Nitpick Machine** -- Commenting on every line just to comment. If the code works and is readable, approve it.
2. **The Blind Fixer** -- Applying every suggestion without evaluating it. Use the triage pattern.
3. **The Auto-Merger** -- Never merge automatically. Review routines suggest; humans decide.
4. **The Style Police** -- Enforcing formatting in reviews. Use pre-commit hooks and linters instead.
5. **The Essay Writer** -- Writing paragraph-long comments. One sentence for the issue, one for the fix.

## Example Output

```markdown
## PR Review Summary

**Verdict:** REQUEST CHANGES

### Critical
- `src/auth/login.ts:47` -- SQL query built via string concatenation.
  Use parameterized queries to prevent SQL injection.

### High
- `src/api/users.ts:123` -- Missing authorization check on DELETE endpoint.
  Any authenticated user can delete any other user's account.

### Medium
- `src/services/cache.ts:89` -- Cache TTL set to 24 hours for user session data.
  If permissions change, stale cache could grant access for up to 24h.
  Suggest reducing to 15 minutes or invalidating on permission change.

### Test Coverage
- New auth endpoints in `src/auth/login.ts` have no test file.

**Risk areas:** auth module (security-sensitive), cache invalidation logic
```

## Resources

- [CodeScene: AI Coding Best Practice Patterns](https://codescene.com/blog/agentic-ai-coding-best-practice-patterns-for-speed-with-quality)
- [PR Babysitting Pattern](https://www.solberg.is/babysit-pr)
