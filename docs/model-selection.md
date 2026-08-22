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

Maintain a matrix only as measured evidence becomes available. A benchmark can
support an explicitly provisional assignment in its own runtime, but it cannot
populate the measured `Quality`, `Cost`, `Latency`, or `Reliability` cells for a
different runtime. Empty cells mean "not evaluated", not "inferior".

### CursorBench 3.2 Cost-Effective Operating Policy

This policy is direct evidence only for the Cursor agent runtime. It uses the
[CursorBench 3.2 leaderboard](https://cursor.com/evals), accessed on
2026-08-22, whose aggregate task mix includes planning, codebase understanding,
bugfinding, code review, instruction following, and advanced tool use. The
benchmark does not publish a result for any individual workflow stage, latency,
or reliability. Therefore the assignments below are operational hypotheses to
pilot, not defaults or profile overrides; use them only as candidates in Zed,
ACP, Claude Code, or another runtime.

| Workflow stage | Use first | Escalate when | CursorBench score and average cost / task | Operating decision |
| --- | --- | --- | --- | --- |
| Routine questions, codebase triage, and planning | `GPT-5.6 Luna / High` | The plan has material ambiguity or drives a multi-file change: `GPT-5.6 Luna / Max` | Luna High: 56.8%, $0.16. Luna Max: 61.1%, $0.39. | Use the cheapest published configuration near 57%; skip `Extra High` as the normal tier. |
| Standard implementation | `GPT-5.6 Luna / Max` | Validation fails, the change is unusually complex, or a higher quality bar is justified: `Grok 4.6 / Medium` | Luna Max: 61.1%, $0.39. Grok Medium: 67.1%, $1.28. | Luna Max is the low-cost implementation baseline; Grok Medium is the first quality escalation. |
| Debugging and code review | `GPT-5.6 Luna / Max` | A wrong diagnosis or missed defect is expensive: `Grok 4.6 / Medium` | Luna Max: 61.1%, $0.39. Grok Medium: 67.1%, $1.28. | Start economically, then pay for the 6.0-point aggregate-score increase when the failure cost warrants it. |
| Trusted delivery and high-risk changes | `Grok 4.6 / Medium` | A final recovery attempt warrants the incremental spend: `Grok 4.6 / High` | Grok Medium: 67.1%, $1.28. Grok High: 69.9%, $2.34. | Keep human approval and repository validation mandatory; CursorBench does not measure delivery safety. |

`GPT-5.6 Luna / Extra High` is better value than `GPT-5.6 Terra / High`: 57.7%
at $0.23 per task versus 54.2% at $0.71. It has a 3.5-point higher score for
67.6% less published cost. However, it is not the normal Luna tier: Luna High
to Luna Max is the more efficient score-cost escalation path in the published
curve. `Extra High` has no proven workflow specialty or latency advantage.

Do not select `GPT-5.6 Terra` on CursorBench 3.2 score-cost grounds. Every
published Terra effort is dominated by another displayed configuration. This
is a benchmark-only conclusion: the leaderboard omits latency, retries,
stalls, tool-call validity, provider routing, actual billing, and safety.

### Generic OpenRouter Policy for Zed

This policy is intended as a portable starting point for the Zed harness and a
terminal agent. It combines OpenRouter's model-level intelligence, coding, and
agentic indices with Design Arena signals, catalog pricing, supported reasoning
efforts, and tool capability. OpenRouter does not publish stage-level scores or
per-task costs, so these are cost-aware hypotheses rather than measured Zed
defaults. The exact model snapshot, effort, provider or routing policy, tool
schema, and actual returned provider must be recorded for every pilot.

| Workflow stage | Use first | Escalate when | OpenRouter evidence and cost signal | Portable operating rule |
| --- | --- | --- | --- | --- |
| Routine questions, reconnaissance, and lightweight planning | `x-ai/grok-4.6-20260810`, effort `low` | The task is ambiguous, spans many files, or needs a longer tool loop: `openai/gpt-5.6-sol-20260709`, effort `medium` | Grok: intelligence 60.9, coding 76.8, agentic 58.7; $2/M input and $6/M output. | Allow provider fallback for reversible work, but record the model and provider actually returned. |
| Standard implementation | `openai/gpt-5.6-sol-20260709`, effort `medium` | Broad or ambiguous change: `anthropic/claude-opus-5-20260723`, effort `high`; fullstack-focused alternative: `moonshotai/kimi-k3-20260715`, effort `high` | GPT: coding 77.4, intelligence 60.9, agentic 57.8; $2/M input and $10/M output. Kimi has Design Arena `agents/fullstack` rank 2 and `models/codecategories` rank 1 at $3/M and $15/M. | Use GPT as the balanced baseline; choose Kimi for a fullstack-shaped task only when its specialization is worth the premium. |
| Debugging and code review | `openai/gpt-5.6-sol-20260709`, effort `medium` | The cost of a missed defect is high: `anthropic/claude-opus-5-20260723`, effort `high`; use `openai/gpt-5.6-sol-20260709`, effort `max` as an independent second pass | GPT provides the lower-cost coding baseline. Claude has the highest observed intelligence and coding indices in this set, 63.1 and 78.0, but costs $5/M input and $25/M output. | Measure root-cause accuracy, regression detection, and false positives; do not infer debugging quality from aggregate indices. |
| Trusted delivery and high-risk changes | `anthropic/claude-opus-5-20260723`, effort `max`, with an approved exact provider endpoint | Human review and project validation; if the approved endpoint is unavailable, stop rather than silently falling back | Claude is the strongest aggregate frontier candidate in this set, but OpenRouter publishes no delivery-safety or repository-validation score. | Set `allow_fallbacks=false` and require an approved endpoint; keep human approval, tests, and data-boundary checks mandatory. |
| Cheap fallback for reversible work | `qwen/qwen3.8-max-20260803`, effort `low`; Grok at `low` is an alternative | The task loops, produces an uncertain result, or fails validation: return to GPT or Claude rather than adding unreviewed writes | Qwen: agentic 58.4, `agents/fullstack` rank 4, `agents/webapps` rank 1; $2/M input and $6/M output. | Apply a token/budget ceiling. Never use this tier for trusted delivery or irreversible actions. |

The policy intentionally does not choose a single universal winner. The practical
cost frontier is: Grok for inexpensive agent loops, GPT-5.6 Sol for balanced
implementation, Kimi for fullstack-oriented specialization, and Claude Opus for
high-cost-of-error work. These roles must be rechecked when provider routing,
model snapshots, prices, or effort behavior change. See OpenRouter's [provider
routing](https://openrouter.ai/docs/guides/routing/provider-selection.md),
[model fallback](https://openrouter.ai/docs/guides/routing/model-fallbacks), and
[tool calling](https://openrouter.ai/docs/guides/features/tool-calling.md)
documentation.

For Zed harness and terminal-agent portability, hold the following constant in a
pilot: canonical model snapshot, effort, provider/fallback policy, tool schema,
`tool_choice`, context, output constraints, permissions, repository revision,
and validation command. Run the same task in both runtimes and record validated
completion, invalid tool calls, retries, stalls, elapsed time, actual provider,
actual model, and billed usage. OpenRouter's catalog cannot substitute for this
runtime evidence.

### Measured Runtime Matrix

| Runtime | Workload | Configuration | Quality | Cost | Latency | Reliability | Evidence | Decision |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Zed | Edit prediction (next-edit) | `ollama` + `sweep-next-edit` | Provisional | ~$0 | 5-10 s cold, <500 ms warm | TBD | [`zed-sweep-next-edit-ollama.md`](research/zed-sweep-next-edit-ollama.md) | Needs pilot validation before promotion |
| Zed | Planning | Not evaluated | - | - | - | - | CursorBench/OpenRouter policy only; no Zed pilot | Inherit global fallback |
| Zed | Safe implementation | Not evaluated | - | - | - | - | CursorBench/OpenRouter policy only; no Zed pilot | Inherit global fallback |
| Zed | Debugging and code review | Not evaluated | - | - | - | - | CursorBench/OpenRouter policy only; no Zed pilot | Inherit global fallback |
| Zed | Trusted delivery | Not evaluated | - | - | - | - | CursorBench/OpenRouter policy only; no Zed pilot | Inherit global fallback |

Use the scorecard and pilot template in
[`skills/workspace/agent-runtime/model-selection/references/selection-policy.md`](../skills/workspace/agent-runtime/model-selection/references/selection-policy.md)
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
