# CLAUDE.md Template: Go Project

> Copy this file to your project root as `CLAUDE.md` and customize.

---

# Project Name

## Overview
[Description of the Go project - CLI tool, web service, library, etc.]

## Tech Stack
- **Language:** Go 1.22+
- **Framework:** [stdlib / Gin / Echo / Fiber / Chi]
- **Database:** [PostgreSQL / MySQL / SQLite] with [sqlx / GORM / sqlc]
- **Testing:** Go testing + [testify / gomock]
- **Build:** Go modules

## Project Structure
```
├── cmd/
│   └── myapp/              # Application entry points
│       └── main.go
├── internal/               # Private application code
│   ├── api/                # HTTP handlers
│   │   ├── handlers/
│   │   ├── middleware/
│   │   └── routes.go
│   ├── domain/             # Business logic
│   │   ├── user/
│   │   └── order/
│   ├── repository/         # Data access
│   │   ├── postgres/
│   │   └── repository.go
│   └── config/             # Configuration
├── pkg/                    # Public libraries
│   └── utils/
├── migrations/             # Database migrations
├── scripts/                # Build and deploy scripts
├── api/                    # API definitions (OpenAPI, proto)
├── go.mod
├── go.sum
├── Makefile
└── Dockerfile
```

## Common Commands
```bash
# Development
go run ./cmd/myapp          # Run the application
go build ./...              # Build all packages
go install ./cmd/myapp      # Install binary

# Testing
go test ./...               # Run all tests
go test -v ./...            # Verbose output
go test -race ./...         # Race detection
go test -cover ./...        # With coverage
go test -coverprofile=coverage.out ./...

# Code Quality
go fmt ./...                # Format code
go vet ./...                # Static analysis
golangci-lint run           # Comprehensive linting
staticcheck ./...           # Additional checks

# Dependencies
go mod tidy                 # Clean up dependencies
go mod download             # Download dependencies
go get -u ./...             # Update dependencies

# Database
make migrate-up             # Run migrations
make migrate-down           # Rollback migrations

# Docker
docker build -t myapp .     # Build container
docker run myapp            # Run container
```

## Code Conventions

### Package Organization
```go
// Each package should have a single responsibility
// internal/user/user.go - domain logic
// internal/user/repository.go - data access
// internal/user/handler.go - HTTP handlers (if applicable)
```

### Naming
- **Packages:** lowercase, single word (`user`, `auth`, `order`)
- **Files:** lowercase, underscore for multi-word (`user_service.go`)
- **Exported:** PascalCase (`UserService`, `NewUser`)
- **Unexported:** camelCase (`userRepo`, `validateEmail`)
- **Interfaces:** -er suffix when single method (`Reader`, `Writer`)

### Error Handling
```go
// Always handle errors explicitly
if err != nil {
    return fmt.Errorf("failed to create user: %w", err)
}

// Use custom error types for domain errors
type NotFoundError struct {
    Resource string
    ID       string
}

func (e NotFoundError) Error() string {
    return fmt.Sprintf("%s with ID %s not found", e.Resource, e.ID)
}
```

### Dependency Injection
```go
// Use constructor injection
type UserService struct {
    repo   UserRepository
    logger *slog.Logger
}

func NewUserService(repo UserRepository, logger *slog.Logger) *UserService {
    return &UserService{repo: repo, logger: logger}
}
```

### Context Usage
```go
// Always pass context as first parameter
func (s *UserService) GetUser(ctx context.Context, id string) (*User, error)

// Respect context cancellation
select {
case <-ctx.Done():
    return ctx.Err()
default:
    // continue processing
}
```

## Testing Patterns

### Table-Driven Tests
```go
func TestValidateEmail(t *testing.T) {
    tests := []struct {
        name    string
        email   string
        wantErr bool
    }{
        {"valid email", "user@example.com", false},
        {"missing @", "userexample.com", true},
        {"empty", "", true},
    }

    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            err := ValidateEmail(tt.email)
            if (err != nil) != tt.wantErr {
                t.Errorf("ValidateEmail() error = %v, wantErr %v", err, tt.wantErr)
            }
        })
    }
}
```

### Test Files
- Tests go in `*_test.go` files in the same package
- Integration tests in `integration_test.go` with build tag
- Use `testdata/` for test fixtures

## Environment Variables
```bash
# .env (development)
APP_ENV=development
APP_PORT=8080
DATABASE_URL=postgres://user:pass@localhost:5432/myapp
LOG_LEVEL=debug
```

Load with: `github.com/joho/godotenv` or `github.com/caarlos0/env`

## Key Files
- `cmd/myapp/main.go` - Application entry point
- `internal/config/config.go` - Configuration loading
- `internal/api/routes.go` - HTTP route definitions
- `Makefile` - Common tasks

## Patterns to Follow
- See `internal/user/service.go` for service layer pattern
- See `internal/api/handlers/user.go` for HTTP handler pattern
- See `internal/repository/postgres/user.go` for repository pattern

## Don't
- Don't use `panic` for recoverable errors - return errors
- Don't ignore errors - handle or explicitly ignore with `_ =`
- Don't use global state - use dependency injection
- Don't put business logic in handlers - use services
- Don't use `init()` for complex initialization
- Don't import `internal/` packages from other modules
