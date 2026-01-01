# Testing Skills for Claude Code

Skills and tools for test-driven development, test generation, and quality assurance.

---

## Test-Driven Development (TDD) Skill

From the Superpowers collection:

```markdown
---
name: test-driven-development
description: Enforces RED-GREEN-REFACTOR cycle
---

# Test-Driven Development

## The Cycle
1. **RED** - Write a failing test first
2. **GREEN** - Write minimal code to pass
3. **REFACTOR** - Clean up while keeping tests green

## Anti-Patterns to Avoid
- Writing tests after implementation
- Testing implementation details
- Skipping the refactor step
- Over-mocking

## Rules
- Never write production code without a failing test
- Tests should be readable as documentation
- One assertion per test when possible
- Test behavior, not implementation
```

---

## Test Generation Skill

Generate comprehensive tests automatically:

```markdown
---
name: test-generator
description: Generate test cases from code or requirements
---

# Test Generator

## When to Use
- New code without tests
- Increasing coverage
- Testing edge cases

## Capabilities
- Analyze code for testable paths
- Generate unit tests
- Generate integration tests
- Edge case identification

## Output Formats
- Jest (JavaScript/TypeScript)
- pytest (Python)
- Go testing
- JUnit (Java)
- RSpec (Ruby)

## Example
Input: "Generate tests for the UserService class"
Output: Comprehensive test suite with:
- Happy path tests
- Error cases
- Edge cases
- Mock setups
```

---

## Coverage Analysis Skill

```markdown
---
name: coverage-analysis
description: Analyze and improve test coverage
---

# Coverage Analysis

## Capabilities
- Identify untested code paths
- Find missing edge cases
- Suggest tests to add
- Prioritize by risk

## Metrics Tracked
- Line coverage
- Branch coverage
- Function coverage
- Statement coverage

## Usage
"Analyze test coverage for src/services/ and suggest improvements"
```

---

## Property-Based Testing Skill

```markdown
---
name: property-testing
description: Generate property-based tests
---

# Property-Based Testing

## When to Use
- Functions with many input combinations
- Parsers and serializers
- Mathematical operations
- Data transformations

## Frameworks
- fast-check (JavaScript)
- Hypothesis (Python)
- QuickCheck (Haskell)
- PropEr (Erlang)

## Example Properties
- Roundtrip: parse(serialize(x)) === x
- Idempotence: f(f(x)) === f(x)
- Associativity: f(a, f(b, c)) === f(f(a, b), c)
```

---

## Mutation Testing Skill

```markdown
---
name: mutation-testing
description: Verify test quality through mutation testing
---

# Mutation Testing

## How It Works
1. Inject small bugs (mutations) into code
2. Run test suite
3. Check if tests catch the bugs
4. Report mutation score

## Mutation Types
- Flip boolean operators
- Change arithmetic operators
- Remove function calls
- Modify return values

## Tools
- Stryker (JS/TS)
- mutmut (Python)
- pitest (Java)
```

---

## Snapshot Testing Skill

```markdown
---
name: snapshot-testing
description: Setup and manage snapshot tests
---

# Snapshot Testing

## When to Use
- React component output
- API response shapes
- Configuration files
- Serialized data structures

## Best Practices
- Review snapshot changes carefully
- Keep snapshots small and focused
- Use inline snapshots for small outputs
- Update intentionally, not automatically
```

---

## E2E Testing Skill

```markdown
---
name: e2e-testing
description: End-to-end testing with Playwright/Cypress
---

# E2E Testing

## Setup
Playwright or Cypress based on project needs.

## Capabilities
- Page interactions
- Form submissions
- Authentication flows
- API mocking
- Visual regression
- Mobile viewports

## Best Practices
- Test user journeys, not implementation
- Use data-testid attributes
- Isolate test data
- Run in CI/CD pipeline

## Example
"Write E2E tests for the checkout flow"
```

---

## Contract Testing Skill

```markdown
---
name: contract-testing
description: API contract testing with Pact
---

# Contract Testing

## When to Use
- Microservices communication
- API versioning
- Consumer-driven contracts

## Workflow
1. Consumer defines expected interactions
2. Generate contract (Pact file)
3. Provider verifies against contract
4. Publish to Pact Broker

## Benefits
- Catch breaking changes early
- Document API behavior
- Decouple services
```

---

## Testing Patterns

### Arrange-Act-Assert (AAA)
```javascript
// Arrange
const user = createTestUser({ name: 'Test' });

// Act
const result = await userService.update(user.id, { name: 'Updated' });

// Assert
expect(result.name).toBe('Updated');
```

### Test Doubles
| Type | Purpose |
|------|---------|
| **Stub** | Provide canned answers |
| **Mock** | Verify interactions |
| **Spy** | Record calls for later verification |
| **Fake** | Working implementation (simplified) |
| **Dummy** | Fill parameter lists |

### Test Isolation
- Reset state between tests
- Use factories for test data
- Avoid shared mutable state
- Mock external dependencies

---

## Testing Commands

Store in `.claude/commands/`:

### test.md
```markdown
Run tests and analyze failures:
1. Run test suite with coverage
2. If failures, analyze and fix
3. Ensure coverage doesn't decrease
4. Report summary
```

### test-watch.md
```markdown
Run tests in watch mode:
1. Start test runner in watch mode
2. Monitor for failures
3. Report changes
```

---

## MCP Servers for Testing

| Server | Purpose |
|--------|---------|
| **Playwright MCP** | Browser automation |
| **Database MCP** | Test data setup |
| **HTTP MCP** | API testing |

---

## Resources

- [Testing Trophy](https://kentcdodds.com/blog/the-testing-trophy-and-testing-classifications) - Kent C. Dodds
- [Test Desiderata](https://kentbeck.github.io/TestDesiderata/) - Kent Beck
- [Playwright Docs](https://playwright.dev/)
- [Jest Docs](https://jestjs.io/)
- [pytest Docs](https://docs.pytest.org/)
