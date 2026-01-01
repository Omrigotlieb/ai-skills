# AI Skills Hub

> **The most comprehensive, actively-maintained collection of Claude Code skills, MCP servers, plugins, tips, and resources.**

[![Daily Updates](https://img.shields.io/badge/updates-daily-brightgreen)](https://github.com/omrigotlieb/ai-skills/commits/main)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Stars](https://img.shields.io/github/stars/omrigotlieb/ai-skills?style=social)](https://github.com/omrigotlieb/ai-skills)

---

## Why This Repository?

The Claude Code ecosystem is evolving rapidly. New skills, MCP servers, and plugins emerge daily across Reddit, GitHub, LinkedIn, and Twitter. **This repository serves as your central hub** to discover, evaluate, and implement the best tools for your AI-powered development workflow.

**What makes us different:**
- **Daily updates** - We actively research Reddit, GitHub, LinkedIn, and Twitter for new tools
- **Curated, not just collected** - Each entry includes use cases, setup guides, and real-world examples
- **Community-driven** - Submit your discoveries via issues or PRs
- **Organized for discovery** - Find exactly what you need with our category system

---

## Table of Contents

- [Official Skills](#official-skills)
- [Community Skills](#community-skills)
- [MCP Servers](#mcp-servers)
- [Plugins](#plugins)
- [Tips & Tricks](#tips--tricks)
- [CLAUDE.md Templates](#claudemd-templates)
- [Resources](#resources)
- [Contributing](#contributing)
- [Changelog](#changelog)

---

## Official Skills

Skills are model-invoked tools that Claude automatically uses when relevant. Unlike slash commands (user-invoked), skills enable intelligent, context-aware automation.

### Document Skills
| Skill | Description | Use Case |
|-------|-------------|----------|
| **xlsx** | Excel spreadsheet manipulation with formulas, formatting, data analysis | Financial reports, data processing |
| **pdf** | PDF text extraction, merging, form handling | Document processing, report generation |
| **docx** | Word document creation with tracked changes | Documentation, contracts |
| **pptx** | PowerPoint presentations with layouts and templates | Pitch decks, presentations |

### Development Skills
| Skill | Description | Use Case |
|-------|-------------|----------|
| **frontend-design** | React & Tailwind design avoiding generic AI aesthetics | UI/UX implementation |
| **artifacts-builder** | Complex HTML artifacts using React and shadcn/ui | Interactive prototypes |
| **mcp-builder** | MCP server creation for external API integration | Tool building |
| **webapp-testing** | Playwright-based web application testing | E2E testing |

### Creative Skills
| Skill | Description | Use Case |
|-------|-------------|----------|
| **algorithmic-art** | Generative art using p5.js with particle systems | Visual content creation |
| **canvas-design** | Visual art creation in PNG/PDF formats | Design assets |
| **slack-gif-creator** | Animated GIFs optimized for Slack | Team communication |

### Meta Skills
| Skill | Description | Use Case |
|-------|-------------|----------|
| **skill-creator** | Interactive tool for building new skills | Skill development |
| **brand-guidelines** | Apply brand colors and typography | Consistent branding |

[View full skills catalog](skills/README.md)

---

## Community Skills

Community-contributed skills that extend Claude's capabilities.

### Featured Collections
| Collection | Description | Stars |
|------------|-------------|-------|
| [obra/superpowers](https://github.com/obra/superpowers) | 20+ battle-tested skills including TDD, debugging, code review | - |
| [obra/superpowers-lab](https://github.com/obra/superpowers-lab) | Experimental cutting-edge techniques | - |
| [claude-scientific-skills](https://github.com/BehiSecc/awesome-claude-skills) | 125+ scientific skills for bioinformatics, ML | - |

### Individual Skills
| Skill | Description | Author |
|-------|-------------|--------|
| **ios-simulator-skill** | iOS app building and testing automation | Community |
| **ffuf-web-fuzzing** | Web fuzzing for penetration testing | Community |
| **playwright-skill** | General browser automation | Community |
| **claude-d3js-skill** | D3.js data visualizations | Community |
| **web-asset-generator** | Favicons, app icons, social media images | Community |

[View full community skills](skills/community/README.md)

---

## MCP Servers

Model Context Protocol servers extend Claude's capabilities with external tools and data sources.

### Essential MCP Servers (Top 10)
| Server | Description | Category |
|--------|-------------|----------|
| **[GitHub MCP](https://github.com/modelcontextprotocol/servers)** | Repository management, PRs, issues, workflows | Git/VCS |
| **[Context7](https://github.com/context7/mcp)** | Real-time library documentation | Documentation |
| **[Filesystem MCP](https://github.com/modelcontextprotocol/servers)** | Secure local file operations | Core |
| **[PostgreSQL MCP](https://github.com/modelcontextprotocol/servers)** | Natural language database queries | Database |
| **[Puppeteer MCP](https://github.com/modelcontextprotocol/servers)** | Browser automation and testing | Automation |
| **[Sequential Thinking](https://github.com/modelcontextprotocol/servers)** | Structured problem-solving | Reasoning |
| **[Brave Search](https://github.com/modelcontextprotocol/servers)** | Privacy-first web search | Search |
| **[Notion MCP](https://github.com/modelcontextprotocol/servers)** | Productivity integration | Productivity |
| **[Figma MCP](https://github.com/modelcontextprotocol/servers)** | Design-to-code workflow | Design |
| **[Zapier MCP](https://github.com/zapier/mcp)** | Connect to 5000+ apps | Integration |

### By Category
- [Database Servers](mcp-servers/database.md)
- [Search & Research](mcp-servers/search.md)
- [Automation](mcp-servers/automation.md)
- [Productivity](mcp-servers/productivity.md)
- [Development](mcp-servers/development.md)

[View full MCP catalog](mcp-servers/README.md)

---

## Plugins

Plugins bundle skills, commands, agents, and MCP servers into shareable packages.

### Featured Plugins
| Plugin | Description | Features |
|--------|-------------|----------|
| **[dx](https://github.com/ykdojo/claude-code-tips)** | Developer experience bundle | /gha, /handoff, /clone commands |
| **[commit-commands](https://claude-plugins.dev)** | Git workflow automation | Commit, push, PR creation |
| **[pr-review-toolkit](https://claude-plugins.dev)** | Code review agents | Review, simplify, analyze |
| **[frontend-design](https://claude-plugins.dev)** | UI development | React component generation |

### Plugin Marketplaces
- [claude-plugins.dev](https://claude-plugins.dev) - Community plugin registry
- [skillsmp.com](https://skillsmp.com) - Agent skills marketplace
- [anthropics/skills](https://github.com/anthropics/skills) - Official skills

[View full plugin catalog](plugins/README.md)

---

## Tips & Tricks

Curated tips from 6+ months of community usage.

### Quick Wins
1. **Plan Mode First** - Press `Shift+Tab` to enter plan mode before coding
2. **Voice Input** - Use voice for faster prompting
3. **Custom Status Line** - Monitor usage and context in real-time
4. **Git Worktrees** - Work on multiple branches simultaneously

### Essential Commands
```bash
/usage        # Check token usage
/clear        # Clear conversation
/mcp          # List MCP servers
/stats        # Session statistics
/compact      # Reduce context size
```

### CLAUDE.md Best Practices
- Keep under 150-200 instructions
- Use WHAT/WHY/HOW framework
- Prefer pointers over code snippets
- Use subdirectory CLAUDE.md for specific contexts

[View all 40+ tips](tips/README.md)

---

## CLAUDE.md Templates

Ready-to-use CLAUDE.md templates for different project types.

| Template | Best For |
|----------|----------|
| [React/Next.js](templates/react-nextjs.md) | Frontend web apps |
| [Python/FastAPI](templates/python-fastapi.md) | Backend APIs |
| [Full-Stack](templates/fullstack.md) | End-to-end projects |
| [Monorepo](templates/monorepo.md) | Multi-package projects |
| [Open Source](templates/opensource.md) | Community projects |
| [Data Science](templates/data-science.md) | ML/AI projects |

[View all templates](templates/README.md)

---

## Resources

### Official Documentation
- [Claude Code Docs](https://code.claude.com/docs)
- [Claude Code Best Practices](https://www.anthropic.com/engineering/claude-code-best-practices)
- [Plugin Creation Guide](https://code.claude.com/docs/en/plugins)
- [Skills Announcement](https://www.anthropic.com/news/skills)

### Community Resources
- [awesome-claude-code](https://github.com/hesreallyhim/awesome-claude-code) - 18k+ stars
- [awesome-claude-skills](https://github.com/travisvn/awesome-claude-skills) - Curated skills list
- [claude-code-tips](https://github.com/ykdojo/claude-code-tips) - 40+ practical tips
- [awesome-mcp-servers](https://github.com/punkpeye/awesome-mcp-servers) - MCP server collection

### Tutorials & Guides
- [ClaudeLog](https://claudelog.com) - Docs, guides, tutorials
- [Agentic Coding Substack](https://agenticcoding.substack.com) - Tips and workflows
- [Dev.to Claude Code Tag](https://dev.to/t/claudecode) - Community articles

### Community
- [r/ClaudeAI](https://reddit.com/r/ClaudeAI) - Reddit community
- [Claude Discord](https://discord.gg/anthropic) - Official Discord

---

## Contributing

We welcome contributions! This repository thrives on community input.

### How to Contribute
1. **Found a new skill/tool?** [Open an issue](../../issues/new?template=new-skill.md)
2. **Have a tip to share?** [Submit a PR](CONTRIBUTING.md)
3. **Spotted an error?** [Report it](../../issues/new?template=bug.md)

### Research Sources We Monitor
- Reddit (r/ClaudeAI, r/LocalLLaMA, r/MachineLearning)
- GitHub trending & releases
- LinkedIn AI/ML communities
- Twitter/X AI developer accounts
- Dev.to, Medium, Substack

[Read contribution guidelines](CONTRIBUTING.md)

---

## Changelog

### 2026-01-01
- Initial repository setup
- Added official skills catalog
- Added top 10 MCP servers
- Added community skills collection
- Created CLAUDE.md templates

[View full changelog](CHANGELOG.md)

---

## Star History

If this repository helps you, please give it a star! It helps others discover these resources.

---

## License

MIT License - see [LICENSE](LICENSE) for details.

---

<p align="center">
  <b>Updated daily with the latest Claude Code skills and tools</b><br>
  <a href="https://github.com/omrigotlieb/ai-skills/stargazers">Star this repo</a> to stay updated
</p>
