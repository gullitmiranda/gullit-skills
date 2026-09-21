# CursorBench 4.0 Research: Cost, Latency, and an Escalation Map

Accessed: 2026-09-21. Refreshed the same afternoon after Grok 4.7 rows
appeared on the live leaderboard.

## Scope and source discipline

This note records the complete published CursorBench 4.0 leaderboard, derives
score-cost and score-steps Pareto frontiers from its displayed values, and
proposes a provisional escalation map for the **Cursor** surface only. It does
not change a runtime, profile, or model default.

It supersedes the analysis in
[`cursorbench-3.2.research.md`](../retired/cursorbench-3.2.research.md) as the current
Cursor hypothesis source. The 3.2 note stays valid as a record of that suite;
**3.2 and 4.0 scores are not comparable** and must not be charted together.

Primary sources:

- [CursorBench 4.0 leaderboard](https://cursor.com/evals) - published rows, changelog, and cost methodology.
- [How we compare model quality in Cursor](https://cursor.com/blog/cursorbench) - suite design and stated limits.

Cursor published 4.0 on 2026-09-10, describing it as "new long-horizon problems
focused on edit, refactor, investigation, intent understanding, managing jobs,
and design adherence" on top of the 3.1 and 3.2 task types. The changelog also
records reporting updates for Sonnet 5 pricing, GPT-5.6 Terra and Luna pricing,
and cache-write costs for Sol, Terra, and Luna. Cursor states that results are
subject to variance and that small score differences may not be statistically
meaningful.

Absolute scores dropped sharply relative to 3.2 (top score 51.8% vs 70.8%),
which is consistent with a harder long-horizon task mix, not with a regression
in the models.

## Published CursorBench 4.0 rows

`Extra High` is Cursor's displayed effort label, written `XHigh` below. Cost is
the published average USD per task, computed by applying each model's published
per-million-token input, cache-read, cache-write, and output prices to the
tokens it used.

| Rank | Model and effort | Score | Cost / task | Tokens / task | Steps / task |
| ---: | --- | ---: | ---: | ---: | ---: |
| 1 | Fable 5.1 Max | 51.8% | $17.28 | 117,236 | 128 |
| 2 | Fable 5.1 XHigh | 51.6% | $13.01 | 87,294 | 101 |
| 3 | Fable 5.1 High | 49.2% | $9.08 | 58,438 | 77 |
| 4 | Fable 5.1 Medium | 46.8% | $7.05 | 45,411 | 63 |
| 5 | Opus 5 Max | 46.6% | $11.95 | 85,384 | 106 |
| 6 | Opus 5 XHigh | 46.1% | $11.43 | 80,094 | 103 |
| 7 | Fable 5.1 Low | 45.1% | $5.44 | 34,795 | 51 |
| 8 | Opus 5 High | 44.7% | $9.00 | 61,405 | 86 |
| 9 | Opus 5 Medium | 43.3% | $6.94 | 45,272 | 72 |
| 10 | GPT-5.6 Sol Max | 41.7% | $8.23 | 42,944 | 99 |
| 11 | Muse Spark 1.3 Max | 41.6% | $2.64 | 52,005 | 98 |
| 12 | Grok 4.6 XHigh | 41.4% | $6.10 | 49,814 | 56 |
| 13 | GPT-5.6 Terra Max | 41.3% | $5.14 | 60,814 | 107 |
| 14 | Opus 5 Low | 40.7% | $4.87 | 31,995 | 57 |
| 15 | Grok 4.6 High | 40.4% | $5.20 | 41,387 | 48 |
| 16 | Gemini 3.8 Flash High | 39.6% | $4.70 | 162,565 | 324 |
| 17 | GPT-5.6 Sol XHigh | 37.7% | $4.40 | 24,729 | 55 |
| 18 | Muse Spark 1.3 XHigh | 37.5% | $2.10 | 40,891 | 83 |
| 19 | Gemini 3.8 Flash Medium | 37.3% | $4.06 | 128,364 | 290 |
| 20 | Grok 4.6 Medium | 36.1% | $3.48 | 24,893 | 40 |
| 21 | GPT-5.6 Luna Max | 35.9% | $1.03 | 87,284 | 208 |
| 22 | GPT-5.6 Sol High | 35.7% | $2.85 | 16,174 | 41 |
| 23 | Sonnet 5 Max | 34.1% | $7.17 | 149,257 | 140 |
| 24 | GPT-5.6 Terra XHigh | 33.6% | $1.81 | 23,436 | 43 |
| 25 | Grok 4.6 Low | 33.4% | $2.25 | 16,307 | 32 |
| 26 | Muse Spark 1.3 High | 33.4% | $1.66 | 30,654 | 69 |
| 27 | GPT-5.6 Luna XHigh | 33.0% | $0.44 | 40,598 | 98 |
| 28 | Muse Spark 1.3 Medium | 32.6% | $1.49 | 27,255 | 64 |
| 29 | Sonnet 5 XHigh | 32.0% | $4.55 | 83,373 | 102 |
| 30 | GPT-5.6 Sol Medium | 31.1% | $1.77 | 10,111 | 32 |
| 31 | Sonnet 5 High | 30.8% | $3.48 | 61,146 | 85 |
| 32 | GPT-5.6 Terra High | 30.7% | $1.11 | 13,162 | 33 |
| 33 | GPT-5.6 Luna High | 29.4% | $0.25 | 23,368 | 64 |
| 34 | Muse Spark 1.3 Low | 29.3% | $0.93 | 17,483 | 47 |
| 35 | Sonnet 5 Medium | 28.0% | $2.31 | 39,114 | 65 |
| 36 | Composer 2.5 | 27.7% | $0.68 | 17,347 | 41 |
| 37 | GPT-5.6 Terra Medium | 27.6% | $0.64 | 7,307 | 25 |
| 38 | GPT-5.6 Terra Low | 25.2% | $0.52 | 5,914 | 23 |
| 39 | GPT-5.6 Sol Low | 24.6% | $0.87 | 4,885 | 21 |
| 40 | Muse Spark 1.3 Minimal | 24.3% | $0.56 | 10,620 | 34 |
| 41 | Sonnet 5 Low | 24.1% | $1.39 | 23,772 | 46 |
| 42 | GPT-5.6 Luna Medium | 22.2% | $0.08 | 7,642 | 32 |
| 43 | GPT-5.6 Luna Low | 16.0% | $0.03 | 3,288 | 18 |

The morning snapshot of this page had 43 rows and no Grok 4.7. The afternoon
reread of [the same leaderboard](https://cursor.com/evals) added four rows
without a changelog entry on the evals page or on cursor.com/changelog:

| Rank | Model and effort | Score | Cost / task | Tokens / task | Steps / task |
| ---: | --- | ---: | ---: | ---: | ---: |
| 6 | Grok 4.7 Extra High | 46.3% | $6.01 | 70,141 | 88 |
| 10 | Grok 4.7 High | 43.9% | $4.69 | 56,382 | 71 |
| 13 | Grok 4.7 Medium | 41.6% | $3.49 | 36,683 | 60 |
| 30 | Grok 4.7 Low | 33.1% | $1.58 | 15,677 | 40 |

Ranks of later rows shift down. Cursor's evals changelog still dates the suite
to 2026-09-10 and does not mention Grok 4.7. Independent evidence that the
*rows appeared today*: this note's morning fetch lacked them; the afternoon
fetch had them. That is not the same as a Cursor launch announcement.

## Score-cost Pareto frontier (all published rows)

A configuration is score-cost Pareto-efficient when no published configuration
has both an equal-or-lower cost and an equal-or-higher score, with one strict
improvement. Using the displayed, rounded values:

| Configuration | Score | Cost / task | Steps | Marginal cost of the step up |
| --- | ---: | ---: | ---: | --- |
| Luna Low | 16.0% | $0.03 | 18 | cheapest observed point |
| Luna Medium | 22.2% | $0.08 | 32 | $0.01 per point |
| Luna High | 29.4% | $0.25 | 64 | $0.02 per point |
| Luna XHigh | 33.0% | $0.44 | 98 | $0.05 per point |
| Luna Max | 35.9% | $1.03 | 208 | $0.20 per point |
| Muse Spark 1.3 XHigh | 37.5% | $2.10 | 83 | $0.67 per point |
| Muse Spark 1.3 Max | 41.6% | $2.64 | 98 | $0.13 per point |
| Fable 5.1 Low | 45.1% | $5.44 | 51 | $0.80 per point |
| Fable 5.1 Medium | 46.8% | $7.05 | 63 | $0.95 per point |
| Fable 5.1 High | 49.2% | $9.08 | 77 | $0.85 per point |
| Fable 5.1 XHigh | 51.6% | $13.01 | 101 | $1.64 per point |
| Fable 5.1 Max | 51.8% | $17.28 | 128 | $21.35 per point |

Three families carry the entire frontier: **Luna, Muse Spark, and Fable**.
Everything else is dominated at every published effort.

Notable exclusions:

- **Every GPT-5.6 Sol effort is dominated.** Sol Max scores 41.7% at $8.23
  while Muse Spark Max scores 41.6% at $2.64 - a 0.1-point gap that Cursor's
  own variance caveat makes meaningless, for 3.1x the cost. There is no budget
  band in which 4.0 supports choosing Sol.
- **Every GPT-5.6 Terra effort is dominated**, repeating the 3.2 finding with a
  different dominator (Muse Spark rather than Luna).
- **Every Opus 5 effort is dominated by Fable 5.1.** Opus Max reaches 46.6% at
  $11.95; Fable Medium reaches 46.8% at $7.05. Opus is the best available
  ceiling when Fable is absent, not an independently efficient choice.
- Fable Max buys 0.2 points for $4.27 over Fable XHigh and should be treated as
  equivalent quality at 1.3x the cost.

## Score-cost frontier under the observed local catalog

Observed on 2026-09-21: **Muse Spark 1.3** is available (it had been disabled in
local settings, now re-enabled). **Fable 5.1 is disabled at the org level** and
requires an org-side change. **Sonnet 5 is disabled locally** by operator
choice, which the data supports - Sonnet is dominated at every effort on both
frontiers, so there is no cost or latency reason to re-enable it. With Fable
removed, the cost frontier collapses to a short ladder:

| Configuration | Score | Cost / task | Steps | Marginal cost of the step up |
| --- | ---: | ---: | ---: | --- |
| Luna Low to XHigh | 16.0 to 33.0% | $0.03 to $0.44 | 18 to 98 | $0.01-0.05 per point |
| Luna Max | 35.9% | $1.03 | 208 | $0.20 per point |
| Muse Spark 1.3 XHigh | 37.5% | $2.10 | 83 | $0.67 per point |
| Muse Spark 1.3 Max | 41.6% | $2.64 | 98 | $0.13 per point |
| Opus 5 Medium | 43.3% | $6.94 | 72 | **$2.53 per point** |
| Opus 5 High | 44.7% | $9.00 | 86 | $1.47 per point |
| Opus 5 XHigh | 46.1% | $11.43 | 103 | $1.74 per point |
| Opus 5 Max | 46.6% | $11.95 | 106 | $1.04 per point |

Muse Spark 1.3 Max at $2.64 dominates twelve more expensive published
configurations: Sol High, Grok 4.6 Medium, Sonnet 5 High, Gemini 3.8 Flash
Medium, Sol XHigh, Sonnet 5 XHigh, Gemini 3.8 Flash High, Opus 5 Low, Terra Max,
Grok 4.6 High, Grok 4.6 XHigh, and Sonnet 5 Max. The entire $2.64-$6.94 band is
empty of efficient points, so the ladder has a real gap there: the next quality
increase costs $4.30 for 1.7 points.

## Score-steps frontier (published steps, not latency)

Steps per task is a published tool-loop metric, **not** an elapsed-time
measurement. It is recorded separately because the frontier it produces is
almost disjoint from the cost frontier:

| Configuration | Score | Steps | Cost / task |
| --- | ---: | ---: | ---: |
| Luna Low | 16.0% | 18 | $0.03 |
| Sol Low | 24.6% | 21 | $0.87 |
| Terra Low | 25.2% | 23 | $0.52 |
| Terra Medium | 27.6% | 25 | $0.64 |
| Grok 4.6 Low | 33.4% | 32 | $2.25 |
| Grok 4.6 Medium | 36.1% | 40 | $3.48 |
| Grok 4.6 High | 40.4% | 48 | $5.20 |
| Fable 5.1 Low | 45.1% | 51 | $5.44 |
| Fable 5.1 Medium | 46.8% | 63 | $7.05 |
| Fable 5.1 High | 49.2% | 77 | $9.08 |

Grok 4.6 appears nowhere on the cost frontier but is the only step-efficient
family in the mid range: Grok 4.6 High reaches 40.4% in 48 steps, while Luna Max
reaches 35.9% in 208 steps. Gemini 3.8 Flash is the opposite extreme at 290-324
steps. Fable is the only family that leads both frontiers at once; Opus is
step-expensive as well as dollar-expensive.

Because CursorBench publishes no elapsed time, the step counts support a
"fewer tool turns" claim but not a "faster" claim. Treat this frontier as a
hypothesis about interactive responsiveness and operator waiting time.

## Cost is a tiebreaker here, not a constraint

The frontiers above optimize published cost per task. That is the wrong primary
objective for this operator, and the correction changes the map more than any
single data point in this note.

Established on 2026-09-21: the operator is a **member** (not admin) of an
employer-covered Cursor org, never hits a usage limit, and sees no on-demand
lines. Model spend is absorbed by the employer. The operator still declines to
waste that money without reason. That makes the decision rule:

```text
1. filter:    quality sufficient for the task
2. objective: least operator time (tool turns, then rework)
3. tiebreak:  least cost among quality-equivalent options
```

Cost therefore ranks third, not first. Two consequences:

- **The Luna track loses its reason to exist for interactive work.** Its only
  advantage was price. Luna Max scores 35.9% in 208 steps; Grok 4.6 High scores
  40.4% in 48 steps. More quality, roughly a quarter of the turns.
- **Terra returns to the map.** It is dominated at every effort on the cost
  frontier, but Terra Low (23 steps) and Terra Medium (25 steps) sit *on* the
  step frontier. Eliminating Terra was an artifact of optimizing dollars.

## Provisional escalation map

These are CursorBench-informed pilot assignments for the Cursor surface, not
defaults, and not evidence of per-stage specialization - 4.0 publishes no
category subscores.

Configurations are grouped into quality clusters using Cursor's own variance
caveat: scores within 2 points are treated as indistinguishable. Within each
cluster, step counts within 5% of the faster configuration (or 5 steps,
whichever is larger) are a time tie, then cost decides. Fable 5.1 is excluded
(disabled at org level) and Sonnet 5 is excluded (disabled locally, and
dominated at every effort on both frontiers). The morning assignment of
Opus 5 High as ceiling and Grok 4.6 Extra High as interactive standard is
superseded by the Grok 4.7 rows.

| Tier | Interactive (operator waiting) | Background / subagent | Use for |
| --- | --- | --- | --- |
| Ceiling, 44.7-46.6% | **Grok 4.7 Extra High** ($6.01, 88 steps) | same | Ambiguous multi-file work, plan implementation, migrations, risky review |
| Standard, 43.3-43.9% | **Grok 4.7 High** ($4.69, 71 steps) | **Muse Spark 1.3 Max** ($2.64, 98 steps) | Normal implementation and review |
| Light, 32.6-36.1% | **Grok 4.6 Medium/Low** ($3.48 / $2.25, 40 / 32 steps) | **Luna XHigh** ($0.44, 98 steps) | Bounded edits, recon, drafts |
| Trivial, 24-28% | **Terra Medium** ($0.64, 25 steps) | **Terra Low** ($0.52, 23 steps) | Renames, lint fixes, lookups, throwaway drafts |

The interactive and background columns are the same evaluation under different
weights, not separate evaluations. Background work is not waited on, so turn
count stops mattering and the cost tiebreaker runs free; interactive work
inverts that. This is why the map needs one measurement pass and two columns.

Fallback: if Grok 4.7 Extra High is not exposed, Opus 5 High ($9.00, 86 steps)
is the next ceiling cell. If Grok 4.6 leaves the catalog, Grok 4.7 Low
($1.58, 40 steps) replaces the interactive Light row.

Supporting observations:

- **Grok 4.7 Extra High takes the ceiling from Opus 5 High.** Same 2-point
  cluster (46.3% vs 44.7%). Steps are a tie (88 vs 86, 2.3%). Cost is 33%
  lower ($6.01 vs $9.00). Opus Extra High and Opus Max remain dominated.
- **Grok 4.7 High is the unique pick in its cluster** (43.9%, 71 steps,
  $4.69), strictly better than Opus 5 Medium on score, steps, and cost.
- **Grok 4.6 remains the step king below ~41%.** 4.6 High (48 steps) and 4.6
  Low (32 steps) still win their interactive clusters. Keep 4.6 for Light
  interactive until it leaves the catalog.
- **Fable 5.1 High vs Grok 4.7 Extra High is no longer a free upgrade.**
  Fable High is 49.2% in 77 steps at $9.08; Grok 4.7 Extra High is 46.3% in
  88 steps at $6.01. Enabling Fable still buys 2.9 points and 11 fewer turns,
  but it costs $3.07 more per task, not $0.08.
- **Top score is 51.8%**, so roughly half of these tasks fail even at the
  Fable ceiling. Published cost per task therefore understates true cost,
  which includes retries and human repair time.

## Surface constraint: effort is fixed for subagents

Observed on 2026-09-21. The Cursor chat model picker exposes an effort control,
but the subagent model list exposes effort **bound into the slug**:
`gpt-5.6-luna-max`, `gpt-5.6-terra-xhigh`, `gpt-5.6-sol-medium`,
`claude-opus-5-thinking-high`, `cursor-grok-4.6-high-fast` (re-check for
Grok 4.7 slugs), `glm-5.2-high`,
`kimi-k3-max`, `kimi-k2.7-code`, `gemini-3.1-pro`, `gemini-3.6-flash-high`,
`composer-2.5-fast`.

Consequences for the map: `Luna XHigh`, `Terra Medium`, `Terra Low`, and
`Grok 4.6 XHigh/Medium/Low` have no subagent slug, and the only exposed Luna is
Max - the one configuration the map advises against. The subagent list also
appears to reflect locally enabled models, so it should be re-read after any
change in the model settings rather than assumed stable.

## Local telemetry: what is and is not recoverable

Checked on 2026-09-21, to test whether past sessions could supply observational
evidence instead of a pilot.

- `~/.cursor/projects/*/agent-transcripts/` - empty in every project. No JSONL
  transcripts exist on this machine.
- `globalStorage/conversation-search.db` (44 MB) - FTS index over title and
  body only. No model, tokens, or cost.
- `globalStorage/state.vscdb` (19 GB) - 1,328 conversations (`composerData:`)
  and 290,156 messages (`bubbleId:`). `modelInfo.modelName` is present on
  **5,522 of 290,156 messages (1.9%)**. `tokenCount` is present on 100% of
  messages and is `{inputTokens: 0, outputTokens: 0}` on **100% of them**.

So local history can identify the model for about 2% of messages and carries no
token or cost data at all. Retroactive cost attribution is not possible. The
bubbles do retain `cursorRules`, `toolResults`, and `capabilities`, so they
remain a possible (thin) sample for rule-adherence analysis.

Observed model distribution across those 5,522 messages, as a record of actual
habit rather than of quality: `gpt-5.5` 2,200; `claude-sonnet-4-6` 575;
`claude-4.6-opus-high-thinking` 486; `claude-4.6-sonnet-medium-thinking` 348;
`gpt-5.6-terra` 297; `gpt-5.4-medium` 221; `claude-opus-4-7` 192; `grok-4.6`
159; `gpt-5.6-sol` 146; `gpt-5.6-luna` 62; `claude-opus-5` 23; single-digit
counts for `kimi-k3`, `composer-2.5`, and `claude-fable-5`. The map's
recommended configurations are barely represented in past usage, so adopting it
is a habit change rather than a refinement.

## Server-side cost data: not available on this account

Cursor removed dollar figures from the Usage page and the CSV export for
self-serve plans (individual and Teams) on 2026-07-31. The Usage page now shows
token counts only, `dashboard/get-filtered-usage-events` returns
`chargedCents: 0`, and because the change is applied on read, **historical
exports were zeroed too**. Enterprise plans kept the dollar view.

The supported route for real cost is the Teams
[Admin API](https://cursor.com/docs/account/teams/admin-api):
`POST https://api.cursor.com/teams/filtered-usage-events` returns event-level
`chargedCents` (model cost plus Cursor Token Rate, reconciling with
`/teams/spend`), filterable by model and user, rate-limited to 60 requests per
minute and polled at most hourly. It requires an admin key.

This operator is a member without admin access, so per-model billed cost is not
obtainable. Practical fallbacks:

- Treat the published `$/task` as a **relative** proxy for plan consumption.
  The ordering across models holds even when the absolute figure is not the
  bill.
- Token counts per model are still visible on the Usage page, which is enough
  to reproduce CursorBench's own methodology (published token prices applied to
  observed tokens) against the operator's real task mix.
- Dashboard - Spending still reports on-demand totals for the cycle, but this
  account has no on-demand lines.

Absent admin access, none of this blocks the outstanding work: quality, rule
adherence, MCP reliability, and wall-clock time are all measurable locally, and
they are the dimensions the leaderboard does not cover.

## Limitations and blockers

- **Cursor-surface evidence only.** 4.0 evaluates Cursor agents. It is direct
  evidence for Cursor and only directional for Zed, Claude Code, ACP, or
  terminal agents. Prompt construction, tool schema, context handling,
  permissions, routing, and sandboxing can change outcomes.
- **Suite version boundary.** 4.0 results must not be compared with 3.2 or
  charted on the same axis. Rankings changed materially between suites - Grok
  4.6 XHigh led 3.2 and sits mid-table in 4.0.
- **Aggregate score only.** No per-category results for planning, bugfinding,
  review, instruction following, or tool use. The track map is a hypothesis
  layered on an aggregate comparison.
- **No variance data.** Cursor warns that small differences may not be
  meaningful but publishes no confidence intervals, task count, or repetition
  count. Treat gaps under about 2 points as unresolved.
- **No latency, reliability, or safety metric.** Steps and tokens are published;
  elapsed time, stall rate, invalid-tool-call rate, instruction-adherence rate,
  and validated-completion rate are not.
- **Price is a benchmark input, not a bill** - and on this account it is not
  even the operator's money. Reported cost applies published token prices;
  actual plan allowances, routing, and cache behaviour differ, and per-model
  billed cost is unobtainable without admin access. Use it as a relative
  tiebreaker only.
- **Catalog coverage gaps.** GLM 5.2, Kimi K3, Kimi K2.7 Code, and Gemini 3.1
  Pro are exposed locally but absent from 4.0. In 3.2, Kimi K3 Max scored 60.8%
  at $2.70 and GLM 5.2 Max 55.0% at $1.76, both competitive - but suites are not
  comparable, so this is a reason for a pilot, not a map position.
- **Unmeasured factors that dominate this workspace.** Skill and rule adherence
  across a large loaded skill set, MCP tool-use reliability (Linear, Slack,
  GitHub), long-context retention, and Portuguese output quality are not scored
  by CursorBench at all.

## What a pilot must close before any default changes

One local pilot, one task set, scored under both weightings (interactive and
background). Cost is recorded as a relative proxy, not measured in dollars.

1. **Validate the step-count proxy.** Every time-based claim here rests on
   published steps, not elapsed time. Measure wall-clock time for Grok 4.6
   XHigh against Muse Spark Max and Opus 5 High; if turns do not translate into
   time, the interactive column collapses into the background column and the
   whole two-column structure is unnecessary.
2. **Measure what the benchmark omits.** Skill and rule adherence, MCP
   tool-call failures (Linear, Slack, GitHub), long-context retention, and
   repair work per task. Rule adherence grades objectively: build tasks whose
   correct answer only exists if the skill was read and followed - wrong
   account under `gh-profile`, skipped worktree under `git-worktree`, a git
   write inside the cache under `ai-skills-cache-safety`, a worktree path in a
   PR body under `publish-safe-links`.
3. **Place GLM 5.2 and Kimi K3 Max on the same task set**, since they have no
   4.0 evidence at all. This is the only route to positioning them, because
   external leaderboards do not run the Cursor harness.
4. **Re-check the leaderboard for the Chinese models.** Cursor scored GLM 5.2
   Max, Kimi K3 (Max/High/Low), and Kimi K2.7 Code in 3.2, so they may return
   to 4.0 at zero effort. See the review trigger below.
5. **Confirm the Fable request.** If the org enables Fable 5.1, re-run the
   ceiling tier against **Grok 4.7 Extra High**, not Opus High. Fable High is
   still higher quality and fewer turns, but it is no longer a same-price swap.

The Cursor SDK (`@cursor/sdk` / `cursor-sdk`) can drive the same prompt across
configurations programmatically; see the `sdk` skill. A minimal harness of 8
tasks across 6 configurations is roughly 50 runs.

## Review triggers specific to this note

- CursorBench publishes a new suite version, adds rows for a new model family
  version (this fired for Grok 4.7 on 2026-09-21), or adds GLM 5.2, Kimi K3,
  Kimi K2.7 Code, or Gemini 3.1 Pro to 4.0.
- Fable 5.1 becomes enabled at the org level.
- The operator gains admin access, or starts hitting a usage limit or
  on-demand billing - either event promotes cost from tiebreaker back to
  constraint and rehabilitates the Luna track.
- The subagent model list changes, since it gates which map rows are
  executable.
- Local pilot evidence contradicts the step-count proxy.

No configuration, profile, or default was edited as part of this research.
