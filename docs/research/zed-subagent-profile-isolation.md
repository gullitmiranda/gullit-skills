# Zed native subagent profile isolation

**Checked:** 2026-07-31 against Zed's current `main` source and documentation.

## Answer

**No.** A native Zed `spawn_agent` child cannot be assigned a different Agent Profile, tool-permission policy, or sandbox policy from its parent at spawn time.

## Decisive evidence

- The [`spawn_agent` input](https://github.com/zed-industries/zed/blob/98f39bfcca6f5c1546232916f307dc062b062f64/crates/agent/src/tools/spawn_agent_tool.rs#L39-L47) accepts only `label`, `message`, and optional `session_id`; it has no profile, tool, permission, or sandbox argument.
- New child threads call [`inherit_parent_settings`](https://github.com/zed-industries/zed/blob/98f39bfcca6f5c1546232916f307dc062b062f64/crates/agent/src/thread.rs#L1299-L1326), which explicitly copies the parent's [`profile_id`](https://github.com/zed-industries/zed/blob/98f39bfcca6f5c1546232916f307dc062b062f64/crates/agent/src/thread.rs#L1428-L1441). Zed resolves the child's available tools from that inherited profile ([source](https://github.com/zed-industries/zed/blob/98f39bfcca6f5c1546232916f307dc062b062f64/crates/agent/src/thread.rs#L4109-L4119)).
- Profiles can restrict a normal Agent thread's available tools, but are not a tool-permission policy; permissions are configured separately ([official docs source](https://github.com/zed-industries/zed/blob/98f39bfcca6f5c1546232916f307dc062b062f64/docs/src/ai/agent-profiles.md)). `agent.tool_permissions` is a shared settings policy, not a child-spawn option ([official docs source](https://github.com/zed-industries/zed/blob/98f39bfcca6f5c1546232916f307dc062b062f64/docs/src/ai/tool-permissions.md)).
- Sandboxing is selected from the shared project and persistent `agent.sandbox_permissions` ([source](https://github.com/zed-industries/zed/blob/98f39bfcca6f5c1546232916f307dc062b062f64/crates/agent/src/sandboxing.rs#L193-L208)). It applies only to `terminal` and `fetch`, and sandboxed terminal commands can write inside open project directories by default ([official docs source](https://github.com/zed-industries/zed/blob/98f39bfcca6f5c1546232916f307dc062b062f64/docs/src/ai/sandboxing.md)).

Zed does support a global `subagent_model` override, but that changes only the model, not the child profile or privileges ([source](https://github.com/zed-industries/zed/blob/98f39bfcca6f5c1546232916f307dc062b062f64/crates/agent/src/thread.rs#L1321-L1325)).

## `pr-delivery` consequence

A strict read-only native child is **not possible** when its parent has write-capable tools. Use a policy-only guardrail: explicitly prohibit tool calls that mutate state, require a text-only report, and have the parent verify that no changes were made. Do not treat that prompt policy as technical isolation.

If technical tool removal is required, use a separately created Zed Agent thread with the `Ask` or `Minimal` profile rather than `spawn_agent`; it is not a differently privileged native child.

## Qualification

This reflects Zed `main` at commit [`98f39bf`](https://github.com/zed-industries/zed/commit/98f39bfcca6f5c1546232916f307dc062b062f64) on the checked date. An installed Zed version may differ, so re-check the linked source and release notes when upgrading.
