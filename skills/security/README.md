# Security Skills for Claude Code

Skills and tools for DevSecOps, vulnerability detection, and secure coding.

> **Note:** AI security review should complement, not replace, human reviews and security tooling.

---

## Security Review Skill

Claude Code includes built-in security review capabilities:

```bash
# Review current changes for security issues
Review my code changes for security vulnerabilities:
- SQL injection
- XSS vulnerabilities
- IDOR bugs
- Authentication issues
- Input validation
```

### Effectiveness (2025 Testing)
| Vulnerability Type | True Positive Rate |
|--------------------|-------------------|
| IDOR (Insecure Direct Object Reference) | 22% |
| XSS (Cross-Site Scripting) | 16% |
| SQL Injection | 5% |
| General vulnerabilities | 14% |

**Best at:** IDOR detection
**Struggles with:** Taint tracking across multiple files

---

## GitHub Action for Security Reviews

Anthropic's official GitHub Action for automated PR security reviews:

```yaml
# .github/workflows/security-review.yml
name: Claude Security Review
on:
  pull_request:
    types: [opened, synchronize]

jobs:
  security-review:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: anthropics/claude-code-action@v1
        with:
          api-key: ${{ secrets.ANTHROPIC_API_KEY }}
          command: security-review
          # Posts inline comments with fixes
```

**Features:**
- Scans code changes for vulnerabilities
- Customizable rules to reduce false positives
- Inline comments with recommended fixes
- Standardizes security reviews across teams

---

## Security-Focused MCP Servers

| Server | Purpose | Link |
|--------|---------|------|
| **Semgrep MCP** | Static analysis, custom rules | [semgrep.dev](https://semgrep.dev) |
| **Snyk MCP** | Dependency vulnerability scanning | Community |
| **Trivy MCP** | Container and IaC scanning | Community |

---

## Security Skills from Community

### Secure Code Review Skill
```markdown
---
name: secure-code-review
description: Review code for OWASP Top 10 vulnerabilities
---

# Secure Code Review

## When to Use
- Before code review
- Before merging PRs
- When auditing existing code

## Checklist
- [ ] SQL Injection (parameterized queries)
- [ ] XSS (output encoding)
- [ ] CSRF (token validation)
- [ ] Authentication/Authorization
- [ ] Sensitive data exposure
- [ ] Security misconfiguration
- [ ] Input validation
- [ ] Error handling (no stack traces)
```

### Dependency Audit Skill
```markdown
---
name: dependency-audit
description: Check dependencies for known vulnerabilities
---

# Dependency Audit

Run:
- npm audit (Node.js)
- pip-audit (Python)
- cargo audit (Rust)
- go mod verify (Go)

Report:
- Critical vulnerabilities
- Outdated packages
- Recommended updates
```

---

## Security Best Practices

### Least Privilege
- Minimize tool permissions in skills
- Use explicit action gates for high-impact actions
- Require confirmations for dangerous operations

### Hook-Based Security
```json
{
  "hooks": {
    "PreToolUse": [{
      "matcher": "Bash",
      "command": "./hooks/block-dangerous.sh"
    }]
  }
}
```

Block patterns:
- `rm -rf /`
- `sudo`
- `curl | sh`
- `> /dev/sda`

### Audit Approved Commands
```bash
npx cc-safe scan
```

Scans `.claude/settings.json` for dangerous patterns.

---

## Known Security Considerations

### Prompt Injection
Adversaries may manipulate instructions to make skills perform unintended actions.

**Mitigation:**
- Defense in depth
- Minimize tool power
- Require confirmations

### Code Execution Risks
Claude Code may execute generated test cases, which could be risky with malicious third-party libraries.

**Mitigation:**
- Container isolation for testing
- Review before execution
- Limit file system access

---

## Resources

- [Claude Security Best Practices](https://www.anthropic.com/security)
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [Semgrep Rules](https://semgrep.dev/explore)
- [DevSecOps with Claude](https://mostafahussein.medium.com/ai-powered-code-security-reviews-for-devsecops-with-claude-12baeacf196f)
