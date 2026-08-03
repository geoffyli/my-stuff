# Secrets & machine-local state — do NOT commit

IntelliJ scatters credentials and machine paths across `options/*.xml`. Unlike
VS Code, there is no single settings file, so the rule is **allowlist, not
blocklist**: only the curated files under `settings/` get committed. Everything
below is either gitignored (`.gitignore`) or simply never copied into the repo.

## Never commit

| File / dir | Why |
|------------|-----|
| `idea.key`, `*.key` | **IntelliJ Ultimate license key.** Personal, non-transferable. |
| `options/github-copilot*.xml`, `options/llm.*.xml`, `options/AIAssistant*.xml` | AI-assistant auth tokens & session state. |
| `grazie/`, `options/grazie*.xml` | Grazie/AI service state. |
| `options/database*.xml`, `dataSources*`, `jdbc-drivers/` | **DB hosts, users, sometimes passwords.** |
| `options/jdk.table.xml` | Absolute SDK paths — machine-specific, regenerate per box. |
| `options/path.macros.xml`, `recentProjects.xml`, `trusted-paths.xml` | Local filesystem paths. |
| `options/proxy.settings.xml` | May contain proxy creds. |
| `workspace/`, `tasks/`, `*.db`, `migration/` | Per-install runtime state, not config. |

## Credentials that are NOT in these files (safe by design)

IntelliJ stores most real passwords in the OS keychain (macOS Keychain /
Windows Credential Manager), not in XML. Those never touch the repo. You will
re-enter them on the work box the first time you use each tool (DB, Git push,
AI assistant, license).

## HTTP Client env files (if you use the Ultimate HTTP Client)

Keep private values out of the repo:

- `http-client.env.json` — safe, shared, non-secret defaults → **may commit** (per-project, not here).
- `http-client.private.env.json` — tokens/keys → **gitignore in the project**, never here.

## Setting up on the Windows work box

1. Sign in to your JetBrains account → Ultimate license activates (no key file needed).
2. Re-enter DB passwords / AI tokens on first use.
3. Run `apply.ps1` to drop the curated, non-secret settings into place.
