# Model Selection

## Purpose

This document has two jobs: a **Cursor operating card** you can use today, and
the durable policy for choosing model configurations on a fixed orchestration
surface. Surface choice belongs to `agent-selection`. The card is a dated
lookup, not a profile default. Rebuild it with `Leaderboard to Map` when the
suite, catalog, or constraint changes.

**Status:** provisional. Populate a surface-specific measured matrix only after
a representative local pilot.

## Cursor operating card

Provisional lookup for daily use on **Cursor only**. Cost is a tiebreaker
(org-covered, no quota). Source:
[cursorbench-4.0.research.md](../.agents/notes/current/cursorbench-4.0.research.md)
(CursorBench 4.0, refreshed 2026-09-21 afternoon for Grok 4.7). Not a Zed,
Claude Code, or terminal default.

### Pick

| Task | You are waiting | Background / subagent |
| --- | --- | --- |
| Ambiguous, multi-file, or costly to get wrong | Grok 4.7 Extra High | Grok 4.7 Extra High |
| Normal implementation or review | Grok 4.7 High | Muse Spark 1.3 Max |
| Bounded edit, recon, or draft | Grok 4.6 Medium or Low | Luna Extra High |
| Rename, lint, lookup, throwaway | Terra Medium | Terra Low |

If Grok 4.7 Extra High is not exposed, use Opus 5 High. If Grok 4.6 is gone
from the catalog, use Grok 4.7 Low for the interactive Light row. Subagent
effort is bound into the slug: if a cell is not exposed, take the next row
**in the same column** - do not switch columns to recover a missing effort.

### Cast

One measurement, two columns. Map the role to the table, then name the
configuration the surface actually exposes.

| Role | Configuration |
| --- | --- |
| Orchestrator | Parent session. Do not downgrade. |
| Implementer | Interactive column for the task class. |
| Review Spec | Different family from the writer: Opus 5 High if the writer is Grok or Muse; Grok 4.7 Extra High if the writer is Opus. |
| Review Standards | Remaining different family, or Muse Spark 1.3 Max. |
| Validation / glue | Background column. |
| Bounded exploration | Interactive Light row if waiting; Luna Extra High if delegated. |

### Do not pick

- Sol at any effort
- Sonnet 5
- Opus Extra High or Opus Max
- Opus 5 High as the default ceiling (keep as fallback if Grok 4.7 Extra High is missing)
- Luna Max while waiting (slow for the quality)
- Grok 4.6 Extra High when 4.7 High is available

If the org enables Fable 5.1, **Fable High replaces Grok 4.7 Extra High** in
both columns. GLM 5.2 and Kimi K3 have no CursorBench 4.0 row; do not place
them from this card.

## Core Rule

Evaluate a complete model configuration, not a model family or nominal token
price in isolation:

```text
provider + model snapshot + effort + thinking/mode
(+ route/tier when the surface exposes them)
```

The orchestration surface is a **precondition and confounder**, not part of the
selection unit. Hold it constant for a pilot.

For example, `gpt-5.6-sol/medium` and `gpt-5.6-terra/xhigh` are distinct
candidates. A less capable model at a higher effort can be both cheaper and more
effective than a larger model at a lower effort for a particular task.

## Selection Principles

1. Confirm the surface (or defer to `agent-selection`), then start with task
   requirements and non-negotiable hard filters—not a provider preference.
2. Compare candidates only under the surface where they will actually be used.
3. Use benchmark results to form hypotheses; validate consequential choices with
   representative local tasks on that surface.
4. Measure quality, cost, latency, reliability, and tool-use behavior together.
5. Change one meaningful variable at a time when evaluating a configuration.
6. Do not promote a single successful task, a marketing claim, or a benchmark
   rank to a default.
7. Keep a known-good fallback while testing a new default.
8. Do not transfer a Cursor catalog default to Zed/gateway (or the reverse)
   without a pilot on the target surface.

## Hard filters before quality evidence

Reject or park candidates that fail any of:

- privacy, repository, or data-boundary restrictions;
- plan / quota / availability on the surface;
- unsupported parameters or missing tool support;
- provider ineligibility on the surface (for example an employer `llm-gateway`
  is ineligible for Cursor agent inference in the current setup—revisit if
  BYOK/OpenAI-compatible routing appears).

Pricing is both a budget filter and a scored dimension (effective cost per
validated completion).

