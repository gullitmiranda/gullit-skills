---
name: agent-selection
description: Recommend the agent cast for a workflow phase—surfaces, models, write sets, and review handoffs. Use before substantial implementation, multi-block plans, parallel workstreams, subagent use, Cursor/Zed selection, or terminal/ACP/Pi-style delegation.
---

# Agent Selection

Choose the execution cast (orchestration surface + model per role) before
substantial work. Do not recommend a surface and leave model or review shape
implicit.

## Hard Rules

- Choose the **orchestration surface** before models. ACP is not a surface —
  write `ACP:<named-agent>`. See
  [references/orchestration-surfaces.md](references/orchestration-surfaces.md).
- **Subagent availability gate:** before recommending or using a subagent,
  check whether the current surface actually exposes a subagent tool (e.g.
  `spawn_agent`, Task tool, background agent). If it does not:
  - Say clearly that subagents are not supported in this surface/profile.
  - Recommend a manual alternative: new agent thread, `ACP:<agent>`, terminal
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
  **chat bullets** (default). Each critical-path role gets surface, a
  **concrete primary model** (not vague `inherit`), effort when exposed, write
  set, capsule type, honest order (`after` vs `parallel`), and fallback. Solo
  sequential work needs an explicit exception reason from that reference.
- Recommend only models the surface exposes; if preferred is missing, mark
  `unavailable` and either the next exposed option or a surface change (do
  not invent slugs). Do not leave Model as only `inherit` or
  “≠ writer if available”.
- Operational cast defaults live here. Durable profile or default-model
  changes use `model-selection` with evidence — do not silently change
  profile defaults from an orchestration sketch.

## Defaults

| Situation | Recommended shape |
| --- | --- |
| Product or architecture decision | Main chat only |
| Domain grilling | Main chat only |
| Multi-block ready plan | Orchestrator + disjoint writers + clean-context reviewers (cast required); prefer Cursor when fine per-role models are needed |
| Bounded exploration | Subagent |
| Parallel side question | Subagent |
| Side path becomes primary | Fork or new thread; new cast |
| Focused single-block implementation | Current surface; cast may be one implementer row. Fine cast → Cursor; employer gateway/OpenRouter non-negotiable → Zed Agent |
| Block or increment review | Parallel Standards ∥ Spec subagents; review capsules; not the writer transcript |
| Long implementation writer | `Terminal:<cli>` or `ACP:<agent>` as writer when needed; keep orchestration on a surface that can cast, or use manual threads + capsules |
| Harness-driven debugging | Terminal agent or IDE agent |
| CI watch/fix loop | Background watcher or terminal agent |
| Slack / Grok / work×xAI paths | Cursor local or cloud |
| Tool switch or resume | Context capsule |
| Exact history required | Full transcript transfer |

## Procedure

1. Classify the phase (decide / explore / implement / review / handoff).
2. Pick the orchestration surface from
   [references/orchestration-surfaces.md](references/orchestration-surfaces.md).
3. Check subagent availability; if absent, stop at alternatives and wait.
4. Build the cast from [references/orchestration-cast.md](references/orchestration-cast.md)
   when the defaults table requires it; otherwise name the single surface+model.
5. Emit reader-facing recommendation (prose + cast). Put any handoff
   `context-capsule` in its own fenced `markdown` block afterward.

## Output

State autonomy mode, why the cast fits, context to transfer, and expected
return in normal Markdown (not a fence). The cast (bullets by default) is
mandatory whenever the multi-block / parallel / review defaults apply.
