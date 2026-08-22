---
name: js-supply-chain-safety
description: >-
  JS package install safety for npm/pnpm/yarn/bun. Use ALWAYS when adding,
  updating, or installing JS packages; editing package.json dependencies; or
  running npm/pnpm/bun/yarn install/update. Covers package manager detection,
  minimum-release-age enforcement, forbidden package.json patterns, and known
  npm worm IOCs (e.g. Mini Shai-Hulud).
---

# JS Supply Chain Safety

Apply this specialization together with `supply-chain-safety`. When their rules differ, the stricter rule wins.

## Hard Rules

- Package manager: use what the repo declares — `packageManager` field in
  `package.json`, else existing lockfile (`pnpm-lock.yaml`,
  `package-lock.json`, `yarn.lock`, `bun.lock`), else default to `pnpm`.
- When defaulting to pnpm in a repo with no PM signal, suggest recording the
  choice (`"packageManager": "pnpm@x.y.z"`).
- CI installs must be lockfile-frozen: `sfw pnpm install --frozen-lockfile`,
  `sfw npm ci`, `sfw bun install --frozen-lockfile`.
- Never add to package.json: `github:user/repo#commit-hash` URLs in
  dependencies, or `prepare`/`postinstall` scripts running obfuscated `.js`
  files.
- Red flags that abort an install: artifact 3x+ larger than the previous
  version; `optionalDependencies` with git URLs; obfuscated install scripts.
- Provenance is not authorization: packages with valid SLSA/OIDC trusted
  publishing can still be malicious (ChainDrop, Aug 2026). Do not treat
  provenance as a safety signal.

## Minimum publish age

Verify the project has a native minimum-release-age config (72h); if missing,
add it — see `references/release-age-configs.md` for per-PM syntax. Fallback
for PMs without support or one-off checks:

```bash
~/.agents/skills/js-supply-chain-safety/scripts/check-pkg-age.sh <pkg> <version>
```

| Age | Risk | Action |
|-----|------|--------|
| < 24h | HIGH | Block — do not install |
| < 7 days | MEDIUM | Warn user, verify with `sfw` first |
| >= 7 days | LOW | Proceed normally |

## Inspecting an npm artifact

```bash
npm view <pkg>@<ver> dist.unpackedSize dist.integrity time
```

## Worm IOCs

When compromise is suspected, check the worm-family artifacts and response
playbook in `references/worm-iocs.md`.
