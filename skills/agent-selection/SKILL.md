---
name: agent-selection
description: Recommend the right agent or runtime for a workflow phase. Use before substantial implementation, long-running work, parallel workstreams, context handoff, subagent use, Cursor/Zed selection, or terminal/ACP/Pi-style agent delegation.
---

# Agent Selection

Choose where the next step should run before doing substantial work.

## Decision Inputs

Consider:

- Task length.
- Need for user judgment.
- Need for IDE feedback.
- Need for branch/worktree isolation.
- Amount of noisy exploration expected.
- Whether validation is command-driven.
- Whether context should stay out of the parent chat.
- Whether exact transcript history matters.

## Defaults

| Situation | Recommended runtime |
| --- | --- |
| Product or architecture decision | Main chat |
| Domain grilling | Main chat |
| Bounded exploration | Subagent |
| Parallel side question | Subagent |
| Side path becomes primary | Fork or new thread |
| Focused implementation | Cursor or Zed agent |
| Long implementation | Terminal, ACP, or Pi-style agent |
| Harness-driven debugging | Terminal agent or IDE agent |
| CI watch/fix loop | Background watcher or terminal agent |
| Tool switch or resume | Context capsule |
| Exact history required | Full transcript transfer |

## Runtime Profiles

### Main chat

Use for decisions, user interviews, prioritization, and final synthesis.

### Subagent

Use for bounded side quests that should return a distilled result.

### Fork or new thread

Use when a side path becomes the new primary path.

### Cursor or Zed agent

Use for focused implementation where IDE review and interaction matter.

### Terminal, ACP, or Pi-style agent

Use for long-running work, mechanical edits, command-driven loops, and isolated
execution.

### Full transcript transfer

Use only when exact history matters. Prefer `context-capsule` for normal handoff.

## Required Recommendation Format

```text
Recommended runtime:
Why:
Context to pass:
Expected return:
```

If the recommendation hands work to another tool or agent, invoke or produce a
`context-capsule` first.
