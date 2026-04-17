# Dependency & Security Audit Routine

## Overview

Proactively catch vulnerable and outdated dependencies before they become incidents.

## Configuration

| Setting | Value |
|---|---|
| **Trigger** | Schedule - Daily at 3:00 PM or Weekly |
| **Connectors** | GitHub |
| **Repositories** | All production repos |
| **Run time** | ~3-5 minutes |

## Prompt

```
Run a dependency health check on this repository.

1. SECURITY VULNERABILITIES:
   - Detect the package manager(s) in use (package.json, requirements.txt, Cargo.toml, go.mod, etc.)
   - Run the appropriate audit command (npm audit, pip-audit, cargo audit, govulncheck, etc.)
   - For each vulnerability found, report:
     - Package name and installed version
     - Severity: critical, high, medium, low
     - CVE identifier if available
     - Fixed version (if a patch exists)
     - Whether it's a direct or transitive dependency

2. OUTDATED DEPENDENCIES:
   - List packages more than 2 major versions behind latest
   - Note any packages with published deprecation notices
   - Flag packages with no releases in the last 12 months (potentially unmaintained)

3. LICENSE COMPLIANCE:
   - Scan for dependencies with copyleft licenses (GPL, AGPL, LGPL)
   - Flag any dependency without a license file
   - Note any license changes in recently updated packages

ACTION:
- If critical/high vulnerabilities have a simple version bump fix:
  Open a draft PR with the version bump and include the CVE details in the PR description
- If the fix requires a major version upgrade:
  Create an issue with migration notes and tag the team member who added the dependency
- If no issues found:
  Report "All dependencies healthy" and exit

Post results summary to #security or print to console.
Include a one-line risk assessment: LOW / MEDIUM / HIGH / CRITICAL.
```

## Customization

**Lockfile focus**: Add "Only report vulnerabilities in packages actually imported (not dev-only dependencies)" for production-focused scans.

**Compliance-heavy teams**: Expand the license section with your organization's approved license list.

**Monorepos**: Add "Scan each workspace/package independently and report per-package results."
