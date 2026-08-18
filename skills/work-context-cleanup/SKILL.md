---
name: work-context-cleanup
description: Clean up and close out active work context using plans as the starting point. Use when the user mentions plan cleanup, cleaning plans, closing a conversation, ending a session, wrapping up work, or doing a general workspace/repo cleanup.
---

# Work Context Cleanup

Close out a work context, using plans as the anchor and correlating branches, worktrees, PRs, issues, commits, validation status, and handoff notes.

## Hard Rules

- Never delete plans. Archive via the `plan-archive` skill, preserving historical content.
- Never archive a plan without clear user intent or confirmation.
- Never remove a worktree, close a PR, delete a branch, commit, push, reset, or change remote state just because cleanup was requested.
- Never commit files under `.cursor/plans/`.
- Do not claim tests, checks, or PR status are green unless verified in the current session.
- Default to a lightweight current-context cleanup. Broad workspace/repo cleanup only when the user explicitly asks.
- Ask before any ambiguous or state-changing action.

## Modes

- **Current Context Cleanup** (default): current conversation, repo, branch, worktree. Fast, non-destructive inspection.
- **General Workspace Cleanup** (explicit ask only): inspect all active plans in `.cursor/plans/` (excluding `.archived/`) and correlate with branches, worktrees, PRs, issues, recent commits.

## Workflow

1. **Confirm scope** — in a multi-repo workspace, identify the target repo first; ask if current-context vs general is ambiguous.
2. **Inspect plans** — current mode: plans tied to current branch/task/worktree/conversation; general mode: active plans under `.cursor/plans/`.
3. **Correlate related work** — branch, worktree, PR, issue, commit, validation, handoff references per plan. Read-only commands only. Treat missing evidence as uncertainty, not proof of completion.
4. **Classify** each plan/context: `active` | `done` | `stale` | `superseded` | `needs-user-decision`.
5. **Recommend the smallest useful action** — keep active plans active; update handoff notes only when useful for resuming; suggest PR metadata sync when the PR no longer matches the diff; suggest archiving done/superseded plans via `plan-archive`.

## Final Response

Simple current-context cleanup:

```markdown
## Cleanup Summary
- Ready to close: <what is complete>
- Still active: <plans, PRs, branches, or worktrees that should remain open>
- Suggested cleanup: <archives, PR syncs, handoff updates, or decisions needed>
- Next conversation: <the best starting point if work continues later>
```

Multiple contexts — group by context, preserving traceability (no generic merged list):

```markdown
## Cleanup Summary
Overall: <one-line state>

## Contexts
### <plan, branch, PR, or worktree name>
- Status: active | done | stale | superseded | needs-user-decision
- Related work: <references>
- Evidence: <what was checked>
- Recommended action: <keep active, archive plan, sync PR, update handoff, or ask user>

## Decisions Needed
- <user confirmations required before any state-changing cleanup>

## Next Conversation
Start from: <best plan, branch, PR, worktree, or next command>
```

If there is nothing to clean up, say so directly and mention any residual uncertainty.
