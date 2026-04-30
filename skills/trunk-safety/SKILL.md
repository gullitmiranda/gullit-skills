---
name: trunk-safety
description: >-
  Safe Trunk (trunk.io) setup and upgrade workflows with version pinning, sha256
  locking, and supply-chain attack protection. Use when the user asks to set up
  Trunk, run trunk init, upgrade trunk tools, enable/disable linters, or mentions
  trunk.yaml, trunk check, trunk fmt, or linter security.
---

# Trunk Safety

Hardened workflows for installing and upgrading Trunk tools, preventing
supply-chain attacks like the Trivy compromise (March 2026).

## Principles

1. **Lock the CLI** -- always use `--lock` so sha256 hashes are in `trunk.yaml`
2. **Pin every version** -- append `!` to all linter/runtime versions to block silent upgrades
3. **Never blind-upgrade** -- always dry-run, review, then apply
4. **Minimal surface** -- only enable tools the project actually needs

## Workflow 1: Fresh Setup

Run when the user wants to set up Trunk in a repo (new or existing).

### Step 1: Initialize

```bash
trunk init --single-player-mode --force --lock -n
```

| Flag | Purpose |
|------|---------|
| `--single-player-mode` | Config is gitignored -- personal, not shared |
| `--force` | Overwrites existing `trunk.yaml` -- needed to generate sha256 block |
| `--lock` | Adds sha256 hashes for the CLI binary per platform |
| `-n` | Answers no to all prompts -- minimal install |

> **Why `--force` instead of `--allow-existing`?**
> `--lock` only writes the sha256 block during a fresh init. Using
> `--allow-existing` on a repo that already has `trunk.yaml` skips the sha256
> generation. Since the skill re-applies actions and pins in subsequent steps,
> and the trunk.yaml is version-controlled, any lost custom config (e.g. ignore
> paths) is visible in `git diff` and easy to restore.

### Step 2: Review changes

If the repo already had a `trunk.yaml`, review `git diff .trunk/trunk.yaml` to
check for lost custom config (ignore paths, disabled linters, etc.) and restore
what's needed before continuing.

### Step 3: Enable recommended actions

```bash
trunk actions enable trunk-check-pre-push trunk-check-pre-commit trunk-fmt-pre-commit
```

### Step 4: Pin all versions

Run the pinning script to append `!` to every versioned entry:

```bash
bash <skill-dir>/scripts/trunk-pin-versions.sh
```

Where `<skill-dir>` is the absolute path to this skill's directory. The script:
- Finds all `@version` entries in `.trunk/trunk.yaml`
- Appends `!` to each (skipping already-pinned ones)
- Shows a before/after diff

### Step 5: Verify

```bash
trunk check --sample 5
```

Run a small sample to confirm everything resolves correctly with pinned versions.

### Step 6: Disable known-risky tools

Check `references/compromised-versions.md` for tools with known supply-chain
incidents. If any are enabled, warn the user and suggest disabling:

```bash
trunk check disable <tool>
```

## Workflow 2: Safe Upgrade

Run when the user wants to upgrade Trunk tools.

### Step 1: Dry-run

```bash
trunk upgrade --dry-run 2>&1
```

Show the output to the user. Highlight which tools have version changes.

### Step 2: Check advisories

Cross-reference each tool being upgraded with `references/compromised-versions.md`.
If any tool has a history of compromise, flag it explicitly.

### Step 3: Confirm with user

Present a summary:
- Tools being upgraded (old version -> new version)
- Any flagged tools
- Ask for explicit confirmation before proceeding

### Step 4: Apply

```bash
trunk upgrade
```

### Step 5: Re-lock CLI (if CLI version changed)

`trunk upgrade` does not regenerate sha256 hashes. If the CLI version was
bumped, re-run init to refresh them:

```bash
trunk init --force --lock -n
```

Then review `git diff .trunk/trunk.yaml` to restore any custom config that was
overwritten (ignore paths, disabled linters, etc.). If only linters/runtimes
were upgraded (not the CLI), skip this step -- the existing sha256 block
remains valid.

### Step 6: Re-pin versions

Run the pinning script again after upgrade:

```bash
bash <skill-dir>/scripts/trunk-pin-versions.sh
```

### Step 7: Smoke test

```bash
trunk check --sample 5
```

## Workflow 3: Enable New Tool

When the user wants to add a linter or formatter:

1. Enable it: `trunk check enable <tool>`
2. Immediately pin its version with `!` in `.trunk/trunk.yaml`
3. Check `references/compromised-versions.md` for that tool
4. Run `trunk check --sample 2` to verify

## Workflow 4: Check Advisories

Periodically check for new vulnerabilities affecting enabled tools.

### Manual run

```bash
bash <skill-dir>/scripts/check-advisories.sh
```

The script queries OSV.dev and (if `gh` is available) the GitHub Advisory
Database for each tool in its registry. It filters out IDs already documented
in `compromised-versions.md` and flags supply-chain / malware findings.

Pass `--update` to bump the "Last updated" date in `compromised-versions.md`.

### Automating

**Option A — GitHub Actions** (recommended): add the
`.github/workflows/trunk-advisory-check.yml` workflow to your repo. Runs
weekly, creates/updates a GitHub issue when critical or supply-chain
advisories are found. Trigger manually via `workflow_dispatch`.

**Option B — Cron**: run weekly and log results locally:

```bash
# crontab -e
0 9 * * 1  bash <skill-dir>/scripts/check-advisories.sh --update >> ~/trunk-advisory-check.log 2>&1
```

### Adding tools to the registry

Edit the `TOOLS` array in `scripts/check-advisories.sh`. Format:

```
name|osv_ecosystem|osv_package|gh_advisory_ecosystem
```

## Linter Ignore Configuration

`.trunk/trunk.yaml` is typically gitignored (especially in `--single-player-mode`).
**Never** put path/rule ignores inside `trunk.yaml`'s `lint.ignore` section — they won't be shared via git.

Instead, always configure ignores in each tool's own standard config file, committed at the repo root:

| Linter | Config file | Ignore mechanism |
|--------|-------------|-----------------|
| checkov | `.checkov.yaml` | `skip-path: [...]` |
| prettier | `.prettierignore` | gitignore-style glob patterns |
| markdownlint | `.markdownlint.json` | `"ignores": ["glob/**"]` and rule toggles (e.g. `"MD013": false`) |
| yamllint | `.yamllint.yaml` | `ignore: |` block with path patterns |
| golangci-lint | `.golangci.yml` | `issues.exclude-rules[].path` |
| shellcheck | `.shellcheckrc` | `disable=SC2312` or `external-sources=true` |

For **actionlint** on Go template files (`.yaml.tpl`) there is no path exclusion in its
config file. Options (in preference order):
1. Add `# trunk-ignore-all(actionlint)` at the top of each template file
2. Keep the ignore in `trunk.yaml` as a last resort, with a comment explaining it can't be shared

## Safety Rules

- **Never** run `trunk upgrade` without `--dry-run` first
- **Never** remove `!` pins without explicit user request
- **Never** enable tools blindly -- always check the compromised versions list
- **Always** re-pin after any upgrade or tool change
- **Always** keep `--lock` sha256 hashes in trunk.yaml

## Additional Resources

- Known compromised versions: [references/compromised-versions.md](references/compromised-versions.md)
- Pinning script: [scripts/trunk-pin-versions.sh](scripts/trunk-pin-versions.sh)
- Advisory checker: [scripts/check-advisories.sh](scripts/check-advisories.sh)
