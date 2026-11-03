# Arc migration — browser replacement survey (Arc vs Zen vs Dia vs alternatives)

Status: complete.

Outcome: Zen adopted as the Arc replacement. Custom search engines (bangs) were
recreated manually through Zen's "Edit Search Engine" dialog (native Zen
feature; stock Firefox lacks it) — ArgoCD instances included. A reusable
extractor/migrator lives in dotfiles at `bin/arc-search-to-zen` for the
remaining engines or other machines; ArgoCD has no OpenSearch suggestions
endpoint, so the Suggestions URL field stays empty for those engines.

Researched 2026-10-23, primary sources only (official sites, help centers, release
notes, GitHub repos). Companion context: Arc announced shutdown on 2026-10-22.

## Requirements (in priority order, from Arc usage)

- **P1 — Spaces with a per-space profile**: separate cookies/logins per space.
- **P2 — Vertical tab management without keeping all tabs loaded**: sidebar tabs +
  auto-archive/unload of inactive tabs (Arc's Today Tabs auto-archived after 12h,
  configurable up to 30 days).
- **P3 — Link Router**: auto-route domains/links to a specific space (Arc's Air
  Traffic Control, at Arc > Settings > Links).
- **P4 — Mobile sync**: dispensable, but noted.
- Cross-cutting: performance with many tabs, and security posture (engine,
  update cadence, who builds it, telemetry/openness).

## Arc sunset facts (baseline for migration urgency)

- Arc stops working entirely on **2026-12-22**; no new accounts since 2026-10-22.
  Mobile sign-in/sync ends 2026-11-23; accounts deleted within 30 days after
  sunset. Arc Search iOS survives as a standalone lite browser.
  Source: https://arc.net , https://resources.arc.net/hc/en-us/articles/44412972248471
- Arc's own rationale: "we can no longer keep Arc as safe and secure as it needs
  to be". No security updates after sunset; no open-sourcing announced.
- One-time export: Settings > Advanced > Export Data produces a per-Space link
  list (`.md`), not a bookmarks file. Boosts are not exportable at all; Easels
  only as PNG. Source:
  https://resources.arc.net/hc/en-us/articles/25583851606039
- Official migration path is Dia: import maps Spaces → Profiles, Favorites →
  icon-only pinned tabs, Folders → Tab Groups. Air Traffic Control and Boosts/Easels
  do **not** exist in Dia. Sources:
  https://resources.arc.net/hc/en-us/articles/44413129117591 ,
  https://resources.arc.net/hc/en-us/articles/44413577819159
- Arc's isolation model, for comparison: Spaces share a Profile's
  logins/cookies/history unless Profiles are assigned; auto-archive of unpinned
  tabs 12h–30d; Air Traffic Control routes by domain; Chromium 156 at sunset,
  weekly security bumps until the end.

## Candidate verdicts

### Zen Browser (zen-browser.app) — closest overall match

- **P1 partial — cookie-level only.** Workspaces can bind a default Firefox
  container each; containers isolate cookies/sessions but not history or
  extensions. True profile separation requires separate Firefox profiles,
  outside the workspace system. Source:
  https://docs.zen-browser.app/user-manual/workspaces
- **P2 yes.** Vertical tabs are core (horizontal tabs explicitly refused). Firefox
  tab unloading + Zen-specific tab unloader (dimmed pending tabs, exclusion list).
  No Arc-style auto-archive of unpinned tabs; the new Library (1.23b) aggregates
  history/closed tabs. Sources: https://docs.zen-browser.app/faq ,
  https://docs.zen-browser.app/guides/about-config-flags
- **P3 yes — Space Routing.** URL-regex rules route links to specific spaces
  (case-insensitive regex, startup routing, `--space` CLI flag). Documented only
  via release notes so far, no docs page. Source:
  https://github.com/zen-browser/desktop/releases
- **P4 no.** No mobile browser and no plans (FAQ). Firefox Sync (Mozilla account)
  covers bookmarks/passwords/history desktop-to-desktop and to Firefox mobile.
  Zen-specific Spaces sync exists desktop-only (1.22b).
- **Security/trust:** MPL-2.0, small team, donation-funded. Tracks upstream Firefox
  security releases within 0–72h (verified in practice: FF 157 → 158.0 → 158.0.1
  during Oct 2026). No explicit telemetry/data-collection policy page found — gap.
  **No Widevine license on macOS**, so DRM streaming (Netflix, Spotify) does not
  work pending Google approval.
- **Status:** stable 1.23.4b (2026-10-20) on Firefox 158.0.1; macOS first-class.
  Sources: https://github.com/zen-browser/desktop ,
  https://docs.zen-browser.app/security , https://docs.zen-browser.app/faq

### Dia (diabrowser.com) — lowest-friction migration, no link router

- **P1 yes.** Profiles with separate tabs/logins, swipe switching, optional
  cross-profile sharing, unused profiles auto-unload. Arc import maps Spaces →
  Profiles.
- **P2 yes.** Sidebar (vertical) tabs, idle-tab sleeping, "tidy tabs" archives
  10+ stale tabs into a temporary group — a credible Today-Tabs successor.
