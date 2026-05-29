# Context And Runtime Rules

## Workstreams

Track each active workstream with:

- Goal.
- Source artifact.
- Branch or worktree.
- Current state.
- Decisions.
- Open questions.
- Validation state.
- Next action.

## Runtime Selection

Default choices:

- Main chat: user decisions, domain grilling, final synthesis.
- Subagent: bounded exploration and side questions.
- Fork or new thread: side path becomes the new main path.
- Cursor or Zed agent: focused implementation with IDE feedback.
- Terminal, ACP, or Pi-style agent: long-running, mechanical, or harness-driven work.
- Full transcript transfer: exact-history audit only.

## Context Transfer

Use `context-capsule` before:

- Handing work to a subagent.
- Starting a fork or new thread.
- Moving between Cursor, Zed, terminal agents, or Pi-style agents.
- Pausing work for later.

Use full transcript copy only when exact wording matters.

## Child Result Contract

Ask child agents to return:

- What they did.
- What they found or changed.
- Files or artifacts touched.
- Validation evidence.
- Blockers and risks.
- Recommended next action.
