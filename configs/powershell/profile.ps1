# ============================================================================
#  PowerShell profile — Windows port of the live-in-terminal (macOS zsh) setup.
#  Loaded by both PowerShell 7 (pwsh) and Windows PowerShell 5.1.
#
#  Design rules:
#   - Every external tool is GUARDED with Get-Command so a missing tool never
#     errors on shell start. Install what you want; the rest stays silent.
#   - No secrets here. Machine-local values go in profile.local.ps1 (gitignored),
#     sourced at the very end.
#   - PS7-only features are version-gated so 5.1 still loads cleanly.
# ============================================================================

# ─── PSReadLine (autosuggestions + syntax highlighting) ─────────────────────
# Replaces zsh-autosuggestions + zsh-syntax-highlighting.
if (Get-Module -ListAvailable -Name PSReadLine) {
    Import-Module PSReadLine

    # Inline predictions from history (like zsh-autosuggestions).
    Set-PSReadLineOption -PredictionSource History
    # ListView needs PSReadLine 2.2+ (ships with PS7). Guard for 5.1.
    if ($PSVersionTable.PSVersion.Major -ge 7) {
        Set-PSReadLineOption -PredictionViewStyle ListView
    }

    # Emacs-style editing + colored syntax.
    Set-PSReadLineOption -EditMode Emacs
    Set-PSReadLineOption -Colors @{ Command = 'Cyan'; Parameter = 'DarkGray' }

    # Up/Down search history by the text already typed (very zsh-like).
    Set-PSReadLineKeyHandler -Key UpArrow   -Function HistorySearchBackward
    Set-PSReadLineKeyHandler -Key DownArrow -Function HistorySearchForward
}

# ─── posh-git (git branch/status in prompt) ─────────────────────────────────
# Replaces the Oh My Zsh git plugin + robbyrussell prompt.
if (Get-Module -ListAvailable -Name posh-git) {
    Import-Module posh-git
}

# ─── Terminal-Icons (icons in Get-ChildItem listings) ───────────────────────
if (Get-Module -ListAvailable -Name Terminal-Icons) {
    Import-Module Terminal-Icons
}

# ─── EDITOR ─────────────────────────────────────────────────────────────────
if (Get-Command nvim -ErrorAction SilentlyContinue) {
    $env:EDITOR = 'nvim'
    $env:VISUAL = 'nvim'
    Set-Alias -Name vim -Value nvim
}

# ─── bat (better cat + colorized help) ──────────────────────────────────────
if (Get-Command bat -ErrorAction SilentlyContinue) {
    # `cat` in PowerShell is an alias for Get-Content; override with bat.
    Remove-Item Alias:cat -ErrorAction SilentlyContinue
    Set-Alias -Name cat -Value bat

    # Colorize --help output for any command, e.g.  `Show-Help git`
    function Show-Help {
        param([Parameter(Mandatory)] [string]$Command)
        & $Command --help 2>&1 | bat --plain --language=help
    }
    Set-Alias -Name bathelp -Value Show-Help
}

# ─── lazygit ────────────────────────────────────────────────────────────────
if (Get-Command lazygit -ErrorAction SilentlyContinue) {
    Set-Alias -Name lg -Value lazygit
}

# ─── Git shortcuts (mirror common muscle memory) ────────────────────────────
# NOTE: PowerShell ships built-in ALIASES gc=Get-Content, gp=Get-ItemProperty,
# gl=Get-Location. Aliases outrank functions in name resolution, so those
# built-ins would shadow the git functions below. Remove them first (scoped to
# this session) so the git shortcuts actually win. gs/ga/gd/glg don't collide.
if (Get-Command git -ErrorAction SilentlyContinue) {
    foreach ($__a in 'gc', 'gp', 'gl') {
        if (Test-Path "Alias:$__a") { Remove-Item "Alias:$__a" -Force }
    }
    Remove-Variable __a -ErrorAction SilentlyContinue

    function gs { git status @args }
    function ga { git add @args }
    function gc { git commit @args }
    function gp { git push @args }
    function gl { git pull @args }
    function gd { git diff @args }
    function glg { git log --oneline --graph --decorate @args }
}

# ─── Python / uv ────────────────────────────────────────────────────────────
# On Mac you alias python->python3 and pip->uv pip against a global venv.
# On Windows `python` is already the right name; only wire uv if present.
if (Get-Command uv -ErrorAction SilentlyContinue) {
    function pip  { uv pip @args }
    function pip3 { uv pip @args }
}

# ─── yazi (file manager, cd on quit) ────────────────────────────────────────
# Mirrors the `y` wrapper from .zshrc: launch yazi, and if you quit inside a
# different directory, the shell follows you there.
if (Get-Command yazi -ErrorAction SilentlyContinue) {
    function y {
        $tmp = [System.IO.Path]::GetTempFileName()
        yazi @args --cwd-file="$tmp"
        $cwd = Get-Content -Path $tmp -ErrorAction SilentlyContinue
        if ($cwd -and (Test-Path -LiteralPath $cwd) -and $cwd -ne $PWD.Path) {
            Set-Location -LiteralPath $cwd
        }
        Remove-Item -Path $tmp -ErrorAction SilentlyContinue
    }
}

# ─── zoxide (smart cd — the `z` command) ────────────────────────────────────
# Must init AFTER other functions so its `z`/`cd` shims win.
if (Get-Command zoxide -ErrorAction SilentlyContinue) {
    Invoke-Expression (& { (zoxide init powershell | Out-String) })
}

# ─── atuin (Ctrl+R history search) ──────────────────────────────────────────
# atuin's PowerShell init requires the module; guarded so absence is silent.
# Up-arrow stays on PSReadLine's history search (atuin binds Ctrl+R only).
if (Get-Command atuin -ErrorAction SilentlyContinue) {
    if (Get-Module -ListAvailable -Name atuin) {
        Import-Module atuin
        Enable-AtuinSearchKeys -CtrlR $true -UpArrow $false
    }
}

# ─── fzf (fuzzy finder) ─────────────────────────────────────────────────────
if ((Get-Command fzf -ErrorAction SilentlyContinue) -and
    (Get-Module -ListAvailable -Name PSFzf)) {
    Import-Module PSFzf
    Set-PsFzfOption -PSReadlineChordProvider 'Ctrl+t' -PSReadlineChordReverseHistory 'Ctrl+r'
}

# ─── LOCAL OVERRIDES ────────────────────────────────────────────────────────
# Machine-specific customizations (work proxies, credentials, extra PATH).
# NOT tracked in the repo — copy profile.local.example.ps1 to profile.local.ps1.
$__local = Join-Path (Split-Path -Parent $PROFILE) 'profile.local.ps1'
if (Test-Path -LiteralPath $__local) {
    . $__local
}
Remove-Variable __local -ErrorAction SilentlyContinue
