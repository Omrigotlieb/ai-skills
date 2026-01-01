# Claude Code Plugins Catalog

Plugins bundle skills, commands, agents, hooks, and MCP servers into shareable packages.

> **Latest:** 239+ Agent Skills available across marketplaces. Plugins are free and open-source.

## What Are Plugins?

Plugins extend Claude Code with custom functionality that can be shared across projects and teams. A plugin can contain:

- **Slash Commands** - User-invoked actions (`/commit`, `/review`)
- **Agents** - Specialized subagents for complex tasks
- **Skills** - Model-invoked expertise
- **Hooks** - Event handlers (pre-commit, post-run)
- **MCP Servers** - External tool integrations

---

## Installing Plugins

```bash
# Register a marketplace first
/plugin marketplace add owner/repo

# Install from marketplace
/plugin install plugin-name@marketplace-name

# Install from GitHub directly
claude plugin install github:username/repo

# Install from local path
claude plugin install ./path/to/plugin
```

---

## Featured Plugins

### Superpowers (obra)
**The most comprehensive development workflow suite**

Professional skills that activate automatically based on context.

**Features:**
- 20+ battle-tested skills (TDD, debugging, code review)
- Automatic skill activation
- Git worktree management
- Parallel agent workflows

**Install:**
```bash
/plugin marketplace add obra/superpowers-marketplace
/plugin install superpowers@superpowers-marketplace
```

**Commands:**
- `/superpowers:brainstorm` - Interactive design refinement
- `/superpowers:write-plan` - Create implementation plan
- `/superpowers:execute-plan` - Execute plan in batches

---

### dx (ykdojo)
**Developer Experience Bundle**

Essential commands for daily development workflow.

**Commands:**
- `/gha` - GitHub Actions helper
- `/handoff` - Create context handoff documents
- `/clone` - Clone conversation branch

**Install:**
```bash
claude plugin install github:ykdojo/dx
```

---

### commit-commands
**Git Workflow Automation**

Streamlined commit, push, and PR workflows.

**Commands:**
- `/commit` - Smart commit with message generation
- `/commit-push-pr` - Full workflow in one command
- `/clean_gone` - Clean up merged branches

**Install:**
```bash
/plugin marketplace add anthropics/claude-code
/plugin install commit-commands@anthropics/claude-code
```

---

### pr-review-toolkit
**Comprehensive PR Review Suite**

Multiple specialized agents for thorough code review.

**Agents:**
| Agent | Purpose |
|-------|---------|
| `code-reviewer` | Style, quality, conventions |
| `code-simplifier` | Simplification suggestions |
| `comment-analyzer` | Comment quality review |
| `silent-failure-hunter` | Error handling analysis |
| `type-design-analyzer` | Type system review |
| `pr-test-analyzer` | Test coverage analysis |

**Commands:**
- `/review-pr [aspects]` - Full PR review

**Install:**
```bash
/plugin install pr-review-toolkit
```

---

### frontend-design
**UI Development**

Production-grade frontend interface generation that avoids generic AI aesthetics.

**Features:**
- React component generation
- Tailwind CSS styling
- Responsive layouts
- Distinctive design patterns

**Install:**
```bash
/plugin install frontend-design
```

---

### feature-dev
**Guided Feature Development**

Architecture-focused feature implementation with specialized agents.

**Agents:**
| Agent | Purpose |
|-------|---------|
| `code-architect` | Design feature architectures |
| `code-explorer` | Analyze existing patterns |
| `code-reviewer` | Review implementations |

**Commands:**
- `/feature-dev [description]` - Start guided development

---

### code-refactoring
**Code Modernization Suite**

Refactoring and legacy modernization tools.

**Agents:**
| Agent | Purpose |
|-------|---------|
| `code-reviewer` | Modern code analysis, security, performance |
| `legacy-modernizer` | Framework migration, tech debt reduction |

---

### ralph-wiggum
**Iterative Problem Solving**

Loop-based approach for complex problem solving.

**Commands:**
- `/ralph-loop PROMPT` - Start iterative loop
- `/cancel-ralph` - Cancel active loop
- `/help` - Explain technique

---

### bmad (BMAD Method)
**Project Management Framework**

Full project lifecycle management with specialized agents.

**Agents:**
- `analyst` - Requirements analysis
- `architect` - System architecture
- `pm` - Project management
- `dev` - Development
- `ux-designer` - UX design
- `tech-writer` - Documentation

