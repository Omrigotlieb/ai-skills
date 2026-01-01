# Search & Research MCP Servers

MCP servers for web search, research, and information retrieval.

---

## Brave Search MCP Server

**Privacy-first web search.**

### Configuration
```json
{
  "brave-search": {
    "command": "npx",
    "args": ["-y", "@modelcontextprotocol/server-brave-search"],
    "env": {
      "BRAVE_API_KEY": "${BRAVE_API_KEY}"
    }
  }
}
```

### Get API Key
1. Go to [brave.com/search/api](https://brave.com/search/api)
2. Sign up for free tier (2000 queries/month)
3. Create API key

### Capabilities
- Web search with no tracking
- News search
- Image search
- Localized results

### Example Prompts
```
"Search for recent articles about Claude Code"
"Find the latest news about AI regulations in Europe"
"What are the top resources for learning Rust in 2025?"
```

---

## Perplexity MCP Server

**AI-powered research assistant.**

### Configuration
```json
{
  "perplexity": {
    "command": "npx",
    "args": ["-y", "@perplexity/mcp-server"],
    "env": {
      "PERPLEXITY_API_KEY": "${PERPLEXITY_API_KEY}"
    }
  }
}
```

### Capabilities
- Deep research queries
- Source citations
- Multi-step reasoning
- Up-to-date information

### Best For
- Complex research questions
- Comparative analysis
- Technical deep dives

---

## Exa MCP Server

**Neural search engine.**

### Configuration
```json
{
  "exa": {
    "command": "npx",
    "args": ["-y", "@exa/mcp-server"],
    "env": {
      "EXA_API_KEY": "${EXA_API_KEY}"
    }
  }
}
```

### Capabilities
- Semantic search
- Find similar content
- Domain filtering
- Content extraction

### Use Cases
- Finding relevant documentation
- Competitor research
- Content discovery

---

## Arxiv MCP Server

**Academic paper search.**

### Configuration
```json
{
  "arxiv": {
    "command": "npx",
    "args": ["-y", "@modelcontextprotocol/server-arxiv"]
  }
}
```

### Capabilities
- Search by topic, author, date
- Download papers
- Extract abstracts
- Category filtering

### Example Prompts
```
"Find recent papers on transformer architectures"
"Search for papers by Ilya Sutskever from 2024"
"What are the latest publications on constitutional AI?"
```

---

## Wikipedia MCP Server

**Encyclopedia access.**

### Configuration
```json
{
  "wikipedia": {
    "command": "npx",
    "args": ["-y", "@modelcontextprotocol/server-wikipedia"]
  }
}
```

### Capabilities
- Article search
- Content extraction
- Summary generation
- Cross-language support

---

## Tavily MCP Server

**Search API optimized for AI.**

### Configuration
```json
{
  "tavily": {
    "command": "npx",
    "args": ["-y", "@tavily/mcp-server"],
    "env": {
      "TAVILY_API_KEY": "${TAVILY_API_KEY}"
    }
  }
}
```

### Capabilities
- AI-optimized search results
- Structured answers
- Source verification
- Topic deep-dives

---

## Documentation Servers

### Context7 MCP
**Real-time library documentation.**

```json
{
  "context7": {
    "command": "npx",
    "args": ["-y", "@context7/mcp-server"]
  }
}
```

Up-to-date docs for any programming library.

### DevDocs MCP
**Unified documentation browser.**

```json
{
  "devdocs": {
    "command": "npx",
    "args": ["-y", "@devdocs/mcp-server"]
  }
}
```

Access to 400+ programming documentation sets.

---

## HuggingFace MCP Server

**ML model and dataset search.**

### Configuration
```json
{
  "huggingface": {
    "command": "npx",
    "args": ["-y", "@huggingface/mcp-server"],
    "env": {
      "HF_TOKEN": "${HF_TOKEN}"
    }
  }
}
```

### Capabilities
- Search models
- Browse datasets
- Find model cards
- Check downloads/popularity

---

## Research Workflow

Combine search servers for comprehensive research:

```json
{
  "mcpServers": {
    "brave-search": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-brave-search"],
      "env": { "BRAVE_API_KEY": "${BRAVE_API_KEY}" }
    },
    "arxiv": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-arxiv"]
    },
    "context7": {
      "command": "npx",
      "args": ["-y", "@context7/mcp-server"]
    }
  }
}
```

### Research Prompts
```
"Research the current state of RAG systems - find web articles, academic papers, and documentation"
"Compare the top 5 vector databases - search for benchmarks and user reviews"
"Find the latest best practices for prompt engineering from both academic and industry sources"
```

---

## Search Tips

### Effective Queries
- Be specific with search terms
- Use domain filtering when possible
- Combine multiple sources for verification
- Ask for citations and sources

### Rate Limits
| Service | Free Tier |
|---------|-----------|
| Brave | 2000/month |
| Perplexity | 5/minute |
| Exa | 1000/month |
| Tavily | 1000/month |

---

## Resources

- [Brave Search API](https://brave.com/search/api)
- [Perplexity API](https://docs.perplexity.ai/)
- [Exa API](https://exa.ai/)
- [Arxiv API](https://arxiv.org/help/api)
