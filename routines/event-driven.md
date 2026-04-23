# Event-Driven Routines

Routines triggered by external events rather than schedules. These respond to PRs, deploys, alerts, and other signals in real time.

---

## PR Review Automation

**Trigger:** `pull_request.opened` or `pull_request.synchronize`  
**Purpose:** Consistent, thorough code review on every PR.

```
Review this pull request.

Apply the following checklist:
1. Logic correctness: trace the main code path and verify it handles the stated goal
2. Edge cases: null/empty inputs, boundary values, concurrent access
3. Security: injection vectors, auth gaps, data exposure, hardcoded secrets
4. Performance: N+1 queries, missing indexes, unbounded loops, large allocations
5. Error handling: are errors caught, logged, and surfaced appropriately?
6. Test coverage: do tests cover the happy path AND failure modes?
7. Style: does the code follow existing patterns in the codebase?

Read CLAUDE.md and REVIEW.md (if present) for project-specific review instructions.

Output: Inline comments on specific lines for issues found.
Post a summary comment with:
- Overall assessment (approve, request changes, comment)
- Issues by severity (Critical > High > Medium > Low)
- Positive callouts (good patterns worth noting)
```

### REVIEW.md Template

Create a `REVIEW.md` at your project root to customize automated reviews:

```markdown
# Review Instructions

## Always Check
- All API endpoints must validate input with zod schemas
- Database queries must use parameterized statements
- New endpoints must have corresponding integration tests

## Skip
- Don't flag CSS formatting issues (handled by Prettier)
- Don't flag import ordering (handled by ESLint)

## Context
- We use a custom auth middleware in src/middleware/auth.ts
- Rate limiting is handled at the API gateway level, not in application code
```

---

## Deploy Verification

**Trigger:** API call from CD pipeline after production deploy  
**Purpose:** Automated smoke test and regression check after every deploy.

```
Post-Deploy Verification

1. Identify what was deployed:
   - Compare the deployed commit SHA against the previous deploy
   - List files changed and their categories (API, UI, config, infra)
2. Run smoke checks:
   - Verify health endpoint responds 200
   - Check that critical API endpoints return expected status codes
   - Verify database connectivity
3. Scan error logs (last 15 minutes):
   - Compare error rate against baseline (pre-deploy average)
   - Flag any new error types not seen before the deploy
4. Decision:
   - If error rate increased >2x: post "ROLLBACK RECOMMENDED" to release channel
   - If new error types detected: post "INVESTIGATE" with stack traces
   - If all clear: post "DEPLOY VERIFIED" with commit summary

Output: Post to Slack release channel via Slack MCP.
```

---

## Alert Triage

**Trigger:** Webhook from monitoring tool (Datadog, Sentry, PagerDuty)  
**Purpose:** Automated first-response to production alerts.

```
Alert Triage

Input: Error message and stack trace from monitoring alert.

1. Parse the stack trace to identify the originating file and function
2. Read the relevant source code (the function and its callers)
3. Check git blame: who last modified this code and when?
4. Check recent commits: was this file changed in the last 48 hours?
5. Correlate with recent deploys: did a deploy happen in the last hour?
6. Assess severity:
   - Does this affect user-facing functionality?
   - Is data integrity at risk?
   - Is this a new error or a recurring one?
7. If a likely fix is identified:
   - Open a draft PR with the proposed fix
   - Tag the on-call engineer for review
8. Post triage summary to the incident channel

Output: Slack message with triage summary and (optionally) a draft PR link.
```

---

## Issue-to-PR Automation

**Trigger:** GitHub issue labeled with `auto-fix` or `claude`  
**Purpose:** Automatically attempt to resolve well-specified issues.

```
Issue-to-PR Automation

1. Read the issue title and body
2. Read any linked issues or referenced PRs
3. Analyze the codebase to understand the affected area
4. Implement the fix or feature described in the issue
5. Write tests for the change
6. Run the test suite to verify nothing breaks
7. Open a PR that:
   - References the original issue (Closes #NNN)
   - Describes what was changed and why
   - Lists any assumptions made
   - Includes test results

Constraints:
- Only modify files directly related to the issue
- Keep the diff under 300 lines
- If the issue is ambiguous, add a comment asking for clarification instead of guessing
- Never modify CI/CD configuration, security-critical code, or database migrations
```

---

## PR Merge Notification

**Trigger:** `pull_request.closed` (merged)  
**Purpose:** Keep the team informed and trigger downstream actions.

```
PR Merge Notification

1. Summarize the merged PR:
   - Title and author
   - Files changed and lines added/removed
   - Key changes in plain language
2. Check if the PR affects:
   - API contracts (changes to request/response schemas)
   - Database schemas (migrations)
   - Configuration (environment variables, feature flags)
   - Dependencies (package.json, requirements.txt)
3. If API changes detected: flag for documentation update
4. If migration detected: flag for DBA review
5. Post summary to the team channel

Output: Slack message with PR summary and any flags.
```

---

## Library Port

**Trigger:** `pull_request.closed` (merged) in a primary SDK repo  
**Purpose:** Keep SDK implementations in sync across languages.

```
Library Port

1. Read the merged PR to understand the change:
   - What feature, fix, or behavior was added?
   - What tests were included?
2. Identify the equivalent files in the target SDK repo
3. Port the change:
   - Translate the logic to the target language idioms
   - Adapt to the target SDK's patterns and conventions
   - Write equivalent tests
4. Open a PR in the target repo:
   - Title: "port: [original PR title] (from [source-lang] SDK)"
   - Reference the original PR
   - Note any adaptation decisions

Constraints:
- Only port if the change is logic, not language-specific tooling
- Flag any change that doesn't have a clear equivalent in the target language
```

---

## Changelog Generation

**Trigger:** GitHub release created or tag pushed  
**Purpose:** Automatically generate release notes from commit history.

```
Changelog Generation

1. Get all commits since the last release tag
2. Categorize each commit:
   - Features (feat:)
   - Bug fixes (fix:)
   - Breaking changes (BREAKING CHANGE or !)
   - Performance (perf:)
   - Documentation (docs:)
   - Other (chore, refactor, style, test)
3. Group by category and write human-readable descriptions
4. Highlight breaking changes at the top with migration instructions
5. Credit contributors

Output format: Markdown changelog entry
Add to CHANGELOG.md under a new version heading.
Also update the GitHub release description.
```

---

## Tips

- **Filters**: Event-driven routines should filter early. Check PR labels, base branch, author, and draft status before doing expensive analysis.
- **Idempotency**: If a routine posts comments, check for existing comments from the bot before posting duplicates. Update existing comments instead.
- **Rate limits**: GitHub API has rate limits. Batch API calls and cache responses when processing multiple PRs.
- **Graceful degradation**: If an external service (Slack, Sentry) is down, write the output to a local file instead of failing silently.
- **Security boundaries**: Never give event-driven routines write access to production databases, CI/CD config, or deployment pipelines. Keep them to code analysis and PR creation.
