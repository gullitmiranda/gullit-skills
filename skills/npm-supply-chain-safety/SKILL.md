---
name: npm-supply-chain-safety
description: >-
  Safe JS dependency management to prevent supply chain attacks (e.g.
  Mini Shai-Hulud / TeamPCP worm). Use ALWAYS when adding, updating, or
  installing JS packages; editing package.json dependencies; running
  npm/pnpm/bun/yarn install/update; or installing global CLI tools.
  Enforces sfw (Socket Firewall) wrapping, mise for global installs,
  minimum-release-age checks, and detects known IOC patterns.
---

# JS Supply Chain Safety

## Mandatory rules

### 1. Global CLI tools: install via mise, never `npm install -g`

Global npm installs run postinstall scripts with your global tokens and leave no
versioned trace. Install global CLIs via mise instead — versioned, reproducible,
and tracked in `~/.config/mise/config.toml`:
```bash
mise use -g npm:<pkg>   # e.g. mise use -g npm:sfw
```

Only exception: a tool that cannot install through mise (e.g. aube peer-dep
resolution bugs) — then use `sfw npm install -g <pkg>` and leave a comment in
the mise config explaining why.

### 2. Project installs: `sfw <pm>`, defaulting to pnpm

Never run bare `npm install` / `pnpm add` / `yarn add` — wrap with `sfw`
(Socket Firewall), which filters package downloads at the network layer before
any package touches disk (no API key needed):

```bash
sfw pnpm install              # drop-in replacement
sfw pnpm add <pkg>@<ver>      # adding/updating a dep
sfw npm install               # when npm is the repo's PM
sfw bun install               # when bun is the repo's PM
```

On guma's machine, `npm`/`pnpm` resolve to sfw wrappers from the dotfiles repo
(`tools/mise/bin/`, symlinked into `~/.local/bin`) — bare `pnpm install` is safe
there, and explicit `sfw pnpm install` does not double-wrap (the wrappers guard
via `SFW_ACTIVE`). Explicit `sfw` matters in contexts without the wrappers: CI,
containers, other machines.

Choose the package manager in this order:
1. `packageManager` field in `package.json`
2. Existing lockfile (`pnpm-lock.yaml`, `package-lock.json`, `yarn.lock`, `bun.lock`)
3. Default: `pnpm`

When picking pnpm for a repo with no PM signal, suggest recording the choice
(`"packageManager": "pnpm@x.y.z"`) so CI and teammates resolve the same PM.

Local, non-resolving commands run directly: `pnpm run build`, `pnpm test`,
`pnpm exec ...`.

`npm ci` / `pnpm install --frozen-lockfile` / `bun install --frozen-lockfile`
are the preferred CI mode (lockfile-exact, no version resolution) — still wrap
with sfw when outside guma's machine, since fetches happen through the firewall.

If `sfw` is not installed, stop and ask the user to install it first. Do not
bypass the check just to keep moving.
```bash
mise use -g npm:sfw   # guma's machine
```

### 3. Enforce minimum publish age (native config first)

The project's package manager config is the primary mechanism — verify it is
configured (see "Minimum-release-age guard — native package manager config"
below); if missing, add it. The native gate blocks too-new packages at install
time with no manual step.

Use the script only as a fallback: projects on package managers without support
(e.g. npm 10), or a one-off manual check outside the install flow:
```bash
~/.agents/skills/npm-supply-chain-safety/scripts/check-pkg-age.sh <pkg> <version>
```

Risk thresholds:
| Age | Risk | Action |
|-----|------|--------|
| < 24h | HIGH | Block — do not install |
| < 7 days | MEDIUM | Warn user, verify with `sfw` first |
| >= 7 days | LOW | Proceed normally |

### 4. Inspect before installing any new or updated package

```bash
npm view <pkg>@<ver> dist.unpackedSize dist.integrity time
```

Red flags that warrant aborting:
- Package is 3x+ larger than the previous version (e.g. 190 KB → 900 KB)
- `optionalDependencies` contains a `github:user/repo#commit-hash` URL
- `prepare` or `postinstall` script runs an obfuscated `.js` file via Bun

### 5. Pin exact versions in package.json

No `^` or `~` for direct dependencies:
```json
{ "dependencies": { "@tanstack/react-router": "1.169.1" } }
```

## Forbidden patterns in package.json

Never add or accept these:
```json
"optionalDependencies": {
  "any-pkg": "github:user/repo#commit-hash"
}
```
```json
"scripts": { "prepare": "bun run some-obfuscated-file.js" }
```

## IOC: check for compromise artifacts

These files/services indicate the Mini Shai-Hulud worm has executed locally.
If any are found, stop work and report immediately:

```
~/.claude/router_runtime.js
~/.claude/setup.mjs
~/.vscode/setup.mjs
~/Library/LaunchAgents/com.user.gh-token-monitor.plist   # macOS
~/.config/systemd/user/gh-token-monitor.service           # Linux
```

Also check:
```bash
npm token list   # look for: "IfYouRevokeThisTokenItWillWipeTheComputerOfTheOwner"
```

## Compromised package versions (Mini Shai-Hulud, 2026-05-11)

Source of truth (full list): https://www.stepsecurity.io/blog/mini-shai-hulud-is-back-a-self-spreading-supply-chain-attack-hits-the-npm-ecosystem

Key compromised versions:
- `@tanstack/react-router`: 1.169.5, 1.169.8
- `@tanstack/router-core`: 1.169.5, 1.169.8
- `@tanstack/router-plugin`: 1.167.38, 1.167.41
- `@tanstack/router-vite-plugin`: 1.166.53, 1.166.56
- `@mistralai/mistralai`: 2.2.3, 2.2.4
- `@opensearch-project/opensearch`: 3.6.2
- `safe-action`: 0.8.3, 0.8.4

## Minimum-release-age guard — native package manager config

**When working on a project, verify it has this configured. If not, add it.**

### pnpm ≥ 10.16 (`pnpm-workspace.yaml` or `.npmrc`)
```yaml
# pnpm-workspace.yaml
minimumReleaseAge: '72h'
blockExoticSubdeps: true   # blocks github: URLs as transitive deps (pnpm 11+)
```
pnpm 11 ships with `minimumReleaseAge: 1440` (24h) as default.

### npm ≥ 11 (`.npmrc`)
```
minimum-release-age=72h
allow-git=none
```
npm 10.x does not support this — recommend upgrading via Node.js 22+.

### Yarn ≥ 4.10 (`.yarnrc.yml`)
```yaml
npmMinimalAgeGate: "72h"
```

### Bun ≥ 1.3 (`bunfig.toml`)
```toml
[install]
minimumReleaseAge = "72h"
```

### Recommended thresholds
| Context | Age |
|---|---|
| Development machine | 24h |
| CI | 72h |
| Production deploys | 7 days |
