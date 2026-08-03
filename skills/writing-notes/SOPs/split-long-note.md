# Splitting a Long Note

## Goal

When a note becomes too long to scan easily, split it into focused child notes and convert the original into a MOC (Map of Content) linking them together.

## When to Split

- The note has grown past ~300-500 lines.
- It covers multiple distinct subtopics that could stand alone.
- Sections are independently useful as references.

## Workflow

1. **Propose sections** — Analyze the note's structure and propose which sections to extract as separate notes. **Wait for user approval** before proceeding.

2. **Create child notes** — For each approved section, follow the [create-child-note.md](create-child-note.md) SOP:
    - Place child notes in the same directory as the original.
    - Each child note gets `parent: "[[Original Note]]"` in its frontmatter.
    - Add contextual wikilinks to build connections to other related notes.

3. **Convert original to MOC** — Transform the original note into a Map of Content:
    - Keep the brief overview at the top.
    - Replace extracted sections with a `## Contents` section containing bulleted wikilinks to the new child notes.
    - Optionally add a brief summary sentence after each link when context aids navigation.
    - Follow the MOC structure rules in [markdown-formatting.md](../references/markdown-formatting.md).

4. **Cleanup (user approval required)** — If any files became obsolete or duplicated by the split, list them and ask for explicit user confirmation before deleting. Never delete without approval.
