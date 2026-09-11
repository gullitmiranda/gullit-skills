# Orchestration Cast

Present the cast in **bullets** in chat (default). Use a wide markdown table
only when the user asks for a table or when writing a durable artifact that
benefits from columns. Keep the cast outside any handoff fence.

Surface names: `Cursor local` | `Cursor cloud` | `Zed Agent` |
`ACP:<named-agent>` | `Terminal:<cli>`. Never write bare `ACP`.

## Chat format (default)

Lead with one line: mode, remaining scope, commit policy.

Then one bullet per **critical-path** role:

```markdown
- **<Role>** (<block id if any>) — <surface> · **<concrete model>** · effort <n/a|value>
  Fallback: <concrete model or surface alternative>.
  Does: <one line>. Write set: <paths/packages>. Capsule: implement|review|n/a.
  Order: <first | after <Role> | parallel with <Role>>.
```

Optional / deferred roles go under a separate heading **Deferred (not on
critical path)** — do not mix them into the main bullets.

Close with: review fixed point(s), spec/plan paths, when reviews fire.

## Hard presentation rules

- **Concrete model required** for every role. Name a model the **surface**
  actually exposes (user-facing name or slug). `inherit` is allowed only as
  **Fallback**, never as the primary Model cell/line — except Orchestrator,
  which may be `Composer (parent)` / current parent model.
- If the preferred model is ineligible on the chosen surface (for example CW
  gateway on Cursor in the current setup), mark `unavailable` and propose a
  surface change — do not invent a slug.
- Reviewers must name a model **different from the writer** when more than one
  is exposed; do not write “≠ writer if available” without picking one.
- **Order must be honest:** use `parallel with` only when work can start at the
  same time on disjoint write sets. If B needs A’s interface or commit, write
  `after <A>` — do not fake parallelism.
- Cast **remaining work only** when the branch is mid-flight. Do not re-list
  completed plan steps as active writers.
- Keep the critical-path cast short (typically ≤6 bullets). Park dual-delivery
  twins, optional worktrees, and speculative roles under Deferred.

## Role heuristics (operational defaults)

Pick only from models the **current surface actually exposes**. If a preferred
model is missing, write `unavailable` and the next best exposed option — do
not invent slugs.

| Role | Prefer | Avoid |
| --- | --- | --- |
| Orchestrator | Parent session model | Downgrading while writers use stronger models |
| Implementer | Strongest coding-capable exposed model for the block | `inherit` as primary; shared write sets |
| Review Spec | Different family from the writer when exposed | Same model+transcript as the writer |
| Review Standards | Different from both writer and Spec when possible | Merging Standards and Spec into one agent |
| Validation / glue | Smaller/faster coding model when exposed | Overspending a max model on Makefile glue |
| Exploration | Main agent for bounded reading; fast subagent only for substantial independent work | Delegating a small lookup or final synthesis |

Effort: set only when the surface exposes it; otherwise `n/a`.

## Capsule types

- **implement**: goal, decisions, constraints, paths, validation commands (`context-capsule` template).
- **review**: diff command, commit list, spec/plan paths, standards paths only — see `context-capsule` review rule. No implementer debug narrative.

## Delegation threshold

One role (orchestrator=implementer) is the default. Add another role only when
its work passes the delegation gate in `../SKILL.md`. Paths alone do not define
write-set independence: artifacts that encode the same evolving decision are a
coupled semantic write set and stay with one writer. Final synthesis remains
with the orchestrator.
