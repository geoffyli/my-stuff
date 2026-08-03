# Note Type Guide

Quick reference for choosing and structuring different note types.

## Type Selection

| Type | Use when... | Key structural feature |
|------|-------------|----------------------|
| Learning notes | Studying a topic for understanding and recall | Progressive build-up, examples, key takeaways |
| Topic summary | Condensing a broad area into an overview | Breadth over depth, organized subsections |
| Technical documentation | Documenting how something works or how to use it | Prerequisites, steps, code blocks, caveats |
| Concept explanation | Explaining a single concept clearly | Definition, intuition, examples, common misconceptions |
| Process notes | Documenting a workflow or procedure | Numbered steps, decision points, expected outcomes |
| Comparison notes | Evaluating alternatives side by side | Parallel structure or table, verdict |
| Reference sheet | Quick-lookup material | Dense, scannable, minimal prose |
| Freeform notes | Anything that doesn't fit above | Flexible; use clear headings and logical flow |

If the type is ambiguous, infer the best fit from the request context. **Learning notes vs. Concept explanation tiebreaker:** Use Concept explanation for a single, isolated concept; use Learning notes for a topic area that contains multiple concepts.

## Templates

Each note type has a dedicated template in `templates/` that provides both frontmatter and the section skeleton:

| Type | Template |
|------|----------|
| Learning Notes | `templates/learning-notes.md` |
| Topic Summary | `templates/topic-summary.md` |
| Technical Documentation | `templates/technical-documentation.md` |
| Concept Explanation | `templates/concept-explanation.md` |
| Process Notes | `templates/process-notes.md` |
| Comparison Notes | `templates/comparison-notes.md` |
| Reference Sheet | `templates/reference-sheet.md` |
| Freeform Notes | No template — use `templates/note.md` (frontmatter only) and apply clear headings with logical flow. |
