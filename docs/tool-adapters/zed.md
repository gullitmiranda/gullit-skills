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

## Read-Only Review Profile

For the isolated review stage in `pr-delivery`, use a dedicated `Review` agent
profile rather than relying on prompt text alone. Its permissions must exclude
file edits and all Git or GitHub mutations: staging, commits, pushes, resets,
checkouts, branch changes, PR edits, review submission, comments, and thread
resolution.

Allow only read/search tools and a terminal sandbox restricted to inspection
commands such as `git diff`, `git show`, `git log`, and `rg`. The parent agent
must pass a compact context capsule with the PR URL, base SHA, head SHA,
relevant specification, standards paths, and expected return format. If the
runtime cannot enforce this profile, do not claim the review was isolated or
read-only.

## When Not To Use Zed

Prefer Cursor subagents when the task is a small side investigation that only
needs a one-paragraph answer.

Prefer a terminal/ACP/Pi-style agent when the task is long-running, mechanical,
or primarily driven by command loops.
