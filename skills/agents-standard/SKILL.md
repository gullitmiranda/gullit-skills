---
name: agents-standard
description: Apply the agent workspace standard (`.agents/` plans lifecycle, scratch, docs taxonomy). Use when creating plans or decision notes in a repo without the standard, when asked to set up the standard in a repo, or when working in a repo that has `.agents/AGENTS.md`.
---

# Agents Standard

A structure for agent working artifacts: plans with lifecycle, decision notes, scratch, and docs taxonomy. Inspired by DeepSeek Harness's Agent Notes.

## Hard Rules

- `.agents/AGENTS.md` in the repo is the authority when it exists — defer to it over this skill.
- Never migrate legacy content without explicit user approval.
- Never commit anything under a `scratch/` path.
- No empty placeholder folders or `.gitkeep` — folders appear with their first artifact.
- `archived/` content is frozen: never edit.

## Mode 1: Guidance (repo has no `.agents/AGENTS.md`)

Apply the standard verbally, without creating structure:

- Plans carry a `Status:` line after the title and a `## Alternatives considered` section.
- Use the repo's existing plans location; keep ephemeral work (tasks, research scratch) out of git.
- Granularity by suffix: `.mission.plan.md` (roadmap), `.slice.plan.md` (executable cut, `parent:` frontmatter), `.plan.md` (task), `.md` (decision note).
- Lifecycle: `proposed → active → implemented | rejected → archived`; folder and `Status:` line must agree.
- Offer setup when the user wants the structure persisted.

## Mode 2: Setup (user asks to install the standard)

1. **Detect repo state**: existing `.cursor/plans` content? existing `docs/`? consumer-facing docs? existing AGENTS.md conventions?
2. **Propose, then confirm**: present the setup with best-guess options from the repo's reality. Ask only what can't be inferred — always including: migrate legacy content now, or leave it? Migration is opt-in, never default.
3. **Create** `.agents/AGENTS.md` adapted from `templates/agents-AGENTS.md` (drop sections the project doesn't need), `.agents/.gitignore` (`scratch/`, `plans/scratch/`), and `docs/AGENTS.md` if the project wants the docs taxonomy. No empty buckets.
4. **If migration approved**: move legacy `.cursor/plans` content into `plans/scratch/` as-is (no bulk reclassification); promote individually only as the user directs. If the repo has an outdated `.agents/AGENTS.md`, diff against `templates/agents-AGENTS.md` and update preserving local adaptations.
5. **Report** what was created, adapted, migrated, and deliberately skipped. Offer follow-up adjustments.

## Working in a repo with the standard

Read `.agents/AGENTS.md` first. Key mechanics: artifact type by suffix; lifecycle by folder with matching `Status:`; ephemeral tasks in `plans/scratch/`; promotion is moving the file; parent linkage via `parent:` frontmatter; when a slice closes, update the parent mission in the same change.
