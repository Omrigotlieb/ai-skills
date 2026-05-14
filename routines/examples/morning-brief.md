# Morning Brief

> `loop.md` template — generates a daily development briefing.

## Usage

Copy to `.claude/loop.md` for on-demand runs with `/loop`. For recurring use, paste the template body into a Desktop scheduled task (Routines > New routine > Local) set to 8:30am weekdays.

## Template

```markdown
Generate a morning development briefing for today.

## Overnight Activity
- List PRs merged since yesterday 5pm
- List PRs opened since yesterday 5pm
- List new issues filed since yesterday 5pm

## Needs Attention
- Open PRs awaiting my review (assigned to me or requested)
- PRs I authored that have new review comments
- CI failures on any of my open branches

## Stale Items
- My PRs with no activity in 3+ days
- Issues assigned to me with no recent updates

Format as a scannable briefing. Use bullet points.
One line per item: "[PR #123] Title — status/action needed"

If a section is empty, write "None" and move on.
Keep total output under 30 lines.
```

## When to use

- Start-of-day routine to prioritize development work
- Team leads wanting a daily overview across multiple repos
- Remote teams needing async standup preparation
