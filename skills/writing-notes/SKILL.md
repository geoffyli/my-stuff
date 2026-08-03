---
name: writing-notes
description: Write, revise, split, and organize Markdown notes and documents, including MOC creation, note splitting, and child note creation. Use when the user asks for learning notes, technical docs, summaries, topic writeups, comparison notes, reference sheets, general Markdown documentation, or any note organization task.
---

# Writing Notes

Use this skill whenever the task is to create, rewrite, expand, clean up, or organize Markdown notes or documents.

## Definition

**Vault** — The root folder for a note collection. It can contain Markdown notes, nested subfolders, and supporting files such as images, attachments, or templates. In this skill, scripts treat the vault as the base directory from which note paths and wikilinks are resolved.

## Goal

Produce Markdown notes that are:
- structurally clear
- easy to scan
- faithful to the source material or requested topic
- consistent in formatting
- useful for future review, not just immediate reading

## Workflow

### 1. Identify the note type

Classify the requested output using the taxonomy in [references/note-type-guide.md](references/note-type-guide.md). Types include: learning notes, topic summary, technical documentation, concept explanation, process notes, comparison notes, reference sheet, and freeform notes.

If the type is ambiguous, infer the best fit from the request context.

### 2. Gather context

Read existing files in scope. If the user specified a target directory, check sibling files to match local conventions (naming patterns, frontmatter style, heading conventions). Review the knowledge organization principles in [references/contents-organizing.md](references/contents-organizing.md) for wikilink, MOC, and parent-child patterns.

If working inside a vault, check for existing Markdown note names across the vault before creating a new file. Avoid duplicate filenames anywhere in the same vault, even across different folders, because they make bare wikilinks ambiguous and harder to maintain.

If the note needs attachments, store them under the vault-level `attachments/` directory instead of beside the note. Use separate subfolders by attachment type. For images, place files under `<vault-path>/attachments/imgs/`.

### 3. Choose structure

Use the template from `templates/` that matches the identified note type — for example, `templates/learning-notes.md` for learning notes or `templates/comparison-notes.md` for a comparison. The template provides both the frontmatter and the section skeleton. See [references/note-type-guide.md](references/note-type-guide.md) for the type → template mapping and selection guidance. Freeform notes have no template; use `templates/note.md` (frontmatter only) and apply clear headings with logical flow.

### 4. Apply formatting rules

Follow the rules in [references/markdown-formatting.md](references/markdown-formatting.md) (formatting, frontmatter, file naming, MOC structure) and [references/contents-organizing.md](references/contents-organizing.md) (wikilinks, parent-child, tags). If the target context has additional style rules (from a companion skill or project configuration), those override the defaults here.

### 5. Draft for usefulness

Optimize for:
- clarity and precision
- structure and scannability
- faithful content with minimal redundancy
- examples where they improve understanding
- diagrams (Mermaid or SVG) for relationships, flows, hierarchies, or data visualizations that need precise layout or color-encoded structure

### 6. Self-check before delivering

Verify:
- [ ] Headings are consistent and hierarchical
- [ ] Bullet points are parallel in structure
- [ ] Terminology is consistent throughout
- [ ] Formatting follows the applicable conventions
- [ ] Examples are included where they add clarity
- [ ] The note serves its stated purpose

When a vault path is available, run the quality-gate scripts to catch mechanical errors automatically. Scripts must be run from the skill's `scripts/` directory (or invoked by absolute path):

```bash
# Validate formatting rules (--strict treats warnings as errors)
python scripts/lint-note.py <vault_dir> --file <note.md> --strict

# Confirm all wikilinks in the note resolve to real files
python scripts/check-links.py <vault_dir> --file <note.md>

# For vault-wide link checks, exclude templates to avoid false positives:
# python scripts/check-links.py <vault_dir> --exclude "templates/**"
```

See [Scripts](#scripts) for full usage reference.

## Scripts

Utility scripts in `scripts/` automate mechanical checks that are tedious to do manually. All are pure Python 3 (no external dependencies). By default they prioritize correctness over strict template conformance.

| Script | Purpose | When to run |
|--------|---------|-------------|
| [`scripts/check-links.py`](scripts/check-links.py) | Find `[[wikilinks]]` pointing to non-existent notes | After writing or editing any note |
| [`scripts/lint-note.py`](scripts/lint-note.py) | Validate naming, frontmatter, headings, and style | Before delivering a new or revised note |
| [`scripts/find-orphans.py`](scripts/find-orphans.py) | Surface notes with no parent and no incoming links | After vault reorganisation or mass edits |

See [`scripts/README.md`](scripts/README.md) for detailed usage, output examples, and agent patterns.

## Standard Operating Procedures

For note organization tasks, follow the appropriate SOP:

| Operation | SOP | When to use |
|-----------|-----|-------------|
| Edit an existing note | [SOPs/edit-notes.md](SOPs/edit-notes.md) | Modifying content while preserving structure and metadata |
| Split a long note | [SOPs/split-long-note.md](SOPs/split-long-note.md) | A note is too long to scan; needs to be broken into focused pieces |
| Create a child note | [SOPs/create-child-note.md](SOPs/create-child-note.md) | Adding a new note under an existing index/overview note |

## Composability

This skill provides both **Markdown writing ability** and **knowledge organization methodology** (frontmatter, wikilinks, MOCs, tags). If a project or system provides its own conventions (e.g., via AGENTS.md or a companion skill), those override the defaults in this skill's reference files.

## Degrees of Freedom

**Decide without asking:**
- Which note type best fits the request
- Section ordering within the chosen structure
- Whether to include a diagram, and whether Mermaid or SVG better suits the content
- Level of detail (unless the user specifies)

**Ask when:**
- The note type is genuinely ambiguous between two very different structures
- The target directory or system is unclear
- The requested scope is very broad and could be split into multiple notes
