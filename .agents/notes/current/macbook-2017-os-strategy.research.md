# MacBook Pro 2017 OS Strategy: SketchUp, Homebrew Exit, and the Linux Option

Accessed: 2026-10-21.
Status: research verified; on-hardware validation deferred by user; OS decision
pending the validation gate below.

## Question

Which OS and toolchain should the personal MacBook Pro 13" (2017, Intel i7,
16 GB RAM, Intel Iris Plus 640, macOS Ventura 13.7.8 — the final Ventura
patch, hardware caps at Ventura officially) run, given that the machine's
primary application goal is SketchUp Desktop and Homebrew no longer installs
on Intel macOS?

## Conclusion

- **Homebrew is effectively unavailable on this machine.** Homebrew 7.0.0
  (September 2026) moved Intel Macs to Tier 3; the installer now requires
  Apple Silicon on supported hardware. No new Intel bottles are built, so
  everything compiles from source, and Intel support is scheduled for removal
  in/after September 2027. Homebrew itself recommends MacPorts for Intel
  macOS. Irony worth noting: Homebrew is Tier 1 on Linux x86_64, so wiping
  the machine for Linux *restores* brew.
- **SketchUp Desktop has no Linux build**, and current SketchUp no longer
  supports Ventura: supported versions are 2024–2026 and supported macOS is
  14 Sonoma and newer. Ventura can still run SketchUp 2025 (which required
  macOS 12+ at release), but that is a dead end once 2025 features are
  insufficient.
- **The decision gate is the `.skp` pipeline on Linux.** If representative
  files open cleanly through OpenSKP-based tools and editing needs do not
  depend on SketchUp Ruby extensions or LayOut, Linux is the best all-around
  option for this machine (brew Tier 1 again; the dotfiles repo already
  carries `linux:` `apt-get` blocks). If the usage does depend on extensions
  or LayOut, stay on macOS: SketchUp 2025 on Ventura now, OpenCore Legacy
  Patcher (OCLP) to Sonoma when a newer SketchUp is needed.
- **mise is not a full brew replacement** (no brew backend), but it covers
  roughly 70–80% of the personal CLI tool list; the remainder goes to
  MacPorts on macOS or apt/brew on Linux.

## Verified findings

### Homebrew on Intel macOS

- Installer gate: Apple Silicon + supported hardware; Intel Macs and macOS
  Ventura are both Tier 3 (no CI, no Apple security updates for Ventura).
- No new Intel bottles; source-only builds; support removal announced for
  in/after September 2027. Homebrew's own docs recommend MacPorts for Intel
  macOS through Sequoia.
- Sources: `docs.brew.sh/Installation`, `docs.brew.sh/Support-Tiers`,
  `brew.sh/blog` (7.0.0 announcement). Verified in the research session that
  preceded this note; not re-fetched today.

### SketchUp Desktop requirements (verified 2026-10-21)

- Supported versions: SketchUp 2024, 2025, 2026. SketchUp 2023 and older are
  unsupported.
- Supported OS targets: Windows 11 and macOS 26 (Tahoe), 15 (Sequoia),
  14+ (Sonoma). There is no Linux target.
- SketchUp 2026 dropped macOS 13 and older. SketchUp 2025 at release required
  macOS 12+ (third-party mirrors of the release notes; not re-verified on a
  Trimble page), so 2025 still installs on Ventura — outside the currently
  supported window.
- Graphics: the new engine needs Metal 2 on macOS; the unsupported-GPU list
  covers 2013–2015 Intel iGPUs (HD 5000/6000, Iris, Iris 6100, Iris Pro).
  The Iris Plus 640 in this machine is not on that list; the classic
  renderer needs OpenGL 3.1.
- Older versions are downloadable at `sketchup.trimble.com/en/download/all`.
- Source: `help.sketchup.com/en/sketchup/system-requirements` (fetched
  directly; the `getting-started/...` variant of this URL 404s — path moved).

### OCLP (OpenCore Legacy Patcher)

- Boots macOS Sonoma (and Sequoia on current OCLP) on 2016–2017 Metal-capable
  Macs, including this one. It does not change the CPU architecture, so brew
  stays Intel Tier 3 — OCLP fixes the SketchUp OS requirement, not Homebrew.
- Widely documented project behavior; not fetched in this session.

### mise backends (verified in the prior session)

- Backends: release-based (GitHub/GitLab/Forgejo), aqua, HTTP/S3, conda,
  language package managers (cargo, npm, pipx, gem, go, ...), vfox/asdf.
  `ubi` is deprecated. **There is no Homebrew backend or plugin.**
- Not covered by mise in the personal tool list: shells (bash/zsh/fish),
  docker/colima/qemu stack, google-cloud-sdk, GUI casks, coreutils/telnet/
  wget/httpie (MacPorts territory on macOS), zinit/fisher (own installers).

### Opening `.skp` on Linux (verified 2026-10-21)

The OpenSKP project (`github.com/iamahsanmehmood/openskp`, MIT) reverse
engineered the SketchUp binary format with no Trimble SDK:

