# CLAUDE.md Templates

Ready-to-use CLAUDE.md templates for different project types. Copy, customize, and use.

## What is CLAUDE.md?

CLAUDE.md is a special file that Claude automatically reads when starting a conversation. It provides persistent context about your project, including:

- Project structure and tech stack
- Coding conventions and style
- Common commands
- Testing instructions
- Environment setup

---

## Available Templates

| Template | Best For | Link |
|----------|----------|------|
| **React/Next.js** | Frontend web applications | [View](react-nextjs.md) |
| **Python/FastAPI** | Backend APIs | [View](python-fastapi.md) |
| **Full-Stack** | End-to-end applications | [View](fullstack.md) |
| **Monorepo** | Multi-package projects | [View](monorepo.md) |
| **Open Source** | Community projects | [View](opensource.md) |
| **Data Science** | ML/AI projects | [View](data-science.md) |

---

## Template Usage

### 1. Copy the Template
```bash
cp templates/react-nextjs.md ./CLAUDE.md
```

### 2. Customize
Edit the template to match your project:
- Update paths and file references
- Add your specific conventions
- Include relevant commands

### 3. Iterate
Add to your CLAUDE.md as you work:
- Press `#` in Claude Code to add quick notes
- Review and refactor periodically

---

## Best Practices

### Keep It Concise
- Aim for 150-200 instructions max
- Claude follows fewer instructions more reliably

### Use the WHAT/WHY/HOW Framework
```markdown
## WHAT
Tech stack, project structure, key files

## WHY
Project purpose, design decisions, constraints

## HOW
Commands, workflows, conventions
```

### Prefer Pointers Over Code
```markdown
# Good - Points to authoritative source
See `src/utils/auth.ts:45` for authentication pattern

# Avoid - Will become outdated
\`\`\`typescript
function authenticate() { ... }
\`\`\`
```

### Use Subdirectory Files
```
project/
├── CLAUDE.md           # Main project context
├── tests/
│   └── CLAUDE.md       # Testing-specific context
└── src/
    └── api/
        └── CLAUDE.md   # API-specific patterns
```

### Don't Duplicate Linter Work
Let tools like ESLint, Prettier, and Black handle formatting. CLAUDE.md should focus on higher-level guidance.

---

## Template Structure

Each template follows this structure:

```markdown
# Project Name

## Overview
Brief project description

## Tech Stack
- Framework: ...
- Language: ...
- Database: ...

## Project Structure
Key directories and their purposes

## Common Commands
\`\`\`bash
npm run dev    # Development server
npm run test   # Run tests
\`\`\`

## Code Conventions
- Naming conventions
- File organization
- Patterns to follow

## Testing
How to run and write tests

## Environment
Setup requirements, env vars

## Key Files
Important files to know about
```

---

## Contributing Templates

Have a template for a specific stack or project type? Submit a PR!

Requirements:
- Follow the standard structure
- Include practical, tested guidance
- Keep it concise and actionable

---

## Resources

- [Using CLAUDE.md Files](https://claude.com/blog/using-claude-md-files)
- [Writing a Good CLAUDE.md](https://www.humanlayer.dev/blog/writing-a-good-claude-md)
- [CLAUDE.md Best Practices](https://arize.com/blog/claude-md-best-practices-learned-from-optimizing-claude-code-with-prompt-learning/)
