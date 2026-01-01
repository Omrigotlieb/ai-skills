# Productivity MCP Servers

MCP servers for personal productivity and team collaboration.

---

## Notion MCP Server

**All-in-one workspace integration.**

### Configuration
```json
{
  "notion": {
    "command": "npx",
    "args": ["-y", "@modelcontextprotocol/server-notion"],
    "env": {
      "NOTION_API_KEY": "${NOTION_API_KEY}"
    }
  }
}
```

### Capabilities
- **Pages** - Create, read, update pages
- **Databases** - Query and filter database views
- **Blocks** - Manipulate page content blocks
- **Search** - Full-text search across workspace

### Example Prompts
```
"Create a new page in my Projects database for 'Website Redesign'"
"Find all tasks assigned to me that are due this week"
"Update the status of 'Feature X' to 'In Progress'"
"Search for meeting notes about the Q4 planning"
```

---

## Obsidian MCP Server

**Knowledge base and note-taking.**

### Configuration
```json
{
  "obsidian": {
    "command": "npx",
    "args": ["-y", "@obsidian/mcp-server"],
    "env": {
      "OBSIDIAN_VAULT_PATH": "/path/to/vault"
    }
  }
}
```

### Capabilities
- Create and edit notes
- Link notes together
- Search content
- Manage tags

### Use Cases
- Personal knowledge management
- Research notes
- Project documentation
- Daily journaling

---

## Google Drive MCP Server

**Cloud file management.**

### Configuration
```json
{
  "google-drive": {
    "command": "npx",
    "args": ["-y", "@modelcontextprotocol/server-gdrive"],
    "env": {
      "GOOGLE_CLIENT_ID": "${GOOGLE_CLIENT_ID}",
      "GOOGLE_CLIENT_SECRET": "${GOOGLE_CLIENT_SECRET}"
    }
  }
}
```

### Capabilities
- Search files
- Read document content
- Create and update files
- Manage permissions

---

## Google Calendar MCP Server

**Calendar management.**

### Configuration
```json
{
  "google-calendar": {
    "command": "npx",
    "args": ["-y", "@modelcontextprotocol/server-google-calendar"],
    "env": {
      "GOOGLE_CREDENTIALS": "${GOOGLE_CREDENTIALS}"
    }
  }
}
```

### Capabilities
- View calendar events
- Create new events
- Find free time slots
- Manage attendees

### Example Prompts
```
"What meetings do I have tomorrow?"
"Schedule a 30-min call with Sarah next week"
"Find a 1-hour slot for team sync between Monday and Wednesday"
```

---

## Todoist MCP Server

**Task management.**

### Configuration
```json
{
  "todoist": {
    "command": "npx",
    "args": ["-y", "@modelcontextprotocol/server-todoist"],
    "env": {
      "TODOIST_API_TOKEN": "${TODOIST_API_TOKEN}"
    }
  }
}
```

### Capabilities
- Create and complete tasks
- Manage projects
- Set due dates and priorities
- Organize with labels

---

## Raycast MCP Server

**macOS productivity launcher.**

### Configuration
```json
{
  "raycast": {
    "command": "npx",
    "args": ["-y", "@raycast/mcp-server"]
  }
}
```

### Capabilities
- Quick actions
- Clipboard history
- Window management
- Custom scripts

---

## Email Integration

### Gmail MCP
```json
{
  "gmail": {
    "command": "npx",
    "args": ["-y", "@modelcontextprotocol/server-gmail"],
    "env": {
      "GOOGLE_CREDENTIALS": "${GOOGLE_CREDENTIALS}"
    }
  }
}
```

### Capabilities
- Read emails
- Send emails
- Search inbox
- Manage labels

---

## Time Tracking

### Toggl MCP
```json
{
  "toggl": {
    "command": "npx",
    "args": ["-y", "@toggl/mcp-server"],
    "env": {
      "TOGGL_API_TOKEN": "${TOGGL_API_TOKEN}"
    }
  }
}
```

### Capabilities
- Start/stop time tracking
- View time entries
- Generate reports
- Manage projects

---

## Combined Productivity Stack

Example configuration for a complete productivity workflow:

```json
{
  "mcpServers": {
    "notion": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-notion"],
      "env": { "NOTION_API_KEY": "${NOTION_API_KEY}" }
    },
    "calendar": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-google-calendar"],
      "env": { "GOOGLE_CREDENTIALS": "${GOOGLE_CREDENTIALS}" }
    },
    "todoist": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-todoist"],
      "env": { "TODOIST_API_TOKEN": "${TODOIST_API_TOKEN}" }
    }
  }
}
```

### Workflow Examples
```
"Create a Notion page for today's meeting notes and add a calendar reminder for follow-up"
"Add all my overdue Todoist tasks to my Notion weekly review"
"What's on my calendar today and what tasks should I prioritize?"
```

---

## Resources

- [Notion MCP](https://github.com/modelcontextprotocol/servers)
- [Obsidian MCP](https://github.com/obsidianmd/mcp-server)
- [Todoist API](https://developer.todoist.com/)
- [Google Workspace APIs](https://developers.google.com/workspace)
