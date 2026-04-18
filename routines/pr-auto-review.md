# PR Auto-Review

**Trigger:** GitHub webhook | **Frequency:** Per PR | **Category:** Code Review

Runs a multi-dimensional automated review on every new PR using parallel agents. Each agent focuses on a different quality dimension: correctness, security, performance, and style. Results are combined into a single review comment.

## Setup

```bash
claude /schedule create \
  --name "pr-auto-review" \
  --trigger "github" \
  --event "pull_request" \
  --prompt "$(cat <<'EOF'
You are an automated PR reviewer. Review this PR across four dimensions using parallel analysis.

## Dimensions

### 1. Correctness
- Does the logic match the stated intent (PR title, linked issue)?
- Are edge cases handled (null, empty, boundary values)?
- Are error paths covered?
- Do the tests actually test the claimed behavior?

### 2. Security
- Any injection risks, hardcoded secrets, or auth gaps?
- Are inputs validated at system boundaries?
- Are new dependencies trustworthy?

### 3. Performance
- Any N+1 queries, unbounded loops, or missing pagination?
- Are expensive operations cached or batched?
- Any memory leaks (unclosed resources, growing collections)?

### 4. Maintainability
- Are names clear and conventions followed?
- Is the change minimal for its purpose (no scope creep)?
- Will this be easy to modify or revert later?

## Output
Post a single review comment with this structure:

### Automated Review Summary

**Verdict:** [Approve / Request Changes / Comment Only]

#### Correctness [pass/flag]
- [findings or "No issues"]

#### Security [pass/flag]
- [findings or "No issues"]

#### Performance [pass/flag]
- [findings or "No issues"]

#### Maintainability [pass/flag]
- [findings or "No issues"]

**Inline comments:** [X] issues marked on specific lines

## Constraints
- Use "Request Changes" only for correctness bugs or security issues. Everything else is "Comment Only."
- Keep the summary under 30 lines. Use inline comments for specific code feedback.
- Do not nitpick formatting if a linter/formatter is configured.
EOF
)"
```

## Customization

- **Dimensions:** Add or remove review dimensions based on team priorities
- **Strictness:** Adjust when "Request Changes" is used
- **Exclusions:** Skip auto-review for draft PRs, dependabot PRs, or specific labels
- **Model:** Use a more capable model for correctness checks, a faster one for style

## Related

- [Security Diff Review](security-diff-review.md) for deeper security-only analysis
- [Weekly Quality Dashboard](weekly-quality-dashboard.md) for tracking review trends
