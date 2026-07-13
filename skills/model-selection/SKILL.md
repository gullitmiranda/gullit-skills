---
name: model-selection
description: Select and validate AI agent model configurations across runtimes. Use when comparing models, effort levels, cost, latency, benchmarks, or profile defaults in Cursor, Zed, Claude Code, ACP, or another agent runtime.
---

# Model Selection

Choose an agent configuration by evaluating the complete setup in its target
runtime. Do not select from a provider leaderboard or nominal token price alone.

Read [references/selection-policy.md](references/selection-policy.md) before
making a recommendation or changing a model default. The durable human-facing
policy is in [docs/model-selection.md](../../docs/model-selection.md).

## Core Rule

Treat this as the selection unit:

```text
provider + model + effort + thinking mode + runtime
```

A model family name is not enough evidence. Different effort settings, tool
schemas, sandboxes, context behavior, and provider integrations can produce
materially different results.

## Workflow

### 1. Establish the decision boundary

Identify:

- target runtime and profiles;
- workload and expected tools;
- quality, latency, and cost constraints;
- provider, privacy, repository, and data-boundary restrictions;
- current default, fallback, and the change being considered.

Ask for clarification if the workload or success criteria are unknown. Do not
assume that a configuration successful in one runtime transfers to another.

### 2. Gather comparable evidence

Use this evidence order:

1. representative local results in the target runtime;
2. comparable reproducible evaluations;
3. runtime-specific public benchmarks;
4. general benchmarks;
5. provider documentation and pricing.

Use public benchmarks to narrow candidates, not to declare a winner. Record the
benchmark's runtime, task type, configuration, version, and date before relying
on it.

### 3. Define a small pilot

Create a task set representative of the intended workload. Hold repository
state, permissions, prompt shape, and validation constant where practical.

For every candidate, capture:

- complete configuration;
- task outcome and validation result;
- elapsed time, retries, and tool failures;
- observed cost or available cost proxy;
- user or operator intervention required.

Change one meaningful variable at a time. If that is impossible, state the
confounder explicitly.

### 4. Evaluate and recommend

Reject a candidate that has an unmitigated safety, data-boundary, correctness,
or tool-reliability failure. Compare the rest using quality, reliability, cost,
latency, operator effort, and runtime fit.

Recommend the smallest configuration that reliably meets the required quality
bar. Retain a known-good fallback while a new configuration is still provisional.

### 5. Apply only an evidence-backed change

Never silently change a runtime or profile default. Before editing settings:

1. state the configuration being replaced and the proposed replacement;
2. summarize the evidence and remaining uncertainty;
3. identify the fallback and review trigger;
4. obtain the user's approval when the change was not explicitly requested.

Do not create profile-specific exceptions until evidence shows a workload needs
one. Otherwise, let profiles inherit the current global fallback.

## Required Output

Return a compact decision record:

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

When the evidence is insufficient, recommend a pilot and provide its task set
and success criteria instead of guessing a default.

## Boundaries

- Do not treat usage telemetry as a quality benchmark.
- Do not transfer a benchmark ranking across runtimes without validation.
- Do not use private repository content in an external evaluation without
  explicit authorization and an appropriate data-boundary review.
- Do not optimize nominal token price at the expense of validated completion,
  safety, or operator time.
