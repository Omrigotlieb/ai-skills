# Memory Consolidation

**Trigger:** Schedule | **Frequency:** Nightly at 5am | **Category:** Documentation

A 4-phase nightly process that keeps agent memory files clean, current, and navigable. Prevents memory bloat, removes contradictions, and ensures the memory index stays under size limits.

## Setup

```bash
claude /schedule create \
  --name "memory-consolidation" \
  --cron "0 5 * * *" \
  --prompt "$(cat <<'EOF'
You are running a nightly memory consolidation routine.

## Phase 1: Orient
- Read the MEMORY.md index file
- List all memory files in the memory directory
- Identify any files not listed in the index and any index entries pointing to missing files

## Phase 2: Gather
- Read each memory file
- Identify memories that overlap or cover the same topic
- Flag memories with relative dates that should be absolute
- Flag memories that contradict each other
- Flag memories that reference files, functions, or patterns that no longer exist in the codebase

## Phase 3: Consolidate
- Merge overlapping memories into single files by topic
- For contradictions, keep the most recent version and note what changed
- Convert any remaining relative dates to absolute dates
- Verify file paths and function names mentioned in memories still exist
- Remove or update memories that reference deleted code

## Phase 4: Prune and Index
- Delete empty or fully-merged memory files
- Update MEMORY.md index:
  - One line per entry, under 150 characters
  - Keep total index under 200 lines
  - Order semantically by topic, not chronologically
- Verify the index is clean and all entries point to existing files

## Constraints
- Do NOT delete memories that might still be relevant. When in doubt, keep and flag for human review.
- Do NOT create new memories. Only consolidate existing ones.
- Log a one-paragraph summary of what changed (files merged, deleted, updated).
EOF
)"
```

## Why This Matters

Agent memory files accumulate over days and weeks. Without consolidation:

- **Index bloat:** The MEMORY.md index exceeds 200 lines and gets truncated
- **Contradictions:** Older memories contradict newer learnings
- **Stale references:** Memories point to renamed or deleted files
- **Duplication:** Multiple files cover the same topic with slight variations

## Customization

- **Frequency:** Run weekly for low-activity projects
- **Aggressiveness:** Adjust the "when in doubt, keep" policy to match your preference
- **Scope:** Target specific memory types (user, feedback, project, reference) per run

## Related

- [Knowledge Base Updater](knowledge-base-updater.md) for appending new learnings
- [Docs Drift Detector](docs-drift-detector.md) for keeping documentation current
