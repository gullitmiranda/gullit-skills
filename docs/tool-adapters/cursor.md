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


## Worktrees

### Recommend Cursor creation before generic Git

When an implementation plan needs an isolated worktree and no user,
`WORKSPACE.md`, or repository `AGENTS.md` path convention applies, recommend
Cursor's native worktree workflow before generic Git creation:

- create or move the task into a worktree from the Agents Window;
- use `/worktree` in the IDE; or
- use `agent --worktree` in the CLI.

Verify the resulting checkout with `git worktree list` and the expected branch
and base before implementation. State that generic Git creation remains the
default if the user continues without selecting Cursor's workflow; do not wait
for confirmation or delay autonomous implementation.

### Use generic creation when path policy wins

When the user, `WORKSPACE.md`, or repository `AGENTS.md` requires a worktree
location, create it through the generic Git workflow at that path. Then open a
Cursor project or agent session rooted in that checkout when the user wants
native file tools. If the user does not switch context, continue in the current
workflow. Do not claim that Cursor automatically attaches an arbitrary existing
worktree in its UI.

Cursor-managed worktrees are subject to its configured cleanup and retention
rules. Review those settings before treating a managed checkout as durable. See
[Cursor worktrees](https://cursor.com/docs/configuration/worktrees) and
[CLI worktrees](https://cursor.com/docs/cli/using#cli-worktrees).

## Parent Chat Checklist

When using Cursor subagents or forks:

- Track which workstream each child owns.
- Track branch/worktree if edits are involved.
- Ask children to return changed files and validation evidence.
- Fold only durable decisions back into the parent context.
