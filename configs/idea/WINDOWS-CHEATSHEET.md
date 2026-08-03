# macOS → Windows differences (IntelliJ IDEA)

The macOS machine is the source of truth. When applying on the Windows work box,
these are the things that differ.

## Config dir location

| OS | Path |
|----|------|
| macOS | `~/Library/Application Support/JetBrains/IntelliJIdea<ver>/` |
| Windows | `%APPDATA%\JetBrains\IntelliJIdea<ver>\` |
| Linux | `~/.config/JetBrains/IntelliJIdea<ver>/` |

`<ver>` is year-based, e.g. `IntelliJIdea2026.1`. `apply.ps1` auto-detects the
newest one. Launch IDEA **once** before running the script so the dir exists.

## Modifier keys

The VSCode Keymap plugin maps most things, but native IntelliJ bindings differ:

| macOS | Windows |
|-------|---------|
| `Cmd` | `Ctrl` |
| `Cmd Shift A` (Find Action) | `Ctrl Shift A` |
| `Opt` / `Alt` | `Alt` |
| `Ctrl` (macOS, rare) | usually `Ctrl` too |

`RECOMMENDATIONS.md` writes shortcuts as `Cmd/Ctrl` for this reason.

## Line endings

Windows may default new files to CRLF. Set project line separator to **LF**:
Settings > Editor > Code Style > Line separator → `Unix and macOS (\n)`, and rely
on `.gitattributes`/`.editorconfig` in each project. Keeps diffs clean against
the macOS-authored repo.

## SDK / JDK paths

`options/jdk.table.xml` is gitignored (absolute paths). On Windows, set the JDK
fresh: File > Project Structure > SDKs > add your Windows JDK install
(e.g. `C:\Program Files\Eclipse Adoptium\jdk-21`).

## Font

If a font referenced in `editor-font` isn't installed on Windows, IDEA falls
back silently. JetBrains Mono ships with the IDE, so prefer it — portable.

## License

No key file. Sign in to your JetBrains account on the Windows box; Ultimate
activates from the account. (`idea.key` is gitignored and macOS-specific anyway.)

## Applying

```powershell
cd configs\idea
./apply.ps1 -DryRun   # preview
./apply.ps1           # copy curated settings
```

Then do the UI imports the script prints (code style, inspections, keymap).
