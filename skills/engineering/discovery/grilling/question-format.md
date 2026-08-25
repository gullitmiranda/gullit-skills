# Grill question card

Each question is its own heading. Keep title, body, options, and suggestion on separate lines.

```markdown
### N. Short title

One or two sentences: what must be decided and why it is unlocked now.

- **A.** First option — short meaning
- **B.** Second option — short meaning

**Suggestion: A.** One sentence why this option wins.
```

## Rules

- Number questions in the round (`1`, `2`, `3`). The title is a short noun phrase, not a paragraph.
- Body is at most two sentences. Do not repeat the title.
- Options are a list. Bold the reply token first (`**A.**`, `**B.**`, or a short name).
- The suggestion is a separate final line. Start with `**Suggestion: <token>.**` then one sentence of why. Never hide it in the body. Never use an unlabeled arrow.
- Separate questions in the same round with `---`.
- Close the round with one line: the user can reply with tokens (`1A 2B`) or override any suggestion.
- Do not use emoji as structure.
