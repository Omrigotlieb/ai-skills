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

After creating the routine at [claude.ai/code/routines](https://claude.ai/code/routines), add an API trigger and copy the endpoint URL and bearer token. Then call it from your pipeline:

```bash
# Replace URL and token with values from your routine's API trigger configuration
curl -X POST "$ROUTINE_ENDPOINT_URL" \
  -H "Authorization: Bearer $ROUTINE_TOKEN" \
  -H "Content-Type: application/json" \
  -d "{\"text\": \"Deploy completed. Service: $SERVICE_NAME, Version: $VERSION, Commit: $COMMIT_SHA\"}"
```

See the [official API trigger docs](https://code.claude.com/docs/en/routines#add-an-api-trigger) for the current endpoint format and required headers.

## Customization

**Canary deploys**: Add "Compare metrics between canary and stable instances. If canary error rate is >2x stable, flag as RED."

**Multi-service**: Add "Check dependent services are still functioning after this deploy."
