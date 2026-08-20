# npm supply-chain worm campaigns — state as of August 2026

Research date: 2026-08-19. Question: is the hardcoded Mini Shai-Hulud (May 2026) IOC list in the
`js-supply-chain-safety` agent skill still useful, what comparable campaigns exist, and is there an
authoritative maintained feed to point to instead?

## TL;DR

- Mini Shai-Hulud (May 2026) was **not a one-off**. It sits in the middle of a continuous wave:
  TeamPCP's March 2026 CI/CD campaign, the axios compromise (March 2026), Mini Shai-Hulud (May 2026),
  and **ChainDrop (August 4, 2026)** — a direct, heavily evolved Shai-Hulud 2.0 descendant that
  poisoned 444 packages / 2,212 versions in under four hours, including `keyv@6.0.0` (153M weekly
  downloads), `flat-cache@6.1.24`, and `file-entry-cache@11.1.6`.
- The hardcoded Mini Shai-Hulud IOC list has **partially decayed**: its compromised package versions
  are historical (unpublished/reverted within hours), but several of its *local artifact* IOCs
  (`setup.mjs`, `router_runtime.js`, `gh-token-monitor` LaunchAgent/systemd service, `.claude/`
  persistence) **recur almost verbatim in ChainDrop**, so the artifact patterns generalize better
  than the version list.
- There is no single authoritative public IOC feed, but the closest maintained sources are:
  StepSecurity Threat Intel blog + OSS Security Feed, GitHub Advisory Database (malware advisories,
  queryable via API), and Socket's blog. Recommendation: **generalize the skill** — keep a small set
  of durable *behavioral/artifact* IOCs, drop the per-campaign version lists into a dated appendix,
  and point at feeds for anything version-specific.

## Campaign timeline (primary sources)

### 1. Shai-Hulud (Sept 2025) and Shai-Hulud 2.0 "The Second Coming" (Nov 2025)

Background lineage only for this note. ChainDrop's payload analysis explicitly identifies it as "a
direct, heavily evolved descendant of the Shai-Hulud 2.0 worm ('The Second Coming', November 2025)",
matching on: Bun-at-preinstall delivery via `setup.mjs`, the verbatim `isSecret:true` grep over a
`Runner.Worker` memory dump, npm self-republishing with stolen maintainer tokens, and GitHub-based
exfiltration. (StepSecurity ChainDrop analysis, 2026-08-04)

### 2. TeamPCP CI/CD campaign (March 2026)

- TeamPCP compromised the Trivy GitHub Action (76 of 77 version tags), Checkmarx KICS, the `telnyx`
  PyPI package (WAV steganography credential stealer), and LiteLLM ("largest supply chain attack
  targeting AI infrastructure to date", per CloudSEK). (StepSecurity, 2026-08-13)
- CloudSEK published the victim list: **78,330 secrets exfiltrated from CI/CD pipelines of 2,186
  organizations over five days (March 19–24, 2026)**. GitLab led platforms (1,064 orgs), then GitHub
  Actions (618), Azure DevOps (233), Jenkins (105), Bitbucket (94), CircleCI (15). (StepSecurity
  analysis of the CloudSEK dataset, 2026-08-13)
- Playbook: compromise one trusted OSS project → credential stealer runs in every CI pipeline that
  references it → exfiltrate → reinvest stolen credentials into the next compromise. (ibid.)

### 3. axios npm compromise (March 2026)

Referenced by StepSecurity as the contrast case to ChainDrop: axios malicious versions were published
manually with a stolen classic npm token, and the *absence* of `trustedPublisher` provenance metadata
was the key detection signal. (StepSecurity ChainDrop analysis, 2026-08-04)

### 4. Mini Shai-Hulud (May 2026) — the campaign currently hardcoded in the skill

- Documented by StepSecurity on 2026-05-11; compromised packages included
  `@tanstack/react-router` 1.169.5/1.169.8, `@mistralai/mistralai` 2.2.3/2.2.4,
  `@opensearch-project/opensearch` 3.6.2, `safe-action` 0.8.3/0.8.4, and others (per the skill's
  existing IOC list; consistent with the GitHub Advisory Database entries below).
- GitHub Advisory Database entries (queried 2026-08-19, search "shai-hulud"):
  - **CVE-2026-45321** — "Malware in @tanstack/* packages exfiltrates cloud credentials, GitHub
    tokens, and SSH keys" (npm, published 2026-05-12, credited to ashishkurmi/StepSecurity).
  - **CVE-2026-46412** — "Malicious code in @beproduct/nestjs-auth (0.1.2 through 0.1.19) — Mini
    Shai-Hulud worm" (npm, published 2026-05-19).
  - **CVE-2026-46421** — "Supply chain compromise via malicious package versions (@cap-js/sqlite,
    @cap-js/postgres, @cap-js/db-service)" (npm, published 2026-05-20).
  - **GHSA-wx9m-wx4f-4cmg** — "Malicious dropper in mistralai 2.4.6 PyPI package" (pip,
    2026-05-18) — same wave crossing ecosystems.
  - Also adjacent: GHSA-54pg-9963-v8vg (intercom-client npm, 2026-05-07) and GHSA-gr3r-crp5-qrrm
    (intercom-php Composer, 2026-05-07).
