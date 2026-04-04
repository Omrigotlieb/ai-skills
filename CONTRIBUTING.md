# Contributing to AI Skills Hub

This repository works best when contributions are easy to verify, easy to maintain, and immediately useful.

## Quick Ways to Help

- Add a verified skill, MCP server, plugin, workflow, or tip
- Fix broken links or outdated installation steps
- Improve descriptions so readers can tell when to use a resource
- Tighten structure or navigation in the docs

## Submit a New Resource

### Option A: Open an Issue

- Use the [submission template](https://github.com/Omrigotlieb/ai-skills/issues/new?template=new-skill.md)
- Include the name, description, link, and best-fit category
- Explain the use case clearly enough that someone can decide whether it is worth trying

### Option B: Submit a Pull Request

1. Fork the repository
2. Add your entry to the appropriate file
3. Follow the existing format of the page you are editing
4. Run the docs validator locally
5. Submit a PR with a focused description

## Quality Bar

### What We Want

- Useful resources that solve a real problem
- Working links to real repositories or docs
- Short, specific descriptions
- Enough context to understand when a resource is worth using
- Maintained or still-relevant projects

### What We Avoid

- Placeholder links or example repositories
- Duplicate entries with no meaningful distinction
- Vague descriptions such as "best tool" or "great for everything"
- Abandoned projects without clear historical value
- Marketing-heavy copy with no setup or usage guidance

## Local Check

Run this before you open a PR:

```bash
python3 scripts/validate_docs.py
```

This check catches:
- broken local Markdown links
- broken section anchors in Markdown files
- placeholder URLs such as `github.com/example/...`

## Entry Format

### Skills

```markdown
| Skill Name | Brief description | Primary use case |
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

## Pull Request Process

1. **Fork and clone**
   ```bash
   git clone https://github.com/YOUR-USERNAME/ai-skills.git
   cd ai-skills
   ```
2. **Create a branch**
   ```bash
   git checkout -b add/skill-name
   ```
3. **Make changes**
   - Follow the formatting of the page you are editing
   - Keep descriptions concise
   - Prefer the most specific page that fits the resource
4. **Run validation**
   ```bash
   python3 scripts/validate_docs.py
   ```
5. **Commit**
   ```bash
   git add .
   git commit -m "Add: [Resource Name] - brief description"
   ```
6. **Push and open a PR**
   ```bash
   git push origin add/skill-name
   ```

## Commit Message Style

- `Add: [Name] - description` for new entries
- `Update: [Name] - what changed` for modifications
- `Fix: description` for broken links, typos, or factual corrections
- `Remove: [Name] - reason` for removals
- `Docs: description` for docs-only improvements

## Report a Problem

- Broken link or outdated doc: [open a fix issue](https://github.com/Omrigotlieb/ai-skills/issues/new?template=bug.md)
- New resource suggestion: [open a submission issue](https://github.com/Omrigotlieb/ai-skills/issues/new?template=new-skill.md)

## Code Of Conduct

- Be respectful and constructive
- Focus on facts, not opinions
- Credit original authors
- No self-promotion spam

## Questions?

Open an issue and keep the question specific to the page or resource you are referring to.
