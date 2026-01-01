# Development Tool MCP Servers

MCP servers for software development workflows.

---

## GitHub MCP Server

**Essential for repository and workflow management.**

### Configuration
```json
{
  "github": {
    "command": "npx",
    "args": ["-y", "@modelcontextprotocol/server-github"],
    "env": {
      "GITHUB_TOKEN": "${GITHUB_TOKEN}"
    }
  }
}
```

### Capabilities
- **Repository Operations** - Clone, search, explore
- **Issues & PRs** - Create, update, review, merge
- **Actions** - View workflows, trigger runs
- **Releases** - Create and manage releases

### Required Scopes
```
repo        - Full repository access
workflow    - GitHub Actions access
read:org    - Organization info (optional)
```

### Example Prompts
```
"Create a PR from feature-branch to main with a summary of changes"
"Show me the failing CI jobs for PR #123"
"List all open issues labeled 'bug' created this week"
"Create a release v1.2.0 with generated changelog"
```

---

## Git MCP Server

**For local git operations.**

### Configuration
```json
{
  "git": {
    "command": "npx",
    "args": ["-y", "@modelcontextprotocol/server-git", "./"]
  }
}
```

### Capabilities
- View git status, diff, log
- Create commits
- Manage branches
- Resolve conflicts

---

## Linear MCP Server

**Project management integration.**

### Configuration
```json
{
  "linear": {
    "command": "npx",
    "args": ["-y", "@modelcontextprotocol/server-linear"],
    "env": {
      "LINEAR_API_KEY": "${LINEAR_API_KEY}"
    }
  }
}
```

### Capabilities
- Create and update issues
- Manage projects and cycles
- Search and filter tickets
- Link to PRs

---

## Sentry MCP Server

**Error tracking and monitoring.**

### Configuration
```json
{
  "sentry": {
    "command": "npx",
    "args": ["-y", "@sentry/mcp-server"],
    "env": {
      "SENTRY_AUTH_TOKEN": "${SENTRY_AUTH_TOKEN}",
      "SENTRY_ORG": "your-org"
    }
  }
}
```

### Capabilities
- View and analyze errors
- Search issues
- Get error trends
- Investigate stack traces

### Example Prompts
```
"Show me the top 5 errors in the last 24 hours"
"Investigate the root cause of issue SENTRY-123"
"What errors are most common for users on mobile?"
```

---

## Slack MCP Server

**Team communication integration.**

### Configuration
```json
{
  "slack": {
    "command": "npx",
    "args": ["-y", "@modelcontextprotocol/server-slack"],
    "env": {
      "SLACK_TOKEN": "${SLACK_BOT_TOKEN}"
    }
  }
}
```

### Capabilities
- Send messages to channels
- Read channel history
- Search messages
- Manage threads

---

## NPM MCP Server

**Package management and discovery.**

### Configuration
```json
{
  "npm": {
    "command": "npx",
    "args": ["-y", "@modelcontextprotocol/server-npm"]
  }
}
```

### Capabilities
- Search packages
- View package info
- Check dependencies
- Compare versions

---

## Docker MCP Server

**Container management.**

### Configuration
```json
{
  "docker": {
    "command": "npx",
    "args": ["-y", "@modelcontextprotocol/server-docker"]
  }
}
```

### Capabilities
- List containers and images
- Start/stop containers
- View logs
- Inspect configurations

---

## VS Code/Cursor Integration MCP

**IDE-specific features.**

### Capabilities
- Read open files
- Navigate workspace
- Access terminal output
- Integrate with extensions

---

## CI/CD Integration

### GitHub Actions
```yaml
# .github/workflows/mcp-check.yml
name: MCP Validation
on: [push]
jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Validate MCP Config
        run: npx @modelcontextprotocol/cli validate .mcp.json
```

---

## Development Workflow Example

Combine multiple MCP servers for a complete workflow:

```json
{
  "mcpServers": {
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": { "GITHUB_TOKEN": "${GITHUB_TOKEN}" }
    },
    "linear": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-linear"],
      "env": { "LINEAR_API_KEY": "${LINEAR_API_KEY}" }
    },
    "sentry": {
      "command": "npx",
      "args": ["-y", "@sentry/mcp-server"],
      "env": { "SENTRY_AUTH_TOKEN": "${SENTRY_AUTH_TOKEN}" }
    }
  }
}
```

### Workflow Prompts
```
"Create a Linear issue for the error in Sentry #123, then create a PR to fix it"
"What Sentry errors are related to the code changed in PR #456?"
"Update the Linear ticket with the PR link after creating it"
```

---

## Resources

- [GitHub MCP](https://github.com/modelcontextprotocol/servers/tree/main/src/github)
- [Linear MCP](https://github.com/modelcontextprotocol/servers)
- [Sentry MCP](https://github.com/getsentry/mcp-server)
- [Official MCP Servers](https://github.com/modelcontextprotocol/servers)
