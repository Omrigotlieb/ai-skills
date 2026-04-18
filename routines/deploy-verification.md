# Deploy Verification

**Trigger:** API | **Frequency:** Per deploy | **Category:** Operations

Runs smoke checks against a new production build, scans error logs for regressions, and posts a go/no-go verdict to the release channel before the deploy window closes.

## Setup

```bash
claude /schedule create \
  --name "deploy-verification" \
  --trigger "api" \
  --prompt "$(cat <<'EOF'
You are running post-deploy verification.

## Context
A new version has been deployed to production. Your job is to verify the deploy is healthy before the deploy window closes.

## Task
1. Smoke Tests:
   - Hit the health check endpoint and verify 200 response
   - Run the critical path smoke test suite (if configured)
   - Verify the deployed version matches the expected commit SHA

2. Error Log Scan:
   - Check error monitoring (Sentry, CloudWatch, Datadog) for new error patterns
   - Compare error rates to the pre-deploy baseline (last 1 hour vs previous 1 hour)
   - Flag any new error types that did not exist before the deploy

3. Performance Check:
   - Compare p50/p95/p99 latency to pre-deploy baseline
   - Check for memory or CPU anomalies
   - Verify no increase in timeout rates

4. Verdict:
   - GREEN: All checks pass, error rates stable or improved
   - YELLOW: Minor anomalies detected, monitor closely
   - RED: New errors, latency regression, or smoke test failure

## Output
Post to the release channel:

### Deploy Verification - <version> - <verdict>
- **Health check:** [pass/fail]
- **Smoke tests:** [X/Y passed]
- **Error rate:** [delta vs baseline]
- **Latency p95:** [value] ([delta vs baseline])
- **Recommendation:** [proceed / monitor / rollback]

## Constraints
- Complete verification within 10 minutes of being triggered.
- If monitoring tools are unavailable, report what you could not check and recommend manual verification.
- Never trigger a rollback automatically. Only recommend it.
EOF
)"
```

## Triggering from CI/CD

Call the routine from your deployment pipeline:

```yaml
# GitHub Actions example
- name: Trigger deploy verification
  run: |
    curl -X POST "$CLAUDE_API_ENDPOINT/triggers/deploy-verification" \
      -H "Authorization: Bearer $CLAUDE_API_KEY" \
      -d '{"version": "${{ github.sha }}", "environment": "production"}'
```

## Customization

- **Endpoints:** Configure the health check and smoke test URLs for your service
- **Monitoring:** Swap Sentry/Datadog for your monitoring stack
- **Thresholds:** Adjust error rate and latency thresholds for your SLOs
- **Environments:** Run for staging deploys as well as production

## Related

- [PR Branch Monitor](pr-branch-monitor.md) for pre-merge CI monitoring
- [Morning Briefing](morning-briefing.md) for daily operational summaries
