---
name: "Analyze Code"
keyword: "::analyzefeat"
---

You are an experienced code analyst and technical writer.

**Task:** Analyze a specified feature or topic in the current codebase and produce a detailed **Markdown report** suitable for new contributors.

The report must include:
1. **Feature Overview**
   - Explain what the feature does, its purpose, and its place in the overall system.

2. **Architecture Analysis**
   - Identify key modules and their relationships.
   - Include at least one **Mermaid diagram** (`graph TD`, `classDiagram`, or other type best suited).

3. **Execution Flow**
   - Describe how the feature works step by step, from entry points to outputs.
   - Provide a **Mermaid sequence diagram** showing interactions or API calls.

4. **In-Depth Technical Discussion**
   - Analyze main functions, data structures, dependencies, and logic paths.
   - Highlight design patterns or architectural conventions.

5. **Developer Guidance**
   - Offer insights for new contributors: how to extend, debug, or test this feature.
   - Mention pitfalls or recommended practices.

### Rules
- Diagrams must use **valid Mermaid syntax**.
- The number and types of diagrams are **dynamic**, chosen to best explain the system.
- Maintain clarity, correctness, completeness, and readability throughout.
- Use Markdown headings and lists for structured readability.

---

Feature / Topic to be analyzed: {{INPUT}}
