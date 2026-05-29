# Context Management

Context management is the discipline of moving only the useful part of a
conversation between agents, tools, workstreams, and future sessions.

The default artifact is a `context capsule`: a concise, portable summary that
can be pasted into any agent or used as the prompt for a subagent.

Use `workflow-intake` before creating a capsule when you are not sure which
workstream should continue or which runtime should execute it.

## Default Rule

Use the smallest context transfer that preserves correctness.

- Use a short note when the next agent only needs one fact.
- Use a context capsule when the next agent needs task state, constraints, and next actions.
- Use full transcript copying only when exact conversational history matters.

## Context Capsule Template

```markdown
# Context Capsule: <short title>

## Goal

What this workstream is trying to accomplish.

## Current State

What has already been discovered, decided, implemented, or ruled out.

## Relevant Artifacts

- Repo/workspace:
- Branch/worktree:
- Plan:
- Issue/PR:
- Important files:
- Commands already run:

## Decisions

- Decision 1 and why it matters.
- Decision 2 and why it matters.

## Constraints

- Safety, data-boundary, compatibility, rollout, or tool constraints.
- Things the next agent must not do.

## Open Questions

- Question 1.
- Question 2.

## Validation State

- Checks already run:
- Checks still needed:
- Known failures:

## Expected Return

What the receiving agent should report back.

## Recommended Next Action

The smallest useful next step.
```

## Workstreams

A workstream is an independently trackable piece of work inside a repository or
workspace. A single parent chat may supervise several workstreams in parallel.

Each workstream should be describable with:

- `id`: short stable name, such as `auth-session-cleanup`.
- `goal`: the outcome being pursued.
- `current_state`: what is true now.
- `artifacts`: plan, issue, PR, branch, worktree, docs, or prototype.
- `decisions`: durable choices already made.
- `open_questions`: unresolved questions that block or shape the work.
- `validation_state`: checks run, checks pending, and known failures.
- `next_action`: the next action another agent can take without guessing.

## Transfer Modes

### Main chat note

Use for tiny branches of discussion that fit in one or two sentences.

Good for:

- Confirming one file path.
- Reporting one subagent finding.
- Tracking a small decision.

### Context capsule

Use when work moves to another agent, another tool, or a future session.

Good for:

- Cursor subagent prompts.
- Cursor fork setup.
- Zed new thread summaries.
- Terminal, ACP, or Pi-style agents.
- Resuming after a long pause.

### Full transcript

Use only when exact wording matters.

Good for:

- Auditing how a decision was made.
- Debugging agent behavior.
- Preserving detailed product discussion that was not yet summarized.

Avoid using full transcripts as the default because they carry stale context,
unresolved branches, and irrelevant tool output.

## Parent Chat Responsibilities

The parent chat should keep the supervisory state:

- Which workstreams exist.
- Which agent/tool owns each active workstream.
- Which branch or worktree each workstream uses.
- Which decisions are durable.
- What result is expected back.

The parent chat should not absorb every side discussion. Ask child agents for
distilled findings, changed files, validation evidence, and next actions.

## Child Agent Responsibilities

Child agents should return:

- What they were asked to do.
- What they found or changed.
- Evidence: files, commands, tests, links, or screenshots.
- Remaining risks or blockers.
- The next recommended action.

They should not return raw logs unless the logs are the evidence.

## Staleness Rules

Before reusing a context capsule:

1. Check whether branch, worktree, issue, PR, or plan references still exist.
2. Re-read files that may have changed since the capsule was written.
3. Treat validation results as stale unless run in the current session or clearly tied to an immutable CI result.
4. Preserve durable decisions, but re-check implementation details.

## Relationship To Handoff

`handoff` and `context-capsule` overlap, but optimize for different moments:

- Use `handoff` when the current conversation is ending or context pressure is high.
- Use `context-capsule` whenever a specific workstream moves across agents or tools.

Many handoffs contain one or more context capsules.
