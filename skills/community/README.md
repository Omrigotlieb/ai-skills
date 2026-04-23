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

## Tools For Skill Development

### [skill-creator](https://github.com/anthropics/skills)
Official interactive skill creation tool.
