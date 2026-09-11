# Work Intake Result

## Source Context

- Provided artifacts:
- Current repository or workspace:
- Branch or worktree:
- Local changes:
- Relevant documentation, issues, or pull requests:

## Artifact Authority

- Source:
- Governing authority:
- Type: local plan | tracked note | legacy local input | non-plan
- Note lifecycle: proposed | current | retired | archived | n/a
- Execution readiness: ready | needs-refinement | blocked | unclear
- Next route: `work-plan` | `build-plan` | `incremental-delivery` | `work-closeout` | user decision

## Status

Inventory only: what exists and its state. **No** agents, models, write sets,
or execution order here — that belongs in Orchestration Sketch.

Use compact bullets (preferred when one delivery / mid-flight resume):

- `<name>` — `done` | `active` | `blocked` | `stale` | `needs-user-decision` — one-line evidence; open decision only if any

Use `###` subsections only when streams are truly independent deliveries that
need separate routes. Still omit cast details from this section.

Omit this section entirely when Source Context + Authority already state a
single obvious mid-flight resume and there is nothing to inventory.

## Execution Recommendation

One short paragraph (two max): execute here or not, autonomy mode, and what
"done" returns. Do not restate the cast or re-list workstream status.

## Orchestration Sketch

Required when Next route is `build-plan` or `incremental-delivery`. Omit only
for clarify / `work-plan` / `work-closeout` / pure user decision with no
execution cast.

This is the **execution** section: remaining critical path only. Do not repeat
Status inventory (no “I2a largely done” bullets here).

Use the **bullet** cast from `agent-selection`
([orchestration-cast.md](../agent-selection/references/orchestration-cast.md)).
Do not default to a wide table in chat.

- Mode / remaining scope / commit policy (one line)
- Critical-path roles as bullets: runtime · **concrete model** · fallback ·
  does / write set / capsule / order (`after` or `parallel`)
- Deferred (optional twin, etc.) — separate heading, or omit
- Review fixed point(s), spec/plan paths, when reviews fire

If solo sequential, give the exception reason in one line.

## Handoff Prompt

Include only when work moves to another runtime. Put the completed
`context-capsule` in one fenced `markdown` block so the user can copy it into
the receiving thread unchanged. Do not repeat the execution recommendation
inside the prompt.

## Risks And Blockers

- Risk or blocker.

## Immediate Next Step

The smallest action to take after the user confirms the recommendation.
