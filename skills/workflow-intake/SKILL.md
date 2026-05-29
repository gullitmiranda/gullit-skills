---
name: workflow-intake
description: Analyze available context and recommend how to start or resume work. Use when the user has a handoff, plan, issue, docs, current workspace state, or asks what to do next before implementation. Produces workstreams, workflow choice, runtime recommendation, and a ready-to-paste next prompt when another agent/thread should execute.
---

# Workflow Intake

Use this skill at the start of a new chat, after a handoff, or whenever the
next step is unclear. It is an intake and routing step, not an implementation
step by default.

## Default Autonomy Preference

Prefer the next implementation step to be as autonomous as safely possible.

Autonomous execution is appropriate when:

- The goal and acceptance criteria are clear.
- The target repo, branch/worktree, and source artifact are known.
- The relevant decisions have already been made.
- The implementation can be validated with commands, tests, CI, or a clear review checklist.
- No immediate user judgment, domain grilling, product decision, or design choice is required.

Autonomous execution is not appropriate when:

- The next step is `grill-with-docs`, product discovery, or architecture decision-making.
- The agent needs the user to choose between meaningful trade-offs.
- The domain language or desired behavior is still ambiguous.
- The safe implementation boundary is unclear.
- Required access, credentials, data, or environment are missing.

When autonomous execution is appropriate, recommend the most autonomous viable
runtime and provide a ready-to-paste prompt or context capsule for that agent.
When it is not appropriate, recommend the collaborative discovery step first.

## Inputs

Accept any combination of:

- Handoff document.
- Plan or PRD.
- Issue or PR.
- Project docs.
- Current workspace state.
- Current branch/worktree.
- Local changes.
- Conversation context.
- User goal.

If no explicit artifact is provided, inspect the current workspace enough to
recommend the next step. Prefer fast, read-only inspection first.

## Process

1. Identify source context.
   - Read provided handoff, plan, docs, issue, or PR.
   - Inspect current repo, branch, worktree, and local changes when relevant.
   - Treat missing evidence as uncertainty, not proof.
2. Identify active workstreams.
   - Separate feature work, bug work, architecture work, cleanup, and open questions.
   - Mark each as active, blocked, done, stale, or needs-user-decision.
3. Choose the workflow.
   - Use `engineering-workflow` for workflow routing.
   - Use external workflow skills only when installed.
4. Choose execution mode.
   - Use `agent-selection`.
   - Decide whether to continue here, use a subagent, fork/new thread, Zed, or terminal/ACP/Pi-style agent.
   - Prefer autonomous implementation when the work is ready and safe.
   - Prefer collaborative discovery when questions or decisions remain.
   - Do not assume the current tool can launch another agent; provide a prompt when manual handoff is needed.
5. Prepare transfer context when needed.
   - Use `context-capsule` before handing work to another tool, thread, or agent.
   - Prefer capsules over full transcripts.
6. Stop before implementation unless the user explicitly asked to continue.

## Default Output

Use [output-template.md](output-template.md).

The most important section is `Execution Recommendation`. It must say whether
to execute in the current thread or route the work somewhere else, and whether
the next phase should be autonomous or collaborative.

## Rules

- Do not implement during intake unless explicitly asked.
- Keep the main chat as supervisor when work should happen elsewhere.
- Bias implementation-ready work toward autonomous execution.
- Do not force autonomy for discovery, grilling, or unresolved decisions.
- Recommend another runtime when it better fits the task shape.
- Generate a ready-to-paste prompt if the recommended runtime cannot be launched automatically.
- Keep recommendations grounded in inspected evidence.
- Do not claim checks, tests, PR status, or branch state unless verified.
