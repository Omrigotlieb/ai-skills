# CLAUDE.md Template: Rust Project

> Copy this file to your project root as `CLAUDE.md` and customize.

---

# Project Name

## Overview
[Description of the Rust project - CLI tool, web service, library, system tool, etc.]

## Tech Stack
- **Language:** Rust (stable)
- **Async Runtime:** [tokio / async-std]
- **Web Framework:** [Axum / Actix-web / Rocket] (if applicable)
- **Database:** [SQLx / Diesel / SeaORM]
- **Serialization:** serde + serde_json
- **Error Handling:** [thiserror / anyhow]
- **CLI:** [clap / argh] (if applicable)

## Project Structure
```
├── src/
│   ├── main.rs             # Binary entry point
│   ├── lib.rs              # Library entry point
│   ├── config.rs           # Configuration
│   ├── error.rs            # Error types
│   ├── domain/             # Business logic
│   │   ├── mod.rs
│   │   ├── user.rs
│   │   └── order.rs
│   ├── handlers/           # HTTP/API handlers
│   │   ├── mod.rs
│   │   └── user.rs
│   ├── repository/         # Data access
│   │   ├── mod.rs
│   │   └── postgres.rs
│   └── utils/              # Utilities
├── tests/                  # Integration tests
│   └── api_tests.rs
├── benches/                # Benchmarks
├── examples/               # Example usage
├── migrations/             # Database migrations
├── Cargo.toml
├── Cargo.lock
├── rust-toolchain.toml     # Rust version pinning
└── .cargo/
    └── config.toml         # Cargo configuration
```

## Common Commands
```bash
# Development
cargo run                   # Run the binary
cargo run --release         # Run optimized
cargo run -- --help         # Run with args

# Building
cargo build                 # Debug build
cargo build --release       # Release build
cargo check                 # Quick syntax check

# Testing
cargo test                  # Run all tests
cargo test -- --nocapture   # Show println! output
cargo test user             # Run tests matching "user"
cargo test --doc            # Run doc tests

# Code Quality
cargo fmt                   # Format code
cargo fmt -- --check        # Check formatting
cargo clippy                # Lint with clippy
cargo clippy -- -D warnings # Treat warnings as errors

# Documentation
cargo doc                   # Generate docs
cargo doc --open            # Generate and open

# Dependencies
cargo update                # Update dependencies
cargo audit                 # Check for vulnerabilities
cargo outdated              # Show outdated deps

# Benchmarks
cargo bench                 # Run benchmarks
```

## Code Conventions

### Module Organization
```rust
// src/lib.rs - public API
pub mod config;
pub mod domain;
pub mod error;

// Re-export commonly used items
pub use config::Config;
pub use error::{Error, Result};
```

### Naming
- **Crates:** lowercase with hyphens (`my-crate`)
- **Modules:** lowercase with underscores (`user_service`)
- **Types:** PascalCase (`UserService`, `CreateUserRequest`)
- **Functions:** snake_case (`create_user`, `validate_email`)
- **Constants:** SCREAMING_SNAKE_CASE (`MAX_CONNECTIONS`)

### Error Handling
```rust
// Define error types with thiserror
use thiserror::Error;

#[derive(Error, Debug)]
pub enum Error {
    #[error("user not found: {0}")]
    NotFound(String),

    #[error("validation error: {0}")]
    Validation(String),

    #[error("database error")]
    Database(#[from] sqlx::Error),
}

pub type Result<T> = std::result::Result<T, Error>;
```

### Async Patterns
```rust
// Use async/await with tokio
use tokio;

#[tokio::main]
async fn main() -> Result<()> {
    let app = build_app().await?;
    app.run().await
}

// Prefer async traits with async-trait
#[async_trait]
pub trait UserRepository: Send + Sync {
    async fn find_by_id(&self, id: Uuid) -> Result<Option<User>>;
    async fn create(&self, user: CreateUser) -> Result<User>;
}
```

### Ownership Patterns
```rust
// Prefer borrowing when possible
fn process_user(user: &User) -> Result<()>

// Use owned types when needed
fn create_user(user: CreateUser) -> Result<User>

// Clone explicitly when required
let user_copy = user.clone();
```

### Builder Pattern
```rust
#[derive(Default)]
pub struct UserBuilder {
    name: Option<String>,
    email: Option<String>,
}

impl UserBuilder {
    pub fn new() -> Self {
        Self::default()
    }

    pub fn name(mut self, name: impl Into<String>) -> Self {
        self.name = Some(name.into());
        self
    }

    pub fn build(self) -> Result<User> {
        Ok(User {
            name: self.name.ok_or(Error::Validation("name required".into()))?,
            email: self.email.ok_or(Error::Validation("email required".into()))?,
        })
    }
}
```

## Testing Patterns

### Unit Tests
```rust
#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_validate_email() {
        assert!(validate_email("user@example.com").is_ok());
        assert!(validate_email("invalid").is_err());
    }

    #[tokio::test]
    async fn test_async_function() {
        let result = async_function().await;
        assert!(result.is_ok());
    }
}
```

### Integration Tests
```rust
// tests/api_tests.rs
use my_crate::build_app;

#[tokio::test]
async fn test_create_user_endpoint() {
    let app = build_app().await;
    let client = reqwest::Client::new();

    let response = client
        .post("http://localhost:3000/users")
        .json(&json!({"name": "Test", "email": "test@example.com"}))
        .send()
        .await
        .unwrap();

    assert_eq!(response.status(), 201);
}
```

## Environment Variables
```bash
# .env
RUST_LOG=debug,my_crate=trace
DATABASE_URL=postgres://user:pass@localhost:5432/myapp
APP_HOST=0.0.0.0
APP_PORT=3000
```

## Key Files
- `src/main.rs` - Application entry point
- `src/lib.rs` - Library exports
- `src/config.rs` - Configuration (use `config` crate)
- `src/error.rs` - Error types
- `Cargo.toml` - Dependencies and metadata

## Patterns to Follow
- See `src/domain/user.rs` for domain model pattern
- See `src/handlers/user.rs` for HTTP handler pattern
- See `src/repository/postgres.rs` for repository pattern

## Performance Considerations
- Use `&str` over `String` when possible
- Prefer `Vec::with_capacity()` for known sizes
- Use `#[inline]` sparingly and measure
- Profile with `cargo flamegraph`

## Don't
- Don't use `.unwrap()` in production code - handle errors
- Don't ignore clippy warnings - fix or explicitly allow
- Don't use `unsafe` without thorough review
- Don't clone unnecessarily - borrow when possible
- Don't block async code - use `spawn_blocking` for CPU work
- Don't leak implementation details in public API
