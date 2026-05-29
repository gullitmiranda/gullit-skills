# Workflows

Workflows compose atomic skills into repeatable paths. They should guide the
agent without turning the repo into one rigid process.

## Available Workflows

- [Feature From Idea](feature-from-idea.md): turn an ambiguous feature idea into implemented, validated work.
- [Bug Diagnosis](bug-diagnosis.md): debug with a reproducible feedback loop before fixing.
- [Existing Plan To PR](existing-plan-to-pr.md): execute an already agreed plan through branch, validation, and PR.
- [Parallel Workstreams](parallel-workstreams.md): supervise multiple plans or side quests in one repo/workspace.
- [Architecture Improvement](architecture-improvement.md): find and execute architecture improvements without mixing them with feature work.

## Common Phases

```text
discover
-> plan
-> select agent/runtime
-> isolate
-> execute
-> validate
-> review/ship
```

Not every workflow uses every phase. Small tasks can skip straight to execution
when the goal, files, runtime, and validation are obvious.

## Workflow Rules

- Keep atomic skills under `skills/<name>/`.
- Use workflow docs to compose skills.
- Use `agent-selection` before substantial or long-running work.
- Use `context-capsule` before handing work to another tool, thread, or agent.
- Keep local plans local; do not commit `.cursor/plans/`.
- Prefer vertical slices over broad horizontal phases.
