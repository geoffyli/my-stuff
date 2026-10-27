# GCW Terminal Setup (Agent Runbook)

Set up a terminal-first workflow on a Google Cloud Workstation (GCW).
The user reaches the GCW from VS Code (Remote-SSH) on a company Windows laptop.
The terminal is the VS Code integrated terminal. Ghostty is not available.

This file is written **for the coding agent on the GCW**. Follow it top to
bottom. It ports the user's macOS setup (from a private dotfiles repo) to the
GCW. All config files are inline, so you do not need that repo.

> Source setup: macOS, Ghostty, zsh + Oh My Zsh, zoxide, fzf, ripgrep, fd,
> bat, delta, yazi, lazygit, Neovim. Written 2026-10-27.

---

## 0. Rules for the agent

Read these before you run anything.

1. **No prebuilt binaries from the web.** Do not download release `.tar.gz`
   files, AppImages, or `curl | sh` installers. Build each tool from source
   with `cargo`, `go`, or `make`. Source tarballs and `git clone` are fine.
2. **No sudo.** Install everything under `$HOME`. On a GCW, only the home
   disk survives a restart. Anything outside `$HOME` can disappear.
3. **Install binaries to `~/.local/bin`.** Keep source checkouts in `~/src`.
4. **Use the company mirrors.** Package registries (crates.io, Go proxy,
   PyPI, npm) may need a company proxy or mirror. If a fetch fails, find the
   existing mirror config on the machine (`~/.cargo/config.toml`,
   `go env GOPROXY`, `pip config list`, `~/.npmrc`, env vars). If none
   exists, ask the user for the mirror URL. Do not disable TLS checks.
5. **Back up before you overwrite.** Move any existing file you replace to
   `~/.dotfiles-backup/<timestamp>/`. Never delete user files.
6. **No secrets in configs.** Put proxies, tokens, and work-only settings in
   `~/.zshrc.local`. That file is never shared.
7. **No self-updaters.** Tools must not update themselves by downloading
   binaries. The lazygit config below turns this off.
8. **No Nerd Font.** The user cannot install fonts on the Windows laptop.
   Keep icons off in every tool. Use plain Unicode and ASCII only.
9. **If a build fails, try the previous release tag** before you patch
   anything. A toolchain that is older than the tool needs is the most
   likely cause.
10. **Report at the end:** each tool, its version, and its status
    (OK / skipped / failed + reason).

---

## 1. Target state

```
$HOME
├── .local/bin/            # every built binary lands here
├── src/                   # source checkouts (safe to delete after build)
├── .oh-my-zsh/            # git clone
├── .zsh/plugins/          # zsh-autosuggestions, zsh-syntax-highlighting
├── .zshrc                 # Section 5.1
├── .zshrc.local           # machine-only settings (create empty if absent)
└── .config/
    ├── bat/config         # Section 5.2
    ├── lazygit/config.yml # Section 5.3
    ├── yazi/              # Section 5.4 (yazi.toml, keymap.toml, init.lua, theme.toml)
    └── nvim/init.lua      # Section 5.5
```

| Tool | Role | Language | Build method |
|------|------|----------|--------------|
| zsh + Oh My Zsh | Shell, prompt (`robbyrussell`), `git` plugin | shell | `git clone` |
| zsh-autosuggestions | Fish-style suggestions | shell | `git clone` |
| zsh-syntax-highlighting | Command highlighting | shell | `git clone` |
| fzf | Fuzzy finder; **Ctrl+R history** (replaces Atuin) | Go | `go install` |
| lazygit | Git TUI | Go | `go install` |
| ripgrep (`rg`) | Fast grep | Rust | `cargo install` |
| fd | Fast find | Rust | `cargo install` |
| bat | `cat` with syntax colors; man pager | Rust | `cargo install` |
| delta | Diff renderer for lazygit | Rust | `cargo install` |
| zoxide | Smart `cd` (`z`) | Rust | `cargo install` |
| yazi (+ `ya`) | File manager TUI | Rust | `git clone` + `cargo build` |
| Neovim | Editor | C | `git clone` + `make` |

Not ported on purpose:

