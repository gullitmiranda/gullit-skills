---
name: trunk-safety
description: >-
  Safe Trunk (trunk.io) setup and upgrade workflows with version pinning, sha256
  locking, supply-chain attack protection, and agent-safe git hooks (PTY/TTY
  hang avoidance). Use when the user asks to set up Trunk, run trunk init,
  upgrade trunk tools, enable/disable linters, mentions trunk.yaml / trunk check
  / trunk fmt, linter security, or when git commit hangs on Trunk hooks in an
  AI agent or pseudo-terminal.
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
- **Never** leave generated tool configs under `.trunk/configs/`. Move or merge them into each tool's standard committed config path so contributors can use the tools without Trunk; preserve existing project config.
- Keep `.trunk/` personal and untracked in single-player setups; never run `trunk config share` or commit Trunk configuration unless explicitly requested.
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
2. Promote every generated config from `.trunk/configs/` to the tool's standard repository path. If that path already exists, merge the generated settings without overwriting project rules. Confirm `git status` shows native tool configs but not `.trunk/`.
3. If the repo already had a `trunk.yaml`, review `git diff .trunk/trunk.yaml` and restore lost custom config (ignore paths, disabled linters).
4. Enable recommended actions:
   ```bash
   trunk actions enable trunk-check-pre-push trunk-check-pre-commit
   ```
   Prefer **check** hooks only. Do **not** enable `trunk-fmt-pre-commit` by
   default in agent-heavy workflows: that hook opens `/dev/tty` when stderr is
   a TTY and hangs AI agents on interactive Prettier/format prompts. Agents
   must run `CI=1 trunk fmt --ci -y` before commit instead (see `git` skill).
   Enable `trunk-fmt-pre-commit` only if the user explicitly wants interactive
   human-local formatting on commit.

For a repo that already has Trunk configured, verify check hooks are enabled
(`trunk actions list`). If `trunk-fmt-pre-commit` is enabled and agents hang on
commit, disable it: `trunk actions disable trunk-fmt-pre-commit`.
5. Pin all versions — finds every `@version` entry in `.trunk/trunk.yaml`, appends `!` (skipping already-pinned), shows a before/after diff:
   ```bash
   bash <skill-dir>/scripts/trunk-pin-versions.sh
   ```
6. Verify: `trunk check --sample 5`
7. Check `references/compromised-versions.md`; if any enabled tool has a known incident, warn the user and suggest `trunk check disable <tool>`.

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

Use when `git commit` appears to hang while Trunk hooks run, especially from an AI agent or pseudo-terminal. Full commit sequence lives in the `git` skill; this workflow is diagnosis + recovery.

Root causes (in order of likelihood for agent hangs):

1. **Interactive TTY prompts**. Trunk's hook does `exec </dev/tty` when stderr is a TTY. Agent runners often allocate a PTY, so Prettier "autoformat?" / "Continue anyway?" wait forever. Closing stdin alone does **not** fix this.
2. **Hook stdin waiting for EOF**. Trunk-generated hooks save stdin with `cat` into a tempfile. If stdin stays open, `cat` waits indefinitely.
3. **Stopped or crashed daemon**. Symptoms: `GRPC Failed`, `Socket closed`, `Connection refused`, `Daemon stopped`.

### Prevention (every agent commit)

```bash
CI=1 trunk fmt --ci -y --upstream HEAD --no-progress </dev/null
CI=1 trunk check --ci -y --upstream HEAD --no-progress </dev/null
# stage any reformatted files, then:
CI=1 GIT_TERMINAL_PROMPT=0 git commit ... </dev/null   # with harness timeout; prefer non-PTY
```

If the repo enables `trunk-fmt-pre-commit` and agents keep hanging, disable that action and keep fmt as an explicit preflight (see Workflow 1).

### Recovery when a commit is already hung

1. Stop the stuck command (do not wait minutes).
2. If logs show daemon/GRPC errors or `trunk daemon status` is unhealthy: `trunk daemon shutdown`, then `CI=1 trunk check --ci --upstream HEAD --no-progress --print-failures`.
3. Inspect `~/.cache/trunk/repos/*/logs/cli.log` and `daemon.log`.
4. Retry with the prevention sequence above. Last resort after a clean preflight: `git commit --no-verify` (declare it explicitly).

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
