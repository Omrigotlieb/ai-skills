# Docs Drift Detection Routine

## Overview

Weekly scan that catches documentation that has fallen out of sync with code changes. Opens update PRs so docs stay accurate without manual tracking.

## Configuration

| Setting | Value |
|---|---|
| **Trigger** | Schedule - Weekly (Mondays at 8:00 AM) |
| **Connectors** | GitHub |
| **Repositories** | Your team's repos |
| **Run time** | ~3-5 minutes |

## Prompt

```
Scan for documentation that has drifted from the code.

1. Find all PRs merged in the last 7 days that changed:
   - API endpoints or route definitions
   - Configuration options or environment variables
   - Public function signatures or class interfaces
   - Database schema or migration files
   - CLI commands or flags

2. For each changed area, check if corresponding documentation exists and is up to date:
   - README.md sections referencing changed code
   - API documentation (OpenAPI specs, doc comments)
   - Configuration guides and .env.example files
   - Architecture decision records (ADRs)
   - Inline code examples in docs/

3. For each drift found:
   - Open a documentation update PR with the suggested change
   - Reference the original PR that caused the drift
   - Keep changes minimal and focused on accuracy

4. For missing documentation (new features with no docs):
   - Create an issue titled "Add documentation for [feature]"
   - Include what needs documenting and link to the source PR

If no drift is detected, report "Documentation is in sync with code." and exit.
```

## Customization

**For API-heavy projects**: Focus on OpenAPI spec drift by comparing endpoint definitions against the spec file.

**For public docs sites**: Add a check that linked URLs in documentation are not returning 404s.
