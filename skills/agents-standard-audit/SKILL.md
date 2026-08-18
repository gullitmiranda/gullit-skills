---
name: agents-standard-audit
description: Audit a repo's conformance to its `.agents/AGENTS.md` standard, migrate legacy plans content, or refresh the local standard after it evolved. Use when the user asks to check plans structure, migrate `.cursor/plans`, or update the agents standard in a repo.
---

# Agents Standard Audit

Brings a repo into conformance with its local `.agents/AGENTS.md`. Runs only on explicit request — never as a precondition for other work.

## Hard Rules

- The repo's `.agents/AGENTS.md` is the spec. If absent, stop and offer setup instead.
- Migration goes through `plans/scratch/` — never reclassify legacy content in bulk.
- Preserve user work: move, never delete, unless the user confirms each deletion.
- `archived/` content is frozen: report violations, never edit archived files.

## Procedure

1. **Read the spec**: `.agents/AGENTS.md` (and `docs/AGENTS.md` if present).
2. **Check conformance** and collect violations:
   - `Status:` line disagrees with the containing bucket folder.
   - Missing `## Alternatives considered` outside scratch.
   - Standalone `.plan.md` (no `parent:`) in the tracked tree.
   - Suffix/granularity mismatch (`.slice.plan.md` without `parent:`, `.mission.plan.md` with `parent:`).
   - Ephemeral-looking content tracked; committed files under scratch paths.
3. **Legacy migration** (if asked): move `.cursor/plans` content into `plans/scratch/` as-is; promote individually only when the user directs.
4. **Spec refresh** (if asked): diff the repo's `.agents/AGENTS.md` against the current canonical template from the `agents-standard` skill; propose updates that preserve local adaptations — never overwrite them silently.
5. Report violations grouped by rule, with proposed fixes; apply only what the user approves.
