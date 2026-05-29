# Zed Adapter

Zed is a good fit for clean-thread implementation and ACP-compatible agent
experiments, especially when the user wants to work in Zed as the primary
editor.

## Use Zed For

- Starting a clean thread from a context capsule.
- Interactive implementation with Zed as the active editor.
- Trying a different ACP or terminal-backed agent on the same workstream.
- Continuing work after Cursor context has become too noisy.

## Starting A Zed Thread

Use a context capsule as the opening message. Include:

- Goal.
- Current state.
- Branch or worktree.
- Relevant files.
- Constraints.
- Validation state.
- Next action.

Avoid pasting full transcripts unless exact wording matters.

## Switching From Cursor To Zed

Before switching:

1. Create or update the context capsule.
2. Confirm the target branch/worktree.
3. List pending validation.
4. State what result should come back to the parent chat.

When the Zed work finishes, return:

- Changed files.
- Commands run.
- Validation result.
- Remaining risks.
- Next recommended action.

## When Not To Use Zed

Prefer Cursor subagents when the task is a small side investigation that only
needs a one-paragraph answer.

Prefer a terminal/ACP/Pi-style agent when the task is long-running, mechanical,
or primarily driven by command loops.