- **P3 no.** No Link Router equivalent anywhere in official materials ("Dia can't
  automatically open certain sites in a specific Profile").
- **P4 no.** No mobile app; only Tab Handoff (open iPhone tabs on Mac).
- **Security/trust:** closed-source, The Browser Company. Chromium M156,
  weekly-ish release energy, heavily AI-centric roadmap; base browsing is free
  and AI is optional. E2E-encrypted sync claimed. macOS GA since Oct 2025,
  Windows 1.0 Oct 2026, Mac↔Windows sync in 1.3.0 (2026-10-22).
  Source: https://www.diabrowser.com/changelog

### Vivaldi — best P2/P4, fails P1

- **P1 no.** Workspaces organize tabs but share one cookie store — no per-space
  profile isolation.
- **P2 yes, best-in-class.** Memory Saver auto-hibernates unused tabs (4 levels);
  manual hibernation of tabs, stacks, or whole workspaces; vertical tab bars.
- **P3 yes.** Workspaces Rules: "If URL contains X → open in workspace Y" — the
  closest native Air Traffic Control equivalent. Routing moves tabs between
  workspaces that share cookies, though.
- **P4 yes.** E2E-encrypted sync, Android + iOS apps.
- **Security/trust:** independent European company, Chromium-based.
  Sources: https://help.vivaldi.com/desktop/tabs/workspaces/ ,
  https://help.vivaldi.com/desktop/tabs/memory-saver/

### Brave — P1 via new containers, no router found

- **P1 yes.** Built-in Containers shipped in v1.92 (Jul 2026): per-container
  cookie/storage isolation, no extension needed. Source:
  https://brave.com/blog/containers/
- **P2 partial.** Vertical tabs shipped in v1.52; no tab sleeping found. One user
  report of the vertical-tabs toggle greyed out on macOS/arm64 (unconfirmed).
- **P3 not found** in official sources.
- **P4 yes.** Sync exists.
- **Security/trust:** open source (MPL), ~4-week Chromium cadence.
  Source: https://brave.com/latest/

### Edge — solid P2/P4, P1 via profiles only

- **P1 via Chromium profiles**, but Edge Workspaces are shared tab sets and
  explicitly do not isolate logins/cookies per workspace; consumer availability
  looks uncertain (still in enterprise docs, dropped from consumer features
  page). Source:
  https://learn.microsoft.com/en-us/deployedge/microsoft-edge-workspaces
- **P2 yes** (vertical tabs + sleeping tabs are long-standing; not re-verified
  this pass — support.microsoft.com unreachable).
- **P3 partial:** automatic profile switching exists (unverified this pass).
- **P4 yes.**

### Others (one-liners)

- **SigmaOS:** alive but stagnant-looking; macOS-only WebKit with per-workspace
  profiles and auto page unloading; site content stale (© 2024). Source:
  https://sigmaos.com
- **Kagi browser** (browser.kagi.com): WebKit, zero telemetry, multi-store extensions,
  macOS/iOS; Windows/Linux pages 404; spaces/vertical-tabs/sync unverified.
- **Floorp:** open-source Firefox fork tying workspaces to containers for
  per-workspace logins; domain rules and sync unverified. Source:
  https://floorp.app
- **Firefox DIY (Multi-Account Containers + Tab Center Reborn):** the only stack
  with P1 + P3 together (MAC's "always open in this container" routes domains);
  vertical tabs are manual-unload only; full assembly cost.
  Sources: https://addons.mozilla.org/en-US/firefox/addon/multi-account-containers/ ,
  https://addons.mozilla.org/en-US/firefox/addon/tabcenter-reborn/

## Comparison matrix

| Candidate | P1 per-space profile | P2 vertical + auto-unload | P3 link router | P4 mobile | Engine / posture |
|---|---|---|---|---|---|
| Zen | Partial (containers: cookies only) | Yes (unload, no auto-archive) | **Yes (Space Routing)** | No | Gecko, MPL, 0–72h FF tracking, no Widevine |
| Dia | **Yes** | Yes (sleep + tidy tabs) | **No** | No | Chromium M156, closed-source |
| Vivaldi | No | **Yes (best)** | Yes (Workspace Rules) | Yes | Chromium, independent |
| Brave | Yes (containers) | Partial (no unload) | No | Yes | Chromium, open source |
| Edge | Profiles only | Yes | Partial (auto profile switch) | Yes | Chromium, Microsoft |
| Firefox DIY | Yes (MAC) | Partial (manual) | Yes (MAC) | Yes | Gecko, Mozilla |
| Kagi browser | Unverified | Unverified | No | Yes (iOS) | WebKit, user-funded |
| SigmaOS | Yes (claimed) | Yes | No | No | WebKit, stagnant |

## Synthesis

- **Zen is the only single browser covering P1 (cookie-level) + P2 + P3.** Its
  Space Routing is a direct Air Traffic Control analog; its container-bound
  workspaces give per-space logins. Weak points: cookie-only isolation (no
  history/extension separation), no auto-archive, no Widevine on macOS, small
  team, no telemetry policy, no mobile client.
- **Dia is the lowest-friction migration** (official importer, same mental
  model, best tab-archiving successor) but **drops the Link Router entirely**
  and is closed-source.
- **Vivaldi is the strongest P2/P4** with native domain→workspace rules, but
  shares one cookie jar across workspaces, killing P1.
- Pragmatic shape: trial **Zen** as primary (P3 is the hardest to replace);
  keep **Dia** as fallback if Zen's cookie-level isolation or Widevine gap
  bites. Chromium holdouts with fewer Arc-like needs: Vivaldi (P2+P4) or Brave
  (P1 via containers).

## Unverified / open items

- Exact Zen Space Routing configuration UX (no docs page yet — release notes only).
- Zen telemetry specifics; controversy history.
- Edge sleeping tabs / auto-profile-switching current state (support pages
  unreachable this pass).
- Brave domain→container auto-routing and macOS/arm64 vertical tabs toggle.
- MAC "always open in this container" behavior (support.mozilla.org bot-blocked).
- Widevine approval timeline for Zen.
