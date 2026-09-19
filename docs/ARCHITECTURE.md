# Architecture

The project has two deliberately small parts.

## 1. Codex MCP sidecar

The sidecar exposes exactly one tool, `submit_hermes_desktop_task`. It validates bounded task text, reads the per-launch local Desktop descriptor, and sends one JSON line through the named pipe. It has no facility for command execution.

## 2. Hermes Desktop bridge

Hermes Desktop owns a named-pipe listener. Once the renderer confirms that the normal prompt pipeline is ready, it forwards an accepted request to the existing Quick Entry submit event with `target: "new"`.

The renderer—not the sidecar—creates the Hermes session and sends the prompt. This is what makes the session ordinary, visible, and durable.

## Acceptance versus completion

The MCP result means only: **Hermes Desktop accepted the task and placed it in a new visible session.** Completion, tool activity, and results live in Hermes. This avoids false success reports and preserves one source of truth.
