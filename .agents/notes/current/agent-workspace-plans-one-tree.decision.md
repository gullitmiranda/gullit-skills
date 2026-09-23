# Agent workspace plans one tree

Status: accepted

Supersedes [agent-workspace-plans-dual-home.decision.md](../retired/agent-workspace-plans-dual-home.decision.md). Amends [agent-workspace-revamp.decision.md](agent-workspace-revamp.decision.md) for local plan location only. Notes, scratch, and tracking rules from the revamp decision remain in force.

The earlier form of this note made `.agents/plans/` the only physical directory, treated `.cursor/plans` as an optional symlink the other way, and required a question before linking or unifying. That ask is retired.

## Purpose

Keep one local plan directory, exposed at both `.agents/plans` and `.cursor/plans`, and let Cursor use `.cursor/plans` so plan formatting and Plan Mode apply.

## Decisions

- `.agents/plans` and `.cursor/plans` are the same ignored local plan tree. One path is a real directory; the other is a relative symlink. Either direction is valid.
- In Cursor, create, edit, and archive plans through `.cursor/plans`. Do not ask which path to use, and do not retarget the write to `.agents/plans`.
- Outside Cursor, use whichever path already exists. If neither exists, create `.agents/plans` as the real directory and symlink `.cursor/plans` to it.
- Before writing a plan, if the other path is missing, create the relative symlink. Do not ask.
- Never leave two real plan directories. If both are real, replace an empty one with a symlink; if both have files, keep one real directory, move non-colliding files into it, and symlink the other. Stop only when the same filename has different content.
- An older repository contract that says plans may be written only under `.agents/plans`, or that the symlink needs a separate question, does not override this.
- Publishable content must never link to either path (`publish-safe-links`).

## Non-goals

- Does not make the plan tree tracked or publishable.
- Does not change note lifecycle under `.agents/notes/`.

## Outcome

Skills, templates, repository `AGENTS.md`, and workflow docs describe one shared plan tree. In Cursor the write path is `.cursor/plans`.
