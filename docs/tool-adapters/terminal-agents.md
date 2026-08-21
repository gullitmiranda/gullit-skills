# Terminal And ACP Agent Adapter

Terminal, ACP, and similar agents are best when the work is long-running,
mechanical, or primarily validated by commands.

## Use Terminal Or ACP Agents For

- Long implementations with many file edits.
- Large mechanical migrations.
- Test-harness-driven bug diagnosis.
- Repeated command loops.
- Work that should not pollute an IDE conversation.
- Isolated execution in a dedicated branch or worktree.

## Handoff Input

Always provide a context capsule. For implementation work, include:

- Repository and worktree path.
- Branch name and base branch.
- Goal and acceptance criteria.
- Relevant files or modules.
- Constraints and forbidden actions.
- Commands already run.
- Required validation.

## Expected Return

Ask the agent to return:

- Summary of changes.
- Changed files.
- Commands run and outcomes.
- Validation evidence.
- Blockers or risks.
- Suggested next action.

## Safety Rules

- Do not hand off ambiguous work without a context capsule.
- Do not send secrets or private credentials in a capsule.
- Prefer a separate worktree for long or parallel implementation.
- Treat validation as stale unless it was run by the executing agent or comes from immutable CI evidence.

## When Not To Use Terminal Agents

Prefer the main chat when the next step is a decision or user interview.

Prefer an IDE agent when the next step depends on visual review, tight editor
feedback, or manual inspection.
