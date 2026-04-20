# Automation Skills for Claude Code

Skills for scheduled tasks, routine maintenance, PR management, and autonomous agent workflows.

> **Related:** For scheduling configuration and daily routine structure, see [Routines](../../routines/README.md). For bare agent prompt templates, see [Agent Prompts](../../prompts/agent-prompts.md). This page contains installable skill definitions with full SKILL.md format.

---

## PR Babysitter Skill

Monitor and maintain pull requests through CI and code review:

```markdown
---
name: pr-babysitter
description: Watch a PR through CI, review feedback, and merge readiness
---

# PR Babysitter

## When to Use
- After opening a PR that needs CI monitoring
- When review comments arrive on your PR
- During active development with frequent pushes

## Instructions
1. Check PR status with `gh pr view`
2. Check CI with `gh pr checks`
3. If CI fails, fetch logs with `gh run view <id> --log-failed`
4. Diagnose and push minimal fixes
5. Read and triage review comments:
   - Fix: clear improvements, apply and push
   - Dismiss: disagree with stated reason
   - Escalate: needs human judgment
6. Stop after 3 fix iterations or when PR is green and approved

## Guidelines
- Never merge without human approval
- Keep fixes minimal and focused on the CI failure
- Do not refactor unrelated code while fixing CI
- Report status clearly between iterations
```

---

## Issue Triage Skill

Classify and organize incoming issues:

```markdown
---
name: issue-triage
description: Classify new issues by type, severity, and affected area
---

# Issue Triage

## When to Use
- Daily morning triage of overnight issues
- When a batch of issues needs classification
- Before sprint planning

## Instructions
1. List open issues with `gh issue list --state open --limit 20`
2. For each issue, analyze:
   - Type: bug, feature request, question, docs
   - Severity: critical (crash/data loss), high (broken feature), medium (degraded), low (cosmetic)
   - Affected area: match file paths or module names mentioned
3. Suggest labels based on analysis
4. Flag duplicates by comparing with recent closed issues
5. Output a summary grouped by severity

## Guidelines
- Never modify issues directly unless explicitly asked
- Flag security-related issues separately with urgency
- Mark stale issues (no activity for 30+ days) for review
```

---

## Dependency Auditor Skill

Multi-language dependency scanning and upgrade planning:

```markdown
---
name: dependency-auditor
description: Scan dependencies for vulnerabilities and plan safe upgrades
---

# Dependency Auditor

## When to Use
- Weekly security audit runs
- Before releases or deployments
- When adding new dependencies

## Instructions
1. Detect project language and package manager
2. Run the appropriate audit command:
   - Node.js: `npm audit --json` or `yarn audit --json`
   - Python: `pip audit --format json`
   - Go: `govulncheck ./...`
   - Rust: `cargo audit --json`
3. Parse results and classify:
   - Critical/High with fix available: create upgrade PR
   - Critical/High without fix: report and suggest alternatives
   - Moderate/Low: include in report only
4. For upgrades, run tests before creating PR
5. Check license compatibility of new dependencies

## Guidelines
- Never upgrade major versions without human approval
- Group related upgrades into a single PR
- Include CVE numbers and descriptions in reports
- Check if vulnerable code paths are actually reachable
```

---

## Release Manager Skill

Automate release preparation and changelog generation:

```markdown
---
name: release-manager
description: Prepare releases with changelog, version bumps, and tag management
---

# Release Manager

## When to Use
- Preparing a new release
- Generating changelogs from merged PRs
- Managing version numbers

## Instructions
1. List merged PRs since last release tag:
   `gh pr list --state merged --search "merged:>LAST_RELEASE_DATE"`
2. Categorize changes using conventional commit prefixes or PR labels:
   - feat: → Added
   - fix: → Fixed
   - docs: → Documentation
   - perf: → Performance
   - breaking: → Breaking Changes
3. Generate changelog entry in Keep a Changelog format
4. Suggest version bump (major/minor/patch) based on changes
5. Create release PR with changelog and version updates

## Guidelines
- Breaking changes always trigger a major version bump
- Never create tags or releases without human approval
- Include migration notes for breaking changes
- Link each changelog entry to its PR
```

---

## CI/CD Pipeline Builder Skill

Create and optimize CI/CD configurations:

```markdown
---
name: ci-pipeline-builder
description: Generate and optimize CI/CD pipelines for common platforms
---

# CI/CD Pipeline Builder

## When to Use
- Setting up CI/CD for a new project
- Optimizing slow pipelines
- Adding new CI steps (linting, testing, deployment)

## Instructions
1. Detect project stack (language, framework, package manager)
2. Choose appropriate CI platform configuration:
   - GitHub Actions: `.github/workflows/`
   - GitLab CI: `.gitlab-ci.yml`
3. Generate pipeline with:
   - Dependency caching for fast installs
   - Parallel test execution where possible
   - Lint/format checks
   - Test suite with coverage reporting
   - Build step with artifact upload
   - Deploy step (if deployment target is specified)
4. Optimize for speed:
   - Cache node_modules, pip cache, Go modules
   - Use matrix builds for multi-version testing
   - Skip unnecessary steps on draft PRs

## Guidelines
- Always include a lint step before tests
- Use specific action versions, not @latest
- Never store secrets in workflow files
- Add concurrency groups to cancel superseded runs
```

---

## Open Source Maintainer Skill

Daily maintenance for open source projects:

```markdown
---
name: oss-maintainer
description: Daily maintenance tasks for open source project health
---

# Open Source Maintainer

## When to Use
- Daily automated maintenance of open source projects
- Weekly project health checks
- Before community calls or updates

## Instructions
1. Scan issues opened in the last 24 hours:
   - Classify by type and severity
   - Check for duplicates against recent issues
   - Flag issues that need maintainer attention
2. Scan PRs opened in the last 24 hours:
   - Check if they follow contribution guidelines
   - Run CI and report status
   - Flag PRs that are ready for review
3. Check dependency health:
   - Run security audit
   - Check for outdated dependencies
4. Generate daily summary:
   - New issues (count and categories)
   - New PRs (count and status)
   - Dependency alerts (if any)
   - Action items for maintainers

## Governance Rules
- Create PRs but never merge them
- Read issues but never respond to them
- Report findings; let humans communicate
- Stay silent if nothing actionable is found

## Guidelines
- Focus on actionable items only
- Group related issues when reporting
- Prioritize security-related items
- Include links to relevant issues/PRs in summaries
```

---

## Deploy Verifier Skill

Post-deployment smoke testing and verification:

```markdown
---
name: deploy-verifier
description: Verify deployments with smoke tests and error log monitoring
---

# Deploy Verifier

## When to Use
- After production deployments
- After staging deployments before promotion
- When monitoring for post-deploy regressions

## Instructions
1. Confirm deployment completed successfully
2. Run smoke tests against the deployed environment:
   - Health check endpoints
   - Core user flows (login, main features)
   - API response times baseline
3. Monitor error logs for the first 15 minutes:
   - Check for new error patterns not seen before deploy
   - Compare error rates with pre-deploy baseline
   - Flag any 5xx spike
4. Report go/no-go status:
   - Green: all smoke tests pass, error rates normal
   - Yellow: tests pass but error rate elevated
   - Red: smoke test failures or error spike

## Guidelines
- Never trigger rollback automatically
- Report anomalies with enough context for humans to decide
- Include comparison with pre-deploy metrics when available
- Check both frontend and backend health
```

---

## Tech Debt Tracker Skill

Identify, classify, and prioritize technical debt:

```markdown
---
name: tech-debt-tracker
description: Scan codebase for technical debt and prioritize remediation
---

# Tech Debt Tracker

## When to Use
- Weekly or monthly debt assessment
- Before planning sprints
- When deciding what to refactor

## Instructions
1. Scan for explicit markers:
   - TODO, FIXME, HACK, XXX, WORKAROUND comments
   - `@deprecated` annotations
   - Disabled tests (skip, xfail, pending)
2. Analyze code health signals:
   - Files with highest churn: `git log --since="30 days ago" --name-only`
   - Largest files by line count
   - Functions with high cyclomatic complexity (if tooling available)
3. Classify each item:
   - Severity: high (blocks features), medium (slows development), low (cosmetic)
   - Effort: small (< 1 hour), medium (1-4 hours), large (> 4 hours)
   - Risk: high (core paths), medium (important features), low (edge cases)
4. Prioritize by: severity * risk / effort (highest value first)

## Guidelines
- Focus on debt that affects active development areas
- Include age of TODO comments (git blame)
- Do not create issues or PRs; output a report for planning
- Update report incrementally, tracking progress over time
```

---

## Resources

- [Routines and Scheduled Tasks](../../routines/README.md)
- [DevOps Skills](../devops/README.md)
- [Security Skills](../security/README.md)
- [Claude Code Routines Documentation](https://code.claude.com/docs/en/routines)
