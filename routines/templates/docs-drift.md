# Docs Drift Detection Routine

## Overview

Catch documentation that falls out of sync with the code by scanning recent changes and cross-referencing docs.

## Configuration

| Setting | Value |
|---|---|
| **Trigger** | Schedule - Weekly (Mondays at 8:00 AM) |
| **Connectors** | GitHub |
| **Repositories** | Repos with documentation |
| **Run time** | ~5-10 minutes |

## Prompt

```
Scan for documentation that has drifted from the code in the last 7 days.

1. IDENTIFY CHANGES - Find all PRs merged in the last 7 days that changed:
   - API endpoints or route definitions (controllers, routers, handlers)
   - Configuration options or environment variables
   - Public function signatures, class interfaces, or exported types
   - Database schema files or migration files
   - CLI commands or flags
   - Authentication/authorization requirements

2. CROSS-REFERENCE DOCS - For each changed area, check:
   - README.md sections that reference the changed code
   - API documentation (OpenAPI/Swagger specs, doc comments, API guides)
   - Configuration guides and environment variable docs
   - Architecture decision records (ADRs) in docs/ or architecture/
   - Inline code comments that describe the changed behavior
   - CHANGELOG.md or release notes

3. FOR EACH DRIFT FOUND:
   - Open a documentation update PR with the suggested change
   - In the PR description, reference the original PR that caused the drift
   - Keep changes minimal and focused on accuracy, not style
   - Assign the PR to the author of the original code change

4. REPORT:
   - Total PRs scanned: [count]
   - Documentation drift found: [count]
   - Update PRs opened: [list with links]
   - Areas with no documentation at all: [list]

If no drift is detected, report "Documentation is in sync with code changes from the last 7 days" and exit.

RESTRICTIONS:
- Only open draft PRs for documentation updates
- Do not modify code files, only documentation
- Do not rewrite documentation style, only fix factual accuracy
```

## Customization

**API-first teams**: Add "Regenerate OpenAPI spec from code annotations and diff against the committed spec file."

**Regulated industries**: Add "Flag any changes to compliance-related documentation that weren't reviewed by the compliance team."
