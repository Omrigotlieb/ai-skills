# Weekly Security Scan Routine

Automated security scanning that checks for dependency vulnerabilities, exposed secrets, and common security anti-patterns in code and configuration.

---

## Overview

| Property | Value |
|----------|-------|
| **Schedule** | `0 6 * * 1` (Monday at 6 AM) or daily for high-security projects |
| **Duration** | 2-5 minutes depending on repo size |
| **Sources** | Package manager audit, git history, source code, Dockerfiles |

## Setup

### Basic: Dependency + Secrets Scan

```bash
claude schedule create \
  --name "security-scan" \
  --cron "0 6 * * 1" \
  --prompt "$(cat <<'EOF'
Run a weekly security scan on this repository.

## Checks

### 1. Dependency Vulnerabilities
- Run the package manager's audit command (npm audit / pip audit / cargo audit)
- For each vulnerability with severity HIGH or CRITICAL:
  - Package name, current version, fixed version
  - CVE ID and brief description
  - Whether it is a direct or transitive dependency
  - Suggested remediation command

### 2. Secrets Detection
- Scan committed files for patterns matching:
  - API keys (AWS, GCP, Azure, Stripe, Twilio, SendGrid)
  - Database connection strings with embedded passwords
  - JWT secrets and private keys
  - OAuth tokens and refresh tokens
  - .env files that should be gitignored
- Check git history for secrets that were committed then removed

### 3. Configuration Security
- Dockerfiles: running as root, using :latest tags, exposing unnecessary ports
- CI config: secrets not using GitHub/CI secret storage
- CORS: overly permissive origins (wildcard *)
- Debug mode enabled in production config files

### 4. Code Patterns
- SQL queries built via string concatenation (injection risk)
- User input rendered without sanitization (XSS risk)
- exec/eval calls with external input (command injection risk)
- Hardcoded credentials in source files
- Missing authentication checks on API endpoints

## Output

### Security Report -- [date]

**Risk Level: [LOW / MEDIUM / HIGH / CRITICAL]**

#### Critical (fix immediately)
- [finding with file:line, impact, and fix command]

#### High (fix this week)
- [finding with context and remediation]

#### Medium (fix soon)
- [finding with context]

#### Informational
- [trends, new dependencies added, configuration notes]

## Rules
- If a critical vulnerability has a fix available, include the exact command to fix it
- For secrets found in history, recommend using git-filter-repo or BFG to clean history
- Do not report findings on test fixtures or example files clearly marked as non-production
- Check if a GitHub issue already exists before recommending one be created
EOF
)"
```

### Daily Security Watch (High-Security Projects)

For projects handling sensitive data, run a lighter daily scan:

```bash
claude schedule create \
  --name "daily-security-watch" \
  --cron "0 6 * * 1-5" \
  --prompt "$(cat <<'EOF'
Quick daily security check. ONLY report if something needs human attention.

1. Run npm audit --audit-level=high (or equivalent)
2. Scan git diff from the last 24 hours for accidentally committed secrets
3. Check if any new dependencies were added -- flag if they have known vulnerabilities

If everything is clean, produce no output.
If issues found, list them with severity and remediation.
EOF
)"
```

### Loop-Based Secrets Scanner

For active development sessions, scan for secrets continuously:

```
/loop 1h scan the git diff from the last hour to check if any API keys,
passwords, tokens, or other sensitive information were accidentally committed.
Alert me immediately if found.
```

## Integration with GitHub Actions

For automated PR-level security review, Anthropic provides an official GitHub Action:

```yaml
# .github/workflows/security-review.yml
name: Security Review
on:
  pull_request:
    types: [opened, synchronize]

# Use the official Anthropic action:
# github.com/anthropics/claude-code-security-review
```

*Source: [anthropics/claude-code-security-review](https://github.com/anthropics/claude-code-security-review)*

## Customization

### Language-Specific Checks

Add checks relevant to your stack:

```markdown
## Additional Checks (Python)
- Scan for pickle.loads with untrusted input (deserialization attack)
- Check for subprocess calls with shell=True and user input
- Verify that Django DEBUG is False in production settings
- Check for missing CSRF protection on form endpoints

## Additional Checks (Node.js)
- Scan for eval() or Function() with user input
- Check for prototype pollution in object merging
- Verify helmet middleware is configured on Express apps
- Check for missing rate limiting on authentication endpoints
```

### Auto-Create Issues

```markdown
For each Critical or High finding:
1. Check if a GitHub issue already exists with a matching title
2. If not, create one with:
   - Title: "[Security] [brief description]"
   - Labels: "security", "priority:high"
   - Body: finding details, affected files, and remediation steps
   - Assign to the most recent committer of the affected file
```

## Example Output

```
### Security Report -- 2026-05-05

**Risk Level: HIGH**

#### Critical (fix immediately)
(none)

#### High (fix this week)
- `express` 4.18.2 has CVE-2026-1234 (path traversal, CVSS 7.5)
  Fix: `npm install express@5.0.1`
  Breaking change: `req.host` no longer includes port
- `src/api/users.ts:45` -- SQL query uses string interpolation with user input
  Use parameterized query: `db.query('SELECT * FROM users WHERE id = $1', [userId])`

#### Medium (fix soon)
- `Dockerfile:1` -- Running as root. Add: `USER node` after install steps
- `.github/workflows/deploy.yml:23` -- API key passed as plain text argument
  Move to GitHub Secrets: `${{ secrets.DEPLOY_API_KEY }}`

#### Informational
- 2 new dependencies added this week: `zod@3.23.0` (clean), `marked@14.0.0` (clean)
- No secrets detected in git diff for the past 7 days
```
