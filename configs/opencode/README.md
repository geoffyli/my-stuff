# OpenCode Config

Portable OpenCode v1 setup, applied inside the GCP Workstation (Linux) that
OpenCode actually runs on. The work Windows laptop never runs OpenCode
directly — it SSHes into the workstation and uses OpenCode there.

## Topology

```
Windows laptop (Chrome, SSH client)
   │  ssh -R 9222:localhost:9222 <workstation>   (forward local Chrome debug port to remote)
   ▼
GCP Workstation (Linux)
   │  OpenCode v1 runs here, with chrome-devtools MCP pointed at 127.0.0.1:9222
   ▼
chrome-devtools-mcp --browserUrl=http://127.0.0.1:9222
   → drives the Chrome instance actually open on the Windows laptop
```

OpenCode's own config, agents, and rules live in this repo and are
symlinked into `~/.config/opencode` on the workstation, so `git pull` is
the only update step.

## Layout

| File | Purpose |
|------|---------|
| `opencode.json` | Global OpenCode config: instructions + MCP servers (chrome-devtools). No secrets. |
| `apply.sh` | Linux apply script — symlinks config, agents, and AGENTS.md into `~/.config/opencode`. |

Agent definitions live at repo root in `agents/*.md` (shared with Claude
Code — see below), not duplicated here. Global rules live in
`instructions/AGENTS.md`.

## Apply (on the workstation)

```bash
cd my-stuff/configs/opencode
./apply.sh            # symlink opencode.json, agents/, AGENTS.md
./apply.sh --dry-run   # preview, write nothing
```

This creates:
- `~/.config/opencode/opencode.json` → `configs/opencode/opencode.json`
- `~/.config/opencode/AGENTS.md` → `instructions/AGENTS.md`
- `~/.config/opencode/agents/` → `agents/`

Symlinks mean a `git pull` in the repo updates the live config immediately
— no re-run of `apply.sh` needed unless a *new* file was added (in which
case re-run to pick up the new symlink).

## Agents are dual-format

`agents/*.md` at repo root carry YAML frontmatter that both Claude Code and
OpenCode v1 understand:

```yaml
---
name: deep-worker
description: "..."
tools: Read, Grep, Glob, Bash, Edit, Write, Agent   # Claude Code field
model: inherit                                       # Claude Code field (ignored by OpenCode)
mode: subagent                                       # OpenCode field
permission:                                          # OpenCode field
  edit: allow
  bash: allow
---
```

Claude Code reads `name`/`description`/`tools`/`model`; OpenCode reads
`description`/`mode`/`permission` from the same file and ignores the rest.
One file, both tools — edit once, applies everywhere.

`model: inherit` has no OpenCode equivalent, so it's simply omitted from
what OpenCode reads — the agent runs on whatever model the parent session
is using, which is the same intent.

## Chrome DevTools bridge (Windows Chrome ← Workstation OpenCode)

Verified 2026-09-17: OpenCode on the workstation can drive the real Chrome
browser open on the Windows laptop, via `chrome-devtools-mcp` connected to
a port-forwarded remote-debugging socket.

### One-time setup

**1. Launch Chrome on Windows with remote debugging enabled.** Chrome must
be started with the debug port open (not toggleable after launch):

```powershell
& "C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9222
```

**2. Forward the port to the workstation over the existing SSH session.**
Using `-R` (remote forward) so the *workstation's* `127.0.0.1:9222` reaches
back to the laptop's `127.0.0.1:9222`:

```powershell
ssh -R 9222:localhost:9222 <user>@<workstation-host>
```

(If connecting through `gcloud workstations ssh` / IAP tunneling instead of
raw `ssh`, add the equivalent local-to-remote port forward flag for that
tool — the forwarding direction is what matters, not the transport.)

**3. `chrome-devtools` MCP server is already wired into `opencode.json`**
in this repo (see above), pointed at `http://127.0.0.1:9222` — the
workstation's local view of the forwarded port. No further config needed
once `apply.sh` has run.

### Why this matters

This turns OpenCode running on a headless-ish Linux workstation into a
full browser-automation agent against the *actual* Chrome the user is
looking at on Windows — no separate headless/remote browser instance to
keep in sync, no screenshots relayed manually. Screenshots, clicks,
console logs, and network inspection all happen against the real session.

### Gotchas

- The SSH port-forward must be re-established every new SSH session (`-R`
  forwards aren't persistent). If chrome-devtools MCP fails to connect,
  check the forward is still up before debugging the MCP config.
- Chrome must be the one launched with `--remote-debugging-port` — a
  regular already-running Chrome window will *not* expose the debug port
  retroactively. Close and relaunch with the flag if needed.
- Port 9222 is a convention here, not a requirement — if it's already in
  use on either end, pick another port and update both the `ssh -R` flag
  and `--browserUrl` in `opencode.json` to match.
