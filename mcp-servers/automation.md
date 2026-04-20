# Automation MCP Servers

MCP servers for browser automation, testing, and workflow orchestration.

---

## Puppeteer MCP Server

**Headless browser automation.**

### Configuration
```json
{
  "puppeteer": {
    "command": "npx",
    "args": ["-y", "@modelcontextprotocol/server-puppeteer"]
  }
}
```

### Capabilities
- **Navigation** - Visit URLs, click, type
- **Screenshots** - Capture full pages or elements
- **Scraping** - Extract data from websites
- **Testing** - Automate E2E flows

### Example Prompts
```
"Take a screenshot of the homepage and identify any layout issues"
"Scrape product prices from this e-commerce page"
"Fill out the contact form with test data"
"Navigate through the checkout flow and report any errors"
```

---

## Playwright MCP Server

**Maintained browser automation for testing, scraping, and UI debugging.**

Use Microsoft's [Playwright MCP server](https://github.com/microsoft/playwright-mcp) when an agent needs persistent browser state, iterative page inspection, console/network debugging, or structured page interaction through accessibility snapshots. For high-volume coding-agent loops, prefer the Playwright CLI plus a skill or project command when concise command output is enough.

### Configuration
```json
{
  "playwright": {
    "command": "npx",
    "args": ["-y", "@playwright/mcp@latest"]
  }
}
```

### Capabilities
- Navigate pages, click elements, fill forms, upload files, and manage dialogs
- Inspect console messages, network requests, tabs, and page state
- Capture screenshots and PDFs for visual evidence
- Run with persistent profiles for logged-in workflows or isolated profiles for tests

### Useful Options
- `--isolated` starts each session with a fresh profile.
- `--storage-state path/to/storage.json` loads a prepared login/session state.
- `--allowed-origins` and `--blocked-origins` narrow what the browser can request, but they are not a security boundary.

### Claude Code Install
```bash
claude mcp add playwright npx @playwright/mcp@latest
```

---

## Browserbase MCP Server

**Cloud browser automation.**

### Configuration
```json
{
  "browserbase": {
    "command": "npx",
    "args": ["-y", "@browserbase/mcp-server"],
    "env": {
      "BROWSERBASE_API_KEY": "${BROWSERBASE_API_KEY}"
    }
  }
}
```

### Capabilities
- Managed browser infrastructure
- Session recording
- CAPTCHA handling
- Proxy rotation

---

## Zapier MCP Server

**Connect 5000+ applications.**

### Configuration
```json
{
  "zapier": {
    "command": "npx",
    "args": ["-y", "@zapier/mcp-server"],
    "env": {
      "ZAPIER_API_KEY": "${ZAPIER_API_KEY}"
    }
  }
}
```

### Capabilities
- Trigger Zaps
- Access connected apps
- Multi-step workflows
- Custom integrations

### Example Workflows
```
"When I create a GitHub issue, create a Notion task and Slack message"
"Send a weekly summary of completed tasks to my email"
"Sync new contacts from Salesforce to Mailchimp"
```

---

## n8n MCP Server

**Self-hosted workflow automation.**

### Configuration
```json
{
  "n8n": {
    "command": "npx",
    "args": ["-y", "@n8n/mcp-server"],
    "env": {
      "N8N_API_URL": "http://localhost:5678",
      "N8N_API_KEY": "${N8N_API_KEY}"
    }
  }
}
```

### Capabilities
- Self-hosted control
- Custom nodes
- Data transformation
- Error handling

---

## Make (Integromat) MCP Server

**Visual workflow builder.**

### Configuration
```json
{
  "make": {
    "command": "npx",
    "args": ["-y", "@make/mcp-server"],
    "env": {
      "MAKE_API_TOKEN": "${MAKE_API_TOKEN}"
    }
  }
}
```

### Capabilities
- Visual scenario builder
- App connections
- Data routing
- Scheduling

---

## Shell/System Automation

### Filesystem MCP
```json
{
  "filesystem": {
    "command": "npx",
    "args": ["-y", "@modelcontextprotocol/server-filesystem", "./workspace"]
  }
}
```

### Capabilities
- File operations (read, write, delete)
- Directory management
- Pattern matching (glob)
- Permission management

---

## Docker MCP Server

**Container automation.**

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
- List containers/images
- Start/stop containers
- Build images
- View logs

---

## CI/CD Automation

### GitHub Actions via GitHub MCP
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

### Workflow Operations
- Trigger workflow runs
- View run status
- Download artifacts
- Check job logs

---

## Automation Patterns

### Web Scraping Workflow
```
1. Use Puppeteer to navigate to page
2. Extract structured data
3. Save to database via Database MCP
4. Notify via Slack MCP
```

### Testing Workflow
```
1. Build project
2. Start test server
3. Run Playwright tests
4. Report results to GitHub PR
```

### Data Pipeline
```
1. Fetch data from API (HTTP MCP)
2. Transform with code
3. Store in database (PostgreSQL MCP)
4. Notify completion (Slack MCP)
```

---

## Combined Automation Stack

```json
{
  "mcpServers": {
    "puppeteer": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-puppeteer"]
    },
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "./data"]
    },
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": { "GITHUB_TOKEN": "${GITHUB_TOKEN}" }
    }
  }
}
```

---

## Security Considerations

### Sandboxing
- Use containers for untrusted automation
- Limit filesystem access paths
- Restrict network access

### Credentials
- Never hardcode credentials
- Use environment variables
- Rotate API keys regularly

### Audit
- Log all automated actions
- Monitor for unusual patterns
- Review automation scripts

---

## Resources

- [Puppeteer Docs](https://pptr.dev/)
- [Playwright MCP](https://github.com/microsoft/playwright-mcp)
- [Playwright plugin for Claude](https://claude.com/plugins/playwright)
- [Playwright Docs](https://playwright.dev/)
- [Zapier Developer](https://developer.zapier.com/)
- [n8n Docs](https://docs.n8n.io/)
