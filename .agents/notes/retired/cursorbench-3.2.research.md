# CursorBench 3.2 Research: Cost-Effective Model Use

Accessed: 2026-08-22

## Scope and source discipline

This note uses only Cursor-owned public sources. It records the complete published
CursorBench 3.2 leaderboard and derives score-cost comparisons from its displayed
values. It does not change a runtime, profile, or model default.

Primary sources:

- [CursorBench 3.2 leaderboard](https://cursor.com/evals) - published rows, task-version changelog, and cost methodology.
- [How we compare model quality in Cursor](https://cursor.com/blog/cursorbench) - CursorBench design and stated limits. This methodology article predates 3.2, so it is used only for durable suite-design claims, not for 3.2 rankings.
- [Cursor pricing](https://cursor.com/pricing) - confirms that plans include model usage and can bill on-demand usage; it does not supply a substitute per-task model cost.

Cursor describes 3.2 as an evaluation of agents on ambiguous, multi-file tasks from
real Cursor sessions. The leaderboard says higher scores are better. Its 3.2
changelog says that 3.1 added codebase-understanding, bugfinding, planning, and
code-review problems; 3.2 added instruction-following and advanced-tool-use
problems. Therefore the task mix is relevant to the requested workflow stages, but
no score is published for any individual stage or task category.

The methodology article says CursorBench is an internal offline suite based on real
engineering sessions. It sources tasks with Cursor Blame, pairs agent requests with
ground-truth solutions, uses agentic graders, and refreshes the suite periodically.
Cursor says it internally considers correctness, code quality, efficiency, and
interaction behavior, but publishes only the aggregate leaderboard fields below.

## Published CursorBench 3.2 rows

The table reproduces every displayed row from the [official leaderboard](https://cursor.com/evals).
`Extra High` is Cursor's displayed effort label; it is the configuration referred to
elsewhere as `xhigh`. Cost is the published average USD cost per task. Cursor says
it computes this from the model's published per-million-token input, cache-read,
cache-write, and output prices applied to the tokens used on each task. The page
reports that the July 2026 Terra and Luna figures were updated for adjusted pricing
and cache-write costs.

| Rank | Model and effort | Score | Cost / task | Tokens / task | Steps / task |
| ---: | --- | ---: | ---: | ---: | ---: |
| 1 | Grok 4.6 Extra High | 70.8% | $2.81 | 41,136 | 46 |
| 2 | Fable 5 Max | 70.5% | $17.32 | 103,525 | 72 |
| 3 | Opus 5 Max | 70.0% | $8.23 | 61,838 | 78 |
| 4 | Grok 4.6 High | 69.9% | $2.34 | 32,449 | 39 |
| 5 | Opus 5 Extra High | 69.3% | $7.35 | 54,239 | 72 |
| 6 | Fable 5 Extra High | 68.4% | $11.73 | 64,971 | 56 |
| 7 | GPT-5.6 Sol Max | 67.2% | $5.69 | 28,320 | 48 |
| 8 | Grok 4.6 Medium | 67.1% | $1.28 | 17,942 | 29 |
| 9 | Opus 5 High | 66.7% | $3.91 | 27,932 | 48 |
| 10 | Fable 5 High | 66.5% | $8.77 | 43,747 | 48 |
| 11 | Fable 5 Medium | 65.2% | $6.80 | 30,366 | 41 |
| 12 | GPT-5.6 Terra Max | 64.9% | $2.31 | 32,969 | 47 |
| 13 | GPT-5.6 Sol Extra High | 64.5% | $3.88 | 19,699 | 38 |
| 14 | Opus 5 Medium | 64.3% | $3.29 | 23,612 | 44 |
| 15 | GPT-5.6 Sol High | 63.5% | $2.79 | 13,867 | 32 |
| 16 | Opus 5 Low | 62.8% | $2.55 | 18,529 | 37 |
| 17 | Opus 4.8 Max | 62.3% | $5.77 | 71,411 | 44 |
| 18 | Fable 5 Low | 62.1% | $4.46 | 18,182 | 31 |
| 19 | Gemini 3.7 Flash High | 61.6% | $1.20 | 38,448 | 99 |
| 20 | Sonnet 5 Max | 61.5% | $4.30 | 92,882 | 86 |
| 21 | GPT-5.6 Luna Max | 61.1% | $0.39 | 87,973 | 61 |
| 22 | Grok 4.6 Low | 61.0% | $0.70 | 10,658 | 23 |
| 23 | Kimi K3 Max | 60.8% | $2.70 | 38,428 | 57 |
| 24 | GPT-5.6 Sol Medium | 60.0% | $1.95 | 9,747 | 27 |
| 25 | Kimi K3 High | 59.7% | $1.89 | 26,846 | 47 |
| 26 | Opus 4.8 Extra High | 59.4% | $4.50 | 51,121 | 40 |
| 27 | GPT-5.6 Terra Extra High | 59.2% | $1.15 | 16,089 | 29 |
| 28 | Gemini 3.7 Flash Medium | 59.0% | $0.95 | 30,953 | 82 |
| 29 | Sonnet 5 Extra High | 58.7% | $2.77 | 52,871 | 67 |
| 30 | GPT-5.5 High | 58.4% | $2.05 | 12,183 | 28 |
| 31 | GPT-5.5 Extra High | 58.4% | $2.85 | 17,534 | 32 |
| 32 | Opus 4.8 High | 58.0% | $3.15 | 33,548 | 33 |
| 33 | GPT-5.6 Luna Extra High | 57.7% | $0.23 | 22,480 | 48 |
| 34 | Sonnet 5 High | 56.9% | $2.13 | 39,483 | 57 |
| 35 | GPT-5.6 Luna High | 56.8% | $0.16 | 15,141 | 40 |
| 36 | Opus 4.8 Medium | 56.1% | $2.81 | 28,384 | 32 |
| 37 | Composer 2.5 | 56.1% | $0.44 | 14,286 | 33 |
| 38 | GLM 5.2 Max | 55.0% | $1.76 | 35,946 | 58 |
| 39 | GPT-5.6 Terra High | 54.2% | $0.71 | 9,468 | 23 |
| 40 | GPT-5.5 Medium | 53.8% | $1.51 | 8,522 | 25 |
| 41 | Gemini 3.7 Flash Low | 53.8% | $0.74 | 20,594 | 68 |
| 42 | Gemini 3.6 Flash High | 53.5% | $1.56 | 30,436 | 64 |
| 43 | Opus 4.8 Low | 53.1% | $2.02 | 19,624 | 27 |
| 44 | GPT-5.6 Sol Low | 52.6% | $1.01 | 5,104 | 19 |
| 45 | Sonnet 5 Medium | 52.4% | $1.44 | 26,200 | 46 |
| 46 | GLM 5.2 High | 51.5% | $1.19 | 21,829 | 49 |
| 47 | Gemini 3.6 Flash Medium | 51.2% | $1.48 | 28,511 | 62 |
| 48 | Kimi K3 Low | 50.5% | $0.99 | 13,007 | 33 |
| 49 | GPT-5.6 Terra Medium | 50.3% | $0.49 | 6,222 | 20 |
| 50 | Kimi K2.7 Code | 49.7% | $1.43 | 31,247 | 58 |
| 51 | GPT-5.6 Luna Medium | 47.7% | $0.08 | 7,095 | 28 |
| 52 | Sonnet 5 Low | 47.7% | $0.87 | 16,269 | 33 |
| 53 | Gemini 3.6 Flash Low | 47.4% | $1.13 | 20,529 | 50 |
| 54 | GPT-5.6 Terra Low | 46.9% | $0.42 | 5,312 | 19 |
| 55 | GPT-5.5 Low | 46.6% | $0.98 | 5,168 | 20 |
| 56 | GPT-5.6 Luna Low | 37.6% | $0.03 | 3,209 | 17 |

## Direct answer: Luna Extra High versus Terra High

For CursorBench's published score and cost dimensions, **GPT-5.6 Luna Extra High is
better value than GPT-5.6 Terra High**. It strictly dominates Terra High:

| Configuration | Score | Cost / task | Tokens / task | Steps / task |
| --- | ---: | ---: | ---: | ---: |
| GPT-5.6 Luna Extra High | 57.7% | $0.23 | 22,480 | 48 |
| GPT-5.6 Terra High | 54.2% | $0.71 | 9,468 | 23 |
| Luna Extra High minus Terra High | +3.5 percentage points | -$0.48 (-67.6%) | +13,012 (+137.4%) | +25 (+108.7%) |

Luna Extra High gives a 3.5-point higher published score at 32.4% of Terra High's
published cost. It uses about 2.4 times as many tokens and 2.1 times as many steps.
Those are not latency measurements, so this does not establish that it is faster or
more responsive. For a tight interactive-latency budget, compare the two locally.

## Pareto and cost-effectiveness findings

A configuration is score-cost Pareto-efficient when no published configuration has
both an equal-or-lower cost and an equal-or-higher score, with one strict improvement.
Using the displayed, rounded values, the frontier is:

| Configuration | Score | Cost / task | Tokens / task | Steps / task | Position |
| --- | ---: | ---: | ---: | ---: | --- |
| GPT-5.6 Luna Low | 37.6% | $0.03 | 3,209 | 17 | Cheapest observed point |
| GPT-5.6 Luna Medium | 47.7% | $0.08 | 7,095 | 28 | Cheapest point at about 48% |
| GPT-5.6 Luna High | 56.8% | $0.16 | 15,141 | 40 | Cheapest point at about 57% |
| GPT-5.6 Luna Extra High | 57.7% | $0.23 | 22,480 | 48 | More score than Luna High at low absolute cost |
| GPT-5.6 Luna Max | 61.1% | $0.39 | 87,973 | 61 | Cheapest point at about 61% |
| Gemini 3.7 Flash High | 61.6% | $1.20 | 38,448 | 99 | Small score gain after Luna Max, much more tool work |
| Grok 4.6 Medium | 67.1% | $1.28 | 17,942 | 29 | Largest quality jump near the $1-$2 band |
| Grok 4.6 High | 69.9% | $2.34 | 32,449 | 39 | Higher-quality escalation |
| Grok 4.6 Extra High | 70.8% | $2.81 | 41,136 | 46 | Highest published score |

All non-frontier rows are score-cost dominated by one of these published
configurations. In particular, every GPT-5.6 Terra effort is dominated:

| Terra configuration | Dominating configuration | Score change | Cost change |
| --- | --- | ---: | ---: |
| Low: 46.9%, $0.42 | Luna Medium: 47.7%, $0.08 | +0.8 points | -$0.34 |
| Medium: 50.3%, $0.49 | Luna High: 56.8%, $0.16 | +6.5 points | -$0.33 |
| High: 54.2%, $0.71 | Luna High: 56.8%, $0.16 | +2.6 points | -$0.55 |
| Extra High: 59.2%, $1.15 | Luna Max: 61.1%, $0.39 | +1.9 points | -$0.76 |
| Max: 64.9%, $2.31 | Grok 4.6 Medium: 67.1%, $1.28 | +2.2 points | -$1.03 |

This establishes a strong benchmark-only case against selecting any Terra effort for
score-cost value in CursorBench 3.2. It is not evidence about latency, reliability,
or use in a non-Cursor runtime.

`Luna Extra High` is Pareto-efficient but not necessarily the best escalation from
`Luna High`. Its extra $0.07 buys 0.9 score points, while the subsequent $0.16 from
Extra High to Max buys 3.4 points. If task routing can mix High and Max across a
portfolio, the displayed Extra High point is above the straight score-cost line
between them. That is an expected-value observation, not evidence that randomized
per-task routing has equivalent quality.

## Provisional workflow assignments

These are CursorBench-informed pilot assignments, not defaults. The benchmark task
mix supports treating its aggregate score as relevant to all four stages, but it
does not justify claims that one configuration is specifically best at planning,
safe implementation, debugging, review, or delivery.

| Workflow stage | Provisional candidate | Benchmark-backed rationale | What remains a hypothesis or requires local evidence |
| --- | --- | --- | --- |
| Planning | GPT-5.6 Luna High; escalate difficult plans to Luna Max | Luna High is the highest-scoring published configuration at or below $0.16 per task. The suite includes planning problems. | Plan completeness, clarification rate, and local codebase understanding are not reported by category. |
| Safe implementation | GPT-5.6 Luna Max as the low-cost pilot; Grok 4.6 Medium as its higher-quality comparison | Luna Max reaches 61.1% at $0.39. Grok Medium increases the aggregate score to 67.1% for $1.28 and uses 29 reported steps. The suite includes multi-file and advanced-tool-use problems. | "Safe" requires actual test execution, invalid-tool-call rate, permission behavior, diff reviewability, and repair work. None is published. |
| Debugging and review | GPT-5.6 Luna Max; compare Grok 4.6 Medium where failures are costly | The suite includes bugfinding and code-review problems, and both candidates lie on the score-cost frontier. | No bugfinding or review subscore is published. The 61 versus 29 step figures are not a latency measure. |
| Trusted delivery | Grok 4.6 Medium; escalate to Grok 4.6 High when the extra 2.8 points justify $1.06 more per task | Grok Medium has the highest aggregate score below $2 per task and is on the frontier; High is the next quality step. | Trusted delivery additionally requires repository-specific validation, data-boundary compliance, tool reliability, human approval, and rollout safeguards. CursorBench does not score them. |

The role rows express an economical escalation path, not verified specialization:
Luna High for inexpensive routine work, Luna Max for a cheap broad-capability
increase, and Grok Medium or High when the quality bar justifies their higher cost.
A local pilot must confirm whether that path holds for the target runtime and
repositories before any default changes.

## Limitations and blockers

- **Cursor-runtime evidence only:** CursorBench evaluates Cursor agents. It is direct evidence for the Cursor runtime, but only directional evidence for Zed, ACP, Claude Code, or any other runtime. Prompt construction, agent harness, tool schema, context handling, permissions, model routing, and sandboxing can change outcomes.
- **Configuration incompleteness:** the leaderboard identifies model and effort, but does not publish the Cursor version, agent prompt, tool definitions, provider/model snapshot, reasoning settings beyond effort, temperature, permissions, task count, repetition count, or confidence intervals.
- **Aggregate score only:** planning, bugfinding, code review, instruction following, and advanced tool use occur in the suite, but there are no per-category results. The proposed workflow mapping is therefore a hypothesis layered on an overall score-cost comparison.
- **No latency metric:** tokens and steps are published, but elapsed time, time to first useful action, throughput, queueing, and stall rate are not. More tokens or steps must not be converted into a latency claim.
- **No reliability or safety measure:** Cursor says it considers interaction behavior internally, but the table has no invalid-tool-call rate, retry/stall rate, instruction-adherence rate, security result, data-boundary result, or validated-completion rate. High benchmark score does not make autonomous delivery trusted.
- **Task and grader limits:** real internal sessions and agentic grading improve task realism but make the suite non-public and not independently reproducible. The task distribution may differ from the target repositories and workloads. Cursor says results are subject to variance and small score differences may not be statistically meaningful; no uncertainty information is published to evaluate individual gaps.
- **Price is a benchmark input, not a bill:** the reported cost is a calculation using published model-token prices. Actual Cursor plan allowances, on-demand charges, routing, cache behavior, quotas, and future price changes can make local billed cost differ.
- **Version drift:** 3.2 added task types relative to 3.1, so results must only be compared within 3.2. The leaderboard already records reporting updates for pricing. Re-check the live page before a pilot or policy decision.

The blocker to selecting a production default is not missing leaderboard rows. It is
missing representative local evidence for validation success, reliability, latency,
actual billed cost, data-boundary behavior, and the target runtime. No configuration
or default was edited as part of this research.
