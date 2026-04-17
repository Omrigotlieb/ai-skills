# Deploy Verification Routine

## Overview

Automated post-deploy smoke checks that verify production deployments succeeded and catch regressions before users do.

## Configuration

| Setting | Value |
|---|---|
| **Trigger** | API (called from CD pipeline after deploy completes) |
| **Connectors** | GitHub, Slack |
| **Repositories** | Deployed service's repo |
| **Run time** | ~2-5 minutes |

## Prompt

```
A production deployment just completed. The deployment context is in the trigger payload.

1. HEALTH CHECKS:
   - Verify the application health endpoint returns 200
   - Check the version/build endpoint reports the expected version
   - Confirm database connectivity and migration status
   - Verify external service dependencies are reachable

2. REGRESSION SCAN:
   - Check application error logs for the last 15 minutes
   - Compare current error rate to the 1-hour pre-deploy baseline
   - Flag any new error patterns not present before the deploy
   - Check for increased latency on critical endpoints (p50, p95, p99)

3. SMOKE TESTS:
   - Test authentication flow (login, token refresh)
   - Test core API endpoints return expected status codes
   - Verify critical user paths are functional
   - Check that background jobs/workers are processing

4. REPORT - Post to #deploys with one of:

   GREEN:
   "Deploy verified. Version [X]. No regressions detected.
   Health: OK | Errors: baseline | Latency: normal | Smoke tests: all passing"

   YELLOW:
   "Deploy warning: [specific concern]. Monitoring.
   [Details of the anomaly and what to watch]"

   RED:
   "Deploy issue detected: [details]. Consider rollback.
   [Specific failures, affected endpoints, error samples]"

If RED, also post to #oncall with failure details and the deploy commit hash.
Never trigger a rollback automatically. Only report and recommend.
```

## Integration

### Triggering from CI/CD

```bash
# After deploy step in your pipeline
curl -X POST https://api.anthropic.com/v1/claude_code/routines/trig_XXXXX/fire \
  -H "Authorization: Bearer $ROUTINE_TOKEN" \
  -H "anthropic-beta: experimental-cc-routine-2026-04-01" \
  -H "anthropic-version: 2023-06-01" \
  -H "Content-Type: application/json" \
  -d "{\"text\": \"Deploy completed. Service: $SERVICE_NAME, Version: $VERSION, Commit: $COMMIT_SHA\"}"
```

## Customization

**Canary deploys**: Add "Compare metrics between canary and stable instances. If canary error rate is >2x stable, flag as RED."

**Multi-service**: Add "Check dependent services are still functioning after this deploy."
