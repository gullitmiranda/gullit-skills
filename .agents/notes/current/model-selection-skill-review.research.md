# Model-selection skill / policy review

Accessed: 2026-09-11

**Status:** research complete (no skill rewrite)

**Scope:** Validate the durable `model-selection` skill and
[`docs/model-selection.md`](../../../docs/model-selection.md) against primary
sources. Focus on the selection unit and evidence hierarchy, plus related claims
about effort/thinking, runtime differences, public leaderboards, and agentic
cost.

**Artifact location:** Repo convention places research notes under
`.agents/notes/current/*.research.md` ([`.agents/AGENTS.md`](../../AGENTS.md)).
Preferred path `.agents/research/` is not the tracked layout; this file follows
the notes convention.

---

## Verdict

The policy is **substantially correct**. Treating the selection unit as more
than a model family name, ranking local target-runtime evidence above general
leaderboards, refusing to promote usage telemetry as quality, and optimizing for
validated completion (including retries and operator time) are all supported by
first-party provider docs, runtime docs, and first-party benchmark methodology.

The main improvements are **precision**, not direction: expand the selection
unit with a few configuration dimensions providers already treat as first-class
(provider routing / endpoint, service tier / Fast mode, reasoning mode, model
snapshot); clarify that “thinking mode” maps differently across vendors; treat
provider capability/pricing constraints as hard filters earlier than rank-5
“docs claims”; and note that runtime-specific public benches (CursorBench, AA
coding-agent index) still need version + harness + effort recorded before they
can populate measured matrix cells.

Confidence on the core selection unit and evidence hierarchy: **strong signal**.
Confidence that every listed related claim holds across all named runtimes:
**strong** for effort/thinking and cost inflation; **strong** for runtime
non-transferability as a design claim; **partial** for quantifying how large
Cursor↔Claude Code↔Zed↔ACP gaps are on identical tasks (primary sources show
different harnesses/capabilities/metrics, not a controlled same-task crosswalk).

---

## What's correct (with citations)

### 1. Selection unit is not “model family alone”

Providers expose independent controls that change quality, latency, and cost:

