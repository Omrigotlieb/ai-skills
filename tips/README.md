# Claude Code Tips & Tricks

50+ curated tips from power users and 6+ months of community usage, organized by skill level.

> **Sources:** [ykdojo/claude-code-tips](https://github.com/ykdojo/claude-code-tips), r/ClaudeAI, community discoveries

---

## Foundational Tips (Start Here)

### 1. Plan Before Coding
**The single most important tip.** Press `Shift+Tab` to enter plan mode before coding.

```
Planning Mode → Coding Mode → Review
```

More time planning = higher success rate. Claude 4.x takes you literally—be prescriptive.

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

**Pro tip:** Start empty, add only repeated instructions. Let it grow organically.

---

### 3. Essential Slash Commands
```bash
/usage        # Check token usage and rate limits
/clear        # Clear conversation (start fresh)
/mcp          # List connected MCP servers
/stats        # Usage statistics graph
/compact      # Reduce context size
/context      # View what's loaded
/init         # Initialize CLAUDE.md for project
/chrome       # Browser integration
```

---

### 4. Voice Input
Use voice for faster, more natural prompting. Local tools:
- **macOS:** SuperWhisper, MacWhisper
- **Cross-platform:** Super Voice Assistant

Talking is faster than typing for complex instructions.

---

### 5. Screenshot and Image Support
Claude excels with visual input.

**macOS Quick Screenshot:**
1. `Cmd+Ctrl+Shift+4` - Screenshot to clipboard
2. `Ctrl+V` - Paste into Claude Code (note: Ctrl, not Cmd!)

This works for UI bugs, design references, error screenshots.

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
├── fix-issue.md      # /project:fix-issue 1234
├── review-pr.md      # /project:review-pr
├── deploy.md         # /project:deploy
└── gha.md            # /project:gha (debug CI)
```

Usage: `/project:fix-issue 1234`

---

### 8. Content Pasting for Blocked URLs
When Claude can't fetch a URL (Reddit, private pages, paywalled):
1. Open the page in your browser
2. `Cmd+A` (select all)
3. `Cmd+C` (copy)
4. Paste directly into Claude Code

Use Notion as a middle-man to preserve link formatting.

---

### 9. Context Management
Monitor and manage context actively:

```bash
/context      # See what's loaded
/compact      # Proactively reduce size
```

**Context is fresh = better performance.** Start new conversations for new topics.

---

### 10. Handoff Documents
Before context gets too large, ask Claude to create a handoff document:

```
Create a handoff document summarizing:
- What was accomplished
- Current state
- Next steps
- Key decisions made
```

Start fresh with the handoff doc.

---

### 11. Background Commands
Press `Ctrl+B` to background long-running commands. Run subagents asynchronously.

---

### 12. Session Resume
```bash
claude --resume
```
Resume previous session with full context preserved.

---

## Advanced Tips

### 13. Container Isolation for Risky Tasks
Run Claude Code in a Docker container for experimental/risky operations.

```bash
# With dangerous permissions in isolated container
docker run -it claude-code --dangerously-skip-permissions
```

Uses tmux as control layer. Safe sandbox for autonomous work.

---

### 14. Gemini CLI as Fallback
Use Gemini CLI through skills to access blocked sites:

```bash
# Create a skill that uses Gemini for Reddit access
claude skill install github:ykdojo/gemini-reddit-skill
```

---

### 15. Slim Down the System Prompt
Apply patches to reduce system prompt from ~20k to ~9k tokens (~55% reduction).

More context for your actual work.

---

### 16. Write-Test Cycles
For autonomous development:
1. Have Claude write code
2. Have Claude write tests
3. Run tests
4. Iterate until passing

Enable with tmux for interactive terminal testing.

---

### 17. Conversation Cloning
Branch conversations to explore different approaches:

```bash
# Clone current conversation with new UUID
# Try approach A in one branch
# Try approach B in another
# Compare results
```

---

### 18. Interactive PR Reviews
```bash
gh pr view 123 --json body,comments,files
```

Claude fetches the PR, analyzes changes, and provides structured feedback at your pace.

---

### 19. Claude Code as DevOps Engineer
Investigate CI failures autonomously:

```
# /project:gha command
Look at the failed GitHub Actions run.
Identify the root cause.
Propose a fix.
```

---

### 20. Exponential Backoff for Long Tasks
Check long-running job status with increasing intervals:
- 1 minute
- 2 minutes
- 4 minutes
- 8 minutes

Token-efficient for monitoring.

---

## Pro Tips

### 21. CLAUDE.md vs Skills vs Commands vs Plugins
Understanding when to use each:

| Tool | Loaded | Invoked By | Best For |
|------|--------|------------|----------|
| **CLAUDE.md** | Always | Auto | Project context, conventions |
| **Skills** | When relevant | Model | Domain expertise, workflows |
| **Commands** | On demand | User (`/cmd`) | Repeated actions, templates |
| **Plugins** | Always | Mixed | Bundled tools, team sharing |

---

### 22. Audit Approved Commands
Use `cc-safe` CLI to scan `.claude/settings.json`:

```bash
npx cc-safe scan
```

Checks for dangerous patterns: `rm -rf`, `sudo`, `curl | sh`, etc.

---

### 23. Test-Driven Development
Write failing tests first, commit them, then implement:

```
1. Write test that defines expected behavior
2. Commit the failing test
3. Implement code to pass
4. Claude can verify its own work
```

---

### 24. Verify Output Multiple Ways
Don't trust blindly:
- Write tests
- Use Git clients (GitHub Desktop)
- Create draft PRs for review
- Ask Claude to self-verify with tables

---

### 25. Choose Right Abstraction Level
Balance between:
- **Vibe coding** (high-level): "Make this work"
- **Deep dive** (line-by-line): Review every change

Adjust based on project criticality.

---

### 26. Simplify Overcomplicated Code
Question Claude's additions:
- "Why did you add this?"
- "Can this be simpler?"
- "Do we really need this abstraction?"

Understand every change.

---

## Hidden Features

### 27. Terminal Setup
Shift+Enter doesn't work for new lines by default.

```
/terminal-setup
```

Run once. Shift+Enter works forever after.

---

### 28. File Drag & Drop
- Normal drag: Opens in IDE
- **Shift + drag**: References file in Claude

---

### 29. Image Paste
- `Cmd+V` won't paste images
- Use `Ctrl+V` instead (yes, even on Mac)

---

### 30. Input Box Navigation
- `Ctrl+A` / `Ctrl+E` - Line start/end
- `Option+Left/Right` - Word navigation
- `Ctrl+G` - Open external editor
- `Ctrl+V` - Paste images

---

### 31. Headless Mode
```bash
claude -p "Review this code for security issues"
```

Unlocks automation: CI/CD integration, automated reviews, batch processing.

---

### 32. Environment Variables (Undocumented)
```bash
CLAUDE_PARALLEL_TOOLS=true
CLAUDE_THINKING_TIMEOUT=60
CLAUDE_DEBUG_MODE=true
```

---

### 33. realpath for Absolute Paths
```bash
realpath ./relative/path
# /absolute/path/to/file
```

Useful when referencing files in different directories.

---

## Productivity Shortcuts

### Status Line Customization
Display model, directory, git branch, token usage with 10 color themes.

### Terminal Aliases
```bash
alias c='claude'
alias ch='claude --chrome'
alias gb='open -a "GitHub Desktop" .'
alias co='code .'
```

### Search Conversation History
```bash
grep -r "keyword" ~/.claude/projects/
```

Query local `.jsonl` files for past discussions.

---

## Common Pitfalls to Avoid

1. **Skipping planning** - Always plan first
2. **Context bloat** - Compact regularly
3. **Too many MCPs** - Slows startup
4. **Vague prompts** - Be specific
5. **Ignoring errors** - Fix them immediately
6. **Not testing** - Write tests alongside code
7. **Blind trust** - Verify Claude's output

---

## Learning Path

1. **Start simple** - Use basic commands, read CLAUDE.md
2. **Add custom commands** - Automate repeated workflows
3. **Install MCP servers** - Extend capabilities
4. **Create skills** - Build domain expertise
5. **Contribute** - Share your discoveries

---

## Resources

### Tip Collections
- [ykdojo/claude-code-tips](https://github.com/ykdojo/claude-code-tips) - 40+ tips with examples
- [24 Claude Code Tips](https://dev.to/oikon/24-claude-code-tips-claudecodeadventcalendar-52b5) - Advent calendar
- [Hidden Features Guide](https://www.sidetool.co/post/claude-code-hidden-features-15-secrets-productivity-2025/) - 15 secrets

### Official
- [Anthropic Best Practices](https://www.anthropic.com/engineering/claude-code-best-practices)
- [Official Documentation](https://code.claude.com/docs)

### Community
- [r/ClaudeAI](https://reddit.com/r/ClaudeAI) - Reddit community
- [Agentic Coding Substack](https://agenticcoding.substack.com) - Weekly tips
