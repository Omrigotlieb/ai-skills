# Development Tool MCP Servers

MCP servers for software development workflows.

---

## GitHub MCP Server

**Essential for repository and workflow management.**

Prefer GitHub's maintained server entry and install guide rather than older reference-server examples.

### Configuration
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

### Capabilities
- **Repository Operations** - Clone, search, explore
- **Issues & PRs** - Create, update, review, merge
- **Actions** - View workflows, trigger runs
- **Releases** - Create and manage releases
- **Toolsets** - Limit access to repos, issues, pull requests, actions, and more to keep context focused

### Remote Option

If your MCP host supports remote HTTP servers, GitHub also hosts a remote MCP endpoint and publishes host-specific install guides for Claude and other clients.

### Typical PAT Scopes
```
repo            - Repository operations
read:packages   - Pull the Docker image when needed
read:org        - Organization and team access
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
      "command": "docker",
      "args": ["run", "-i", "--rm", "-e", "GITHUB_PERSONAL_ACCESS_TOKEN", "ghcr.io/github/github-mcp-server"],
      "env": { "GITHUB_PERSONAL_ACCESS_TOKEN": "${GITHUB_PAT}" }
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

- [GitHub MCP Server](https://github.com/mcp/io.github.github/github-mcp-server)
- [MCP Registry](https://github.com/modelcontextprotocol/registry)
- [Linear MCP](https://github.com/modelcontextprotocol/servers)
- [Sentry MCP](https://github.com/getsentry/mcp-server)
- [Official MCP Servers](https://github.com/modelcontextprotocol/servers)
