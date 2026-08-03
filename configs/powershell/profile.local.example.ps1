# ============================================================================
#  profile.local.ps1 TEMPLATE — machine-local overrides & secrets.
#  Copy this to profile.local.ps1 (which is GITIGNORED) and edit.
#  It is sourced at the END of profile.ps1, so it wins over defaults.
#  NEVER commit profile.local.ps1.
# ============================================================================

# --- Extra PATH entries specific to this machine ---
# $env:PATH = "C:\tools\bin;" + $env:PATH

# --- Secrets / API keys (example) ---
# $env:OPENROUTER_API_KEY = "sk-or-REPLACE_ME"

# --- Work proxy / corporate settings ---
# $env:HTTP_PROXY  = "http://proxy.corp.example:8080"
# $env:HTTPS_PROXY = "http://proxy.corp.example:8080"

# --- Any machine-specific aliases/functions ---
# Set-Alias -Name work -Value "C:\path\to\thing.exe"
