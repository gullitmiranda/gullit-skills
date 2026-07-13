# Feature From Idea

Use this workflow when the user starts with an ambiguous feature idea or a
problem statement that still needs domain alignment.

## Flow

```text
workspace-status
-> zoom-out when the code area is unfamiliar
-> grill-with-docs
-> plan or to-prd
-> incremental-delivery or to-issues
-> agent-selection
-> git-worktree when isolation is needed
-> tdd
-> quality
-> pr
```

## Steps

1. Understand the workspace.
   - Use `workspace-status` when multiple repos may be involved.
   - Identify the target repo and current git state.

2. Build the code and domain map.
   - Use `zoom-out` if the code area is unfamiliar.
   - Use `grill-with-docs` when terminology, domain rules, or decisions are fuzzy.
   - Update `CONTEXT.md` or ADRs only when the skill's rules say to.

3. Produce a plan artifact.
   - Use `plan` for local operational planning.
   - Use `to-prd` when the result should become a durable issue-tracker artifact.

4. Split into vertical slices.
   - Use `incremental-delivery` for PR sequencing and validation.
   - Use `to-issues` when slices should become independently pickable issues.

5. Choose the runtime.
   - Use `agent-selection`.
   - Keep discussion in the main chat.
   - Use subagents for exploration.
   - Use terminal/ACP/Pi-style agents for long implementation.

6. Implement.
   - Use `git-worktree` when work must be isolated.
   - Use `tdd` for behavior-first implementation.
   - Keep each slice reviewable.

7. Close the slice.
   - Run `quality`.
   - Use `pr` when a pull request is requested.
   - Return validation evidence and remaining risks.

## Expected Outputs

- Clear domain terms and decisions.
- A local plan or PRD.
- Vertical slices with dependencies.
- Runtime recommendation.
- Implementation with tests or documented validation.
- PR-ready summary when requested.
