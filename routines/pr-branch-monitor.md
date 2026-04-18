# PR Branch Monitor

**Trigger:** Loop | **Frequency:** Dynamic (checks frequently during CI, backs off when idle) | **Category:** CI/CD

Continuously monitors the current PR: fixes failing CI, addresses review comments, and reports status. Uses Claude Code's built-in dynamic pacing to check frequently when active and wait longer when idle.

## Setup

Create a `loop.md` file in your project root:

```markdown
# loop.md

Check the status of the current branch's open PR and take action:

1. **CI Status:**
   - If any CI job is failing, pull the job log, diagnose the failure, and push a fix
   - If CI is pending, report and wait

2. **Review Comments:**
   - If there are new unresolved review comments, address each one
   - For code change requests: implement the change, commit, and push
   - For questions: reply with an explanation
   - For suggestions you disagree with: reply explaining your reasoning

3. **Merge Conflicts:**
   - If the branch has merge conflicts with the base branch, resolve them

4. **Status Report:**
   - If everything is green and no pending comments, report in one line
   - If you made changes, summarize what you did

Do not start new features or refactoring. Only tend to the existing PR.
```

Then start the loop:

```bash
# Dynamic pacing (recommended) - Claude decides when to check
claude /loop

# Fixed interval - check every 5 minutes
claude /loop 5m
```

## How Dynamic Pacing Works

Claude adjusts the check interval based on what it finds:

| State | Interval | Reason |
|---|---|---|
| CI running | 60-120s | Check back when build finishes |
| CI just failed | Immediate | Diagnose and fix now |
| Waiting for review | 600-1200s | No point checking every minute |
| Review comments arrived | Immediate | Address while reviewer is active |
| Everything green | 1200-1800s | Idle maintenance mode |

## Customization

- **Scope:** Monitor a specific PR by adding the PR number to the prompt
- **Actions:** Remove the "push a fix" step if you want review-only monitoring
- **Notifications:** Add Slack notifications when CI goes red or green
- **Multiple PRs:** Run separate loops for different PRs in different terminals

## Related

- [Morning Briefing](morning-briefing.md) for daily PR status summaries
- [Weekly Quality Dashboard](weekly-quality-dashboard.md) for longer-term trends
