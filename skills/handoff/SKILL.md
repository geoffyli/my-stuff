---
name: handoff
description: Compact the current conversation into a structured handoff index for the next agent to pick up.
argument-hint: "What will the next session focus on?"
---

Generate a handoff document for the next agent using the template at TEMPLATE.md in this skill folder (read it first).

Rules:
- All 8 sections are required. Write "None" if a section has nothing to report.
- All `[file]` pointers in Changelist and Context Pointers must use absolute paths.
- Context pointers: flat annotated list, one entry per line, format `[type] pointer — reason`. Types: [file] [commit] [url] [env]. Order by relevance — most critical first.
- Do not duplicate content already in commits, diffs, files, or PRDs. Pointer + reason only.
- If the user passed an argument describing the next session's focus, tailor context pointers and Next Action to that focus. If no argument, infer from conversation.

Output the completed handoff directly in chat, inside a single markdown code fence.
