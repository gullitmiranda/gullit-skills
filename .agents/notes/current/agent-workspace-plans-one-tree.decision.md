# Agent workspace plans one tree

Status: accepted

Supersedes [agent-workspace-plans-dual-home.decision.md](agent-workspace-plans-dual-home.decision.md). Amends [agent-workspace-revamp.decision.md](agent-workspace-revamp.decision.md) for local plan location only. Notes, scratch, and tracking rules from the revamp decision remain in force.

## Purpose

Keep Cursor Plan Mode / UI working through `.cursor/plans` without allowing two independent plan directories. Dual independent homes risk split plans; a single physical tree with an optional compatibility symlink avoids that.

## Decisions

- `.agents/plans/` is the only physical local plan tree.
- `.cursor/plans` may exist only as a compatibility symlink to that tree (typically `../.agents/plans`), so Cursor resolves the same files.
- Agents may read or edit through either path when they resolve to the same tree.
- Create and archive plans under `.agents/plans/` (including `.archived/`).
- Never create a second real plan directory. If both paths are real directories, stop and ask to unify before writing.
- Create, repair, or migrate the symlink only with explicit user direction.
- Publishable content must never link to either path (`publish-safe-links`).

## Non-goals

- Does not make the plan tree tracked or publishable.
- Does not auto-migrate existing real `.cursor/plans/` trees without explicit approval.
- Does not change note lifecycle under `.agents/notes/`.

## Outcome

Skills, templates, repository `AGENTS.md`, and workflow docs describe one physical plan tree plus an optional Cursor-facing symlink, not two independent homes.
