# Evening Review Routine

**Schedule:** Daily, 6 PM · **Duration:** 15–20 minutes · **Trigger:** Cron, manual, or desktop task

## What It Does

A structured daily reflection that captures what happened, identifies patterns, and sets up tomorrow. The key insight: **separate capture from synthesis** — don't try to simultaneously experience your day and make sense of it.

## Setup

### As a Scheduled Task

```bash
claude schedule create \
  --name "evening-review" \
  --cron "0 18 * * 1-5" \
  --prompt "$(cat <<'EOF'
Run my evening review for today.

## Process
Guide me through these 6 questions, one at a time. Wait for my response to each before proceeding.

1. **Mood & Energy**: "How are you feeling at the end of today? Rate energy 1-10."
2. **Key Activities**: "What were the 2-3 most significant things you did today?"
3. **Progress**: "What moved the needle today toward your bigger goals?"
4. **Blockers**: "What felt unresolved or frustrating?"
5. **Tomorrow**: "What are the 1-3 key goals for tomorrow?"
6. **Capture**: "Any ideas, insights, or things you want to remember?"

## Output
After all 6 questions, write a structured review to `journal/daily/YYYY-MM-DD.md`:

```
# Daily Review — YYYY-MM-DD

**Theme:** [One phrase that captures the day]
**Energy:** [1-10]
**Mood:** [From their response]

## Key Activities
- [Activity 1]
- [Activity 2]

## Progress
[What moved toward goals]

## Blockers
[What's unresolved]

## Tomorrow
- [ ] [Goal 1]
- [ ] [Goal 2]

## Captured Ideas
[Any insights or ideas mentioned]

## Meta
[Any patterns you notice across recent reviews — optional, add after 5+ entries exist]
```

Keep the review factual and concise. Don't editorialize.
EOF
)"
```

### As a Custom Command (Interactive)

Create `.claude/commands/evening-review.md`:

```markdown
Run my evening review. Ask me these questions one at a time:

1. How are you feeling? Rate energy 1-10.
2. What were the 2-3 most significant things you did today?
3. What moved the needle toward your bigger goals?
4. What felt unresolved or frustrating?
5. What are 1-3 key goals for tomorrow?
6. Any ideas or insights to capture?

After all questions, write the review to `journal/daily/YYYY-MM-DD.md`.
```

Usage: `/project:evening-review`

## Example Output

```markdown
# Daily Review — 2026-04-24

**Theme:** Shipped the auth migration
**Energy:** 7/10
**Mood:** Satisfied but tired

## Key Activities
- Merged auth migration PR #847 after 3 days of review
- Paired with Alex on rate limiting design
- Handled production memory spike in payments-service

## Progress
- Auth migration was the last blocker for Q2 security milestone
- Rate limiting design is 80% done — should ship by Monday

## Blockers
- Flaky test in payments-service CI still unresolved — blocked PR #851
- Still waiting on legal sign-off for data retention policy

## Tomorrow
- [ ] Fix flaky test_rate_limit_window
- [ ] Finish rate limiting implementation
- [ ] Follow up with legal on data retention

## Captured Ideas
- Could automate the deploy-freeze notification — too easy to forget
- The memory spike pattern looks like a connection pool leak, worth a deeper investigation

## Meta
Energy has been 6-7 range all week — might need to protect some focus time tomorrow morning.
```

## Building Habits

**Week 1–2:** Run manually when you remember. It's OK to skip days.

**Week 3–4:** Set a gentle reminder (calendar event or scheduled notification). Aim for 4 out of 5 weekdays.

**Month 2+:** Make it automatic. The value compounds as patterns emerge across entries.

## Customization

**For engineering managers**, add:
- "Any team dynamics to note?"
- "Did anyone do something worth recognizing?"

**For founders**, add:
- "What did you learn about customers today?"
- "Any strategic assumptions challenged?"

**For IC engineers**, add:
- "Did you learn a new technique or tool?"
- "Any technical debt you noticed?"

## Connecting to Weekly Retro

The evening review feeds directly into the [Weekly Retrospective](weekly-retro.md). The weekly routine reads your daily entries and synthesizes trends — this is why consistent daily capture matters more than perfect daily analysis.

## Tips

- **15 minutes is the target** — if it takes longer, your answers are too detailed
- **Don't grade yourself** — capture what happened, not how well you did
- **Skip the meta section** until you have 5+ entries — patterns need data
- **Output location matters**: Choose somewhere you'll actually see it again. A journal folder, Notion, or Obsidian all work.
