# grill-with-docs

A locally maintained skill for challenging plans against a project domain model,
resolving terminology, and recording durable decisions in the appropriate
documentation.

## Origin

This skill is derived from Matt Pocock’s
[`grill-with-docs`](https://github.com/mattpocock/skills/tree/e3b90b5238f38cdea5996e16861dcae28ef52eda/skills/engineering/grill-with-docs)
at upstream commit `e3b90b5238f38cdea5996e16861dcae28ef52eda`.

The local version preserves the upstream intent and adds the project-specific
working-document model: use specs for evolving behavior, requirements, and
implementation decisions; reserve ADRs for durable architectural trade-offs.

## Dependencies

This skill is self-contained. It does not require any other skill from
`mattpocock/skills` to be installed.

`SKILL.md` references these local supporting files:

- [`CONTEXT-FORMAT.md`](CONTEXT-FORMAT.md) for glossary structure.
- [`ADR-FORMAT.md`](ADR-FORMAT.md) for architectural decision records.

Keep those files alongside `SKILL.md` if the skill is moved or copied.

## Upstream relationship

This copy is maintained independently and is not automatically synchronized
with the upstream skill. Review upstream changes deliberately before adopting
them here.

## License and attribution

The upstream source is licensed under the MIT License, copyright (c) 2026 Matt
Pocock. Its required copyright and permission notice is preserved in
[`UPSTREAM-LICENSE.md`](UPSTREAM-LICENSE.md).
