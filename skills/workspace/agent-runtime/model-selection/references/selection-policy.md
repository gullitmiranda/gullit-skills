# Selection Policy Reference

Use this reference with `model-selection` to turn a model-choice question into
a comparable, reversible decision. It adds evaluation detail to the durable
policy in [`docs/model-selection.md`](../../../../../docs/model-selection.md).

The orchestration surface must already be fixed (see `agent-selection`
surfaces reference). Do not treat surface as a dimension of the model product.

## Evaluation Record

Create one record per candidate and task. Capture values as observed, with a
date and source for any quoted price or benchmark.

```markdown
## Candidate

- Surface (named) and version:
- Profile or execution mode:
- Provider / endpoint / routing:
- Model snapshot:
- Effort:
- Thinking / mode:
- Tier / Fast / other surface toggles:
- Relevant surface settings:
- Price or quota source and date:

## Task

- Workload:
- Repository state or fixture:
- Prompt and context:
- Available tools and permissions:
- Validation command or review criterion:

## Result

- Outcome:
- Validation result:
- Elapsed time:
- Retries or interventions:
- Tool failures or stalls:
- Observed cost or proxy:
- Safety or data-boundary concerns:
- Notes and confounders:
```

Avoid recording credentials, private prompts, source code, customer data, or
other sensitive context. Use a safe fixture, redacted summary, or local-only
note when the task cannot be shared.

## Effort / thinking map (vendor)

| Surface / API | Effort-like | Thinking-like | Notes |
| --- | --- | --- | --- |
| OpenAI Responses | `reasoning.effort` | (internal reasoning tokens) | GPT-5.6 also has `reasoning.mode` |
| Anthropic API | `output_config.effort` | `thinking.type` adaptive/enabled/disabled | UI thinking toggle ≠ effort |
| Claude Code | `/effort`, env, settings | thinking toggle / budgets | Defaults vary by model |
| Gemini | — | `thinkingLevel` / `thinkingBudget` | Do not set both |
| Cursor | effort picker | thinking UI / Fast | Plan may lock knobs |
| Zed / OpenRouter | catalog effort | provider-dependent | Record actual returned provider |

## Pilot Design

A useful pilot is small enough to finish and varied enough to resemble real
work. Select tasks from the intended workload, for example:

| Workload | Representative task | Required evidence |
| --- | --- | --- |
| Question or planning | Summarize a bounded code area and propose a plan. | The plan is grounded in the repository and names verification steps. |
| Safe implementation | Make a small, validated code or documentation change. | The requested change is complete and focused checks pass. |
| Review | Identify material issues in a bounded diff. | Findings are accurate, actionable, and do not invent defects. |
| Debugging | Reproduce and isolate a known failure. | The explanation matches evidence and the proposed fix is validated. |
| Trusted delivery | Prepare a release or delivery step with explicit safeguards. | The agent observes permissions, destination, and validation constraints. |

Keep these factors constant for a candidate comparison whenever possible:

- orchestration surface and agent implementation;
- repository revision or fixture;
- task prompt and supplied context;
- profile, tools, permissions, and sandbox;
- completion and validation criteria;
- time and budget limits;
- Fast / service tier unless that is the single changed variable.

If an important factor differs, mark the result as directional rather than
comparable.

## Scorecard

Score qualitatively unless the user has defined numeric thresholds. A numeric
score can hide a critical reliability or safety failure.

| Dimension | Questions |
| --- | --- |
| Quality | Was the result correct, complete, maintainable, and validated? |
| Reliability | Did it follow instructions, use tools correctly, and finish without repeated recovery? |
| Cost | What was the effective cost per validated completion, including retries? |
| Latency | How long until useful work began and validation completed? |
| Operator effort | How much clarification, correction, and supervision was required? |
| Surface fit | Did context, tool use, sandboxing, and provider routing behave predictably on this surface? |
| Safety | Did it respect approvals, data boundaries, and execution constraints? |

A candidate with an unresolved safety, data-boundary, correctness, or
reliability failure is not eligible for a default, regardless of its cost or
latency.

Among eligible candidates, prefer lowest effective cost per validated
completion (or lowest operator time if cost is flat), then lower effort/tier.

## Interpreting External Evidence

Record external evidence as a hypothesis with its scope:

```markdown
- Source:
- Source URL:
- Date accessed:
- Suite version:
- Surface / harness:
- Provider, model snapshot, effort, and mode:
- Benchmark task mix:
- Comparable to target workload: yes / partial / no
- What this evidence can support:
- What local pilot is still required:
```

Examples of common limits:

- A benchmark that uses a different editor, tool schema, or harness may not
  predict results on Cursor, Zed Agent, Claude Code, or a named ACP agent.
- A benchmark may omit effort level, thinking mode, price tier, or retries.
- Suite versions are not comparable (for example CursorBench 3.2 vs 4.0).
- A public task set may not represent the repository's language, tests, or
  risk profile.
- Usage telemetry (OpenRouter rankings, Zed Agent Metrics) can show adoption
  or latency trends but cannot prove quality.

## Decision Template

```markdown
# Model Selection Decision: <surface and workload>

## Decision

- Selected configuration:
- Previous configuration:
- Fallback:
- Effective date:
- Review trigger:

## Evidence

- Local pilot:
- Comparable benchmark:
- Pricing and latency observations:
- Known uncertainty:

## Rationale

Why this is the smallest configuration that reliably meets the workload's
quality, safety, latency, and cost constraints (lowest validated $/completion,
then lower effort/tier).

## Follow-up

- Next task cohort:
- Owner:
- Decision review date or event:
```

## Default Promotion Checklist

Before promoting a candidate to a global or profile-specific default, verify:

- [ ] The full configuration and target surface are recorded.
- [ ] Hard filters (privacy, eligibility, plan, parameters) passed.
- [ ] The pilot represents the intended workload and has objective validation.
- [ ] Quality and reliability meet the documented bar.
- [ ] Cost and latency are acceptable for the intended use.
- [ ] Safety, data-boundary, and permission behavior were observed.
- [ ] A known-good fallback exists.
- [ ] The decision and review trigger are documented.

If any item is incomplete, keep the current default and describe the smallest
additional pilot needed.
