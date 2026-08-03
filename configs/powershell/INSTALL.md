# PowerShell Install Guide (Windows)

## 0. Prerequisites

- **PowerShell 7** (recommended): `winget install Microsoft.PowerShell`.
  Windows PowerShell 5.1 is built in and also supported, but some features
  (ListView predictions) are PS7-only and are auto-skipped on 5.1.
- **winget** (App Installer) — preinstalled on Windows 10/11. If missing,
  install "App Installer" from the Microsoft Store.
- **A Nerd Font** for icons/prompt glyphs (Terminal-Icons, posh-git):
  `winget install DEVCOM.JetBrainsMonoNerdFont` (or from nerdfonts.com), then
  select it in your terminal. The `../windows-terminal/settings.json` already
  points at `JetBrainsMono Nerd Font`.

## 1. Execution policy (once)

Profiles are scripts, so allow local scripts for your user:

```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

## 2. Apply

```powershell
cd my-stuff\configs\powershell
./apply.ps1 -Both -Modules -Tools
```

- `-Both` writes the profile to **both** profile paths:
  - PS7: `Documents\PowerShell\profile.ps1`
  - PS5.1: `Documents\WindowsPowerShell\profile.ps1`
- `-Modules` installs from `modules.txt` (PSGallery).
- `-Tools` installs from `tools.txt` (winget).
- Existing profiles are backed up (`.bak.<timestamp>`) before overwrite.

Run pieces independently if you prefer, e.g. `./apply.ps1 -Modules` only.

## 3. Profile paths reference

| Edition | `$PROFILE.CurrentUserAllHosts` |
|---------|-------------------------------|
| PowerShell 7 | `~\Documents\PowerShell\profile.ps1` |
| Windows PowerShell 5.1 | `~\Documents\WindowsPowerShell\profile.ps1` |

(If OneDrive redirects your Documents folder, these live under the OneDrive
Documents path — `$PROFILE` always resolves to the correct one.)

## 4. Tool notes

- **atuin**: the `atuin` PowerShell module provides `Enable-AtuinSearchKeys`.
  If `Install-Module atuin` fails, atuin's own installer / newer versions may
  ship the integration differently — check `atuin --help` and
  https://docs.atuin.sh. The profile guards this, so a missing module just
  means no Ctrl+R rebind (PSReadLine history search still works).
- **PSFzf**: needs the `fzf` binary (in `tools.txt`) *and* the `PSFzf` module.
- **zoxide/bat/lazygit/yazi**: pure binaries; the profile detects them via
  `Get-Command`.

## 5. Verify

```powershell
# In a fresh PowerShell:
$PROFILE                       # confirm which profile loaded
Get-Command z, bat, lazygit, atuin, yazi -ErrorAction SilentlyContinue
gs                             # git status shortcut
```

## Troubleshooting

- **"running scripts is disabled"** → step 1 (execution policy).
- **No icons / boxes instead of glyphs** → Nerd Font not selected in the
  terminal (step 0).
- **A tool "not recognized"** → not installed or not on PATH; re-run
  `./apply.ps1 -Tools`, then open a new terminal so PATH refreshes.
- **Slow startup** → usually atuin/zoxide history import on first run; settles
  after. Comment a block in `profile.ps1` to isolate if needed.
