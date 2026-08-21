# Architecture Improvement

Use this workflow when the code is becoming hard to understand, test, change, or delegate.

## Flow

```text
work-intake
-> workspace-status
-> inspect modules, callers, interfaces, and test surfaces
-> grill-with-docs for durable terminology or trade-offs
-> work-plan
-> incremental-delivery when multiple independent refactors are needed
-> agent-selection
-> build
-> quality
-> pr when requested
```

## Steps

1. Understand the target area and identify concrete sources of friction such as leaky interfaces, shallow modules, missing test surfaces, or low locality.
2. Use `grill-with-docs` when domain terminology or an architectural trade-off needs user alignment.
3. Create a ready local implementation plan with `work-plan`; do not treat a decision note as the execution contract.
4. Use `incremental-delivery` to keep independent refactor slices reviewable and testable.
5. Choose the runtime and isolation level, then execute with `build` and validate through the improved interface where possible.

## Expected outputs

- Architecture candidate summary.
- Durable note or documentation only when it captures lasting knowledge.
- Ready local plan and independently validated increments when needed.
- Validation evidence and remaining trade-offs.

## Avoid

- Mixing unrelated feature behavior into architecture cleanup.
- Introducing abstractions without a concrete locality or leverage gain.
- Re-litigating durable decisions without new evidence.
- Shipping prototype code as production code.