| Mac item | Reason |
|----------|--------|
| Ghostty and its shell integration | VS Code terminal replaces it. VS Code injects its own shell integration. |
| Atuin | Out of scope. fzf Ctrl+R replaces it. History stays local. |
| Homebrew, nvm, bun, LM Studio, Antigravity, Obsidian, JDK paths | Mac-only or not needed. |
| Claude Code helpers (`cc-*`) | Not part of this setup. |
| `YAZI_ADAPTER=iterm2` | Let yazi detect the VS Code terminal itself. |

---

## 2. Preflight checks

Run these and record the output. Stop and tell the user if a **required**
item is missing.

```bash
uname -a
echo "SHELL=$SHELL"
command -v zsh git make gcc cc cargo rustc go python3 file col curl unzip
zsh --version; git --version; cargo --version; rustc --version; go version
python3 --version
cmake --version 2>/dev/null || echo "cmake: missing"
command -v nvim && nvim --version | head -1
go env GOPROXY GOBIN
cat ~/.cargo/config.toml 2>/dev/null
echo "TERM=$TERM TERM_PROGRAM=$TERM_PROGRAM COLORTERM=$COLORTERM"
df -h "$HOME"
```

| Item | Required for | If missing |
|------|--------------|-----------|
| `zsh`, `git` | everything | Stop. Ask the user. |
| `cargo`, `rustc` | rg, fd, bat, delta, zoxide, yazi | Stop. Ask the user. |
| `go` | fzf, lazygit | Stop. Ask the user. |
| `gcc`/`cc`, `make` | Neovim, some Rust crates | Skip Neovim. Report. |
| `cmake` | Neovim | `python3 -m pip install --user cmake ninja` (source build via PyPI mirror is fine). |
| `file` | yazi (MIME detection) | yazi will not preview correctly. Report. |
| `col` | bat as `MANPAGER` | Leave out the `MANPAGER` lines in `.zshrc`. |

Then create the folders:

```bash
mkdir -p ~/.local/bin ~/src ~/.zsh/plugins ~/.config
export PATH="$HOME/.local/bin:$PATH"
```

---

## 3. Build and install the tools

### 3.1 Go tools: fzf, lazygit

```bash
export GOBIN="$HOME/.local/bin"
go install github.com/junegunn/fzf@latest
go install github.com/jesseduffield/lazygit@latest
fzf --version && lazygit --version
```

- fzf must be **0.48 or newer**. The `.zshrc` uses `fzf --zsh`.
- If the local Go is too old for `@latest`, install an older tag
  (for example `@v0.xx.y`) that matches the `go` line in that tag's `go.mod`.

### 3.2 Rust tools: ripgrep, fd, bat, delta, zoxide

```bash
cargo install --locked --root "$HOME/.local" ripgrep
cargo install --locked --root "$HOME/.local" fd-find
cargo install --locked --root "$HOME/.local" bat
cargo install --locked --root "$HOME/.local" git-delta
cargo install --locked --root "$HOME/.local" zoxide
rg --version; fd --version; bat --version; delta --version; zoxide --version
```

- `--root "$HOME/.local"` puts binaries in `~/.local/bin`.
- **bat must be 0.25 or newer.** Older versions do not bundle the
  `Catppuccin Mocha` theme. Check with `bat --list-themes | grep -i catppuccin`.
- If crates.io is blocked, set up source replacement to the company mirror in
  `~/.cargo/config.toml`. Ask the user for the URL if you cannot find it.
- If `rustc` is too old for the newest crate, pin an older version:
  `cargo install --locked --version <x.y.z> ...`. Check the crate's
  `rust-version` field.

### 3.3 yazi

The config in Section 5.4 needs **yazi 25.5 or newer** (it uses `[mgr]` and
`ya pkg`). The user runs 26.1.x on the Mac.

```bash
cd ~/src
git clone https://github.com/sxyazi/yazi.git
cd yazi
git tag --sort=-creatordate | head -5    # pick the newest release tag
git checkout <newest-tag>
cargo build --release --locked
cp target/release/yazi target/release/ya ~/.local/bin/
yazi --version; ya --version
```

