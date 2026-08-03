#!/usr/bin/env python3
"""Merge VS Code settings JSONC files. Later files override earlier ones.

Usage: merge_settings.py base.json [override.json ...]

- Strips // and /* */ comments so JSONC inputs parse.
- Top-level keys are shallow-merged (a later file's key replaces an earlier
  one wholesale) except that dict-valued keys are deep-merged one level, so
  things like "files.exclude" or "[markdown]" combine instead of clobbering.
- Missing files are skipped silently (e.g. optional settings.local.json).
- Emits pretty-printed strict JSON to stdout.
"""
import json
import re
import sys


def strip_jsonc(text: str) -> str:
    # Remove /* */ block comments.
    text = re.sub(r"/\*.*?\*/", "", text, flags=re.S)
    # Remove // line comments, but not inside strings.
    out = []
    for line in text.splitlines():
        in_str = False
        esc = False
        cut = None
        for i, ch in enumerate(line):
            if esc:
                esc = False
                continue
            if ch == "\\":
                esc = True
                continue
            if ch == '"':
                in_str = not in_str
                continue
            if not in_str and ch == "/" and i + 1 < len(line) and line[i + 1] == "/":
                cut = i
                break
        out.append(line if cut is None else line[:cut])
    text = "\n".join(out)
    # Remove trailing commas before } or ].
    text = re.sub(r",(\s*[}\]])", r"\1", text)
    return text


def load(path: str):
    try:
        with open(path, encoding="utf-8") as f:
            return json.loads(strip_jsonc(f.read()))
    except FileNotFoundError:
        return {}


def deep_merge(a: dict, b: dict) -> dict:
    result = dict(a)
    for k, v in b.items():
        if k in result and isinstance(result[k], dict) and isinstance(v, dict):
            result[k] = {**result[k], **v}
        else:
            result[k] = v
    return result


def main() -> None:
    if len(sys.argv) < 2:
        sys.exit("usage: merge_settings.py base.json [override.json ...]")
    merged: dict = {}
    for path in sys.argv[1:]:
        merged = deep_merge(merged, load(path))
    json.dump(merged, sys.stdout, indent=2, ensure_ascii=False)
    print()


if __name__ == "__main__":
    main()