| Vendor | First-class control | Material claim |
| --- | --- | --- |
| OpenAI | `reasoning.effort` (+ separate `reasoning.mode` on GPT-5.6) | Lower effort favors speed/token usage; higher effort thinks more completely for higher quality. Modes `standard`/`pro` are independent of effort. ([Reasoning models](https://developers.openai.com/api/docs/guides/reasoning)) |
| Anthropic | `output_config.effort` + adaptive/manual thinking | Effort is soft guidance for how often/deeply Claude thinks; levels from `low` to `max`/`xhigh` change behavior. ([Thinking steering and cost](https://platform.claude.com/docs/en/build-with-claude/thinking-steering-and-cost); [Claude Help: model/effort/thinking](https://support.claude.com/en/articles/8664678-change-the-model-effort-and-thinking-settings)) |
| Google | `thinkingBudget` / `thinkingLevel` | Thinking improves final-response quality; billed on full thought tokens; lowering thinking level reduces cost/latency. ([Gemini thinking](https://ai.google.dev/gemini-api/docs/thinking)) |
| Claude Code | model + effort + thinking toggles | Same product surface: effort controls adaptive reasoning depth; thinking is a separate UI/API concern. ([Claude Code model config](https://code.claude.com/docs/en/model-config)) |
| Cursor | model + effort + Fast mode + plan pools | Start plan locks medium effort and blocks Fast; Fast variants are priced higher (often ~2×). ([Cursor Models & Pricing](https://cursor.com/docs/models-and-pricing)) |
| OpenRouter / Zed | model + upstream **provider** routing | Same model id can hit different endpoints; `order`, `allow_fallbacks`, `require_parameters`, etc. change routing. ([OpenRouter provider routing](https://openrouter.ai/docs/guides/routing/provider-selection.md); [Zed gateway docs](https://zed.dev/docs/ai/use-a-gateway)) |

The skill’s compact unit
`provider + model + effort + thinking mode + runtime` is therefore directionally
right: provider docs treat effort/thinking as part of the effective
configuration, and gateways make “provider” more than a brand label.

### 2. Never silently change runtime/profile defaults

Claude Code documents layered defaults (user settings, project/managed settings,
org defaults, env vars, session-only `/model`), including cases where choosing a
model does **not** persist as the saved default. ([Claude Code model
config](https://code.claude.com/docs/en/model-config)) Cursor pricing and plan
tiers constrain which effort/Fast settings are even available.
([Models & Pricing](https://cursor.com/docs/models-and-pricing)) The skill’s
hard rule against silent default changes matches how these products actually
store and override configuration.

### 3. Usage telemetry is not a quality benchmark

OpenRouter’s rankings page states explicitly that token-volume rankings
“measure adoption, not quality” and do not rank accuracy, reasoning, or
benchmark performance. ([OpenRouter rankings](https://openrouter.ai/rankings))

Zed Agent Metrics publishes popularity and turn-time distributions and
documents that turn time depends on model configuration, context size, task
complexity, and infrastructure; model-level breakdowns are unavailable for many
external ACP agents. ([Zed Agent Metrics](https://zed.dev/agent-metrics)) That
matches the policy’s warning that Zed metrics must not be the sole basis for
choosing a model.

### 4. Do not transfer benchmark rankings across runtimes without validation

Cursor’s own methodology says CursorBench tasks come from real Cursor sessions
and agents are evaluated in Cursor’s production-aligned harness; public
benchmarks (SWE-bench family, Terminal-Bench puzzle tasks) are called out as
poorly aligned with developer agent work. ([How we compare model quality in
Cursor](https://cursor.com/blog/cursorbench); [Composer 2 technical
report](https://cursor.com/resources/Composer2.pdf)) Cursor also ships an SDK so
third parties can run the **same agent loop** in their harness—implying that
changing the loop is a different measurement.
([Cursor evals / SDK](https://cursor.com/docs/evals))

Artificial Analysis’s Coding Agent Index aggregates **agent variants** on
end-to-end software-engineering tasks (DeepSWE, Terminal-Bench, SWE-Atlas-QnA)
with pass@1 and pooled cost/token/time metrics—not a bare model-family Elo.
([Coding Agent Index methodology](https://artificialanalysis.ai/methodology/coding-agents-benchmarking/))

ACP is a protocol with negotiated capabilities (session, MCP, auth, filesystem /
terminal surfaces differing by version). Different agents behind ACP are not the
same runtime merely because the editor speaks ACP.
([ACP v2 overview](https://agentclientprotocol.com/rfds/v2/overview);
[initialization](https://agentclientprotocol.com/protocol/v2/initialization);
Zed’s cross-agent metrics narrative: [Agent Metrics](https://zed.dev/agent-metrics))

### 5. Do not optimize nominal token price over validated completion / safety / operator time

Primary sources treat higher reasoning as **conditional**, not free quality:

- OpenAI: increase to `high`/`xhigh` only when evals show a measurable gain;
  “Higher reasoning effort isn't automatically better” and can cause
  overthinking, unnecessary searching, or quality regressions under weak stop
  criteria or open-ended tools.
  ([Model guidance / latest-model](https://developers.openai.com/api/docs/guides/latest-model);
  [Reasoning models](https://developers.openai.com/api/docs/guides/reasoning))
- Anthropic: thinking tokens are billed as output; prior thinking in context is
  billed as input; in a tool-use loop each request has its own `max_tokens`, so
  that cap does **not** bound whole-turn spend.
  ([Thinking steering and cost](https://platform.claude.com/docs/en/build-with-claude/thinking-steering-and-cost))
- Gemini: pricing is based on full thought tokens even when only a summary is
  returned; lowering thinking level is the recommended cost/latency control.
  ([Gemini thinking](https://ai.google.dev/gemini-api/docs/thinking))
- Cursor: Fast modes and Max Mode (legacy) change effective $/token; plan pools
  and Cursor Token Rate alter operator bill beyond raw API sticker price.
  ([Models & Pricing](https://cursor.com/docs/models-and-pricing))

The skill’s “effective cost per validated completion, including retries” and
operator-effort scorecard match these mechanics.

### 6. Evidence hierarchy

The ordered ladder—

1. local results in the target runtime
2. comparable reproducible evals
3. runtime-specific public benchmarks
4. general benchmarks
5. provider docs/pricing

—aligns with Cursor’s hybrid offline (CursorBench) + online (live traffic /
controlled ablations) process, and with Cursor’s critique that public benches
fail alignment, grading, and contamination tests for coding agents.
([CursorBench blog](https://cursor.com/blog/cursorbench))

Placing CursorBench above general SWE/Arena-style benches for Cursor defaults is
justified by Cursor’s first-party claim that CursorBench better separates models
developers experience as different. Using OpenRouter/AA indices only as
hypotheses for other runtimes matches those products’ own scope (OpenRouter
usage ≠ quality; AA index = specific agent-suite aggregate).

### 7. Pilot methodology (one variable; capture outcome/time/retries/cost/intervention)

OpenAI’s guidance to raise effort only when **evals** justify the cost/latency,
Anthropic’s note that agent harnesses often steer thinking per step via prompts
while holding request parameters fixed (to preserve cache), and AA’s
multi-attempt pass@1 plus cost/time reporting all support small, controlled
pilots with confounders recorded.
([Reasoning](https://developers.openai.com/api/docs/guides/reasoning);
[Thinking steering](https://platform.claude.com/docs/en/build-with-claude/thinking-steering-and-cost);
[AA coding-agent methodology](https://artificialanalysis.ai/methodology/coding-agents-benchmarking/))

### 8. Recommend smallest config that meets the quality bar; keep known-good fallback

Supported by OpenAI’s “not automatically better” / overthinking warning and by
Anthropic’s advice that if `max_tokens` truncates, either raise the cap **or**
lower effort when the task was over-thought.
([Latest-model guidance](https://developers.openai.com/api/docs/guides/latest-model);
[Thinking cost control](https://platform.claude.com/docs/en/build-with-claude/thinking-steering-and-cost))

### 9. Boundary with `agent-selection`

`agent-selection` owns per-role picks inside an execution cast and says durable
profile/default changes require `model-selection` with evidence.
(`agent-selection` skill hard rules.) That split matches the problem: cast
choices are orchestration; promoting a default is a measured configuration
change. No primary-source conflict found.

### Related claims (explicit checks)

| Claim | Verdict | Primary support |
| --- | --- | --- |
| Effort/thinking materially changes results for Claude, GPT, Gemini, etc. | **Correct** | OpenAI effort table; Anthropic effort table + Help Center; Gemini thinking quality + billing ([links above](#1-selection-unit-is-not-model-family-alone)) |
| Cursor vs Claude Code vs Zed vs ACP can differ for the “same” model | **Correct as a systems claim** | Different tools/harnesses (CursorBench production loop; Claude Code config surface; Zed OpenRouter routing + multi-agent ACP metrics; ACP capability negotiation). Not a published same-prompt multi-runtime bake-off. |
| Public leaderboards should narrow candidates, not declare coding-agent winners | **Correct** | OpenRouter: adoption ≠ quality. Cursor: public benches misaligned. AA Agentic Index FAQ-style guidance: composite score vs use-case-specific benchmarks ([Agentic Index](https://artificialanalysis.ai/models/capabilities/agentic)). LMSYS/Arena historically ranks chat preference / category votes, not IDE agent completion ([LMSYS Arena site migration](https://www.lmsys.org/blog/2024-09-20-arena-new-site/); methodology blogs). |
| Agentic cost pitfalls (retries, tool loops inflate effective cost) | **Correct** | Anthropic per-request `max_tokens` in tool loops; billed thinking tokens; Gemini full-thought billing; OpenAI higher effort + pro mode increase tokens/latency; Cursor Fast/Max surcharges. |

---

## Gaps / inaccuracies

1. **Selection unit is slightly incomplete relative to first-party APIs.**
   The five-tuple omits dimensions that primary docs treat as material:
   - **Model snapshot / version** (Claude Code warns about remaps/retirement;
     catalogs use dated slugs).
   - **Upstream provider / endpoint / routing policy** (OpenRouter `provider`
     object; Zed custom models).
   - **Service tier / Fast / priority** (Cursor Fast pricing; OpenAI Fast /
     service-tier notes).
   - **Reasoning mode** (`standard` vs `pro` on GPT-5.6), distinct from effort.
   - **Context / Max Mode / extended context** (Cursor Max Mode API+20%; large
     context windows change cost behavior).
   - **Plan / quota constraints** (Cursor Start locks effort/Fast).
   Prose elsewhere in the skill already mentions tools/sandbox/context; the
   compact formula should not imply those are optional footnotes.

2. **“Thinking mode” is overloaded across vendors.**
   Anthropic’s product UI separates **effort** from a **thinking toggle**; the
   API uses adaptive vs enabled thinking types; Gemini uses budget/level;
   OpenAI mostly folds “thinking” into reasoning effort/mode. Without a short
   mapping note, operators may equate Cursor “thinking” UI with Claude effort.

3. **Evidence hierarchy ranks “provider documentation and pricing” last.**
   Correct for *quality marketing claims*. Incorrect if read as “ignore pricing
   until the end”: availability, privacy/ZDR, data-retention (e.g. Cursor notes
   on Fable), unsupported parameters, and plan locks are **constraints** that
   should filter candidates before pilots. The durable doc already mentions
   constraints in step 1 of the procedure; the hierarchy bullet list can be
   misread in isolation.

4. **CursorBench placement is right for Cursor, with two caveats.**
   - Cursor itself says offline graders can look good while online developer
     experience regresses—so “runtime-specific public/offline bench” is not the
     top of Cursor’s own ladder; **online** signals sit alongside it.
     ([CursorBench blog](https://cursor.com/blog/cursorbench))
   - Suites are versioned (blog notes 3.1 vs older scores not comparable; policy
     cites 3.2 in places). Scores must be scoped to suite version/date.

5. **AA / OpenRouter “general” evidence sometimes already includes effort.**
   AA agentic listings and OpenRouter catalog fields expose effort/reasoning
   metadata. The skill correctly says to record configuration; it should not
   imply all public indices are effort-agnostic. When the leaderboard row
   *is* a full config, it is still not a Zed/Cursor/Claude Code transfer proof.

6. **“Smallest configuration” is underspecified.**
   Primary sources optimize different axes (effort, model tier, Fast mode,
   autonomy). Without defining “smallest” (lowest effort that passes? cheapest
   validated $/success? least privilege?), recommendations can disagree.

7. **ACP is a protocol, not a homogeneous runtime.**
   Grouping “ACP” next to Cursor/Zed/Claude Code is fine as a *surface*, but
   selection must name the **agent implementation** behind ACP (Claude Agent,
   Codex, Zed Agent, etc.), as Zed’s metrics already distinguish them.

8. **Provisional matrices in `docs/model-selection.md` create policy tension.**
   Disclaimers say hypotheses-only, but concrete CursorBench/OpenRouter stage
   tables look like defaults. That does not falsify the skill’s rules, but it
   increases the risk of violating “don’t promote a benchmark rank to a
   default” in practice.

9. **No first-party source found that ranks LMSYS/Arena as a coding-agent
   completion winner.**
   The skill’s caution is correct; any internal wording that treats Arena Elo
   as interchangeable with CursorBench/AA coding-agent pass@1 would be wrong.

10. **Broken / stale internal references (integrity, accessed 2026-09-11).**
    - Skill links to [`zed-sweep-next-edit-setup.md`](../../../skills/workspace/agent-runtime/model-selection/zed-sweep-next-edit-setup.md)
      which is **missing**.
    - Docs matrix cites [`research/zed-sweep-next-edit-ollama.md`](../../../docs/research/zed-sweep-next-edit-ollama.md)
      which is **missing**.
    - Evidence hierarchy still links `[CursorBench](https://cursorbench.github.io/)` —
      that URL returns **404**. Canonical page is
      [cursor.com/cursorbench](https://cursor.com/cursorbench) (also historically
      [cursor.com/evals](https://cursor.com/evals)).
    - Durable doc’s “CursorBench 3.2 Cost-Effective Operating Policy” (accessed
      2026-08-22) is **suite-stale**: as of 2026-09-10 Cursor publishes
      **CursorBench 4.0** with a new long-horizon task mix and a different
      score/cost frontier (e.g. Fable 5.1 Max leads; Luna/Grok absolute scores
      are not comparable to 3.2). The *methodology* of the skill remains right;
      the numeric stage table does not.

11. **Lean-skill fit.**
    `SKILL.md` body is ~64 lines (lean target ~20–40). Procedure density and
    the decision template earn some of that length; residual cut candidates
    are restating the docs intro and the missing zed-sweep pointer.

---

## Recommended improvements (prioritized)

### P0 — Fix broken links and quarantine stale CursorBench 3.2 table

- Remove or restore the missing `zed-sweep-next-edit-*` links.
- Replace `cursorbench.github.io` with `https://cursor.com/cursorbench`.
- Move the 3.2 numeric operating policy into the dated research note
  (`.agents/notes/current/cursorbench-3.2.research.md`) and either refresh a
  **4.0 hypothesis shortlist** after a new pass or leave the durable doc
  procedure-only until a pilot exists. OpenRouter stage tables should stay
  clearly labeled as shortlist hypotheses, not defaults.

### P0 — Clarify the selection unit

Expand the canonical unit (in skill + durable doc) to something like:

```text
runtime (+ agent implementation)
+ provider/endpoint/routing
+ model snapshot
+ effort (+ reasoning mode if distinct)
+ thinking/budget controls as exposed by that runtime
+ material runtime toggles (Fast/Max/context, tools, sandbox, permissions)
```

Keep a short form for chat, but require the evaluation record to capture the
full set (the existing candidate template is already close).

### P0 — Split constraints vs quality evidence

In the evidence hierarchy, state explicitly:

- **Hard filters first:** privacy, data boundary, plan availability, supported
  parameters, approved endpoints.
- **Then** the quality ladder (local → comparable evals → runtime benches →
  general benches → qualitative docs).

Pricing remains both a filter (budget) and a scored dimension (effective
$/validated completion).

### P1 — Vendor mapping note for effort/thinking

Add a one-screen reference:

| Runtime/API | Effort-like | Thinking-like | Notes |
| --- | --- | --- | --- |
| OpenAI Responses | `reasoning.effort` | (internal reasoning tokens) | GPT-5.6 also has `reasoning.mode` |
| Anthropic API | `output_config.effort` | `thinking.type` adaptive/enabled/disabled | UI toggle ≠ effort |
| Claude Code | `/effort`, env, settings | thinking toggle / `MAX_THINKING_TOKENS` | Defaults vary by model |
| Gemini | — | `thinkingLevel` / `thinkingBudget` | Don’t set both |
| Cursor | effort picker | thinking UI / Fast | Plan may lock knobs |

### P1 — Strengthen leaderboard interpretation rules

Require every external score to record: source URL, date, suite version, agent
harness, model snapshot, effort/mode, provider endpoint if known, task mix, and
what local pilot remains. Explicitly classify OpenRouter token rankings and Zed
session/turn metrics as **adoption/ops**, not quality.

### P1 — Define “smallest configuration”

Operationalize as: among candidates that meet the quality/safety bar with
acceptable reliability, prefer the one with lowest **effective cost per
validated completion** (or lowest operator time if cost is flat), and only then
prefer lower effort/tier. Document the tie-break.

### P2 — Align Cursor evidence with Cursor’s hybrid loop

For Cursor default promotion, treat CursorBench as necessary but not
sufficient; note online/regression signals or a small live pilot cohort, matching
Cursor’s own methodology.

### P2 — ACP wording

Say “ACP client + named agent,” not “ACP” as if it were one model runtime.

### P3 — Optional: add service-tier / Fast to pilot confounders

When comparing Cursor candidates, hold Fast vs standard constant unless that
is the single changed variable.

---

## Primary sources consulted

| Source | URL | Used for |
| --- | --- | --- |
| OpenAI — Reasoning models | https://developers.openai.com/api/docs/guides/reasoning | Effort levels, quality/latency/cost tradeoff, reasoning mode |
| OpenAI — Model guidance / latest model | https://developers.openai.com/api/docs/guides/latest-model | “Higher effort isn’t automatically better”; evals-gated escalation |
| Anthropic — Thinking steering and cost | https://platform.claude.com/docs/en/build-with-claude/thinking-steering-and-cost | Effort table; thinking billing; tool-loop `max_tokens` |
| Anthropic Help — Model, effort, thinking | https://support.claude.com/en/articles/8664678-change-the-model-effort-and-thinking-settings | Product UI: effort vs thinking as separate settings |
| Claude Code — Model configuration | https://code.claude.com/docs/en/model-config | Runtime-specific model/effort/thinking defaults and precedence |
| Google AI — Gemini thinking | https://ai.google.dev/gemini-api/docs/thinking | Thinking improves quality; full-thought billing; lower level for cost |
| Cursor — Models & Pricing | https://cursor.com/docs/models-and-pricing | Effort locks, Fast pricing, pools, Max Mode, Token Rate |
| Cursor — How we compare model quality | https://cursor.com/blog/cursorbench | CursorBench methodology; public-bench limits; online+offline |
| Cursor — CursorBench page | https://cursor.com/cursorbench | Suite versions / task mix framing |
| Cursor — Evals / SDK | https://cursor.com/docs/evals | Same agent loop for external evals |
| Cursor — Composer 2 technical report | https://cursor.com/resources/Composer2.pdf | Production harness evaluation claim |
| Zed — Agent Metrics | https://zed.dev/agent-metrics | Telemetry ≠ quality; cross-agent ACP metrics; turn-time confounders |
| Zed — Use a gateway | https://zed.dev/docs/ai/use-a-gateway | OpenRouter provider routing in Zed |
| OpenRouter — Rankings | https://openrouter.ai/rankings | Usage rankings are not quality |
| OpenRouter — Provider routing | https://openrouter.ai/docs/guides/routing/provider-selection.md | Provider selection changes effective endpoint |
| Artificial Analysis — Coding Agent Index methodology | https://artificialanalysis.ai/methodology/coding-agents-benchmarking/ | Agent-variant index; pass@1; cost/tokens/time |
| Artificial Analysis — Agentic Index | https://artificialanalysis.ai/models/capabilities/agentic | Composite vs use-case interpretation |
| Artificial Analysis — Intelligence benchmarking | https://artificialanalysis.ai/methodology/intelligence-benchmarking/ | Broader index composition (context) |
| Agent Client Protocol — v2 overview / init / migration | https://agentclientprotocol.com/rfds/v2/overview ; https://agentclientprotocol.com/protocol/v2/initialization ; https://agentclientprotocol.com/protocol/v2/migration | Runtime capability differences under ACP |
| LMSYS — Arena new site | https://www.lmsys.org/blog/2024-09-20-arena-new-site/ | Arena scope expansion / chat-origin context |
| Internal policy under review | `docs/model-selection.md`, `model-selection` skill + `references/selection-policy.md`, `agent-selection` skill | Claims being validated |

**Not used as authorities:** secondary blogs, Reddit, or third-party “ClaudeKit”
guides (encountered in search; discarded for claim support).

---

## Bottom line for skill maintainers

Keep the hard rules and evidence ladder. Tighten the selection-unit formula and
constraint-vs-evidence wording so the skill matches how OpenAI, Anthropic,
Google, Cursor, Zed, OpenRouter, AA, and ACP actually expose configuration.
Do not weaken the “pilot in the target runtime” requirement—primary sources
increasingly treat the **agent harness** as part of the measurement.
