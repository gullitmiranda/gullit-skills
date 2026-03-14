---
name: plan
description: Create or update project plans. Use when the user asks to create a plan, update a plan, or break down work into a plan (in or out of plan mode). Always use standard plan format and location so plans are consistent.
---
# Plan

When creating or updating plans (in plan mode or in normal chat):

1. **Location**: Save plan files in `.cursor/plans/`. Do not create plan files in the workspace root or ad-hoc locations.
2. **Format**: Use the standard plan format (`.plan.md` extension) and the same structure Cursor uses for native plans (e.g. tasks in the expected plan format), so plans are consistent whether generated in plan mode or not.
3. **Structure**: Objective, Tasks, Dependencies, Acceptance Criteria, Notes (markdown with clear sections). Match the task/todo format of `.plan.md` plans.
4. **Content**: Clear, actionable task breakdown; include dependencies and prerequisites.
5. **Never**: Add timelines, schedules, cronograms, or time estimates (unless the user explicitly asks for them).

If the user has not specified a filename, use a descriptive name with `.plan.md` extension (e.g. `my-feature.plan.md`). For full structure details, see the **workflow** skill (Planning Workflow section).
