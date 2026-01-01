# Effective Claude Code Prompts

A collection of battle-tested prompts and prompting patterns for Claude Code.

## Prompting Principles

### The TCRO Framework

Structure prompts with:

1. **Task** - What's the job to be done?
2. **Context** - Why are we doing this?
3. **Requirements** - Explicit list of must-haves
4. **Output** - Expected format and deliverables

```
Task: Implement user authentication
Context: We're building an MVP and need basic auth before launch
Requirements:
- JWT tokens with refresh mechanism
- Password hashing with bcrypt
- Rate limiting on login attempts
- Unit tests for auth functions
Output: Implementation with tests, ready to commit
```

---

## Feature Development Prompts

### New Feature
```
Implement [feature description].

Context:
- This is for [user type / use case]
- Related code is in [files/directories]

Requirements:
- [Specific requirement 1]
- [Specific requirement 2]
- Follow patterns in [reference file]
- Include tests

Keep diffs under 200 lines. Start with a plan.
```

### Add to Existing
```
Add [functionality] to [component/module].

Current behavior: [describe]
Desired behavior: [describe]

Constraints:
- Don't break existing tests
- Maintain backward compatibility
- Follow existing patterns in this file
```

---

## Bug Fixing Prompts

### Debug Error
```
I'm seeing this error:

[paste error message/stack trace]

This happens when [describe reproduction steps].

Expected: [what should happen]
Actual: [what happens instead]

Investigate the root cause and fix it.
```

### Fix with Context
```
Bug: [brief description]
File: [file path]
Line: [approximate location]

Symptoms:
- [symptom 1]
- [symptom 2]

I've tried:
- [what you've tried]

Find and fix the issue, add a test to prevent regression.
```

---

## Code Review Prompts

### Review Changes
```
Review my changes in [file/directory]:

Focus on:
1. Logic correctness
2. Edge cases
3. Error handling
4. Performance implications
5. Security concerns

Provide specific feedback with file:line references.
```

### Pre-Commit Check
```
I'm about to commit these changes. Check for:
- Security vulnerabilities
- Missing error handling
- Unhandled edge cases
- Code that doesn't match project style
- Missing tests for new functionality

If issues found, list them. Otherwise confirm ready to commit.
```

---

## Refactoring Prompts

### Safe Refactor
```
Refactor [function/class/module] to [goal].

Constraints:
- Keep all tests passing
- Don't change public API
- Make incremental changes
- Document any breaking changes

Start by writing tests for current behavior if missing.
```

### Extract Pattern
```
Extract [functionality] from [location] into [new location].

The extracted code should:
- Be self-contained
- Have clear inputs/outputs
- Include its own tests
- Be documented

Show me the plan before implementing.
```

---

## Testing Prompts

### Add Tests
```
Add tests for [function/component/module].

Cover:
- Happy path
- Error cases
- Edge cases
- Boundary conditions

Follow existing test patterns in [test file reference].
```

### Test-First
```
I need to implement [feature].

Before writing code:
1. Write failing tests that define the expected behavior
2. Show me the tests
3. Then implement to make them pass
```

---

## Documentation Prompts

### Generate Docs
```
Document [function/class/API]:

Include:
- Purpose and use case
- Parameters with types
- Return value
- Example usage
- Any gotchas or limitations

Use [JSDoc/docstring/markdown] format.
```

### README Update
```
Update the README to reflect recent changes:
- [Change 1]
- [Change 2]

Keep it concise. Update installation, usage, and API sections as needed.
```

---

## Exploration Prompts

### Understand Codebase
```
I'm new to this codebase. Help me understand:
1. Project structure and architecture
2. Key entry points
3. How [specific feature] works
4. Main dependencies and their roles

Start with a high-level overview, then drill into [area of interest].
```

### Find Code
```
Find where [functionality] is implemented.

I need to understand:
- Which files are involved
- The data flow
- Key functions and their responsibilities

Show me the relevant code paths.
```

### Trace Execution
```
Trace the execution path for [user action].

From [entry point] to [end result]:
- What functions are called?
- What data is passed?
- Where could issues occur?
```

---

## Git & Workflow Prompts

### Commit Message
```
Review my staged changes and write a commit message.

Follow conventional commits format:
type(scope): description

Include a body if changes are significant.
Don't include files that shouldn't be committed.
```

### PR Description
```
Create a PR description for my changes:

Include:
- Summary of changes (2-3 sentences)
- What problem this solves
- How it was tested
- Any notes for reviewers
```

---

## Performance Prompts

### Optimize
```
This code is slow: [paste code or file reference]

Profile and identify bottlenecks.
Suggest optimizations with expected impact.
Implement the most impactful improvements.
Don't sacrifice readability for micro-optimizations.
```

### Review Performance
```
Review [function/module] for performance issues:

Check for:
- N+1 queries
- Unnecessary iterations
- Memory leaks
- Blocking operations
- Missing caching opportunities
```

---

## Advanced Patterns

### Multi-Step Task
```
I need to [complex task].

Break this into steps:
1. List the steps needed
2. Wait for my approval
3. Execute one step at a time
4. Verify each step before proceeding

Start with the plan.
```

### Constrained Changes
```
Make this change: [description]

Constraints:
- Only modify [specific files]
- Don't change [protected areas]
- Keep changes minimal
- Preserve existing behavior for [cases]
```

### Compare Approaches
```
I need to implement [feature].

Compare these approaches:
1. [Approach A]
2. [Approach B]

For each, explain:
- Pros and cons
- Complexity
- Maintenance burden
- Performance implications

Recommend one with justification.
```

---

## Anti-Patterns to Avoid

### Too Vague
```
❌ "Fix the bug"
❌ "Make it better"
❌ "Add tests"
```

### Missing Context
```
❌ "Why doesn't this work?" [no code shown]
❌ "Implement auth" [no requirements]
```

### Too Broad
```
❌ "Build the entire feature"
❌ "Refactor everything"
```

---

## Tips for Better Results

1. **Be specific** - Include file paths, function names, exact requirements
2. **Provide context** - Explain the "why" behind requests
3. **Set constraints** - Lines of code limits, patterns to follow
4. **Request format** - Specify how you want the output
5. **One thing at a time** - Break complex tasks into steps
6. **Show examples** - Reference existing code patterns
7. **Iterate** - Refine based on initial results

---

## Resources

- [Getting Good Results](https://www.dzombak.com/blog/2025/10/getting-good-results-from-claude-code-writing-good-prompts/)
- [Claude Best Practices](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-4-best-practices)
- [Anthropic Engineering Guide](https://www.anthropic.com/engineering/claude-code-best-practices)
- [awesome-claude-prompts](https://github.com/langgptai/awesome-claude-prompts)
