---
name: skill-writing
description: Write or audit agent skills following the lean-skill standard. Use when creating a new skill, reviewing an existing SKILL.md, or when a skill feels verbose, bloated, or ignored by the agent.
---

# Skill Writing

Skills are instructions loaded into a crowded context. Every line competes for
attention with the user's task. Write what the model would NOT do on its own;
cut the rest.

Format and logistics (frontmatter, directories, naming rules) are covered by
Zed's built-in `create-skill`. This skill governs content quality.

## The Standard

- **Short body, explicit boundaries.** The model already knows the domain
  (what slop is, how to review code, how to write a plan). Your job is scope,
  procedure, and limits — not tutorials or taxonomies.
- **Description is the trigger.** It decides whether the skill loads. Make it
  specific: what it does + when to use. No marketing. Never reference other
  skills in the description — it pollutes the activation decision and breaks
  on renames. Cross-references between skills belong in the body, and only
  when territories genuinely overlap.
- **Procedure in 3-5 steps.** Scope → act → report. If it needs more, the skill
  is doing two jobs; split it.
- **Hard Rules section for limits, near the top.** What to never touch, what
  to do when in doubt, safety rails. This is where detail earns its tokens —
  and where attention is highest. Place Hard Rules right after the one-line
  purpose, before the procedure.
- **No restating the obvious.** If a competent agent would do it unprompted,
  delete the line.

## Auditing an Existing Skill

1. Read the SKILL.md. For each line, ask: "would the model do this anyway?"
   If yes, cut.
2. Check the description: does it say what + when, concisely?
3. Check that limits/edge cases live in a Hard Rules section near the top
   (right after the purpose, before the procedure), not scattered.
4. Verify examples/templates earn their place — move long ones to reference
   files and point at them.
5. Report what was cut and why, grouped by section.

## Creating a New Skill

1. Name: lowercase-hyphenated, matches the directory.
2. Description: one or two sentences, what + when.
3. Body: one-line purpose, Hard Rules, then Procedure (3-5 steps).
4. Supporting files only when the content is too long to inline — reference
   them by relative path.
5. Target ~20-40 lines for the SKILL.md body. Longer needs justification.
