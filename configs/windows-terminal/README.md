# Windows Terminal Config

`settings.json` for Windows Terminal, themed to match the macOS Ghostty setup:
**Catppuccin Mocha**, **JetBrainsMono Nerd Font** size 14, ~92% opacity with
acrylic. Pairs with `../powershell/` (PowerShell 7 is the default profile).

## Prerequisites

- **JetBrainsMono Nerd Font**:
  `winget install DEVCOM.JetBrainsMonoNerdFont` (or nerdfonts.com). Without a
  Nerd Font, posh-git / Terminal-Icons glyphs render as boxes.
- **PowerShell 7** for the default profile: `winget install Microsoft.PowerShell`.

## Apply

Windows Terminal settings live at (Store install):

```
%LOCALAPPDATA%\Packages\Microsoft.WindowsTerminal_8wekyb3d8bbwe\LocalState\settings.json
```

Steps:

1. **Back up** your current settings:
   ```powershell
   $wt = "$env:LOCALAPPDATA\Packages\Microsoft.WindowsTerminal_8wekyb3d8bbwe\LocalState\settings.json"
   Copy-Item $wt "$wt.bak"
   ```
2. Copy this file over it:
   ```powershell
   Copy-Item .\settings.json $wt -Force
   ```
3. Windows Terminal reloads on save. If it doesn't, restart it.

> Prefer merging by hand? Open Windows Terminal → Settings → *Open JSON file*,
> and copy the `schemes` (Catppuccin Mocha), `profiles.defaults`, and
> `defaultProfile` sections in. The profile **GUIDs** here are the standard
> well-known ones for PowerShell 7 / Windows PowerShell / Git Bash, so they
> should match your install; if a profile doesn't appear, check its GUID in
> your own settings and update `defaultProfile`.

## Notes

- `defaultProfile` points at PowerShell 7. Change it to the Windows PowerShell
  GUID (`{61c54bbd-...}`) if you don't install PS7.
- Git Bash profile matches the VS Code default terminal (`../vscode/`).
- Non-Store (unpackaged / Preview) installs use a different settings path —
  see the Windows Terminal docs.
