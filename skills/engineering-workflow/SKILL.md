---
name: engineering-workflow
description: Route engineering work through the right workflow, skills, and runtime. Use when the user asks how to approach work, starts ambiguous feature work, has multiple workstreams, needs a bug workflow, or wants to combine personal skills with Matt Pocock-style skills.
---

# Engineering Workflow

Choose the workflow before doing substantial work. If starting from a handoff,
plan, issue, docs, workspace state, or a "what should we do next?" question,
run `workflow-intake` first — it decides whether work continues here or is
routed elsewhere.

## Hard Rules

- Keep local plans local; do not commit `.cursor/plans/`.
- Treat external skills as dependencies to compose, not content to copy. The locally maintained `grill-with-docs` is the documented exception; see [its README](../grill-with-docs/README.md).
- Keep the main chat for decisions, supervision, and final synthesis; subagents for bounded exploration; terminal/ACP/Pi-style agents for long-running or mechanical work.

## Protocol

1. Classify the request: ambiguous feature, bug/regression, existing plan/PRD, parallel workstreams, or architecture improvement.
2. Pick the route below (details in [workflows.md](workflows.md)).
3. Choose the runtime using `agent-selection`.
4. Use `context-capsule` before handing work to another tool, thread, or agent.
5. Apply atomic skills as needed; do not duplicate their instructions here.

Routes may reference external skills from `mattpocock/skills`.

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

- Prefer vertical slices over broad horizontal phases.

## References

- For workflow details, see [workflows.md](workflows.md).
- For context transfer rules, see [context.md](context.md).
