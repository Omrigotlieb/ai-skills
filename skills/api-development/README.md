# API Development Skills

Skills for designing, documenting, and implementing REST APIs with Claude Code.

---

## API Design Skill

Design REST APIs following best practices:

```markdown
---
name: api-design
description: Design REST APIs with best practices
---

# API Design

## When to Use
- Designing new API endpoints
- Refactoring existing APIs
- Planning API versioning

## Best Practices
- Use nouns for resources (/users, /orders)
- HTTP verbs for actions (GET, POST, PUT, DELETE)
- Plural resource names
- Nested resources for relationships
- Consistent naming conventions

## Versioning
- URL versioning: /v1/users
- Header versioning: Accept: application/vnd.api+json;version=1

## Error Handling
Return consistent error format:
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Human readable message",
    "details": [...]
  }
}

## Pagination
- Cursor-based for large datasets
- Offset-based for smaller sets
- Include total count and navigation links
```

---

## API Documentation Generator

Auto-generate OpenAPI/Swagger specs:

```markdown
---
name: api-documenter
description: Generate API documentation from code
---

# API Documentation Generator

## Capabilities
- Extract endpoints from code
- Generate OpenAPI 3.0 specs
- Create request/response examples
- Document authentication methods

## Output Formats
- OpenAPI 3.0 YAML/JSON
- Markdown documentation
- Postman collections

## Example Usage
"Generate OpenAPI spec for the user service endpoints"
```

---

## Spring Boot OpenAPI Skill

For Spring Boot 3.x applications:

```markdown
---
name: spring-boot-openapi
description: Setup Swagger UI with SpringDoc
---

# Spring Boot OpenAPI Documentation

## Dependencies
implementation 'org.springdoc:springdoc-openapi-starter-webmvc-ui:2.3.0'

## Configuration
@OpenAPIDefinition(
  info = @Info(
    title = "API Title",
    version = "1.0.0",
    description = "API Description"
  )
)

## Annotations
- @Operation(summary = "...")
- @ApiResponse(responseCode = "200", description = "...")
- @Parameter(description = "...")
- @Schema(description = "...")

## Access
- Swagger UI: /swagger-ui.html
- OpenAPI JSON: /v3/api-docs
```

---

## Swagger Explorer MCP

Analyze and explore OpenAPI specifications:

**Capabilities:**
- Parse Swagger/OpenAPI specs
- Explore endpoints dynamically
- Filter by tags, paths, methods
- Validate schemas
- Understand request/response structures

**Use Cases:**
- Working with unfamiliar APIs
- Validating API implementations
- Generating client code
- Testing API contracts

---

## API Testing Skills

### Contract Testing
```markdown
---
name: api-contract-testing
description: Verify API contracts match implementation
---

Compare OpenAPI spec against actual implementation:
1. Parse OpenAPI spec
2. Extract endpoint definitions
3. Make test requests
4. Validate responses match schema
5. Report discrepancies
```

### Integration Testing
```markdown
---
name: api-integration-testing
description: Test API endpoints end-to-end
---

Generate integration tests:
- Happy path tests
- Error cases
- Edge cases
- Authentication scenarios
- Rate limiting behavior
```

---

## API Design Patterns

### Resource Naming
```
GET    /users              # List users
POST   /users              # Create user
GET    /users/{id}         # Get user
PUT    /users/{id}         # Update user
DELETE /users/{id}         # Delete user
GET    /users/{id}/orders  # User's orders
```

### Response Envelope
```json
{
  "data": { ... },
  "meta": {
    "page": 1,
    "total": 100
  },
  "links": {
    "next": "/users?page=2"
  }
}
```

### Error Format
```json
{
  "error": {
    "code": "RESOURCE_NOT_FOUND",
    "message": "User not found",
    "details": {
      "id": "123"
    }
  }
}
```

---

## Recommended MCP Servers

| Server | Purpose |
|--------|---------|
| **Swagger Explorer** | Parse and explore OpenAPI specs |
| **Postman MCP** | Collection management and testing |
| **HTTP MCP** | Make API requests directly |

---

## Resources

- [OpenAPI Specification](https://spec.openapis.org/oas/latest.html)
- [REST API Design Best Practices](https://restfulapi.net/)
- [API Design Guidelines](https://github.com/microsoft/api-guidelines)
- [SpringDoc OpenAPI](https://springdoc.org/)
