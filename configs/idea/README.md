# IntelliJ IDEA Config

Portable, version-controlled IntelliJ IDEA (Ultimate) setup for Java/Kotlin. The
macOS machine is the source of truth; the work Windows laptop (where JetBrains
Settings Sync isn't used) pulls this repo and applies it. Mirrors the
philosophy of `../vscode`.

## Why this doesn't look like the VS Code folder

VS Code has one mergeable `settings.json`. IDEA scatters config across dozens of
`options/*.xml` files, many holding secrets or machine paths. So instead of
merging everything, this folder is **allowlist + recommendations**: a small set
of curated, non-secret config files, plus opinionated docs on how to configure
the rest by hand. The live macOS install was scanned and found to be near-stock,
so most value here is recommended best practice, not a raw dump.

## Layout

| Path | Purpose |
|------|---------|
| `README.md` | This file. |
| `RECOMMENDATIONS.md` | **Start here.** Deep guide to using IDEA well (navigation, refactoring, debug, Spring, VCS, AI). |
| `plugins.md` | Documented plugin list (manual Marketplace install). |
| `secrets.md` | What must never be committed and why. |
| `WINDOWS-CHEATSHEET.md` | macOS → Windows path/keymap/line-ending differences. |
| `settings/codestyles/Google.xml` | Google Java style baseline (+ Kotlin official). Import via UI. |
| `settings/inspection/Recommended.xml` | Tightened inspection profile. Import via UI. |
| `settings/templates/JavaKotlin.xml` | Starter live templates. |
| `settings/options/editor.xml` | Curated editor behavior toggles. |
| `apply.sh` / `apply.ps1` | Stage curated files into the JetBrains config dir. |
| `.gitignore` | Blocks license key, DB creds, AI tokens, machine state. |

## Apply

### Windows (work box)
```powershell
cd configs\idea
./apply.ps1 -DryRun    # preview what gets copied
./apply.ps1            # copy curated settings (backs up existing, timestamped)
```

### macOS / Linux
```bash
cd configs/idea
./apply.sh --dry-run
./apply.sh
```

Both scripts auto-detect the newest `IntelliJIdea<ver>` config dir. **Launch
IDEA once first** so that dir exists.

## After applying — manual steps (unavoidable in IDEA)

The scripts stage files, but IDEA activates a few only through its UI:

1. **Plugins** — install from `plugins.md` (Marketplace), restart.
2. **Keymap** — Settings > Keymap → **VSCode**.
3. **Code style** — Settings > Editor > Code Style > gear > Import Scheme → `Google`.
4. **Inspections** — Settings > Editor > Inspections > gear > Import Profile → `Recommended`.
5. **SDK** — File > Project Structure > SDKs → add the machine's JDK.

Then read `RECOMMENDATIONS.md`.

## Secrets — read `secrets.md`

Nothing secret is committed. The license key, DB credentials, and AI tokens are
gitignored or stored in the OS keychain. You re-authenticate on each machine.

## Updating the repo from macOS

If you customize something worth keeping (a code style tweak, a live template),
copy the specific XML from `~/Library/Application Support/JetBrains/IntelliJIdea<ver>/`
into the matching `settings/` path here — **check it for secrets first** (see
`secrets.md`). Don't bulk-copy `options/`; most of it is machine-local.
