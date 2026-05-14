# Issue Triage

> `loop.md` template — triages and labels incoming GitHub issues.

## Usage

Use as a Cloud routine (nightly schedule) or Desktop scheduled task.

## Template

```markdown
Triage all GitHub issues opened since the last run.

For each issue:

1. **Categorize** — Apply one label:
   - `bug`: Describes broken behavior with reproduction steps
   - `feature`: Requests new functionality
   - `docs`: Documentation improvement or correction
   - `question`: Asks how to use something
   - `needs-triage`: Cannot determine category from description

2. **Assess priority** — Check which files/modules are referenced.
   If the issue affects a critical path (auth, payments, data pipeline),
   add the `priority:high` label.

3. **Assign** — If CODEOWNERS maps the affected files to a team member,
   assign them. Otherwise leave unassigned.

4. **Request info** — If the issue lacks reproduction steps or version
   info, comment asking for details. Do not label as `bug` until
   reproduction steps are provided.

After processing all issues, generate a summary:
- Total issues processed
- Breakdown by category
- High-priority items (list titles)
- Issues needing more info from reporter

If no new issues: "No new issues since last triage."
```

## When to use

- Open source projects with high issue volume
- Teams that want pre-groomed issue queues each morning
- Reducing time-to-first-response on bug reports
