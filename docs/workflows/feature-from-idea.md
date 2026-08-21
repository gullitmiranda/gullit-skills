# Feature From Idea

Use this workflow when a feature idea or problem statement still needs domain alignment.

## Flow

```text
work-intake
-> workspace-status
-> grill-with-docs when terms or decisions are unclear
-> plan
-> incremental-delivery when independent deliveries are needed
-> agent-selection
-> git-worktree when isolation is needed
-> build-plan
-> quality
-> pr when requested
-> work-closeout when requested
```

## Steps

1. Understand the workspace and target repository.
2. Clarify domain terms, behavior, and material trade-offs before execution.
3. Create one ready local implementation plan with `plan`.
4. Use `incremental-delivery` only when the work needs independently reviewable deliveries.
5. Select the runtime and isolation level with `agent-selection` and `git-worktree`.
6. Execute the ready contract with `build-plan`, validate it with `quality`, and use `pr` only when requested.
7. Use `work-closeout` when the user wants to assess, archive, discard, or distill the local plan.

## Expected outputs

- Clear domain terms and decisions.
- A ready local plan under `.agents/plans/` when planning is needed.
- Independent deliveries only when justified.
- Validation evidence and remaining risks.
