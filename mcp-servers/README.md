# MCP Servers Catalog

<div align="center">

[![Official Registry](https://img.shields.io/badge/registry-official-green)](https://github.com/modelcontextprotocol/registry)
[![GitHub MCP](https://img.shields.io/badge/github-mcp%20by%20GitHub-black)](https://github.com/mcp/io.github.github/github-mcp-server)
[![Official](https://img.shields.io/badge/official-25%2B-purple)](https://github.com/modelcontextprotocol/servers)

[**Database**](database.md) | [**Development**](development.md) | [**Productivity**](productivity.md) | [**Search**](search.md) | [**Automation**](automation.md)

</div>

Model Context Protocol (MCP) servers extend Claude Code with external tools and data sources. They provide structured interfaces for Claude to interact with databases, APIs, file systems, and more.

> **Use the registry first:** start with the [official MCP Registry](https://github.com/modelcontextprotocol/registry), then verify the source repo and install docs before adding a server to your setup.

## Discovery Workflow

1. Search the [official MCP Registry](https://github.com/modelcontextprotocol/registry) for maintained servers and current install metadata.
2. Prefer official vendor-published servers when they exist, especially for GitHub, Notion, Sentry, and other sensitive integrations.
3. Use community awesome lists to discover options, then confirm the canonical repo before documenting or installing anything.

## Quick Start

Add an MCP server to your `.mcp.json`:

```json
{
  "mcpServers": {
    "server-name": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-name"]
    }
  }
}
```

---

## Essential MCP Servers (Top 10)

### 1. GitHub MCP Server
**Category:** Git/VCS | **Source:** [GitHub MCP Server](https://github.com/mcp/io.github.github/github-mcp-server)

Connect Claude to GitHub's REST API for repository management.

**Capabilities:**
- Read/manage issues and PRs
- Trigger CI/CD workflows
- Analyze commits and branches
- Repository search and stats
- Limit available tools with toolsets to reduce noise and token usage

```json
{
  "github": {
    "command": "docker",
    "args": ["run", "-i", "--rm", "-e", "GITHUB_PERSONAL_ACCESS_TOKEN", "ghcr.io/github/github-mcp-server"],
    "env": {
      "GITHUB_PERSONAL_ACCESS_TOKEN": "${GITHUB_PAT}"
    }
  }
}
```

If your MCP host supports remote HTTP servers, GitHub also publishes a hosted MCP endpoint and host-specific install guides.

---

### 2. Context7 MCP
**Category:** Documentation | **Source:** [context7/mcp](https://github.com/context7/mcp)

Real-time library documentation fetching - never get outdated API examples again.

**Capabilities:**
- Up-to-date API docs for any library
- Version-specific code examples
- Auto-detects library versions

```json
{
  "context7": {
    "command": "npx",
    "args": ["-y", "@context7/mcp-server"]
  }
}
```

---

### 3. Filesystem MCP Server
**Category:** Core | **Source:** [modelcontextprotocol/servers](https://github.com/modelcontextprotocol/servers)

Secure local file operations with granular permissions.

**Capabilities:**
- Read/write files
- Directory management
- File search with patterns
- Permission controls

```json
{
  "filesystem": {
    "command": "npx",
    "args": ["-y", "@modelcontextprotocol/server-filesystem", "/allowed/path"]
  }
}
```

---

### 4. Sequential Thinking MCP
**Category:** Reasoning | **Source:** [modelcontextprotocol/servers](https://github.com/modelcontextprotocol/servers)

Structured problem-solving that mirrors human cognitive patterns.

**Capabilities:**
- Step-by-step reasoning
- Problem decomposition
- Reflection and revision
- Complex analysis

---

### 5. Puppeteer MCP Server
**Category:** Automation | **Source:** [modelcontextprotocol/servers](https://github.com/modelcontextprotocol/servers)

Browser automation for testing and scraping.

**Capabilities:**
- Web scraping
- Screenshot capture
- Form automation
- E2E testing support

```json
{
  "puppeteer": {
    "command": "npx",
    "args": ["-y", "@modelcontextprotocol/server-puppeteer"]
  }
}
```

---

### 6. Brave Search MCP
**Category:** Search | **Source:** [modelcontextprotocol/servers](https://github.com/modelcontextprotocol/servers)

Privacy-first web search with high-quality results.

**Capabilities:**
- Web search
- News search
- Current information access
- No tracking

```json
{
  "brave-search": {
    "command": "npx",
    "args": ["-y", "@modelcontextprotocol/server-brave-search"],
    "env": {
      "BRAVE_API_KEY": "your-key"
    }
  }
}
```

---

### 7. Memory MCP Server
**Category:** Context | **Source:** [modelcontextprotocol/servers](https://github.com/modelcontextprotocol/servers)

Persistent memory across conversations.

**Capabilities:**
- Store key information
- Retrieve context
- Build knowledge base

---

### 8. Notion MCP
**Category:** Productivity | **Source:** [Notion MCP docs](https://developers.notion.com/docs/mcp)

Notion workspace integration with a hosted OAuth flow for most users.

**Capabilities:**
- Page creation/editing
- Database queries
- Content search

---

### 9. Figma MCP
**Category:** Design | **Source:** [modelcontextprotocol/servers](https://github.com/modelcontextprotocol/servers)

Design-to-code workflow integration.

**Capabilities:**
- Read Figma designs
- Extract design tokens
- Generate components

---

### 10. Zapier MCP
**Category:** Integration | **Source:** [zapier/mcp](https://github.com/zapier/mcp)

Connect to 5000+ applications through a single MCP.

**Capabilities:**
- Cross-app automation
- Workflow triggers
- Data synchronization

---

## Database Servers

### SQL Databases

| Server | Database | Features | Link |
|--------|----------|----------|------|
| **PostgreSQL MCP** | PostgreSQL | Natural language queries, schema exploration, optimization | [Official](https://github.com/modelcontextprotocol/servers) |
| **MySQL MCP** | MySQL | Query generation, data analysis | Community |
| **SQLite MCP** | SQLite | Local database operations | [Official](https://github.com/modelcontextprotocol/servers) |
| **Neon MCP** | Neon PostgreSQL | Serverless Postgres integration | [Neon](https://github.com/neondatabase/mcp-server-neon) |

### NoSQL Databases

| Server | Database | Features | Link |
|--------|----------|----------|------|
| **MongoDB MCP** | MongoDB | Atlas/Community/Enterprise support, aggregation pipelines | [Official](https://github.com/mongodb-js/mongodb-mcp-server) |
| **Redis MCP** | Redis | Data store operations, search | Official |
| **Elasticsearch MCP** | Elasticsearch | Natural language search, index management | [Elastic](https://github.com/elastic/mcp-server-elasticsearch) |

### Multi-Database

| Server | Description | Databases Supported |
|--------|-------------|---------------------|
| **Database MCP** | Unified interface via genai-toolbox | 40+ databases |
| **Polyglot DB MCP** | Cross-database queries | PostgreSQL, MongoDB, Neo4j, Elasticsearch, Redis, 15+ more |

---

## DevOps & Cloud Servers

| Server | Category | Description |
|--------|----------|-------------|
| **Docker MCP** | Containers | Container management and orchestration |
| **Kubernetes MCP** | Orchestration | K8s cluster operations |
| **Terraform MCP** | IaC | Infrastructure provisioning |
| **AWS MCP** | Cloud | AWS service interactions |
| **GCP MCP** | Cloud | Google Cloud operations |
| **Cloudflare MCP** | Edge | Workers, KV, R2 management |

---

## Development Tools

| Server | Category | Description |
|--------|----------|-------------|
| **Sentry MCP** | Error Tracking | Issue tracking, error analysis |
| **Linear MCP** | Project Management | Issue and project management |
| **Slack MCP** | Communication | Team messaging integration |
| **Git MCP** | Version Control | Local git operations |
| **NPM MCP** | Package Management | Package info and search |

---

## AI & Research

| Server | Category | Description |
|--------|----------|-------------|
| **Perplexity MCP** | Search | AI-powered research |
| **Exa MCP** | Search | Neural search engine |
| **Arxiv MCP** | Research | Academic paper search |
| **HuggingFace MCP** | ML | Model and dataset access |

---

## Productivity

| Server | Category | Description |
|--------|----------|-------------|
| **Google Drive MCP** | Storage | File management |
| **Google Calendar MCP** | Calendar | Event management |
| **Todoist AI / MCP** | Tasks | Task management with a maintained hosted endpoint |
| **Obsidian MCP** | Notes | Knowledge base integration |
| **Raycast MCP** | Launcher | Raycast integration |

---

## Best Practices

### Performance Tips
```bash
# Check MCP status
/mcp

# View MCP context overhead
/context
```

- **Limit to 2-3 MCPs** for primary tasks
- **Too many MCPs** slow startup significantly
- **Monitor overhead** with `/context`

### Security
- **Environment variables** for tokens (never commit)
- **Path restrictions** for filesystem access
- **Network boundaries** for external API servers

### Configuration Example
```json
{
  "mcpServers": {
    "github": {
      "command": "docker",
      "args": ["run", "-i", "--rm", "-e", "GITHUB_PERSONAL_ACCESS_TOKEN", "ghcr.io/github/github-mcp-server"],
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "${GITHUB_PAT}"
      }
    },
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "./src"]
    },
    "context7": {
      "command": "npx",
      "args": ["-y", "@context7/mcp-server"]
    }
  }
}
```

---

## Resources

### Official Discovery
- [MCP Registry](https://github.com/modelcontextprotocol/registry) - Official registry service for MCP servers
- [GitHub MCP Server](https://github.com/mcp/io.github.github/github-mcp-server) - GitHub-maintained server entry with install guides
- [Official MCP Servers](https://github.com/modelcontextprotocol/servers) - Reference servers from the MCP organization

### Awesome Lists
- [punkpeye/awesome-mcp-servers](https://github.com/punkpeye/awesome-mcp-servers) - Main curated list
- [wong2/awesome-mcp-servers](https://github.com/wong2/awesome-mcp-servers) - With official integrations
- [TensorBlock/awesome-mcp-servers](https://github.com/TensorBlock/awesome-mcp-servers) - 7,260+ servers cataloged
- [rohitg00/awesome-devops-mcp-servers](https://github.com/rohitg00/awesome-devops-mcp-servers) - DevOps focused

### Directories
- [MCPcat](https://mcpcat.io) - Searchable MCP directory
- [Glama MCP](https://glama.ai/mcp/servers) - MCP server browser

### Official
- [MCP Specification](https://modelcontextprotocol.io)
- [MCP TypeScript SDK](https://github.com/modelcontextprotocol/typescript-sdk)
- [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk)
