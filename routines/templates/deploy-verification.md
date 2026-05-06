# Deploy Verification Routine

## Overview

Automated post-deployment health check triggered by your CD pipeline. Runs smoke tests, checks error rates, and posts a go/no-go verdict before the deploy window closes.

## Configuration

| Setting | Value |
|---|---|
| **Trigger** | API (called from CD pipeline via HTTP POST) |
| **Connectors** | GitHub, Slack |
| **Run time** | ~3-5 minutes |

## Prompt

```
A production deployment just completed. Verify it succeeded.

The deployment context is provided in the API trigger payload.

1. Health checks:
   - Verify the application responds on its health endpoint
   - Check that the version endpoint reports the expected version
   - Verify database connectivity and migration status

2. Error monitoring:
   - Check error logs for the last 15 minutes for new error patterns
   - Compare error rate to the 1-hour pre-deploy baseline
   - Flag any new exception types not seen before the deploy

3. Smoke tests:
   - Run the critical path smoke test suite
   - Verify key API endpoints return expected status codes
   - Check response times against baseline (flag >50% increase)

4. Rollback assessment:
   - If errors detected, identify the likely causing commit
   - Check if the issue is isolated or widespread

Post results to #deploys with severity:
- GREEN: "Deploy verified. No regressions detected. Version: [version]"
- YELLOW: "Deploy warning: [specific concern]. Monitoring for 30 minutes."
- RED: "Deploy issue detected: [details]. Recommend rollback. Likely cause: [commit]"

If RED, also post to #oncall with failure details and the rollback command.
Never roll back automatically. Always recommend and wait for human action.
```

## API Trigger Setup

Call the routine from your CD pipeline:

```bash
curl -X POST https://api.anthropic.com/v1/claude_code/routines/{trigger_id}/fire \
  -H "Authorization: Bearer $ROUTINE_TOKEN" \
  -H "anthropic-beta: experimental-cc-routine-2026-04-01" \
  -H "anthropic-version: 2023-06-01" \
  -H "Content-Type: application/json" \
  -d '{"text": "Deployed version 2.4.1 to production at 14:32 UTC. Commit: abc123"}'
```

## Customization

**For canary deployments**: Add a comparison between canary and stable instances.

**For multi-region**: Check each region independently and report per-region status.
