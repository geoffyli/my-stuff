#!/usr/bin/env python3
"""
find-orphans.py — Identify orphaned notes in a Markdown vault.

An orphan note is one that satisfies ALL of the following:
  1. No `parent` field in its frontmatter (or the field is empty / null)
  2. No other note in the vault links to it via a [[wikilink]]

Orphan notes are disconnected from the knowledge graph. Typical remedies:
  - Add the note to a relevant MOC under a ## Contents heading
  - Set a `parent` field in the note's frontmatter
  - Delete the note if it is no longer relevant

Usage:
    python find-orphans.py <vault_dir>
    python find-orphans.py <vault_dir> --exclude "templates/**"
    python find-orphans.py <vault_dir> --exclude "templates/**" --exclude "archive/**"

Exit codes:
    0 — No orphans found
    1 — Orphans found
    2 — Usage / argument error
"""

import argparse
import sys
from pathlib import Path

from _vault_utils import EMPTY_FRONTMATTER_VALUES
from _vault_utils import extract_targets_from_text
from _vault_utils import frontmatter_value
from _vault_utils import note_lookup_keys
from _vault_utils import parse_frontmatter


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def has_parent(content: str) -> bool:
    """Return True if the note has a non-empty parent field in its frontmatter."""
    parsed = parse_frontmatter(content.splitlines())
    if not parsed.has_frontmatter:
        return False
    raw_value = frontmatter_value(parsed.fields, "parent").strip().strip("\"'")
    return raw_value not in EMPTY_FRONTMATTER_VALUES and bool(raw_value)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Identify orphaned notes in a Markdown vault.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument("vault_dir", help="Path to the notes/vault directory")
    parser.add_argument(
        "--exclude",
        metavar="PATTERN",
        action="append",
        default=[],
        help='Glob pattern (relative to vault_dir) to exclude, e.g. "templates/**".'
        " Can be repeated.",
    )
    args = parser.parse_args()

    vault_dir = Path(args.vault_dir).expanduser().resolve()
    if not vault_dir.is_dir():
        print(f"Error: '{vault_dir}' is not a directory.", file=sys.stderr)
        sys.exit(2)

    # ── Collect all .md files, applying exclusions ───────────────────────────
    all_md = list(vault_dir.rglob("*.md"))

    excluded: set[Path] = set()
    for pattern in args.exclude:
        excluded.update(vault_dir.glob(pattern))

    files = [f for f in all_md if f not in excluded]

    # ── Load content ─────────────────────────────────────────────────────────
    contents: dict[Path, str] = {}
    for md_file in files:
        try:
            contents[md_file] = md_file.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            contents[md_file] = ""

    # ── Build set of all incoming link targets, excluding self-links ─────────
    referenced_by_others: set[str] = set()
    for md_file, text in contents.items():
        own_keys = note_lookup_keys(md_file, vault_dir)
        for target in extract_targets_from_text(text):
            if target not in own_keys:
                referenced_by_others.add(target)

    # ── Identify orphans ─────────────────────────────────────────────────────
    orphans: list[Path] = []
    for md_file in sorted(files):
        is_referenced = bool(note_lookup_keys(md_file, vault_dir) & referenced_by_others)
        has_par = has_parent(contents[md_file])
        if not is_referenced and not has_par:
            orphans.append(md_file)

    # ── Report ───────────────────────────────────────────────────────────────
    total = len(files)
    print(f"Scanned {total} note(s) in: {vault_dir}\n")

    if not orphans:
        print("✓ No orphan notes found.")
        sys.exit(0)

    print(f"Found {len(orphans)} orphan note(s):\n")
    for md_file in orphans:
        try:
            rel = md_file.relative_to(vault_dir)
        except ValueError:
            rel = md_file
        print(f"  {rel}")

    print()
    print("─" * 60)
    print(
        f"⚠ {len(orphans)} orphan(s) out of {total} note(s). "
        "Consider linking into a MOC or adding a parent field."
    )
    sys.exit(1)


if __name__ == "__main__":
    main()
