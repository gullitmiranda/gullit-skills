---
name: user-preferences
description: Canonical portable preferences for guma across all projects and agent runtimes. Load before creating, editing, or publishing a durable or publishable artifact.
---

# User Preferences

This is the canonical cross-runtime policy for guma. Runtime-specific instructions
must load this skill before artifact work; do not add agent-specific behavior here.

Before adding a preference, check whether it is runtime-specific or task-specific.
Keep portable personal policy here and route the rest to the relevant runtime adapter
or topical skill.

## How to Interpret My Instructions

My instructions are approximate. I'm not the one doing the work — you are, and you see the reality I can't. My words are pointers toward what I actually want: the simplest, cleanest, most correct outcome. That goal outranks my literal wording, in any context — not just implementation, but debugging, research, planning, ops, writing, anything.

When you hit a wall — a command that doesn't work as I described, a constraint that contradicts another, a case that doesn't fit, an assumption that fails — the wall is information. Something is wrong with the instruction, the assumption, or the approach. Stop and reconsider. Don't patch around it.

If the right path diverges from what I said, diverging is correct: take it and present the divergence. An honest blocker is a good outcome. A "working" result built on workarounds — flags, special cases, conversion shims, parallel paths — is the worst outcome, regardless of effort already spent.

Exception: during migrations, adapters and conversion shims between old and new interfaces are legitimate design, not workarounds. See `codebase-design`.

## Artifact language

- Write all durable and publishable technical artifacts in English by default: source code, code comments, documentation, plans, commit messages, pull requests, issues, review comments, release notes, and generated text intended for publication.
- Use another language only when the user explicitly requests it or a repository instruction or applicable task-specific skill explicitly requires it.
- Do not infer an artifact's language from the language of the conversation.

## Naming preferences

- Prefer using `work` instead of organization- or employer-specific abbreviations in directory and namespace naming when the value is not a fixed identifier.

## Link formatting

- When referencing any external resource, include a clickable URL whenever possible; compact raw URLs are welcome and often preferred over label-only references, and bare numbers or abbreviations should only be used when no URL is available.

## Git commit destinations

- In the user's **personal** GitHub repos (owner `gullitmiranda`, e.g. `~/code/gullit/...`), committing/pushing directly to `main` is allowed without explicit per-task confirmation. The safety skill's "never commit to main/master" rule applies to shared or organizational repos, not personal ones. Still keep commits well-scoped and reversible.

## PR Review Comments

- When the user asks to resolve PR review comments from automated review agents, handle each targeted comment individually by replying in GitHub or updating the PR, whichever best resolves it, and then mark the thread/comment as resolved before finishing.
