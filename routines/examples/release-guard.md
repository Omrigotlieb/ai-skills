# Release Guard

> `loop.md` template — monitors a release branch through the deploy pipeline.

## Usage

Copy to `.claude/loop.md` and run `/loop 15m`.

## Template

```markdown
Monitor the release branch and deployment pipeline.

1. **Pre-deploy**: Check if the release PR is approved and CI is green.
   If CI is red, diagnose and push a fix. Report blocker status.

2. **During deploy**: If a deployment is in progress, check the deployment
   status. Report any errors from the deployment logs.

3. **Post-deploy**: If a deployment completed, check error monitoring
   for new error patterns in the past 15 minutes. Compare error rates
   and API response times against the pre-deploy baseline.

Report format:
- BLOCKED: [reason] — deployment cannot proceed
- DEPLOYING: [stage] — deployment in progress
- DEPLOYED: [status] — GREEN/YELLOW/RED with details
- IDLE: no deployment activity

Never rollback, cancel, or trigger deployments. Report status only.
```

## When to use

- Release day monitoring without manual babysitting
- Overnight deployments where you want a status trail
- Multi-stage deploy pipelines needing continuous oversight
