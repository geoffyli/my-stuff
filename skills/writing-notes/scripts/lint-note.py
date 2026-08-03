#!/usr/bin/env python3
"""
lint-note.py — Validate Markdown notes against writing-notes skill formatting rules.

Checks applied per file:
  [naming]    Title Case words, no special characters, no leading digit, ≤50 chars,
              no "MOC" suffix in filename
  [frontmatter] Frontmatter integrity and wikilink quoting inside YAML; warn on missing required fields (parent, tags, related)
  [heading]   Exactly one H1, no level skipping (e.g. H2→H4), max depth H4
  [style]     Avoid trailing "Related" / "See Also" section heading
  [list]      Single space after list marker (- or N.)

Usage:
    python lint-note.py <file.md>
    python lint-note.py <vault_dir>
    python lint-note.py <vault_dir> --file <note.md>
    python lint-note.py <vault_dir> --strict   # warnings count as errors

Exit codes:
    0 — No issues (or warnings-only without --strict)
    1 — Errors found (or warnings found with --strict)
    2 — Usage / argument error
"""

import argparse
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

from _vault_utils import WIKILINK_RE
from _vault_utils import parse_frontmatter

# ---------------------------------------------------------------------------
# Patterns
# ---------------------------------------------------------------------------

import re

HEADING_RE = re.compile(r"^(#{1,6})\s+\S")

# List marker with more than one space: "- ·item" or "1. ·item" (· = extra space)
BAD_LIST_SPACING_RE = re.compile(r"^(\s*)(?:-  |\d+\.  )")

# Filename characters that are explicitly forbidden
FORBIDDEN_CHARS_RE = re.compile(r'[!@#$%^&*()\[\]{};:",<>?/\\|+=`~]')

# Small words that are allowed in lowercase (inside Title Case filenames)
LOWERCASE_EXCEPTIONS = frozenset(
    {
        "a",
        "an",
        "the",
        "and",
        "but",
        "or",
        "nor",
        "for",
        "yet",
        "so",
        "as",
        "at",
        "by",
        "in",
        "of",
        "on",
        "to",
        "up",
        "via",
        "vs",
    }
)

# Headings that indicate a trailing "Related" section (disallowed per style rules)
RELATED_HEADINGS = frozenset(
    {
        "related",
        "related notes",
        "see also",
        "further reading",
    }
)


# ---------------------------------------------------------------------------
# Data types
# ---------------------------------------------------------------------------


@dataclass
class Issue:
    level: str  # 'error' | 'warning'
    rule: str  # dotted rule identifier
    line: Optional[int]  # 1-based line number, or None for file-level issues
    message: str

    def __str__(self) -> str:
        icon = "✗" if self.level == "error" else "⚠"
        loc = f"line {self.line:4d}" if self.line is not None else "file-level"
        return f"    {icon} [{self.rule}] {loc}: {self.message}"


def resolve_file_arg(vault_dir: Path, raw_path: str) -> Path:
    """Resolve a file argument relative to the vault when not absolute."""
    file_path = Path(raw_path).expanduser()
    if not file_path.is_absolute():
        file_path = vault_dir / file_path
    return file_path.resolve()


# ---------------------------------------------------------------------------
# Individual check functions
# ---------------------------------------------------------------------------


def check_filename(stem: str) -> list[Issue]:
    issues: list[Issue] = []

    # Leading digit
    if stem and stem[0].isdigit():
        issues.append(
            Issue(
                "error",
                "naming/no-leading-digit",
                None,
                f'Filename starts with a digit: "{stem}"',
            )
        )

    # Forbidden special characters
    if FORBIDDEN_CHARS_RE.search(stem):
        bad = FORBIDDEN_CHARS_RE.findall(stem)
        issues.append(
            Issue(
                "error",
                "naming/no-special-chars",
                None,
                f'Forbidden characters in filename ({", ".join(set(bad))}): "{stem}"',
            )
        )

    # "MOC" suffix
    words = stem.split()
    if words and words[-1].upper() == "MOC":
        issues.append(
            Issue(
                "warning",
                "naming/no-moc-suffix",
                None,
                f'Filename should not end with "MOC": "{stem}"',
            )
        )

    # Length
    if len(stem) > 50:
        issues.append(
            Issue(
                "warning",
                "naming/length",
                None,
                f'Filename is {len(stem)} chars (recommended ≤50): "{stem}"',
            )
        )

    # Title Case — every word except small-word exceptions must start uppercase
    if words:
        # First word is always required to be capitalised (skip numeric words)
        if not words[0][0].isupper() and not words[0][0].isdigit():
            issues.append(
                Issue(
                    "warning",
                    "naming/title-case",
                    None,
                    f'First word of filename should be capitalised: "{stem}"',
                )
            )
        else:
            # Check subsequent words
            for w in words[1:]:
                if not w:
                    continue
                # Skip words starting with digits (years, version numbers, etc.)
                if w[0].isdigit():
                    continue
                lower_w = w.lower()
                if lower_w not in LOWERCASE_EXCEPTIONS and not w[0].isupper():
                    issues.append(
                        Issue(
                            "warning",
                            "naming/title-case",
                            None,
                            f'Word "{w}" in filename should be Title Case: "{stem}"',
                        )
                    )
                    break  # report once per file to avoid noise

    return issues


