---
name: stdio-mcp-reload
description: Make edits to a stdio MCP server script take effect in live Zed threads. Use after editing code that a Zed context server runs (slack-mcp-stdio, skillsmcp, or any `context_servers` command), or when tools from an edited server keep failing with stale behavior.
---

# stdio-mcp-reload

Zed spawns one stdio MCP server process per thread session. Editing the script
does nothing to live processes: they keep the old code in memory until they are
replaced. This skill retires them safely.

## Hard Rules

- Never restart Zed and never recreate threads. Settings (profiles, tool lists,
  `context_servers` entries) hot-reload and apply on the next message; only the
  running server *processes* go stale.
- Smoke-test first, kill later. If the smoke test fails, do not kill anything:
  a live process running old code beats no server. Fix the script first.
- Kill only processes whose command line matches the edited script's path. List
  them and confirm every PID before killing; nothing else.
- Smoke tests must not print tokens or other secrets. Bound output with
  `head`/`tail`.

## Procedure

1. Smoke-test the edited script standalone (no Zed involved) with a minimal MCP
   handshake. For `slack-mcp-stdio`:
   `printf '%s\n%s\n%s\n' '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2025-03-26","capabilities":{},"clientInfo":{"name":"smoke","version":"0"}}}' '{"jsonrpc":"2.0","method":"notifications/initialized"}' '{"jsonrpc":"2.0","id":2,"method":"tools/list"}' | bin/slack-mcp-stdio 2>/dev/null | head -3`
   Expect the initialize result and a tools list. Adapt the handshake for
   servers with a different protocol surface.
2. List live instances: `ps -eo pid,etime,command | grep '[<script-path>]'`.
3. Kill every instance — all of them run pre-edit code — then verify the same
   `ps` command returns nothing.
4. Report: threads respawn a fresh server on their next message. If a thread's
   tools do not return, restart the server from Settings -> AI -> MCP Servers.
   If the current session itself uses the server, expect its calls to fail
   until the next message respawns it.
