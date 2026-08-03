# IntelliJ IDEA plugins — documented list, manual install

IDEA has no reliable `--install-plugin` CLI, so install these from
**Settings > Plugins > Marketplace** (search by the plugin name). The IDs are
listed for precision — you can paste a Marketplace URL
`https://plugins.jetbrains.com/plugin/<id>` if search is ambiguous.

Derived from the current macOS install (`plugins/` dir) plus recommendations.

## Core — install these (matches current macOS setup)

| Plugin | ID / search term | Why |
|--------|------------------|-----|
| **VSCode Keymap** | `com.intellij.plugins.vscode.keymap` → "VSCode Keymap" | Muscle memory matches your `configs/vscode` setup. Enable via Settings > Keymap > "VSCode". |
| GitHub Copilot | "GitHub Copilot" | AI completion (auth on first use — token not in repo). |
| Spring (bundled in Ultimate) | ships with Ultimate | Spring Boot run configs, beans, actuator. Just enable. |
| Python | "Python" | Full Python support (you use it alongside JVM). |
| ideolog | "Ideolog" | Log-file highlighting / folding. |
| Svelte | "Svelte" | Svelte web work. |

> `python-ce`, `ml-llm`, `ej`, `Spring` appear in your install dir but are
> either bundled, community-edition duplicates, or vendor add-ons — no separate
> Marketplace step needed on Ultimate.

## Recommended additions for Java/Kotlin (not yet installed)

| Plugin | Why |
|--------|-----|
| **google-java-format** | Byte-exact Google Java formatting; pairs with `codestyles/Google.xml`. Enable per-project. |
| **Key Promoter X** | Learns you the shortcut every time you click a toolbar button — fastest way to internalize the keymap. |
| **SonarQube for IDE** (SonarLint) | On-the-fly bug/smell detection beyond built-in inspections. |
| **Rainbow Brackets** | Nested-bracket readability. |
| **.ignore** | `.gitignore`/`.dockerignore` authoring. |
| **GitToolBox** | Inline blame, auto-fetch, branch status. |
| **String Manipulation** | Case conversion, sorting, escaping — huge time saver. |

## After install

1. Restart IDEA.
2. Settings > Keymap → select **VSCode**.
3. Enable google-java-format per project (Settings > google-java-format).
4. See `RECOMMENDATIONS.md` for how to actually use all this.
