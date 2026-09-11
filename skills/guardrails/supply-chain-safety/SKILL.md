---
name: supply-chain-safety
description: >-
  Universal supply-chain protection when installing packages or global CLI
  tools in any ecosystem. Use always when installing or updating packages or
  global CLI tools. Requires Socket Firewall where the installed edition
  supports it, exact pinning, release-age checks, and pre-install inspection.
---

# Supply Chain Safety

Universal rules for installing packages in any ecosystem.

## Hard Rules

- Check the installed Socket Firewall edition's official ecosystem and package
  manager support before constructing an install or update command.
- For officially supported package managers, `sfw` is mandatory:
  `sfw <pm> install`. If `sfw` is unavailable, stop and ask the user to install
  it; do not bypass it.
- Do not require or attempt `sfw` for an unsupported ecosystem. Socket Firewall
  Free does not support Go, Java, Ruby, or .NET.
- For unsupported ecosystems, pin exact versions, complete the manual
  pre-install inspection below, then invoke the native package manager directly.
- For npm, pnpm, Yarn, and Bun, load and follow the dedicated
  `js-supply-chain-safety` skill; its stronger rules take precedence.
- For global CLI tools in supported ecosystems, prefer
  `mise use -g <backend>:<pkg>`. If mise fails, use the `sfw`-wrapped native
  package manager and retain the tool as a commented entry in
  `~/.config/mise/config.toml` explaining why. For unsupported ecosystems, use
  the inspected, exactly pinned native package manager command directly.
- Pin exact versions for direct dependencies. Do not use floating ranges such as
  `^`, `~`, or `>=`.
- Abort and report anomalous artifact growth, obfuscated install or build hooks,
  or packages and dependencies that do not resolve to an official registry or
  source.

## Minimum release age

Enforce minimum publish age through the ecosystem's native mechanism when one
exists. Otherwise, verify it manually; `sfw` may supplement this check only for
package managers supported by the installed edition.

| Context | Age |
|---|---|
| Development machine | 24h |
| CI | 72h |
| Production deploys | 7 days |

## Pre-install inspection

Before installing any new or updated package, verify its release date, artifact
size delta from the previous version, install and build hooks or scripts, and
official registry or source provenance.
