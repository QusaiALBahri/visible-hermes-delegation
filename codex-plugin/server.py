"""MCP sidecar for visible, local Hermes Desktop delegation on Windows."""

from __future__ import annotations

import json, os, secrets, sys
from pathlib import Path

DESCRIPTOR = Path(os.environ.get("APPDATA", "")) / "Hermes" / "codex-desktop-bridge.json"
MAX_TASK_CHARS = 8_000

def send(message):
    sys.stdout.write(json.dumps(message, ensure_ascii=True) + "\n")
    sys.stdout.flush()

def submit(arguments):
    task = arguments.get("task")
    if not isinstance(task, str) or not task.strip() or len(task) > MAX_TASK_CHARS:
        raise ValueError("task must be non-empty and at most 8,000 characters")
    try:
        descriptor = json.loads(DESCRIPTOR.read_text(encoding="utf-8"))
        pipe_name, capability = descriptor["pipeName"], descriptor["capability"]
    except (OSError, ValueError, KeyError, TypeError) as exc:
        raise RuntimeError("Hermes Desktop is not running with Visible Hermes Delegation enabled.") from exc
    request_id = secrets.token_urlsafe(12)
    payload = json.dumps({"requestId": request_id, "text": task.strip(), "capability": capability}).encode() + b"\n"
    try:
        with open(pipe_name, "r+b", buffering=0) as pipe:
            pipe.write(payload)
            response = json.loads(pipe.read(4096).decode().strip())
    except (OSError, ValueError, UnicodeDecodeError) as exc:
        raise RuntimeError("Could not reach the Hermes Desktop bridge.") from exc
    if response.get("accepted") is not True:
        raise RuntimeError(str(response.get("reason") or "Hermes did not accept the task."))
    return {"content": [{"type": "text", "text": f"Submitted to a new visible Hermes Desktop session. Tracking ID: {request_id}. The complete execution record remains in Hermes."}], "isError": False}

TOOL = {"name": "submit_hermes_desktop_task", "description": "Create a visible Hermes Desktop session and submit one task through Hermes normal chat pipeline.", "inputSchema": {"type": "object", "additionalProperties": False, "properties": {"task": {"type": "string", "minLength": 1, "maxLength": MAX_TASK_CHARS}}, "required": ["task"]}}

def main():
    for line in sys.stdin:
        request = {}
        try:
            request = json.loads(line)
            method, message_id = request.get("method"), request.get("id")
            if method == "notifications/initialized": continue
            if method == "initialize":
                send({"jsonrpc": "2.0", "id": message_id, "result": {"protocolVersion": "2024-11-05", "capabilities": {"tools": {}}, "serverInfo": {"name": "visible-hermes-delegation", "version": "0.1.0"}}})
            elif method == "tools/list": send({"jsonrpc": "2.0", "id": message_id, "result": {"tools": [TOOL]}})
            elif method == "tools/call" and (request.get("params") or {}).get("name") == TOOL["name"]:
                send({"jsonrpc": "2.0", "id": message_id, "result": submit((request.get("params") or {}).get("arguments") or {})})
            else: send({"jsonrpc": "2.0", "id": message_id, "error": {"code": -32601, "message": "Unsupported method"}})
        except (ValueError, RuntimeError) as exc:
            send({"jsonrpc": "2.0", "id": request.get("id"), "error": {"code": -32602, "message": str(exc)}})

if __name__ == "__main__": main()
