# Creating a Child Note

## Definition

A child note is a content note that belongs under a broader concept note or MOC. It elaborates on a specific topic within that parent context and must always have a parent.

## Workflow

1. **Create the file** — Place it in the same directory as its parent MOC. Name it descriptively following the [file naming conventions](../references/markdown-formatting.md#file-naming-conventions).

2. **Define frontmatter** — The `parent` field is mandatory and must contain a wikilink to the parent MOC:
    ```yaml
    ---
    parent: "[[Parent MOC Name]]"
    tags:
    related:
    ---
    ```
    Always include all three fields. Leave `tags` empty — it is human-maintained. Leave `related` empty unless there are related notes not mentioned in the body.

3. **Write content** — Fill in the note content following [markdown-formatting.md](../references/markdown-formatting.md):
    - Ensure it can be understood independently but references the parent context where useful.
    - Add contextual wikilinks to build connections to other knowledge notes.

4. **Update the parent MOC** — Add a bulleted wikilink (e.g., `- [[Name of New Child Note]]`) to the parent MOC's `## Contents` section. This completes the bidirectional link.
