---
name: grilling
description: Grill the user relentlessly about a plan, decision, or idea. Use when the user wants to stress-test their thinking, or uses any 'grill' trigger phrases.
---

Interview until you reach a shared understanding. Map a **design tree**: every decision branches into the decisions that hang off it.

Work the tree in **rounds**. The **frontier** is every decision whose prerequisites are already settled. Ask the whole frontier in one round, then wait.

## Hard Rules

- Do not act on the plan until the user confirms shared understanding.
- Never ask the user for a fact you can look up. Dispatch a sub-agent for filesystem or codebase facts; only decisions go to the user.
- A question that depends on another still-open question belongs to a later round.
- Format every question with [question-format.md](question-format.md). Never use emoji as structure, or smash title, body, options, and suggestion into one paragraph.

## Procedure

1. Map the design tree from the current proposal and identify the frontier.
2. Ask every frontier question in one round, using the question card. Each question gets a labeled suggestion.
3. After answers, recompute the frontier and ask the next round.
4. Stop when the frontier is empty. Summarize settled decisions and wait for confirmation before acting.
