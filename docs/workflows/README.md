# Workflows

Workflows compose atomic skills into repeatable paths without creating a second policy layer.

## Available workflows

- [Feature From Idea](feature-from-idea.md): turn an ambiguous feature into validated work.
- [Bug Diagnosis](bug-diagnosis.md): establish evidence before fixing a defect.
- [Existing Plan To PR](existing-plan-to-pr.md): execute a ready local plan or clear request.
- [Parallel Workstreams](parallel-workstreams.md): supervise independent work without collisions.
- [Architecture Improvement](architecture-improvement.md): improve a codebase without mixing unrelated feature work.
- [PR Delivery](pr-delivery.md): create, review, and watch a pull request when requested.

## Common phases

```text
work-intake
-> clarify or discover
-> work-plan
-> select runtime
-> isolate when needed
-> build
-> validate
-> review or ship when requested
-> work-closeout when closure is requested
```

Use `work-intake` for a handoff, plan, issue, documentation, workspace state, or broad next-step question. It recommends the route and runtime; it does not imply implementation in the same thread.

Small tasks can proceed directly to `build` only when a ready local implementation plan already defines scope, decisions, runtime, and validation. Otherwise create or refine the plan with `work-plan` first.

## Workflow rules

- Compose atomic skills; do not duplicate their policy in workflow documentation.
- Use `agent-selection` before substantial or long-running work.
- Use `context-capsule` before handing work to another tool, thread, or agent.
- Keep implementation plans local under `.agents/plans/`; never commit them.
- Prefer vertical slices over broad horizontal phases.
