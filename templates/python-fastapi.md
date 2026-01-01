# CLAUDE.md Template: Python/FastAPI

> Copy this file to your project root as `CLAUDE.md` and customize.

---

# Project Name

## Overview
[Brief description of what this API does]

## Tech Stack
- **Framework:** FastAPI
- **Language:** Python 3.11+
- **Database:** [PostgreSQL/SQLite]
- **ORM:** [SQLAlchemy/SQLModel]
- **Validation:** Pydantic
- **Testing:** pytest

## Project Structure
```
src/
├── main.py           # Application entry point
├── api/
│   ├── routes/       # API route handlers
│   ├── deps.py       # Dependency injection
│   └── middleware.py # Custom middleware
├── core/
│   ├── config.py     # Settings and configuration
│   └── security.py   # Auth and security
├── models/           # SQLAlchemy/SQLModel models
├── schemas/          # Pydantic schemas
├── services/         # Business logic
├── repositories/     # Data access layer
└── utils/            # Utility functions

tests/
├── conftest.py       # Pytest fixtures
├── api/              # API tests
└── unit/             # Unit tests
```

## Common Commands
```bash
# Development
uvicorn src.main:app --reload     # Start dev server
python -m pytest                   # Run tests
python -m pytest --cov             # Tests with coverage

# Database
alembic upgrade head               # Run migrations
alembic revision --autogenerate    # Create migration

# Code quality
ruff check .                       # Linting
ruff format .                      # Formatting
mypy src/                          # Type checking
```

## Code Conventions

### API Routes
- Group routes by resource in separate files
- Use dependency injection for common dependencies
- Return Pydantic schemas, not ORM models

```python
@router.get("/{id}", response_model=UserResponse)
async def get_user(
    id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> UserResponse:
    ...
```

### Schemas (Pydantic)
- `Create` suffix for creation: `UserCreate`
- `Update` suffix for updates: `UserUpdate`
- `Response` suffix for responses: `UserResponse`

### Services
- Business logic lives in services, not routes
- Services receive repositories via dependency injection
- Raise custom exceptions, let middleware handle HTTP

### Error Handling
- Use custom exception classes in `core/exceptions.py`
- Middleware converts to appropriate HTTP responses

## Testing
```bash
pytest                           # All tests
pytest -v                        # Verbose
pytest tests/api/                # API tests only
pytest -k "test_user"            # Pattern match
pytest --cov=src --cov-report=html
```

- Use `TestClient` for API tests
- Fixtures in `conftest.py` for common setup
- Mock external services

## Environment Variables
```
DATABASE_URL=postgresql://...
SECRET_KEY=your-secret-key
DEBUG=false
```

Use `python-dotenv` and `.env` file for local development.

## Key Files
- `src/main.py:1` - FastAPI app initialization
- `src/core/config.py:1` - Settings class
- `src/api/deps.py:1` - Dependency injection
- `src/core/security.py:1` - JWT and auth

## Patterns to Follow
- See `src/api/routes/users.py` for route pattern
- See `src/services/user_service.py` for service pattern
- See `src/repositories/user_repo.py` for repository pattern

## Don't
- Don't put business logic in route handlers
- Don't return ORM models directly from API
- Don't use raw SQL - use ORM queries
- Don't commit `.env` files