- If the build fails because `rustc` is too old, try the previous tag, but
  stay at 25.5 or newer. If no tag fits, stop and report the `rustc` version.
- Do not run `rustup update` if it would download prebuilt toolchains. Ask
  the user first.
- Optional preview helpers (skip if not present, do not build): `ffmpeg`,
  `7z`, `jq`, `pdftoppm`, ImageMagick. yazi still works without them.

### 3.4 Neovim

Skip this section if `nvim --version` already shows **0.10 or newer**.

```bash
cd ~/src
git clone https://github.com/neovim/neovim.git
cd neovim
git checkout stable
make CMAKE_BUILD_TYPE=Release CMAKE_INSTALL_PREFIX="$HOME/.local"
make install
nvim --version | head -1
```

- The build downloads bundled dependencies (LuaJIT, libuv, and others) as
  **source** tarballs from GitHub. That is allowed.
- If `gettext`/`msgfmt` is missing, the build may stop on translations. Add
  `CMAKE_EXTRA_FLAGS="-DENABLE_TRANSLATIONS=OFF"` to the first `make` command.
- If `make` cannot find `cmake`, make sure `~/.local/bin` (pip `--user`
  scripts) is on `PATH`.

### 3.5 Oh My Zsh and zsh plugins

Use `git clone`. Do **not** run the Oh My Zsh `curl | sh` installer, because
it rewrites `~/.zshrc`.

```bash
git clone --depth 1 https://github.com/ohmyzsh/ohmyzsh.git ~/.oh-my-zsh
git clone --depth 1 https://github.com/zsh-users/zsh-autosuggestions ~/.zsh/plugins/zsh-autosuggestions
git clone --depth 1 https://github.com/zsh-users/zsh-syntax-highlighting ~/.zsh/plugins/zsh-syntax-highlighting
```

---

## 4. Back up existing dotfiles

```bash
TS=$(date +%Y%m%d-%H%M%S); BK="$HOME/.dotfiles-backup/$TS"; mkdir -p "$BK"
for p in .zshrc .config/bat .config/lazygit .config/yazi .config/nvim; do
  [ -e "$HOME/$p" ] && mkdir -p "$BK/$(dirname "$p")" && mv "$HOME/$p" "$BK/$p"
done
touch ~/.zshrc.local
echo "Backup: $BK"
```

If `~/.zshrc` already has company settings (proxy, SDK paths, internal
tools), copy those lines into `~/.zshrc.local`. Tell the user what you moved.

---

## 5. Config files

Write each file exactly as shown. Comments mark every change from the Mac.

### 5.1 `~/.zshrc`

