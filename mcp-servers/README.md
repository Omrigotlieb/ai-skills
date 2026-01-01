# MCP Servers Catalog

Model Context Protocol (MCP) servers extend Claude Code with external tools and data sources. They provide structured interfaces for Claude to interact with databases, APIs, file systems, and more.

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
**Category:** Git/VCS | **Source:** [modelcontextprotocol/servers](https://github.com/modelcontextprotocol/servers)

Connect Claude to GitHub's REST API for repository management.

**Capabilities:**
- Read/manage issues and PRs
- Trigger CI/CD workflows
- Analyze commits and branches
- Repository search

```json
{
  "github": {
    "command": "npx",
    "args": ["-y", "@modelcontextprotocol/server-github"],
    "env": {
      "GITHUB_TOKEN": "your-token"
    }
  }
}
```

---

### 2. Context7 MCP
**Category:** Documentation | **Source:** [context7/mcp](https://github.com/context7/mcp)

Real-time library documentation fetching.

**Capabilities:**
- Up-to-date API docs
- Version-specific examples
- Code snippet generation

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

Secure local file operations.

**Capabilities:**
- Read/write files
- Directory management
- File search
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

### 4. PostgreSQL MCP Server
**Category:** Database | **Source:** [modelcontextprotocol/servers](https://github.com/modelcontextprotocol/servers)

Natural language database queries.

**Capabilities:**
- SQL query generation
- Schema exploration
- Data analysis
- Query optimization

```json
{
  "postgres": {
    "command": "npx",
    "args": ["-y", "@modelcontextprotocol/server-postgres"],
    "env": {
      "DATABASE_URL": "postgresql://..."
    }
  }
}
```

---

### 5. Puppeteer MCP Server
**Category:** Automation | **Source:** [modelcontextprotocol/servers](https://github.com/modelcontextprotocol/servers)

Browser automation and testing.

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

### 6. Sequential Thinking MCP
**Category:** Reasoning | **Source:** [modelcontextprotocol/servers](https://github.com/modelcontextprotocol/servers)

Structured problem-solving process.

**Capabilities:**
- Step-by-step reasoning
- Problem decomposition
- Reflection and revision

---

### 7. Brave Search MCP
**Category:** Search | **Source:** [modelcontextprotocol/servers](https://github.com/modelcontextprotocol/servers)

Privacy-first web search.

**Capabilities:**
- Web search
- News search
- Current information access

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

### 8. Notion MCP
**Category:** Productivity | **Source:** [modelcontextprotocol/servers](https://github.com/modelcontextprotocol/servers)

Notion workspace integration.

**Capabilities:**
- Page creation/editing
- Database queries
- Content search

---

### 9. Figma MCP
**Category:** Design | **Source:** [modelcontextprotocol/servers](https://github.com/modelcontextprotocol/servers)

Design-to-code workflow.

**Capabilities:**
- Read Figma designs
- Extract design tokens
- Generate components

---

### 10. Zapier MCP
**Category:** Integration | **Source:** [zapier/mcp](https://github.com/zapier/mcp)

Connect to 5000+ applications.

**Capabilities:**
- Cross-app automation
- Workflow triggers
- Data synchronization

---

## By Category

- [Database Servers](database.md) - PostgreSQL, MySQL, MongoDB, SQLite
- [Search & Research](search.md) - Brave, Google, Perplexity
- [Automation](automation.md) - Puppeteer, Playwright, Browser tools
- [Productivity](productivity.md) - Notion, Slack, Linear, GitHub
- [Development](development.md) - Sentry, Docker, Kubernetes

---

## Best Practices

### Performance
- **Limit MCP count**: 2-3 servers for your primary tasks
- **Monitor startup**: Too many MCPs slow down Claude Code

### Security
- **Token management**: Use environment variables, never commit tokens
- **Path restrictions**: Limit filesystem access to specific directories
- **Network boundaries**: Be cautious with servers that access external APIs

### Debugging
```bash
# Check MCP status
/mcp

# View MCP details in context
/context
```

---

## Resources

- [MCP Specification](https://modelcontextprotocol.io)
- [Official MCP Servers](https://github.com/modelcontextprotocol/servers)
- [awesome-mcp-servers](https://github.com/punkpeye/awesome-mcp-servers)
- [MCPcat Directory](https://mcpcat.io)