def check_frontmatter(
    parsed_frontmatter,
    all_lines: list[str],
) -> list[Issue]:
    issues: list[Issue] = []

    if not parsed_frontmatter.has_frontmatter:
        issues.append(
            Issue("warning", "frontmatter/missing", None, "No frontmatter block found")
        )
        return issues

    if not parsed_frontmatter.is_closed:
        issues.append(
            Issue(
                "error",
                "frontmatter/unclosed",
                None,
                "Frontmatter starts with `---` but has no closing delimiter",
            )
        )

    # Detect missing required fields
    for field in ("parent", "tags", "related"):
        if field not in parsed_frontmatter.fields:
            issues.append(
                Issue(
                    "warning",
                    "frontmatter/missing-field",
                    None,
                    f'Required frontmatter field missing: "{field}"',
                )
            )

    # Detect unquoted wikilinks inside YAML values
    fm_end = parsed_frontmatter.body_start
    for i, line in enumerate(all_lines[:fm_end], start=1):
        if line.rstrip() == "---":
            continue
        for wl_m in WIKILINK_RE.finditer(line):
            start = wl_m.start()
            # Check that the character before the [[ is a quote (or start of value after colon)
            prefix = line[:start]
            # If there's no quote immediately before [[, it's unquoted
            # Pattern: ": [[" or "- [[" without a surrounding quote
            before_char = prefix.rstrip()
            if before_char.endswith(":") or before_char.endswith("-"):
                # No quote wrapping — flag it
                issues.append(
                    Issue(
                        "error",
                        "frontmatter/unquoted-wikilink",
                        i,
                        f"Wikilink not quoted in YAML: {wl_m.group(0)}"
                        ' — use "[[Note Name]]"',
                    )
                )

    return issues


def check_headings(body: list[tuple[int, str]]) -> list[Issue]:
    issues: list[Issue] = []
    h1_count = 0
    prev_level = 0
    last_heading_name = ""
    last_heading_lineno: Optional[int] = None

    for lineno, line in body:
        m = HEADING_RE.match(line)
        if not m:
            continue

        level = len(m.group(1))
        heading_text = line.lstrip("#").strip()

        if level == 1:
            h1_count += 1
            if h1_count > 1:
                issues.append(
                    Issue(
                        "error",
                        "heading/single-h1",
                        lineno,
                        f'Multiple H1 headings — second H1: "{heading_text}"',
                    )
                )

        if level > 4:
            issues.append(
                Issue(
                    "error",
                    "heading/max-depth",
                    lineno,
                    f'Heading depth H{level} exceeds maximum H4: "{heading_text}"',
                )
            )

        # Level-skip: going deeper must not skip a level
        if prev_level > 0 and level > prev_level + 1:
            issues.append(
                Issue(
                    "error",
                    "heading/level-skip",
                    lineno,
                    f'Heading skips from H{prev_level} to H{level}: "{heading_text}"',
                )
            )

        prev_level = level
        last_heading_name = heading_text
        last_heading_lineno = lineno

    if h1_count == 0:
        issues.append(Issue("error", "heading/no-h1", None, "No H1 heading found"))

    # Trailing "Related" / "See Also" section
    if last_heading_name.lower() in RELATED_HEADINGS:
        issues.append(
            Issue(
                "warning",
                "style/no-related-section",
                last_heading_lineno,
                f'Trailing "{last_heading_name}" section is not allowed — '
                "use in-content wikilinks or the frontmatter `related` field",
            )
        )

    return issues


