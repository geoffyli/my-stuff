#!/usr/bin/env python3
"""
check-links.py — Detect broken wikilinks in Markdown notes.

Scans a vault directory for [[wikilinks]] that point to non-existent notes.
Uses case-insensitive matching (consistent with how Obsidian resolves links).
Fenced code blocks are skipped so example wikilinks don't produce false positives.

Usage:
    python check-links.py <vault_dir>
    python check-links.py <vault_dir> --file <specific_note.md>
    python check-links.py <vault_dir> --summary
    python check-links.py <vault_dir> --exclude "templates/**"
    python check-links.py <vault_dir> --exclude "templates/**" --exclude "archive/**"

Exit codes:
    0 — No broken links found
    1 — Broken links found
    2 — Usage / argument error
"""

import argparse
import sys
from pathlib import Path

from _vault_utils import WIKILINK_RE
from _vault_utils import build_note_index
from _vault_utils import normalize_link_target
from _vault_utils import strip_fenced_code_blocks
from _vault_utils import strip_inline_code


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def resolve_file_arg(vault_dir: Path, raw_path: str) -> Path:
    """Resolve a file argument relative to the vault when not absolute."""
    file_path = Path(raw_path).expanduser()
    if not file_path.is_absolute():
        file_path = vault_dir / file_path
    return file_path.resolve()


def check_file(
    md_file: Path,
    note_index,
) -> list[tuple[int, str]]:
    """Return [(line_number, broken_target), ...] for broken wikilinks in this file."""
    try:
        raw = md_file.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as exc:
        print(f"  [ERROR] Cannot read {md_file}: {exc}", file=sys.stderr)
        return []

    content = strip_fenced_code_blocks(raw)
    broken: list[tuple[int, str]] = []

    for lineno, line in enumerate(content.splitlines(), start=1):
        # Strip inline code segments from the line before scanning
        line_no_inline = strip_inline_code(line)
        for m in WIKILINK_RE.finditer(line_no_inline):
            target = m.group(1)
            if normalize_link_target(target) and not note_index.has_target(target):
                broken.append((lineno, target))

    return broken


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Detect broken wikilinks in Markdown notes.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument("vault_dir", help="Path to the notes/vault directory")
    parser.add_argument(
        "--file",
        metavar="FILE",
        help="Check a single file instead of the whole vault",
    )
    parser.add_argument(
        "--summary",
        action="store_true",
        help="Print summary counts only (no per-link detail)",
    )
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

    note_index = build_note_index(vault_dir)

    if args.file:
        target_path = resolve_file_arg(vault_dir, args.file)
        if not target_path.exists():
            print(f"Error: '{target_path}' does not exist.", file=sys.stderr)
            sys.exit(2)
        files_to_check = [target_path]
    else:
        all_md = sorted(vault_dir.rglob("*.md"))
        excluded: set[Path] = set()
        for pattern in args.exclude:
            excluded.update(vault_dir.glob(pattern))
        files_to_check = [f for f in all_md if f not in excluded]

    total_files = len(files_to_check)
    files_with_issues = 0
    total_broken = 0

    print(f"Scanning {total_files} file(s) in: {vault_dir}\n")

    for md_file in files_to_check:
        broken = check_file(md_file, note_index)
        if not broken:
            continue

        files_with_issues += 1
        total_broken += len(broken)

        if not args.summary:
            try:
                rel = md_file.relative_to(vault_dir)
            except ValueError:
                rel = md_file
            print(f"  {rel}")
            for lineno, target in broken:
                print(f"    line {lineno:4d}: [[{target}]] — target not found")
            print()

    # ── Summary ──────────────────────────────────────────────────────────────
    print("─" * 60)
    if total_broken == 0:
        print(f"✓ No broken links found ({total_files} file(s) checked).")
        sys.exit(0)
    else:
        print(
            f"✗ {total_broken} broken link(s) across "
            f"{files_with_issues}/{total_files} file(s)."
        )
        sys.exit(1)


if __name__ == "__main__":
    main()