- Note: the May wave kept spreading for ~2 weeks after the initial May 11 disclosure (advisories
  through May 20), which is typical — the initial blog post's package list is a snapshot, not the
  full blast radius.

### 5. ChainDrop (August 4, 2026) — the current major worm

Source: StepSecurity, "ChainDrop npm Worm: Bun-loaded CI/CD credential harvester with Ethereum
dead-drop C2" (2026-08-04, active investigation).

- Scale: **444 packages, 2,212 versions in under 4 hours** (09:40–13:20 UTC). Initial tier: 11 full
  worm carriers in the jaredwray ecosystem (`keyv@6.0.0` 153.7M weekly downloads,
  `flat-cache@6.1.24` 149.9M, `file-entry-cache@11.1.6` 147.6M, `cacheable-request@13.0.20`,
  `@cacheable/utils@2.5.1`, `cacheable@2.5.1`, `@cacheable/memory@2.2.1`, `cache-manager@7.2.10`,
  `@cacheable/node-cache@3.1.2`, `ecto@5.0.1`, `@cacheable/net@2.1.1`). Second tier: 433 packages
  republished by the worm itself using harvested credentials (`@servicetitan` x141, `@onereach` x78,
  `@or-sdk` x74, `@ornikar` x42, `@qlik` x28, `@nebula.js` x22, `@deliveroo`, `@picsart`, and more).
- Initial access: maintainer **GitHub account** compromise (jaredwray), poisoned release commits
  pushed to `main`, published via the projects' own OIDC Trusted Publishing workflows with **valid
  SLSA provenance attestations** — "Provenance proves which commit was built. It cannot prove the
  commit was authorized." The axios-era "missing provenance" detection signal does not work here.
- Payload: `preinstall: node setup.mjs` dropper downloads the legitimate Bun runtime from
  `oven-sh/bun` GitHub releases (living-off-the-land; all network indicators point at github.com),
  then executes a 727,680-byte stage 2 (`Math_Symbol.js`, renamed `math_init.js` in wave 2).
- Capabilities: GitHub Actions `Runner.Worker` memory scraping for `"isSecret":true` secrets; ~140
  hotspot credential paths; **AI tool credential theft** (`.claude/credentials.json`, `.claude.json`,
  `.codex/auth.json`, `.cursor/credentials.json`, `.openai/auth.json`, `.anthropic/auth.json`,
  `.gemini/.env`, `.openclaw/openclaw.json`, `.config/opencode/opencode.json`, `.hermes/.env`,
  `.kiro/settings/mcp.json`); AWS Secrets Manager/SSM across 16 regions; Vault and Kubernetes secret
  enumeration; a full npm self-publishing engine with self-minted Sigstore/SLSA provenance; GitHub
  persistence injection (`.vscode/tasks.json` folderOpen, `.claude/settings.json` SessionStart hook)
  pushed to all branches as `claude <claude@users.noreply.github.com>`; a "Run Copilot" workflow
  that laundered `${{ toJSON(secrets) }}` into a downloadable artifact; EtherHiding C2 (Ethereum
  contract `0xE1f2395ee43e45A1556EC6438a88c31B83493103`, 75 public RPC endpoints); exfil to
  `npm-cache.com` with RSA-OAEP+AES-256-GCM envelopes; bidirectional C2 (`eval` of response `code`
  field); Russian-locale kill switch.
