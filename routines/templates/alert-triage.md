# Alert Triage Routine

## Overview

When monitoring tools fire alerts, this routine correlates them with recent code changes and provides actionable triage to reduce mean time to resolution.

## Configuration

| Setting | Value |
|---|---|
| **Trigger** | API (called from monitoring/alerting systems) |
| **Connectors** | GitHub, Slack |
| **Repositories** | Service repos for alerting services |
| **Run time** | ~3-5 minutes |

## Prompt

```
An alert has fired. The alert payload is included in the trigger text.

1. PARSE ALERT:
   - Identify: service name, error type, affected endpoint/component, severity
   - Extract: stack trace, error message, request context if available
   - Note: when the alert started firing and current frequency

2. CORRELATE WITH CODE CHANGES:
   - Search commits from the last 48 hours in the affected service's repository
   - Focus on changes to: the affected endpoint, shared libraries, configuration, dependencies
   - For each potentially related commit, assess likelihood of causing the issue (high/medium/low)

3. IF A RECENT COMMIT LIKELY CAUSED IT:
   - Identify the specific change and explain why it likely caused the error
   - If it's a simple fix (config error, missing null check, typo):
     Draft a fix PR and link it in the triage summary
   - If it's complex:
     Create an issue with the diagnosis and assign to the commit author
   - Post to #oncall:
     "Alert [name] likely caused by [commit hash] by @[author].
     Change: [one-line description]
     Proposed fix: [PR link or issue link]
     Severity: [assessment]"

4. IF NO RECENT COMMIT CORRELATES:
   - Check if this is a known recurring alert pattern (search closed issues)
   - Check if it could be infrastructure-related (deployment timing, resource limits)
   - Post to #oncall:
     "Alert [name] - no recent code change found.
     Possible cause: [infrastructure / external dependency / intermittent issue]
     Recommended next steps: [specific actions]"

RESTRICTIONS:
- Never merge fix PRs automatically
- Always create fixes as draft PRs for human review
- Never dismiss or silence alerts
- If the alert payload is unclear or malformed, post to #oncall asking for manual investigation
```

## Integration

```bash
# From Datadog webhook
curl -X POST https://api.anthropic.com/v1/claude_code/routines/trig_XXXXX/fire \
  -H "Authorization: Bearer $TOKEN" \
  -H "anthropic-beta: experimental-cc-routine-2026-04-01" \
  -H "anthropic-version: 2023-06-01" \
  -H "Content-Type: application/json" \
  -d "{\"text\": \"$ALERT_BODY\"}"
```

## Customization

**Runbook integration**: Add "Check the service's runbook at docs/runbooks/ for known remediation steps."

**Escalation**: Add "If severity is critical and the alert has been firing for >30 minutes, also post to #incident-response."
