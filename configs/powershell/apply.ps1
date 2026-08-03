<#
.SYNOPSIS
  Apply the PowerShell profile on Windows.
.DESCRIPTION
  Copies profile.ps1 to the current PowerShell's $PROFILE (and optionally to
  BOTH PowerShell 7 and Windows PowerShell 5.1 profile paths), and optionally
  installs the modules (PSGallery) and CLI tools (winget) it depends on.
.PARAMETER Both
  Also write the profile to the *other* PowerShell edition's profile path, so
  pwsh and Windows PowerShell 5.1 share the same profile.
.PARAMETER Modules
  Install modules listed in modules.txt from the PowerShell Gallery.
.PARAMETER Tools
  Install CLI tools listed in tools.txt via winget.
.PARAMETER DryRun
  Show what would happen; change nothing.
.EXAMPLE
  ./apply.ps1                       # copy profile to current $PROFILE only
  ./apply.ps1 -Both -Modules -Tools # full setup for both PS editions
  ./apply.ps1 -DryRun               # preview
#>
param(
  [switch]$Both,
  [switch]$Modules,
  [switch]$Tools,
  [switch]$DryRun
)

$ErrorActionPreference = 'Stop'
$Here = Split-Path -Parent $MyInvocation.MyCommand.Path
$Source = Join-Path $Here 'profile.ps1'

if (-not (Test-Path $Source)) { throw "profile.ps1 not found next to apply.ps1" }

function Get-ProfilePaths {
  # Current edition's CurrentUserAllHosts profile.
  $paths = @($PROFILE.CurrentUserAllHosts)
  if ($Both) {
    $docs = [Environment]::GetFolderPath('MyDocuments')
    # The two well-known per-user profile locations.
    $paths += (Join-Path $docs 'PowerShell\profile.ps1')          # PS 7
    $paths += (Join-Path $docs 'WindowsPowerShell\profile.ps1')   # PS 5.1
  }
  $paths | Select-Object -Unique
}

# --- Copy profile ---
foreach ($dest in Get-ProfilePaths) {
  $destDir = Split-Path -Parent $dest
  if ($DryRun) {
    Write-Host "[dry-run] would copy profile.ps1 -> $dest"
    continue
  }
  New-Item -ItemType Directory -Force -Path $destDir | Out-Null
  if (Test-Path $dest) {
    Copy-Item $dest "$dest.bak.$(Get-Date -Format yyyyMMddHHmmss)"
  }
  Copy-Item $Source $dest -Force
  Write-Host "Profile written -> $dest"

  # Seed a profile.local.ps1 next to it if none exists (from the example).
  $localExample = Join-Path $Here 'profile.local.example.ps1'
  $localTarget  = Join-Path $destDir 'profile.local.ps1'
  if ((Test-Path $localExample) -and -not (Test-Path $localTarget)) {
    Copy-Item $localExample $localTarget
    Write-Host "  seeded $localTarget (edit it for machine-local secrets)"
  }
}

# --- Install modules ---
if ($Modules) {
  $modFile = Join-Path $Here 'modules.txt'
  Get-Content $modFile | Where-Object { $_ -and -not $_.TrimStart().StartsWith('#') } | ForEach-Object {
    $name = $_.Trim()
    if ($DryRun) { Write-Host "[dry-run] would Install-Module $name"; return }
    try {
      Install-Module -Name $name -Scope CurrentUser -Force -AllowClobber -ErrorAction Stop
      Write-Host "Module installed: $name"
    } catch {
      Write-Warning "Module '$name' not installed: $($_.Exception.Message)"
    }
  }
}

# --- Install tools (winget) ---
if ($Tools) {
  if (-not (Get-Command winget -ErrorAction SilentlyContinue)) {
    Write-Warning "winget not found; skipping CLI tools. Install App Installer from the Microsoft Store."
  } else {
    $toolFile = Join-Path $Here 'tools.txt'
    Get-Content $toolFile | Where-Object { $_ -and -not $_.TrimStart().StartsWith('#') } | ForEach-Object {
      $id = ($_ -split '#')[0].Trim()
      if (-not $id) { return }
      if ($DryRun) { Write-Host "[dry-run] would winget install $id"; return }
      winget install --id $id -e --source winget --accept-package-agreements --accept-source-agreements
    }
  }
}

Write-Host ""
Write-Host "Done. Open a new PowerShell to load the profile."
Write-Host "If profile scripts are blocked, run once (as your user):"
Write-Host "  Set-ExecutionPolicy -Scope CurrentUser RemoteSigned"