```zsh
# ─── XDG ─────────────────────────────────────────────────────────────────────
export XDG_CONFIG_HOME="$HOME/.config"

# ─── PATH ────────────────────────────────────────────────────────────────────
# GCW: all tools are built into ~/.local/bin (no Homebrew).
export PATH="$HOME/.local/bin:$PATH"
[ -f "$HOME/.cargo/env" ] && . "$HOME/.cargo/env"

# ─── OH MY ZSH ───────────────────────────────────────────────────────────────
export ZSH="$HOME/.oh-my-zsh"
ZSH_THEME="robbyrussell"
plugins=(git)
[ -f "$ZSH/oh-my-zsh.sh" ] && source "$ZSH/oh-my-zsh.sh"

# ─── BAT ─────────────────────────────────────────────────────────────────────
# Colorized man pages via bat (needs `col`; remove these two lines if missing)
export MANPAGER="sh -c 'col -bx | bat -l man -p'"
export MANROFFOPT="-c"

# Colorize --help output for any command: e.g. `help cargo`
alias bathelp='bat --plain --language=help'
help() { "$@" --help 2>&1 | bathelp; }

# ─── ALIASES ─────────────────────────────────────────────────────────────────
alias lg='lazygit'

# ─── EDITOR ──────────────────────────────────────────────────────────────────
export EDITOR="nvim"
export VISUAL="nvim"

# ─── FZF ─────────────────────────────────────────────────────────────────────
# GCW: replaces Atuin. Ctrl+R = history search, Ctrl+T = file picker,
# Alt+C = cd into a sub-directory.
if command -v fzf &>/dev/null; then
  source <(fzf --zsh)
  export FZF_DEFAULT_COMMAND='fd --type f --hidden --exclude .git'
  export FZF_CTRL_T_COMMAND="$FZF_DEFAULT_COMMAND"
  export FZF_ALT_C_COMMAND='fd --type d --hidden --exclude .git'
  export FZF_DEFAULT_OPTS='--height 40% --layout=reverse --border'
fi

# Bigger shared history (Atuin used to cover this)
HISTSIZE=100000
SAVEHIST=100000
setopt SHARE_HISTORY HIST_IGNORE_DUPS HIST_IGNORE_SPACE

# ─── YAZI ────────────────────────────────────────────────────────────────────
# GCW: no YAZI_ADAPTER pin. yazi detects the VS Code terminal itself.
# y wrapper: change directory on quit
function y() {
  local tmp cwd
  tmp="$(mktemp -t "yazi-cwd.XXXXXX")"
  command yazi "$@" --cwd-file="$tmp"
  IFS= read -r -d '' cwd < "$tmp"
  [ "$cwd" != "$PWD" ] && [ -d "$cwd" ] && builtin cd -- "$cwd"
  rm -f -- "$tmp"
}

# ─── ZOXIDE ──────────────────────────────────────────────────────────────────
command -v zoxide &>/dev/null && eval "$(zoxide init zsh)"

# ─── LOCAL OVERRIDES ─────────────────────────────────────────────────────────
# Company proxies, SDK paths, and secrets go here. Not shared.
[ -f "$HOME/.zshrc.local" ] && source "$HOME/.zshrc.local"

# ─── ZSH PLUGINS ─────────────────────────────────────────────────────────────
# Load order matters: autosuggestions first, syntax-highlighting LAST.
[ -f "$HOME/.zsh/plugins/zsh-autosuggestions/zsh-autosuggestions.zsh" ] && \
  source "$HOME/.zsh/plugins/zsh-autosuggestions/zsh-autosuggestions.zsh"
[ -f "$HOME/.zsh/plugins/zsh-syntax-highlighting/zsh-syntax-highlighting.zsh" ] && \
  source "$HOME/.zsh/plugins/zsh-syntax-highlighting/zsh-syntax-highlighting.zsh"
```

### 5.2 `~/.config/bat/config`

Same as the Mac. No changes needed.

```
--theme="Catppuccin Mocha"
--style="numbers,changes,header,grid,snip"
--paging=auto
--pager="less -RFX"
--italic-text=always
--tabs=4
--wrap=auto
--map-syntax "*.conf:INI"
--map-syntax "*.env:DotENV"
--map-syntax "*.zshrc:Bash"
--map-syntax "*.bashrc:Bash"
--map-syntax "*.zprofile:Bash"
--map-syntax "*Dockerfile*:Dockerfile"
```

### 5.3 `~/.config/lazygit/config.yml`

Changes from the Mac: icons off, `open` replaced with `$BROWSER`, generic
remote URL for the "open in browser" command, self-update off.

