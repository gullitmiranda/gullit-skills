---
name: agents-standard
description: Apply the agent workspace standard (`.agents/` plans lifecycle, scratch, docs taxonomy). Use when creating plans or decision notes in a repo without the standard, when asked to set up the standard in a repo, or when working in a repo that has `.agents/AGENTS.md`.
---

# Agents Standard

A structure for agent working artifacts: plans with lifecycle, decision notes, scratch, and docs taxonomy. Inspired by DeepSeek Harness's Agent Notes.

## Hard Rules

- `.agents/AGENTS.md` in the repo is the authority when it exists — defer to it over this skill.
- Never migrate legacy content without explicit user approval.
- Treat `.cursor/plans/` and repository-declared scratch paths as local inputs: never move, promote, commit, or synchronize them implicitly.
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

Read `.agents/AGENTS.md` first. It defines the artifact types, lifecycle, tracking, and local-draft boundaries for that repository.

Before implementation, classify each input as a tracked lifecycle artifact, local draft or scratch, or non-plan input. Local material may inform execution but stays unchanged unless the user explicitly directs a promotion.

For an explicit request to implement a tracked executable plan, prepare the branch or worktree before changing `proposed` to `active`. Do not infer the contract of a tracked slice stub; return to planning or ask the user.

Close an `active` tracked slice only after its implementation is committed, validated, and reviewed. Move it to `implemented` with a matching `Status:` line and update its parent mission in the same change. `implemented` does not require a PR, merge, or release; record those references only when known. With `--no-commit`, leave the tracked plan `active` and report that closure remains pending.
