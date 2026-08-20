---
name: plan
description: Create or update project plans. Use when the user asks to create a plan, update a plan, or break down work into a plan (in or out of plan mode). Always use standard plan format and location so plans are consistent.
---
# Plan

Route plan work through repository policy before applying a runtime default.

## Hard Rules

- Read `.agents/AGENTS.md` first when it exists. It is authoritative for plan location, format, lifecycle, promotion, and versioning.
- Treat `.cursor/plans/` and repository-declared scratch paths as local drafts: they may inform a plan, but are never moved, promoted, committed, or synchronized implicitly.
- Never migrate an existing local draft into a tracked plan without an explicit user request.
- Never create plan files in the workspace root, `tmp/`, or any ad-hoc location.

## Routing

### 1. Repository standard

When `.agents/AGENTS.md` exists, follow its artifact types, entry lifecycle state, required format, parent linkage, and tracking rules. Create a new durable artifact only in the location and state it prescribes. Do not treat a request to plan as permission to promote a local draft; create or promote only as the user explicitly directs.

### 2. Runtime fallback

Use this table only when the repository has no agent-workspace standard:

| Tool | Location | Format/extension | Committed? |
|------|----------|-----------------|------------|
| **Cursor** | `.cursor/plans/<name>.plan.md` | `.plan.md` — integrates with Cursor plan UI | No — gitignored; never commit |
| **Claude CLI** | `.cursor/plans/<name>.plan.md` | `.plan.md` | No — gitignored; never commit |
| **Factory / Droid** | `.factory/orchestrator/<name>.md` | Plain `.md` | Yes — committed alongside code |

If the user has not specified a filename, use a descriptive name (for example, `my-feature.plan.md` for Cursor or `my-feature.md` for Droid).

## Content

Repository authority requirements override this fallback structure. Otherwise use Objective, Tasks, Dependencies, Acceptance Criteria, and Notes; keep tasks actionable and omit timelines, schedules, cronograms, and time estimates unless the user explicitly asks.
