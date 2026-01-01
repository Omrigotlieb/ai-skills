# Documentation Skills for Claude Code

Skills for generating, maintaining, and organizing documentation.

---

## README Generator Skill

```markdown
---
name: readme-generator
description: Generate comprehensive README files
---

# README Generator

## When to Use
- New projects without documentation
- Outdated README files
- Open source project setup

## Sections Generated
1. **Title & Badges** - Project name, shields.io badges
2. **Description** - What the project does
3. **Features** - Key capabilities
4. **Installation** - Step-by-step setup
5. **Usage** - Code examples
6. **Configuration** - Options and environment variables
7. **API Reference** - Function/endpoint docs
8. **Contributing** - How to contribute
9. **License** - License information

## Example
"Generate a comprehensive README for this Node.js API project"
```

---

## JSDoc/TSDoc Generator Skill

```markdown
---
name: jsdoc-generator
description: Generate TypeScript/JavaScript documentation
---

# JSDoc/TSDoc Generator

## Capabilities
- Generate JSDoc comments
- Type annotations
- Parameter descriptions
- Return value documentation
- Example code blocks

## Example Output
/**
 * Authenticates a user with the given credentials
 * @param {string} email - The user's email address
 * @param {string} password - The user's password
 * @returns {Promise<AuthResult>} Authentication result with token
 * @throws {AuthenticationError} If credentials are invalid
 * @example
 * const result = await authenticate('user@example.com', 'password');
 * console.log(result.token);
 */
```

---

## API Documentation Skill

```markdown
---
name: api-documenter
description: Generate OpenAPI specs and API docs
---

# API Documentation

## Capabilities
- Extract endpoints from code
- Generate OpenAPI 3.0 specs
- Create request/response examples
- Document authentication methods

## Output Formats
- OpenAPI 3.0 YAML/JSON
- Markdown documentation
- Postman collections
- Swagger UI ready

## Example
"Generate OpenAPI spec for all REST endpoints in src/routes/"
```

---

## Changelog Generator Skill

```markdown
---
name: changelog-generator
description: Generate and maintain changelog
---

# Changelog Generator

## Format
Based on [Keep a Changelog](https://keepachangelog.com/):

- **Added** - New features
- **Changed** - Changes in existing functionality
- **Deprecated** - Soon-to-be removed features
- **Removed** - Removed features
- **Fixed** - Bug fixes
- **Security** - Vulnerability fixes

## Capabilities
- Parse git commits
- Group by category
- Link to issues/PRs
- Follow semver

## Example
"Generate changelog entries from commits since last release"
```

---

## Architecture Documentation Skill

```markdown
---
name: architecture-docs
description: Document system architecture
---

# Architecture Documentation

## Diagrams Generated
- System context diagram
- Container diagram
- Component diagram
- Sequence diagrams

## Formats
- Mermaid (markdown-compatible)
- PlantUML
- ASCII diagrams
- Excalidraw

## C4 Model Support
1. **Context** - System in environment
2. **Container** - High-level tech choices
3. **Component** - Major building blocks
4. **Code** - Class/function level

## Example
"Document the authentication flow as a sequence diagram"
```

---

## Code Comments Skill

```markdown
---
name: code-comments
description: Add meaningful code comments
---

# Code Comments

## When to Comment
- Complex algorithms
- Non-obvious business logic
- Workarounds and their reasons
- Performance optimizations
- Security considerations

## When NOT to Comment
- Self-explanatory code
- Trivial operations
- What the code does (obvious from reading)

## Best Practices
- Explain WHY, not WHAT
- Keep comments up to date
- Use TODO/FIXME/HACK markers
- Reference issue numbers
```

---

## Documentation Patterns

### Decision Records (ADR)

```markdown
# ADR-001: Use PostgreSQL for primary database

## Status
Accepted

## Context
We need a relational database for our application.

## Decision
We will use PostgreSQL 15.

## Consequences
- Need PostgreSQL expertise on team
- Complex queries supported
- ACID compliance guaranteed
```

### Runbooks

```markdown
# Runbook: Deploy to Production

## Prerequisites
- Access to production cluster
- Deployment credentials

## Steps
1. Verify staging tests passed
2. Create release tag
3. Run deployment script
4. Verify health checks
5. Monitor for 15 minutes

## Rollback
1. Run rollback script
2. Verify previous version active
```

---

## Documentation Commands

### docs.md
```markdown
Generate documentation for recent changes:
1. Identify modified files
2. Update relevant docs
3. Add JSDoc where missing
4. Update README if needed
```

### adr.md
```markdown
Create Architecture Decision Record:
1. Gather context
2. Document decision
3. List alternatives considered
4. Record consequences
```

---

## MCP Servers for Documentation

| Server | Purpose |
|--------|---------|
| **Notion MCP** | Wiki documentation |
| **Confluence MCP** | Enterprise docs |
| **GitHub MCP** | README, wiki |
| **Swagger MCP** | API documentation |

---

## Resources

- [Diátaxis Framework](https://diataxis.fr/) - Documentation system
- [Write the Docs](https://www.writethedocs.org/) - Community
- [The Documentation System](https://documentation.divio.com/) - Four types of docs
- [OpenAPI Spec](https://spec.openapis.org/oas/latest.html)
