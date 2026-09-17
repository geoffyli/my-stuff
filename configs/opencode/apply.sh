#!/usr/bin/env bash
# Apply OpenCode config on the Linux GCP Workstation.
# Symlinks this repo's opencode config, agents, and AGENTS.md into
# ~/.config/opencode so `git pull` in the repo is the only update step.
#
# Usage:
#   ./apply.sh              # symlink config + agents + AGENTS.md
#   ./apply.sh --dry-run    # show what would be linked, change nothing
set -euo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$HERE/../.." && pwd)"
OC_DIR="$HOME/.config/opencode"

DRY=0
for a in "$@"; do
  case "$a" in
    --dry-run) DRY=1 ;;
    *) echo "Unknown arg: $a" >&2; exit 1 ;;
  esac
done

link() {
  local src="$1" dst="$2"
  if [ "$DRY" = "1" ]; then
    echo "would link: $dst -> $src"
    return
  fi
  mkdir -p "$(dirname "$dst")"
  if [ -e "$dst" ] && [ ! -L "$dst" ]; then
    cp -r "$dst" "$dst.bak.$(date +%Y%m%d%H%M%S)"
    rm -rf "$dst"
  fi
  ln -sfn "$src" "$dst"
  echo "linked: $dst -> $src"
}

echo "OpenCode config dir: $OC_DIR"
link "$HERE/opencode.json"        "$OC_DIR/opencode.json"
link "$REPO_ROOT/instructions/AGENTS.md" "$OC_DIR/AGENTS.md"
link "$REPO_ROOT/agents"          "$OC_DIR/agents"

echo "Done."
