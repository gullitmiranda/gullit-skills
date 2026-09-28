---
name: cursor-zed-handoff
description: Continue a Cursor conversation in Zed from its ID, or coordinate thread titles and archiving across both editors. Use for selective cross-editor handoffs and closeout, not bulk migration.
---

# Cursor-Zed Handoff

Keep work resumable in either editor while transferring only the context needed now.

## Hard Rules

- A handoff is not a move or a closeout. Do not archive either conversation merely because work continues in the other editor.
- Never edit Cursor or Zed internal databases, transcript files, or UI state. A skill cannot rename or archive a thread through a CLI that does not support it; recommend verified UI steps instead.
- Distinguish local Cursor conversation UUIDs from Cloud Agent IDs (`bc-...`). The Cloud Agents archive API does not apply to local conversations; use it only for an explicitly requested, verified Cloud Agent after confirming the consequences with the user.
- Do not copy full transcripts, secrets, or work context into another repository or a public artifact. Keep IDs and editor-specific paths in the chat unless the user asks for a safe durable handoff.

## Procedure

1. Get the Cursor conversation ID, project path if needed, and the user's intended next action. Locate the matching local transcript under `~/.cursor/projects/*/agent-transcripts/<id>/`; if missing, investigate read-only storage or ask for context rather than inventing a transcript.
2. Extract the decisions, constraints, pending work, relevant paths, and blockers. Compare with the current repository and worktree state; treat old validation and reported completion as stale until rechecked. For a portable handoff, use `context-capsule` rather than pasting chat history.
3. Suggest a short Zed thread title describing the project and current task, not just the Cursor ID. The user can edit it by clicking the title in the Agent Panel. If work later returns to Cursor, provide the same concise context in reverse.
4. Report the state of each thread separately: keep active if there is unfinished work or an expected return; suggest archiving only after the handoff is confirmed or the work is truly finished. In Zed, the user can archive a finished thread from the Threads Sidebar and restore it from Thread History. For local Cursor conversations, offer archive instructions only when verified in the installed UI; otherwise say that automation is unconfirmed. Never delete either conversation as part of a handoff.

Zed UI references: [titles](https://zed.dev/docs/ai/agent-panel#thread-titles), [thread history](https://zed.dev/docs/ai/parallel-agents#thread-history). Cloud Agent lifecycle: [Cursor API](https://cursor.com/docs/cloud-agent/api/endpoints.md#archive-an-agent).
