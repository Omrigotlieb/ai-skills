# Docs Drift Detector

**Trigger:** Schedule | **Frequency:** Weekly | **Category:** Documentation

Scans merged PRs since the last run and identifies documentation that references changed APIs, function signatures, or configurations. Opens update PRs against stale docs so they stay current with the code.

## Setup

```bash
claude /schedule create \
  --name "docs-drift-detector" \
  --cron "0 9 * * 1" \
  --prompt "$(cat <<'EOF'
You are detecting documentation drift.

## Task
1. Gather Changes:
   - List all PRs merged since last Monday
   - Extract the files changed in each PR
   - Identify changes to public APIs, function signatures, configuration options, CLI flags, and environment variables

2. Scan Documentation:
   - Search all Markdown files, README files, and doc comments for references to the changed APIs/functions/configs
   - Check inline code examples for outdated function calls or parameter names
   - Check configuration examples for renamed or removed options

3. For each stale reference found:
   - Determine the correct current value from the code
   - Draft the documentation fix

4. Submit fixes:
   - If fewer than 5 fixes: open a single PR titled "Docs: update references after recent changes"
   - If 5+ fixes: group by area and open separate PRs
   - Link each fix to the PR that caused the drift

## Constraints
- Only fix clear, mechanical drift (renamed functions, changed defaults, removed options).
- Do NOT rewrite prose or change documentation style. Only update factual references.
- If unsure whether a reference is stale, add a comment to the doc file rather than changing it.
- Skip vendored, generated, or third-party documentation.
EOF
)"
```

## What It Catches

| Drift Type | Example |
|---|---|
| Renamed function | Docs say `getUser()`, code renamed to `fetchUser()` |
| Changed parameter | Docs show `timeout: int`, code changed to `timeout_ms: float` |
| Removed option | Docs reference `--verbose` flag, CLI removed it |
| Changed default | Docs say "defaults to 30s", code changed to 60s |
| New required field | API added required `api_version` field, docs don't mention it |

## Customization

- **Scope:** Limit to specific doc directories (e.g., `docs/`, `README.md` only)
- **Sensitivity:** Skip minor changes like type hint updates
- **Delivery:** Open issues instead of PRs for teams that prefer manual doc updates
- **Frequency:** Run daily for fast-moving APIs, monthly for stable ones

## Related

- [Memory Consolidation](memory-consolidation.md) for keeping agent memory files current
- [Knowledge Base Updater](knowledge-base-updater.md) for project knowledge updates
