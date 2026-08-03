# SVG Generation Specification

Rules and patterns for producing self-contained SVG visualizations embedded in Markdown notes.

## Goal

Transform source content into a single, self-contained SVG that communicates essential ideas clearly and memorably — without any supporting HTML, CSS files, or JavaScript beyond what is natively embedded in the SVG.

The goal is not to decorate information. The goal is to **make structure visible** — to reveal relationships, hierarchies, sequences, and proportions that are hard to see in prose.

---

## Non-Negotiable Constraints

- Output a **single self-contained `.svg` file** only.
- Use **only SVG, with inline `<style>` and optionally `<script>`** inside the SVG.
- Do **not** use external fonts, images, stylesheets, or scripts.
- Use system fonts only: `system-ui`, `sans-serif`, `monospace`, `serif`.
- The file must render correctly when opened directly in a browser or embedded in a document with no network access.
- Target a **680px intrinsic width** with `viewBox="0 0 680 H"` and `width="100%" height="auto"` for responsive scaling.

---

## Visualization Type Selection

Before writing a single SVG element, identify the **primary cognitive task** the viewer needs to perform. Choose the type that best serves that task.

| Cognitive task | Best visualization type |
|---|---|
| Understand a process or flow | Flowchart, pipeline, swimlane |
| Understand a system with parts | Structural / containment diagram |
| Understand a mechanism or physical thing | Illustrative cross-section or spatial metaphor |
| Compare options or alternatives | Side-by-side panel, matrix, quadrant |
| See quantities and proportions | Bar chart, area chart, dot plot, treemap |
| Trace a timeline or history | Horizontal or vertical timeline |
| Navigate a taxonomy or hierarchy | Tree, cluster, indented list diagram |
| See relationships and connections | Node-link graph, chord diagram |
| Build a mental model of an abstraction | Conceptual diagram with spatial metaphor |
| Hold a dense reference in one view | Reference card, annotated table, cheat sheet |

If the source contains multiple concept types, identify the one **primary cognitive task** and build the hero visualization around it. Handle secondary content in clearly separated zones (legend, sidebar, footnote panel, inset).

---

## Content Analysis Protocol

Before writing any SVG, analyze the source content along these four dimensions.

### 1. Structure Detection

Identify what kind of structure is latent in the content:
- **Sequential** — steps, stages, phases, transformations, timelines
- **Hierarchical** — categories, subcategories, parts, components, levels
- **Relational** — dependencies, causation, flows, connections, networks
- **Comparative** — options, tradeoffs, alternatives, ranked lists
- **Quantitative** — magnitudes, proportions, distributions, trends
- **Spatial** — physical layouts, cross-sections, maps, arrangements

### 2. Density Calibration

Count the number of distinct entities (steps, categories, data points, etc.):
- 3–7 entities → single focused visualization, generous whitespace
- 8–15 entities → group into clusters or tiers; use color to distinguish groups
- 16+ entities → impose a strong hierarchy; consider a reference card format

### 3. What Must Be Preserved

Identify which of the following must appear:
- Exact labels or names (terminology matters)
- Causal or directional relationships (arrows, flows)
- Relative magnitudes (sizes, lengths, areas must encode data)
- Temporal order (left-to-right or top-to-bottom reads as time)
- Grouping or containment (things inside other things)
- Exceptions, caveats, edge cases (use footnote bands or callout panels)

### 4. Visual Priority Map

Before drawing, mentally rank all elements into three tiers:
- **Tier 1** (largest, highest contrast) — the single most important idea or entity
- **Tier 2** (mid-weight, clear but subordinate) — supporting structure
- **Tier 3** (small, muted) — annotation, labels, caveats, secondary data

The SVG must make this priority legible without the viewer reading a single word first.

---

## Visual Design System

### Layout Principles

- **Reading gravity**: the eye enters top-left. The most important element should be near the top-center.
- **Directional consistency**: choose one flow direction (top→bottom or left→right) and maintain it throughout. Never mix flow directions in the same diagram.
- **Zone separation**: use whitespace, thin hairlines (0.5px), or light fill panels to separate distinct sections.
- **Breathing room**: minimum 20px padding inside any container; minimum 16px gap between sibling elements; minimum 40px margin from the SVG edge.

### Typography Rules

