# Existing Plan To PR

Use this workflow when the user already has a plan, issue, PRD, or clear task
and wants execution rather than more discovery.

## Flow

```text
read existing plan or issue
-> agent-selection
-> git-worktree when requested or needed
-> incremental-delivery if scope is large
-> tdd or focused implementation
-> quality
-> pr
```

## Steps

1. Read the source artifact.
   - Use the existing issue, PRD, plan, or user request as the source of truth.
   - Do not re-plan from scratch unless the artifact is stale or ambiguous.

2. Check scope.
   - If it is small and clear, implement directly.
   - If it is large, use `incremental-delivery` to split it into reviewable slices.

3. Choose the runtime.
   - Use `agent-selection`.
   - Use Cursor or Zed for focused implementation with tight IDE review.
   - Use terminal/ACP/Pi-style agents for long mechanical work.
   - Use a context capsule for tool handoff.

4. Isolate work.
   - Use `git-worktree` when explicitly requested or when parallel work would be safer in a separate worktree.
   - Keep each branch focused.

5. Execute.
   - Use `tdd` when behavior can be tested first.
   - Keep changes aligned with the source artifact.
   - Avoid opportunistic refactors outside the slice.

6. Validate.
   - Run targeted checks during iteration.
   - Run the appropriate quality gate before handoff.
   - Do not claim validation that was not run.

7. Prepare PR.
   - Use `pr` when the user requests a PR.
   - Keep the PR title/body aligned with the actual diff.
   - Include validation evidence and risk notes.

## Expected Outputs

- Implemented slice or feature.
- Validation evidence.
- Updated source artifact only when appropriate.
- PR-ready branch or created PR when requested.
