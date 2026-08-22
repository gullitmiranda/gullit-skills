---
name: context-capsule
description: Create a portable context capsule for subagents, forks, Zed threads, terminal agents, ACP/Pi-style agents, handoff, or later resume. Use before transferring work across tools or when managing parallel workstreams.
---

# Context Capsule

Create the smallest useful context package that lets another agent continue
without reading the whole conversation.

## Hard Rules

- Do not include secrets or private credentials.
- Do not include work-only information in personal or public repositories unless it is explicitly safe.
- Mark validation as stale unless it was run in the current session or is immutable CI evidence.
- Do not hide blockers; make them explicit.
- When the capsule is a prompt for another thread, return its complete content
  in one fenced `markdown` block. Keep recommendations and other reader-facing
  guidance outside that block.

## Process

1. Identify the target audience (parent chat, child subagent, forked conversation, Zed thread, terminal/ACP/Pi-style agent, future resume).
2. Include only context needed for the next action; preserve durable decisions and constraints without over-preserving stale implementation details.
3. Use [template.md](template.md). Prefer links, paths, branch names, issue numbers, and validation commands over raw transcript excerpts.
4. End with one recommended next action. For child agents, state the expected return format.
