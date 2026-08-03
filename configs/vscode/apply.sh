#!/usr/bin/env bash
# Apply VS Code config on macOS / Linux.
# Merges settings.shared.json + settings.<os>.json + settings.local.json
# into the real User/settings.json, copies keybindings + snippets, and
# optionally installs the curated core extensions.
#
# Usage:
#   ./apply.sh              # merge settings + copy keybindings/snippets
#   ./apply.sh --ext        # also install core extensions
#   ./apply.sh --dry-run    # show what would be written, change nothing
set -euo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Resolve VS Code User dir per OS.
case "$(uname -s)" in
  Darwin) USER_DIR="$HOME/Library/Application Support/Code/User"; OS_FILE="settings.macos.json" ;;
  Linux)  USER_DIR="$HOME/.config/Code/User"; OS_FILE="settings.macos.json" ;;  # linux reuses macos overrides
  *) echo "Unsupported OS for apply.sh; use apply.ps1 on Windows." >&2; exit 1 ;;
esac

DRY=0; EXT=0
for a in "$@"; do
  case "$a" in
    --dry-run) DRY=1 ;;
    --ext) EXT=1 ;;
    *) echo "Unknown arg: $a" >&2; exit 1 ;;
  esac
done

command -v python3 >/dev/null || { echo "python3 required for JSON merge." >&2; exit 1; }

echo "VS Code User dir: $USER_DIR"
mkdir -p "$USER_DIR/snippets"

MERGED="$(python3 "$HERE/merge_settings.py" \
  "$HERE/settings.shared.json" \
  "$HERE/$OS_FILE" \
  "$HERE/settings.local.json")"

if [ "$DRY" = "1" ]; then
  echo "--- merged settings.json (dry run) ---"
  echo "$MERGED"
else
  # Back up existing settings once per run.
  if [ -f "$USER_DIR/settings.json" ]; then
    cp "$USER_DIR/settings.json" "$USER_DIR/settings.json.bak.$(date +%Y%m%d%H%M%S)"
  fi
  printf '%s\n' "$MERGED" > "$USER_DIR/settings.json"
  cp "$HERE/keybindings.json" "$USER_DIR/keybindings.json"
  cp "$HERE"/snippets/*.json "$USER_DIR/snippets/" 2>/dev/null || true
  echo "Settings, keybindings, and snippets applied."
fi

if [ "$EXT" = "1" ]; then
  command -v code >/dev/null || { echo "'code' CLI not on PATH; skip extensions." >&2; exit 0; }
  echo "Installing core extensions..."
  grep -v '^#' "$HERE/extensions-core.txt" | grep . | while read -r ext; do
    code --install-extension "$ext" --force
  done
  echo "Extensions installed."
fi

echo "Done."
