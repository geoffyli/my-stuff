# Visualization Tool

Generate and display HTML content in the user's browser when visual aids would deepen understanding.

## How It Works

1. Write a self-contained HTML file to `/tmp/learn-viz-<descriptive-name>.html`
2. Open it in Chrome using `mcp__chrome__new_page` with a `file://` URL
3. Reference the visualization in conversation and continue the session

## When to Use

Agent judgment — visualize when:

- Concepts have spatial or structural relationships (architectures, flows, trees)
- Comparing multiple things side-by-side (tradeoffs, feature matrices, before/after)
- Code examples benefit from syntax highlighting and formatting
- A timeline or sequence is clearer visually than in words
- The user is struggling with something that has a natural visual representation

Don't visualize simple definitions, straightforward explanations, or anything that works fine in plain text. Most learning happens in conversation — visuals are supplementary.

## HTML Guidelines

- Fully self-contained: inline CSS, inline JS if needed, no external dependencies
- System fonts: `system-ui, -apple-system, sans-serif`; monospace for code: `ui-monospace, monospace`
- Support dark mode via `@media (prefers-color-scheme: dark)`
- Layout with modern CSS (flexbox, grid)
- Diagrams: inline SVG preferred
- Code blocks: `<pre><code>` with basic syntax highlighting via inline styles
- Target width: ~800px
- Keep it simple — purpose is clarity, not design showcase
