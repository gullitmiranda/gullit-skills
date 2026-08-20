# npm worm IOCs — detection and response

Behavioral and artifact IOCs for the Shai-Hulud worm family (Shai-Hulud Sept
2025 → Shai-Hulud 2.0 Nov 2025 → Mini Shai-Hulud May 2026 → ChainDrop Aug
2026). These artifacts persist across campaigns nearly verbatim, making them
useful for post-compromise detection — not prevention. Prevention comes from
campaign-independent controls (minimum release age, sfw, install-script
blocking).

## Local compromise artifacts

If any of these exist, the worm has executed on the machine. Stop work and
report immediately:

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

## Response playbook

- **Do NOT revoke stolen tokens before cleaning the machine.** The worm
  family's token monitor watches for revocation and fires a destructive
  payload when it detects it. Clean artifacts first, then rotate credentials.
- The worm steals AI-tool credentials too: check `~/.claude/credentials.json`,
  `~/.codex/auth.json`, `~/.cursor/credentials.json` for exposure and rotate.

## Detection traps that no longer work

- **Provenance is not authorization.** ChainDrop (Aug 2026) was published with
  valid SLSA provenance via OIDC trusted publishing. A package having
  provenance says nothing about whether it is malicious.

## Campaign-specific compromised versions

Do not hardcode version lists here — they decay within hours (packages get
unpublished; the canonical record moves to CVEs). For version-specific checks,
query live sources instead:

- GitHub Advisory Database (malware advisories, API-queryable):
  https://github.com/advisories?query=malware+npm
- StepSecurity Threat Intel blog: https://www.stepsecurity.io/blog

Known major campaigns for context: TeamPCP CI/CD wave (Mar 2026), Mini
Shai-Hulud (May 2026), ChainDrop (Aug 2026, 444 packages / 2,212 versions,
started with `keyv@6.0.0`).
