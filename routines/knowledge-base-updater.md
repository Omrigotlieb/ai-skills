# Knowledge Base Updater

**Trigger:** End of session / Schedule | **Frequency:** Daily | **Category:** Documentation

Reviews what the agent learned during the day (patterns, gotchas, style preferences, resolved issues) and appends corrections to the project knowledge base files (CLAUDE.md, AGENTS.md). Creates a feedback loop where each coding session makes the next one more effective.

## Setup

```bash
claude /schedule create \
  --name "knowledge-base-updater" \
  --cron "0 18 * * 1-5" \
  --prompt "$(cat <<'EOF'
You are updating the project knowledge base with today's learnings.

## Task
1. Review today's activity:
   - Read git log for commits made today
   - Read any conversation logs or session transcripts available
   - Identify patterns: what went wrong, what was surprising, what worked well

2. Extract learnings worth persisting:
   - Build commands that are non-obvious
   - Test patterns that caught real bugs
   - Configuration gotchas discovered during debugging
   - Style preferences expressed in code review feedback
   - Architectural decisions made and their rationale

3. Check existing knowledge base:
   - Read CLAUDE.md (and AGENTS.md if it exists)
   - Identify if any existing entries are now outdated or contradicted
   - Identify if any new learnings duplicate existing entries

4. Update the knowledge base:
   - Append new entries to the appropriate section of CLAUDE.md
   - Update or remove outdated entries
   - Keep entries concise (1-2 lines each)
   - Group by topic (build, test, deploy, conventions, gotchas)

## Constraints
- Only add learnings that will be useful in FUTURE sessions. Skip one-time fixes.
- Do not remove entries unless you can verify they are wrong (test them if possible).
- Do not restructure or reformat existing entries. Only add, update, or remove.
- Keep CLAUDE.md under 200 lines. If approaching the limit, consolidate related entries.
- Commit changes with message "docs: update knowledge base with daily learnings"
EOF
)"
```

## What Gets Captured

| Category | Example Learning |
|---|---|
| Build | "Run `make gen` before `make test` - code generation must happen first" |
| Test | "Integration tests require `docker compose up db` running locally" |
| Deploy | "Staging deploy needs `ENV=staging` or it defaults to production config" |
| Conventions | "Error types follow `ErrXxxYyy` naming, not `XxxError`" |
| Gotchas | "The `cache` package silently swallows panics - always check error returns" |

## Customization

- **Trigger:** Run at end-of-session instead of scheduled, by adding to a PostSession hook
- **Scope:** Update CLAUDE.md only, or also maintain AGENTS.md, CONTRIBUTING.md
- **Review:** Require human approval before committing by opening a PR instead of direct commit
- **Sources:** Include Slack discussions or Linear comments as input alongside git history

## Related

- [Memory Consolidation](memory-consolidation.md) for agent memory file maintenance
- [Docs Drift Detector](docs-drift-detector.md) for keeping docs in sync with code changes
