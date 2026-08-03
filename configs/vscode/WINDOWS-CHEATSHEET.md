# macOS → Windows Cheatsheet

Everything universal lives in `settings.shared.json` and needs no change. Only
the OS-specific keys below differ. The apply scripts handle these automatically
via `settings.windows.json`; this sheet is for manual setup or debugging.

## Settings that change

| Setting | macOS value | Windows value |
|---------|-------------|---------------|
| `terminal.integrated.defaultProfile.osx` | `zsh` | *(not used on Windows — omit)* |
| `terminal.integrated.defaultProfile.windows` | *(not used on macOS)* | `Git Bash` |
| `terminal.external.osxExec` | `iTerm.app` | *(omit; use `terminal.external.windowsExec` if wanted)* |
| `python.defaultInterpreterPath` | `/opt/homebrew/bin/python3` | your Windows Python, e.g. `C:\\Python312\\python.exe` — or `""` to auto-detect |

## Finding your Windows Python path

```powershell
where.exe python
# or
(Get-Command python).Source
```
Paste the result into `settings.windows.json` → `python.defaultInterpreterPath`
(use double backslashes in JSON: `C:\\Users\\you\\...python.exe`), or leave it
`""` and let the Python extension pick.

## Terminal notes

- The repo assumes **Git Bash** as the default Windows terminal profile. Install
  Git for Windows so the profile exists. Prefer PowerShell instead? Change the
  value in `settings.windows.json` to `"PowerShell"`.
- The two custom keybindings in `keybindings.json` send terminal escape
  sequences (Ctrl+Enter → line continuation, Shift+Enter → ESC+CR). They are
  OS-neutral and copy over unchanged.

## Paths recap

| | macOS | Windows |
|-|-------|---------|
| User settings dir | `~/Library/Application Support/Code/User/` | `%APPDATA%\Code\User\` |
| `code` CLI | usually on PATH after install | enable via *Shell Command: Install 'code' command in PATH* from the command palette |

## Things that may not apply at work

Some settings/extensions reference tools that may be absent on the work laptop
(private ChatGPT proxy, whisper-assistant, Gemini project). They're harmless if
the extension isn't installed. Fill the corresponding secret in
`settings.local.json` only if you actually use that tool there.
