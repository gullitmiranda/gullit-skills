# Model Selection

## Purpose

This document defines the durable policy for choosing models across Cursor, Zed,
Claude Code, ACP runtimes, and future agent providers. It describes how to make
a selection, not a static leaderboard or a provider-specific configuration.

**Status:** provisional. Populate a runtime-specific matrix only after a
representative local pilot.

## Core Rule

Evaluate a complete configuration, not a model family or nominal token price in
isolation:

```text
provider + model + effort + thinking mode + runtime
```

For example, `gpt-5.6-sol/medium` and `gpt-5.6-terra/xhigh` are distinct
candidates. A less capable model at a higher effort can be both cheaper and more
effective than a larger model at a lower effort for a particular task.

## Selection Principles

1. Start with task requirements and non-negotiable constraints, not a provider
   preference.
2. Compare candidates under the runtime where they will actually be used.
3. Use benchmark results to form hypotheses; validate consequential choices with
   representative local tasks.
4. Measure quality, cost, latency, reliability, and tool-use behavior together.
5. Change one meaningful variable at a time when evaluating a configuration.
6. Do not promote a single successful task, a marketing claim, or a benchmark
   rank to a default.
7. Keep a known-good fallback while testing a new default.

## Evidence Hierarchy

Use the strongest available evidence, in this order:

1. Repeated results on representative local tasks in the target runtime.
2. Reproducible evaluations that match the target runtime, tools, and effort.
3. Runtime-specific public benchmarks, such as
   [CursorBench](https://cursorbench.github.io/).
4. General public benchmarks that expose a comparable task and configuration.
5. Provider documentation, pricing, and qualitative claims.

A benchmark result does not transfer automatically between runtimes. Prompt
construction, tool definitions, sandboxing, context handling, provider routing,
and effort controls can materially change outcomes.

Operational telemetry is useful for capacity and adoption decisions, but is not
a model-quality ranking. For example,
[Zed Agent Metrics](https://zed.dev/agent-metrics) must not be used as the sole
basis for choosing a model.

## Decision Procedure

### 1. Classify the workload

Record the workload's risk and constraints before comparing models:

- task type: question, planning, implementation, review, debugging, or research;
- autonomy: interactive, supervised, or long-running;
- quality bar: acceptable error rate and required validation;
- tool requirements: terminal, browser, subagents, MCP, or sandbox;
- latency budget and cost budget;
- privacy, provider, repository, or data-boundary restrictions.

### 2. Create comparable candidates

For each candidate, record the complete configuration and the environment:

```text
runtime:
provider:
model:
effort:
thinking mode:
runtime version and relevant settings:
pricing source and date:
```

Do not compare candidates when an unknown setting changes the effective
configuration. If two factors must change together, record that limitation.

### 3. Run a representative pilot

Use a small task set that covers the work the configuration is expected to do.
For each task, preserve the task prompt, repository state, permissions, outcome,
validation result, elapsed time, retries, and observed cost.

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
| Runtime fit | Context use, tool behavior, sandbox compatibility, and provider stability. |

### 5. Decide and record

Choose the smallest configuration that reliably meets the workload's quality
bar. Record the evidence, uncertainty, fallback, and review date in the
runtime's decision record or pilot notes.

Do not set profile-specific defaults while the evidence is incomplete. Profiles
should inherit the available global fallback until a workload needs a documented
exception.

## Provisional Matrix

Maintain a matrix only as measured evidence becomes available. Empty cells mean
"not evaluated", not "inferior".

| Runtime | Workload | Configuration | Quality | Cost | Latency | Reliability | Evidence | Decision |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Zed | Planning | Not evaluated | - | - | - | - | - | Inherit global fallback |
| Zed | Safe implementation | Not evaluated | - | - | - | - | - | Inherit global fallback |
| Zed | Trusted delivery | Not evaluated | - | - | - | - | - | Inherit global fallback |

Use the scorecard and pilot template in
[`skills/model-selection/references/selection-policy.md`](../skills/model-selection/references/selection-policy.md)
when adding evidence.

## Review Triggers

Re-evaluate a selection when any of the following changes:

- the runtime, provider integration, tool schema, context handling, or sandbox;
- the model, effort setting, thinking mode, price, quota, or availability;
- the workload mix, validation requirements, or data-boundary constraints;
- repeated local failures, unexpected cost, or latency regressions;
- credible new evidence that is comparable to the target configuration.

Do not change a default merely because a new model is announced. Run the
smallest pilot that can confirm or reject the proposed change.

## Related Skill

Use `model-selection` when selecting or revisiting an agent model configuration.
The skill operationalizes this policy and loads its detailed scorecard on demand.
