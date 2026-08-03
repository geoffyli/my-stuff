# Knowledge Organization Guide

Rules for organizing Markdown notes into a connected, navigable knowledge base.

## Philosophy

### Flat Organization Over Deep Hierarchies

- **Minimal folder depth** — Folders serve as broad domain categorization only, not detailed organization.
- **Wikilinks as primary connectors** — Use `[[note name]]` to create relationships between concepts rather than nested folder structures.
- **Tags as secondary organization** — Use `#tag` for cross-cutting themes and content categorization.
- **Discoverability through connections** — Related notes should be findable through link networks, not folder navigation.

## Maps of Content (MOC) Pattern

- **MOCs serve as navigation hubs** — Index notes that link to related content within a domain.
- **Build knowledge networks** — Connect individual notes into coherent knowledge structures.
- **Avoid deep nesting** — MOCs can reference other MOCs or notes, but keep hierarchy shallow.
- **Focus on relationships** — Emphasize how concepts connect rather than rigid categorization.

## Parent-Child Relationships

- **Frontmatter-based hierarchy** — Use `parent: "[[Parent Note]]"` field to establish clear relationships.
- **Bidirectional awareness** — Parent notes should link to their children; children must reference their parent.
- **Logical grouping** — Use when notes naturally belong under a broader concept or when splitting large notes into subnotes.
- **Maintain context** — Child notes should be meaningful both independently and within their parent context.

## Attachment Organization

- **Use a vault-level attachments root** — Store attachments under `attachments/` at the vault root.
- **Separate by type** — Use subfolders by attachment kind rather than mixing files together.
- **Images go under `attachments/imgs/`** — Place note images in `<vault-path>/attachments/imgs/`.
- **Keep note folders content-focused** — Avoid scattering attachment files beside Markdown notes unless the vault already uses a different established convention.

## Wikilink Guidelines

### When to Create Wikilinks

- **Concept references** — Any mention of a specific concept that has (or should have) its own note.
- **Related knowledge** — Connecting ideas across different domains or notes.
- **MOC connections** — Linking from content notes to relevant Maps of Content.
- **Parent-child relationships** — Bidirectional links between parent and child notes.
- **Cross-domain connections** — Linking concepts across different knowledge areas.

### Wikilink Syntax

**Content wikilinks:**
- Basic reference: `[[Note Name]]`
- Section linking: `[[Note Name#Section Header]]`

**Frontmatter wikilinks:**
- Correct: `parent: "[[Note Name]]"` — quotes around entire wikilink
- Correct: `- "[[Related Note]]"` — quotes around each wikilink in lists
- Wrong: `parent: [[Note Name]]` — missing quotes

### Wikilink Integrity

- **Verify target notes exist** — Every wikilink must point to an existing note before finalizing content.
- **Avoid duplicate note filenames in the same vault** — Multiple notes with the same filename create ambiguous bare wikilinks such as `[[Topic]]`. Prefer unique filenames vault-wide.
- **Create missing notes immediately** — When a required note does not exist, create it so no broken references remain.
- **Bidirectional link maintenance** — If Note A links to Note B, Note B should reference Note A.
- **Update parent notes** when creating child notes with appropriate wikilinks.
- **Check for broken links** when modifying note titles or moving content.

### Link Quality

- **Prefer specific over general** — Link to `[[Machine Learning Algorithms]]` not `[[Tech]]`.
- **Maintain link context** — Ensure surrounding text makes the link purpose clear.
- **Avoid link clustering** — Don't create excessive links in single paragraphs.

## Tag Organization

**Agent restriction:** AI agents are **PROHIBITED** from modifying tags in any way.
- Never add, remove, or modify tags in frontmatter or inline.
- Tags are human-maintained only.
- Read existing tags for context and content placement decisions.
- Use tag patterns to inform wikilink suggestions and understand note relationships.
