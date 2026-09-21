---
name: agent-selection
description: Recommend the agent cast for a workflow phase—surfaces, models, write sets, and review handoffs. Use before substantial implementation, multi-block plans, parallel workstreams, subagent use, Cursor/Zed selection, or terminal/ACP/Pi-style delegation.
---

# Agent Selection

Choose the lightest execution cast that fits the work. Keep work in the main
agent by default; add roles only when delegation has a concrete benefit.

## Hard Rules

- **Delegation gate:** keep the task in the main agent unless a delegated unit:
  - is independently executable without sharing evolving decisions or context;
  - is large enough that parallelism or clean-context review repays handoff cost;
  - has a bounded, mergeable output and, for writers, a disjoint semantic write set.
  Multiple steps or files do not establish independence. Do not delegate product
  decisions, final synthesis, tightly coupled documentation, or work the main
  agent can complete directly with a few tool calls. This gate still applies when
  another skill recommends or assumes background delegation.
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
- For independently executable multi-block plans, parallel streams, or
  block/increment review, present an **orchestration cast** using
  [references/orchestration-cast.md](references/orchestration-cast.md) in
  **chat bullets** (default). Each critical-path role gets surface, a
  **concrete primary model** (not vague `inherit`), effort when exposed, write
  set, capsule type, honest order (`after` vs `parallel`), and fallback. A
  coupled multi-step task may use a one-role cast without special pleading.
- Recommend only models the surface exposes; if preferred is missing, mark
  `unavailable` and either the next exposed option or a surface change (do
  not invent slugs). Do not leave Model as only `inherit` or
  “≠ writer if available”.
- Operational cast defaults live here. On Cursor, fill each role from the
  operating card in
  [docs/model-selection.md](../../../../docs/model-selection.md). Durable
  profile or default-model changes use `model-selection` with evidence — do
  not silently change profile defaults from an orchestration sketch.

## Defaults

| Situation | Recommended shape |
| --- | --- |
| Product or architecture decision | Main chat only |
| Domain grilling | Main chat only |
| Independent multi-block ready plan | Orchestrator + disjoint writers + clean-context reviewers (cast required); prefer Cursor when fine per-role models are needed |
| Coupled multi-step work or final synthesis | Main agent; a one-role cast is sufficient |
| Bounded exploration | Main agent unless enough independent reading exists to amortize the handoff |
| Parallel side question | Subagent only when it passes the delegation gate |
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
2. Apply the delegation gate to each proposed role; collapse coupled work into
   the main agent.
3. Pick the orchestration surface from
   [references/orchestration-surfaces.md](references/orchestration-surfaces.md).
4. If delegation remains, check subagent availability; if absent, stop at
   alternatives and wait.
5. Build and emit the smallest honest cast. Put any handoff `context-capsule`
   in its own fenced `markdown` block afterward.

## Output

State autonomy mode, why the cast fits, context to transfer, and expected
return in normal Markdown (not a fence). For every delegated role, state its
independence and expected benefit. A cast is mandatory for independent
multi-block, parallel, or review work; it may contain one role for coupled work.
