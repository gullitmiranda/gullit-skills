# Selection Policy Reference

Use this reference with `model-selection` to turn a model-choice question into
a comparable, reversible decision. It adds evaluation detail to the durable
policy in [`docs/model-selection.md`](../../../docs/model-selection.md).

## Evaluation Record

Create one record per candidate and task. Capture values as observed, with a
date and source for any quoted price or benchmark.

```markdown
## Candidate

- Runtime and version:
- Profile or execution mode:
- Provider:
- Model:
- Effort:
- Thinking mode:
- Relevant runtime settings:
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

- repository revision or fixture;
- task prompt and supplied context;
- profile, tools, permissions, and sandbox;
- completion and validation criteria;
- time and budget limits.

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
| Runtime fit | Did context, tool use, sandboxing, and provider routing behave predictably? |
| Safety | Did it respect approvals, data boundaries, and execution constraints? |

A candidate with an unresolved safety, data-boundary, correctness, or
reliability failure is not eligible for a default, regardless of its cost or
latency.

## Interpreting External Evidence

Record external evidence as a hypothesis with its scope:

```markdown
- Source:
- Source URL:
- Date accessed:
- Runtime:
- Provider, model, effort, and mode:
- Benchmark task mix:
- Comparable to target workload: yes / partial / no
- What this evidence can support:
- What local pilot is still required:
```

Examples of common limits:

- A benchmark that uses a different editor, tool schema, or harness may not
  predict results in Zed, Cursor, Claude Code, or ACP.
- A benchmark may omit effort level, thinking mode, price tier, or retries.
- A public task set may not represent the repository's language, tests, or
  risk profile.
- Usage telemetry can show adoption or availability but cannot prove quality.

## Decision Template

```markdown
# Model Selection Decision: <runtime and workload>

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
quality, safety, latency, and cost constraints.

## Follow-up

- Next task cohort:
- Owner:
- Decision review date or event:
```

## Default Promotion Checklist

Before promoting a candidate to a global or profile-specific default, verify:

- [ ] The full configuration and target runtime are recorded.
- [ ] The pilot represents the intended workload and has objective validation.
- [ ] Quality and reliability meet the documented bar.
- [ ] Cost and latency are acceptable for the intended use.
- [ ] Safety, data-boundary, and permission behavior were observed.
- [ ] A known-good fallback exists.
- [ ] The decision and review trigger are documented.

If any item is incomplete, keep the current default and describe the smallest
additional pilot needed.
