# Bug Diagnosis

Use this workflow for a reported bug, regression, failing test, exception, or performance problem.

## Flow

```text
work-intake
-> workspace-status when repository context is unclear
-> establish a reproducible feedback loop
-> work-plan
-> agent-selection
-> build
-> quality
-> work-closeout when requested
```

## Steps

1. Confirm the target repository and user-visible symptom.
2. Create the fastest deterministic signal available: a failing test, script, request, browser harness, replay, or fixture.
3. Reproduce and minimize the failure before proposing a fix. Probe one variable at a time and keep temporary instrumentation easy to remove.
4. Create or refine one ready local implementation plan with `work-plan`, then execute the proven fix with `build`.
5. Re-run the original feedback loop, remove temporary instrumentation, and run `quality`.

## Expected outputs

- Reproduction evidence.
- A proven cause or explicitly bounded uncertainty.
- The smallest justified fix.
- Regression coverage when an appropriate test surface exists.
- Validation evidence and any follow-up architecture friction.