def check_list_spacing(body: list[tuple[int, str]]) -> list[Issue]:
    issues: list[Issue] = []
    for lineno, line in body:
        if BAD_LIST_SPACING_RE.match(line):
            issues.append(
                Issue(
                    "warning",
                    "list/single-space",
                    lineno,
                    "List marker should be followed by exactly one space",
                )
            )
    return issues


# ---------------------------------------------------------------------------
# Per-file entry point
# ---------------------------------------------------------------------------


def lint_file(md_file: Path) -> list[Issue]:
    issues: list[Issue] = []

    # ── Filename ─────────────────────────────────────────────────────────────
    issues.extend(check_filename(md_file.stem))

    # ── Read content ─────────────────────────────────────────────────────────
    try:
        content = md_file.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as exc:
        issues.append(Issue("error", "io/read-error", None, f"Cannot read file: {exc}"))
        return issues

    all_lines = content.splitlines()

    # ── Frontmatter ──────────────────────────────────────────────────────────
    parsed_frontmatter = parse_frontmatter(all_lines)
    issues.extend(check_frontmatter(parsed_frontmatter, all_lines))

    # ── Body checks (skip fenced code blocks) ────────────────────────────────
    body_clean = _filter_outside_fences(all_lines, parsed_frontmatter.body_start)

    issues.extend(check_headings(body_clean))
    issues.extend(check_list_spacing(body_clean))

    return issues


def _filter_outside_fences(
    all_lines: list[str],
    body_start: int,
) -> list[tuple[int, str]]:
    """Return (1-based-lineno, line) for body lines not inside fenced code blocks."""
    result: list[tuple[int, str]] = []
    in_fence = False
    fence_marker = ""
    for i, line in enumerate(all_lines[body_start:], start=body_start + 1):
        stripped = line.strip()
        if not in_fence:
            if stripped.startswith("```") or stripped.startswith("~~~"):
                in_fence = True
                fence_marker = stripped[:3]
            else:
                result.append((i, line))
        else:
            if stripped.startswith(fence_marker):
                in_fence = False
    return result


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Validate Markdown notes against writing-notes skill rules.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument("target", help="A .md file or directory to lint")
    parser.add_argument(
        "--file",
        metavar="FILE",
        help="When target is a vault directory, lint only this file within the vault",
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Treat warnings as errors (exit 1 if any warnings are found)",
    )
    args = parser.parse_args()

    target = Path(args.target).expanduser().resolve()
    if args.file:
        if not target.is_dir():
            print(
                "Error: when using --file, target must be a vault directory.",
                file=sys.stderr,
            )
            sys.exit(2)
        vault_dir = target
        target_file = resolve_file_arg(vault_dir, args.file)
        if not target_file.exists():
            print(f"Error: '{target_file}' does not exist.", file=sys.stderr)
            sys.exit(2)
        files_to_check = [target_file]
    elif target.is_file():
        files_to_check = [target]
        vault_dir = target.parent
    elif target.is_dir():
        files_to_check = sorted(target.rglob("*.md"))
        vault_dir = target
    else:
        print(f"Error: '{target}' does not exist.", file=sys.stderr)
        sys.exit(2)

    total_files = len(files_to_check)
    files_with_issues = 0
    total_errors = 0
    total_warnings = 0

    print(f"Linting {total_files} file(s)...\n")

    for md_file in files_to_check:
        issues = lint_file(md_file)
        if not issues:
            continue

        errors = [i for i in issues if i.level == "error"]
        warnings = [i for i in issues if i.level == "warning"]

        files_with_issues += 1
        total_errors += len(errors)
        total_warnings += len(warnings)

        try:
            label = str(md_file.relative_to(vault_dir))
        except ValueError:
            label = str(md_file)

        print(f"  {label}  ({len(errors)} error(s), {len(warnings)} warning(s))")
        for issue in issues:
            print(issue)
        print()

    # ── Summary ──────────────────────────────────────────────────────────────
    print("─" * 60)
    if total_errors == 0 and total_warnings == 0:
        print(f"✓ All {total_files} file(s) passed linting.")
        sys.exit(0)

    suffix = f"across {files_with_issues}/{total_files} file(s)."
    if total_errors > 0:
        print(f"✗ {total_errors} error(s), {total_warnings} warning(s) {suffix}")
        sys.exit(1)
    else:
        print(f"⚠ {total_warnings} warning(s) {suffix}")
        sys.exit(1 if args.strict else 0)


if __name__ == "__main__":
    main()
