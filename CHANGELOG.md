# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

---

## [Unreleased]

### Added
- Looking for new skills and tools daily!

---

## [1.4.0] - 2026-01-02

### Added

**New Skill Categories**
- **Performance Skills** (`skills/performance/`) - 10+ skills
  - Performance profiling (Node.js, Python, Go, Rust)
  - Frontend performance (Core Web Vitals)
  - Backend optimization
  - Memory optimization
  - Algorithm complexity analysis
  - Load testing (k6, Artillery, JMeter)
  - Caching strategies

- **AI/ML Skills** (`skills/ai-ml/`) - 12+ skills
  - LLM integration (Anthropic, OpenAI, Cohere)
  - Prompt engineering techniques
  - RAG implementation (vector DBs, chunking)
  - Model fine-tuning (LoRA, full fine-tune)
  - Computer vision (YOLO, CLIP, multimodal)
  - ML pipelines (MLflow, W&B, Feast)
  - Data processing (pandas, polars, dask)
  - AI safety guardrails

### Changed
- Updated skills count badge to 250+
- Enhanced skills catalog with new categories

---

## [1.3.0] - 2026-01-02

### Added

**New Skill Categories**
- **Testing Skills** (`skills/testing/`) - 12+ skills
  - TDD workflow (RED-GREEN-REFACTOR)
  - Test generation (Jest, pytest, Go)
  - Coverage analysis
  - Property-based testing
  - Mutation testing
  - Snapshot testing
  - E2E testing (Playwright, Cypress)
  - Contract testing (Pact)

- **DevOps Skills** (`skills/devops/`) - 15+ skills
  - GitHub Actions debugging
  - Docker optimization
  - Kubernetes manifests
  - Terraform IaC
  - CI/CD pipeline design
  - Deployment strategies
  - Monitoring & observability
  - Incident response

- **Documentation Skills** (`skills/documentation/`) - 8+ skills
  - README generator
  - JSDoc/TSDoc generator
  - API documentation
  - Changelog generator
  - Architecture diagrams (C4)
  - Code comments best practices
  - ADR templates
  - Runbook templates

- **Database Skills** (`skills/database/`) - 10+ skills
  - SQL query writing & optimization
  - Database design
  - Migration management
  - Query optimization
  - ORM skills (Prisma, SQLAlchemy)
  - NoSQL skills (MongoDB, Redis)
  - Repository pattern
  - Unit of Work pattern

### Changed
- Enhanced main README with centered badges and quick navigation
- Updated skills catalog with category counts
- Improved formatting across all sections

---

## [1.2.0] - 2026-01-02

### Added

**New Sections**
- **Hooks Guide** - Complete documentation of Claude Code hooks
  - 8 hook types (PreToolUse, PostToolUse, UserPromptSubmit, etc.)
  - Exit code system and matcher patterns
  - 8 practical examples with code
- **Workflows Section** - Battle-tested automation patterns
  - Feature development workflow (Planning-First)
  - Code review workflow with checklists
  - Debugging workflow (5-Why technique)
  - Git operations and custom commands
- **Prompts Section** - Effective prompting guide
  - TCRO Framework (Task, Context, Requirements, Output)
  - Templates for features, bugs, reviews, refactoring
  - Anti-patterns to avoid

**New CLAUDE.md Templates**
- Go template - Web services, CLI tools, stdlib patterns
- Rust template - Async, error handling, ownership patterns
- React Native template - Mobile app development

### Changed
- Updated main README with new sections navigation
- Reorganized templates into categories (Web, Backend, Mobile)

---

## [1.1.0] - 2026-01-01

### Added

**Skills Catalog Expansion**
- Added Superpowers collection (obra) with 15+ professional skills
  - TDD, debugging, collaboration, planning skills
  - Commands: /superpowers:brainstorm, /superpowers:write-plan, /superpowers:execute-plan
- Added Scientific Skills section (125+ skills)
  - 26+ scientific database skills (PubMed, ChEMBL, UniProt, etc.)
  - 54+ Python package skills (RDKit, Scanpy, BioPython, etc.)
  - 15+ scientific integrations (Benchling, DNAnexus, etc.)
- Added more community skills with proper attribution

**MCP Servers Expansion**
- Added database servers section (MongoDB, Redis, Elasticsearch, Neon)
- Added DevOps & Cloud servers (Docker, Kubernetes, Terraform, AWS, GCP)
- Added Development tools (Sentry, Linear, Slack, Git, NPM)
- Added AI & Research servers (Perplexity, Exa, Arxiv, HuggingFace)
- Added Productivity servers (Google Drive, Calendar, Todoist, Obsidian)
- Added stats: 7,260+ MCP servers available, 8M+ downloads

**Plugins Expansion**
- Added Superpowers plugin with full documentation
- Added dx plugin (ykdojo)
- Added pr-review-toolkit with all 6 agents documented
- Added feature-dev, code-refactoring, ralph-wiggum plugins
- Added bmad (BMAD Method) project management plugin
- Added plugin marketplaces section with install commands
- Added hooks documentation with examples

**CLAUDE.md Templates**
- Added Full-Stack template (Next.js + API + Database)
- Added Monorepo template (Turborepo/pnpm workspaces)
- Added Data Science/ML template (notebooks, experiments, MLflow)
- Added Open Source template (contribution, releases, docs)

### Changed
- Restructured skills README with clear categories
- Enhanced MCP servers README with configuration examples
- Improved plugins README with comprehensive install guides

---

## [1.0.0] - 2026-01-01

### Added

**Repository Structure**
- README with comprehensive overview and navigation
- CONTRIBUTING guide for community submissions
- Issue templates for skill submissions and bug reports
- MIT License

**Skills Catalog**
- Official skills documentation (xlsx, pdf, docx, pptx, frontend-design, etc.)
- Community skills section with featured collections
- Skill creation guide

**MCP Servers**
- Top 10 essential MCP servers with setup examples
- Category-based organization
- Configuration snippets for each server

**Plugins**
- Featured plugin catalog (dx, commit-commands, pr-review-toolkit)
- Plugin marketplace links
- Plugin creation guide

**Tips & Tricks**
- 20+ curated tips organized by skill level
- Essential commands reference
- Best practices and common pitfalls

**CLAUDE.md Templates**
- React/Next.js template
- Python/FastAPI template
- Template usage guide

---

## How We Track Changes

Each day we research:
- Reddit (r/ClaudeAI, r/LocalLLaMA)
- GitHub (trending, releases, awesome lists)
- LinkedIn AI communities
- Twitter/X AI developers
- Dev.to, Medium, Substack

New discoveries are added to the appropriate section with a changelog entry.

---

## Version Format

- **Major (X.0.0)**: Significant restructuring or new sections
- **Minor (0.X.0)**: New categories or substantial additions
- **Patch (0.0.X)**: Individual skill/tool additions, fixes
