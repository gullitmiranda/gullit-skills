# Zed Adapter

Zed is a good fit for clean-thread implementation and ACP-compatible agent
experiments, especially when the user wants to work in Zed as the primary
editor.

## Use Zed For

- Starting a clean thread from a context capsule.
- Interactive implementation with Zed as the active editor.
- Trying a different ACP or terminal-backed agent on the same workstream.
- Continuing work after Cursor context has become too noisy.

## Skill invocation compatibility

Use `work-plan` and `build` as public skill names. Do not assume `/plan` or `/build` is available as a skill command: Zed runtime configuration may reserve, reinterpret, or omit slash commands. The legacy `plan` and `build-plan` entries are compatibility-only.

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

## Review Boundaries

A native Zed `spawn_agent` child inherits its parent's profile and tool
capabilities. It cannot be assigned the `Review` profile or a stricter
permission/sandbox policy at spawn time. See
[the research note](../research/zed-subagent-profile-isolation.md) for the
source-backed limitation.

`pr-delivery` defaults to `auto`, which resolves to `guarded` in a native Zed
thread:

1. Before spawning the child, the parent verifies that local `HEAD` and remote
   PR head both equal the fixed review SHA, then records the clean
   worktree/index status and branch.
2. The child receives a compact capsule and explicit no-mutation, text-only
   instructions.
3. The parent verifies the same fixed-SHA and clean-worktree conditions after
   every child returns. Any difference stops the flow as
   `review-integrity-unknown`.

This is a policy guardrail, not a technically read-only reviewer. Never report
it as isolated or capability-enforced.

Use `pr-delivery --review-mode strict` only in a runtime that can technically
remove child write and GitHub mutation capabilities and run the same
fixed-revision checks. In Zed, strict isolation is unavailable to native
subagents. A separate top-level thread is an alternative only after its exact
profile, tool permissions, and sandbox settings have been verified to exclude
all mutation paths; a named `Review` profile alone is not sufficient and cannot
be selected by native subagent delegation.

## When Not To Use Zed

Prefer Cursor subagents when the task is a small side investigation that only
needs a one-paragraph answer.

Prefer a terminal/ACP/Pi-style agent when the task is long-running, mechanical,
or primarily driven by command loops.
