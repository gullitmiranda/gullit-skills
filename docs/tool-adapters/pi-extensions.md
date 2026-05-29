# Pi Extensions Adapter

Pi-style extensions are useful as runtime helpers around an agent. This repo
does not require Pi, but borrows several workflow ideas from Pi setups.

## Useful Extension Patterns

### Transcript copy

Examples such as `copy-all` are useful when exact conversational history must
move to another tool.

Default: prefer a context capsule. Use transcript copy only for audit,
debugging agent behavior, or preserving unstructured discussion before it can be
summarized.

### Changed-file tracking

Diff tracking after an agent run helps review and handoff:

- What files changed?
- Which changes came from this run?
- Which file should the user inspect first?

This pattern is useful for future automation, but the portable fallback is to
ask the executing agent to return changed files explicitly.

### Usage and cost reporting

Usage summaries help understand agent runtime cost and context behavior. Keep
these as optional operational tools, not workflow prerequisites.

### Runtime status

Status indicators such as tokens-per-second or current model help users notice
slow or stuck sessions. They are quality-of-life improvements, not core
workflow state.

### MCP and web tooling

MCP and web extensions can broaden a terminal agent's capabilities. Keep their
configuration tool-specific and document only the workflow assumption:

- If a workflow requires a service, confirm the tool has that service.
- If not, hand off only the part that can be completed with available tools.

## What To Record In This Repo

Record:

- Transfer principles.
- Adapter guidance.
- References to useful external setups.
- Future automation ideas.

Do not record:

- Tool-specific secrets.
- Local session logs.
- Copied transcripts.
- Extension source code from external repos.

## Future Candidates

Only promote an adapter idea into a local extension after it is repeatedly
useful. Good candidates:

- Create context capsule from current session.
- Track changed files from last agent run.
- Show active workstream and branch.
- Summarize validation evidence.
