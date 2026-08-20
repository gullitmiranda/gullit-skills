# Minimum-release-age — native package manager configs

**When working on a project, verify it has this configured. If not, add it.**
The native gate blocks too-new packages at install time with no manual step.

Thresholds: 24h on dev machines, 72h in CI, 7 days for production deploys.

## pnpm ≥ 10.16 (`pnpm-workspace.yaml` or `.npmrc`)
```yaml
# pnpm-workspace.yaml
minimumReleaseAge: '72h'
blockExoticSubdeps: true   # blocks github: URLs as transitive deps (pnpm 11+)
```
pnpm 11 ships with `minimumReleaseAge: 1440` (24h) as default.

## npm ≥ 11 (`.npmrc`)
```
minimum-release-age=72h
allow-git=none
```
npm 10.x does not support this — recommend upgrading via Node.js 22+.

## Yarn ≥ 4.10 (`.yarnrc.yml`)
```yaml
npmMinimalAgeGate: "72h"
```

## Bun ≥ 1.3 (`bunfig.toml`)
```toml
[install]
minimumReleaseAge = "72h"
```
