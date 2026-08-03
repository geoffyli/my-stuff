#!/usr/bin/env python3
"""Shared helpers for writing-notes vault scripts."""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

WIKILINK_RE = re.compile(r"\[\[([^\]]+)\]\]")
EMPTY_FRONTMATTER_VALUES = frozenset({"", "~", "null", "Null", "NULL", '""', "''", "[]"})

# File extensions Obsidian can resolve via [[wikilink]] embeds (beyond .md)
ATTACHMENT_EXTENSIONS = frozenset(
    {
        ".svg",
        ".png",
        ".jpg",
        ".jpeg",
        ".gif",
        ".webp",
        ".bmp",
        ".pdf",
        ".mp3",
        ".mp4",
        ".webm",
        ".wav",
        ".ogg",
        ".csv",
    }
)


@dataclass(frozen=True)
class FrontmatterParseResult:
    fields: dict[str, list[str]]
    body_start: int
    has_frontmatter: bool
    is_closed: bool


@dataclass(frozen=True)
class NoteIndex:
    stem_keys: frozenset[str]
    path_keys: frozenset[str]

    def has_target(self, raw_target: str) -> bool:
        target = normalize_link_target(raw_target)
        if not target:
            return False
        return target in self.path_keys or target in self.stem_keys


def normalize_link_target(raw: str) -> str:
    """Normalize a wikilink target for case-insensitive existence checks.

    Strips anchors, aliases, known file extensions (.md and attachment types),
    and lowercases the result to match how Obsidian resolves links.
    """
    target = raw.split("#", 1)[0].split("|", 1)[0].strip().replace("\\", "/")
    lower = target.lower()
    dot = lower.rfind(".")
    if dot > 0:
        ext = lower[dot:]
        if ext == ".md" or ext in ATTACHMENT_EXTENSIONS:
            target = target[:dot]
    return target.strip("/").lower()


def strip_fenced_code_blocks(text: str) -> str:
    """Replace lines inside fenced code blocks with blank lines."""
    result: list[str] = []
    in_fence = False
    fence_marker = ""
    for line in text.splitlines(keepends=True):
        stripped = line.strip()
        if not in_fence:
            if stripped.startswith("```") or stripped.startswith("~~~"):
                in_fence = True
                fence_marker = stripped[:3]
                result.append("\n")
            else:
                result.append(line)
        else:
            if stripped.startswith(fence_marker):
                in_fence = False
            result.append("\n")
    return "".join(result)


def strip_inline_code(text: str) -> str:
    """Remove simple inline code spans to avoid false positives."""
    return re.sub(r"`[^`\n]*`", "", text)


# Directories excluded from vault indexing (internal, not user content)
_EXCLUDED_DIRS = frozenset({".obsidian", ".trash", ".git", "node_modules", ".vscode", "logseq"})


def build_note_index(vault_dir: Path) -> NoteIndex:
    """Index notes and attachment files in a single directory pass.

    Markdown files are indexed by both stem and vault-relative path (without
    extension).  Attachment files (images, SVGs, PDFs, etc.) are indexed
    identically so that ``[[diagram.svg]]`` and ``[[subfolder/diagram.svg]]``
    style embeds resolve correctly.
    """
    stem_keys: set[str] = set()
    path_keys: set[str] = set()
    for f in vault_dir.rglob("*"):
        if not f.is_file():
            continue
        # Skip files inside internal/hidden directories
        try:
            parts = f.relative_to(vault_dir).parts
        except ValueError:
            continue
        if _EXCLUDED_DIRS.intersection(parts):
            continue

        ext = f.suffix.lower()
        if ext == ".md":
            stem_keys.add(f.stem.lower())
            path_keys.add(note_path_key(f, vault_dir))
        elif ext in ATTACHMENT_EXTENSIONS:
            stem_keys.add(f.stem.lower())
            path_keys.add(f.relative_to(vault_dir).with_suffix("").as_posix().lower())

    return NoteIndex(frozenset(stem_keys), frozenset(path_keys))


def note_lookup_keys(md_file: Path, vault_dir: Path) -> set[str]:
    """Return all lookup keys that should match links to this note."""
    return {md_file.stem.lower(), note_path_key(md_file, vault_dir)}


def note_path_key(md_file: Path, vault_dir: Path) -> str:
    """Return the vault-relative note path without suffix, lowercased."""
    rel = md_file.relative_to(vault_dir)
    return rel.with_suffix("").as_posix().lower()


def extract_targets_from_text(text: str) -> set[str]:
    """Extract normalized wikilink targets from note text outside code spans."""
    clean = strip_inline_code(strip_fenced_code_blocks(text))
    targets: set[str] = set()
    for match in WIKILINK_RE.finditer(clean):
        target = normalize_link_target(match.group(1))
        if target:
            targets.add(target)
    return targets


def parse_frontmatter(lines: list[str]) -> FrontmatterParseResult:
    """Parse simple YAML frontmatter delimited by leading/trailing ---."""
    if not lines or lines[0].rstrip() != "---":
        return FrontmatterParseResult({}, 0, False, True)

    fields: dict[str, list[str]] = {}
    current_key: str | None = None
    current_lines: list[str] = []

    for index, line in enumerate(lines[1:], start=1):
        if line.rstrip() == "---":
            if current_key:
                fields[current_key] = current_lines
            return FrontmatterParseResult(fields, index + 1, True, True)

        key_match = re.match(r"^(\w+):", line)
        if key_match:
            if current_key:
                fields[current_key] = current_lines
            current_key = key_match.group(1)
            current_lines = [line]
        elif current_key:
            current_lines.append(line)

    if current_key:
        fields[current_key] = current_lines
    return FrontmatterParseResult(fields, len(lines), True, False)


def frontmatter_value(fields: dict[str, list[str]], key: str) -> str:
    """Return a scalar-ish frontmatter value for a key."""
    raw_lines = fields.get(key)
    if not raw_lines:
        return ""
    first_line = raw_lines[0]
    _, _, value = first_line.partition(":")
    if value.strip():
        return value.strip()
    for line in raw_lines[1:]:
        stripped = line.strip()
        if stripped:
            return stripped
    return ""
