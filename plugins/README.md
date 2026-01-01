# Claude Code Plugins Catalog

Plugins bundle skills, commands, agents, hooks, and MCP servers into shareable packages.

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
# From a marketplace
claude plugin install marketplace:plugin-name

# From GitHub
claude plugin install github:username/repo

# From local path
claude plugin install ./path/to/plugin
```

---

## Featured Plugins

### [dx](https://github.com/ykdojo/claude-code-tips)
**Developer Experience Bundle**

Essential commands for daily development workflow.

**Commands:**
- `/gha` - GitHub Actions helper
- `/handoff` - Create context handoff documents
- `/clone` - Clone conversation branch

```bash
claude plugin install github:ykdojo/dx
```

---

### [commit-commands](https://claude-plugins.dev)
**Git Workflow Automation**

Streamlined commit, push, and PR workflows.

**Commands:**
- `/commit` - Smart commit with message generation
- `/commit-push-pr` - Full workflow in one command
- `/clean_gone` - Clean up merged branches

```bash
claude plugin install marketplace:commit-commands
```

---

### [pr-review-toolkit](https://claude-plugins.dev)
**Code Review Agents**

Comprehensive PR review with specialized agents.

**Agents:**
- `code-reviewer` - Style and quality checks
- `code-simplifier` - Simplification suggestions
- `comment-analyzer` - Comment quality review
- `silent-failure-hunter` - Error handling analysis
- `type-design-analyzer` - Type system review

**Commands:**
- `/review-pr [aspects]` - Full PR review

```bash
claude plugin install marketplace:pr-review-toolkit
```

---

### [frontend-design](https://claude-plugins.dev)
**UI Development**

Production-grade frontend interface generation.

**Features:**
- React component generation
- Tailwind CSS styling
- Avoids generic AI aesthetics
- Responsive layouts

```bash
claude plugin install marketplace:frontend-design
```

---

### [feature-dev](https://claude-plugins.dev)
**Feature Development**

Guided feature implementation with architecture focus.

**Agents:**
- `code-architect` - Design feature architectures
- `code-explorer` - Analyze existing patterns
- `code-reviewer` - Review implementations

**Commands:**
- `/feature-dev [description]` - Start guided development

```bash
claude plugin install marketplace:feature-dev
```

---

### [code-refactoring](https://claude-plugins.dev)
**Refactoring Tools**

Code modernization and quality improvement.

**Agents:**
- `code-reviewer` - Modern code analysis
- `legacy-modernizer` - Framework migration

```bash
claude plugin install marketplace:code-refactoring
```

---

## Plugin Marketplaces

| Marketplace | Description | Link |
|-------------|-------------|------|
| **claude-plugins.dev** | Community plugin registry | [Visit](https://claude-plugins.dev) |
| **skillsmp.com** | Agent skills marketplace | [Visit](https://skillsmp.com) |
| **anthropics/skills** | Official skills | [GitHub](https://github.com/anthropics/skills) |

---

## Creating Your Own Plugin

### Plugin Structure
```
my-plugin/
├── plugin.json         # Metadata
├── commands/           # Slash commands
│   └── my-command.md
├── agents/             # Specialized agents
│   └── my-agent.md
├── skills/             # Agent skills
│   └── my-skill/
├── hooks/              # Event handlers
│   └── pre-commit.sh
└── .mcp.json           # MCP configuration
```

### plugin.json
```json
{
  "name": "my-plugin",
  "version": "1.0.0",
  "description": "What my plugin does",
  "author": "Your Name",
  "commands": ["commands/my-command.md"],
  "agents": ["agents/my-agent.md"],
  "skills": ["skills/my-skill"]
}
```

### Command File (commands/my-command.md)
```markdown
# My Command

Description of what this command does.

## Usage
/project:my-command [args]

## Steps
1. First step...
2. Second step...
```

---

## Best Practices

### For Users
- **Start small**: Install 1-2 plugins that match your workflow
- **Review before installing**: Check the plugin source
- **Update regularly**: Keep plugins current

### For Authors
- **Single responsibility**: Each plugin should do one thing well
- **Clear documentation**: Include usage examples
- **Version properly**: Follow semver
- **Test thoroughly**: Verify all commands and agents work

---

## Resources

- [Plugin Documentation](https://code.claude.com/docs/en/plugins)
- [Plugin Creation Guide](https://code.claude.com/docs/en/plugins/create)
- [claude-plugins.dev](https://claude-plugins.dev)
