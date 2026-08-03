<#
.SYNOPSIS
  Apply VS Code config on Windows.
.DESCRIPTION
  Merges settings.shared.json + settings.windows.json + settings.local.json
  into %APPDATA%\Code\User\settings.json, copies keybindings + snippets, and
  optionally installs the curated core extensions.
.EXAMPLE
  ./apply.ps1                # merge settings + copy keybindings/snippets
  ./apply.ps1 -Ext           # also install core extensions
  ./apply.ps1 -DryRun        # print merged settings, change nothing
#>
param(
  [switch]$Ext,
  [switch]$DryRun
)

$ErrorActionPreference = 'Stop'
$Here = Split-Path -Parent $MyInvocation.MyCommand.Path
$UserDir = Join-Path $env:APPDATA 'Code\User'

# Prefer python for a robust JSONC merge (matches macOS behavior).
$python = (Get-Command python -ErrorAction SilentlyContinue) `
  ?? (Get-Command python3 -ErrorAction SilentlyContinue)
if (-not $python) {
  throw "Python is required for the settings merge. Install it, or merge settings.shared.json + settings.windows.json manually (see WINDOWS-CHEATSHEET.md)."
}

Write-Host "VS Code User dir: $UserDir"
New-Item -ItemType Directory -Force -Path (Join-Path $UserDir 'snippets') | Out-Null

$merged = & $python.Source (Join-Path $Here 'merge_settings.py') `
  (Join-Path $Here 'settings.shared.json') `
  (Join-Path $Here 'settings.windows.json') `
  (Join-Path $Here 'settings.local.json')

if ($DryRun) {
  Write-Host "--- merged settings.json (dry run) ---"
  Write-Output $merged
} else {
  $target = Join-Path $UserDir 'settings.json'
  if (Test-Path $target) {
    Copy-Item $target "$target.bak.$(Get-Date -Format yyyyMMddHHmmss)"
  }
  Set-Content -Path $target -Value $merged -Encoding UTF8
  Copy-Item (Join-Path $Here 'keybindings.json') (Join-Path $UserDir 'keybindings.json') -Force
  Copy-Item (Join-Path $Here 'snippets\*.json') (Join-Path $UserDir 'snippets\') -Force -ErrorAction SilentlyContinue
  Write-Host "Settings, keybindings, and snippets applied."
}

if ($Ext) {
  if (-not (Get-Command code -ErrorAction SilentlyContinue)) {
    Write-Warning "'code' CLI not on PATH; skipping extensions."
  } else {
    Write-Host "Installing core extensions..."
    Get-Content (Join-Path $Here 'extensions-core.txt') |
      Where-Object { $_ -and -not $_.StartsWith('#') } |
      ForEach-Object { code --install-extension $_.Trim() --force }
    Write-Host "Extensions installed."
  }
}

Write-Host "Done."
