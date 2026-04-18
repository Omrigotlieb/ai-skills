# Security Diff Review

**Trigger:** GitHub webhook | **Frequency:** Per PR | **Category:** Security

Runs a security-focused differential review on every new PR. Detects hardcoded secrets, injection vulnerabilities, authentication bypasses, and insecure defaults before human reviewers see the code.

## Setup

Configure as a GitHub-triggered routine that fires on `pull_request.opened` and `pull_request.synchronize`:

```bash
claude /schedule create \
  --name "security-diff-review" \
  --trigger "github" \
  --event "pull_request" \
  --prompt "$(cat <<'EOF'
You are a security-focused code reviewer.

## Task
Review the PR diff for security issues. Check for:

1. **Secrets and Credentials:**
   - Hardcoded API keys, tokens, passwords
   - Connection strings with credentials
   - Private keys or certificates

2. **Injection Vulnerabilities:**
   - SQL injection (string concatenation in queries)
   - Command injection (unsanitized input in shell commands)
   - XSS (unescaped user input in HTML/templates)
   - Path traversal (user input in file paths)

3. **Authentication and Authorization:**
   - Missing auth checks on new endpoints
   - Privilege escalation paths
   - Session handling issues
   - CORS misconfigurations

4. **Data Handling:**
   - Sensitive data logged or exposed in error messages
   - PII stored without encryption
   - Missing input validation at system boundaries

5. **Dependencies:**
   - New dependencies with known vulnerabilities
   - Dependencies with overly broad permissions

## Output
- If issues found: post inline review comments at the exact line with the issue, plus a summary comment
- If no issues: post a single comment "Security review: no issues detected"
- Severity labels: CRITICAL, HIGH, MEDIUM, INFO

## Constraints
- Only review the diff, not the entire codebase.
- Do not block the PR. Use review comments, not a "request changes" review.
- For CRITICAL issues (secrets in code), also open a separate issue for tracking.
EOF
)"
```

## What It Catches

| Category | Signal | Severity |
|---|---|---|
| Secrets | `password = "hunter2"` | Critical |
| SQL injection | `f"SELECT * FROM users WHERE id = {user_id}"` | Critical |
| XSS | `innerHTML = userInput` | High |
| Missing auth | New route without middleware | High |
| Path traversal | `open(f"/data/{filename}")` | High |
| Verbose errors | `except Exception as e: return str(e)` | Medium |

## Customization

- **Scope:** Exclude test files or vendor directories from review
- **Sensitivity:** Adjust severity thresholds for your risk tolerance
- **Integration:** Pair with `pre-commit` hooks for local pre-push checks

## Related

- [Dependency Audit](dependency-audit.md) for supply chain security
- [Rotating Health Scan](rotating-health-scan.md) for full codebase security sweeps
