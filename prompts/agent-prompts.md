# Agent Prompt Templates

Ready-to-use prompt templates for autonomous and semi-autonomous Claude Code agents. These prompts are designed for scheduled tasks, routines, and loop-based workflows.

## Prompt Design Principles

1. **Be explicit about success criteria** - define what "done" looks like
2. **Set boundaries** - specify what the agent should and should not do
3. **Include output format** - tell the agent how to report results
4. **Start non-destructive** - create PRs but never merge, read but never respond
5. **Cap iterations** - always set a maximum number of fix attempts

---

## Daily Maintenance Agent

```
You are a project maintenance assistant. Perform the following checks
and report ONLY if there is something actionable:

1. List issues opened in the last 24 hours: `gh issue list --state open`
2. List PRs opened in the last 24 hours: `gh pr list --state open`
3. Run the test suite and note any failures
4. Run dependency audit for security vulnerabilities
5. Check for merge conflicts on open PRs

For security-critical fixes, create a PR on a new branch.
For non-critical findings, include in summary only.
Send email summary grouped by category if anything found.
Stay silent if everything is clean.
```

## PR Review Agent

```
Review this PR against the team's quality checklist.

Check for:
- Security issues: SQL injection, XSS, command injection, hardcoded secrets
- Performance concerns: N+1 queries, missing indexes, unbounded loops
- Error handling: uncaught exceptions, missing validation at boundaries
- Test coverage: new code paths without tests

Leave inline comments with severity labels:
- CRITICAL: must fix before merge
- WARNING: should fix, but not a blocker
- SUGGESTION: optional improvement

Add a summary comment with overall pass/fail status.
Focus on bugs and security. Skip style nits covered by linters.
```

## CI Fix Agent

```
The CI pipeline has failed. Diagnose and fix:

1. Run `gh pr checks` to identify which checks failed
2. For each failing check, run `gh run view <id> --log-failed`
3. Analyze the failure:
   - Test failure: read the test, understand the assertion, fix the code
   - Lint failure: apply the required formatting or style fix
   - Build failure: check for missing imports, type errors, syntax issues
   - Dependency failure: update lockfile or fix version constraints
4. Apply minimal fixes. Do not refactor unrelated code.
5. Run the tests locally to verify the fix
6. Commit and push with a clear message explaining what was fixed

Stop after 3 fix attempts. If still failing, report what you tried
and what the remaining issue is.
```

## Code Review Response Agent

```
Review comments have been left on this PR. Address them:

1. Read each unresolved review comment
2. Triage into categories:
   - Fix: the reviewer is right, apply the change
   - Discuss: you disagree, leave a reply explaining why
   - Clarify: the comment is ambiguous, ask a follow-up question
3. For each "Fix" item:
   - Make the change
   - Reply to the comment confirming the fix
4. For each "Discuss" item:
   - Write a respectful reply with your reasoning
   - Do not change the code
5. Push all fixes in a single commit

Never dismiss review comments without explanation.
Never force-push or rewrite history.
```

## Security Audit Agent

```
Perform a security review of this codebase:

1. Check for OWASP Top 10 vulnerabilities:
   - Injection (SQL, command, LDAP)
   - Broken authentication
   - Sensitive data exposure
   - XXE, XSS, CSRF
   - Insecure deserialization
   - Components with known vulnerabilities
2. Scan for hardcoded secrets:
   - API keys, tokens, passwords in source
   - .env files committed to git
   - Credentials in config files
3. Review authentication and authorization:
   - Password hashing (bcrypt/argon2, not MD5/SHA1)
   - Session management
   - Role-based access control
4. Check dependency security:
   - Run `npm audit` / `pip audit` / equivalent
   - Flag dependencies with known CVEs

Report findings with:
- Severity (critical/high/medium/low)
- File and line number
- Description and remediation suggestion
- CWE reference where applicable

Do not modify code. This is an audit.
```

## Deploy Verification Agent

```
A deployment just completed. Verify it:

1. Check deployment status via CI/CD pipeline
2. Run smoke tests:
   - Hit the health check endpoint
   - Verify the main page loads (2xx response)
   - Test one authenticated endpoint
   - Check API response times are within baseline
3. Monitor error logs for 10 minutes:
   - Compare error rate with pre-deploy baseline
   - Flag any new error patterns
   - Check for elevated 5xx responses
4. Report status:
   - GREEN: all checks pass, error rates normal
   - YELLOW: checks pass but anomalies detected
   - RED: smoke test failures or error spike

Never trigger rollback. Report and let humans decide.
Include specific error messages and timestamps in the report.
```

## Weekly Report Agent

```
Generate a weekly development report covering the past 7 days:

1. Merged PRs: `gh pr list --state merged --search "merged:>YYYY-MM-DD"`
   - Group by: features, fixes, refactoring, docs, dependencies
   - Note any breaking changes
2. Open PRs: `gh pr list --state open`
   - Age and review status
   - Flag any PR open > 5 days
3. Issues: `gh issue list`
   - Opened vs closed this week
   - Oldest open issues
4. CI health:
   - Success rate for the week
   - Average build time
5. Contributors:
   - Who merged what (summary, not detailed)

Format as a concise report suitable for a team standup or email.
Keep under 40 lines.
```

## Dependency Upgrade Agent

```
Check for safe dependency upgrades:

1. Identify all dependencies with available non-major updates
2. For each upgrade candidate:
   a. Check the changelog for breaking changes
   b. Apply the upgrade
   c. Run the full test suite
   d. If tests pass, keep the upgrade
   e. If tests fail, revert and note the failure
3. Create a single PR with all successful upgrades
4. Include in the PR description:
   - List of upgraded packages with old and new versions
   - Summary of notable changes from changelogs
   - Any failed upgrade attempts and why

Never upgrade major versions without explicit approval.
Group related packages (e.g., @types/* with their parent).
```

## Documentation Sync Agent

```
Check documentation for staleness:

1. List PRs merged in the last 7 days that changed:
   - Function signatures or API endpoints
   - Configuration options or environment variables
   - Database schemas or data models
   - CLI commands or flags
2. For each changed item, search docs/ and README files for references
3. Flag any documentation that references:
   - Renamed functions or variables
   - Removed configuration options
   - Changed API response formats
   - Outdated examples

Output a list of docs that need updating with:
- File path and line number
- What changed and when (PR reference)
- Suggested update

Do not modify documentation. Create a report for human review.
```

---

## Tips for Writing Agent Prompts

### Do
- Define clear stop conditions
- Set maximum iteration counts
- Specify the output format
- Include error handling instructions
- Use concrete tool commands (`gh pr list`, not "check PRs")

### Don't
- Let agents run indefinitely
- Allow destructive actions without human approval
- Skip the triage step (Fix/Dismiss/Escalate)
- Assume the agent has context from previous runs
- Mix monitoring and modification in the same prompt

### Template Structure

```
[Role and context]

[Numbered steps with specific commands]

[Output format and reporting instructions]

[Boundaries and stop conditions]
```

---

## Resources

- [Routines and Scheduled Tasks](../routines/README.md)
- [Automation Skills](../skills/automation/README.md)
- [Workflows](../workflows/README.md)
- [Claude Code Routines Documentation](https://code.claude.com/docs/en/routines)
