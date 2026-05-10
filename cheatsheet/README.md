# Claude Code Cheatsheet

Quick reference guide for Claude Code commands, shortcuts, and patterns.

---

## Essential Commands

| Command | Description |
|---------|-------------|
| `/help` | Show all available commands |
| `/clear` | Clear conversation history |
| `/compact` | Reduce context size |
| `/context` | View loaded context |
| `/usage` | Check token usage |
| `/stats` | Show usage statistics |
| `/mcp` | List connected MCP servers |
| `/init` | Initialize CLAUDE.md file |
| `/config` | View configuration |

---

## Keyboard Shortcuts

### Navigation
| Shortcut | Action |
|----------|--------|
| `Shift+Tab` | Toggle plan mode |
| `Ctrl+C` | Cancel current operation |
| `Ctrl+L` | Clear screen |
| `↑` / `↓` | Navigate command history |

### Input
| Shortcut | Action |
|----------|--------|
| `Shift+Enter` | New line (after `/terminal-setup`) |
| `Ctrl+V` | Paste images (not Cmd+V!) |
| `Ctrl+G` | Open external editor |
| `Ctrl+A` | Move to line start |
| `Ctrl+E` | Move to line end |

### Files
| Shortcut | Action |
|----------|--------|
| `Shift+Drag` | Reference file in Claude |
| `#` | Add quick note to CLAUDE.md |

---

## CLI Flags

```bash
# Basic usage
claude                     # Start interactive session
claude "prompt"            # Single prompt (headless)
claude -p "prompt"         # Headless mode
claude --resume            # Resume previous session

# Configuration
claude --chrome            # Enable Chrome integration
claude --model opus        # Use specific model
claude --no-mcp            # Disable MCP servers

# Output
claude -o file.txt         # Save output to file
claude --json              # JSON output mode
```

---

## Routines & Scheduling

```bash
# Cloud routines (run on Anthropic infrastructure)
/schedule daily PR review at 9am
/schedule weekly on Monday, audit dependencies
/schedule tomorrow at 3pm, clean up feature flags
/schedule list                     # List all routines
/schedule update                   # Edit a routine
/schedule run                      # Trigger immediately

# Session-scoped loops
/loop 5m check the deploy          # Fixed interval
/loop check CI and fix failures    # Dynamic interval (Claude picks)
/loop                              # Built-in maintenance prompt
/loop 20m /review-pr 1234          # Re-run a command

# One-time reminders
remind me at 3pm to push the release branch
in 45 minutes, check whether tests passed
```

| Option | Runs on | Machine needed | Survives restart |
|--------|---------|---------------|-----------------|
| Cloud routine | Anthropic cloud | No | Yes |
| Desktop task | Your machine | Yes (app open) | Yes |
| `/loop` | Your machine | Yes (session open) | With `--resume` |

See [Routines guide](../workflows/routines.md) for production-ready prompt templates.

---

## File References

```
# Reference files in prompts
"Look at src/index.ts"
"Compare utils.py and helpers.py"

# Reference line numbers
"See src/auth.ts:45-67"

# Reference functions
"Find the authenticate function"
```

---

## Prompt Patterns

### Features
```
Implement [feature]:
1. [Requirement 1]
2. [Requirement 2]
Use [pattern] approach.
Add tests.
```

### Bug Fixes
```
Bug: [description]
Expected: [behavior]
Actual: [behavior]
Steps to reproduce:
1. [step]
```

### Code Review
```
Review this code for:
- Security issues
- Performance problems
- Best practices
```

### Refactoring
```
Refactor [component] to:
- Use [pattern]
- Improve [aspect]
Keep tests passing.
```

---

## CLAUDE.md Quick Reference

### File Locations
```
~/.claude/CLAUDE.md    # Global (all projects)
./CLAUDE.md            # Project root
./src/CLAUDE.md        # Subdirectory context
```

### Basic Structure
```markdown
# Project Name

## Tech Stack
- Framework: Next.js 15
- Language: TypeScript

## Commands
- `npm run dev` - Development
- `npm run test` - Tests

## Conventions
- Use functional components
- Prefer named exports
```

---

## MCP Configuration

### Location
```
~/.mcp.json           # Global MCP servers
./.mcp.json           # Project-specific
```

### Example
```json
{
  "mcpServers": {
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": { "GITHUB_TOKEN": "${GITHUB_TOKEN}" }
    }
  }
}
```

---

## Hooks Configuration

### Location
```json
// .claude/settings.json
{
  "hooks": {
    "PreToolUse": [{
      "matcher": "Bash",
      "command": "./hooks/validate.sh"
    }]
  }
}
```

### Exit Codes
| Code | Meaning |
|------|---------|
| 0 | Allow |
| 1 | Block (show error) |
| 2 | Block (silent) |

---

## Custom Commands

### Location
```
.claude/commands/
├── feature.md     # /project:feature
├── review.md      # /project:review
└── deploy.md      # /project:deploy
```

### Usage
```bash
/project:feature "Add user auth"
/user:mycommand "argument"
```

---

## Context Management

```bash
# Check context size
/context

# Reduce context
/compact

# Clear and start fresh
/clear
```

### Best Practices
- Keep conversations focused
- Use `/compact` when context grows
- Start new conversations for new topics
- Use handoff documents for continuity

---

## Git Operations

```
# Commit workflow
"Commit these changes with a descriptive message"

# PR creation
"Create a PR for this feature branch"

# Review PR
"Review PR #123"
```

---

## Quick Tips

1. **Plan First** - Use `Shift+Tab` before coding
2. **Screenshot Issues** - Paste with `Ctrl+V`
3. **Voice Input** - Faster than typing
4. **Worktrees** - Parallel branch work
5. **Custom Commands** - Automate workflows
6. **Context Fresh** - `/compact` regularly

---

## Environment Variables

```bash
# Optional configuration
CLAUDE_PARALLEL_TOOLS=true
CLAUDE_THINKING_TIMEOUT=60
ANTHROPIC_API_KEY=your-key
```

---

## Common Patterns

### Test-First Development
```
1. Write failing test
2. Implement to pass
3. Refactor
4. Verify tests still pass
```

### Feature Development
```
1. Plan (Shift+Tab)
2. Implement incrementally
3. Test each step
4. Review changes
5. Commit
```

### Debugging
```
1. Reproduce issue
2. Add logging
3. Narrow down cause
4. Fix
5. Add regression test
```

---

## Resources

- [Official Docs](https://code.claude.com/docs)
- [Tips & Tricks](../tips/README.md)
- [Workflows](../workflows/README.md)
- [CLAUDE.md Templates](../templates/README.md)
