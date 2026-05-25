---
name: work-context-cleanup
description: Clean up and close out active work context using plans as the starting point. Use when the user mentions plan cleanup, cleaning plans, closing a conversation, ending a session, wrapping up work, or doing a general workspace/repo cleanup.
---

# Work Context Cleanup

Use this skill to organize the end of a work context. Plans are the anchor, but related branches, worktrees, PRs, issues, commits, validation status, and handoff notes matter too.

Default to a lightweight current-context cleanup. Only do a broad workspace or repo cleanup when the user explicitly asks for it.

## Modes

### Current Context Cleanup

Use by default when the user says things like:
- "cleanup plans"
- "clean up before we stop"
- "close this conversation"
- "wrap up this session"
- "maybe it is time to end this conversation"

Focus on the current conversation, current repository, current branch, and current worktree. Prefer fast, non-destructive inspection over a broad scan.

### General Workspace Cleanup

Use only when the user explicitly asks for a general cleanup of the repo or workspace.

Inspect all active plans in `.cursor/plans/` for the target repo or workspace, then correlate them with visible branches, worktrees, PRs, issues, and recent commits when evidence is available.

## Workflow

1. Confirm the target scope.
   - For a multi-repo workspace, identify the target repo before interpreting plans, branches, or PRs.
   - If scope is ambiguous, ask whether the user means the current context or a general cleanup.

2. Inspect plans.
   - Current-context mode: find plans related to the current branch, current task, current worktree, open files, or conversation context.
   - General mode: list active plans under `.cursor/plans/`, excluding `.cursor/plans/.archived/`.

3. Correlate related work.
   - Check for branch, worktree, PR, issue, commit, validation, or handoff references in each relevant plan.
   - Use non-destructive commands and read-only service calls unless the user asks for a change.
   - Treat missing evidence as uncertainty, not proof that work is complete.

4. Classify each context or plan.
   - `active`: still represents ongoing work.
   - `done`: appears complete and ready to close out.
   - `stale`: likely outdated, but not clearly replaced.
   - `superseded`: replaced by a newer plan, branch, PR, or documented direction.
   - `needs-user-decision`: cleanup would require judgment or a state-changing action.

5. Recommend the smallest useful action.
   - Keep active plans active.
   - Update handoff notes only when useful for continuing later.
   - Suggest PR metadata sync if the PR no longer matches the current diff.
   - Suggest archiving done or superseded plans.
   - Ask before taking any ambiguous or state-changing action.

6. Archive through the dedicated skill.
   - When a plan should be archived, use the `plan-archive` skill.
   - Preserve historical content. Do not delete plans.

## Guardrails

- Never delete plans.
- Never archive a plan without clear user intent or confirmation.
- Never remove a worktree, close a PR, delete a branch, commit, push, reset, or change remote state just because cleanup was requested.
- Never commit files under `.cursor/plans/`.
- Do not claim tests, checks, or PR status are green unless verified in the current session.
- Keep cleanup output short. This skill is for closing context, not producing a long report.
- Do not compress multiple contexts into one generic list. Preserve traceability between each plan, branch, worktree, PR, and recommended action.

## Final Response

Use an adaptive handoff.

For a simple current-context cleanup, end with:

```markdown
## Cleanup Summary
- Ready to close: <what is complete>
- Still active: <plans, PRs, branches, or worktrees that should remain open>
- Suggested cleanup: <archives, PR syncs, handoff updates, or decisions needed>
- Next conversation: <the best starting point if work continues later>
```

For multiple plans, branches, worktrees, or PRs, group the result by context:

```markdown
## Cleanup Summary
Overall: <one-line state of the workspace or work context>

## Contexts
### <plan, branch, PR, or worktree name>
- Status: active | done | stale | superseded | needs-user-decision
- Related work: <plan, branch, worktree, PR, issue, or commit references>
- Evidence: <what was checked>
- Recommended action: <keep active, archive plan, sync PR, update handoff, or ask user>

### <next context>
- Status: <classification>
- Related work: <references>
- Evidence: <what was checked>
- Recommended action: <next action>

## Decisions Needed
- <user confirmations required before any state-changing cleanup>

## Next Conversation
Start from: <best plan, branch, PR, worktree, or next command>
```

If there is nothing to clean up, say so directly and mention any residual uncertainty.