**Workflows:**
- `/bmad:create-tech-spec` - Create technical specifications
- `/bmad:create-epics-and-stories` - Break down requirements
- `/bmad:dev-story` - Execute development stories
- `/bmad:code-review` - Adversarial code review

---

## Plugin Marketplaces

| Marketplace | Description | Install |
|-------------|-------------|---------|
| **anthropics/claude-code** | Official Anthropic plugins | `/plugin marketplace add anthropics/claude-code` |
| **obra/superpowers-marketplace** | Curated development tools | `/plugin marketplace add obra/superpowers-marketplace` |
| **claude-plugins.dev** | Community registry | [Visit](https://claude-plugins.dev) |
| **skillsmp.com** | Agent skills marketplace | [Visit](https://skillsmp.com) |
| **aitmpl.com** | 100+ templates and plugins | [Visit](https://www.aitmpl.com/plugins) |

---

## Notable Plugin Collections

### Seth Hobson's Repository
80+ specialized sub-agents available via plugins.

### Dan Ávila's Marketplace
- DevOps automation
- Documentation generation
- Project management
- Testing suites

### Claude Code Plugins Plus Skills
239 Agent Skills with interactive Jupyter tutorials.

---

## Creating Your Own Plugin

### Plugin Structure
```
my-plugin/
├── plugin.json         # Metadata (required)
├── commands/           # Slash commands
│   └── my-command.md
├── agents/             # Specialized agents
│   └── my-agent.md
├── skills/             # Agent skills
│   └── my-skill/
│       └── SKILL.md
├── hooks/              # Event handlers
│   ├── pre-commit.sh
│   └── post-tool-use.sh
└── .mcp.json           # MCP configuration
```

### plugin.json
```json
{
  "name": "my-plugin",
  "version": "1.0.0",
  "description": "What my plugin does",
  "author": "Your Name",
  "homepage": "https://github.com/you/my-plugin",
  "commands": ["commands/my-command.md"],
  "agents": ["agents/my-agent.md"],
  "skills": ["skills/my-skill"],
  "hooks": {
    "pre-commit": "hooks/pre-commit.sh"
  }
}
```

### Command File (commands/my-command.md)
```markdown
# My Command

Description of what this command does.

## Usage
/project:my-command [args]

## Arguments
- `arg1` - Description

## Steps
1. First step...
2. Second step...
```

### Agent File (agents/my-agent.md)
```markdown
# My Agent

You are a specialized agent for [purpose].

## Capabilities
- Capability 1
- Capability 2

## Instructions
When invoked, you should...

## Output Format
Return results as...
```

---

## Best Practices

### For Users
- **Start small**: Install 1-2 plugins that match your workflow
- **Review source**: Check the plugin repository before installing
- **Update regularly**: Keep plugins current for security/features
- **Check overhead**: Too many plugins can slow Claude Code

### For Authors
- **Single responsibility**: Each plugin should do one thing well
- **Clear documentation**: Include usage examples
- **Version properly**: Follow semver for updates
- **Test thoroughly**: Verify all commands and agents work
- **Include examples**: Show real-world usage

---

## Hooks

Plugins can include hooks that trigger on events:

| Hook | Trigger |
|------|---------|
| `pre-commit` | Before git commit |
| `post-commit` | After git commit |
| `pre-tool-use` | Before tool execution |
| `post-tool-use` | After tool execution |
| `on-error` | When errors occur |

### Hook Example
```bash
#!/bin/bash
# hooks/pre-commit.sh

# Run linting before commit
npm run lint

# Exit non-zero to block commit
if [ $? -ne 0 ]; then
  echo "Linting failed. Commit blocked."
  exit 1
fi
```

---

## Resources

### Official
- [Plugin Documentation](https://code.claude.com/docs/en/plugins)
- [Plugin Creation Guide](https://code.claude.com/docs/en/plugins/create)
- [Marketplace Guide](https://code.claude.com/docs/en/plugin-marketplaces)
- [Anthropic Plugins](https://www.anthropic.com/news/claude-code-plugins)

### Community
- [claude-plugins.dev](https://claude-plugins.dev) - Community registry
- [awesome-claude-code-plugins](https://github.com/hekmon8/awesome-claude-code-plugins) - Curated list
- [claude-code-plugins-plus-skills](https://github.com/jeremylongshore/claude-code-plugins-plus-skills) - 239+ skills
