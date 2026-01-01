# Contributing to AI Skills Hub

Thank you for your interest in contributing! This repository thrives on community input.

## Ways to Contribute

### 1. Submit a New Skill/Tool

Found a useful skill, MCP server, plugin, or tip? Here's how to add it:

**Option A: Open an Issue**
- Use our [New Skill Template](../../issues/new?template=new-skill.md)
- Provide the name, description, link, and use case

**Option B: Submit a Pull Request**
1. Fork the repository
2. Add your entry to the appropriate file
3. Follow the format below
4. Submit a PR with a clear description

### 2. Improve Existing Content

- Fix typos or errors
- Add better descriptions
- Update outdated links
- Add examples or use cases

### 3. Share Tips & Tricks

Have a Claude Code workflow that saves you time? Share it in `tips/`

---

## Entry Format

### Skills
```markdown
| Skill Name | Brief description (under 100 chars) | Primary use case |
```

### MCP Servers
```markdown
| Server Name | Description | Category | [Link](url) |
```

### Tips
```markdown
## Tip Title

**Category:** [Foundational/Intermediate/Advanced/Pro]

Brief description of the tip.

### How to Use
Step-by-step instructions...

### Example
\`\`\`bash
# Example code or commands
\`\`\`
```

---

## Quality Guidelines

### What We're Looking For
- **Useful** - Solves a real problem or saves significant time
- **Working** - Tested and functional
- **Documented** - Has clear instructions or documentation
- **Maintained** - Actively maintained (for tools/plugins)

### What We Avoid
- Abandoned projects (no updates in 6+ months without good reason)
- Duplicate functionality (unless significantly better)
- Low-quality or spammy submissions
- Tools with security concerns

---

## Research Sources

We actively monitor these sources for new tools. You can help by sharing discoveries from:

- **Reddit**: r/ClaudeAI, r/LocalLLaMA, r/MachineLearning, r/programming
- **GitHub**: Trending repos, new releases, awesome lists
- **LinkedIn**: AI/ML developer posts
- **Twitter/X**: @AnthropicAI, AI developer accounts
- **Blogs**: Dev.to, Medium, Substack, personal blogs
- **Discord**: Anthropic official, AI developer communities

---

## Pull Request Process

1. **Fork & Clone**
   ```bash
   git clone https://github.com/YOUR-USERNAME/ai-skills.git
   cd ai-skills
   ```

2. **Create a Branch**
   ```bash
   git checkout -b add/skill-name
   # or
   git checkout -b fix/description
   ```

3. **Make Changes**
   - Follow existing formatting
   - Test any links you add
   - Keep descriptions concise

4. **Commit**
   ```bash
   git add .
   git commit -m "Add: [Skill Name] - brief description"
   ```

5. **Push & Create PR**
   ```bash
   git push origin add/skill-name
   ```
   Then open a PR on GitHub.

---

## Commit Message Format

- `Add: [Name] - description` - New entries
- `Update: [Name] - what changed` - Modifications
- `Fix: description` - Bug fixes, typos
- `Remove: [Name] - reason` - Removing entries
- `Docs: description` - Documentation changes

---

## Code of Conduct

- Be respectful and constructive
- Focus on facts, not opinions
- Credit original authors
- No self-promotion spam

---

## Questions?

Open an issue with the question label, or join the discussion in existing issues.

Thank you for helping make this the best Claude Code resource hub!