```yaml
gui:
  sidePanelWidth: 0.3333
  mainPanelSplitMode: flexible
  scrollHeight: 3
  scrollPastBottom: true
  scrollOffMargin: 3
  # GCW: no Nerd Font on the client → icons off
  nerdFontsVersion: ""
  showFileTree: true
  showFileIcons: false
  showCommandLog: true
  commandLogSize: 8
  showBottomLine: true
  border: rounded
  filterMode: fuzzy
  mouseEvents: true
  skipDiscardChangeWarning: false
  skipStashWarning: false
  skipAmendWarning: false
  skipRewordInEditorWarning: false
  branchColorPatterns:
    "^(main|master)$": "green"
    "^feat/":          "yellow"
    "^fix/":           "red"
    "^chore/":         "cyan"
    "^docs/":          "blue"

theme:
  activeBorderColor:         [green, bold]
  inactiveBorderColor:       [default]
  selectedLineBgColor:       [blue]
  selectedRangeBgColor:      [blue]
  optionsTextColor:          [blue]
  cherryPickedCommitBgColor: [cyan]
  cherryPickedCommitFgColor: [blue]
  unstagedChangesColor:      [red]

git:
  paging:
    colorArg: always
    pager: delta --dark --paging=never --line-numbers
    useConfig: false
  autoFetch: true
  fetchAll: true
  autoRefresh: true
  autoForwardBranches: onlyMainBranches
  log:
    order: topo-order
    showGraph: when-maximised
  localBranchSortOrder: recency
  diffContextSize: 5
  autoStageResolvedConflicts: true
  mainBranches: [main, master]
  skipHookPrefix: "WIP"

commit:
  signOff: false
  autoWrapCommitMessage: true
  autoWrapWidth: 72

os:
  edit: "nvim {{filename}}"
  editAtLine: "nvim +{{line}} {{filename}}"
  editAtLineAndWait: "nvim +{{line}} {{filename}}"
  # GCW: VS Code Remote sets $BROWSER to a helper that opens the URL on the
  # Windows client.
  openLink: '"$BROWSER" {{link}}'

customCommands:
  # Open the repo's web page. Converts git@host:org/repo.git → https://host/org/repo
  - key: "O"
    context: "global"
    command: |
      url=$(git remote get-url origin | sed -E 's#^git@([^:]+):#https://\1/#; s#^ssh://([^@]+@)?([^/:]+)(:[0-9]+)?/#https://\2/#; s#\.git$##')
      "$BROWSER" "$url"
    description: "Open repo in browser"
    output: none

# GCW: never self-update (it downloads prebuilt binaries)
update:
  method: never

notARepository: prompt
```

If `$BROWSER` is empty in the VS Code terminal, keep the config. Tell the user
that `O` and link opening will not work there.

### 5.4 yazi: `~/.config/yazi/`

Changes from the Mac: openers use `nvim` and `code` instead of macOS `open`,
icons off, jump keys point at Linux paths.

**`yazi.toml`**

```toml
[mgr]
ratio          = [1, 4, 3]
sort_by        = "natural"
sort_dir_first = true
show_hidden    = true
show_symlink   = true
scrolloff      = 8
linemode       = "mtime"

[preview]
wrap          = "yes"
image_delay   = 80
image_filter  = "lanczos3"
image_quality = 75
max_width     = 1000
max_height    = 1000

[[plugin.prepend_fetchers]]
id  = "git"
url = "*"
run = "git"

[[plugin.prepend_fetchers]]
id  = "git"
url = "*/"
run = "git"

# GCW: no macOS `open`. Edit in Neovim; "open" sends the file to the
# VS Code editor window via the `code` CLI that Remote-SSH provides.
[opener]
edit = [
  { run = "nvim %s", block = true, desc = "Edit with Neovim" },
]
open = [
  { run = "code %s", orphan = true, desc = "Open in VS Code" },
]

[open]
prepend_rules = [
  { mime = "text/*", use = "edit" },
  { url = "*.md",    use = "edit" },
  { url = "*.json",  use = "edit" },
  { url = "*.yaml",  use = "edit" },
  { url = "*.yml",   use = "edit" },
]
```

**`theme.toml`** (new on GCW: turns icons off)

```toml
# No Nerd Font on the client. Empty icon rules = no icon glyphs.
[icon]
globs = []
dirs  = []
files = []
exts  = []
conds = []
```

If icons still show as boxes after this, check the yazi docs for the current
icon keys in `theme.toml` for the installed version, and fix this file.

**`init.lua`**

```lua
require("full-border"):setup {
  type = ui.Border.ROUNDED,
}

require("git"):setup {
  order = 1500,
}

require("smart-enter"):setup {
  open_multi = true,
}
```

**`keymap.toml`**

Ask the user which folder holds their repos. Use it for `g p`. If they do not
answer, use `~/projects` if it exists, else remove the `g p` block.

