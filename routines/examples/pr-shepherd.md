# PR Shepherd

> `loop.md` template — keeps a pull request healthy through its lifecycle.

## Usage

Copy to `.claude/loop.md` and run `/loop` or `/loop 10m`.

## Template

```markdown
Check the open PR on this branch. Work through these checks in order:

1. **CI status**: If any jobs failed, pull the log, diagnose the failure,
   and push a minimal fix. If it's a known flaky test, re-run the job.

2. **Review comments**: If new review comments arrived, address each one.
   Push a fix commit for code changes. Resolve the conversation thread
   after addressing it. If a comment requires discussion, reply with
   your reasoning instead of changing the code.

3. **Merge conflicts**: If the PR has conflicts with the base branch,
   rebase onto the latest base and force-push.

4. **Checks complete**: If CI is green, no unresolved comments remain,
   and the PR is approved, say "PR is ready to merge" in one line.

5. **Nothing to do**: If everything is green and quiet, say
   "PR healthy — no action needed" in one line.

Never merge the PR. Never close it. Only push fixes and reply to comments.
```

## When to use

- Active PR development where you want continuous CI triage
- Waiting for reviewer feedback and want responses addressed quickly
- Release branches that need constant health monitoring
