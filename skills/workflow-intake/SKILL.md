---
name: workflow-intake
description: Analyze available context and recommend how to start or resume work. Use when the user has a handoff, plan, issue, docs, current workspace state, or asks what to do next before implementation. Produces workstreams, workflow choice, runtime recommendation, and a ready-to-paste next prompt when another agent/thread should execute.
---

# Workflow Intake

Intake and routing step for a new chat, a handoff, or an unclear next step.
Not an implementation step by default.

## Hard Rules

- Do not implement during intake unless explicitly asked.
- Do not move, promote, commit, or otherwise mutate a plan artifact during intake.
- Read `.agents/AGENTS.md` before selecting `plan` or `build-plan` when it exists; it is authoritative for plan location, format, lifecycle, and versioning.
- Do not claim checks, tests, PR status, or branch state unless verified.
- Keep recommendations grounded in inspected evidence.
- Do not assume the current tool can launch another agent; provide a ready-to-paste prompt when manual handoff is needed.

## Autonomy Preference

Bias implementation-ready work toward autonomous execution. Autonomous is appropriate when:

- Goal and acceptance criteria are clear.
- Target repo, branch/worktree, and source artifact are known.
- Relevant decisions have already been made.
- The implementation can be validated with commands, tests, CI, or a clear review checklist.
- No immediate user judgment, grilling, product decision, or design choice is required.

Autonomous is not appropriate when the next step is `grill-with-docs`, product discovery, or architecture decision-making; when the user must choose between meaningful trade-offs; when domain language or desired behavior is ambiguous; when the safe implementation boundary is unclear; or when required access, credentials, data, or environment are missing.

When autonomous is appropriate, recommend the most autonomous viable runtime plus a ready-to-paste prompt or context capsule. Otherwise recommend the collaborative discovery step first.

## Inputs

Accept any combination of: handoff document, plan/PRD, issue/PR, project docs, current workspace state, branch/worktree, local changes, conversation context, user goal. If no explicit artifact is provided, inspect the current workspace enough to recommend the next step; prefer fast, read-only inspection first.

## Plan Authority

For every potential plan input, inspect the repository standard before interpreting the artifact. Record the source path, governing authority, and one type:

- `tracked`: a lifecycle artifact in the authority's tracked plan tree; record its lifecycle state and parent.
- `local`: a `.cursor/plans/` or repository-declared scratch draft; it can inform work but remains local and unchanged.
- `non-plan`: a handoff, issue, PR, chat context, or other input with no plan lifecycle.

Also record whether durable tracking is needed, whether the execution contract is ready, and the next route. Route an explicit implementation request for a tracked, executable plan to `build-plan`; route a stub to `plan` or the user. A local draft may support an independently executable request, but must never be promoted or synchronized implicitly.

## Process

1. Identify source context: read provided artifacts; inspect the repo, branch, worktree, and local changes when relevant. For a potential plan, read `.agents/AGENTS.md` first and produce its Plan Authority classification. Treat missing evidence as uncertainty, not proof.
2. Identify active workstreams (feature, bug, architecture, cleanup, open questions); mark each active, blocked, done, stale, or needs-user-decision.
3. Choose the workflow via `engineering-workflow`; use external workflow skills only when installed. Detect by checking the session's available-skills list or the skill directories (`~/.agents/skills/`, `~/.cursor/skills/`).
4. Choose execution mode via `agent-selection` (continue here, subagent, fork/new thread, Zed, or terminal/ACP/Pi-style agent); prefer autonomous implementation when ready and safe, collaborative discovery when questions remain.
5. Prepare transfer context with `context-capsule` when handing work elsewhere; prefer capsules over full transcripts.
6. Stop before implementation unless the user explicitly asked to continue.

## Default Output

Use [output-template.md](output-template.md).

The most important section is `Execution Recommendation`. It must say whether
to execute in the current thread or route the work somewhere else, and whether
the next phase should be autonomous or collaborative.

## Rules

- Keep the main chat as supervisor when work should happen elsewhere.
- Recommend another runtime when it better fits the task shape.
- Generate a ready-to-paste prompt if the recommended runtime cannot be launched automatically.
