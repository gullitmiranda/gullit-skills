---
name: plan
description: Create or update project plans. Use when the user asks to create a plan, update a plan, or break down work into a plan (in or out of plan mode). Always use standard plan format and location so plans are consistent.
---
# Plan

When creating or updating plans, check which tool you are before choosing the location and format.

## Routing by tool

| Tool | Location | Format/extension | Committed? |
|------|----------|-----------------|------------|
| **Cursor** | `.cursor/plans/<name>.plan.md` | `.plan.md` — integrates with Cursor plan UI | No — gitignored; NEVER commit |
| **Claude CLI** | `.cursor/plans/<name>.plan.md` | `.plan.md` | No — gitignored; NEVER commit |
| **Factory / Droid** | `.factory/orchestrator/<name>.md` | Plain `.md` | Yes — committed alongside code |

**Decision rule:** If you are Cursor or Claude CLI, use `.cursor/plans/` with `.plan.md`. If you are Factory/Droid, use `.factory/orchestrator/` with plain `.md`. Never create plan files in the workspace root, `tmp/`, or any ad-hoc location.

## Content (applies to all tools)

- **Structure**: Objective, Tasks, Dependencies, Acceptance Criteria, Notes
- **Content**: Clear, actionable task breakdown; include dependencies and prerequisites
- **Never**: Add timelines, schedules, cronograms, or time estimates (unless the user explicitly asks)

If the user has not specified a filename, use a descriptive name (e.g. `my-feature.plan.md` for Cursor, `my-feature.md` for Droid).