- Two font sizes only: **14px** for primary labels and titles, **12px** for secondary labels, annotations, and captions.
- Two font weights only: **500** (medium) for primary labels and section headings, **400** (regular) for body text and annotations.
- **Sentence case** always — never title case, never all-caps (except single-character axis labels).
- **SVG text never wraps automatically.** Every line break requires an explicit `<tspan x="..." dy="1.2em">`. If a label needs two lines, shorten it first. Only use multi-line tspan when shortening loses critical meaning.
- **Estimate rendered width before placing text**: at 14px, allow ~8px per Latin character; at 12px, allow ~7px. A 20-character label at 14px needs ~160px horizontal clearance.
- Use `dominant-baseline="central"` on every text element that must vertically center within a shape.

### Color System

Define a minimal palette in `<style>` using CSS custom properties. All fills, strokes, and text colors must reference these variables — never hardcode hex values outside the `:root` block.

```css
:root {
  /* Backgrounds */
  --bg:        #ffffff;
  --surface:   #f5f4f0;
  --surface-2: #ebebE6;

  /* Foreground */
  --ink:       #1a1a18;
  --ink-2:     #5a5a55;
  --ink-3:     #9a9a94;

  /* Accent palette — 3 to 5 values; assign by category, not sequence */
  --a1: #3b6fd4;
  --a2: #1d9e75;
  --a3: #d85a30;
  --a4: #7f77dd;  /* omit if not needed */
  --a5: #ba7517;  /* omit if not needed */

  /* Structural */
  --border:    rgba(26,26,24,0.15);
  --border-2:  rgba(26,26,24,0.30);
  --shadow:    rgba(26,26,24,0.08);
}

@media (prefers-color-scheme: dark) {
  :root {
    --bg:        #1c1c1a;
    --surface:   #282825;
    --surface-2: #323230;
    --ink:       #e8e6dc;
    --ink-2:     #a8a69e;
    --ink-3:     #68665e;
    --border:    rgba(232,230,220,0.15);
    --border-2:  rgba(232,230,220,0.30);
    --shadow:    rgba(0,0,0,0.3);
    --a1: #5b8fe4;
    --a2: #3dbf91;
    --a3: #e87050;
    --a4: #9f98e8;
    --a5: #d49030;
  }
}
```

**Color assignment rules:**
- Color encodes **category or intensity**, never sequence or decoration.
- Use `--a1` for the most important entities; `--a2` and `--a3` for secondary groupings.
- Use `--surface` and `--surface-2` for structural containers, never accent colors.
- Maximum 4 distinct accent colors in one visualization.
- Text placed on a colored fill must use a dark shade from the same color family — never `--ink` directly on a colored background.
- Gridlines, tick marks, and decorative borders: always `--border` or `--ink-3`. Never an accent color.

### Stroke and Shape Standards

- Container borders: `stroke="var(--border)" stroke-width="0.5"`.
- Emphasized borders: `stroke="var(--border-2)" stroke-width="1"`.
- Connector lines and arrows: `stroke="var(--ink-3)" stroke-width="1" fill="none"`.
- Highlighted connectors: `stroke="var(--a1)" stroke-width="1.5" fill="none"`.
- Corner radius: `rx="4"` for subtle rounding; `rx="8"` for card-style; `rx="999"` for pills/badges only.
- **Never use drop shadows, blurs, or glow effects.**
- Gradients: only when encoding a continuous physical property. One `<linearGradient>` between exactly two stops from the same color family. No decorative gradients.

### Arrow and Connector Standards

Always include this `<defs>` block at the top of every SVG that uses arrows:

```svg
<defs>
  <marker id="arr" viewBox="0 0 10 10" refX="9" refY="5"
          markerWidth="6" markerHeight="6" orient="auto-start-reverse">
    <path d="M2 1 L8 5 L2 9" fill="none"
          stroke="context-stroke" stroke-width="1.5"
          stroke-linecap="round" stroke-linejoin="round"/>
  </marker>
</defs>
```

Use `marker-end="url(#arr)"` on connector lines. The `context-stroke` value means the arrowhead inherits the line's color automatically.

**Routing rule**: A connector must never visually cross through an unrelated node or label. If a direct path would cross something, route around it with an L-bend: `<path d="M x1 y1 L x1 ym L x2 ym L x2 y2" fill="none" .../>`. Compute `ym` to clear all obstructions.

---

## Visualization Patterns

### Pattern A — Process Flow / Flowchart

