# Visible Hermes Delegation

![Two AI collaborators exchanging a task card](assets/hero.png)

**Delegate a task from Codex to Hermes without losing the audit trail.**

Visible Hermes Delegation creates a new, ordinary Hermes Desktop session for every delegation. The task, progress, tools used, and final result remain in Hermes where a human can inspect them. Codex orchestrates; Hermes executes; neither leaves a hidden background run behind.

> العربية: كل تفويض ينشئ جلسة ظاهرة داخل Hermes ويحفظ فيها الرسالة والنتيجة كاملة.

## Why this exists

Agent handoffs often trade observability for automation. A fast worker may finish a task in a terminal or a private backend run, leaving the person who requested it without a readable record.

This project uses Hermes Desktop's **normal message-submission path**. It is deliberately not screen automation, not clipboard pasting, and not a scraper for Hermes's private WebSocket credentials.

## What you get

| Component | Responsibility |
| --- | --- |
| `codex-plugin/` | MCP tool: `submit_hermes_desktop_task` |
| `hermes-desktop-patch/` | A narrow local bridge owned by Hermes Desktop |
| `assets/hero.png` | Repository hero image |
| `docs/` | Installation, architecture, and security guidance |

## Flow

```text
Codex request
  -> local MCP sidecar
  -> per-launch Windows named pipe
  -> Hermes Desktop
  -> new visible Hermes session
  -> normal Hermes execution transcript
```

Every submitted task carries a short tracking ID in its first message, for example:

```text
[Codex delegation · AbCdEf123456]

Review the draft and produce a concise report.
```

## Security model

- No HTTP server and no exposed network port.
- No scraping, copying, or logging of Hermes gateway/WebSocket credentials.
- A fresh named-pipe name and capability are generated for each Hermes Desktop launch.
- The MCP tool accepts one bounded text task only; it does not expose arbitrary shell execution.
- Hermes remains the visible system of record for delegated work.

Read [SECURITY.md](SECURITY.md) before installing this on a shared machine.

## Status

This is a **Windows reference implementation**. The Codex side is packaged as an MCP plugin; the Hermes side is a small Desktop integration patch intended to become an upstream Hermes capability. Do not distribute a rebuilt unsigned Hermes executable. Build from trusted source or wait for an upstream release.

## Quick start

1. Install Hermes Desktop from a trusted source and keep it running.
2. Apply and build the Desktop integration in `hermes-desktop-patch/` from the Hermes source tree.
3. Install `codex-plugin/` as a local Codex plugin.
4. In a new Codex task, call `submit_hermes_desktop_task` with the work request.
5. Open Hermes: a new session contains the original task and its outcome.

Detailed steps: [Windows installation guide](docs/INSTALL-WINDOWS.md).

## Example

**Codex:** “Open a new Hermes session and analyse these CSV files. Produce a draft, then stop for review.”

**Result:** Hermes creates a normal visible session, performs the task with its configured tools and models, and keeps the full transcript in that session. Codex can then review the result and decide what to do next.

## Contributing

Contributions should preserve three rules: visible sessions, local-only transport, and no private-token scraping. See [architecture notes](docs/ARCHITECTURE.md).

## License

MIT. See [LICENSE](LICENSE). Hermes itself is separately licensed by Nous Research under MIT.
