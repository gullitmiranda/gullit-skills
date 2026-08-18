---
name: agents-standard
description: Apply the agent workspace standard (`.agents/` plans lifecycle, scratch, docs taxonomy). Use when creating plans or decision notes in a repo without the standard, when asked to set up the standard in a repo, or when working in a repo that has `.agents/AGENTS.md`.
---

# Agents Standard

A structure for agent working artifacts: plans with lifecycle, decision notes, scratch, and docs taxonomy. Inspired by DeepSeek Harness's Agent Notes.

## Hard Rules

- `.agents/AGENTS.md` in the repo is the authority when it exists — defer to it over this skill.
- Setup never migrates legacy content by default.
- Never commit anything under a `scratch/` path.
- No empty placeholder folders or `.gitkeep` — folders appear with their first artifact.

## If the repo has no `.agents/AGENTS.md` (loose guidance)

Apply the spirit without imposing structure: plans carry a `Status:` line and `## Alternatives considered`; use the repo's existing plans location; keep ephemeral work out of git. Offer setup if the user asks for structure.

## Setup procedure (when the user asks)

1. Interview: does the project have consumer-facing docs? Which plan tools are used (Cursor `.cursor/plans`, others)? Any existing `.cursor/plans` content?
2. Create `.agents/AGENTS.md` adapted to the answers from the canonical template (`templates/agents-AGENTS.md`), `.agents/.gitignore` (`scratch/`, `plans/scratch/`), and `docs/AGENTS.md` if the project wants the docs taxonomy.
3. Create no empty lifecycle buckets — they appear with the first artifact.
4. Legacy `.cursor/plans` content: only touch if the user asks; default is leaving it alone.
5. Report what was created and what was deliberately skipped.

## Working in a repo with the standard

Read `.agents/AGENTS.md` first. Key mechanics: artifact type by suffix (`.mission.plan.md` / `.slice.plan.md` / `.plan.md` / note `.md`); lifecycle by folder (`proposed/ active/ implemented/ rejected/ archived/`, status must match); ephemeral tasks in `plans/scratch/`; promotion is moving the file; parent linkage via `parent:` frontmatter.
