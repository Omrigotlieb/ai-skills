# Weekly Retrospective Routine

**Schedule:** Sunday evening · **Duration:** 20–30 minutes · **Trigger:** Cron or manual · **Depends on:** [Evening Review](evening-review.md) daily entries

## What It Does

Synthesizes your daily reviews into a weekly picture. Identifies trends in energy, recurring blockers, and progress velocity. Produces a forward-looking plan for the next week.

## Setup

### As a Scheduled Task

```bash
claude schedule create \
  --name "weekly-retro" \
  --cron "0 19 * * 0" \
  --prompt "$(cat <<'EOF'
Run my weekly retrospective.

## Steps
1. Read all daily review files from `journal/daily/` for this past week
2. If daily reviews are missing, check git log and calendar for activity context

## Guide me through 5 phases:

### Phase 1: Theme
"In one sentence, what defined this week?"

### Phase 2: Highlights
"What are you most proud of this week? What went well?"

### Phase 3: Challenges
"What didn't go as planned? What was harder than expected?"

### Phase 4: Lessons
"What did you learn? What would you do differently?"

### Phase 5: Forward Look
"What's the ONE thing to nail next week?"

## Output
Write to `reviews/weekly/YYYY-WW.md`:

```
# Weekly Retrospective — Week WW, YYYY

**Theme:** [One sentence]

## By the Numbers
- Days reviewed: X/5
- Average energy: X/10
- Energy trend: [rising/stable/declining]

## Highlights
- [Win 1]
- [Win 2]

## Challenges
- [Challenge 1]
- [Challenge 2]

## Patterns Noticed
[Recurring themes across daily reviews — energy dips, blocker types, productive conditions]

## Lessons
- [Lesson 1]
- [Lesson 2]

## Next Week
**One thing:** [The priority]

### Also planned:
- [ ] [Item 1]
- [ ] [Item 2]

## Stale Items
[Tasks or projects with no progress in 7+ days — flag for decision: continue, defer, or drop]
```
EOF
)"
```

### As a Custom Command

Create `.claude/commands/weekly-retro.md`:

```markdown
Run my weekly retrospective.

1. Read daily reviews from `journal/daily/` for this week
2. Ask me 5 questions (one at a time):
   - What defined this week?
   - What went well?
   - What didn't go as planned?
   - What did you learn?
   - What's the ONE thing to nail next week?
3. Write retrospective to `reviews/weekly/YYYY-WW.md`

Include: energy trends, recurring patterns, stale items needing a decision.
```

## Example Output

```markdown
# Weekly Retrospective — Week 17, 2026

**Theme:** Finally cleared the security backlog, but at the cost of new feature work.

## By the Numbers
- Days reviewed: 4/5 (missed Wednesday)
- Average energy: 6.5/10
- Energy trend: declining (started at 8, ended at 5)

## Highlights
- Shipped auth migration — 3-week effort complete
- Rate limiting design approved by team
- Mentored Alex on database optimization patterns

## Challenges
- Flaky test blocked payments-service PR all week
- Lost most of Thursday to an unplanned production incident
- Deploy freeze compressed merge timeline

## Patterns Noticed
- Energy drops on days with 4+ meetings (happened twice this week)
- Most productive work happened before 11 AM
- Blockers involving other teams took 2-3x longer than estimated

## Lessons
- Should have escalated the flaky test on Tuesday instead of Thursday
- Batching code reviews into a single afternoon slot worked well — keep doing this

## Next Week
**One thing:** Ship rate limiting to production

### Also planned:
- [ ] Fix flaky test permanently (not just skip)
- [ ] Start Q3 planning doc
- [ ] Schedule 1:1s for team performance reviews

## Stale Items
- Dashboard rework spec (no progress in 12 days) → Decision needed: defer to Q3?
- Logging improvements RFC (no progress in 8 days) → Waiting on ops team input
```

## Connecting the System

```
Daily Evening Reviews → Weekly Retro → Monthly/Quarterly Goals
        ↓                    ↓
    journal/daily/      reviews/weekly/
```

The weekly retro reads daily reviews. If you skip daily reviews, the weekly retro still works — it just uses git log and calendar data instead, which captures activity but not energy/mood/reflection.

## Tips

- **Sunday evening is ideal** — you're far enough from work to be reflective, close enough to remember details
- **Don't optimize for length** — a 200-word retro that surfaces one real insight beats a 1000-word catalog
- **The "stale items" section is the most valuable** — it forces decisions on things you've been avoiding
- **After 4 weekly retros**, you'll have enough data to see monthly patterns. Consider a monthly synthesis at that point.
