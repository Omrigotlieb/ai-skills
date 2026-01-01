# Database Skills for Claude Code

Skills for database design, querying, optimization, and migrations.

---

## SQL Query Skill

```markdown
---
name: sql-query
description: Write and optimize SQL queries
---

# SQL Query Writing

## Capabilities
- Write complex queries (JOINs, subqueries, CTEs)
- Optimize slow queries
- Explain query plans
- Database-specific syntax (PostgreSQL, MySQL, SQLite)

## Best Practices
- Use parameterized queries (prevent SQL injection)
- Select only needed columns
- Index foreign keys
- Use EXPLAIN ANALYZE

## Example
"Write a query to find users with more than 5 orders in the last month"
```

---

## Database Design Skill

```markdown
---
name: database-design
description: Design database schemas
---

# Database Design

## When to Use
- New applications
- Schema refactoring
- Data modeling

## Capabilities
- Entity-relationship design
- Normalization (1NF, 2NF, 3NF, BCNF)
- Index strategy
- Constraint design

## Deliverables
- ERD diagrams (Mermaid)
- CREATE TABLE statements
- Index recommendations
- Migration scripts

## Example
"Design a database schema for an e-commerce platform with users, products, orders"
```

---

## Migration Skill

```markdown
---
name: database-migration
description: Create and manage database migrations
---

# Database Migrations

## Frameworks Supported
- Prisma (Node.js)
- SQLAlchemy/Alembic (Python)
- Flyway/Liquibase (Java)
- golang-migrate (Go)
- Rails ActiveRecord (Ruby)

## Best Practices
- Small, focused migrations
- Always provide rollback
- Test in staging first
- Backup before migration
- Handle data migrations separately

## Example
"Create a migration to add a 'status' column to the orders table"
```

---

## Query Optimization Skill

```markdown
---
name: query-optimization
description: Optimize slow database queries
---

# Query Optimization

## Analysis Steps
1. Run EXPLAIN ANALYZE
2. Identify sequential scans
3. Check for missing indexes
4. Look for N+1 queries
5. Analyze join order

## Common Fixes
| Problem | Solution |
|---------|----------|
| Full table scan | Add index |
| N+1 queries | Eager loading |
| Large result sets | Pagination |
| Complex JOINs | Denormalize |
| Lock contention | Optimize transactions |

## Tools
- pg_stat_statements (PostgreSQL)
- EXPLAIN ANALYZE
- Query profilers
```

---

## ORM Skills

### Prisma Skill
```markdown
---
name: prisma
description: Prisma ORM usage and optimization
---

# Prisma

## Capabilities
- Schema design
- Query optimization
- Migration management
- Type-safe queries

## Example Schema
model User {
  id        Int      @id @default(autoincrement())
  email     String   @unique
  posts     Post[]
  createdAt DateTime @default(now())
}
```

### SQLAlchemy Skill
```markdown
---
name: sqlalchemy
description: SQLAlchemy ORM and Core
---

# SQLAlchemy

## Capabilities
- Model definitions
- Relationship mapping
- Query building
- Session management

## Best Practices
- Use declarative base
- Manage sessions properly
- Use async for high concurrency
```

---

## NoSQL Skills

### MongoDB Skill
```markdown
---
name: mongodb
description: MongoDB queries and schema design
---

# MongoDB

## Capabilities
- Document schema design
- Aggregation pipelines
- Index strategies
- Sharding considerations

## When to Use
- Flexible schemas
- Document-oriented data
- High write throughput
- Horizontal scaling needed
```

### Redis Skill
```markdown
---
name: redis
description: Redis caching and data structures
---

# Redis

## Use Cases
- Session storage
- Caching
- Rate limiting
- Pub/sub messaging
- Leaderboards

## Data Structures
| Type | Use Case |
|------|----------|
| String | Simple cache |
| Hash | Object storage |
| List | Queues |
| Set | Unique items |
| Sorted Set | Rankings |
```

---

## Database Patterns

### Repository Pattern
```typescript
interface UserRepository {
  findById(id: string): Promise<User | null>;
  findByEmail(email: string): Promise<User | null>;
  create(data: CreateUserDto): Promise<User>;
  update(id: string, data: UpdateUserDto): Promise<User>;
  delete(id: string): Promise<void>;
}
```

### Unit of Work
```python
class UnitOfWork:
    def __enter__(self):
        self.session = Session()
        return self

    def __exit__(self, *args):
        self.session.close()

    def commit(self):
        self.session.commit()

    def rollback(self):
        self.session.rollback()
```

---

## Database Commands

### db-schema.md
```markdown
Analyze and document database schema:
1. Connect to database
2. Extract schema information
3. Generate ERD
4. Document relationships
```

### db-optimize.md
```markdown
Optimize database performance:
1. Identify slow queries
2. Analyze query plans
3. Suggest indexes
4. Recommend schema changes
```

---

## MCP Servers for Databases

| Server | Purpose |
|--------|---------|
| **PostgreSQL MCP** | PostgreSQL queries |
| **MySQL MCP** | MySQL operations |
| **MongoDB MCP** | MongoDB queries |
| **Redis MCP** | Redis operations |
| **SQLite MCP** | SQLite database |

---

## Resources

- [Use The Index, Luke](https://use-the-index-luke.com/) - SQL indexing
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [Prisma Documentation](https://www.prisma.io/docs)
- [Database Design Tutorial](https://www.lucidchart.com/pages/database-diagram/database-design)
