# Claude Code Tips & Tricks

40+ curated tips from 6+ months of community usage, organized by skill level.

---

## Foundational Tips (Start Here)

### 1. Plan Before Coding
**The single most important tip.** Press `Shift+Tab` to enter plan mode before coding.

```
Planning Mode → Coding Mode → Review
```

More time planning = higher success rate.

---

### 2. Use CLAUDE.md Files
Treat Claude like an engineer being onboarded. Create documentation it can reference.

**Two levels:**
- `~/.claude/CLAUDE.md` - Personal preferences, global conventions
- `./CLAUDE.md` - Project-specific context

**What to include:**
- Tech stack and structure
- Common commands
- Code style guidelines
- Testing instructions

---

### 3. Essential Slash Commands
```bash
/usage        # Check token usage
/clear        # Clear conversation (start fresh)
/mcp          # List connected MCP servers
/stats        # Session statistics
/compact      # Reduce context size
/context      # View what's loaded
```

---

### 4. Voice Input
Use voice for faster, more natural prompting. Claude handles conversational input well.

---

### 5. Screenshot and Image Support
Claude excels with visual input.

**macOS Quick Screenshot:**
1. `Cmd+Ctrl+Shift+4` - Screenshot to clipboard
2. `Ctrl+V` - Paste into Claude Code (note: Ctrl, not Cmd)

---

## Intermediate Tips

### 6. Git Worktrees for Parallel Work
Work on multiple branches simultaneously without switching.

```bash
# Create worktree for a feature
git worktree add ../feature-branch feature-branch

# Claude can work in one while you review another
```

---

### 7. Custom Commands
Store repeated workflows in `.claude/commands/`:

```
.claude/commands/
├── fix-issue.md
├── review-pr.md
└── deploy.md
```

Usage: `/project:fix-issue 1234`

---

### 8. Content Pasting for Blocked URLs
When Claude can't fetch a URL:
1. Open the page in your browser
2. `Cmd+A` (select all)
3. `Cmd+C` (copy)
4. Paste directly into Claude Code

Works for Reddit, private pages, paywalled content.

---

### 9. Context Management
Monitor and manage context actively:

```bash
/context      # See what's loaded
/compact      # Proactively reduce size
```

Remove unused MCP tools to reduce overhead.

---

### 10. Use Handoff Documents
Before context gets too large, ask Claude to create a handoff document summarizing:
- What was accomplished
- Current state
- Next steps

Start fresh with the handoff doc.

---

## Advanced Tips

### 11. Container Isolation for Risky Tasks
Run Claude Code in a Docker container for experimental/risky operations.

```bash
# Claude controls another Claude instance in a container
# Uses tmux as the control layer
# Safe sandbox for autonomous work
```

See [ykdojo/claude-code-tips](https://github.com/ykdojo/claude-code-tips) for Docker setup.

---

### 12. Multi-Model Orchestration
Use Gemini CLI as a "minion" for specific tasks:
- Long document processing
- Tasks where Claude is rate-limited
- Cost optimization

---

### 13. System Prompt Optimization
The default system prompt can be reduced by ~55% for faster responses.

See the system prompt patches in the tips repository.

---

### 14. Write-Test Cycles
For autonomous development:
1. Have Claude write code
2. Have Claude write tests
3. Run tests
4. Iterate until passing

This loop can run with minimal supervision.

---

### 15. Conversation Cloning
Branch conversations to explore different approaches:
- Try approach A in one branch
- Try approach B in another
- Compare results

---

## Pro Tips

### 16. Skills vs Commands vs CLAUDE.md
Understanding when to use each:

| Tool | Invoked By | Best For |
|------|------------|----------|
| Skills | Model (automatic) | Domain expertise, workflows |
| Commands | User (`/command`) | Repeated actions, templates |
| CLAUDE.md | Model (reads on start) | Project context, conventions |

---

### 17. Abstraction Level Control
Be explicit about the level of abstraction:
- "High-level architecture only"
- "Implementation details for this function"
- "Line-by-line explanation"

---

### 18. Background Processes
```bash
# Run long processes in background
npm run build &

# Claude can work on other tasks while waiting
```

---

### 19. Interactive PR Reviews
```bash
/review-pr 123
```

Claude fetches the PR, analyzes changes, and provides structured feedback.

---

### 20. Exponential Backoff for Long Tasks
For processes that might fail:
1. Try with short timeout
2. If fails, increase timeout
3. Repeat with exponential increase

---

## Productivity Shortcuts

### Input Box Navigation
- `Ctrl+A` - Beginning of line
- `Ctrl+E` - End of line
- `Ctrl+U` - Clear line
- `Ctrl+W` - Delete word backward

### Mode Switching
- `Tab` - Cycle modes forward
- `Shift+Tab` - Cycle modes backward
- `Escape` - Cancel current operation

---

## Common Pitfalls to Avoid

1. **Skipping planning** - Always plan first
2. **Context bloat** - Compact regularly
3. **Too many MCPs** - Slows startup
4. **Vague prompts** - Be specific
5. **Ignoring errors** - Fix them immediately

---

## Resources

- [40+ Tips Repository](https://github.com/ykdojo/claude-code-tips)
- [Official Best Practices](https://www.anthropic.com/engineering/claude-code-best-practices)
- [24 Claude Code Tips](https://dev.to/oikon/24-claude-code-tips-claudecodeadventcalendar-52b5)
- [Agentic Coding Substack](https://agenticcoding.substack.com)
