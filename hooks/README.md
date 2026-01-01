# Claude Code Hooks

Hooks are user-defined shell commands that execute automatically at specific points in Claude Code's lifecycle. They enable custom automation, security controls, and workflow enhancements.

> **Released:** June 2025 | **Docs:** [Official Hooks Reference](https://code.claude.com/docs/en/hooks)

## Quick Start

Add hooks to your settings file:

```json
// ~/.claude/settings.json (global) or .claude/settings.json (project)
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "command": "./hooks/validate-command.sh"
      }
    ]
  }
}
```

---

## Hook Types

| Hook | When It Fires | Can Block? | Use Cases |
|------|---------------|------------|-----------|
| **UserPromptSubmit** | Before Claude processes user input | Yes | Context injection, prompt validation |
| **PreToolUse** | Before a tool executes | Yes | Security blocking, validation |
| **PostToolUse** | After a tool completes | No* | Logging, cleanup, formatting |
| **Notification** | When Claude sends alerts | No | TTS, desktop notifications |
| **Stop** | When Claude finishes responding | Yes | Force continuation |
| **SubagentStop** | When a subagent completes | No | Completion announcements |
| **PreCompact** | Before context compaction | No | Transcript backups |
| **SessionStart** | On session initialization | No | Load development context |

*PostToolUse cannot undo execution but can signal errors to Claude

---

## Exit Codes

| Code | Effect | Use Case |
|------|--------|----------|
| **0** | Success, stdout shown in transcript | Normal completion |
| **2** | Block action, stderr sent to Claude | Security blocking (PreToolUse) |
| **Other** | Non-blocking, stderr shown to user | Warnings, logging failures |

---

## Matchers

Matchers determine which tools trigger a hook:

```json
{
  "matcher": "Bash",           // Exact match
  "matcher": "Edit|Write",     // Multiple tools (OR)
  "matcher": ".*",             // All tools (regex)
  "matcher": "Task"            // Subagent tasks
}
```

**Common Tool Names:**
- `Bash` - Shell commands
- `Read` - File reading
- `Write` - File creation
- `Edit` - File modification
- `Glob` - File pattern matching
- `Grep` - Content search
- `Task` - Subagent spawning
- `WebFetch` - URL fetching
- `WebSearch` - Web searches

---

## Examples

### 1. Security: Block Dangerous Commands

```bash
#!/bin/bash
# hooks/block-dangerous.sh

# Read the command from stdin (JSON)
INPUT=$(cat)
COMMAND=$(echo "$INPUT" | jq -r '.tool_input.command // empty')

# Patterns to block
DANGEROUS_PATTERNS=(
  "rm -rf /"
  "rm -rf ~"
  "rm -rf \*"
  "> /dev/sda"
  "mkfs"
  "dd if="
  ":(){:|:&};:"
)

for pattern in "${DANGEROUS_PATTERNS[@]}"; do
  if [[ "$COMMAND" == *"$pattern"* ]]; then
    echo "BLOCKED: Dangerous command detected: $pattern" >&2
    exit 2
  fi
done

exit 0
```

**Configuration:**
```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "command": "./hooks/block-dangerous.sh"
      }
    ]
  }
}
```

---

### 2. Auto-Format After Edits

```bash
#!/bin/bash
# hooks/auto-format.sh

INPUT=$(cat)
FILE=$(echo "$INPUT" | jq -r '.tool_input.file_path // empty')

if [[ -z "$FILE" ]]; then
  exit 0
fi

# Format based on file extension
case "$FILE" in
  *.py)
    black "$FILE" 2>/dev/null || ruff format "$FILE" 2>/dev/null
    ;;
  *.js|*.ts|*.jsx|*.tsx)
    prettier --write "$FILE" 2>/dev/null
    ;;
  *.go)
    gofmt -w "$FILE" 2>/dev/null
    ;;
  *.rs)
    rustfmt "$FILE" 2>/dev/null
    ;;
esac

exit 0
```

**Configuration:**
```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "command": "./hooks/auto-format.sh"
      }
    ]
  }
}
```

---

### 3. Context Injection

```bash
#!/bin/bash
# hooks/inject-context.sh

# Prepend project context to every prompt
cat << EOF
[Project Context]
- Current sprint: Authentication refactor
- Key files: src/auth/, tests/auth/
- Standards: TypeScript strict, 80% test coverage
- Today: $(date +%Y-%m-%d)

[User Prompt]
EOF

# Pass through the original prompt
cat

exit 0
```

**Configuration:**
```json
{
  "hooks": {
    "UserPromptSubmit": [
      {
        "command": "./hooks/inject-context.sh"
      }
    ]
  }
}
```

---

### 4. Auto-Commit After Changes

```bash
#!/bin/bash
# hooks/auto-commit.sh

INPUT=$(cat)
FILE=$(echo "$INPUT" | jq -r '.tool_input.file_path // empty')

if [[ -n "$FILE" && -f "$FILE" ]]; then
  git add "$FILE"
  git commit -m "Auto-commit: Updated $FILE" --no-verify 2>/dev/null || true
fi

exit 0
```

---

### 5. TTS Notifications

```bash
#!/bin/bash
# hooks/speak-notification.sh

INPUT=$(cat)
MESSAGE=$(echo "$INPUT" | jq -r '.message // empty')

if [[ -n "$MESSAGE" ]]; then
  # macOS
  say "$MESSAGE" &

  # Linux (requires espeak)
  # espeak "$MESSAGE" &
fi

exit 0
```

**Configuration:**
```json
{
  "hooks": {
    "Notification": [
      {
        "command": "./hooks/speak-notification.sh"
      }
    ]
  }
}
```

---

### 6. Lint Before Commit

```bash
#!/bin/bash
# hooks/pre-commit-lint.sh

INPUT=$(cat)
COMMAND=$(echo "$INPUT" | jq -r '.tool_input.command // empty')

# Only run for git commit commands
if [[ "$COMMAND" != *"git commit"* ]]; then
  exit 0
fi

# Run linting
echo "Running pre-commit checks..." >&2

if ! npm run lint --silent; then
  echo "Linting failed. Fix errors before committing." >&2
  exit 2
fi

if ! npm run typecheck --silent; then
  echo "Type checking failed. Fix errors before committing." >&2
  exit 2
fi

exit 0
```

---

### 7. Transcript Backup Before Compact

```bash
#!/bin/bash
# hooks/backup-transcript.sh

BACKUP_DIR="$HOME/.claude/backups"
mkdir -p "$BACKUP_DIR"

TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="$BACKUP_DIR/transcript_$TIMESTAMP.json"

# Save the current context
cat > "$BACKUP_FILE"

echo "Transcript backed up to $BACKUP_FILE" >&2
exit 0
```

**Configuration:**
```json
{
  "hooks": {
    "PreCompact": [
      {
        "command": "./hooks/backup-transcript.sh"
      }
    ]
  }
}
```

---

### 8. Load Project Context on Start

```bash
#!/bin/bash
# hooks/session-init.sh

# Load environment-specific context
if [[ -f ".claude/context.md" ]]; then
  cat ".claude/context.md"
fi

# Add current git status
echo ""
echo "## Git Status"
git status --short 2>/dev/null || echo "Not a git repository"

# Add recent commits
echo ""
echo "## Recent Commits"
git log --oneline -5 2>/dev/null || true

exit 0
```

---

## Advanced Patterns

### JSON Response Format

For complex control flow, return structured JSON:

```bash
#!/bin/bash
# hooks/advanced-control.sh

INPUT=$(cat)
TOOL=$(echo "$INPUT" | jq -r '.tool_name')

# Complex validation logic
if should_block "$TOOL"; then
  cat << EOF
{
  "decision": "block",
  "reason": "This operation requires approval",
  "suggestion": "Try using a safer alternative"
}
EOF
  exit 2
fi

echo '{"decision": "allow"}'
exit 0
```

---

### GitButler Integration

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Edit|MultiEdit|Write",
        "command": "but claude pre-tool"
      }
    ],
    "PostToolUse": [
      {
        "matcher": "Edit|MultiEdit|Write",
        "command": "but claude post-tool"
      }
    ]
  }
}
```

---

## Best Practices

1. **PreToolUse for gates** - Block dangerous operations before they happen
2. **PostToolUse for cleanup** - Format, lint, log after changes
3. **Keep hooks fast** - Slow hooks degrade the experience
4. **Use project hooks** - Commit `.claude/settings.json` for team consistency
5. **Test thoroughly** - Bad hooks can break your workflow
6. **Log judiciously** - stderr goes to user, stdout to transcript

---

## Resources

- [Official Hooks Documentation](https://code.claude.com/docs/en/hooks)
- [claude-code-hooks-mastery](https://github.com/disler/claude-code-hooks-mastery) - Comprehensive examples
- [GitButler Integration](https://docs.gitbutler.com/features/ai-integration/claude-code-hooks)
- [Demystifying Hooks](https://www.brethorsting.com/blog/2025/08/demystifying-claude-code-hooks/)
