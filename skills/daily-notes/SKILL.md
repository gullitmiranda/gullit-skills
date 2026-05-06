---
name: daily-notes
description: Create or improve personal daily work notes in Portuguese. Use when the user says `/daily [date]`, "daily note", "nota do dia", "resumo do dia", "SessionApp", or asks to turn daily activity into a concise Markdown note.
---

# Daily Notes

## Goal

Create a concise Markdown daily note for SessionApp, focused on what was actually done and what remains pending.

Default destination:

`/Users/guma/Library/CloudStorage/GoogleDrive-gullitmiranda@gmail.com/My Drive/Documents/Daily Notes`

Default filename:

`daily-note-YYYY-MM-DD.md`

## Date handling

- `/daily` means today in the user's local timezone.
- `/daily YYYY-MM-DD` uses that date.
- `/daily ontem` uses the previous calendar day.
- If the user is editing an existing daily note, update that file instead of creating a new one.

## Workflow

1. Gather activity evidence from GitHub, local commits, existing notes, and current conversation context.
2. Use Slack only when authentication is already available or the user explicitly wants Slack included.
3. If the note file already exists, read it first and preserve user edits.
4. Write or update the Markdown file in the Daily Notes directory.
5. Keep the final response short and mention the file path.

## Structure

Use this structure unless the user asks otherwise:

```markdown
# Resumo do Dia - YYYY-MM-DD

## Resumo Executivo

[1-2 short paragraphs explaining the real focus of the day.]

## Principais Atividades

- [Clear, short bullet.]
- [Clear, short bullet.]

## Números

- [Only include metrics with evidence.]

## Highlights

### [Theme]

- [Specific action with outcome/link when useful.]

## Pendências

- [Pending item with context and timing.]

## Tema do Dia

- [Theme phrase.]
- [Theme phrase.]
```

## Writing style

- Write in Portuguese (BR).
- Prefer first person past tense: "Corrigi", "Avancei", "Investiguei", "Aumentei".
- Keep bullets short, but not vague.
- Explain impact or scope: prefer "Aumentei a capacidade do node pool de GPU T4 em `prd-1`" over "Mergeei capacidade GPU T4".
- Group related work into one coherent front when it belongs to the same initiative.
- Avoid turning the note into a changelog. Use links for important PRs, but keep the prose readable.
- If pending work is risky after hours, note that it will be handled in business hours.
- Preserve a good existing structure instead of rewriting the whole document unnecessarily.

## Quality checks

- No invisible/gremlin characters.
- No unsupported claims. If a source was unavailable, either omit it or state the limitation briefly.
- Do not invent PR status; verify when status matters.
