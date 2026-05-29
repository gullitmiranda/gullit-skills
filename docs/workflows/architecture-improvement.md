# Architecture Improvement

Use this workflow when the code is becoming hard to understand, test, change, or
delegate to agents.

## Flow

```text
workspace-status
-> zoom-out
-> improve-codebase-architecture
-> grill-with-docs for durable decisions
-> incremental-delivery
-> agent-selection
-> implementation slice
-> quality
-> pr
```

## Steps

1. Understand the area.
   - Use `workspace-status` when multiple repos may be involved.
   - Use `zoom-out` for a map of modules, callers, and domain concepts.

2. Find architecture candidates.
   - Use `improve-codebase-architecture`.
   - Look for shallow modules, leaky interfaces, missing test surfaces, and low locality.
   - Do not propose broad rewrites as the default.

3. Decide what matters.
   - Use `grill-with-docs` when the candidate depends on domain terminology or a durable trade-off.
   - Record glossary terms or ADRs only when the external skill's criteria are met.

4. Split the work.
   - Use `incremental-delivery`.
   - Keep refactor slices separate from feature behavior when possible.
   - Make each slice independently reviewable and testable.

5. Choose runtime and isolation.
   - Use `agent-selection`.
   - Use subagents for exploration.
   - Use terminal/ACP/Pi-style agents for large mechanical refactors.
   - Use worktrees for parallel or risky edits.

6. Validate.
   - Prefer tests through the improved interface.
   - Run `quality`.
   - Use `pr` when requested.

## Expected Outputs

- Architecture candidate summary.
- Decision record when needed.
- Incremental implementation plan.
- Clear test surface.
- Validation evidence.

## Anti-Patterns

- Mixing architecture cleanup with unrelated feature work.
- Creating new abstractions without a concrete locality or leverage gain.
- Re-litigating existing ADRs without new evidence.
- Shipping prototype code as production code.