- Reads both containers: modern VFF (2021+, a ZIP with a custom header) and
  legacy MFC CArchive (2013–2020). Writes real legacy-format `.skp`
  (validated against the actual SketchUp SDK). Python, TypeScript, .NET,
  Dart, C++; runs on Linux/macOS/Windows.
- Converts `.skp` to GLB, OBJ, STL, PLY, DXF 3D, IFC4, JSON, and ThatOpen
  Fragments — so any Linux CAD/BIM tool can ingest converted files.
- Real-file version sweep: 2014–2018, 2020, 2021, 2025 and V6–V8/2013
  parse cleanly; V3–V5 and 2019 hit known gaps in some language ports
  (Python-only fixes so far).
- CAD/DCC integrations, both early: **blender-openskp** (import + export,
  collection-instancing; also listed on `extensions.blender.org`; Blender
  4.2+) and **freecad-openskp** (import + export with real B-rep geometry,
  not triangulated). Materials/layers are not yet carried over in either.
  `skppy` (community Blender addon) claims materials including VRay and
  n-gon support — forum claims, not verified.
- Production users include **IngeTrazo**, a free Linux-first 3D modeler for
  civil engineering and architecture positioned as a SketchUp alternative
  (uses OpenSKP as its native `.skp` import backend, replacing a
  Wine + proprietary DLL path), and FrameSmart (Linux-hosted viewer).
- SketchUp Free/Go also runs in a browser, which works on Linux — the
  official web option.

### What does not migrate off SketchUp

- The Ruby extension ecosystem (OpenCutList, FlexTools, ...).
- LayOut (2D documentation generated from the model).
- Dynamic Components interactive behavior (attributes are extracted, but
  the behavior is SketchUp-only).
- The push/pull modeling UX: Blender is a mesh/DCC paradigm, FreeCAD is
  parametric; IngeTrazo is the closest Linux-native SketchUp-like tool.

## Options considered

| Option | SketchUp | Dev tooling | Verdict |
| --- | --- | --- | --- |
| Stay on Ventura | SketchUp 2025 only (officially out of the supported OS window); dead end | brew gone; mise + MacPorts | Status quo; fine short-term |
| OCLP to Sonoma | Current SketchUp supported again | brew still Tier 3 Intel | The macOS path if SketchUp Desktop stays essential |
| Linux (distro of choice) | No SketchUp Desktop; `.skp` via OpenSKP pipeline, Blender/FreeCAD/IngeTrazo, SketchUp Web | brew Tier 1; dotfiles `linux:` blocks already exist | Best overall if the validation gate passes |

## Validation gate (defined, deliberately not executed)

Run with representative personal `.skp` files before wiping macOS:

1. On macOS (Ventura): `pip install openskp`; parse, `buildScene()`, export
   to GLB/OBJ/IFC4. Check component hierarchy, materials, and dimensions.
2. On macOS: Blender 4.2+ with the OpenSKP Import/Export extension (and
   compare `skppy` for material fidelity).
3. Live-USB Linux boot on the MBP 2017 (pre-T2, installs are
   straightforward; Broadcom Wi-Fi firmware is the usual caveat) and rerun
   the same pipeline on hardware.
4. Gate: every representative file opens clean AND editing needs do not
   depend on Ruby extensions or LayOut → proceed with Linux. Otherwise →
   stay macOS per the options table.

## Parked

- Making the dotfiles repo brew-optional (mise + MacPorts fallbacks for the
  `darwin:` blocks) was proposed and not yet accepted.

## Verification honesty

Verified directly on 2026-10-21: SketchUp system requirements page, OpenSKP
repository README (features, version sweep, integrations, production users),
the Blender extension listing, and the skppy Blender Artists thread.
From the prior session, verified: Homebrew installation/support-tier pages,
mise backend docs. Not verified: actual `.skp` conversion behavior on guma's
files (validation deferred), `skppy` quality claims, OCLP behavior on this
specific machine, and the SketchUp 2025 minimum-OS claim on a Trimble page.

## Sources

- [Homebrew Installation docs](https://docs.brew.sh/Installation) and
  [Support Tiers](https://docs.brew.sh/Support-Tiers); [brew.sh blog](https://brew.sh/blog)
- [SketchUp Hardware and Software Requirements](https://help.sketchup.com/en/sketchup/system-requirements);
  [Trimble download page for older versions](https://sketchup.trimble.com/en/download/all)
- [mise dev-tools backends](https://mise.jdx.dev/dev-tools/backends/)
- [OpenSKP repository](https://github.com/iamahsanmehmood/openskp);
  [openskp.com web viewer](https://openskp.com);
  [OpenSKP Import/Export — Blender Extensions](https://extensions.blender.org/add-ons/openskp-import-export/);
  [blender-openskp](https://github.com/iamahsanmehmood/blender-openskp);
  freecad-openskp and the IngeTrazo/FrameSmart entries are linked from the
  OpenSKP README's CAD/DCC Integrations and Used-in-Production tables
- [skppy and SketchUp .skp import/export — Blender Artists](https://blenderartists.org/t/skppy-and-sketchup-skp-import-export/1649961)
