# Editing Existing Notes

## Goal

Modify existing notes while preserving their structure, metadata, wikilink connections, and relationships.

## Workflow

1. **Read first** — Read the full note before editing. Understand its structure, frontmatter (especially `parent` and `related` fields), and how it connects to other notes via wikilinks.

2. **Preserve frontmatter** — Keep existing frontmatter fields intact unless the edit explicitly requires changes:
    - Maintain `parent` relationships unless explicitly restructuring.
    - Keep `related` links unless they become irrelevant.
    - **Never modify `tags`** — tags are human-maintained only.

3. **Update content** — Make the requested changes. Keep the note focused on its topic. If it's growing too long, consider splitting it (see [split-long-note.md](split-long-note.md)).

4. **Maintain wikilink connections** — Improve or update wikilinks as content changes:
    - Ensure bidirectional links remain valid (if this note links to another, that note should link back).
    - Update parent MOCs if note titles or relationships change.
    - Verify all wikilinks still resolve after modifications.

5. **Verify formatting** — Confirm the edited note still follows [markdown-formatting.md](../references/markdown-formatting.md) rules.

6. **Run quality-gate scripts** — From the skill's `scripts/` directory:

    ```bash
    # Validate formatting rules
    python lint-note.py <vault_dir> --file <note.md>

    # Check all wikilinks in the edited note still resolve
    python check-links.py <vault_dir> --file <note.md>
    ```
