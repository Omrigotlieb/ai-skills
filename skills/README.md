# Claude Code Skills Catalog

<div align="center">

[![Official Skills](https://img.shields.io/badge/Official-15%2B-blue)](https://github.com/anthropics/skills)
[![Community Skills](https://img.shields.io/badge/Community-150%2B-green)](community/README.md)
[![Scientific](https://img.shields.io/badge/Scientific-125%2B-purple)](https://github.com/K-Dense-AI/claude-scientific-skills)

</div>

Skills are model-invoked tools that Claude automatically uses when relevant to your task. Unlike slash commands which you explicitly trigger, skills enable intelligent, context-aware automation.

> **Latest Update:** January 2026 - Added 200+ skills across all categories

## How Skills Work

1. **Model-Invoked**: Claude decides when to use a skill based on context
2. **Automatic Loading**: Skills are loaded only when relevant
3. **Portable**: Same format works in Claude Code, Claude.ai, and API
4. **Folder Structure**: Each skill contains SKILL.md + optional scripts and resources

## Installing Skills

```bash
# Via the anthropics/skills marketplace
claude skill install <skill-name>

# From a GitHub repository
claude skill install github:username/repo/skill-name

# From superpowers marketplace
/plugin marketplace add obra/superpowers-marketplace
/plugin install superpowers@superpowers-marketplace
```

---

## Official Skills (Anthropic)

### Document Processing

| Skill | Description | Use Case |
|-------|-------------|----------|
| **xlsx** | Excel manipulation: formulas, formatting, pivot tables, charts, data analysis | Financial reports, data processing |
| **pdf** | PDF operations: text extraction, merging, splitting, form handling, OCR | Document processing, report generation |
| **docx** | Word documents: creation, editing, tracked changes, templates, styles | Documentation, contracts, proposals |
| **pptx** | PowerPoint: slides, layouts, templates, animations, speaker notes | Pitch decks, presentations |

### Development & Technical

| Skill | Description | Use Case |
|-------|-------------|----------|
| **frontend-design** | React & Tailwind components avoiding generic AI aesthetics | UI/UX implementation |
| **artifacts-builder** | Complex interactive HTML artifacts with React/shadcn/ui | Interactive prototypes |
| **mcp-builder** | Create MCP servers for external API integration | Tool building |
| **webapp-testing** | Playwright-based E2E web application testing | QA automation |

### Creative & Design

| Skill | Description | Use Case |
|-------|-------------|----------|
| **algorithmic-art** | Generative art with p5.js, randomness, particle systems | Visual content |
| **canvas-design** | Visual art creation in PNG and PDF formats | Design assets |
| **slack-gif-creator** | Animated GIFs optimized for Slack display | Team communication |

### Communication & Enterprise

| Skill | Description | Use Case |
|-------|-------------|----------|
| **brand-guidelines** | Apply brand colors, typography, and style guidelines | Consistent branding |
| **internal-comms** | Status reports, newsletters, FAQ writing | Team updates |

### Meta Skills

| Skill | Description | Use Case |
|-------|-------------|----------|
| **skill-creator** | Interactive Q&A tool for building new skills | Skill development |

---

## Superpowers Collection (obra)

The most comprehensive skill library for professional development. Install via:
```bash
/plugin marketplace add obra/superpowers-marketplace
/plugin install superpowers@superpowers-marketplace
```

### Testing Skills

| Skill | Description | Trigger |
|-------|-------------|---------|
| **test-driven-development** | Enforces RED-GREEN-REFACTOR cycle with anti-patterns reference | Implementing features |
| **verification-before-completion** | Confirms fixes are actually working before claiming done | Before task completion |

### Debugging Skills

| Skill | Description | Trigger |
|-------|-------------|---------|
| **systematic-debugging** | Four-phase root cause analysis with tracing and defense | Debugging issues |

### Collaboration Skills

| Skill | Description | Trigger |
|-------|-------------|---------|
| **brainstorm** | Socratic method for refining designs through questions | Design discussions |
| **writing-plans** | Creates detailed implementation plans with bite-sized tasks | Planning features |
| **executing-plans** | Batch execution with human checkpoints | Implementing plans |
| **dispatching-parallel-agents** | Enables concurrent subagent workflows | Complex tasks |
| **requesting-code-review** | Pre-review quality checklist | Before PR |
| **receiving-code-review** | Handles feedback integration gracefully | After review |
| **using-git-worktrees** | Manages isolated development branches | Parallel work |
| **finishing-a-development-branch** | Handles merge/PR decisions and cleanup | Branch completion |
| **subagent-driven-development** | Two-stage review: spec compliance, then code quality | Quality assurance |

### Meta Skills

| Skill | Description | Trigger |
|-------|-------------|---------|
| **writing-skills** | Framework for creating new skills with testing methodology | Creating skills |
| **using-superpowers** | Introduction to the skills system | Getting started |

### Superpowers Commands

```bash
/superpowers:brainstorm     # Interactive design refinement
/superpowers:write-plan     # Create implementation plan
/superpowers:execute-plan   # Execute plan in batches
```

---

## Scientific Skills (125+)

For research, bioinformatics, and data science. Source: [K-Dense-AI/claude-scientific-skills](https://github.com/K-Dense-AI/claude-scientific-skills)

### Scientific Databases (26+)

| Skill | Description | Domain |
|-------|-------------|--------|
| **openalex** | Academic publication search and analysis | Research |
| **pubmed** | Biomedical literature database | Life Sciences |
| **chembl** | Bioactivity database for drug discovery | Chemistry |
| **uniprot** | Protein sequence and function database | Bioinformatics |
| **cosmic** | Cancer mutation database | Oncology |
| **clinicaltrials** | Clinical trials registry | Medicine |
| **ncbi-gene** | Gene information database | Genetics |

### Python Packages (54+)

| Skill | Description | Domain |
|-------|-------------|--------|
| **rdkit** | Molecular modeling and cheminformatics | Chemistry |
| **scanpy** | Single-cell RNA-seq analysis | Genomics |
| **biopython** | Biological computation tools | Bioinformatics |
| **pytorch-lightning** | Deep learning framework | ML |
| **scikit-learn** | Machine learning library | Data Science |
| **pennylane** | Quantum machine learning | Quantum |
| **qiskit** | Quantum computing | Quantum |

### Scientific Integrations (15+)

| Skill | Description | Platform |
|-------|-------------|----------|
| **benchling** | Life sciences R&D platform | Lab Management |
| **dnanexus** | Genomics data analysis | Cloud |
| **latchbio** | Bioinformatics workflows | Cloud |
| **omero** | Image data management | Microscopy |
| **protocols-io** | Protocol sharing | Methods |

### Categories Covered
- Bioinformatics & Genomics
- Cheminformatics & Drug Discovery
- Proteomics & Mass Spectrometry
- Clinical Research & Precision Medicine
- Machine Learning & AI
- Quantum Computing

---

## Skill Categories

Detailed guides for specific skill domains:

| Category | Skills | Description | Link |
|----------|--------|-------------|------|
| **Security** | 10+ | DevSecOps, vulnerability detection, secure coding | [View](security/README.md) |
| **API Development** | 8+ | REST design, OpenAPI, documentation | [View](api-development/README.md) |
| **Testing** | 12+ | TDD, test generation, coverage, E2E | [View](testing/README.md) |
| **DevOps** | 15+ | CI/CD, Docker, Kubernetes, Terraform | [View](devops/README.md) |
| **Documentation** | 8+ | README, API docs, changelogs, ADRs | [View](documentation/README.md) |
| **Database** | 10+ | SQL, ORM, migrations, optimization | [View](database/README.md) |
| **Community** | 150+ | Community-contributed skills | [View](community/README.md) |

---

## Community Skills

See [community/README.md](community/README.md) for more community-contributed skills.

### Featured Individual Skills

| Skill | Description | Author |
|-------|-------------|--------|
| **ios-simulator-skill** | iOS app building and testing automation | Community |
| **playwright-skill** | General browser automation | Community |
| **claude-d3js-skill** | D3.js data visualizations | Community |
| **web-asset-generator** | Favicons, app icons, social images | Community |
| **ffuf-web-fuzzing** | Web fuzzing for pentesting | Community |
| **prevent-confirmatory** | Prevents automatic agreeable responses | @brunoasm |

---

## Creating Your Own Skills

### Skill Structure (Agent Skills Spec)
```
my-skill/
├── SKILL.md          # Main instructions (required)
├── examples/         # Example inputs/outputs
├── scripts/          # Helper scripts
└── resources/        # Additional files
```

### SKILL.md Format
```markdown
---
name: my-skill-name
description: Brief description of what this skill does
version: 1.0.0
---

# My Skill Name

## When to Use
- Trigger condition 1
- Trigger condition 2

## Instructions
Step-by-step guidance for Claude...

## Examples

### Example 1: Basic Usage
**Input:** User asks for X
**Output:** Claude does Y

## Guidelines
- Guideline 1
- Guideline 2
```

### Best Practices
1. **Keep instructions focused** - 150-200 instructions max
2. **Clear trigger conditions** - When should this skill activate?
3. **Multiple examples** - Show various use cases
4. **Test thoroughly** - Verify with different scenarios
5. **Document dependencies** - What else does this need?

### Skill Locations
```bash
# Personal skills (all projects)
~/.claude/skills/my-skill/

# Project skills (this repo only)
.claude/skills/my-skill/
```

---

## Resources

### Official
- [Skills Documentation](https://code.claude.com/docs/en/skills)
- [Skills Announcement](https://www.anthropic.com/news/skills)
- [Agent Skills Spec](https://agentskills.io)
- [anthropics/skills](https://github.com/anthropics/skills)

### Community
- [obra/superpowers](https://github.com/obra/superpowers) - Professional skills library
- [K-Dense-AI/claude-scientific-skills](https://github.com/K-Dense-AI/claude-scientific-skills) - 125+ scientific skills
- [awesome-claude-skills](https://github.com/travisvn/awesome-claude-skills) - Curated list
- [Skills Marketplace](https://skillsmp.com) - Skills directory

### Tutorials
- [Skills Explained](https://claude.com/blog/skills-explained) - Official comparison guide
- [Writing Skills Blog](https://blog.fsck.com/2025/10/16/skills-for-claude/) - Practical guide
