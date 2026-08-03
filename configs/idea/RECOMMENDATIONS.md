# IntelliJ IDEA — how to actually use it well (Java/Kotlin, Ultimate)

Opinionated guide. Assumes the **VSCode Keymap** plugin is active, so shortcuts
below use VS Code bindings where they differ; the native IntelliJ binding is
shown in `(parens)` when it matters. macOS uses `Cmd`, Windows `Ctrl` — written
as `Cmd/Ctrl`.

---

## 1. First-run setup order

1. Sign in to JetBrains account → Ultimate license activates.
2. Install plugins (`plugins.md`), restart.
3. Settings > Keymap → **VSCode**.
4. Run `apply.ps1` / `apply.sh` → editor + templates staged.
5. Import code style (`Google`) and inspection profile (`Recommended`) via the UI
   dialogs the script prints.
6. Set project SDK: `File > Project Structure > SDK`. Kotlin style:
   add `kotlin.code.style=official` to the project's `gradle.properties`.

---

## 2. Navigation — the real speed unlock

IDEA's superpower is semantic navigation. Stop scrolling; jump.

| Action | Shortcut | Note |
|--------|----------|------|
| Search Everywhere | `Shift Shift` | Classes, files, actions, settings — one box. |
| Go to class | `Cmd/Ctrl O` (native) | Type CamelCase initials: `NPE` → `NullPointerException`. |
| Go to file | `Cmd/Ctrl P` | |
| Go to symbol | `Cmd/Ctrl Alt O` | Method/field by name. |
| Find action | `Cmd/Ctrl Shift P` | Run any IDE command without hunting menus. |
| Go to declaration | `F12` / `Cmd/Ctrl click` | |
| Go to implementation | `Cmd/Ctrl F12` | Down through interfaces. |
| Find usages | `Shift F12` (`Alt F7` native) | |
| Recent files | `Cmd/Ctrl E` | Then type to filter. |
| Recent locations | `Cmd/Ctrl Shift E` | Files + the code you were reading. |
| Back / Forward | `Cmd/Ctrl [` / `]` | Navigation history. |
| Structure popup | `Cmd/Ctrl F12` | File outline; type to filter. |
| Bookmarks | `F11` toggle, `Cmd/Ctrl F11` mnemonic | |

**Habit:** never open the Project tree to find a file. `Shift Shift` or `Cmd/Ctrl P`.

---

## 3. Refactoring — let the IDE edit for you

This is where IDEA beats editors. Everything is safe (updates all references).

| Refactor | Shortcut |
|----------|----------|
| Rename (everywhere) | `F2` (`Shift F6` native) |
| Extract method | `Cmd/Ctrl Alt M` |
| Extract variable | `Cmd/Ctrl Alt V` |
| Extract field / constant / param | `Cmd/Ctrl Alt F` / `C` / `P` |
| Inline | `Cmd/Ctrl Alt N` |
| Change signature | `Cmd/Ctrl F6` |
| Refactor This (menu) | `Cmd/Ctrl Alt Shift T` |
| Move class/member | `F6` |

**Intentions / quick-fix:** `Cmd/Ctrl .` (native `Alt Enter`) on any warning or
even valid code — offers context actions (add null check, convert to switch
expression, chain to stream, add `@Override`, create test, etc.). Press it
constantly; it's the single highest-leverage key.

---

## 4. Code generation

- `Cmd/Ctrl N` (native `Alt Insert`) in a class → generate constructor, getters/
  setters, `equals`/`hashCode`, `toString`, override methods, test.
- Postfix completion: type `expr.` then `nn`, `null`, `for`, `var`, `sout`,
  `notnull`, `req` → expands in place. e.g. `list.for` + Tab → for-each loop.
- Live templates: `psvm`, `logger`, `test5`, `dataclass`, `ktest` (shipped in
  `templates/JavaKotlin.xml`) plus built-ins `iter`, `fori`, `sout`.

---

## 5. Run / Debug

- Run current file/test: click the gutter ▶, or `Ctrl R` (native `Ctrl R`/`Shift F10`).
- Debug: gutter bug icon, or `F5` (VSCode keymap).
- **Conditional breakpoints:** right-click the breakpoint → condition expression.
- **Evaluate expression** while paused: `Alt F8` — run arbitrary code in context.
- **Drop frame / reset to method start** to re-run without restarting.
- Debugger inline values show right in the editor — no watch window needed.
- For Spring Boot: use the generated Spring run config (not a plain main) so
  actuator/devtools wiring works.

---

## 6. Spring (Ultimate)

- Beans gutter icons → jump to injection points and bean definitions.
- `Endpoints` tool window: see all HTTP mappings, hit them with the built-in
  HTTP Client (`.http` files) — no Postman needed.
- `application.yml`/`.properties` get completion + validation for known keys.
- Diagram: right-click a config class → Diagrams > Show Beans Dependencies.

---

## 7. Ultimate tools worth using

- **HTTP Client** (`.http` scratch or file): version-controlled API calls.
  Keep secrets in `http-client.private.env.json` (gitignored — see `secrets.md`).
- **Database tool window**: attach a DB, get schema-aware SQL completion, run
  queries, diff schemas. Creds live in the OS keychain, not the repo.
- **Profiler**: `Run > Profile` for async-profiler flame graphs on any run config.
- **Scratch files** (`Cmd/Ctrl Shift N`): throwaway Java/Kotlin/SQL/JSON that
  runs without a project.

---

## 8. Editing multi-cursor (VS Code muscle memory carries over)

| Action | Shortcut |
|--------|----------|
| Add cursor to next match | `Cmd/Ctrl D` |
| Add cursor above/below | `Cmd/Ctrl Alt ↑/↓` |
| Select all occurrences | `Cmd/Ctrl Shift L` |
| Expand/shrink selection | `Alt ↑ / ↓` (semantic!) |
| Move line up/down | `Alt Shift ↑/↓` |
| Duplicate line | `Cmd/Ctrl Shift D` (native `Cmd/Ctrl D`) |
| Comment line | `Cmd/Ctrl /` |

`Alt ↑` (semantic expand) is smarter than VS Code's — it grows by AST node.

---

## 9. VCS

- Commit tool window (`Cmd/Ctrl K`): stage hunks, run inspections + reformat on
  commit (enable those checkboxes once).
- `Cmd/Ctrl Shift K` push. `Annotate` (right gutter) for inline blame.
- **Local History** (right-click file > Local History): IDE-level undo across
  days, independent of Git. Saved me more than once.
- Shelve vs stash: Shelve is IDEA-native, survives across branches, diffable.

---

## 10. AI assistance

- GitHub Copilot (installed): inline completions.
- JetBrains AI Assistant (`ml-llm`): explain/refactor/generate-tests actions in
  the right-click menu and `Alt Enter`. Auth on first use; tokens never in repo.
- Both auth locally — nothing to commit.

---

## 11. Settings that pay off (set once)

- Editor > General > **Auto Import** → "Add unambiguous imports on the fly" +
  "Optimize imports on the fly".
- Editor > General > Appearance → show method separators.
- Editor > Code Style > enable "Reformat + Optimize imports" in the commit dialog.
- Editor > Inspections → activate the **Recommended** profile.
- `Cmd/Ctrl Shift A` → "Registry" only if you know what you're changing.
- Increase memory if projects are large: Help > Change Memory Settings → 2048–4096 MB.

---

## 12. Learn-the-keymap tip

Install **Key Promoter X**. Every time you click something that has a shortcut,
it nags you with the shortcut. Two weeks of that and your hands know the IDE.
