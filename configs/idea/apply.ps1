<#
.SYNOPSIS
  Apply curated IntelliJ IDEA config on Windows.
.DESCRIPTION
  Copies settings\* into the active JetBrains config dir under %APPDATA%.
  Backs up anything it overwrites (timestamped .bak). Never touches secrets.
.EXAMPLE
  ./apply.ps1            # copy curated settings
  ./apply.ps1 -DryRun    # show what would be copied, change nothing
#>
param([switch]$DryRun)
$ErrorActionPreference = 'Stop'
$Here = Split-Path -Parent $MyInvocation.MyCommand.Path
$Src  = Join-Path $Here 'settings'

$Base = Join-Path $env:APPDATA 'JetBrains'
$Cfg  = Get-ChildItem -Path $Base -Directory -Filter 'IntelliJIdea*' -ErrorAction SilentlyContinue |
        Sort-Object Name | Select-Object -Last 1
if (-not $Cfg) {
  throw "No IntelliJIdea config dir under $Base. Launch IDEA once, then re-run."
}
Write-Host "Target config dir: $($Cfg.FullName)"

function Copy-Curated([string]$Rel) {
  $from = Join-Path $Src $Rel
  if (-not (Test-Path $from)) { return }
  $to = Join-Path $Cfg.FullName $Rel
  if ($DryRun) { Write-Host "would copy: $Rel"; return }
  New-Item -ItemType Directory -Force -Path (Split-Path $to) | Out-Null
  if (Test-Path $to) { Copy-Item $to "$to.bak.$(Get-Date -Format yyyyMMddHHmmss)" }
  Copy-Item $from $to -Force
  Write-Host "copied: $Rel"
}

Copy-Curated 'options\editor.xml'
Copy-Curated 'templates\JavaKotlin.xml'
Copy-Curated 'codestyles\Google.xml'
Copy-Curated 'inspection\Recommended.xml'

Write-Host ""
Write-Host "Staged. Manual activation still needed for some items:"
Write-Host "  - Code style : Settings > Editor > Code Style > gear > Import Scheme > 'Google'"
Write-Host "  - Inspections: Settings > Editor > Inspections > gear > Import Profile > 'Recommended'"
Write-Host "  - Keymap     : install the 'VSCode Keymap' plugin (see plugins.md), then pick it"
Write-Host "Restart IDEA to pick up editor/template changes."
