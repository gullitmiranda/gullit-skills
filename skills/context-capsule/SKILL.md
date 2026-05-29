---
name: context-capsule
description: Create a portable context capsule for subagents, forks, Zed threads, terminal agents, ACP/Pi-style agents, handoff, or later resume. Use before transferring work across tools or when managing parallel workstreams.
---

# Context Capsule

Create the smallest useful context package that lets another agent continue
without reading the whole conversation.

## When To Use

Use before:

- Launching a subagent for a bounded workstream.
- Forking a conversation.
- Starting a new Zed thread.
- Handing work to a terminal, ACP, or Pi-style agent.
- Pausing work for later.
- Returning a side investigation to the parent chat.

Do not use full transcript transfer unless exact conversational history matters.

## Process

1. Identify the target audience:
   - Parent chat.
   - Child subagent.
   - Forked conversation.
   - Zed thread.
   - Terminal/ACP/Pi-style agent.
   - Future resume.
2. Include only context needed for the next action.
3. Preserve durable decisions and constraints.
4. Mark validation as stale unless it was run in the current session or is immutable CI evidence.
5. End with one recommended next action.

## Output Format

Use [template.md](template.md).

Keep the capsule concise. Prefer links, paths, branch names, issue numbers, and
validation commands over raw transcript excerpts.

## Rules

- Do not include secrets or private credentials.
- Do not include work-only information in personal or public repositories unless it is explicitly safe.
- Do not over-preserve stale implementation details.
- Do not hide blockers; make them explicit.
- For child agents, state the expected return format.
