---
name: trunk-safety
description: >-
  Safe Trunk (trunk.io) setup and upgrade workflows with version pinning, sha256
  locking, and supply-chain attack protection. Use when the user asks to set up
  Trunk, run trunk init, upgrade trunk tools, enable/disable linters, or mentions
  trunk.yaml, trunk check, trunk fmt, or linter security.
---

# Trunk Safety

Hardened install/upgrade workflows for Trunk tools, preventing supply-chain
attacks like the Trivy compromise (March 2026).

## Hard Rules

- **Always** init with `--lock` so sha256 hashes for the CLI binary land in `trunk.yaml`; keep them there.
- **Always** pin every linter/runtime version with a trailing `!` to block silent upgrades; re-pin after any upgrade or tool change.
- **Never** run `trunk upgrade` without `--dry-run` first and explicit user confirmation.
- **Never** remove `!` pins without explicit user request.
- **Never** enable tools blindly — check `references/compromised-versions.md` first.
- **Never** put path/rule ignores in `trunk.yaml`'s `lint.ignore` — it is typically gitignored (single-player mode), so ignores won't be shared. Use each tool's own committed config file (see Linter Ignore Configuration).
- Only enable tools the project actually needs.

## Workflow 1: Fresh Setup

1. Initialize:
   ```bash
   trunk init --single-player-mode --force --lock -n
   ```
   - `--single-player-mode` — config is gitignored: personal, not shared
   - `--force` — overwrites existing `trunk.yaml`; required because `--lock` only writes the sha256 block during a fresh init (`--allow-existing` skips it). Lost custom config is visible in `git diff` and easy to restore.
   - `--lock` — sha256 hashes for the CLI binary per platform
   - `-n` — no to all prompts: minimal install
2. If the repo already had a `trunk.yaml`, review `git diff .trunk/trunk.yaml` and restore lost custom config (ignore paths, disabled linters).
3. Enable recommended actions:
   ```bash
   trunk actions enable trunk-check-pre-push trunk-check-pre-commit trunk-fmt-pre-commit
   ```

For a repo that already has Trunk configured, verify the same three hooks
are enabled (`trunk actions list`) and enable any that are missing.
4. Pin all versions — finds every `@version` entry in `.trunk/trunk.yaml`, appends `!` (skipping already-pinned), shows a before/after diff:
   ```bash
   bash <skill-dir>/scripts/trunk-pin-versions.sh
   ```
5. Verify: `trunk check --sample 5`
6. Check `references/compromised-versions.md`; if any enabled tool has a known incident, warn the user and suggest `trunk check disable <tool>`.

## Workflow 2: Safe Upgrade

1. Dry-run and show the user which tools have version changes:
   ```bash
   trunk upgrade --dry-run 2>&1
   ```
2. Cross-reference each tool being upgraded with `references/compromised-versions.md`; flag any with a history of compromise.
3. Present old -> new versions plus flagged tools; get explicit confirmation.
4. Apply: `trunk upgrade`
5. If the CLI version changed, re-lock — `trunk upgrade` does not regenerate sha256 hashes:
   ```bash
   trunk init --force --lock -n
   ```
   Then review `git diff .trunk/trunk.yaml` to restore overwritten custom config. If only linters/runtimes changed, skip — the existing sha256 block remains valid.
6. Re-pin: `bash <skill-dir>/scripts/trunk-pin-versions.sh`
7. Smoke test: `trunk check --sample 5`

## Workflow 3: Enable New Tool

1. Check `references/compromised-versions.md` for the tool BEFORE enabling it.
2. `trunk check enable <tool>`
3. Immediately pin its version with `!` in `.trunk/trunk.yaml`
4. Verify: `trunk check --sample 2`

A compromised tool must never be enabled, even briefly.

## Workflow 4: Agent-safe Git Hooks

Use when `git commit` appears to hang while Trunk hooks run, especially from an AI agent or pseudo-terminal.

Root causes:

1. **Hook stdin waiting for EOF** (most common). Trunk-generated hooks save stdin with `cat` into a tempfile before redirecting stdin to `/dev/tty` or `/dev/null`. In agent-run commands stdin can stay open, so `cat` waits indefinitely.
2. **Stopped or crashed daemon** (fallback case, not the default assumption). Symptoms: `GRPC Failed`, `Socket closed`, `Connection refused`, `Daemon stopped`.

Default behavior: leave the daemon alone and run the final commit with stdin explicitly closed by appending `</dev/null`. For multi-line messages, write to a temp file and use `git commit -F <message-file> </dev/null`.

Optional preflight (without stopping the daemon):

- `trunk check --ci --upstream HEAD --no-progress`
- `trunk fmt --ci --upstream HEAD --no-progress`

Fallback recovery — only when the commit still hangs with `</dev/null`, output shows daemon/GRPC errors, or `trunk daemon status` confirms unhealthy:

1. Stop the stuck command.
2. `trunk daemon shutdown`
3. `trunk check --ci --upstream HEAD --no-progress --print-failures`
4. Inspect `~/.cache/trunk/repos/*/logs/cli.log` and `daemon.log` for `Socket closed`, `Connection refused`, `Daemon stopped`, or the linter that was running last.
5. Retry the commit with `</dev/null`.

Optional mitigation: if one linter repeatedly crashes the daemon in a personal repo, prefer a repo-specific ignore/disable over repeated daemon stops. Broad IaC/security linters such as `checkov` may be too noisy for personal dotfiles unless scoped carefully.

## Workflow 5: Check Advisories

```bash
bash <skill-dir>/scripts/check-advisories.sh
```

Queries OSV.dev and (if `gh` is available) the GitHub Advisory Database for each tool in its registry; filters out IDs already documented in `compromised-versions.md`; flags supply-chain / malware findings. `--update` bumps the "Last updated" date in `compromised-versions.md`.

Automation:

- **GitHub Actions (recommended):** add `.github/workflows/trunk-advisory-check.yml` — runs weekly, creates/updates a GitHub issue on critical or supply-chain advisories, manual trigger via `workflow_dispatch`.
- **Cron:** `0 9 * * 1  bash <skill-dir>/scripts/check-advisories.sh --update >> ~/trunk-advisory-check.log 2>&1`

Add tools via the `TOOLS` array in `scripts/check-advisories.sh`. Format: `name|osv_ecosystem|osv_package|gh_advisory_ecosystem`

## Linter Ignore Configuration

Configure ignores in each tool's own standard config file, committed at the repo root:

| Linter | Config file | Ignore mechanism |
|--------|-------------|-----------------|
| checkov | `.checkov.yaml` | `skip-path: [...]` |
| prettier | `.prettierignore` | gitignore-style glob patterns |
| markdownlint | `.markdownlint.json` | `"ignores": ["glob/**"]` and rule toggles (e.g. `"MD013": false`) |
| yamllint | `.yamllint.yaml` | `ignore: |` block with path patterns |
| golangci-lint | `.golangci.yml` | `issues.exclude-rules[].path` |
| shellcheck | `.shellcheckrc` | `disable=SC2312` or `external-sources=true` |

For **actionlint** on Go template files (`.yaml.tpl`) there is no path exclusion in its config file. Options, in preference order:

1. Add `# trunk-ignore-all(actionlint)` at the top of each template file
2. Keep the ignore in `trunk.yaml` as a last resort, with a comment explaining it can't be shared

## Resources

- Known compromised versions: [references/compromised-versions.md](references/compromised-versions.md)
- Pinning script: [scripts/trunk-pin-versions.sh](scripts/trunk-pin-versions.sh)
- Advisory checker: [scripts/check-advisories.sh](scripts/check-advisories.sh)
