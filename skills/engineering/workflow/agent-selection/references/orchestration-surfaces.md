# Orchestration Surfaces

A **surface** is where the cast lives (orchestrator), not a model and not a
protocol. Choose the surface before picking models. ACP is never a surface by
itself — name `ACP:<agent>` (for example `ACP:claude-code`).

Skill **content** may be shared across agents via symlinks. Do not assume
identical **wiring**: ACP external agents do not inherit Zed profiles/skills;
Cursor rules and Zed settings remain agent-exclusive.

## Capability matrix

| Capability | Cursor Local | Cursor Cloud | Zed Agent | `ACP:<agent>` | `Terminal:<cli>` |
| --- | --- | --- | --- | --- | --- |
| Fine cast (per-role model, Task/spawn) | Strong | Strong | Weak (manual threads) | Owned by the named agent | CLI-dependent |
| Parallel / background | Strong | Strong | Thread parallel yes | Thread parallel yes | Yes, outside IDE |
| Custom / CW gateway providers | No in current setup | No in current setup | Yes | Only if that agent talks to the gateway | Yes if CLI points at gateway |
| OpenRouter / multi-provider | Cursor catalog only | Cursor catalog only | Yes | Agent-dependent | Yes |
| Slack / Grok Bot / CW×xAI paths | Yes | Yes | Not the center | No | No |

"CW gateway / No in current setup" on Cursor means **eligibility today**: the
CloudWalk `llm-gateway` is not reachable as a Cursor agent provider without
their server path. Revisit if BYOK/OpenAI-compatible Cursor routing appears.

## Decision rules (provisional)

1. Need a fine cast (multi-role, clean review, background) → **Cursor** as
   orchestrator.
2. CW gateway or OpenRouter model is non-negotiable → **Zed Agent** (or
   Terminal); accept manual cast + capsules.
3. ACP on Zed → pick a **named** agent; orchestration stays human/weak unless
   that agent exposes its own cast tools.
4. Slack / Grok / CW×xAI agent paths → **Cursor** (local or cloud).
5. Never promote a Cursor model default as a Zed/gateway default without a
   pilot on that surface.

## Related

- Cast format: [orchestration-cast.md](orchestration-cast.md)
- Durable model config / pilots: `model-selection` (surface is precondition)
