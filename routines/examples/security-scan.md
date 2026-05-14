# Security Scan

> `loop.md` template — nightly dependency and code security audit.

## Usage

Use as a Desktop scheduled task at midnight, or a Cloud routine on a daily schedule.

## Template

```markdown
Run a security audit on this repository.

1. Check dependencies for known vulnerabilities using the project's
   package manager (npm audit, pip audit, cargo audit, etc.)

2. Scan files changed in the past 24 hours for hardcoded secrets:
   - API keys, tokens, passwords in source files
   - .env files accidentally committed
   - Private keys or certificates

3. Review recent changes for common vulnerability patterns:
   - SQL injection (string concatenation in queries)
   - XSS (unescaped user input in templates)
   - Command injection (unsanitized input in shell commands)
   - Path traversal (user input in file paths)

4. Check for overly permissive file permissions on sensitive files
   (config files, key files, credential stores)

Report format:
- CRITICAL: [count] — list each with file:line and description
- WARNING: [count] — list each with file:line and description
- INFO: [count] — summary only

If no issues: "Security scan clean — no issues detected."

For CRITICAL findings, create a GitHub issue with the label
"security" and assign based on CODEOWNERS.

Never auto-fix security issues. Never commit changes. Report only.
```

## When to use

- Nightly security baseline for active repositories
- Pre-release security gate (run before cutting a release branch)
- Compliance workflows requiring regular security audits
