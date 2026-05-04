# Community Skills

Community-contributed skills can be excellent, but they vary a lot in quality. This page focuses on verified collections, curation standards, and how to submit a real skill without filling the catalog with placeholder entries.

> Links last verified: 2026-04-23

---

## Strong Starting Points

### [obra/superpowers](https://github.com/obra/superpowers)
Battle-tested skills for professional development workflows.

**Included Skills:**
- Test-Driven Development (TDD)
- Debugging workflows
- Code review automation
- Documentation generation
- Refactoring patterns

```bash
claude skill install github:obra/superpowers
```

---

### [obra/superpowers-lab](https://github.com/obra/superpowers-lab)
Experimental skills pushing the boundaries of what is possible.

**Focus Areas:**
- Advanced reasoning techniques
- Multi-step automation
- Novel interaction patterns

```bash
claude skill install github:obra/superpowers-lab
```

---

### [BehiSecc/awesome-claude-skills](https://github.com/BehiSecc/awesome-claude-skills)
Curated awesome-list of Claude skills from the community. Check the repo for current scope and categories.

---

### [netresearch/claude-code-marketplace](https://github.com/netresearch/claude-code-marketplace)
Maintained Agent Skills marketplace with source-referenced skill repos for TYPO3, PHP modernization, Go, Docker, Jira, security, data tooling, and repository workflow automation.

Good fit when you want a practical marketplace to browse by concrete engineering workflow instead of a long generic awesome-list. The marketplace manifest points to individual source repositories, so inspect the specific skill repo before installing it.

```bash
/plugin marketplace add netresearch/claude-code-marketplace
```

---

## How To Evaluate A Community Skill

Use this checklist before you install or recommend one:

- The repository is real, public, and maintained.
- The skill explains what triggers it and what problem it solves.
- There are concrete examples, not just claims.
- Setup steps are short enough that someone can reproduce them.
- The skill adds specific leverage instead of wrapping generic advice.

---

## Submitting a Community Skill

1. Create a GitHub repository with your skill.
2. Follow the [skill structure guidelines](../README.md#creating-your-own-skills).
3. Make sure the repository includes a real `SKILL.md` and usage guidance.
4. [Open a submission issue](https://github.com/Omrigotlieb/ai-skills/issues/new?template=new-skill.md) in this repo.
5. We will review it before adding it to the catalog.

### Minimum Quality Requirements

- Clear documentation
- Working examples or clear demonstrations
- Active maintenance
- No security concerns
- No placeholder links or unverifiable claims

---

## What We Do Not List

- Placeholder repositories
- Example links that do not resolve to real projects
- Skills with vague descriptions and no usage guidance
- Near-duplicates that do not materially differ from an existing entry

---

## Workflow & Agent Orchestration

### [rohitg00/awesome-claude-code-toolkit](https://github.com/rohitg00/awesome-claude-code-toolkit)
The most comprehensive single collection: 135 agents, 35 skills, 42 commands, 176+ plugins, 20 hooks, 15 rules, 7 templates, and 14 MCP configs.

---

### [ComposioHQ/awesome-claude-skills](https://github.com/ComposioHQ/awesome-claude-skills)
1000+ production-ready skills across Claude Code, Codex, Cursor, and Gemini CLI. Cross-agent compatible.

---

### [ComposioHQ/awesome-claude-plugins](https://github.com/ComposioHQ/awesome-claude-plugins)
Curated plugins that extend Claude Code with custom commands, agents, hooks, and MCP servers.

---

### [shinpr/claude-code-workflows](https://github.com/shinpr/claude-code-workflows)
Production-ready multi-agent pipeline: Analyze → Design → Plan → Implement → Verify. Each phase runs in a fresh agent context. Includes `/recipe-implement` and specialized agents (requirement-analyzer, technical-designer, work-planner, task-executor, quality-fixer).

---

### [barkain/claude-code-workflow-orchestration](https://github.com/barkain/claude-code-workflow-orchestration)
Plugin for multi-step workflow orchestration with automatic task decomposition, parallel agent execution, and plan-mode integration.

---

### [Piebald-AI/claude-code-system-prompts](https://github.com/Piebald-AI/claude-code-system-prompts)
All of Claude Code's internal system prompts extracted and versioned across 167+ releases. Includes sub-agent prompts for Plan, Explore, and Task modes. Essential reference for writing effective agent prompts.

---

### [shining319/claude-code-single-person-workflow](https://github.com/shining319/claude-code-single-person-workflow)
Plugins for solo developers: docs, database design, product management, UI/UX, and solution architecture in one marketplace.

---

### [quemsah/awesome-claude-plugins](https://github.com/quemsah/awesome-claude-plugins)
Automated adoption metrics for Claude Code plugins across GitHub repos using n8n workflows.

---

## Tools For Skill Development

### [skill-creator](https://github.com/anthropics/skills)
Official interactive skill creation tool.
