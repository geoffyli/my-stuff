# Windows Productivity Tools (Open Source)

A short, opinionated list of open-source projects that improve daily work on
Windows. The focus is **locked-down corporate machines**: no admin rights,
AppLocker or EDR (Carbon Black, CrowdStrike) blocking unknown `.exe` files, and
no Visual Studio / .NET SDK.

The trick is to prefer tools that run as **web pages or scripts** (Node,
Python, browser) over tools that ship a new native binary.

> Research notes, not tested configs. Verify each project on the target
> machine before relying on it.

## Quick picks

| Need | Pick | Stack | Why |
|------|------|-------|-----|
| Offline developer toolbox | [IT-Tools](https://github.com/CorentinTh/it-tools) | Vue 3, TypeScript, Vite | Static site. No `.exe`. Runs in the browser. |
| App launcher / global search | [Ueli](https://github.com/oliverschwendener/ueli) | TypeScript, Electron | Closest to Raycast / Alfred on Windows. Only needs Node. |
| Launcher, native feel | [Flow Launcher](https://github.com/Flow-Launcher/Flow.Launcher) | C#, .NET (WPF) | Deepest system integration. Plugin ecosystem. |
| Toolbox, native app | [DevToys](https://github.com/DevToys-app/DevToys) | C#, .NET | Same tool set as IT-Tools, as a desktop app. |
| System utilities suite | [PowerToys](https://github.com/microsoft/PowerToys) | C++, C# | Launcher, window layouts, text extractor, and more. |
| Hotkeys and automation | [AutoHotkey](https://github.com/AutoHotkey/AutoHotkey) | AutoHotkey script | Global hotkeys, text expansion, window control. |
| Screenshots and capture | [ShareX](https://github.com/ShareX/ShareX) | C#, .NET | Region capture, annotation, screen recording. |

## 1. Developer toolbox

### IT-Tools (recommended on restricted machines)

- **What:** 100+ small tools: JSON format/validate, Base64 and URL encode, JWT
  decode, hashes, cron parser, SQL formatter, color converter.
- **Why it fits:** It is a static single-page app. All work happens in the
  browser sandbox. The build produces only HTML, JS, and CSS, so no binary
  triggers a security policy.
- **Run it locally:**

  ```bash
  # 1. Unpack the source ZIP and enter the folder
  cd it-tools

  # 2. Install dependencies and build static files
  npm install
  npm run build

  # 3. Serve the output (either one)
  npx serve dist -l 3000
  # cd dist && python -m http.server 3000
  ```

  Open `http://localhost:3000` in the browser. It works offline after the
  build. Add a bookmark.

### DevToys

Same idea as IT-Tools, packaged as a desktop app. It gives a smoother native
experience but needs the .NET SDK to build and produces executables. Use it
only when installing binaries is allowed.

## 2. Launcher and global search

Global hotkeys and a tray icon need native code. A pure script cannot do this
well, so the realistic options are:

### Ueli (Electron)

- Global hotkey, file search, shell commands, calculator, web bookmarks.
- Build needs only Node.js and npm:

  ```bash
  npm install
  npm run build
  npm start
  ```

- **Caveat:** Electron starts child processes. Some corporate policies block
  this. Test `npm start` before investing time.

### Flow Launcher

- The most polished Windows launcher. Large plugin ecosystem.
- **Caveat:** It is a .NET WPF app. It needs the .NET SDK to build from source
  and it creates `.exe` files, so it is the most likely to be blocked.

### Roll your own (fallback)

If every GUI framework is blocked, a small Python script can cover the core
need:

- Index your work folders with `os.scandir` and keep the result in memory.
- Show a minimal `tkinter` input box.
- Open the match with `subprocess.Popen` or `os.startfile`.

## 3. Other useful tools

| Tool | Use it for |
|------|------------|
| [PowerToys](https://github.com/microsoft/PowerToys) | FancyZones (window layouts), PowerToys Run (launcher), Text Extractor (OCR), Keyboard Manager. Needs install rights. |
| [AutoHotkey](https://github.com/AutoHotkey/AutoHotkey) | Remap keys, text snippets, window automation. A portable build exists, but check policy. |
| [ShareX](https://github.com/ShareX/ShareX) | Screenshots with annotation, GIF and video capture. |

## 4. Choosing by environment

| Factor | Node / web (IT-Tools) | Python script | Native .NET (DevToys, Flow) |
|--------|-----------------------|---------------|-----------------------------|
| Build dependency | `node`, `npm` | `python` | .NET SDK + desktop workload |
| Chance of being blocked | Very low (runs in browser) | Low (plain script) | Medium to high (new `.exe`) |
| Toolbox experience | Excellent | Basic (CLI-like) | Good, but larger |
| Global hotkeys | Weak | Good (via Windows APIs) | Best |

## 5. Suggested rollout

1. **Toolbox first.** Build IT-Tools, serve `dist` with
   `python -m http.server`, bookmark it. This covers most daily format and
   encode tasks with no compliance risk.
2. **Then the launcher.** Test whether Node scripts and Electron run on the
   machine. If yes, try Ueli from source. If not, use the Python fallback or
   PowerToys Run if installable.