Use for: ordered steps, decision trees, pipelines, approval workflows.

- **Layout**: Single flow direction (top→bottom preferred; left→right for wide content with few steps).
- **Node sizing**: Same-type nodes share identical dimensions. Single-line: 44px tall. Two-line: 56px tall. Decision diamonds: 60×60px.
- **Node width**: `max(title_chars × 8, subtitle_chars × 7) + 24px` minimum. Never let text overflow a node.
- **Connectors**: 60px minimum gap between nodes. Arrow lines stop 2px before the node edge.
- **Decisions**: Use `<polygon>` diamond shapes for branch points; label both exit paths near the connector line.
- **Max**: 7 nodes before splitting into subflows.

### Pattern B — Structural / Containment Diagram

Use for: systems with parts, nested architectures, "things inside things".

- **Layout**: Concentric or layered containers. Outermost: largest rect, `rx="16"`, lightest fill (`--surface`).
- **Nesting depth**: Maximum 3 levels.
- **Padding**: 20px minimum between any container wall and its inner content.
- **Color by level**: Outer = `--surface`. Inner = `--surface-2` for neutral regions, accent (lightest shade) for distinct regions.
- **Labels**: Section titles at top-left of each container, 14px 500-weight.

### Pattern C — Illustrative / Conceptual Diagram

Use for: mechanisms, physical cross-sections, abstract spatial metaphors.

- Use `<path>`, `<ellipse>`, `<circle>`, `<polygon>`, curved connectors freely.
- Color as intensity: warm tones (`--a3`) = energy/activity; cool tones (`--a1`) = calm/low energy; gray = neutral structure.
- Labels go in the margins, connected by thin dashed leader lines (`stroke-dasharray="3 3"`, `stroke="var(--ink-3)"`).
- **Text over shapes is forbidden.** If a label must sit inside a region, that region needs ≥20px clear space around the text in every direction.
- One optional gradient encoding a continuous physical property.

### Pattern D — Data Visualization / Chart

Use for: quantities, proportions, distributions, trends.

- **Bar chart**: Bars as `<rect>`. Minimum bar width: 16px. Horizontal grid lines only: `stroke="var(--ink-3)" stroke-width="0.5" stroke-dasharray="4 4"`. Axis lines: `stroke="var(--border-2)" stroke-width="1"`.
- **Axes**: x-axis at bottom, y-axis at left. Tick labels: 12px regular, `--ink-2`. Axis titles: 12px 500-weight, `--ink-2`. Always include units.
- **Data labels**: Place value labels above bars or at data points. Never inside a bar unless there is 8px clearance above and below.
- **Color**: One accent color per data series. Never gradient fills for bars — flat fills only.
- **Zero baseline**: Bar charts must start at zero unless the range explicitly makes this misleading, in which case annotate the non-zero baseline.

### Pattern E — Timeline

Use for: chronological events, historical sequences, version histories.

- **Layout**: Horizontal for fewer than 8 events; vertical for 8 or more.
- **Spine**: A single line, `stroke="var(--border-2)" stroke-width="2"`.
- **Event markers**: Circles (`r="5"`) on the spine. Primary events: filled with `--a1`. Minor events: `--surface-2` fill with `--border-2` stroke.
- **Labels**: Alternate above/below (horizontal) or left/right (vertical) to prevent overlap. Date: 12px `--ink-2`. Event name: 14px 500-weight `--ink`.
- **Max**: 10 events before grouping by era.

### Pattern F — Comparison / Matrix

Use for: tradeoffs, options evaluation, feature comparison, quadrant positioning.

- **Side-by-side**: Equal-width columns separated by a hairline or 16px gap. Column headers: accent-colored band, 14px medium. Rows: alternate `--bg` and `--surface`.
- **Quadrant**: 2×2 grid with labeled axes. Prominent cross at center. Quadrant labels in corners at 12px italic, `--ink-2`.
- **Matrix table**: Header row: `--surface-2`. Data cells: `--bg`. Cell text: 12px. Cell padding: 8px horizontal, 6px vertical. Borders: `--border` at 0.5px.

### Pattern G — Reference Card / Cheat Sheet

Use for: dense reference material, taxonomies, glossaries, command references.

