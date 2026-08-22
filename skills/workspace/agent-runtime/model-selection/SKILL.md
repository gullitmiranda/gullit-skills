---
name: model-selection
description: Select and validate AI agent model configurations across runtimes. Use when comparing models, effort levels, cost, latency, benchmarks, or profile defaults in Cursor, Zed, Claude Code, ACP, or another agent runtime.
---

# Model Selection

Choose an agent configuration by evaluating the complete setup in its target
runtime. Do not select from a provider leaderboard or nominal token price alone.

Read [references/selection-policy.md](references/selection-policy.md) before
making a recommendation or changing a model default. The durable human-facing
policy is in [docs/model-selection.md](../../../../docs/model-selection.md).

Zed edit-predictions setup notes are in
[`zed-sweep-next-edit-setup.md`](zed-sweep-next-edit-setup.md).

## Hard Rules

- Never silently change a runtime or profile default.
- Do not treat usage telemetry as a quality benchmark.
- Do not transfer a benchmark ranking across runtimes without validation.
- Do not use private repository content in an external evaluation without explicit authorization and a data-boundary review.
- Do not optimize nominal token price at the expense of validated completion, safety, or operator time.

## Core Rule

The selection unit is:

```text
provider + model + effort + thinking mode + runtime
```

A model family name is not enough evidence; effort settings, tool schemas,
sandboxes, context behavior, and provider integrations can produce materially
different results.

## Workflow

1. Establish the decision boundary: target runtime and profiles; workload and expected tools; quality, latency, and cost constraints; provider, privacy, repository, and data-boundary restrictions; current default, fallback, and the change being considered. Ask for clarification if the workload or success criteria are unknown. Do not assume a configuration that works in one runtime transfers to another.
2. Gather comparable evidence, in order: (1) representative local results in the target runtime; (2) comparable reproducible evaluations; (3) runtime-specific public benchmarks; (4) general benchmarks; (5) provider documentation and pricing. Use public benchmarks to narrow candidates, not to declare a winner; record the benchmark's runtime, task type, configuration, version, and date before relying on it.
3. Define a small pilot: a task set representative of the workload, holding repository state, permissions, prompt shape, and validation constant where practical. For each candidate capture complete configuration, task outcome and validation result, elapsed time, retries and tool failures, observed cost or cost proxy, and operator intervention required. Change one meaningful variable at a time; if impossible, state the confounder explicitly.
4. Evaluate and recommend: reject any candidate with an unmitigated safety, data-boundary, correctness, or tool-reliability failure. Compare the rest on quality, reliability, cost, latency, operator effort, and runtime fit. Recommend the smallest configuration that reliably meets the quality bar; retain a known-good fallback while a new configuration is provisional.
5. Apply only an evidence-backed change. Before editing settings: state the configuration being replaced and the proposed replacement; summarize the evidence and remaining uncertainty; identify the fallback and review trigger; obtain the user's approval when the change was not explicitly requested. Do not create profile-specific exceptions until evidence shows a workload needs one; otherwise let profiles inherit the global fallback.

## Required Output

```markdown
## Model Selection Decision

- Runtime and workload:
- Candidate configurations:
- Evidence and its limits:
- Quality, cost, latency, and reliability comparison:
- Recommendation:
- Fallback:
- Confidence and review trigger:
- Next pilot, if evidence is incomplete:
```

When the evidence is insufficient, recommend a pilot with its task set and
success criteria instead of guessing a default.
