# PR Monitor Routine

**Schedule:** Every 15–30 min during work hours · **Trigger:** `/loop` or cron · **Requires:** GitHub CLI (`gh`)

## What It Does

Watches your open PRs through the full lifecycle — from push to merge. Monitors CI status, triages review feedback, implements fixes for actionable comments, and escalates blocking issues.

## Setup

### Using Loop Mode (Recommended)

```bash
# Monitor a specific PR
claude /loop 15m "Monitor PR #123: check CI status, review comments, fix actionable feedback, and report status"

# Monitor all your open PRs
claude /loop 30m "Check all my open PRs: CI status, review comments, merge readiness. Fix what you can, escalate what you can't."
```

### As a Scheduled Task

```bash
claude schedule create \
  --name "pr-monitor" \
  --cron "*/30 9-18 * * 1-5" \
  --prompt "$(cat <<'EOF'
Monitor my open pull requests.

## Steps
1. Run `gh pr list --author @me` to get all my open PRs
2. For each PR:
   a. Check CI status with `gh pr checks`
   b. Fetch review comments with `gh pr view --comments`
   c. Categorize each comment as:
      - **Fix**: Clear, actionable code change needed
      - **Discuss**: Needs human judgment or context
      - **Resolved**: Already addressed or acknowledged

3. For Fix items:
   - Implement the change
   - Run relevant tests
   - Commit and push
   - Reply to the review comment explaining the fix

4. For Discuss items:
   - Summarize the discussion point
   - Flag for my attention

5. Output a status report with:
   - PR number, title, CI status (pass/fail/pending)
   - Actions taken (fixes pushed)
   - Items needing my attention
   - Estimated merge readiness (ready / blocked / needs review)
EOF
)"
```

### As a Custom Command

Create `.claude/commands/pr-status.md`:

```markdown
Check the status of my open pull requests.

For each PR:
1. CI status (pass/fail/pending)
2. Review status (approved/changes requested/pending)
3. Unresolved review comments
4. Merge conflicts

Categorize each PR as: Ready to merge / Needs fixes / Needs review / Blocked

For any PR with actionable review feedback, implement the fixes if they're straightforward.
```

## Example Output

```markdown
# PR Status — 2026-04-24 14:30

### PR #847: Auth migration to JWT
- **CI:** ✅ All checks passing
- **Reviews:** 1 approved, 1 changes-requested
- **Actions taken:** Fixed import ordering (reviewer comment), pushed commit `a3f2b1c`
- **Status:** Needs re-review from @alex after pushed fix
- **Merge readiness:** Needs review

### PR #851: Add rate limiting to /api/auth
- **CI:** ❌ Failing — test_rate_limit_window flaky
- **Reviews:** Pending (requested from @sarah, @mike)
- **Actions taken:** None — CI failure is a known flaky test, not related to this PR
- **Status:** Needs review + CI fix
- **Merge readiness:** Blocked (flaky test)

### 📋 Needs Your Attention
1. PR #847: @alex asked "Should we add a migration rollback script?" → Discuss
2. PR #851: Flaky test `test_rate_limit_window` blocking CI — consider skipping or fixing
```

## Loop Behavior

When running in `/loop` mode, the monitor follows an escalation pattern:

| Iteration | Focus |
|-----------|-------|
| 1 | Full status scan, identify all issues |
| 2 | Fix actionable review comments, re-check CI |
| 3 | Verify fixes landed, check for new comments |
| 4+ | Light monitoring — only report changes |

**Max iterations per PR:** 3 fix cycles before escalating to you. This prevents infinite fix loops on subjective feedback.

## Customization

**Adjust monitoring frequency:**
- Active deploy: 5–10 min
- Waiting for review: 30 min
- Low priority: 1 hour

**Add notification destinations:**
- Slack: Post status to a channel when PRs become mergeable
- Desktop: Use push notifications for CI failures

**Filter by priority:**
```bash
# Only monitor PRs with specific labels
claude /loop 15m "Monitor PRs labeled 'urgent' or 'release-blocker': ..."
```

## Tips

- **Start with one PR** before monitoring all open PRs — build confidence in the fix quality
- **Set a fix budget**: Tell the agent "only push fixes for style/formatting issues, escalate logic changes"
- **Combine with Nightly Maintenance**: The nightly routine can handle stale PRs and branch cleanup
