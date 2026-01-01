# Database MCP Servers

Comprehensive guide to MCP servers for database operations.

---

## PostgreSQL MCP Server

**The most popular database MCP server for relational data.**

### Configuration
```json
{
  "postgresql": {
    "command": "npx",
    "args": ["-y", "@modelcontextprotocol/server-postgres"],
    "env": {
      "POSTGRES_CONNECTION_STRING": "postgresql://user:pass@localhost:5432/db"
    }
  }
}
```

### Capabilities
- **Natural Language Queries** - "Show me all users who signed up last month"
- **Schema Exploration** - Understand tables, columns, relationships
- **Query Optimization** - Suggest indexes and improvements
- **Data Analysis** - Aggregations, groupings, statistics

### Example Prompts
```
"Show me the top 10 customers by order value"
"Explain the relationship between orders and products tables"
"Create an index to improve query performance on users.email"
"Find potential duplicate records in the customers table"
```

---

## MongoDB MCP Server

**For document-based database operations.**

### Configuration
```json
{
  "mongodb": {
    "command": "npx",
    "args": ["-y", "@mongodb-js/mongodb-mcp-server"],
    "env": {
      "MONGODB_CONNECTION_STRING": "mongodb+srv://user:pass@cluster.mongodb.net/"
    }
  }
}
```

### Capabilities
- **Collection Operations** - CRUD operations on documents
- **Aggregation Pipelines** - Complex data transformations
- **Index Management** - Create and analyze indexes
- **Atlas Features** - Search, charts, triggers

### Example Prompts
```
"Find all orders with total > $100 from last week"
"Create an aggregation to group sales by product category"
"Suggest indexes for the users collection based on query patterns"
```

---

## Redis MCP Server

**For in-memory data structure operations.**

### Configuration
```json
{
  "redis": {
    "command": "npx",
    "args": ["-y", "@modelcontextprotocol/server-redis"],
    "env": {
      "REDIS_URL": "redis://localhost:6379"
    }
  }
}
```

### Capabilities
- **Key Operations** - GET, SET, DEL with TTL
- **Data Structures** - Hashes, lists, sets, sorted sets
- **Pub/Sub** - Message publishing
- **Search** - RediSearch integration

### Use Cases
- Session management
- Caching layer
- Rate limiting
- Real-time leaderboards

---

## SQLite MCP Server

**For local database development and testing.**

### Configuration
```json
{
  "sqlite": {
    "command": "npx",
    "args": ["-y", "@modelcontextprotocol/server-sqlite", "./database.db"]
  }
}
```

### Capabilities
- Create and manage tables
- Run queries without external setup
- Perfect for prototyping
- No server required

---

## Neon MCP Server

**Serverless PostgreSQL with branching.**

### Configuration
```json
{
  "neon": {
    "command": "npx",
    "args": ["-y", "@neondatabase/mcp-server-neon"],
    "env": {
      "NEON_API_KEY": "your-api-key"
    }
  }
}
```

### Features
- **Database Branching** - Create instant copies for testing
- **Serverless Scaling** - Auto-scales to zero
- **Connection Pooling** - Built-in pgBouncer

---

## Elasticsearch MCP Server

**For search and analytics.**

### Configuration
```json
{
  "elasticsearch": {
    "command": "npx",
    "args": ["-y", "@elastic/mcp-server-elasticsearch"],
    "env": {
      "ELASTICSEARCH_URL": "http://localhost:9200",
      "ELASTICSEARCH_API_KEY": "your-key"
    }
  }
}
```

### Capabilities
- Full-text search
- Analytics and aggregations
- Index management
- Vector search (dense vectors)

---

## Multi-Database Servers

### Database MCP (genai-toolbox)
Supports 40+ databases through a unified interface:
- PostgreSQL, MySQL, MariaDB
- MongoDB, DynamoDB
- BigQuery, Snowflake
- And many more

### Polyglot DB MCP
Cross-database queries and operations:
- SQL and NoSQL together
- Data migration helpers
- Schema comparison

---

## Best Practices

### Security
1. **Never commit credentials** - Use environment variables
2. **Read-only where possible** - Limit write access
3. **Restrict IP ranges** - Use allowlists
4. **Audit logging** - Track all queries

### Performance
1. **Connection pooling** - Reuse connections
2. **Query limits** - Set reasonable row limits
3. **Index usage** - Verify indexes are used
4. **Monitor slow queries** - Log long-running queries

### Example Secure Config
```json
{
  "postgresql": {
    "command": "npx",
    "args": ["-y", "@modelcontextprotocol/server-postgres"],
    "env": {
      "POSTGRES_CONNECTION_STRING": "${DATABASE_URL}",
      "READ_ONLY": "true",
      "MAX_ROWS": "1000"
    }
  }
}
```

---

## Resources

- [PostgreSQL MCP](https://github.com/modelcontextprotocol/servers/tree/main/src/postgres)
- [MongoDB MCP](https://github.com/mongodb-js/mongodb-mcp-server)
- [Neon MCP](https://github.com/neondatabase/mcp-server-neon)
- [Elasticsearch MCP](https://github.com/elastic/mcp-server-elasticsearch)
