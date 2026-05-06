# Dependency & Security Audit Routine

## Overview

Weekly scan for security vulnerabilities, outdated packages, and license issues. Creates actionable fix PRs for simple version bumps and issues for complex remediation.

## Configuration

| Setting | Value |
|---|---|
| **Trigger** | Schedule - Weekly (Mondays at 9:00 AM) |
| **Connectors** | GitHub |
| **Repositories** | All team repos |
| **Run time** | ~3-5 minutes per repo |

## Prompt

```
Run a dependency health check on this repository.

1. Security vulnerabilities:
   - Run the package manager's audit command (npm audit, pip-audit, cargo audit, etc.)
   - Flag any critical or high severity issues
   - Include CVE ID, affected package, current version, and fixed version for each

2. Outdated dependencies:
   - List packages more than 2 major versions behind
   - Note any dependencies with deprecation warnings
   - Check if the latest version has breaking changes documented

3. License compliance:
   - Flag any new dependencies added in the last 7 days with copyleft licenses (GPL, AGPL)
   - Note any dependencies without a license file

4. Remediation:
   - For critical vulnerabilities with a simple version bump fix: open a draft PR
   - For complex fixes or breaking changes: create an issue with remediation steps
   - Group related fixes into a single PR where possible

Post results summary to #security or print to console:
- Critical/high vulnerability count
- Packages needing major updates
- License concerns
- PRs or issues created

If no issues found, post "Dependencies healthy. No action needed." and exit.
```

## Customization

**For stricter compliance**: Add SBOM (Software Bill of Materials) generation as a final step.

**For monorepos**: Run the audit per package/workspace and group results by service.

**Adjusting frequency**: High-security environments should run daily; low-risk projects can run monthly.
