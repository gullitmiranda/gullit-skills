---
name: agent-selection
description: Recommend the agent cast for a workflow phase—runtimes, models, write sets, and review handoffs. Use before substantial implementation, multi-block plans, parallel workstreams, subagent use, Cursor/Zed selection, or terminal/ACP/Pi-style delegation.
---

# Agent Selection

Choose the execution cast (runtime + model per role) before substantial work.
Do not recommend a single runtime and leave model or review shape implicit.

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
- For multi-block plans, parallel streams, or block/increment review, present
  an **orchestration cast** using
  [references/orchestration-cast.md](references/orchestration-cast.md) in
  **chat bullets** (default). Each critical-path role gets runtime, a
  **concrete primary model** (not vague `inherit`), effort when exposed, write
  set, capsule type, honest order (`after` vs `parallel`), and fallback. Solo
  sequential work needs an explicit exception reason from that reference.
- Recommend only models the runtime exposes; if preferred is missing, mark
  `unavailable` and give the next exposed option. Do not invent model slugs.
  Do not leave Model as only `inherit` or “≠ writer if available”.
- Operational cast defaults live here. Durable profile or default-model changes
  use `model-selection` with evidence — do not silently change profile defaults
  from an orchestration sketch.

## Defaults

| Situation | Recommended shape |
| --- | --- |
| Product or architecture decision | Main chat only |
| Domain grilling | Main chat only |
| Multi-block ready plan | Orchestrator + disjoint writers + clean-context reviewers (cast required) |
| Bounded exploration | Subagent |
| Parallel side question | Subagent |
| Side path becomes primary | Fork or new thread; new cast |
| Focused single-block implementation | Cursor or Zed agent; cast may be one implementer row |
| Block or increment review | Parallel Standards ∥ Spec subagents; review capsules; not the writer transcript |
| Long implementation | Terminal, ACP, or Pi-style agent as writer runtime |
| Harness-driven debugging | Terminal agent or IDE agent |
| CI watch/fix loop | Background watcher or terminal agent |
| Tool switch or resume | Context capsule |
| Exact history required | Full transcript transfer |

## Procedure

1. Classify the phase (decide / explore / implement / review / handoff).
2. Check subagent availability; if absent, stop at alternatives and wait.
3. Build the cast from [references/orchestration-cast.md](references/orchestration-cast.md)
   when the defaults table requires it; otherwise name the single runtime+model.
4. Emit reader-facing recommendation (prose + cast). Put any handoff
   `context-capsule` in its own fenced `markdown` block afterward.

## Output

State autonomy mode, why the cast fits, context to transfer, and expected
return in normal Markdown (not a fence). The cast (bullets by default) is
mandatory whenever the multi-block / parallel / review defaults apply.