## Evidence Hierarchy

After hard filters, use the strongest available quality evidence, in this order:

1. Repeated results on representative local tasks on the target surface.
2. Reproducible evaluations that match the target surface, tools, and effort.
3. Surface-specific public benchmarks, such as
   [CursorBench](https://cursor.com/cursorbench).
4. General public benchmarks that expose a comparable task and configuration.
5. Provider documentation and qualitative claims.

A benchmark result does not transfer automatically between surfaces. Prompt
construction, tool definitions, sandboxing, context handling, provider routing,
and effort controls can materially change outcomes. Suite versions are not
comparable (for example CursorBench 3.2 vs 4.0).

Operational telemetry is useful for capacity and adoption decisions, but is not
a model-quality ranking. For example,
[Zed Agent Metrics](https://zed.dev/agent-metrics) and OpenRouter token-volume
rankings must not be used as the sole basis for choosing a model.

## Decision Procedure

### 1. Classify the workload and surface

Record before comparing models:

- orchestration surface (named; never bare `ACP`);
- task type: question, planning, implementation, review, debugging, or research;
- autonomy: interactive, supervised, or long-running;
- quality bar: acceptable error rate and required validation;
- tool requirements: terminal, browser, subagents, MCP, or sandbox;
- latency budget and cost budget;
- privacy, provider, repository, or data-boundary restrictions.

### 2. Create comparable candidates

For each candidate, record the complete configuration and the environment:

```text
surface:
provider / endpoint / routing:
model snapshot:
effort:
thinking / mode:
tier / Fast / other surface toggles:
surface version and relevant settings:
pricing source and date:
```

Do not compare candidates when an unknown setting changes the effective
configuration. If two factors must change together, record that limitation.

### 3. Run a representative pilot

Use a small task set that covers the work the configuration is expected to do.
For each task, preserve the task prompt, repository state, permissions, outcome,
validation result, elapsed time, retries, and observed cost. Hold the surface
constant.

Include at least one task that exercises the expected tools and one task that
requires the expected quality bar. A task that cannot be validated should not
be the sole evidence for a default.

### 4. Compare results

Reject candidates with a safety, data-boundary, correctness, or tool-reliability
failure that cannot be mitigated. For the remaining candidates, compare:

| Dimension | What to observe |
| --- | --- |
| Outcome quality | Correctness, completeness, reviewability, and validation result. |
| Reliability | Retries, stalls, invalid tool calls, and instruction adherence. |
| Cost | Effective cost per completed, validated task. |
| Latency | Time to useful first action and time to validated completion. |
| Operator effort | Intervention, clarification, and repair work required. |
| Surface fit | Context use, tool behavior, sandbox compatibility, and provider stability. |

### 5. Decide and record

Among eligible candidates, choose the lowest effective cost per validated
completion (or lowest operator time if cost is flat), then lower effort/tier.
Record the evidence, uncertainty, fallback, and review date.

Do not set profile-specific defaults while the evidence is incomplete. Profiles
should inherit the available global fallback until a workload needs a documented
exception.

## Leaderboard to Map

A published leaderboard is a list of configurations, not a decision. Converting
one into an escalation map requires the parameters below to be **recorded
explicitly**, because each is a choice that changes the outcome. Reuse these
parameters when refreshing a map so that successive versions stay comparable.

### 1. Availability masks, applied before any quality comparison

Mask the catalog down to what is actually selectable, and record each exclusion
with its reason and date:

- enabled at the org or tenant level;
- enabled in local settings (an operator may have disabled a model deliberately;
  record whether the data supports that choice);
- effort selectable on the target execution mode. Effort is not always a free
  control - a surface may bind effort into a fixed model identifier, which
  removes map rows that the chat picker would allow.

A configuration excluded by a mask is not "inferior"; it is unavailable. Keep it
listed with its mask so the map can be re-derived when the mask lifts.

### 2. Quality clusters, not ranks

Group configurations whose scores fall within the suite's declared variance
(absent a published confidence interval, a stated "small differences may not be
meaningful" caveat justifies a fixed threshold - CursorBench 4.0 used 2 points).
Treat each cluster as one quality tier and select **within** it, never across
ranks inside it.

This step is what prevents paying for rank noise. It routinely reveals that a
lower effort of the same model dominates a higher one, and that configurations
several ranks apart are equivalent.

### 3. Criterion order, derived from who actually pays

State the objective function before comparing anything, and derive it from the
operator's real constraint rather than assuming cost is primary:

```text
filter:    quality sufficient for the task class
objective: <the operator's binding constraint>
tiebreak:  <the non-binding but still valued dimension>
```

Cost is a **constraint** when the operator pays, faces a quota, or hits usage
limits. It is a **tiebreaker** when spend is absorbed by an org, no limit is
reached, and the operator still declines to waste money. It is **irrelevant**
only if explicitly disclaimed. Establish which case applies - do not default to
cost-first, because a cost-first reading of a leaderboard systematically hides
configurations that are time-efficient and mid-priced.

### 4. Weighting contexts, not separate evaluations

Where the same model serves materially different execution contexts (operator
waiting vs. background or delegated work), run **one** measurement pass and
apply two weightings. Turn count and latency dominate when the operator waits;
the cost tiebreaker runs free when nobody is waiting. Two evaluations would
double the effort to measure the same quality.

Within a cluster, treat step counts within 5% of the faster configuration (or
5 steps, whichever is larger) as tied on operator time, then apply the cost
tiebreak. A 2-step gap must not revive a configuration that costs a third more.

### 5. Proxies, each declared with its limit

Record every proxy and what it cannot support:

| Proxy | Supports | Does not support |
| --- | --- | --- |
| Steps or tool turns per task | Fewer round trips | A latency or elapsed-time claim |
| Published cost per task | Relative ordering of spend | The operator's actual bill |
| Aggregate benchmark score | Overall capability hypothesis | Per-stage or per-category specialization |

### 6. Declared exclusions

Close the map by naming what it does not account for. For an agent workspace
this typically includes skill and rule adherence, MCP or tool-call reliability,
long-context retention, and output-language quality - none of which public
coding benchmarks score. A map that omits this list will be read as more
authoritative than its evidence allows.

## Provisional Matrix

Maintain a matrix only as measured evidence becomes available. A benchmark can
support an explicitly provisional assignment on its own surface, but it cannot
populate the measured `Quality`, `Cost`, `Latency`, or `Reliability` cells for a
different surface. Empty cells mean "not evaluated", not "inferior".

### CursorBench shortlist

The current Cursor shortlist and escalation map is
[`.agents/notes/current/cursorbench-4.0.research.md`](../.agents/notes/current/cursorbench-4.0.research.md)
(CursorBench 4.0, accessed 2026-09-21, refreshed the same afternoon for Grok 4.7). The earlier
[`cursorbench-3.2.research.md`](../.agents/notes/retired/cursorbench-3.2.research.md)
remains valid only as a record of that suite.

The research notes are evidence, not the daily lookup. The **Cursor operating
card** at the top of this document is the lookup; it is still not a profile
default. Suite versions are not comparable: do not chart 3.2 and 4.0 scores
together or carry a ranking across them. Refresh the card from a new dated
research note by applying `Leaderboard to Map`, then a local pilot on Cursor.

Use [CursorBench](https://cursor.com/cursorbench) as a surface-specific
hypothesis source for Cursor only.

### Generic OpenRouter Policy for Zed

This policy is a portable starting point for the **Zed Agent** and terminal
agents that can use OpenRouter (or an employer gateway where configured). It is not a
Cursor catalog. OpenRouter does not publish stage-level scores or per-task
costs, so these are cost-aware hypotheses rather than measured Zed defaults.
Record model snapshot, effort, provider/routing, tool schema, and actual
returned provider for every pilot.

| Workflow stage | Use first | Escalate when | OpenRouter evidence and cost signal | Portable operating rule |
| --- | --- | --- | --- | --- |
| Routine questions, reconnaissance, and lightweight planning | `x-ai/grok-4.6-20260810`, effort `low` | The task is ambiguous, spans many files, or needs a longer tool loop: `openai/gpt-5.6-sol-20260709`, effort `medium` | Grok: intelligence 60.9, coding 76.8, agentic 58.7; $2/M input and $6/M output. | Allow provider fallback for reversible work, but record the model and provider actually returned. |
| Standard implementation | `openai/gpt-5.6-sol-20260709`, effort `medium` | Broad or ambiguous change: `anthropic/claude-opus-5-20260723`, effort `high`; fullstack-focused alternative: `moonshotai/kimi-k3-20260715`, effort `high` | GPT: coding 77.4, intelligence 60.9, agentic 57.8; $2/M input and $10/M output. Kimi has Design Arena `agents/fullstack` rank 2 and `models/codecategories` rank 1 at $3/M and $15/M. | Use GPT as the balanced baseline; choose Kimi for a fullstack-shaped task only when its specialization is worth the premium. |
| Debugging and code review | `openai/gpt-5.6-sol-20260709`, effort `medium` | The cost of a missed defect is high: `anthropic/claude-opus-5-20260723`, effort `high`; use `openai/gpt-5.6-sol-20260709`, effort `max` as an independent second pass | GPT provides the lower-cost coding baseline. Claude has the highest observed intelligence and coding indices in this set, 63.1 and 78.0, but costs $5/M input and $25/M output. | Measure root-cause accuracy, regression detection, and false positives; do not infer debugging quality from aggregate indices. |
| Trusted delivery and high-risk changes | `anthropic/claude-opus-5-20260723`, effort `max`, with an approved exact provider endpoint | Human review and project validation; if the approved endpoint is unavailable, stop rather than silently falling back | Claude is the strongest aggregate frontier candidate in this set, but OpenRouter publishes no delivery-safety or repository-validation score. | Set `allow_fallbacks=false` and require an approved endpoint; keep human approval, tests, and data-boundary checks mandatory. |
| Cheap fallback for reversible work | `qwen/qwen3.8-max-20260803`, effort `low`; Grok at `low` is an alternative | The task loops, produces an uncertain result, or fails validation: return to GPT or Claude rather than adding unreviewed writes | Qwen: agentic 58.4, `agents/fullstack` rank 4, `agents/webapps` rank 1; $2/M input and $6/M output. | Apply a token/budget ceiling. Never use this tier for trusted delivery or irreversible actions. |

The policy intentionally does not choose a single universal winner. Recheck when
provider routing, snapshots, prices, or effort behavior change. See OpenRouter's
[provider routing](https://openrouter.ai/docs/guides/routing/provider-selection.md),
[model fallback](https://openrouter.ai/docs/guides/routing/model-fallbacks), and
[tool calling](https://openrouter.ai/docs/guides/features/tool-calling.md)
documentation.

For Zed and terminal portability, hold constant: snapshot, effort,
provider/fallback policy, tool schema, permissions, repository revision, and
validation. OpenRouter's catalog cannot substitute for surface evidence.

### Measured Surface Matrix

| Surface | Workload | Configuration | Quality | Cost | Latency | Reliability | Evidence | Decision |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Zed Agent | Edit prediction (next-edit) | `ollama` + `sweep-next-edit` | Provisional | ~$0 | 5-10 s cold, <500 ms warm | TBD | Pilot notes TBD | Needs pilot validation before promotion |
| Zed Agent | Planning | Not evaluated | - | - | - | - | OpenRouter shortlist only; no Zed pilot | Inherit global fallback |
| Zed Agent | Safe implementation | Not evaluated | - | - | - | - | OpenRouter shortlist only; no Zed pilot | Inherit global fallback |
| Zed Agent | Debugging and code review | Not evaluated | - | - | - | - | OpenRouter shortlist only; no Zed pilot | Inherit global fallback |
| Zed Agent | Trusted delivery | Not evaluated | - | - | - | - | OpenRouter shortlist only; no Zed pilot | Inherit global fallback |

Use the scorecard and pilot template in
[`skills/workspace/agent-runtime/model-selection/references/selection-policy.md`](../skills/workspace/agent-runtime/model-selection/references/selection-policy.md)
when adding evidence.

## Review Triggers

Re-evaluate a selection when any of the following changes:

- the surface, provider integration, tool schema, context handling, or sandbox;
- the model snapshot, effort, thinking/mode, route/tier, price, quota, or availability;
- the workload mix, validation requirements, or data-boundary constraints;
- repeated local failures, unexpected cost, or latency regressions;
- credible new evidence that is comparable to the target configuration;
- provider eligibility on a surface (for example Cursor BYOK / gateway support).

Do not change a default merely because a new model is announced. Run the
smallest pilot that can confirm or reject the proposed change.

## Related Skills

- `model-selection` — operationalizes this policy and loads the scorecard.
- `agent-selection` — chooses the orchestration surface and cast; see
  `references/orchestration-surfaces.md`.
- employer-gateway skill — work LLM gateway wiring on Zed Agent.
