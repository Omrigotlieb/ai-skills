# Deploy Watch

> `loop.md` template — watches a deployment and reports status changes.

## Usage

Run `/loop 2m` when a deployment starts. Press `Esc` when done.

## Template

```markdown
Watch the current deployment. Check:

1. **Build status**: Is the build step complete? If it failed, pull the
   build log and identify the error.

2. **Test results**: Did post-build tests pass? Report any failures
   with the test name and error message.

3. **Rollout progress**: What percentage of instances have the new version?
   Report the current rollout percentage.

4. **Error rates**: Check error monitoring for spikes since the deploy
   started. Compare current error rate to the pre-deploy baseline.

5. **Response times**: Check if p50/p95/p99 latencies have regressed
   compared to the 1-hour pre-deploy window.

Report one line per check:
- BUILD: pass/fail
- TESTS: pass/fail (N failures)
- ROLLOUT: N%
- ERRORS: normal/elevated (rate)
- LATENCY: normal/elevated (p99)

If all checks pass at 100% rollout: "Deploy complete — all clear."
If any check fails: flag it prominently and describe the issue.

Never trigger rollbacks. Report status only.
```

## When to use

- Production deployments needing real-time status
- Canary deploys where error rates need continuous monitoring
- After-hours deployments where you want a status record
