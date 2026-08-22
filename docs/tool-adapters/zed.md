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

## Worktrees

### Recommend Zed creation before generic Git

When an implementation plan needs an isolated worktree, recommend Zed's native
flow before generic Git creation when the user has a natural decision point:

1. Use the title-bar worktree picker or `git: worktree` to create or select the
   checkout.
2. Open or continue in that worktree project.
3. Start a thread in that project so its native file tools target the isolated
   checkout.

State that generic Git creation remains the default if the user continues
without choosing this flow. Do not wait for confirmation or delay autonomous
implementation.

Use generic Git creation when the user, `WORKSPACE.md`, or repository
`AGENTS.md` requires a path that Zed's managed flow cannot satisfy.

### Attach an externally created worktree only as a fallback

After generic Git creation, the recommended Zed path is to open the checkout as
an independent project, for example with `zed -n <worktree-path>`, then start a
new thread using a context capsule.

To retain the existing thread instead, use **File > Add Folder to Project** and
select the worktree. This broadens the current multi-root project to include
both checkouts, so the next prompt should name the exact root the agent may
edit. If the user chooses neither option, continue in the current thread with
the existing terminal workflow.

`zed -a` adds a separate project to the window's Threads Sidebar; it does not
add a root to the current project. Likewise, `agent.tool_permissions` controls
approval and `agent.sandbox_permissions.write_paths` controls terminal writes;
neither gives native file tools access to a path outside the project roots. See
[Windows & Projects](https://zed.dev/docs/windows-and-projects),
[Tool Permissions](https://zed.dev/docs/ai/tool-permissions), and
[Sandboxing](https://zed.dev/docs/ai/sandboxing).

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
