---
name: js-supply-chain-safety
description: >-
  JS-specific supply-chain rules on top of supply-chain-safety. Use ALWAYS
  when adding, updating, or installing JS packages; editing package.json
  dependencies; or running npm/pnpm/bun/yarn install/update. Covers package
  manager detection, native minimum-release-age configs, forbidden
  package.json patterns, and known npm worm IOCs (e.g. Mini Shai-Hulud).
---

# JS Supply Chain Safety

Extends `supply-chain-safety` (sfw wrapping, mise globals, release-age
principle, pre-install inspection, version pinning). This skill adds the
JS-specific mechanics.

## Mandatory rules

### 1. Choose the package manager the repo already uses

Detection order:
1. `packageManager` field in `package.json`
2. Existing lockfile (`pnpm-lock.yaml`, `package-lock.json`, `yarn.lock`, `bun.lock`)
3. Default: `pnpm`

```bash
sfw pnpm install              # drop-in replacement
sfw pnpm add <pkg>@<ver>      # adding/updating a dep
sfw npm install               # when npm is the repo's PM
sfw bun install               # when bun is the repo's PM
```

When picking pnpm for a repo with no PM signal, suggest recording the choice
(`"packageManager": "pnpm@x.y.z"`) so CI and teammates resolve the same PM.

Local, non-resolving commands run directly: `pnpm run build`, `pnpm test`,
`pnpm exec ...`.

### 2. Lockfile-frozen installs are the preferred CI mode

- `pnpm install --frozen-lockfile`
- `npm ci`
- `bun install --frozen-lockfile`

Lockfile-exact, no version resolution. Still wrap with sfw when outside
guma's machine, since fetches happen through the firewall.

### 3. Enforce minimum publish age (native config first)

The project's package manager config is the primary mechanism — verify it is
configured (see "Minimum-release-age guard — native package manager config"
below); if missing, add it. The native gate blocks too-new packages at install
time with no manual step.

Use the script only as a fallback: projects on package managers without support
(e.g. npm 10), or a one-off manual check outside the install flow:
```bash
~/.agents/skills/js-supply-chain-safety/scripts/check-pkg-age.sh <pkg> <version>
```

Risk thresholds:
| Age | Risk | Action |
|-----|------|--------|
| < 24h | HIGH | Block — do not install |
| < 7 days | MEDIUM | Warn user, verify with `sfw` first |
| >= 7 days | LOW | Proceed normally |

### 4. Inspect npm artifacts before installing

```bash
npm view <pkg>@<ver> dist.unpackedSize dist.integrity time
```

Red flags that warrant aborting:
- Package is 3x+ larger than the previous version (e.g. 190 KB → 900 KB)
- `optionalDependencies` contains a `github:user/repo#commit-hash` URL
- `prepare` or `postinstall` script runs an obfuscated `.js` file via Bun

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

Thresholds per context are defined in `supply-chain-safety` (24h dev / 72h CI
/ 7d production).
