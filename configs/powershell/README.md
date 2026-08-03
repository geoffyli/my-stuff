# PowerShell Config

A Windows PowerShell profile that ports my macOS terminal experience
([live-in-terminal](https://github.com/geoffyli/live-in-terminal): zsh + zoxide
+ atuin + bat + lazygit + yazi) to the work Windows laptop. Targets **both**
PowerShell 7 (`pwsh`) and Windows PowerShell 5.1 with one guarded profile.

> Authored on macOS where `pwsh` isn't installed, so it can't be run here.
> Every tool init is guarded — a missing tool is silently skipped, never an
> error on shell start. Test on Windows and iterate.

## Layout

| File | Purpose |
|------|---------|
| `profile.ps1` | The shared profile. Aliases, functions, tool init. **No secrets.** |
| `profile.local.example.ps1` | Template for machine-local secrets/overrides → copy to `profile.local.ps1` (gitignored). |
| `modules.txt` | PowerShell Gallery modules to install. |
| `tools.txt` | winget CLI tool package ids (zoxide, bat, lazygit, atuin, fzf, yazi). |
| `apply.ps1` | Copies the profile to `$PROFILE`, optionally installs modules + tools. |
| `INSTALL.md` | Full walkthrough, per-PS-version notes, execution policy. |

## What the profile gives you

| Mac tool | Windows equivalent in this profile |
|----------|------------------------------------|
| zsh-autosuggestions / syntax-highlighting | PSReadLine (prediction + colors) |
| Oh My Zsh git plugin | posh-git prompt |
| zoxide (`z`) | zoxide |
| atuin (Ctrl+R) | atuin |
| bat + `bathelp`/`help` | bat + `Show-Help`/`bathelp` |
| lazygit (`lg`) | `lg` alias |
| yazi (`y` cd-on-quit) | `y` function |
| Terminal-Icons in `ls` | Terminal-Icons |
| `EDITOR=nvim` | `$env:EDITOR=nvim`, `vim`→nvim |
| git shortcuts | `gs ga gc gp gl gd glg` |

Not ported: `cc-official`/`cc-copilot`/`cc-status` (Mac proxy workflow, by choice).

## Quick start (Windows)

```powershell
git clone https://github.com/geoffyli/my-stuff
cd my-stuff\configs\powershell

# Allow local profile scripts once (per user):
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned

# Full setup for both PS editions: copy profile + install modules + tools
./apply.ps1 -Both -Modules -Tools

# Preview only:
./apply.ps1 -DryRun
```

Open a new terminal to load it. See **INSTALL.md** for details, and
`../windows-terminal/` for the matching Windows Terminal theme (Catppuccin
Mocha + JetBrainsMono Nerd Font).

## Secrets

Never in the tracked profile. Copy `profile.local.example.ps1` →
`profile.local.ps1` (gitignored) beside your `$PROFILE` and put keys/proxies
there. `apply.ps1` seeds it for you if missing.