```toml
[[mgr.prepend_keymap]]
on   = "l"
run  = "plugin smart-enter"
desc = "Enter directory or open file"

[[mgr.prepend_keymap]]
on   = "T"
run  = "plugin toggle-pane min-preview"
desc = "Show or hide the preview pane"

[[mgr.prepend_keymap]]
on   = "<Tab>"
run  = "plugin toggle-pane max-preview"
desc = "Maximize or restore the preview pane"

[[mgr.prepend_keymap]]
on   = "!"
run  = 'shell "$SHELL" --block'
desc = "Open shell here"

[[mgr.prepend_keymap]]
on   = ["g", "h"]
run  = "cd ~"
desc = "Go home"

[[mgr.prepend_keymap]]
on   = ["g", "p"]
run  = "cd ~/projects"   # GCW: replace with the user's repo root
desc = "Go projects"

[[mgr.prepend_keymap]]
on   = "z"
run  = "cd --zoxide"
desc = "Jump with zoxide"

[[mgr.prepend_keymap]]
on   = ["g", "l"]
run  = "plugin lazygit"
desc = "Open lazygit"
```

**Plugins.** Install with `ya pkg` (it uses `git clone` from GitHub). This
writes `package.toml` and `plugins/`:

```bash
ya pkg add yazi-rs/plugins:git
ya pkg add yazi-rs/plugins:smart-enter
ya pkg add yazi-rs/plugins:full-border
ya pkg add yazi-rs/plugins:toggle-pane
ya pkg add Lil-Dank/lazygit
ya pkg list
```

`Lil-Dank/lazygit` is new on GCW. The Mac keymap binds `g l` to it, but the
Mac never installed it.

### 5.5 `~/.config/nvim/init.lua`

Change from the Mac: a clipboard block (OSC 52). Over SSH there is no system
clipboard. OSC 52 sends yanks to the Windows clipboard through the terminal.

```lua
-- 1. LEADER
vim.g.mapleader = " "
vim.g.maplocalleader = " "

-- 2. OPTIONS
vim.opt.number = true
vim.opt.relativenumber = true
vim.opt.tabstop = 4
vim.opt.shiftwidth = 4
vim.opt.expandtab = true
vim.opt.smartindent = true
vim.opt.wrap = false
vim.opt.termguicolors = true
vim.opt.scrolloff = 8
vim.opt.signcolumn = "yes"
vim.opt.cursorline = true
vim.opt.splitright = true
vim.opt.splitbelow = true
vim.opt.ignorecase = true
vim.opt.smartcase = true
vim.opt.hlsearch = true
vim.opt.incsearch = true
vim.opt.clipboard = "unnamedplus"
vim.opt.undofile = true
vim.opt.updatetime = 250
vim.opt.timeoutlen = 300

-- GCW: clipboard over SSH via OSC 52 (copy only).
-- Paste comes from Neovim's own register; use Ctrl+V in the terminal to
-- paste from Windows. Reading the clipboard via OSC 52 can hang, so it is
-- not used.
if vim.env.SSH_TTY or vim.env.TERM_PROGRAM == "vscode" then
  local ok, osc52 = pcall(require, "vim.ui.clipboard.osc52")
  if ok then
    local function paste()
      return { vim.fn.split(vim.fn.getreg(""), "\n"), vim.fn.getregtype("") }
    end
    vim.g.clipboard = {
      name = "OSC 52 (copy only)",
      copy = { ["+"] = osc52.copy("+"), ["*"] = osc52.copy("*") },
      paste = { ["+"] = paste, ["*"] = paste },
    }
  end
end

-- 3. KEYMAPS
vim.keymap.set("n", "<leader>nh", ":nohl<CR>", { desc = "Clear search highlights" })
vim.keymap.set("n", "<C-h>", "<C-w>h", { desc = "Go to left window" })
vim.keymap.set("n", "<C-j>", "<C-w>j", { desc = "Go to lower window" })
vim.keymap.set("n", "<C-k>", "<C-w>k", { desc = "Go to upper window" })
vim.keymap.set("n", "<C-l>", "<C-w>l", { desc = "Go to right window" })
vim.keymap.set("n", "<C-d>", "<C-d>zz")
vim.keymap.set("n", "<C-u>", "<C-u>zz")
vim.keymap.set("i", "jk", "<ESC>", { desc = "Exit insert mode with jk" })
vim.keymap.set("n", "<A-j>", ":m .+1<CR>==", { desc = "Move line down" })
vim.keymap.set("n", "<A-k>", ":m .-2<CR>==", { desc = "Move line up" })

-- 4. PLUGINS (lazy.nvim, cloned from GitHub on first launch)
local lazypath = vim.fn.stdpath("data") .. "/lazy/lazy.nvim"
if not (vim.uv or vim.loop).fs_stat(lazypath) then
  vim.fn.system({
    "git", "clone", "--filter=blob:none",
    "https://github.com/folke/lazy.nvim.git",
    "--branch=stable", lazypath,
  })
end

if not (vim.uv or vim.loop).fs_stat(lazypath) then
  vim.notify("lazy.nvim not found — run nvim again to retry the bootstrap", vim.log.levels.WARN)
else
  vim.opt.rtp:prepend(lazypath)
  require("lazy").setup({
    {
      "kdheepak/lazygit.nvim",
      lazy = true,
      cmd = {
        "LazyGit",
        "LazyGitConfig",
        "LazyGitCurrentFile",
        "LazyGitFilter",
        "LazyGitFilterCurrentFile",
      },
      dependencies = { "nvim-lua/plenary.nvim" },
      keys = {
        { "<leader>lg", "<cmd>LazyGit<cr>", desc = "LazyGit" },
      },
      config = function()
        vim.g.lazygit_floating_window_scaling_factor = 0.9
        vim.g.lazygit_floating_window_winblend = 0
      end,
    },
  }, {
    -- GCW: no Nerd Font → plain ASCII icons in the lazy.nvim UI
    ui = {
      icons = {
        cmd = "cmd", config = "cfg", event = "evt", ft = "ft", init = "init",
        keys = "keys", plugin = "plug", runtime = "rt", require = "req",
        source = "src", start = "start", task = "task", lazy = "lazy",
      },
    },
  })
end
```

