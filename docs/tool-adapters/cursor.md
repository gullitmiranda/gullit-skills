# Cursor Adapter

Cursor is the default environment for interactive planning, code review, and
multi-agent exploration.

## Use Cursor Main Chat For

- Product and architecture decisions.
- `grill-with-docs` sessions where the user is actively answering questions.
- Final synthesis across multiple workstreams.
- PR framing and review-oriented summaries.

## Use Cursor Subagents For

- Codebase reconnaissance.
- Parallel exploration of independent areas.
- Bounded review or research tasks.
- Side questions that should return a distilled answer.

Subagent prompt requirements:

- Include the workstream goal.
- Include the exact question to answer.
- Include relevant constraints.
- Ask for a concise result, evidence, and next action.

Do not ask subagents to return full logs unless logs are the evidence.

## Use Cursor Fork For

- A side branch that becomes the new primary path.
- Work that needs inherited context but should no longer burden the parent chat.
- Restarting an implementation path after a major design change.

Before forking, create or update a context capsule so the new thread has a
clean framing even if it inherits older context.

## Use Cursor Plans For

Cursor and Claude CLI plans belong under:

```text
.cursor/plans/<workstream>.plan.md
```

These are local operational state and must not be committed.

## Parent Chat Checklist

When using Cursor subagents or forks:

- Track which workstream each child owns.
- Track branch/worktree if edits are involved.
- Ask children to return changed files and validation evidence.
- Fold only durable decisions back into the parent context.
