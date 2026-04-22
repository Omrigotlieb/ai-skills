# Skills vs MCP Servers vs Slash Commands vs Hooks

If you've opened the Claude Code docs and come away asking "wait, when do I reach for which of these?" — you're not alone. This page is the answer.

> Facts verified against [code.claude.com/docs](https://code.claude.com/docs/en/skills) on 2026-04-22. If something on this page disagrees with the official docs, trust the docs and [open an issue](https://github.com/Omrigotlieb/ai-skills/issues/new?template=bug.md).

## The confusion, stated plainly

Three things changed recently that broke people's mental models:

1. **Custom slash commands were merged into skills.** A file at `.claude/commands/deploy.md` and one at `.claude/skills/deploy/SKILL.md` both produce `/deploy` and behave the same way. Quoting the official docs: *"Custom commands have been merged into skills."* The old `.claude/commands/` directory keeps working — skills are just a superset.
2. **MCP is about tools, not instructions.** An MCP server gives Claude *something it can call*. A skill gives Claude *something it should read and apply*. These are unrelated primitives that people mix up because both "extend Claude."
3. **Hooks are not Claude's idea.** Hooks run in the harness around Claude, not inside the model's loop. They fire at event boundaries and can block, log, or inject — deterministically, every time.

So the four-way comparison collapses to **three real primitives**:

| Primitive | What it is | Who drives it |
|---|---|---|
| **Skill** (includes what we used to call slash commands) | A markdown playbook with YAML frontmatter | Claude or user |
| **MCP server** | A process exposing tools, resources, prompts over a protocol | Claude (picks tools from it) |
| **Hook** | An event handler (shell / HTTP / prompt) wired into the harness | The harness, on events |

Everything below is the detail.

---

## Side-by-side comparison

| Dimension | Skills | MCP Servers | Hooks |
|---|---|---|---|
| **Purpose** | Give Claude instructions, playbooks, or domain knowledge | Give Claude access to external tools and data | Enforce behavior at lifecycle events |
| **Who invokes** | Model auto-loads when relevant, or user types `/skill-name` | Model decides to call a tool | Harness fires on event (PreToolUse, Stop, etc.) |
| **Deterministic?** | No — model decides whether to follow the instructions | No — model decides whether to call the tool | Yes — runs every time the event matches |
| **File format** | `SKILL.md` with YAML frontmatter | `.mcp.json` config + a server process (http/sse/stdio) | JSON in `settings.json` under `"hooks"` |
| **Where it lives** | `~/.claude/skills/`, `.claude/skills/`, plugin | `.mcp.json` (project) or `~/.claude.json` (user) | `.claude/settings.json` or `~/.claude/settings.json` |
| **When loaded into context** | Description always loaded; body loads when invoked | Tool schemas loaded on demand (Tool Search default) | Never — runs outside model context |
| **Can block an action?** | No (it's advice, not enforcement) | No | **Yes** — PreToolUse hooks can deny |
| **Shareable via plugin?** | Yes | Yes | Yes |
| **Use case in one line** | "Apply our API conventions" | "Read Sentry issues" | "Never let rm -rf run in this repo" |

---

## Worked examples

### A skill

File: `.claude/skills/commit/SKILL.md`

```yaml
---
name: commit
description: Stage and commit the current changes with a conventional-commits message
disable-model-invocation: true
allowed-tools: Bash(git add *) Bash(git commit *) Bash(git status *)
---

Commit the current changes:

1. Run `git status` and `git diff` to see what changed
2. Stage the relevant files by name (never `git add -A`)
3. Write a conventional-commits message under 72 chars
4. Create the commit. Do not push.
```

What this does: a user types `/commit` and the markdown body becomes Claude's instructions. `disable-model-invocation: true` means Claude won't auto-trigger it — deploys and commits should be deliberate. `allowed-tools` grants the git permissions the skill needs so the user isn't prompted to approve each call.

### An MCP server entry

File: `.mcp.json` (project root)

```json
{
  "mcpServers": {
    "sentry": {
      "type": "http",
      "url": "https://mcp.sentry.dev/"
    }
  }
}
```

What this does: Claude can now discover and call Sentry tools (list issues, fetch event details, etc.). The skill/command analogue would be "tell Claude what to do"; MCP is "give Claude the phone number to call." The model still decides whether to call it.

### A hook

File: `.claude/settings.json`

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "if": "Bash(rm -rf *)",
            "command": "echo 'blocked by hook: rm -rf not allowed' && exit 1"
          }
        ]
      }
    ]
  }
}
```

What this does: every time Claude is about to invoke the Bash tool, the harness checks the `if` condition. If it matches, the hook runs; `exit 1` blocks the tool call. Claude does not get to argue with this — it's enforcement, not persuasion.

---

## Decision matrix

Match your intent to a primitive.

| I want to... | Reach for | Why |
|---|---|---|
| Teach Claude our team's API conventions | **Skill** (reference type) | Loads when relevant, costs nothing when not |
| Give Claude a `/deploy` button | **Skill** with `disable-model-invocation: true` | User-only invocation; Claude can't deploy unilaterally |
| Let Claude read Sentry issues while debugging | **MCP server** | External system access, tool-driven |
| Let Claude post to Slack | **MCP server** | Same reason — external API call |
| **Absolutely prevent** `rm -rf` from running | **Hook** (`PreToolUse`) | Skills are advice; hooks are enforcement |
| Run a linter after every file edit | **Hook** (`PostToolUse` on `Write\|Edit`) | Deterministic, fires every time |
| Document a one-off migration procedure Claude should follow once | **Skill** (invoked once) | That's exactly what skills are for |
| Store static facts ("our DB is Postgres 15, our CI is GitHub Actions") | **CLAUDE.md** | Facts, not playbooks — CLAUDE.md is cheaper |
| Block a command only in CI | **Hook** with a check on environment | Hooks run in the harness, not the model |
| Package a reusable set of skills + hooks + MCP for teammates | **Plugin** (bundles all three) | Plugins are the distribution unit |

---

## Honest trade-offs

### Skills are advice, not rules
A skill that says "never force-push to main" will sometimes be ignored. Models make judgment calls. If you need enforcement, use a hook. Skills + hooks together are a common pattern: skill explains the *why*, hook enforces the *what*.

### MCP servers multiply gracefully, but not infinitely
With Tool Search on (default in 2026), adding 50 MCP servers costs little context because tool schemas defer-load. If you disable Tool Search, every tool schema loads up front and you'll blow your context budget. Check before bulk-installing.

### Hooks run in the harness — they have no memory
A hook is a stateless function. It can't learn from prior runs, can't reason about context, can't ask a question. It's a deterministic gate. Don't try to build intelligent behavior in hooks; keep them narrow and fast.

### "Skills have merged with commands" has a gotcha
Your old `.claude/commands/foo.md` still works. But if you create a skill at `.claude/skills/foo/SKILL.md`, the skill wins (same name). Pick one location per command; don't have both.

### CLAUDE.md is not dead
Skills replace *procedures* (repeatable playbooks). CLAUDE.md is still the right place for *facts* (project stack, conventions, where things live). Facts are cheap to keep always-loaded; procedures are not.

### Hooks can deadlock or timeout
A hook that shells out to a slow script with no timeout will stall every tool call. Default timeout is 600 seconds — long. Set shorter timeouts explicitly for anything under production load, and use `async: true` for work that doesn't gate the decision.

---

## Further reading

All links are to official Claude Code documentation. Links last verified 2026-04-22.

- [Skills](https://code.claude.com/docs/en/skills) — full skill specification, frontmatter reference, subagent execution, dynamic context injection
- [MCP servers](https://code.claude.com/docs/en/mcp-servers) — transports, scopes, authentication
- [Hooks](https://code.claude.com/docs/en/hooks) — event types, matcher syntax, headless mode notes
- [Plugins](https://code.claude.com/docs/en/plugins) — packaging skills, hooks, and MCP together
- [Memory (CLAUDE.md)](https://code.claude.com/docs/en/memory) — when to use CLAUDE.md over a skill
- [Agent Skills open standard](https://agentskills.io) — cross-tool skill specification

---

*Found a mistake? This page is public-accountable — open an issue or PR in [this repo](https://github.com/Omrigotlieb/ai-skills) and we'll fix it.*
