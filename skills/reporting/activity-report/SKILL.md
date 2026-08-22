---
name: activity-report
description: Generate evidence-based activity reports from Slack, GitHub, and Linear. Use for daily, weekly, standup, catch-up, and contribution summaries.
---

# Activity Report

Generate concise work reports that reconcile delivery evidence with tracker status.

## Hard Rules

- Default sources are Slack, GitHub, and Linear. State every unavailable source and never infer its missing data.
- Use GitHub as delivery evidence and Linear as the work-tracking source. When they disagree, describe the discrepancy instead of silently choosing one.
- Group the report by project, workstream, or business outcome, never by source.
- Every material claim needs an exact `YYYY-MM-DD` event date and a full source URL when available. An update date proves activity, not completion.
- Do not create or update GitHub, Linear, or Slack records while gathering a report.
- Present the report directly. Save a file only when the user requests a persistent artifact.

## Procedure

1. **Scope the report.** Resolve the target person, inclusive date range, requested language, and requested sources. For another person, resolve Slack identity, email, GitHub login, and Linear identity when available.

2. **Gather evidence.** Query sources in parallel after confirming access.
   - **Slack:** collect authored messages, mentions, and decision or blocker threads.
   - **GitHub:** collect authored and reviewed pull requests, commits, and issues. Record creation, merge, close, and current-state timestamps separately.
   - **Linear:** collect issues created by and assigned to the target that changed in the period, including completed issues. Capture title, project or team, status, start date, completion date, update date, dependencies, and URL. Also inspect currently started issues.

3. **Reconcile status.** Link pull requests and issues to their Linear records and relevant Slack context. Use `Done` only with a completed Linear status or merge evidence. Keep `In Review`, `In Progress`, `Triage`, `Backlog`, and `Blocked` exactly as tracked. If a merged pull request still has a stale tracker state, report both facts and flag tracker reconciliation.

4. **Write the report.** Use the requested language and this structure:

   ```markdown
   # Work Report - [YYYY-MM-DD] to [YYYY-MM-DD]

   **Sources:** [available sources]
   **Coverage note:** [unavailable or incomplete sources]

   ## Executive Summary
   [Completed outcomes, active work, and the main risk or decision.]

   ## Workstreams
   ### [Project or outcome]
   **Goal:** [Why it matters.]
   - [YYYY-MM-DD] [Action or decision], supported by [source](URL).

   | Status dimension | Current state | Evidence and date |
   | --- | --- | --- |
   | Technical delivery | Merged, open, closed, or not applicable | [Pull request](URL), YYYY-MM-DD |
   | Tracker | Done, In Progress, In Review, Triage, Backlog, Blocked, or unavailable | [Issue](URL), YYYY-MM-DD |

   **Next step or blocker:** [Specific action, dependency, owner, or None known.]

   ## Items Requiring Attention
   - **[Workstream] - [status]:** [why], [date], [link].
   ```

## Date and Status Rules

- Use the merge date for a merged pull request, the completion date for a completed issue, and the creation date for newly scoped work.
- Use an update date only when no stronger event date exists, and label it as an update.
- A closed pull request without merge evidence is closed, not delivered.
- Triage and Backlog mean scoped or planned work, not active implementation.
- Mention counts only as supporting evidence; do not let counts replace status and outcomes.
