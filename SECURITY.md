# Security policy

## Design boundaries

This project must never:

- expose a listener beyond the local computer;
- extract Hermes gateway tokens, OAuth credentials, or API keys;
- turn an MCP request into arbitrary shell execution;
- claim that a task completed when Hermes only accepted it.

The bridge uses a random Windows named-pipe endpoint plus a per-launch capability. Both disappear when Hermes exits. The MCP server returns an acceptance and tracking ID; the authoritative execution record is the visible Hermes session.

## Reporting a vulnerability

Do not open a public issue for a credential, authorization, or local privilege concern. Contact the maintainer privately with a minimal reproduction and redact any secrets.

## Shared computers

Do not install the reference implementation on a shared Windows account. The design assumes the operating-system user account is the trust boundary.
