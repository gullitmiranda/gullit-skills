---
name: engineering-workflow
description: Route engineering work through the right workflow, skills, and runtime. Use when the user asks how to approach work, starts ambiguous feature work, has multiple workstreams, needs a bug workflow, or wants to combine personal skills with Matt Pocock-style skills.
---

# Engineering Workflow

Use this skill to choose the workflow before doing substantial work.

If the user is starting from a handoff, plan, issue, docs, current workspace
state, or a broad "what should we do next?" question, use `workflow-intake`
first. `workflow-intake` decides whether work should continue in the current
thread or be routed to another agent/runtime.

## Quick Protocol

1. Classify the request:
   - Ambiguous feature or product idea.
   - Bug, regression, exception, or failing test.
   - Existing plan, issue, or PRD ready for execution.
   - Parallel workstreams.
   - Architecture improvement.
2. Choose the workflow from [workflows.md](workflows.md).
3. Choose the runtime using `agent-selection`.
4. Use `context-capsule` before handing work to another tool, thread, or agent.
5. Apply atomic skills as needed. Do not duplicate their instructions here.

## Default Routes

Routes may reference external skills from `mattpocock/skills`. The locally
maintained `grill-with-docs` is an exception; its upstream provenance and
self-contained support files are documented in [its README](../grill-with-docs/README.md).

### Ambiguous feature

```text
workspace-status
-> zoom-out (mattpocock/skills) or grill-with-docs
-> plan or to-prd (mattpocock/skills)
-> incremental-delivery or to-issues (mattpocock/skills)
-> agent-selection
-> git-worktree when isolation is needed
-> tdd (mattpocock/skills)
-> quality
-> pr when requested
```

### Bug or regression

```text
workspace-status
-> agent-selection
-> diagnose (mattpocock/skills)
-> regression test when possible
-> quality
-> pr when requested
```

### Existing plan

```text
read source artifact
-> agent-selection
-> git-worktree when requested or needed
-> incremental-delivery if scope is large
-> implementation
-> quality
-> pr when requested
```

### Parallel workstreams

```text
identify workstreams
-> assign owner/runtime
-> create context capsule per child
-> isolate branch/worktree when needed
-> execute independently
-> return distilled results
```

### Architecture improvement

```text
zoom-out (mattpocock/skills)
-> improve-codebase-architecture (mattpocock/skills)
-> grill-with-docs for durable decisions
-> incremental-delivery
-> agent-selection
-> implementation slice
```

## Rules

- Keep the main chat for decisions, supervision, and final synthesis.
- Use subagents for bounded exploration and parallel side questions.
- Use terminal/ACP/Pi-style agents for long-running or mechanical work.
- Keep local plans local; do not commit `.cursor/plans/`.
- Prefer vertical slices over broad horizontal phases.
- Treat external skills as dependencies to compose, not content to copy. The locally maintained `grill-with-docs` is the documented exception; see [its README](../grill-with-docs/README.md).

## References

- For workflow details, see [workflows.md](workflows.md).
- For context transfer rules, see [context.md](context.md).
