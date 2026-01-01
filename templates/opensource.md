# CLAUDE.md Template: Open Source Project

> Copy this file to your project root as `CLAUDE.md` and customize.

---

# Project Name

## Overview
[Brief description of what this open source project does and its main use case]

## Tech Stack
- **Language:** [Primary language]
- **Framework:** [If applicable]
- **Build Tool:** [npm/cargo/go/etc.]
- **Testing:** [Test framework]
- **CI/CD:** GitHub Actions

## Project Structure
```
├── src/                      # Source code
│   ├── lib/                  # Core library code
│   ├── cli/                  # CLI interface (if applicable)
│   └── index.ts              # Main entry point
├── tests/                    # Test files
│   ├── unit/
│   └── integration/
├── docs/                     # Documentation
│   ├── getting-started.md
│   ├── api.md
│   └── examples/
├── examples/                 # Example usage
├── .github/
│   ├── workflows/            # CI/CD workflows
│   ├── ISSUE_TEMPLATE/
│   └── PULL_REQUEST_TEMPLATE.md
├── CHANGELOG.md
├── CONTRIBUTING.md
├── LICENSE
└── README.md
```

## Common Commands
```bash
# Development
npm install              # Install dependencies
npm run dev              # Development mode with watch
npm run build            # Production build

# Testing
npm test                 # Run all tests
npm run test:watch       # Watch mode
npm run test:coverage    # With coverage report

# Code Quality
npm run lint             # Run linter
npm run lint:fix         # Fix linting issues
npm run format           # Format code
npm run typecheck        # TypeScript check

# Documentation
npm run docs             # Generate docs
npm run docs:serve       # Serve docs locally

# Release
npm run release          # Prepare release
npm run publish          # Publish to npm
```

## Contributing Guidelines

### Commit Messages
Follow [Conventional Commits](https://www.conventionalcommits.org/):
```
feat: add new feature
fix: resolve bug in parser
docs: update API documentation
test: add tests for utils
refactor: simplify validation logic
chore: update dependencies
```

### Branch Naming
```
feat/short-description
fix/issue-number-description
docs/what-documented
refactor/what-refactored
```

### Pull Request Process
1. Fork and create feature branch
2. Write tests for changes
3. Ensure all tests pass
4. Update documentation
5. Submit PR with description

### Code Review Checklist
- [ ] Tests added/updated
- [ ] Documentation updated
- [ ] CHANGELOG updated (for features/fixes)
- [ ] No breaking changes (or documented)
- [ ] Follows existing code style

## API Design Principles

### Public API
- Stable and well-documented
- Breaking changes require major version bump
- Deprecate before removing

### Naming Conventions
- Functions: `camelCase`
- Types/Classes: `PascalCase`
- Constants: `UPPER_SNAKE_CASE`
- Files: `kebab-case`

### Error Handling
- Use descriptive error messages
- Include error codes for programmatic handling
- Document all possible errors

## Testing Strategy

### Unit Tests
- Test individual functions/modules
- Mock external dependencies
- Aim for high coverage of core logic

### Integration Tests
- Test module interactions
- Use real dependencies where feasible
- Test edge cases and error paths

### Test File Location
```
src/utils/parser.ts        → tests/unit/utils/parser.test.ts
src/lib/client.ts          → tests/integration/client.test.ts
```

## Documentation Guidelines

### README Structure
1. Project name and badges
2. One-line description
3. Installation
4. Quick start example
5. API overview
6. Contributing link
7. License

### API Documentation
- Document all public exports
- Include usage examples
- Note any gotchas or limitations

### Code Comments
- Explain "why" not "what"
- Document complex algorithms
- JSDoc for public APIs

## Release Process

### Versioning
Follow [Semantic Versioning](https://semver.org/):
- MAJOR: Breaking changes
- MINOR: New features (backward compatible)
- PATCH: Bug fixes

### Release Checklist
1. Update version in package.json
2. Update CHANGELOG.md
3. Run full test suite
4. Build and verify
5. Create git tag
6. Publish to package registry
7. Create GitHub release

## Environment Variables
```bash
# Development
DEBUG=true               # Enable debug logging

# Testing
CI=true                  # Running in CI environment
TEST_TIMEOUT=5000        # Test timeout in ms

# Publishing
NPM_TOKEN=               # npm auth token (CI only)
```

## Key Files
- `src/index.ts` - Main entry point and public API
- `src/lib/core.ts` - Core functionality
- `CONTRIBUTING.md` - Contribution guidelines
- `.github/workflows/ci.yml` - CI pipeline

## Don't
- Don't introduce breaking changes without major version bump
- Don't merge without tests
- Don't commit generated files (except when necessary)
- Don't expose internal implementation details
- Don't skip CHANGELOG entries for user-facing changes
- Don't ignore failing CI checks
