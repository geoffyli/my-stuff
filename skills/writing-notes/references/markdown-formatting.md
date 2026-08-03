# Markdown Formatting Rules

Default rules for Markdown notes. If a target system or project has its own style rules (provided by another skill or project config), those take precedence.

## File Naming Conventions

- **Lead with broader concept** — Start with the outer/parent concept to avoid duplicates (e.g., `Redis Strings.md` not `Strings.md`).
- **Use Title Case** — Capitalize main words for consistency.
- **Avoid duplicate note filenames within a vault** — Do not create two Markdown notes with the same filename in different folders of the same vault. Duplicate names make bare wikilinks ambiguous and increase maintenance risk.
- **No special characters** — Avoid `!@#$%^&*()` or other symbols.
- **No leading numbers** — Don't start filenames with digits (`01-`, `2024-`, etc.).
- **No "MOC" in filenames** — Use `Factory Pattern.md` not `Factory Pattern MOC.md`.
- **Use spaces for readability** — `Machine Learning Algorithms.md` not `machine-learning-algorithms.md`.
- **Keep reasonable length** — Aim for under 50 characters when possible.

## Frontmatter Metadata Standards

### Standard Template

```yaml
---
parent: "[[Parent Note Name]]"
tags:
related:
  - "[[Related Note 1]]"
  - "[[Related Note 2]]"
---
```

### Field Rules

- **`parent`** — Mandatory for all notes. Always include the key. Must reference an existing parent note using wikilink syntax; set to empty only for vault root-level notes that have no parent.
- **`tags`** — Human-maintained only. Always include the key; leave the value empty. Agents must never add, remove, or modify tags.
- **`related`** — Always include the key; leave the value empty when not used. Populate only with notes NOT directly mentioned in content. If mentioned in content, use contextual wikilinks instead.

### Agent Frontmatter Guidelines

**When creating new notes:**
- Always write all three fields (`parent`, `tags`, `related`). Leave `tags` and `related` empty when not populated — do not omit them.
- Set `parent` to the appropriate parent note wikilink.
- Leave `tags` empty — humans will add tags if needed.
- Only populate `related` if related notes aren't mentioned in content.

**When editing existing notes:**
- Preserve all existing frontmatter structure and formatting.
- Never modify the `tags` field.
- Maintain existing `parent` relationships unless explicitly restructuring.

## MOC (Maps of Content) Structure

MOCs are structured navigation hubs with a specific format:
- Begin with a brief overview.
- Main content under a `## Contents` heading, using a hierarchical bulleted list of wikilinks.
- **Intentional link duplication** — If a MOC links to a sub-MOC, the sub-MOC's content links should also be listed (indented) directly below it for discoverability. Separate sub-MOC blocks with a blank line.
- Maximum indentation level: 3.

Example:
```markdown
# AI MOC

A brief overview of the Artificial Intelligence domain.

## Contents
- [[Large Language Models MOC]] — language models and their variants
	- [[GPT-4]]
	- [[LLaMA]]

- [[Computer Vision]]
	- [[Object Detection]]

- [[Reinforcement Learning]]
```

## Heading Structure

- Exactly one `#` (H1) per file, used as the document title.
- Use sequential heading levels: `##`, then `###`, then `####`. No skipping (no `###` without a `##` first).
- Maximum depth: `####` (H4). If you need deeper structure, reorganize into subsections or separate files.

## Lists

- One space after the list marker: `- item` and `1. step` (not `-  item` or `1.  step`).
- Use 2-space or tab indentation for nested list items (4 spaces may render incorrectly in Obsidian).
- Keep bullet points parallel in grammatical structure within a single list.

## Code

- Use fenced code blocks with a language identifier for code snippets: ` ```python `, ` ```bash `, etc.
- Use inline code (`backticks`) for commands, filenames, technical identifiers, and short expressions within prose.

## Attachments

- Store note attachments under the vault-level `attachments/` directory, not beside individual notes.
- Separate attachments by type using subfolders under `attachments/`.
- Image files should be stored under `<vault-path>/attachments/imgs/`.
- When adding an attachment reference, follow any existing local link style in the vault.

## Diagrams (Mermaid)

Add a Mermaid diagram when:
- Relationships or connections are complex enough that text alone is confusing.
- There is a process flow, decision tree, or hierarchy to show.
- The diagram genuinely clarifies — not just decorates.

Place diagrams after the concept introduction, before the detailed explanation. Use a fenced code block with the `mermaid` language tag.

## Diagrams (SVG)

Use SVG when the visualization needs precise layout, color-encoded data, multiple visual zones, or richer structure than Mermaid can express cleanly.

**Choose SVG when:**
- Comparing options or showing quantitative data (charts, proportions, ranked lists)
- The diagram has multiple color-coded categories or visual hierarchy that carries meaning
- A dense reference card or structured layout is needed
- The diagram benefits from dark-mode support or responsive scaling

**Mermaid is sufficient when:**
- The diagram is a simple flowchart, sequence, or entity-relationship diagram
- A quick structural sketch matters more than visual polish

**Generating SVGs:** Follow the full specification in [references/svg-generation.md](references/svg-generation.md). Produce a single, self-contained `.svg` file with inline `<style>` and no external dependencies.

**Storing and embedding SVGs:**
- Save the file under `<vault-path>/attachments/imgs/` using a descriptive Title Case filename (e.g., `Redis Data Structures.svg`).
- Embed in the note with `![[Redis Data Structures.svg]]`.
- Place the embed after the concept introduction, before the detailed explanation — same rule as Mermaid.

## Mathematical Expressions (LaTeX)

Use LaTeX when mathematical notation is clearer than plain text:
- **Inline**: `$...$` for expressions within sentences.
- **Display**: `$$...$$` on their own line for standalone equations.

Use LaTeX for: formal notation, complexity analysis (e.g., $O(n \log n)$), statistical expressions, calculus, linear algebra.
Skip LaTeX for: simple counts, casual arithmetic, programming variables (use code formatting instead).

## General Style

- Avoid noisy decoration: excessive bold, emoji, or horizontal rules.
- Prefer concrete examples over abstract descriptions when explaining concepts.
- Keep paragraphs focused; break long blocks at natural topic shifts.
- Avoid unnecessary verbosity — say it once, clearly.
- No trailing "Related" sections — do not append a "Related" heading or list at the bottom of a note; use in-content wikilinks or the frontmatter `related` field instead.
