# Dependency Audit

**Trigger:** Schedule | **Frequency:** Nightly at 2am | **Category:** Security

Scans all package manifests for outdated dependencies, known CVEs, and breaking changes. Opens GitHub issues for critical vulnerabilities so the team can act first thing in the morning.

## Setup

```bash
claude /schedule create \
  --name "dependency-audit" \
  --cron "0 2 * * *" \
  --prompt "$(cat <<'EOF'
You are running a nightly dependency audit.

## Task
1. Identify all package manifests (package.json, requirements.txt, pyproject.toml, Gemfile, go.mod, Cargo.toml)
2. For each manifest:
   - Check for packages with known CVEs using `npm audit`, `pip-audit`, `cargo audit`, or equivalent
   - Identify packages more than 2 major versions behind
   - Flag packages that have been deprecated or abandoned
3. Cross-reference findings with the National Vulnerability Database

## Output
- For CRITICAL or HIGH severity CVEs: open a GitHub issue titled `[Security] CVE-XXXX in <package>` with remediation steps
- For outdated packages (2+ major versions behind): open a single summary issue titled `[Dependencies] Outdated packages report - <date>`
- Post a one-paragraph summary to the team's notification channel
- If no issues found, log "All dependencies current, no CVEs detected" and exit

## Constraints
- Do NOT auto-upgrade packages. Only report and recommend.
- Do NOT open duplicate issues. Check for existing open issues before creating new ones.
- Include the current version, latest version, and changelog link for each flagged package.
EOF
)"
```

## What It Catches

| Signal | Example | Severity |
|---|---|---|
| Known CVE | `lodash@4.17.15` has prototype pollution | Critical/High |
| Major version lag | `react@16.x` when `19.x` is stable | Medium |
| Abandoned package | No commits in 2+ years, no maintainer | Low |
| Deprecated package | Marked deprecated on registry | Medium |

## Customization

- **Scope:** Add or remove manifest types based on your stack
- **Threshold:** Change "2 major versions" to match your team's tolerance
- **Output:** Replace GitHub issues with Slack messages or email for lighter-weight alerts
- **Frequency:** Run weekly instead of nightly for low-churn projects

## Related

- [Security skills](../skills/security/README.md) for manual security review patterns
- [Rotating Health Scan](rotating-health-scan.md) for broader code health checks
