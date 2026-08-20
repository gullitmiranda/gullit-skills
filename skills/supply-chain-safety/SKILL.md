---
name: supply-chain-safety
description: >-
  Universal supply-chain protection when installing packages or global CLI
  tools in ANY ecosystem (npm, pip, cargo, go, gem). Use ALWAYS when installing
  or updating packages, or installing global CLI tools. Enforces sfw (Socket
  Firewall) wrapping, mise for global installs, minimum-release-age, and
  pre-install inspection.
---

# Supply Chain Safety

Universal rules for installing packages in any ecosystem.

## Hard Rules

- Always prefix install/update commands with `sfw` (Socket Firewall), in every
  context: `sfw <pm> install`. If `sfw` is unavailable, stop and ask the user
  to install it — never bypass to keep moving.
- Global CLI tools: prefer `mise use -g <backend>:<pkg>` (npm:, pipx:, cargo:,
  go:, gem:). If mise fails (e.g. resolver bugs), fall back to
  `sfw <pm> install -g <pkg>` AND keep the tool as a commented line in
  `~/.config/mise/config.toml` explaining why — the config stays the central
  inventory either way.
- Pin exact versions for direct dependencies. No floating ranges (`^`, `~`,
  `>=`) in any manifest.
- Abort and report when: the artifact is anomalously large vs. the previous
  version, an install/build hook runs obfuscated code, or dependencies point
  outside the official registry (git URLs, direct tarballs).

## Minimum release age

Enforce a minimum publish age via the ecosystem's native mechanism when one
exists; where none exists, rely on sfw plus manual inspection.

| Context | Age |
|---|---|
| Development machine | 24h |
| CI | 72h |
| Production deploys | 7 days |

## Pre-install inspection

Before installing any new or updated package, check: release date, artifact
size vs. previous version, install/build scripts it will run, and whether all
dependencies come from the official registry.
