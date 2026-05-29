# Bug Diagnosis

Use this workflow when the user reports a bug, regression, failing test,
exception, or performance problem.

## Flow

```text
workspace-status
-> agent-selection
-> diagnose
-> tdd for regression coverage when appropriate
-> quality
-> pr
```

## Steps

1. Confirm the target repo and symptom.
   - Use `workspace-status` if the workspace has multiple repos.
   - Restate the user-visible failure.

2. Choose the runtime.
   - Use IDE agent when reproduction needs interactive inspection.
   - Use terminal/ACP/Pi-style agent when the bug can be driven by a command loop, test harness, script, or replay.
   - Use a context capsule before handing the bug to another tool.

3. Build the feedback loop.
   - Use `diagnose`.
   - Do not start by guessing fixes.
   - Create the fastest deterministic signal available: failing test, script, curl command, browser harness, replay, or fixture.

4. Reproduce and minimize.
   - Confirm the loop shows the same bug the user described.
   - Minimize until the failure is sharp enough to debug.

5. Hypothesize and instrument.
   - Rank hypotheses.
   - Probe one variable at a time.
   - Tag temporary debug output so cleanup is easy.

6. Fix and prevent regression.
   - Add a regression test at the right interface when possible.
   - If no good test surface exists, record that as architecture friction.
   - Apply the smallest fix that addresses the proven cause.

7. Close out.
   - Re-run the original feedback loop.
   - Remove temporary instrumentation.
   - Run `quality`.
   - Use `pr` when requested.

## Expected Outputs

- Repro command or harness.
- Proven cause.
- Fix.
- Regression coverage or documented reason it was not possible.
- Validation evidence.
- Architecture follow-up if the code was hard to test.
