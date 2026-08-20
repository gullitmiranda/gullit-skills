# npm worm IOCs (Mini Shai-Hulud)

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

## Compromised package versions (2026-05-11)

Source of truth (full list): https://www.stepsecurity.io/blog/mini-shai-hulud-is-back-a-self-spreading-supply-chain-attack-hits-the-npm-ecosystem

Key compromised versions:
- `@tanstack/react-router`: 1.169.5, 1.169.8
- `@tanstack/router-core`: 1.169.5, 1.169.8
- `@tanstack/router-plugin`: 1.167.38, 1.167.41
- `@tanstack/router-vite-plugin`: 1.166.53, 1.166.56
- `@mistralai/mistralai`: 2.2.3, 2.2.4
- `@opensearch-project/opensearch`: 3.6.2
- `safe-action`: 0.8.3, 0.8.4