- **Layout**: 1 column for 5–8 items; 2 columns for 9–20 items; 3 columns for 21–40 items.
- **Section headers**: `--surface` band, full column width, 14px medium, `--ink`, 8px padding.
- **Item rows**: 12px regular, alternating `--bg` / `--surface`, 6px vertical padding.
- **Callout boxes**: 3px left border in `--a3`, `--surface` background, 12px regular text, 12px padding.
- **Density ceiling**: More than 40 items belongs in a document, not a reference card.

---

## SVG Technical Requirements

### File Structure Template

```svg
<svg xmlns="http://www.w3.org/2000/svg"
     viewBox="0 0 680 H"
     width="100%" height="auto"
     role="img"
     aria-labelledby="svg-title svg-desc">

  <title id="svg-title"><!-- Short, descriptive title --></title>
  <desc id="svg-desc"><!-- One-sentence description of what the visualization shows --></desc>

  <style>
    :root { /* CSS custom properties */ }
    @media (prefers-color-scheme: dark) { :root { /* dark overrides */ } }
    @media (prefers-reduced-motion: reduce) { * { animation: none !important; transition: none !important; } }
    text { font-family: system-ui, sans-serif; fill: var(--ink); }
    .label-primary   { font-size: 14px; font-weight: 500; }
    .label-secondary { font-size: 12px; font-weight: 400; fill: var(--ink-2); }
    .label-muted     { font-size: 12px; font-weight: 400; fill: var(--ink-3); }
  </style>

  <defs>
    <marker id="arr" viewBox="0 0 10 10" refX="9" refY="5"
            markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M2 1 L8 5 L2 9" fill="none"
            stroke="context-stroke" stroke-width="1.5"
            stroke-linecap="round" stroke-linejoin="round"/>
    </marker>
  </defs>

  <rect width="680" height="H" fill="var(--bg)"/>

  <!-- Visualization content -->

</svg>
```

### ViewBox Sizing Protocol

1. Lay out all elements with their correct coordinates.
2. Find `max_y` = bottom edge of the lowest element (add 4px for text descenders).
3. Set viewBox height `H` = `max_y + 40` (40px bottom padding).
4. Verify: no element has coordinates or extent outside x=[0, 680] or y=[0, H].
5. **Never use negative coordinates.**
6. For `text-anchor="end"` elements: verify that `x − (char_count × 7)` > 0 before placing.

### Accessibility Requirements

- Every SVG must have `<title>` and `<desc>` with meaningful content.
- Use `role="img"` on the root SVG element.
- Decorative shapes that carry no semantic meaning: add `aria-hidden="true"`.
- Groups representing meaningful units: add `role="group"` and `aria-label="..."`.

### Animation Standards (Optional)

Animation is appropriate only when it encodes a meaningful state change or draws attention to a critical element.

**Permitted**: one-shot entrance animation on page load (max 1.2s); one-shot data update transition (max 0.4s); subtle pulse on an interactive element.

**Always wrap animations**:
```css
@media (prefers-reduced-motion: no-preference) {
  .animated-element { animation: myAnimation 0.6s ease-out forwards; }
}
```

**Forbidden**: infinite loops on non-physical diagrams; rapid flicker; animations that obscure the static view.

---

## Quality Checklist

Before finalizing the SVG, verify each item:

**Content**
- [ ] All critical entities from the source content are represented.
- [ ] Important caveats or exceptions are visible.
- [ ] No invented relationships or facts not grounded in the source.

**Visual**
- [ ] A 3-second viewer can identify the topic without reading.
- [ ] Visual hierarchy matches the priority map (Tier 1 > Tier 2 > Tier 3).
- [ ] Color encodes category or intensity — never sequence or decoration.
- [ ] No more than 4 accent colors.
- [ ] No element overflows the viewBox.
- [ ] No two elements overlap unintentionally.
- [ ] No connector arrows pass through unrelated nodes or labels.

**Technical**
- [ ] viewBox height = actual content height + 40px.
- [ ] All vertically centered text has `dominant-baseline="central"`.
- [ ] No `text-anchor="end"` text extends past x=0.
- [ ] Dark mode CSS is present.
- [ ] `prefers-reduced-motion` disables all animations.
- [ ] `<title>` and `<desc>` are meaningful.
- [ ] No external resources are referenced.

**Typography**
- [ ] No text extends beyond its container.
- [ ] Multi-line text uses explicit `<tspan>` — no implicit wrapping.
- [ ] Only 14px and 12px font sizes; only 400 and 500 weights.
- [ ] Sentence case throughout.
