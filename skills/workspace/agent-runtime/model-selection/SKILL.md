---
name: model-selection
description: Select and validate AI agent model configurations on a fixed orchestration surface. Use when choosing which model to run a task on, comparing models, effort levels, cost, latency, benchmarks, or profile defaults in Cursor, Zed, Claude Code, or another named agent surface.
---

# Model Selection

Choose a model configuration for a surface that is already fixed. Do not select
from a provider leaderboard or nominal token price alone. Surface choice
belongs to `agent-selection`.

Read [references/selection-policy.md](references/selection-policy.md) before
making a recommendation or changing a model default. The durable human-facing
policy, including the **Cursor operating card**, is in
[docs/model-selection.md](../../../../docs/model-selection.md).

## Daily pick vs default change

Two different questions share this skill. Do not mix their outputs.

- **Daily pick** ("which model for this task / today"): confirm the surface.
  On Cursor, answer from the operating card in `docs/model-selection.md` in a
  short lookup: task class, waiting vs background, pick, fallback if the
  preferred cell is not exposed. Do not emit the Decision template. Do not
  reopen the Pareto argument unless the user asks why.
- **Default change, comparison, or pilot**: follow the workflow below and emit
  the Decision template. The operating card is the current hypothesis, not
  evidence that a profile default should change.

Per-role picks inside an execution cast still belong to `agent-selection`. Point
that skill at the same operating card; do not invent a second lookup.

## Hard Rules

- Never silently change a profile or surface default.
- Do not treat usage telemetry as a quality benchmark.
- Do not transfer a benchmark ranking across surfaces without validation.
- Do not use private repository content in an external evaluation without
  explicit authorization and a data-boundary review.
- Do not optimize nominal token price at the expense of validated completion,
  safety, or operator time.
- Apply hard filters before the quality ladder: privacy, data boundary, plan
  availability, supported parameters, and provider eligibility on the chosen
  surface (for example an employer `llm-gateway` is ineligible on Cursor in the current
  setup).
- Per-role model picks inside an execution cast belong to `agent-selection`.
  Use this skill when changing durable defaults, comparing candidates with
  evidence, or running a pilot—not to replace the orchestration cast.
- If the orchestration surface is unset or contested, stop and use
  `agent-selection` first.

## Core Rule

The selection unit is:

```text
provider + model snapshot + effort + thinking/mode
(+ route/tier when the surface exposes them)
```

The orchestration surface is a **precondition and confounder**, not part of the
product being selected. Hold it constant for a pilot. A model family name alone
is not enough evidence.

## Workflow

1. Confirm surface and decision boundary: named surface (or defer to
   `agent-selection`); workload; quality/latency/cost constraints; hard
   filters; current default, fallback, and proposed change. Reject ineligible
   provider/surface pairs before gathering quality evidence.
2. Gather comparable evidence, in order: (1) representative local results on
   that surface; (2) comparable reproducible evaluations; (3) surface-specific
   public benchmarks; (4) general benchmarks; (5) provider documentation and
   qualitative claims. Use public benchmarks to narrow candidates, not to
   declare a winner; record suite version, date, harness, and configuration.
3. Define a small pilot on the fixed surface. Capture configuration, outcome,
   validation, elapsed time, retries/tool failures, observed cost, and operator
   intervention. Change one meaningful variable at a time; state confounders.
4. Evaluate and recommend: reject unmitigated safety, data-boundary,
   correctness, or tool-reliability failures. Among the rest, prefer the lowest
   effective cost per validated completion (or lowest operator time if cost is
   flat), then lower effort/tier. Keep a known-good fallback while provisional.
5. Apply only an evidence-backed change with user approval when not explicitly
   requested. Do not create profile-specific exceptions until evidence shows a
   workload needs one.

## Required Output

```markdown
## Model Selection Decision

- Surface and workload:
- Candidate configurations:
- Evidence and its limits:
- Quality, cost, latency, and reliability comparison:
- Recommendation:
- Fallback:
- Confidence and review trigger:
- Next pilot, if evidence is incomplete:
```

Write the decision in the language of the conversation; the template is
illustrative. If saved or published, follow the artifact-language policy in
`user-preferences`.

When evidence is insufficient, recommend a pilot with task set and success
criteria instead of guessing a default.
