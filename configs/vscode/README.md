# VS Code Config

Portable, version-controlled VS Code setup. The macOS machine is the source of
truth; the work Windows laptop (where GitHub Settings Sync can't sign in) pulls
this repo and applies it.

## Layout

| File | Purpose |
|------|---------|
| `settings.shared.json` | Universal settings for every machine. **No secrets.** |
| `settings.macos.json` | macOS-only overrides (zsh, iTerm, Homebrew Python). |
| `settings.windows.json` | Windows-only overrides (Git Bash, Python path). |
| `settings.local.example.json` | Template for machine-local **secrets**. Copy → `settings.local.json`. |
| `keybindings.json` | Copied verbatim to the User dir. |
| `snippets/` | Copied verbatim to `User/snippets/`. |
| `extensions-core.txt` | Curated extension list the apply scripts install. |
| `merge_settings.py` | JSONC merge helper (later file wins; dicts deep-merge). |
| `apply.sh` | macOS/Linux apply script. |
| `apply.ps1` | Windows (PowerShell) apply script. |

Final `settings.json` = `shared` + `<os>` + `local` merged, later files winning.

## Secrets — read first

Secrets never live in the committed files. They go in `settings.local.json`,
which is **gitignored**. To set up secrets on a machine:

```bash
cp settings.local.example.json settings.local.json
# edit settings.local.json with your real keys, then run apply
```

Keys currently expected: `whisper-assistant.apiKey` (OpenAI), `chatgpt.apiBase`
(private proxy), `geminicodeassist.project` (GCP project id).

> The OpenAI key previously lived in plaintext settings. It has been removed
> from the repo. Rotate any key that was ever committed or synced.

## Apply — scripted

### macOS / Linux
```bash
cd configs/vscode
./apply.sh            # merge settings + copy keybindings & snippets
./apply.sh --ext      # also install core extensions
./apply.sh --dry-run  # preview merged settings, write nothing
```

### Windows (PowerShell)
```powershell
cd configs\vscode
./apply.ps1           # merge settings + copy keybindings & snippets
./apply.ps1 -Ext      # also install core extensions
./apply.ps1 -DryRun   # preview merged settings, write nothing
```

Both scripts back up any existing `settings.json` (timestamped `.bak`) before
overwriting, and require Python 3 for the merge.

## Apply — manual (no scripts)

VS Code User dir:
- macOS: `~/Library/Application Support/Code/User/`
- Windows: `%APPDATA%\Code\User\`
- Linux: `~/.config/Code/User/`

Steps:
1. Open `settings.shared.json`, then paste the keys from `settings.<your-os>.json`
   over/into it, then paste your `settings.local.json` keys last (they win).
   Save the result as `User/settings.json`. See **WINDOWS-CHEATSHEET.md** for the
   exact macOS→Windows line changes.
2. Copy `keybindings.json` → `User/keybindings.json`.
3. Copy `snippets/*.json` → `User/snippets/`.
4. Install extensions:
   ```bash
   grep -v '^#' extensions-core.txt | grep . | xargs -L1 code --install-extension
   ```
   (PowerShell: `Get-Content extensions-core.txt | ? {$_ -and -not $_.StartsWith('#')} | % { code --install-extension $_ }`)

## Updating the repo from the macOS machine

When you change settings on macOS and want to capture them, hand-port the new
universal keys into `settings.shared.json` (keep secrets out). Extensions:
`code --list-extensions` and add wanted ones to `extensions-core.txt`.