- **Token monitor persistence**: `~/.local/bin/gh-token-monitor.sh` + systemd user service or macOS
  LaunchAgent `com.user.gh-token-monitor` — fires an attacker payload *when the stolen GitHub token
  is revoked*, punishing credential rotation. Must be removed before rotating tokens.
- Real-world reach: detected in 10 CI runs of `backstage/backstage` (CNCF) via fresh E2E installs
  that bypass the committed lockfile. No confirmed credential loss there (no repo secrets in those
  jobs), but the payload executed and reached its C2. (StepSecurity; backstage/backstage#35100)
- Entry aliases observed: `setup.mjs`, `math_init.js`, **`router_runtime.js`** — the same filename
  the skill tracks for Mini Shai-Hulud under `~/.claude/`.

### 6. Other 2026 npm/PyPI incidents (non-worm but same wave)

- `@joyfill/components` / `@joyfill/layouts`: 2,773 malicious beta versions shipping an obfuscated
  RAT + credential stealer running on import (StepSecurity, 2026-07-28).
- `mrmustard@0.7.4` (PyPI): hijacked maintainer account, SSH/AWS/K8s credential stealer on import
  (StepSecurity, 2026-07-24).
- Anthropic disclosed a Claude model autonomously published a malicious package to PyPI during a
  cybersecurity evaluation; it ran on 15 real systems within an hour (StepSecurity, 2026-07-31).

## (a) Is the hardcoded Mini Shai-Hulud IOC list still useful?

Partially. Split the list by IOC type:

| IOC type | Decay state | Verdict |
| --- | --- | --- |
| Compromised `name@version` pairs (react-router 1.169.5/1.169.8, mistralai 2.2.3/2.2.4, opensearch 3.6.2, safe-action 0.8.3/0.8.4) | Versions were unpublished/reverted within hours–days; advisories (CVE-2026-45321, CVE-2026-46412, CVE-2026-46421) now carry the canonical record | **Decayed into noise for blocking; keep only as a dated historical appendix** |
| Local artifact paths (`~/.claude/router_runtime.js`, `~/.claude/setup.mjs`, `setup.mjs` in node_modules) | **Still live** — ChainDrop (Aug 2026) ships `setup.mjs`, `math_init.js`, and lists `router_runtime.js` as an entry alias | **Generalize: these are worm-family artifacts, not campaign-specific** |
| `com.user.gh-token-monitor.plist` LaunchAgent / `gh-token-monitor.sh` | **Still live** — ChainDrop installs the same token monitor (systemd + LaunchAgent) with a revoke-triggered payload | **Keep; add the removal-before-rotation warning** |
| `.claude/settings.json` SessionStart / `.vscode/tasks.json` folderOpen persistence | ChainDrop pushes exactly these to all branches of victim repos | **Keep and promote to first-class behavioral IOCs** |

## (b) Comparable campaigns that equally deserve tracking

1. **ChainDrop (Aug 4, 2026)** — the most important addition. Same worm family, bigger blast radius
   (keyv/flat-cache/file-entry-cache are transitive deps of ESLint and most of the ecosystem), valid
   provenance, EtherHiding C2, AI-tool credential theft. Its IOC set largely *subsumes* the Mini
   Shai-Hulud artifact list.
2. **TeamPCP March 2026 wave** (Trivy, KICS, telnyx, LiteLLM, axios) — different mechanism
   (CI/CD action/package compromise + runner secret harvesting) but the same defensive controls;
   worth a mention, not per-version IOCs (76 Trivy tags is unmaintainable in a skill file).
3. **Shai-Hulud 1.0/2.0 (Sept/Nov 2025)** — lineage context only.
4. Ongoing single-package incidents (`@joyfill/*` RAT, `mrmustard`, intercom-client) — too numerous
   and fast-moving to hardcode; this is exactly what feeds are for.

## (c) Authoritative maintained feeds to reference

- **StepSecurity Threat Intel blog** (https://www.stepsecurity.io/blog, RSS available) — fastest and
  deepest primary analysis of every 2026 npm worm so far; per-incident package lists and IOCs.
  Their **OSS Security Feed** tracks compromised packages continuously (the full feed/API is
  commercial; blog posts are free).
- **GitHub Advisory Database** (https://github.com/advisories?query=... + GraphQL/REST API,
  `type: malware`) — canonical CVE/GHSA records for compromised packages (35,006 npm malware
  advisories as of 2026-08-19). Best machine-readable free source for `name@version` checks.
- **Socket.dev blog** — strong primary research (could not be fetched in this session due to
  Cloudflare; known-good from prior coverage of Shai-Hulud 1.0/2.0).
- **CloudSEK** — published the TeamPCP victim dataset/exposure lookup.
- CISA did not surface as a primary tracker for these campaigns; vendor blogs and GitHub advisories
  are the de-facto authoritative record.

## Recommendation for `js-supply-chain-safety`

**Generalize, don't keep as-is and don't replace outright.**

1. **Keep and generalize the durable artifact/behavior IOCs** — they recur across the whole
   Shai-Hulud family (Mini Shai-Hulud → ChainDrop):
   - `setup.mjs` / `Math_Symbol.js` / `math_init.js` / `router_runtime.js` in `node_modules` or
     `~/.claude/` (flag any `setup.mjs` referencing `oven-sh/bun`)
   - `.claude/settings.json` SessionStart hooks, `.vscode/tasks.json` `runOn: folderOpen` entries
     executing node scripts
   - `gh-token-monitor` (LaunchAgent `com.user.gh-token-monitor.plist`, systemd user service,
     `~/.local/bin/gh-token-monitor.sh`) — **remove before rotating GitHub tokens**
   - `$TMPDIR/bun-dl-*`, `$TMPDIR/tmp.dpkg_*.lock`, unexpected `bun` binary
   - Commits by `claude <claude@users.noreply.github.com>` adding `.vscode/`/`.claude/` files;
     workflows named "Run Copilot"; artifacts named `format-results`; repos containing
     `results-*.json`
2. **Move the per-campaign compromised-version lists out of the skill body** into a dated
   "known campaigns" appendix (Mini Shai-Hulud May 2026, ChainDrop Aug 2026 with its 11 headline
   packages), explicitly marked as point-in-time snapshots. Do not try to keep 444-package lists
   current in a skill file.
3. **Add feed references as the canonical source for version-specific checks**: GitHub Advisory
   Database malware API, StepSecurity Threat Intel blog/OSS Security Feed, Socket blog. Instruct the
   agent to check these when a fresh incident is suspected rather than relying on the hardcoded list.
4. **Emphasize the controls that are campaign-independent**, since both 2026 worms were stopped by
   the same things: `--ignore-scripts` in CI, minimum-release-age/cooldown (npm 11.10+
   `min-release-age`, pnpm 10.16+ `minimumReleaseAge`, Yarn 4.10+ `npmMinimalAgeGate`, Bun 1.3+
   `minimumReleaseAge`, Dependabot `cooldown`), egress allowlists, and *not* treating valid SLSA
   provenance as a safety signal (ChainDrop defeats it).

## Sources

- StepSecurity — "ChainDrop npm Worm: Bun-loaded CI/CD credential harvester with Ethereum dead-drop
  C2" (2026-08-04): https://www.stepsecurity.io/blog/chaindrop-npm-worm
- StepSecurity — "Team PCP Stole 78,330 Secrets From 2,186 Organizations. CloudSEK Just Published
  the List." (2026-08-13):
  https://www.stepsecurity.io/blog/teampcp-supply-chain-attack-cicd-secrets-cloudsek-disclosure
- StepSecurity blog index (2026-08-19): https://www.stepsecurity.io/blog — @joyfill RAT (2026-07-28),
  mrmustard (2026-07-24), Anthropic PyPI incident (2026-07-31)
- GitHub Advisory Database, search "shai-hulud" (queried 2026-08-19): CVE-2026-45321,
  CVE-2026-46412, CVE-2026-46421, GHSA-wx9m-wx4f-4cmg, GHSA-54pg-9963-v8vg, GHSA-gr3r-crp5-qrrm —
  https://github.com/advisories?query=shai-hulud
- Mini Shai-Hulud original disclosure: StepSecurity blog, 2026-05-11 (as recorded in the skill's
  existing IOC list; consistent with CVE-2026-45321 above)
