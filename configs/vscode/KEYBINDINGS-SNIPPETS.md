# Keybindings & Snippets

## Keybindings (`keybindings.json`)

Two custom bindings, both scoped to `terminalFocus` and using
`workbench.action.terminal.sendSequence` to inject raw bytes into the terminal.

| Key | Sends | Why |
|-----|-------|-----|
| `Ctrl+Enter` | `\` + CRLF (`\\\r\n`) | Line continuation — start a new shell/REPL line without executing, as if you typed a trailing backslash. |
| `Shift+Enter` | ESC + CR (`\r`) | Insert a newline inside TUIs / agent CLIs (e.g. multi-line prompt boxes) that treat ESC-CR as "newline, don't submit". |

These are OS-neutral and copy over to any machine unchanged. They only fire when
a terminal has focus, so they don't interfere with editor shortcuts.

### Adding more

Edit `keybindings.json` here, then re-run the apply script (or copy it into the
User dir). Keep it valid JSONC. To discover a command id, open the Keyboard
Shortcuts UI in VS Code (`Cmd/Ctrl+K Cmd/Ctrl+S`), right-click an entry →
*Copy Command ID*.

## Snippets (`snippets/`)

Per-language snippet files, copied verbatim to `User/snippets/`.

Current:
- `javascript.json` — `cl` → `console.log($1);`

### Adding more

Create `snippets/<language>.json` (e.g. `python.json`, `typescript.json`). Format:

```json
{
  "Snippet name": {
    "prefix": "trigger",
    "body": ["line one $1", "line two $0"],
    "description": "what it does"
  }
}
```

`$1`, `$2` = tab stops; `$0` = final cursor; `${1:label}` = placeholder text.
Re-run the apply script to push new snippet files to the User dir.