Then install the plugins headless:

```bash
nvim --headless "+Lazy! sync" +qa
```

---

## 6. Make zsh the VS Code terminal shell

The login shell on a GCW is often bash. `chsh` may need sudo, and
`/etc/passwd` changes may not survive a restart. Use the VS Code remote
setting instead.

1. Find the zsh path: `command -v zsh`.
2. Edit `~/.vscode-server/data/Machine/settings.json` on the GCW. Create it if
   it does not exist. Merge these keys (keep other keys):

   ```json
   {
     "terminal.integrated.profiles.linux": {
       "zsh": { "path": "/usr/bin/zsh", "args": ["-l"] }
     },
     "terminal.integrated.defaultProfile.linux": "zsh"
   }
   ```

   Replace `/usr/bin/zsh` with the real path from step 1.
3. Tell the user to open a **new** VS Code terminal (or reload the window).

Optional fallback for plain `ssh` sessions. Add it only if the user agrees.
Put it at the **end** of `~/.bashrc`:

```bash
# Switch interactive bash sessions to zsh (GCW terminal setup)
if [[ $- == *i* ]] && [ -z "$ZSH_VERSION" ] && command -v zsh >/dev/null && [ -z "$NO_AUTO_ZSH" ]; then
  exec zsh -l
fi
```

---

## 7. Verify

Run each check in a **new** zsh terminal. Report the results as a table.

```bash
for t in zsh fzf lazygit rg fd bat delta zoxide yazi ya nvim; do
  printf "%-8s %s\n" "$t" "$(command -v $t >/dev/null && $t --version 2>/dev/null | head -1 || echo MISSING)"
done
echo "$SHELL / $ZSH_VERSION"
bat --list-themes | grep -q "Catppuccin Mocha" && echo "bat theme OK"
ya pkg list
nvim --headless "+checkhealth lazy" +qa 2>&1 | tail -5
zsh -i -c 'echo zsh-startup-OK' 2>&1 | tail -3
```

Manual checks for the user (list them in your report):

