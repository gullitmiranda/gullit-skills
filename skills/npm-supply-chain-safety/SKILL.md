---
name: npm-supply-chain-safety
description: >-
  Safe npm dependency management to prevent supply chain attacks (e.g.
  Mini Shai-Hulud / TeamPCP worm). Use ALWAYS when adding, updating, or
  installing npm packages; editing package.json dependencies; or running
  npm install/update. Enforces socket CLI usage, minimum-release-age
  checks, and detects known IOC patterns.
---

# npm Supply Chain Safety

## Mandatory rules

### 1. Never run `npm install` directly

Always prefer `socket npm install` — it performs static analysis before any package touches disk:

```bash
socket npm install              # drop-in replacement
socket npm install <pkg>@<ver>  # adding/updating a dep
```

`npm ci` is the only safe exception (uses lockfile exactly, no network resolution).

If `socket` is not installed, stop and ask the user to install it first. Do not
bypass the Socket check just to keep moving.
```bash
npm install -g @socketregistry/socket
```

### 2. Check publish age before installing (minimum-release-age guard)

Before updating to any new version, run:
```bash
~/.agents/skills/npm-supply-chain-safety/scripts/check-pkg-age.sh <pkg> <version>
```

Risk thresholds:
| Age | Risk | Action |
|-----|------|--------|
| < 24h | HIGH | Block — do not install |
| < 7 days | MEDIUM | Warn user, verify with `socket` first |
| >= 7 days | LOW | Proceed normally |

### 3. Inspect before installing any new or updated package

```bash
npm view <pkg>@<ver> dist.unpackedSize dist.integrity time
```

Red flags that warrant aborting:
- Package is 3x+ larger than the previous version (e.g. 190 KB → 900 KB)
- `optionalDependencies` contains a `github:user/repo#commit-hash` URL
- `prepare` or `postinstall` script runs an obfuscated `.js` file via Bun

### 4. Pin exact versions in package.json

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

For full list see: https://www.stepsecurity.io/blog/mini-shai-hulud-is-back-a-self-spreading-supply-chain-attack-hits-the-npm-ecosystem

Key packages to watch (versions that were compromised):
- `@tanstack/react-router`: 1.169.5, 1.169.8
- `@tanstack/router-core`: 1.169.5, 1.169.8
- `@tanstack/router-plugin`: 1.167.38, 1.167.41
- `@tanstack/router-vite-plugin`: 1.166.53, 1.166.56
- `@mistralai/mistralai`: 2.2.3, 2.2.4
- `@opensearch-project/opensearch`: 3.6.2
- `safe-action`: 0.8.3, 0.8.4

Use the StepSecurity advisory above as the source of truth for the full list.

## Minimum-release-age guard — native package manager config

All major package managers now support this natively. **When working on a project, verify it has this configured. If not, add it.**

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

For manual checks or projects on npm 10, use the bundled script:
```bash
~/.agents/skills/npm-supply-chain-safety/scripts/check-pkg-age.sh <pkg> <version>
```
