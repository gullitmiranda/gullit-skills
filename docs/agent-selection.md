# Agent Selection

Agent selection decides where the next step should run before substantial work
starts. The goal is to match the task shape to the runtime, not to force every
task through the same IDE chat.

If the current state is unclear, run `workflow-intake` first. Intake identifies
workstreams and then calls into this decision layer.

## Inputs

Consider these factors before choosing a runtime:

- Task length: short, medium, or long-running.
- Feedback style: conversational, IDE-interactive, test-harness-driven, or batch.
- Isolation need: same branch, separate worktree, forked thread, or external workspace.
- Context need: one fact, context capsule, inherited thread, or full transcript.
- Risk: destructive commands, broad edits, secrets, data boundary, or CI impact.
- Ownership: main chat supervision, child agent execution, or human-in-the-loop.
- Autonomy readiness: implementation-ready, collaborative, or discovery-first.

## Default Choices

| Work type | Default runtime | Why |
| --- | --- | --- |
| Product or architecture decision | Main chat | Keeps the durable decision close to the user. |
| Domain grilling | Main chat | Requires tight user feedback and terminology alignment. |
| Codebase reconnaissance | Subagent | Keeps exploration noise out of the parent context. |
| Parallel side question | Subagent | Returns a distilled answer without polluting the main thread. |
| Side path becomes main path | Cursor fork or new Zed thread | Preserves enough context while giving the path its own thread. |
| Focused implementation | Cursor or Zed agent | Works well when IDE feedback and file review matter. |
| Long implementation | Terminal, ACP, or Pi-style agent | Better for isolated, long-running, or mechanical execution. |
| Implementation-ready work | Most autonomous safe runtime | Prefer autonomous execution when decisions and validation are clear. |
| Discovery, grilling, or unresolved decisions | Main chat | Requires user judgment before autonomous execution is safe. |
| Harness-driven debugging | Terminal agent or IDE agent | Choose terminal when the loop is command-driven; IDE when interactive inspection matters. |
| CI watch/fix loop | Background watcher or terminal agent | Avoids tying up the main chat with polling. |
| PR preparation | Main chat or IDE agent | Needs synthesis, diff awareness, and concise review framing. |
| Tool switch or resume | Context capsule | Gives any agent the minimum useful state. |
| Audit or exact history transfer | Full transcript copy | Use only when exact wording matters. |

## Decision Tree

```text
1. Does the next step require user judgment now?
   -> Yes: main chat.

2. Is this a bounded investigation whose output is a short finding?
   -> Yes: subagent.

3. Did a side investigation become the primary path?
   -> Yes: fork or start a new thread with a context capsule.

4. Is the task long-running, mechanical, or likely to involve many tool calls?
   -> Yes: hand over to terminal/ACP/Pi-style agent with a context capsule.

5. Is the implementation ready for autonomous execution?
   -> Yes: choose the most autonomous safe runtime and pass a context capsule.

6. Does the task need tight IDE feedback, visual inspection, or manual review?
   -> Yes: Cursor or Zed agent.

7. Is the work a CI/watch/fix loop?
   -> Yes: background watcher or terminal agent.

8. Otherwise:
   -> Keep it in the current agent and create a capsule only if the work branches.
```

## Runtime Profiles

### Main chat

Best for:

- Decisions.
- User interviews.
- Final synthesis.
- Prioritization and trade-off discussion.

Avoid for:

- Long-running implementation.
- Noisy codebase exploration.
- Polling loops.

### Cursor subagent

Best for:

- Parallel codebase exploration.
- Research questions.
- Review of a bounded area.
- Side branches that return a distilled result.

Avoid for:

- Work that requires the parent to see every intermediate step.
- Long implementation that should own its own branch/worktree.

### Cursor fork

Best for:

- Turning a side branch into the new main conversation.
- Preserving rich inherited context without continuing to burden the old parent thread.

Avoid for:

- Small investigations that can return one paragraph.

### Zed agent

Best for:

- Interactive implementation when Zed is the active editor.
- Starting a clean thread from a summary.
- Trying a different ACP or terminal-backed agent while keeping the editor loop.

Avoid for:

- Work that only needs a short subagent answer in Cursor.

### Terminal, ACP, or Pi-style agent

Best for:

- Long implementation.
- Large mechanical edits.
- Test-harness-driven debugging.
- Isolated execution with a clear context capsule.
- Tooling experiments and custom extensions.

Avoid for:

- Product decisions that need live user alignment.
- Ambiguous work without a capsule or plan.

### Full transcript transfer

Best for:

- Exact-history audit.
- Debugging agent behavior.
- Preserving unstructured discussion before it can be summarized.

Avoid for:

- Normal implementation handoff.
- Work where a context capsule is enough.

## Escalation Rules

Escalate from the current runtime when:

- The task grows beyond the current context budget.
- The next step would create a lot of noisy exploration.
- The work needs its own branch, worktree, or tool loop.
- The agent is blocked because the current tool lacks required capabilities.
- The side path is now more important than the original path.

Before escalating, create or update a context capsule.

## Required Output

When recommending a runtime, say:

- Recommended runtime.
- Autonomy mode.
- Why it fits this phase.
- What context to pass.
- What result should come back.

Example:

```text
Recommended runtime: terminal agent.
Autonomy mode: autonomous.
Why: this is a long, harness-driven implementation with repeated test runs.
Context: pass the context capsule plus the target branch/worktree.
Expected return: changed files, commands run, validation result, blockers.
```
