# ai-skills star-growth refresh — design

Date: 2026-04-22
Owner: Omri Gotlieb
Status: Awaiting user review before implementation

## Context

`ai-skills` is a curated markdown repo of Claude Code skills, MCP server guides, `CLAUDE.md` templates, and workflows. User reference-compared it to `skillsdirectory.com` (a live marketplace, 36k+ skills). Product paths differ, so we are not trying to match breadth. Goal is to raise star-earning signal of the existing repo.

Journalist-read problems with current state:

1. Badges and copy claim "200+ skills," "150+ community," "125+ scientific," "15+ skills" — the bulk of which are links to upstream collections (`anthropics/skills`, `obra/superpowers`, `K-Dense-AI/claude-scientific-skills`), not content hosted here. A skeptical reader notices. On HN or Reddit, one callout tanks a launch.
2. Marketing voice is louder than substance ("Why This Repo Is Worth Starring," "Better Than A Link Dump"). High-star awesome lists are notably understated.
3. No unique asset. Templates, cheatsheet, MCP guides, skills catalog all exist elsewhere in comparable form. There is no single piece people will screenshot.

## Goals

1. Stop the overstatement. Every claim in the repo must be provable by reading the repo.
2. Ship one shareable flagship piece that fills a real gap in the ecosystem.
3. Tighten the README so the differentiator is clear in the first screenful.

## Non-goals

- Adding new top-level categories (Design, Writing, Marketing, Business) — rejected, dilutes identity.
- Claiming skills are "tested" or "verified" when we have not run them.
- Rewriting each category subdirectory README. Separate effort.
- Building a website / static site. Stays a markdown repo.

## The three changes

### Change 1 — README overhaul (moderate-aggressive)

**Remove:**
- "Why This Repo Is Worth Starring" section.
- "Better Than A Link Dump" section.
- "Get Useful In 5 Minutes" section (pick-your-path table already does this job).
- Inflated badges with unverified counts.

**Keep:**
- Hero SVG and title.
- Pick Your Path table.
- What You Get table.
- Contribution Standard section.
- CI / license / PRs-welcome badges (these are real).

**Add:**
- Tight lede: one sentence that names what this repo is and the unique bar it holds. Working draft: *"A curated directory of Claude Code skills, MCP servers, and CLAUDE.md templates. External links are checked in CI; every entry notes when it was last verified."*
- "Links last verified: YYYY-MM-DD" line near the top.
- Prominent link to the flagship piece (Change 2).

### Change 2 — Flagship: `docs/skills-vs-mcp-vs-commands-vs-hooks.md`

A practical comparison of the four primary Claude Code extensibility primitives. Newcomers are genuinely confused about which to reach for, and no existing public piece nails it cleanly.

**Structure:**
1. One-paragraph lede.
2. Side-by-side comparison table: primitive, who invokes (model / user / event), where it lives, packaging, distribution, typical use case.
3. One worked example per primitive (minimal, copy-pasteable).
4. Decision matrix — "I want to X → reach for Y" with ~10 rows.
5. Honest trade-offs section: when each is the wrong choice.
6. Further reading links (official docs only).

**Accuracy requirement:** primitive behavior must be current as of 2026-04-22. Dispatch a research agent to pull current state from official Claude Code docs before drafting.

### Change 3 — Skills catalog honesty pass

Edits to `skills/README.md`:

- Remove "Latest Update: January 2026 - Added 200+ skills" line.
- Remove or rewrite "Official 15+ / Community 150+ / Scientific 125+" badges — if kept, they must state the honest in-repo count or be explicitly labeled as upstream counts.
- Remove "12+ / 10+ / 8+" etc. counts from the category table unless those match content that actually exists in each subdirectory README.
- Add a one-line header: *"This is a curated index of Claude Code skills. Most entries link to upstream collections — we don't rehost. Links last verified: YYYY-MM-DD."*
- Spot-check each link in the catalog during the edit; flag dead links for follow-up.

## Parallel work plan

Main thread (me):
- Write the README rewrite.
- Write the flagship comparison piece.
- Apply the honesty pass to `skills/README.md`.
- Run `python3 scripts/validate_docs.py` at the end.

Dispatched agents (research only, no writes):
- **Agent R1 — claims audit.** Walk `README.md`, `skills/README.md`, and each category subdirectory's README. For every numeric claim ("X+ skills," "Added N"), report honest count based on actual content. Return a table: claim → location → honest value → recommendation (remove / correct / leave).
- **Agent R2 — primitives fact-check.** Using the claude-code-guide subagent, pull current authoritative behavior of Skills, MCP servers, slash commands, and hooks from official Claude Code docs. Return a structured fact-sheet per primitive: invocation model, file format, location, lifecycle. Will seed the flagship piece.

Agents return structured notes; I write the final prose. Voice consistency requires single authorship.

## Done criteria

- README value prop is readable in one screenful without scrolling.
- `docs/skills-vs-mcp-vs-commands-vs-hooks.md` exists, links from README, and is accurate to 2026-04-22 behavior.
- No numeric claim in the repo exceeds what a reader can verify from the content.
- "Links last verified" dates present on README and `skills/README.md`.
- `python3 scripts/validate_docs.py` passes.

## Risks

- **Flagship quality gates everything.** If the comparison piece is mediocre, the repo looks the same but now with a thin flagship. Mitigation: fact-check via research agent, keep the piece tight, ship it only if it earns its link.
- **Tone shift may surprise.** Removing the cheerful marketing sections changes the repo's character. User signed off on moderate-aggressive; we stop there, we don't go cold.
- **Link rot on claims audit.** Agent R1 may surface dead links that need fixing. If volume is high, we fix the obvious ones and file issues for the rest rather than blocking this work.
- **"Honest counts" may look small.** If `skills/README.md` goes from "200+ skills" to "index of 60 links," the first impression dips before it lifts. Acceptable because the long-term signal is credibility.

## Open questions

None blocking. Proceeding on user approval of this spec.
