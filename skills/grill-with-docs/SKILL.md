---
name: grill-with-docs
description: "Grilling session that challenges your plan against the existing domain model, sharpens terminology, and updates documentation inline: CONTEXT.md for glossary terms, specs for evolving behavior and implementation plans, and ADRs only for durable architectural trade-offs. Use when user wants to stress-test a plan against their project's language and documented decisions."
---

<what-to-do>

Interview me relentlessly about every aspect of this plan until we reach a shared understanding. Walk down each branch of the design tree, resolving dependencies between decisions one-by-one. For each question, provide your recommended answer.

Ask the questions one at a time, waiting for feedback on each question before continuing.

If a question can be answered by exploring the codebase, explore the codebase instead.

</what-to-do>

## Hard Rules

- `CONTEXT.md` is a glossary and nothing else — totally devoid of implementation details. Never use it as a spec, scratch pad, or decision log.
- Specs are the default working document for evolving behavior, scenarios, requirements, constraints, open questions, implementation approach, and decision rationale.
- Offer an ADR only when all three hold: (1) hard to reverse, (2) surprising without context, (3) the result of a real trade-off. Otherwise keep rationale in the spec.
- Create files lazily — only when you have something to write.
- Update docs inline as terms/decisions resolve. Don't batch.

## Doc locations

```
/
├── CONTEXT.md                  ← glossary (single-context repos)
├── CONTEXT-MAP.md              ← if present, multi-context; points to per-context CONTEXT.md/specs/docs/adr
├── specs/                      ← specs (also common: docs/specs/)
└── docs/adr/                   ← ADRs
```

Prefer the repo's existing spec location. In multi-context repos, context-specific specs and ADRs live under each context directory (e.g. `src/ordering/specs/`, `src/ordering/docs/adr/`); system-wide ones stay at root. `CONTEXT-MAP.md` is discovery (points to per-context docs); the per-context docs are the authority — they complement each other, never override.

Formats: [CONTEXT-FORMAT.md](./CONTEXT-FORMAT.md), [ADR-FORMAT.md](./ADR-FORMAT.md).

## During the session

- **Challenge against the glossary** — when the user's term conflicts with `CONTEXT.md`, call it out immediately: "Your glossary defines 'cancellation' as X, but you seem to mean Y — which is it?"
- **Sharpen fuzzy language** — propose a precise canonical term for vague or overloaded words.
- **Discuss concrete scenarios** — invent edge-case scenarios that force precision about boundaries between concepts.
- **Cross-reference with code** — when the user states how something works, check the code; surface contradictions.
- **Update docs inline** — resolved term → `CONTEXT.md` now; resolved behavior/plan → active spec now (create or propose a focused spec if none exists and the plan needs durable capture).
