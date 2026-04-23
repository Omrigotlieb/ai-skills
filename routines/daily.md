# Daily Routines

Routines that run once per day to keep you informed and your codebase healthy.

---

## Morning Briefing

**Schedule:** Weekdays at 8:30am  
**Purpose:** Start the day with a clear picture of what needs attention.

```
Morning Briefing Routine

1. Check email (via Gmail MCP) and categorize:
   - Needs Response: messages requiring a reply today
   - Worth Knowing: updates relevant to current work
   - FYI: everything else
2. Check calendar (via Google Calendar MCP) for today's meetings
3. Check Slack (via Slack MCP) for overnight activity:
   - Direct messages and mentions
   - Key channel updates
4. Check GitHub for:
   - PRs awaiting my review
   - PRs I authored that have new comments
   - Issues assigned to me
5. Produce a single summary with:
   - Top 5-7 action items ranked by urgency
   - Today's meeting schedule
   - Any blockers or deadlines

Output format: Markdown summary posted to my daily notes.
```

### Minimal Version (No MCP Required)

```
Morning Briefing (Git-only)

1. Show PRs awaiting review: gh pr list --reviewer=@me
2. Show my open PRs with new activity: gh pr list --author=@me
3. Show issues assigned to me: gh issue list --assignee=@me
4. Show yesterday's merged PRs in this repo
5. Summarize as a prioritized action list
```

---

## Daily Code Review

**Schedule:** Weekdays at 9:00am  
**Purpose:** Catch issues in yesterday's commits before they compound.

```
Review all commits pushed to main in the last 24 hours.

For each commit:
1. Check for bugs or logic errors
2. Check for security issues (hardcoded secrets, injection vectors, auth gaps)
3. Check for error handling gaps
4. Identify code that needs comments or documentation

Output format:
- Summary of commits reviewed (count, authors, areas changed)
- Issues found (severity, file:line, description, suggestion)
- If no issues: "All clear - N commits reviewed"
```

---

## Activity Summary

**Schedule:** Weekdays at 6:00pm  
**Purpose:** Record what got done today for standups and retrospectives.

```
Generate a daily activity summary.

1. Run: git log --since="8am today" --oneline --author="$(git config user.name)"
2. Categorize commits by work theme (feature, bugfix, refactor, docs, chore)
3. List files changed with line counts
4. Note any PRs opened, merged, or reviewed today

Output format: Markdown summary suitable for a standup update.
Structure:
- What I shipped
- What I reviewed
- What's in progress
- Blockers (if any)
```

### With Token Metrics

If you have [ccusage](https://github.com/ryoppippi/ccusage) installed:

```
Generate a daily activity summary with cost metrics.

1. Run: npx ccusage --today (for token usage and cost)
2. Run: git log --since="8am today" --oneline
3. Categorize by work theme
4. Calculate cost-per-commit ratio

Output: Markdown summary with work themes and efficiency metrics.
```

---

## Nightly Backlog Grooming

**Schedule:** Weeknights at 10:00pm  
**Purpose:** Keep the issue tracker tidy without manual effort.

```
Groom the GitHub issue backlog.

1. Fetch issues opened today: gh issue list --state open --json number,title,body,labels,assignees
2. For unlabeled issues:
   - Read the issue body
   - Apply appropriate labels based on content (bug, feature, docs, chore)
   - Assign to the relevant code owner based on files likely affected
3. For issues older than 30 days with no activity:
   - Add a "stale" label
   - Post a comment asking if the issue is still relevant
4. Post a summary of actions taken

Skip conditions: Don't run if no new issues were opened today.
```

---

## Tips

- **Idempotency**: Design routines so re-running them replaces output rather than duplicating it. Use fixed file paths or update existing comments instead of creating new ones.
- **Cost control**: Daily routines on Cloud Routines count against your daily limit. Use the git-only versions when you don't need MCP integrations.
- **Time zones**: Schedule morning routines 30 minutes before your typical start time so results are ready when you sit down.
- **Failure handling**: Routines that post to external services (Slack, email) should degrade gracefully -- write a local report if the service is unavailable.
