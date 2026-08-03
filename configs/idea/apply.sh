#!/usr/bin/env bash
# Apply curated IntelliJ IDEA config on macOS/Linux.
# Copies settings/* into the active JetBrains config dir. Backs up anything it
# overwrites (timestamped .bak). Never touches secrets (see secrets.md).
#
#   ./apply.sh            # copy curated settings
#   ./apply.sh --dry-run  # show what would be copied, change nothing
set -euo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SRC="$HERE/settings"
DRY=0
[[ "${1:-}" == "--dry-run" ]] && DRY=1

# Locate newest IntelliJIdea config dir.
if [[ "$OSTYPE" == darwin* ]]; then
  BASE="$HOME/Library/Application Support/JetBrains"
else
  BASE="$HOME/.config/JetBrains"
fi
CFG="$(ls -d "$BASE"/IntelliJIdea*/ 2>/dev/null | sort | tail -1 || true)"
if [[ -z "${CFG:-}" ]]; then
  echo "No IntelliJIdea config dir under $BASE. Launch IDEA once, then re-run." >&2
  exit 1
fi
echo "Target config dir: $CFG"

copy() { # src-relative-path
  local rel="$1" from="$SRC/$1" to="$CFG/$1"
  [[ -f "$from" ]] || return 0
  if [[ $DRY -eq 1 ]]; then echo "would copy: $rel"; return 0; fi
  mkdir -p "$(dirname "$to")"
  [[ -f "$to" ]] && cp "$to" "$to.bak.$(date +%Y%m%d%H%M%S)"
  cp "$from" "$to"
  echo "copied: $rel"
}

# Curated files (codestyle/inspection/templates are imported via UI too — see README).
copy options/editor.xml
copy templates/JavaKotlin.xml

# Code styles & inspections: copy into place, but IDEA usually needs a UI import
# to activate them. We stage them so the import dialog finds them.
copy codestyles/Google.xml
copy inspection/Recommended.xml

cat <<'EOF'

Staged. Manual activation still needed for some items:
  - Code style : Settings > Editor > Code Style > gear > Import Scheme > "Google"
  - Inspections: Settings > Editor > Inspections > gear > Import Profile > "Recommended"
  - Keymap     : install the "VSCode Keymap" plugin (see plugins.md), then pick it
Restart IDEA to pick up editor/template changes.
EOF
