---
name: supply-chain-safety
description: >-
  Universal supply-chain protection when installing packages or global CLI
  tools in ANY ecosystem (npm, pip, cargo, go, gem). Use ALWAYS when installing
  or updating packages, or installing global CLI tools. Enforces sfw (Socket
  Firewall) wrapping, mise for global installs, minimum-release-age, and
  pre-install inspection. For JS-specific package manager rules, see
  js-supply-chain-safety.
---

# Supply Chain Safety (universal)

Principles that apply to any package ecosystem. Ecosystem-specific skills
(e.g. `js-supply-chain-safety`) extend this one — when both apply, follow both.

## Mandatory rules

### 1. Every package install goes through sfw

`sfw` (Socket Firewall) filters package downloads at the network layer before
anything touches disk — no API key needed, wraps any tool that fetches over
HTTP:

```bash
sfw <pm> install           # e.g. sfw pnpm install, sfw pip install -r reqs.txt
```

On guma's machine, common PMs already resolve to sfw wrappers from the dotfiles
repo (`tools/mise/bin/`, symlinked into `~/.local/bin`) — bare `pnpm install`
is safe there, and explicit `sfw <pm> install` does not double-wrap (guarded
via `SFW_ACTIVE`). Explicit `sfw` matters in contexts without the wrappers:
CI, containers, other machines.

If `sfw` is not available in the context, stop and ask the user to install it
first. Do not bypass the firewall just to keep moving.
```bash
mise use -g npm:sfw   # guma's machine
```

### 2. Global CLI tools: prefer mise, fallback is first-class

Prefer mise so globals are versioned and reproducible:
```bash
mise use -g <backend>:<pkg>   # npm:, pipx:, cargo:, go:, gem:
```

Fallback is a normal path, not a shameful exception: if mise fails (e.g. aube
resolver bugs on complex peer-dep graphs), install with
`sfw <pm> install -g <pkg>` AND keep the tool listed in
`~/.config/mise/config.toml` as a commented line explaining why it is
installed manually. The config stays the central inventory either way.

### 3. Minimum release age

Fresh releases are the highest-risk window for hijacked packages. Enforce a
minimum publish age using the ecosystem's native mechanism when one exists
(see ecosystem skills); where none exists, rely on sfw plus manual inspection.

| Context | Age |
|---|---|
| Development machine | 24h |
| CI | 72h |
| Production deploys | 7 days |

### 4. Inspect before installing any new or updated package

Whatever the ecosystem, check before install: the package's release date,
artifact size vs. the previous version, install/build scripts it will run,
and whether dependencies come from the official registry (not git URLs or
direct tarball links).

Abort and report when the artifact is anomalously large, an install hook runs
obfuscated code, or dependencies point outside the official registry.

### 5. Pin exact versions for direct dependencies

No floating ranges (`^`, `~`, `>=`) for direct dependencies in any manifest.

## Ecosystem-specific skills

- `js-supply-chain-safety` — npm/pnpm/yarn/bun: PM detection, native
  release-age configs, package.json forbidden patterns, npm worm IOCs.
