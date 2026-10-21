# Coding-Agent Benchmarks for Build and Review Casts

Accessed: 2026-10-21.

## Question

CursorBench was the main hypothesis source for build casts. Is it still the
right source when most build work runs on Zed Agent or a terminal agent backed
by an employer gateway that serves frontier models and self-hosted open-weight
models (GLM, Kimi, DeepSeek, Qwen)? Which public benchmarks fit better?

## Conclusion

- CursorBench stays valid for the **Cursor** surface only. It measures Cursor's
  harness, so it cannot rank configurations for Zed or a terminal agent.
- No single public benchmark replaces it. Use a small evidence stack, one source
  per question, and treat every row as a hypothesis until a local pilot on the
  target surface confirms it.
- For self-hosted open-weight models, public rows describe the **vendor's
  serving** (precision, context length, sampling). A self-hosted deployment with
  different quantization, context caps, or output caps is a different
  configuration. Public rows only narrow candidates.

## Evidence stack

| Question | Source | Why | Main limit |
| --- | --- | --- | --- |
| Build: head-to-head on the exact candidates | [DeepSWE v1.1](https://deepswe.datacurve.ai/) | Freshly written repo tasks; rows include `glm-5.3`, `kimi-k3`, `deepseek-v4-*`, and the frontier set; reports cost, steps, and confidence intervals | Fresh tasks may under-represent large legacy codebases |
| Build: one composite number | [Artificial Analysis Coding Agent Index](https://artificialanalysis.ai/agents/coding-agents) | Composite of DeepSWE, Terminal-Bench, and a repo Q&A suite; reports cost, tokens, time per task | Composite weights hide per-skill profile; chart rows render client-side |
| Review and "would this merge" quality | [FrontierCode 1.1](https://cognition.com/frontiercode) | Graded on maintainer mergeability (correctness, tests, scope discipline, codebase standards), not only on passing tests; covers Kimi K3, GLM 5.3, DeepSeek V4.1 Flash, Fable 5.1, and the frontier set | Grades a model's own patches; a proxy for review judgment, not reviewing someone else's diff |
| Terminal-agent realism | [Terminal-Bench](https://www.tbench.ai/) (4.0, via Artificial Analysis) | Closest task shape to a terminal coding agent | Small task count, wide confidence intervals; read repeats, not one score |
| Long-horizon and context resilience | [METR time horizons](https://metr.org/time-horizons) (concept) and an Artificial Analysis long-context eval (rows) | Only public signals on long tasks and long-context reasoning | METR states it is no longer actively updated; no live long-horizon *coding* benchmark was verified |
| Cursor surface only | [CursorBench](https://cursor.com/evals) | Same harness as the target when the surface is Cursor | Does not transfer to other surfaces |

Verified directly on 2026-10-21: DeepSWE v1.1 lists `glm-5.3`, `kimi-k3`, and
`deepseek-v4-*`; FrontierCode 1.1 uses mergeability as the grading standard and
lists Kimi K3, GLM 5.3, DeepSeek V4.1 Flash, and Fable 5.1. Other version
numbers and row coverage above come from a delegated research pass and were
not re-verified line by line.

## Not worth using for this decision

- Aider polyglot: stale and single-file edit-format compliance, not agent work.
- LiveCodeBench and contest-style suites: wrong task distribution.
- SWE-bench Verified as a primary ranking: saturation and contamination
  concerns; SWE-bench Pro is better documented but covers older open-weight
  generations and mixes capped and uncapped runs.
- Usage telemetry (OpenRouter rankings, editor agent metrics): adoption, not
  quality.

## What no public benchmark covers

These need the local pilot:

- behavior under the surface's compaction policy and the model's real usable
  window (combined prompt plus completion caps);
- output caps that truncate large file writes;
- silent routing changes: provider fallbacks, budget downgrades, or reroutes
  that swap the model mid-thread;
- skill and rule adherence, tool-call reliability on the surface's tool schema,
  and latency at long prompt lengths.

## Follow-up

- Run a representative pilot on the target surface before changing any default
  (see `docs/model-selection.md`, Decision Procedure).
- Refresh this note when DeepSWE, FrontierCode, or Terminal-Bench publish a new
  suite version, or when a new self-hosted snapshot becomes available.
