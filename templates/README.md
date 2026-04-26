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

The advice below maps to current Anthropic guidance ([memory docs](https://code.claude.com/docs/en/memory), [best practices](https://code.claude.com/docs/en/best-practices), verified April 2026) and to practitioner experience reports.

### Keep it short
Anthropic's memory docs explicitly recommend **under ~200 lines per CLAUDE.md file**. Longer files consume context and reduce adherence. Diagnostic: if Claude keeps ignoring a rule despite repeated emphasis, the file is usually too long, not the rule too weak.

### Be specific, not aspirational
Vague rules underperform concrete ones. From Anthropic's own example:

- Avoid: *"Format code properly"*
- Prefer: *"Use 2-space indentation"*

Use **MUST**, **MUST NOT**, **IMPORTANT**, or **YOU MUST** for the rules you actually need followed — Anthropic explicitly endorses this emphasis.

### Don't duplicate the linter
ESLint, Prettier, Black, gofmt already enforce style. Mentioning the same rules in CLAUDE.md wastes context Claude could spend on things only humans can encode.

### Short snippets OK, real implementations no
A 5-10 line illustrative example is fine (Anthropic's own examples include them). Pasting real implementation code is not — it rots, then misleads. Reference the source by path: *"See `src/auth/login.ts:45` for the canonical pattern."*

---

## CLAUDE.md vs Skills vs `.claude/rules/`

Three primitives, three jobs. Picking the wrong one is the most common bloat source. This is the single biggest architectural shift in Claude Code since this directory was first written, and it changes how templates should be used.

| Primitive | Loaded when | Right for |
|---|---|---|
| **CLAUDE.md** | Every session, always | Project-wide facts and rules that always apply |
| **`.claude/rules/<name>.md`** with `paths:` frontmatter | When Claude touches matching files | Path-scoped rules (e.g., "in `tests/`, use vitest") |
| **Skill** at `.claude/skills/<name>/SKILL.md` | On demand — model or user invokes | Workflows and playbooks that only sometimes apply |

If your CLAUDE.md has grown into "if you're doing X, do Y" sections, those are skills waiting to happen. Move them and the always-on file gets shorter and more reliable.

For the deeper comparison (skills vs MCP vs hooks too), see the [primitives flagship](../docs/skills-vs-mcp-vs-commands-vs-hooks.md).

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

**Official (canonical, current April 2026):**
- [Memory: How Claude remembers your project](https://code.claude.com/docs/en/memory)
- [Best Practices for Claude Code](https://code.claude.com/docs/en/best-practices)
- [Using CLAUDE.md Files (blog)](https://claude.com/blog/using-claude-md-files)

**Practitioner deep-dives:**
- [Writing a Good CLAUDE.md (HumanLayer, Nov 2025)](https://www.humanlayer.dev/blog/writing-a-good-claude-md) — source of the "150-200 instructions" heuristic and the "pointers over code" guidance
- [CLAUDE.md Best Practices (Arize, Nov 2025)](https://arize.com/blog/claude-md-best-practices-learned-from-optimizing-claude-code-with-prompt-learning/) — quantitative results from prompt learning
- [CLAUDE.md best practices: from basic to adaptive (dev.to, Feb 2025)](https://dev.to/cleverhoods/claudemd-best-practices-from-basic-to-adaptive-9lm) — L0-L6 maturity model
