# AI Skills Hub

A curated field guide for Claude Code skills, MCP servers, plugins, workflows, and reusable `CLAUDE.md` templates.

[![Docs Checks](https://github.com/Omrigotlieb/ai-skills/actions/workflows/docs-checks.yml/badge.svg)](https://github.com/Omrigotlieb/ai-skills/actions/workflows/docs-checks.yml)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Stars](https://img.shields.io/github/stars/Omrigotlieb/ai-skills?style=social)](https://github.com/Omrigotlieb/ai-skills)

[Skills](skills/README.md) | [MCP Servers](mcp-servers/README.md) | [Plugins](plugins/README.md) | [Templates](templates/README.md) | [Cheatsheet](cheatsheet/README.md) | [Tips](tips/README.md) | [Hooks](hooks/README.md) | [Workflows](workflows/README.md)

## What This Repo Is

AI tooling changes fast, and most discovery still happens through scattered GitHub repos, docs pages, Reddit posts, and social threads. This repository organizes the useful parts into a docs-first hub you can browse quickly and copy from immediately.

The emphasis is on:
- practical starting points instead of hype
- reusable docs and templates you can adopt today
- contributor-friendly structure that can keep improving over time

## Start Here

| If you want to... | Start here |
|---|---|
| Set up Claude Code on a new project | [CLAUDE.md templates](templates/README.md) |
| Find useful skills by category | [Skills catalog](skills/README.md) |
| Add external tools and integrations | [MCP servers guide](mcp-servers/README.md) |
| Improve daily workflow | [Tips](tips/README.md) and [Workflows](workflows/README.md) |
| Learn commands and shortcuts fast | [Cheatsheet](cheatsheet/README.md) |
| Understand automation hooks | [Hooks guide](hooks/README.md) |

## Recommended First 10 Minutes

1. Copy a template from [templates/README.md](templates/README.md) into your project as `CLAUDE.md`.
2. Add one or two high-value tools from [mcp-servers/README.md](mcp-servers/README.md).
3. Skim the [cheatsheet](cheatsheet/README.md) for commands and shortcuts you will actually use.
4. Pick one workflow from [workflows/README.md](workflows/README.md) and standardize on it.

## Repository Map

| Section | What you will find |
|---|---|
| [skills/README.md](skills/README.md) | Official skills, community collections, and focused category guides |
| [mcp-servers/README.md](mcp-servers/README.md) | Curated MCP picks plus 5 category breakdowns |
| [plugins/README.md](plugins/README.md) | Plugin concepts, marketplaces, and notable packages |
| [templates/README.md](templates/README.md) | 13 copy-ready `CLAUDE.md` templates |
| [cheatsheet/README.md](cheatsheet/README.md) | Commands, shortcuts, config snippets, and quick reference |
| [tips/README.md](tips/README.md) | Practical usage advice and day-to-day patterns |
| [hooks/README.md](hooks/README.md) | Hook types, behavior, and examples |
| [workflows/README.md](workflows/README.md) | Repeatable delivery, review, and debugging workflows |
| [prompts/README.md](prompts/README.md) | Prompt patterns for common development tasks |

## Why This Structure Works

- You can browse by job to be done, not just by raw link dump.
- The reusable assets live in-repo, especially the templates.
- The docs are organized so contributors can improve one section without touching everything else.
- The repository includes automated docs validation to catch broken local links and placeholder URLs before they land.

## Contributing

Contributions are most useful when they add verified resources, clearer explanations, or stronger examples.

- Submit a new resource: [open a submission issue](https://github.com/Omrigotlieb/ai-skills/issues/new?template=new-skill.md)
- Report a broken link or outdated doc: [open a fix issue](https://github.com/Omrigotlieb/ai-skills/issues/new?template=bug.md)
- Improve a page directly: [read the contribution guide](CONTRIBUTING.md)

Before opening a PR, run:

```bash
python3 scripts/validate_docs.py
```

## License

MIT. See [LICENSE](LICENSE).
