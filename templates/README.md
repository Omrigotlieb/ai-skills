# CLAUDE.md Templates

Ready-to-use CLAUDE.md templates for different project types. Copy, customize, and use.

> **13 templates** covering web, backend, mobile, and more

## What is CLAUDE.md?

CLAUDE.md is a special file that Claude automatically reads when starting a conversation. It provides persistent context about your project, including:

- Project structure and tech stack
- Coding conventions and style
- Common commands
- Testing instructions
- Environment setup

---

## Available Templates

### Web & Frontend
| Template | Best For | Link |
|----------|----------|------|
| **React/Next.js** | Frontend web applications, SSR, App Router | [View](react-nextjs.md) |
| **Full-Stack** | End-to-end Next.js applications with API & DB | [View](fullstack.md) |
| **Vue.js** | Vue 3 applications with Composition API | [View](vue.md) |
| **Angular** | Angular 17+ standalone applications | [View](angular.md) |

### Backend
| Template | Best For | Link |
|----------|----------|------|
| **TypeScript** | TypeScript projects (Node.js, Bun, Deno) | [View](typescript.md) |
| **Python/FastAPI** | Python REST APIs, microservices | [View](python-fastapi.md) |
| **Python/Django** | Django web applications with DRF | [View](django.md) |
| **Go** | Go web services, CLI tools, high-performance APIs | [View](go.md) |
| **Rust** | Rust applications, systems programming, CLI tools | [View](rust.md) |

### Mobile
| Template | Best For | Link |
|----------|----------|------|
| **React Native** | Cross-platform mobile apps (iOS + Android) | [View](mobile-react-native.md) |

### Project Types
| Template | Best For | Link |
|----------|----------|------|
| **Monorepo** | Multi-package projects with Turborepo/pnpm | [View](monorepo.md) |
| **Data Science** | ML/AI projects, notebooks, experiments | [View](data-science.md) |
| **Open Source** | Community projects, libraries, contribution | [View](opensource.md) |

---

## Template Usage

### 1. Copy the Template
```bash
# Copy to your project root
cp templates/react-nextjs.md ./CLAUDE.md

# Or download directly
curl -o CLAUDE.md https://raw.githubusercontent.com/Omrigotlieb/ai-skills/main/templates/react-nextjs.md
```

### 2. Customize
Edit the template to match your project:
- Update paths and file references
- Add your specific conventions
- Include relevant commands
- Remove sections that don't apply

### 3. Iterate
Add to your CLAUDE.md as you work:
- Press `#` in Claude Code to add quick notes
- Review and refactor periodically
- Keep it under 200 lines

---

## Best Practices

### Keep It Concise
- Aim for 150-200 instructions max
- Claude follows fewer instructions more reliably
- Move details to per-folder CLAUDE.md files

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
```typescript
function authenticate() { ... }
```
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
```bash
npm run dev    # Development server
npm run test   # Run tests
```

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

## Don't
What to avoid
```

---

## Contributing Templates

Have a template for a specific stack or project type? Submit a PR!

**Requested Templates:**
- [x] Django/Python *(Added!)*
- [x] Vue.js *(Added!)*
- [x] Angular *(Added!)*
- [x] TypeScript *(Added!)*
- [ ] Spring Boot/Java
- [ ] Laravel/PHP
- [ ] Flutter/Dart
- [ ] Svelte/SvelteKit
- [ ] Elixir/Phoenix

**Requirements:**
- Follow the standard structure
- Include practical, tested guidance
- Keep it concise and actionable
- Add to this README's table

---

## Resources

- [Using CLAUDE.md Files](https://claude.com/blog/using-claude-md-files)
- [Writing a Good CLAUDE.md](https://www.humanlayer.dev/blog/writing-a-good-claude-md)
- [CLAUDE.md Best Practices](https://arize.com/blog/claude-md-best-practices-learned-from-optimizing-claude-code-with-prompt-learning/)
