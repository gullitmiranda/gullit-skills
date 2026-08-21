# Existing Plan To PR

Use this workflow when the user has a ready local plan, issue, or clear task and wants execution rather than discovery.

## Flow

```text
work-intake
-> plan when the source needs refinement
-> agent-selection
-> git-worktree when requested or needed
-> incremental-delivery when scope needs independent deliveries
-> build-plan
-> quality
-> pr when requested
-> work-closeout when requested
```

## Steps

1. Read the source and verify whether it is a ready local plan, tracked note, legacy input, or non-plan request.
2. Create or refine one local plan with `plan` unless the source is already a ready local implementation plan. Resolve execution-relevant product, scope, or architecture decisions before implementation.
3. Choose the runtime and isolate work when needed.
4. Execute the ready contract with `build-plan`; use `incremental-delivery` only for independently reviewable deliveries.
5. Run the appropriate validation and use `pr` only when the user requests a pull request.
6. Use `work-closeout` when the user wants to assess or change the local plan after implementation.

## Expected outputs

- Implemented scope aligned with the source contract.
- Validation evidence and remaining risks.
- A pull-request-ready branch or created pull request only when requested.
