# Email Triage Routine

**Schedule:** Daily, 7 AM · **Duration:** 2–5 min to run, saves 20–30 min/day · **Requires:** Gmail MCP

## What It Does

Processes your inbox automatically — classifies messages, drafts replies for urgent items, labels and archives the rest. This is the single most recommended starting automation across all productivity communities.

## Setup

### Prerequisites

Set up a Gmail MCP server. See [MCP Server guides — Productivity](../mcp-servers/README.md) for current installation options and verified package names.

### As a Scheduled Task

```bash
claude schedule create \
  --name "email-triage" \
  --cron "0 7 * * *" \
  --prompt "$(cat <<'EOF'
Triage my email inbox.

## Steps
1. Fetch all unread emails from the last 24 hours
2. For each email, classify into one of these categories:
   - **Urgent**: Needs a reply today. From a real person about a time-sensitive topic.
   - **Action Required**: Needs a reply this week but not today.
   - **FYI**: Informational — team updates, notifications, status reports.
   - **Newsletter/Promo**: Marketing, subscriptions, automated digests.

3. For each Urgent email:
   - Draft a reply and save it as a Gmail draft
   - Keep the tone professional and concise
   - If you don't have enough context, draft a reply asking for clarification

4. For FYI emails:
   - Apply the "Read Later" label

5. For Newsletter/Promo emails:
   - Apply the "Newsletters" label
   - Mark as read

6. Output a summary with:
   - Count per category
   - List of Urgent items with sender, subject, and your draft summary
   - List of Action Required items with sender and subject
   - Any emails you couldn't confidently classify (flag for manual review)

Keep the summary under 300 words.
EOF
)"
```

### As a Custom Command

Create `.claude/commands/triage-email.md`:

```markdown
Triage my email inbox.

## Process
1. Fetch all unread emails from the last 24 hours
2. Classify each as: Urgent, Action Required, FYI, or Newsletter/Promo
3. Draft replies for Urgent emails (save as Gmail drafts)
4. Label FYI as "Read Later", Newsletters as "Newsletters" and mark read
5. Flag anything you can't confidently classify

## Output
Summary with counts, urgent items listed with draft summaries, and any items flagged for manual review. Under 300 words.
```

## Example Output

```markdown
# Email Triage — 2026-04-24

**Processed:** 23 emails

| Category | Count |
|----------|-------|
| Urgent | 2 |
| Action Required | 4 |
| FYI | 11 |
| Newsletter/Promo | 5 |
| Needs Review | 1 |

### 🚨 Urgent (drafts saved)
1. **Sarah Chen** — "Auth migration timeline" → Drafted: confirmed Thursday merge target, flagged the deploy freeze
2. **ops-alerts** — "Memory spike payments-service" → Drafted: acknowledged, will investigate by 10 AM

### 📋 Action Required
1. Mike R. — "Q2 planning input needed" (due Friday)
2. HR — "Benefits enrollment reminder" (due April 30)
3. Alex T. — "Design review feedback" (no deadline stated)
4. Legal — "Data retention policy update" (due this week)

### ⚠️ Needs Manual Review
1. Unknown sender (external) — "Partnership opportunity" — couldn't determine if legitimate
```

## Customization

**Adjust classification rules** for your context:
- Add VIP senders who are always Urgent
- Route specific subjects to specific labels
- Set different thresholds for weekdays vs. weekends

**Add output destinations:**
- Slack DM: Post summary to `#morning-briefing` channel
- File: Write to `briefs/email-triage-YYYY-MM-DD.md`
- Combine with Morning Briefing: Feed the urgent items into your daily brief

## Tips

- **Review drafts before sending** for the first 2 weeks — build trust in the classifications
- **Tune the prompt** after a week: add senders or subjects that were misclassified
- **Combine with Morning Briefing**: Run email triage at 7:00, morning briefing at 7:30 — the briefing can reference triage results
