# Claude Code Workflows

Battle-tested workflows and automation patterns for Claude Code. These patterns come from Anthropic's internal usage and the community.

## Quick Navigation

- [Routines & Scheduled Agents](#routines--scheduled-agents) ← **New**
- [Feature Development](#feature-development)
- [Code Review](#code-review)
- [Debugging](#debugging)
- [Refactoring](#refactoring)
- [Documentation](#documentation)
- [Testing](#testing)
- [Git Operations](#git-operations)
- [Project Exploration](#project-exploration)
- [Multi-Agent Patterns](#multi-agent-patterns) ← **New**

---

## Routines & Scheduled Agents

Claude Code can run prompts automatically on a schedule, via API, or in response to GitHub events. See the **[full Routines guide](routines.md)** for setup instructions, ready-to-use prompts, and best practices.

**Quick examples of what people schedule:**

| Routine | Trigger | What it does |
|---------|---------|-------------|
| Morning standup prep | Daily 8:30am | Digest overnight PRs, issues, CI failures → Slack |
| Nightly issue triage | Daily 11pm | Auto-label and assign new issues |
| Weekly dependency audit | Monday 7am | Scan for CVEs, open fix PR |
| Overnight PR review | Daily midnight | Leave inline review comments on open PRs |
| Docs-drift detection | Friday 3pm | Flag stale docs after code changes |
| Deploy verification | On release | Smoke-check health endpoints, report to Slack |
| PR status monitor | `/loop 5m` | Watch CI, auto-fix failures, notify when ready |

**Three tiers:** `/loop` (session), Desktop scheduled task (local), Cloud routine (runs on Anthropic infra, laptop off).

→ [Full guide with prompts and best practices](routines.md)

---

## Feature Development

### The Planning-First Workflow

The most reliable pattern for implementing features:

```
1. Plan Mode → 2. Implement → 3. Test → 4. Review → 5. Commit
```

**Step 1: Enter Plan Mode**
```
Press Shift+Tab to enter plan mode
```

**Step 2: Request a Plan**
```
Implement user authentication with JWT tokens.

Requirements:
- Login/logout endpoints
- Token refresh mechanism
- Password hashing with bcrypt
- Rate limiting on auth endpoints

Propose a 3-step plan with small diffs and tests.
```

**Step 3: Review and Approve**
Claude will analyze the codebase and propose an implementation plan. Review each step before proceeding.

**Step 4: Implement in Batches**
```
Implement step 1 of the plan. Keep diffs under 200 lines.
```

**Step 5: Test Each Step**
```
Run the tests for the auth module and fix any failures.
```

---

### Custom Command: Feature Development

Create `.claude/commands/feature.md`:

```markdown
# Feature Development

Implement the following feature: $ARGUMENTS

## Process
1. First, analyze the existing codebase to understand patterns
2. Create a detailed implementation plan
3. Implement in small, testable increments
4. Write tests alongside implementation
5. Run tests and fix any issues

## Constraints
- Keep each diff under 200 lines
- Follow existing code patterns
- Maintain test coverage above 80%
- Use existing utilities where possible

## Output
After each step, summarize:
- What was implemented
- What tests were added
- What's next
```

Usage: `/project:feature add user profile page with avatar upload`

---

## Code Review

### PR Review Workflow

```
# Review a specific PR
Review PR #123. Focus on:
1. Logic correctness
2. Edge cases
3. Security implications
4. Performance considerations
5. Test coverage

Provide specific, actionable feedback.
```

### Pre-Commit Review

```
Before I commit, review these changes:
- Check for security issues
- Verify error handling
- Ensure tests cover new code
- Look for any code smells
```

### Custom Command: Code Review

Create `.claude/commands/review.md`:

```markdown
# Code Review

Review the current changes in this repository.

## Checklist
- [ ] No security vulnerabilities (SQL injection, XSS, etc.)
- [ ] Proper error handling
- [ ] Tests for new functionality
- [ ] No hardcoded secrets or credentials
- [ ] Follows project coding standards
- [ ] No performance regressions
- [ ] Documentation updated if needed

## Output Format
For each issue found:
1. **Severity**: Critical / High / Medium / Low
2. **Location**: file:line
3. **Issue**: Description
4. **Suggestion**: How to fix

If no issues: Confirm the code is ready to commit.
```

---

## Debugging

### Systematic Debugging Workflow

```
I'm seeing this error: [paste error]

Debug this systematically:
1. Identify the error source
2. Trace the execution path
3. Find the root cause
4. Propose a fix
5. Verify the fix doesn't break anything else
```

### The 5-Why Technique

```
The user login is failing.

Apply the 5-Why technique:
1. Why is login failing?
2. Why is [that] happening?
3. Continue until root cause is found

Then propose a fix.
```

### Custom Command: Debug

Create `.claude/commands/debug.md`:

```markdown
# Debug Issue

Investigate and fix: $ARGUMENTS

## Process
1. Reproduce the issue (if possible)
2. Gather relevant logs and error messages
3. Trace the code path
4. Identify root cause
5. Implement fix
6. Verify fix works
7. Check for regression

## Output
- Root cause explanation
- Fix implemented
- Test added to prevent regression
```

---

## Refactoring

### Safe Refactoring Workflow

```
Refactor the UserService class to use dependency injection.

Constraints:
- Make incremental changes
- Keep all tests passing after each change
- Don't change external API
- Document any breaking changes
```

### Extract and Test Pattern

```
Extract the validation logic from createUser() into a separate function.

1. First, write tests for the current behavior
2. Extract the function
3. Verify tests still pass
4. Add any missing edge case tests
```

---

## Documentation

### Auto-Document Workflow

```
Generate documentation for the API module:
1. List all public endpoints
2. Document request/response formats
3. Include example usage
4. Note any authentication requirements
```

### README Generation

```
Create a README for this project that includes:
- Project description
- Installation instructions
- Usage examples
- API reference
- Contributing guidelines
```

---

## Testing

### Test-First Workflow

```
I need to add email validation.

1. First, write tests for:
   - Valid email formats
   - Invalid email formats
   - Edge cases (empty, null, special chars)
2. Then implement to make tests pass
3. Refactor if needed
```

### Coverage Improvement

```
Analyze test coverage for src/services/.
Identify untested code paths and write tests for:
1. Happy paths that are missing
2. Error handling
3. Edge cases
```

---

## Git Operations

### Commit Workflow

```
Review my changes and create a commit:
1. Stage relevant files
2. Write a descriptive commit message following conventional commits
3. Don't include any debug code or console.logs
```

### Branch Cleanup

```
Clean up my git branches:
1. List branches merged to main
2. Show branches with no recent commits
3. Delete local branches that are gone on remote
```

### Rebase Helper

```
Help me rebase my feature branch onto main:
1. Show me the commits that will be rebased
2. Identify potential conflicts
3. Guide me through the rebase
```

---

## Project Exploration

### New Project Onboarding

```
I'm new to this codebase. Help me understand:
1. Project structure and architecture
2. Key entry points
3. Main dependencies
4. How to run locally
5. How to run tests
```

### Code Archaeology

```
Explain the history of the auth module:
1. When was it created?
2. Major changes over time
3. Current state and any technical debt
4. Who are the main contributors?
```

### Dependency Analysis

```
Analyze our dependencies:
1. Which are outdated?
2. Any with security vulnerabilities?
3. Which are unused?
4. Suggest updates with breaking change warnings
```

---

## Workflow Automation

### Setting Up Project Commands

Create these files in `.claude/commands/`:

**plan.md**
```markdown
Create an implementation plan for: $ARGUMENTS

Output a numbered list of steps, each with:
- What will be changed
- Files affected
- Estimated complexity (S/M/L)
```

**implement.md**
```markdown
Implement the next step in the current plan.
- Keep changes small and focused
- Write tests alongside code
- Update docs if needed
```

**test.md**
```markdown
Run tests and fix any failures.
Focus on: $ARGUMENTS

If all tests pass, summarize coverage.
```

**ship.md**
```markdown
Prepare changes for shipping:
1. Run all tests
2. Run linting
3. Create commit with conventional message
4. Summarize what's being shipped
```

---

## Best Practices

### Effective Prompting

1. **Be specific**: Include file paths, function names, exact requirements
2. **Provide context**: Explain the "why" behind requests
3. **Set constraints**: Lines of code, patterns to follow, files to avoid
4. **Request format**: Ask for specific output structure

### Managing Context

1. **Use `/compact`** when context gets large
2. **Create handoff documents** for long sessions
3. **Start fresh** for unrelated tasks
4. **Use subagents** for isolated subtasks

### Iteration Patterns

1. **Small batches**: Implement in chunks, verify each
2. **Test frequently**: Run tests after every significant change
3. **Review often**: Check Claude's work before proceeding
4. **Course correct early**: Address issues immediately

---

## Multi-Agent Patterns

Orchestrate multiple agents on complex tasks. Four core patterns:

| Pattern | How it works | Best for |
|---------|-------------|----------|
| **Split-and-Merge** | Parallel sub-agents (security, perf, tests), merged report | Code review |
| **Sequential Pipeline** | Analyze → Design → Plan → Implement → Verify | Feature development |
| **Headless Batch** | `claude -p` in CI/CD with JSON output | Automated gates |
| **Agent Teams** | Persistent roles (orchestrator, implementer, reviewer, debugger) | Large projects |

→ [Full patterns with copy-paste prompts](routines.md#multi-agent-routine-patterns)

---

## Resources

### Official
- [Common Workflows — Claude Code Docs](https://code.claude.com/docs/en/common-workflows)
- [Best Practices — Anthropic Engineering](https://www.anthropic.com/engineering/claude-code-best-practices)
- [Effective Context Engineering](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)
- [Effective Harnesses for Long-Running Agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents)

### Community
- [claude-code-workflows — shinpr](https://github.com/shinpr/claude-code-workflows)
- [awesome-claude-code — hesreallyhim](https://github.com/hesreallyhim/awesome-claude-code)
- [awesome-claude-code-toolkit — rohitg00](https://github.com/rohitg00/awesome-claude-code-toolkit)
- [9 Parallel Agents for Code Review — hamy.xyz](https://hamy.xyz/blog/2026-02_code-reviews-claude-subagents)
- [5 Claude Code Workflow Patterns — MindStudio](https://www.mindstudio.ai/blog/claude-code-agentic-workflow-patterns)
