# Claude Code Skills Catalog

Skills are model-invoked tools that Claude automatically uses when relevant to your task. Unlike slash commands which you explicitly trigger, skills enable intelligent, context-aware automation.

## How Skills Work

1. **Model-Invoked**: Claude decides when to use a skill based on context
2. **Automatic Loading**: Skills are loaded only when relevant
3. **Folder Structure**: Each skill contains instructions, scripts, and resources

## Installing Skills

```bash
# Via the anthropics/skills marketplace
claude skill install <skill-name>

# From a GitHub repository
claude skill install github:username/repo/skill-name
```

---

## Official Skills

### Document Processing

| Skill | Description | Install |
|-------|-------------|---------|
| **xlsx** | Excel manipulation: formulas, formatting, pivot tables, data analysis | `claude skill install xlsx` |
| **pdf** | PDF operations: text extraction, merging, splitting, form handling | `claude skill install pdf` |
| **docx** | Word documents: creation, editing, tracked changes, templates | `claude skill install docx` |
| **pptx** | PowerPoint: slides, layouts, templates, speaker notes | `claude skill install pptx` |

### Development

| Skill | Description | Install |
|-------|-------------|---------|
| **frontend-design** | React & Tailwind components avoiding generic AI aesthetics | `claude skill install frontend-design` |
| **artifacts-builder** | Complex interactive HTML artifacts with React/shadcn/ui | `claude skill install artifacts-builder` |
| **mcp-builder** | Create MCP servers for external API integration | `claude skill install mcp-builder` |
| **webapp-testing** | Playwright-based E2E web application testing | `claude skill install webapp-testing` |

### Creative

| Skill | Description | Install |
|-------|-------------|---------|
| **algorithmic-art** | Generative art with p5.js, randomness, particle systems | `claude skill install algorithmic-art` |
| **canvas-design** | Visual art creation in PNG and PDF formats | `claude skill install canvas-design` |
| **slack-gif-creator** | Animated GIFs optimized for Slack display | `claude skill install slack-gif-creator` |

### Communication

| Skill | Description | Install |
|-------|-------------|---------|
| **brand-guidelines** | Apply Anthropic brand colors and typography | `claude skill install brand-guidelines` |
| **internal-comms** | Status reports, newsletters, FAQ writing | `claude skill install internal-comms` |

### Meta

| Skill | Description | Install |
|-------|-------------|---------|
| **skill-creator** | Interactive Q&A tool for building new skills | `claude skill install skill-creator` |

---

## Community Skills

See [community/README.md](community/README.md) for community-contributed skills.

---

## Creating Your Own Skills

### Skill Structure
```
my-skill/
├── skill.md          # Main instructions
├── examples/         # Example inputs/outputs
├── scripts/          # Helper scripts
└── resources/        # Additional files
```

### skill.md Format
```markdown
# My Skill Name

## Description
What this skill does...

## When to Use
- Trigger condition 1
- Trigger condition 2

## Instructions
Step-by-step guidance...

## Examples
### Example 1
Input: ...
Output: ...
```

### Best Practices
1. Keep instructions focused and specific
2. Include clear trigger conditions
3. Provide multiple examples
4. Test with various scenarios
5. Document any dependencies

---

## Resources

- [Official Skills Documentation](https://code.claude.com/docs/en/skills)
- [Skills Announcement](https://www.anthropic.com/news/skills)
- [Creating Skills Guide](https://code.claude.com/docs/en/plugins)