| Check | Expected |
|-------|----------|
| Type `git sta` | Grey suggestion appears (autosuggestions). Command is colored (syntax highlighting). |
| Ctrl+R | fzf history list opens. |
| Ctrl+T | fzf file picker opens. |
| `z <dir>` after visiting it once | Jumps to that folder. |
| `y`, then `q` in another folder | Shell `cd`s to that folder. |
| In yazi: `g l` | lazygit opens. |
| In yazi: `o` on a non-text file | File opens in the VS Code editor. |
| `lg`, then a diff | Diff is rendered by delta with line numbers. |
| `man ls` | Colored man page. |
| In nvim: `yy`, then Ctrl+V in Windows Notepad | Line is pasted (OSC 52 works). |
| No boxes or `?` glyphs in yazi, lazygit, nvim | Icons are off. |

---

## 8. For the user: VS Code settings on the Windows laptop

The agent on the GCW cannot change these. They live in the Windows VS Code
**User** settings. They stop VS Code from taking keys that the shell, fzf,
and Neovim need.

```jsonc
{
  // Ctrl+K is a VS Code chord prefix. Send it to the terminal (nvim <C-k>).
  "terminal.integrated.allowChords": false,

  // Alt+j / Alt+k in nvim: stop Alt from focusing the menu bar.
  "window.enableMenuBarMnemonics": false,
  "window.customMenuBarAltFocus": false,

  // Let VS Code draw inline images (yazi image preview).
  "terminal.integrated.enableImages": true,

  // No Nerd Font: use a plain monospace font.
  "terminal.integrated.fontFamily": "'Cascadia Mono', Consolas, monospace",

  "terminal.integrated.scrollback": 10000,

  // Send these keys to the shell when the terminal has focus.
  // Each "-<command>" removes that command from the skip list.
  "terminal.integrated.commandsToSkipShell": [
    "-workbench.action.quickOpen",       // Ctrl+P: previous history line, Ctrl+E: end of line
    "-workbench.action.togglePanel",     // Ctrl+J: nvim window down
    "-workbench.action.toggleSidebarVisibility" // Ctrl+B: back one char
  ]
}
```

Notes:

- Test each shortcut in the terminal first. Add an entry only if VS Code
  takes the key. To find the command name, open **Keyboard Shortcuts**
  (Ctrl+K Ctrl+S) and search for the key.
- If too many keys conflict, use `"terminal.integrated.sendKeybindingsToShell": true`.
  This sends almost all keys to the shell. The cost: most VS Code shortcuts
  stop working while the terminal has focus. F1 still opens the command
  palette.
- These keys are already in `configs/vscode/settings.windows.json` in the
  `my-stuff` repo. On Windows, run `configs/vscode/apply.ps1` to apply them.

---

## 9. Troubleshooting

| Symptom | Likely cause | Fix |
|---------|--------------|-----|
| `cargo install` cannot reach crates.io | No mirror configured | Add source replacement in `~/.cargo/config.toml`. Ask the user for the mirror URL. |
| `error: package requires rustc 1.xx` | Toolchain too old | Pin an older crate version or yazi tag. |
| `go: go.mod requires go >= 1.xx` | Go too old | Use an older tag of fzf or lazygit. Or let `GOTOOLCHAIN=auto` fetch a newer Go **only if** the Go proxy serves it. |
| Ctrl+R opens a VS Code dialog | VS Code takes the key | Section 8. |
| Boxes or `?` in yazi | Icons still on | Check `theme.toml` (5.4). |
| yazi shows no image previews | VS Code images off, or no image adapter | Set `terminal.integrated.enableImages`. It is cosmetic. Skip if it still fails. |
| `nvim` yank does not reach Windows | Terminal ignores OSC 52 | Use a VS Code selection + Ctrl+C. Report it. |
| New terminal is still bash | Machine settings not applied | Reload the VS Code window. Check the zsh path in Section 6. |
| Tools gone after a GCW restart | Installed outside `$HOME` | Reinstall under `~/.local`. |

---

## 10. Updating later

Re-run the build commands in Section 3 with newer versions:

- `go install <module>@latest`
- `cargo install --locked --root "$HOME/.local" <crate>` (add `--force` to rebuild)
- `git pull` + rebuild in `~/src/yazi` and `~/src/neovim`
- `git -C ~/.oh-my-zsh pull`, and the same in each `~/.zsh/plugins/*` folder
- `ya pkg upgrade`, then `nvim "+Lazy sync"`
