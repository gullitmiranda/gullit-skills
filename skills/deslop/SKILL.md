---
name: deslop
description: Remove AI slop from code comments, docs, and generated text. Use when the user asks to deslop, clean up AI-generated artifacts, or tighten verbose AI prose before committing or opening a PR.
---

# Deslop

Remove AI slop: comments that restate code, sycophantic or filler prose,
buzzwords, decorative emoji, excessive emphasis. You know what slop looks like.

## Procedure

1. **Scope**: paths or diff from the user; otherwise the current working diff.
2. **Edit surgically**: delete noise, rewrite verbose prose to its shortest
   accurate form. Match surrounding style. Do not reformat or refactor.
3. **Report**: what was removed/rewritten per file. If nothing was slop, say so.

## Hard Rules

- Never delete license headers, linter directives, `TODO`/`FIXME`/`HACK` with
  context, or comments explaining *why* (constraints, workarounds, ticket refs).
- Never change code behavior. Comments and prose only.
- In doubt whether a comment carries information? Keep it and flag it.
