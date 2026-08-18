---
name: agent-selection
description: Recommend the right agent or runtime for a workflow phase. Use before substantial implementation, long-running work, parallel workstreams, context handoff, subagent use, Cursor/Zed selection, or terminal/ACP/Pi-style agent delegation.
---

# Agent Selection

Choose where the next step should run before doing substantial work.

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

## Hard Rules

- **Subagent availability gate:** before recommending or using a subagent,
  check whether the current runtime actually exposes a subagent tool (e.g.
  `spawn_agent`, Task tool, background agent). If it does not:
  - Say clearly that subagents are not supported in this runtime/profile.
  - Recommend a manual alternative: new agent thread, ACP agent, terminal
    agent, or a `context-capsule` the user pastes into another session.
  - Never run the requested work in the current thread proactively. Wait for
    the user to pick an alternative.
  Rationale: "run in background" executed in the parent thread blocks the
  conversation and duplicates work the user expected to happen elsewhere.
- If the recommendation hands work to another tool or agent, invoke or
  produce a `context-capsule` first.

## Required Recommendation Format

```text
Recommended runtime:
Why:
Context to pass:
Expected return:
```
