# Windows Productivity Tools (Open Source)

A short, opinionated list of open-source projects that improve daily work on
Windows. The focus is **company-managed machines** with these limits:

- No downloading prebuilt `.exe` or installer files.
- Source code arrives as a ZIP. We build or run it ourselves.
- Python and Node.js/JavaScript work. **.NET does not work for now.**

So the rule is: prefer projects that run as **web pages, scripts, or
`pip`/`npm` packages**. Avoid projects that need a .NET SDK or ship a new
native binary.

> Research notes, not tested configs. Last research round: 2026-10-12.
> Facts marked **(README)** were read from the project page. Facts marked
> **(check)** are from memory or inference. Verify them on the target machine.

## Quick picks

| Need | Pick | Stack | Runs from source? |
|------|------|-------|-------------------|
| Offline dev toolbox | [IT-Tools](https://github.com/CorentinTh/it-tools) | Vue, TypeScript | Yes. Static site. |
| Data/crypto "Swiss Army knife" | [CyberChef](https://github.com/gchq/CyberChef) | JavaScript | Yes. Static site. |
| Diagrams / whiteboard | [Excalidraw](https://github.com/excalidraw/excalidraw) | React, TypeScript | Yes (check build steps). |
| API client (GUI) | [Bruno](https://github.com/usebruno/bruno) | JavaScript, Electron | Needs Electron. |
| API client (terminal) | [Posting](https://github.com/darrenburns/posting) | Python, Textual | Yes, `pip`. |
| HTTP from the shell | [HTTPie](https://github.com/httpie/cli) | Python | Yes, `pip`. |
| Debug HTTP(S) traffic | [mitmproxy](https://github.com/mitmproxy/mitmproxy) | Python | Yes, `pip`. |
| SQL client (terminal) | [Harlequin](https://github.com/tconbeer/harlequin) | Python, Textual | Yes, `pip`. |
| Postgres CLI | [pgcli](https://github.com/dbcli/pgcli) | Python | Yes, `pip`. |
| System monitor | [Glances](https://github.com/nicolargo/glances) | Python | Yes, `pip`. |
| App launcher | [Ueli](https://github.com/oliverschwendener/ueli) | TypeScript, Electron | Needs Electron. |
| App launcher (alt.) | [Cerebro](https://github.com/cerebroapp/cerebro) | JavaScript, Electron | Needs Electron. |
| SSH/SFTP client | [electerm](https://github.com/electerm/electerm) | JavaScript, Electron | Needs Electron. |

## Constraint check: what can still block you

A project can be "Python" or "JS" and still fail on a locked machine.

| Risk | Where it appears | What to test first |
|------|------------------|--------------------|
| `npm install` downloads the Electron binary | Ueli, Cerebro, Bruno, electerm | `npm install electron` in an empty folder. Then `npx electron --version`. |
| Native Node modules need a C++ compiler (`node-gyp`) | Some Electron apps | Look for `node-gyp` errors during `npm install`. |
| `pip` installs prebuilt wheels with `.pyd`/`.dll` files | Glances (`psutil`), Harlequin (DuckDB), Posting (tree-sitter) | `pip install psutil` in a venv. Then run it. |
| Installer tools that are themselves binaries | `uv`, `pipx` bootstrap scripts | Use plain `pip` in a venv instead. |
| Node/Python version too new for the machine | CyberChef asks for Node 24 **(README)** | `node -v`, `python --version` |
| Tool listens on a network port | Glances web mode, mitmproxy, IT-Tools server | Bind to `127.0.0.1` only. Check company policy. |

**Test order:** (1) `python -m http.server`, (2) `pip install` of a package
with a wheel, (3) `npm install electron`. The result tells you which section
below is usable.

## 1. Static web tools (lowest risk)

These build to HTML/JS/CSS. They run in the browser. No `.exe` is created.

### IT-Tools

100+ small tools: JSON, Base64, JWT, hashes, cron, SQL format, colors.

```bash
cd it-tools
npm install
npm run build
cd dist && python -m http.server 3000   # or: npx serve dist -l 3000
```

### CyberChef

Chain operations in "recipes": encode/decode, crypto, compression, parsing,
regex, diff, timestamps, and more. All processing runs in the browser, and it
can run on a closed network **(README)**.

```bash
cd CyberChef
npm install
npm run build        # output in build/prod
cd build/prod && python -m http.server 8080
```

- License: Apache-2.0 **(README)**.
- Needs Node.js 24 per `.nvmrc` **(README)**. If your Node is older, try the
  tagged release ZIP of an older version, or `npm run build` may fail.
- If you hit out-of-memory errors, run `npm run setheapsize` first **(README)**.

### Excalidraw (whiteboard / diagrams)

- MIT. React + TypeScript, Yarn **(README)**.
- The README does not list run commands. Use the Development Guide at
  `docs.excalidraw.com/docs/introduction/development` **(check)**.

### draw.io (diagrams.net)

- Apache-2.0 for the source. Icon sets and templates have separate terms
  **(README)**.
- The README says the editor is `src/main/webapp/index.html`. A static server
  on that folder should work **(check)**.

## 2. Python tools (install with `pip` in a venv)

```bash
python -m venv .venv
.venv\Scripts\activate
pip install <package>
```

If you must work from a source ZIP, run `pip install .` in the unpacked folder.

| Tool | What it does | Notes |
|------|--------------|-------|
| [HTTPie](https://github.com/httpie/cli) | `http`/`https` commands. Readable HTTP client for APIs. BSD-3 **(README)**. | Smallest footprint. Good first install. |
| [Posting](https://github.com/darrenburns/posting) | Terminal API client, like Postman. Requests are YAML files. Apache-2.0 **(README)**. | README uses `uv`. Try `pip install posting`. Imports cURL, Postman, OpenAPI. |
| [mitmproxy](https://github.com/mitmproxy/mitmproxy) | Intercept and inspect HTTP/1, HTTP/2, WebSocket traffic. `mitmproxy`, `mitmdump`, `mitmweb`. MIT **(README)**. | Needs a trusted CA cert to read TLS. Company policy may forbid this. |
| [Harlequin](https://github.com/tconbeer/harlequin) | Terminal SQL IDE. DuckDB and SQLite built in. Postgres, MySQL via extras. MIT **(README)**. | Python 3.9+. `pip install harlequin`. Good for local CSV/Parquet via DuckDB. |
| [pgcli](https://github.com/dbcli/pgcli) | Postgres CLI with autocomplete. BSD-3 **(README)**. | Siblings: `mycli` (MySQL), `litecli` (SQLite) **(check)**. |
| [Glances](https://github.com/nicolargo/glances) | Cross-platform `top`/`htop`. Terminal, web UI, REST API. LGPL-3 **(README)**. | Python 3.10+. Windows needs `windows-curses`. `glances -w` serves on `127.0.0.1:61208`. |
| [marimo](https://github.com/marimo-team/marimo) | Reactive Python notebook. Notebooks are plain `.py` files. Apache-2.0 **(README)**. | `pip install marimo`. Cleaner diffs than Jupyter. |
| [VisiData](https://github.com/saulpw/visidata) | Terminal spreadsheet for CSV, JSON, SQLite, Excel. GPL-3 **(README)**. | README lists Windows only **with WSL**. Test before relying on it. |

Other well-known Python tools worth a look **(check, not re-verified)**:
`pre-commit` (git hook runner), `mkdocs` (docs from Markdown), `ruff`
(linter; ships a compiled wheel).

## 3. JavaScript tools

### Launchers (Electron)

Global hotkeys and tray icons need native code. Electron is the realistic
route when .NET is blocked. Test `npm install electron` first.

| Tool | Notes |
|------|-------|
| [Ueli](https://github.com/oliverschwendener/ueli) | Hotkey, file search, shell commands, calculator, bookmarks. Closest to Raycast/Alfred. Build: `npm install`, `npm run build`, `npm start`. |
| [Cerebro](https://github.com/cerebroapp/cerebro) | MIT. Electron + React. Plugin install from the search bar (`plugins <name>`). Build: `yarn --force`, `yarn package` **(README)**. README does not state Windows support or the last release date, so check repo activity. |

### Clients (Electron)

| Tool | Notes |
|------|-------|
| [Bruno](https://github.com/usebruno/bruno) | MIT. Offline API client. Collections are plain-text files in a folder, so they work with git **(README)**. README has no build steps. Read `contributing.md`. |
| [electerm](https://github.com/electerm/electerm) | MIT. SSH, SFTP, serial, RDP, VNC client. README says dev mode "may only work in Linux" and suggests Node 24 **(README)**. The web version, `electerm-web`, avoids Electron. |

### Small Node CLIs

Install with `npm install` in a project folder, then run with `npx`
**(check)**: `serve` (static file server), `http-server`,
`npm-check-updates`.

## 4. Not usable right now (.NET or native binary)

Kept here so you know why they are not in the picks.

| Tool | Why blocked |
|------|-------------|
| [DevToys](https://github.com/DevToys-app/DevToys) | .NET. Use IT-Tools or CyberChef instead. |
| [Flow Launcher](https://github.com/Flow-Launcher/Flow.Launcher) | .NET (WPF). Use Ueli or Cerebro instead. |
| [PowerToys](https://github.com/microsoft/PowerToys) | Native C++/C#. Needs an installer. |
| [ShareX](https://github.com/ShareX/ShareX) | .NET. |
| [AutoHotkey](https://github.com/AutoHotkey/AutoHotkey) | Native binary. Python `pynput` or `keyboard` can replace simple hotkeys **(check)**. |
| [Tabby](https://github.com/Eugeny/tabby) | Electron terminal. README gives no build steps; it points to `HACKING.md` **(README)**. Windows Terminal or VS Code terminal may already be enough. |

## 5. Suggested rollout

1. **Toolbox.** Build IT-Tools and CyberChef. Serve both with
   `python -m http.server`. Bookmark them.
2. **Python CLI set.** In one venv, install HTTPie, Glances, and Harlequin.
   Add Posting or mitmproxy if needed.
3. **Launcher.** Run the Electron test. If it passes, build Ueli. If it
   fails, write a small Python launcher (see below) or skip it.

### Fallback: small Python launcher

If Electron is blocked, a script can cover the core need:

- Index work folders with `os.scandir`. Keep the index in memory.
- Show a `tkinter` input box.
- Open the match with `os.startfile`.
