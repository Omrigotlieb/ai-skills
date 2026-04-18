# Nightly Bug Hunter

**Trigger:** Schedule | **Frequency:** Nightly at 2:30am | **Category:** Operations

Pulls the top-priority bug from your issue tracker, explores the codebase, implements a fix with tests, and opens a draft PR for human review. Developers arrive to a proposed solution instead of a blank slate.

## Setup

```bash
claude /schedule create \
  --name "nightly-bug-hunter" \
  --cron "30 2 * * *" \
  --prompt "$(cat <<'EOF'
You are a nightly bug-fixing agent.

## Task
1. Query the issue tracker (GitHub Issues / Linear / Jira) for the highest-priority open bug:
   - Filter: label "bug", status "open", sorted by priority then age
   - Skip issues labeled "needs-discussion" or "blocked"
   - Skip issues you have already attempted (check for a "bot-attempted" label)

2. Read the issue description and any linked context (stack traces, screenshots, related PRs)

3. Explore the codebase to understand the relevant code paths:
   - Use the error message or stack trace to locate the affected code
   - Read surrounding code to understand the intended behavior
   - Check git blame to understand recent changes to the area

4. Implement a fix:
   - Create a new branch named `fix/<issue-number>-<short-description>`
   - Make the minimal change needed to fix the bug
   - Write or update tests that reproduce the bug and verify the fix
   - Run the existing test suite to confirm no regressions

5. Open a draft PR:
   - Title: `Fix #<issue-number>: <short description>`
   - Body: explain what caused the bug, what the fix does, and link the issue
   - Mark as draft so a human reviews before merge
   - Add the "bot-attempted" label to the issue

## Constraints
- Only attempt ONE bug per night. Quality over quantity.
- If the fix requires changes to more than 5 files, skip it and add a comment explaining why it needs human attention.
- If tests fail after your fix, do NOT push. Add a comment to the issue with your analysis.
- Never force-push or modify existing branches.
- Do not close the issue. The human reviewer decides when the fix is ready.
EOF
)"
```

## What Makes This Effective

- **Overnight compute:** Uses idle hours productively
- **Draft PRs:** Human review gate prevents bad fixes from shipping
- **Single bug limit:** Prevents cascading failures from ambitious overnight changes
- **Skip mechanism:** The "bot-attempted" label prevents re-attempting failed fixes

## Customization

- **Issue source:** Swap GitHub Issues for Linear (`linear` MCP) or Jira
- **Complexity limit:** Adjust the 5-file threshold based on your codebase
- **Priority filter:** Change label filters to match your triage system
- **Frequency:** Run on weeknights only with `30 2 * * 1-5`

## Related

- [Deploy Verification](deploy-verification.md) for post-deploy smoke checks
- [PR Branch Monitor](pr-branch-monitor.md) for monitoring the draft PR after it is opened
