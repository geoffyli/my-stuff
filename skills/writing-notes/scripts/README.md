# Writing Notes — Scripts

Utility scripts for validating and auditing Markdown note vaults.  
All scripts are **pure Python 3 stdlib** — no external dependencies to install.

---

## Scripts at a glance

| Script | Purpose | Run frequency |
|--------|---------|---------------|
| [`check-links.py`](#check-linkspy) | Detect broken `[[wikilinks]]` | After writing or editing any note |
| [`lint-note.py`](#lint-notepy) | Validate note formatting rules | Before delivering a new note |
| [`find-orphans.py`](#find-orphanspy) | Find disconnected notes | After vault reorganisation |

---

## check-links.py

Scans for `[[wikilinks]]` that point to non-existent notes or attachment files.  
Uses **case-insensitive matching** (same as Obsidian), supports both bare note names and folder-qualified links such as `[[AI/Transformers]]`, and skips fenced/inline code to avoid false positives on examples.

**Attachment support:** Links to non-Markdown files (`.svg`, `.png`, `.jpg`, `.jpeg`, `.gif`, `.webp`, `.bmp`, `.pdf`, `.mp3`, `.mp4`, `.webm`, `.wav`, `.ogg`, `.csv`) are also resolved. This means `[[diagram.svg]]` or `![[photo.png]]` embeds are validated against actual files in the vault. Internal directories (`.obsidian`, `.trash`, `.git`) are excluded from indexing.

```bash
# Check the whole vault
python check-links.py /path/to/vault

# Check a single file only
python check-links.py /path/to/vault --file /path/to/vault/My Note.md

# Print counts only (no per-link detail)
python check-links.py /path/to/vault --summary
```

**Output example:**
```
Scanning 42 file(s) in: /path/to/vault

  Machine Learning.md
    line   14: [[Gradient Descent]] — target not found
    line   27: [[Backpropagation]]  — target not found

────────────────────────────────────────────────────────────
✗ 2 broken link(s) across 1/42 file(s).
```

**Exit codes:** `0` = clean · `1` = broken links found · `2` = usage error  
**Rule enforced:** [Wikilink Integrity](../references/contents-organizing.md#wikilink-integrity) — *"Every wikilink must point to an existing note."*

---

## lint-note.py

Validates a note (or all notes in a vault) against the formatting rules defined in  
[`references/markdown-formatting.md`](../references/markdown-formatting.md).

Default philosophy: this is a **correctness-first** linter. Hard failures are reserved for invalid structure or misleading syntax. Stylistic recommendations remain warnings unless `--strict` is used.

Checks performed:

| Category | Rule |
|----------|------|
| **Naming** | Title Case words (numeric words like years are skipped), no forbidden special chars, no leading digit, ≤ 50 chars, no "MOC" suffix |
| **Frontmatter** | Warn if frontmatter is missing; error on unclosed frontmatter or unquoted wikilinks inside YAML |
| **Headings** | Error on missing/multiple H1, level-skipping (e.g. H2 → H4), or depth beyond H4 |
| **Style** | Warn on trailing "Related" / "See Also" section heading |
| **Lists** | Warn on list markers with more than one trailing space |

```bash
# Lint a single note
python lint-note.py /path/to/vault/My Note.md

# Lint a single note relative to a vault
python lint-note.py /path/to/vault --file "My Note.md"

# Lint all notes in the vault
python lint-note.py /path/to/vault

# Treat warnings as errors (stricter gate)
python lint-note.py /path/to/vault --strict
```

**Output example:**
```
Linting 1 file(s)...

  My Note.md  (2 error(s), 1 warning(s))
    ✗ [frontmatter/unclosed]  file-level: Frontmatter starts with `---` but has no closing delimiter
    ✗ [heading/level-skip]   line   18: Heading skips from H2 to H4: "Deep Dive"
    ⚠ [naming/length]       file-level: Filename is 53 chars (recommended ≤50)

────────────────────────────────────────────────────────────
✗ 2 error(s), 1 warning(s) across 1/1 file(s).
```

**Exit codes:** `0` = clean · `1` = errors (or warnings with `--strict`) · `2` = usage error

---

## find-orphans.py

Identifies notes that are **disconnected from the knowledge graph** — they have no  
incoming `[[wikilinks]]` from other notes AND no `parent` field set in their frontmatter.

Self-links do not count, folder-qualified links do count, and `parent:` text in the note body does not count.

```bash
# Check the whole vault
python find-orphans.py /path/to/vault

# Exclude templates and archive folders
python find-orphans.py /path/to/vault --exclude "templates/**" --exclude "archive/**"
```

**Output example:**
```
Scanned 42 note(s) in: /path/to/vault

Found 2 orphan note(s):

  Scratch Ideas.md
  Old Experiment.md

────────────────────────────────────────────────────────────
⚠ 2 orphan(s) out of 42 note(s). Consider linking into a MOC or adding a parent field.
```

**Exit codes:** `0` = no orphans · `1` = orphans found · `2` = usage error  
**Typical remedies:**
- Add the note to a MOC under `## Contents`
- Set `parent: "[[Parent Note]]"` in the note's frontmatter
- Delete the note if it is no longer relevant (confirm with user first)

---

## Agent usage patterns

### After writing a new note

```bash
# 1. Validate formatting (--strict treats warnings as errors before delivery)
python lint-note.py /vault --file "New Note.md" --strict

# 2. Verify all wikilinks in the new note resolve
python check-links.py /vault --file "New Note.md"
```

### After editing or renaming a note

```bash
# Check that no existing wikilinks are now broken vault-wide
python check-links.py /vault
```

### After vault reorganisation (moving, restructuring)

```bash
python check-links.py /vault --exclude "templates/**"
python find-orphans.py /vault --exclude "templates/**"
```

### Full vault audit

```bash
python lint-note.py /vault
python check-links.py /vault --exclude "templates/**"
python find-orphans.py /vault --exclude "templates/**"
```
