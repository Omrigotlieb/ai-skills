# PR Review Automation Routine

## Overview

Automated first-pass code review that catches mechanical issues so human reviewers can focus on design and architecture decisions.

## Configuration

| Setting | Value |
|---|---|
| **Trigger** | GitHub - `pull_request.opened` (non-draft) OR Schedule - Daily at noon |
| **Connectors** | GitHub |
| **Repositories** | Repos requiring review |
| **Run time** | ~3-5 minutes per PR |

## Prompt (GitHub Trigger - Single PR)

```
Review this pull request. Apply the following checklist systematically.

SECURITY (critical - block merge if found):
- SQL injection: check for string concatenation in queries, unparameterized inputs
- XSS: check for unescaped user input in templates or dangerouslySetInnerHTML
- Command injection: check for user input passed to exec, spawn, or system calls
- Path traversal: check for user input in file paths without sanitization
- Secrets: flag hardcoded API keys, tokens, passwords, or connection strings
- Auth: verify new endpoints have proper authentication and authorization checks
- Input validation: check that user input is validated at system boundaries

PERFORMANCE (warning):
- N+1 queries: flag loops that execute database queries
- Missing indexes: check if new query patterns need database indexes
- Unbounded operations: flag queries without LIMIT, loops without bounds
- Large payloads: flag endpoints that could return unbounded data (missing pagination)
- Unnecessary computation: flag expensive operations that could be cached or memoized

CODE QUALITY (suggestion):
- Error handling: verify async operations have error handling, catch blocks aren't empty
- Test coverage: check that new code paths have corresponding test cases
- Dead code: flag unused imports, unreachable code, commented-out blocks
- Naming: flag inconsistencies with existing codebase conventions
- Complexity: flag functions over 50 lines or with cyclomatic complexity > 10

Leave inline comments on specific lines with severity labels:
- [CRITICAL] - Must fix before merge (security issues, data loss risks)
- [WARNING] - Should fix, creates technical debt if ignored
- [SUGGESTION] - Nice to have, improves quality but not blocking

Add a summary comment at the end with:
- Overall assessment: PASS / PASS WITH WARNINGS / NEEDS CHANGES
- Count of findings by severity
- One-paragraph summary of the PR's purpose and quality

RESTRICTIONS:
- Create draft PRs only if suggesting code changes
- Never merge or approve PRs
- Never push to the PR branch directly
- If uncertain about a finding, label it [QUESTION] instead of a false positive
```

## Prompt (Scheduled - Batch Review)

```
Review all open PRs in this repository that:
- Were opened or updated in the last 24 hours
- Are not in draft state
- Have not been reviewed by this routine yet (check for existing bot comments)

For each PR, apply the full review checklist (security, performance, code quality).
Leave inline comments and a summary comment on each.

After reviewing all PRs, post a digest to #code-review:
- Number of PRs reviewed
- PRs with critical findings (link to each)
- PRs that look ready for human review

If no PRs match the criteria, post "No PRs need automated review today" and exit.
```

## GitHub Trigger Filters

Recommended filters for the GitHub trigger:

| Filter | Value | Reason |
|---|---|---|
| Base branch | `main` | Only review PRs targeting main |
| Is draft | `false` | Skip work-in-progress |
| From fork | `true` (optional) | Extra scrutiny for external contributions |

## Customization

**Language-specific checks**: Add language-specific items like "Check for proper use of `async/await`" for TypeScript or "Verify `defer` for resource cleanup" for Go.

**Team standards**: Replace generic quality checks with your team's specific conventions from CLAUDE.md.

**Severity tuning**: Adjust what counts as critical vs. warning based on your codebase's risk profile.
