---
name: zeropath
description: Triage and work ZeroPath security findings/issues, using the ZeroPath CLI for supported interactions and running scans only when explicitly requested or needed for validation. Use when the user mentions ZeroPath, zeropath, ZeroPath findings, security scan results, or URLs under https://zeropath.com/.
---

# ZeroPath

Use this skill for ZeroPath security findings, existing scan results, PRs that
address ZeroPath issues, explicit scan requests, and any text that references
`https://zeropath.com/`.

## Hard Rules

- Always use the `zeropath` CLI for communication with ZeroPath.
- Before relying on a ZeroPath command, check the current CLI surface with
  `zeropath --help` or `zeropath <command> --help`.
- Do not use browser automation, manual HTTP calls, MCP tools, scraping, or UI
  navigation for ZeroPath while a CLI path exists.
- If the CLI is missing, unauthenticated, or does not support the requested
  action, stop and report the blocker. Do not improvise with direct API calls.
- Do not trigger a new ZeroPath scan by default.
- Never expose `clientSecret`, API tokens, CI secrets, or sensitive finding
  payloads in chat, docs, PR bodies, issue bodies, or comments.

## Default Posture: Existing Findings First

- The default job is to evaluate, fix, document, or discuss existing ZeroPath
  findings supplied by the user, a PR body/comment, commit context, CLI output,
  SARIF, or another existing scan result.
- Do not add ZeroPath scans to unrelated work, normal PR creation, or generic
  security review tasks.
- Do not run a new scan just because a PR or document mentions ZeroPath.
- Run a ZeroPath scan only when:
  - The user explicitly asks for a scan.
  - The task is to validate a ZeroPath fix and scan validation is necessary and
    practical.
  - The repository's established workflow requires a scan for this specific
    ZeroPath task.
- If a new scan may be remote, expensive, slow, or noisy, state that before
  running it unless the user already asked directly.

## Links and References

- In chat replies, documents, PR bodies, issue bodies, comments, release notes,
  and changelogs, always write ZeroPath finding URLs as complete visible URLs.
- Canonical issue URL format: `https://zeropath.com/app/issues/<uuid>`.
- Do not use UUID-only references, shortened links, hidden markdown labels like
  `[View](https://zeropath.com/app/issues/<uuid>)`, or vague references like
  `ZeroPath 6.3` without the full finding URL when the finding URL is known.
- If the finding URL is unknown, ask for it or use the CLI to obtain it when the
  CLI supports that action.

## CLI Workflow

1. Confirm the CLI is available:

   ```bash
   zeropath --help
   ```

2. For existing findings, use user-supplied URLs, PR/comment context, CLI output,
   or SARIF as the source of finding details. If more details are needed and the
   CLI does not expose a read/list operation, ask the user for the missing
   ZeroPath details or full finding URL.

3. For scan work, inspect the scan command first:

   ```bash
   zeropath scan --help
   ```

4. Prefer repo-based scans when the repository URL and branch are known:

   ```bash
   zeropath scan --repository-url <repo-url> --vcs github --branch <branch>
   ```

5. Use local scans only when repo-based scan is not appropriate or the user asks
   for a local SARIF artifact:

   ```bash
   zeropath scan <directory> <output.sarif>
   ```

6. Treat SARIF and scan output as local evidence until reviewed. Do not publish
   raw output that may include secrets, PII, absolute machine paths, or unrelated
   findings.

## Triage

When triaging a finding, capture only useful, non-sensitive facts:

- Full ZeroPath finding URL, if known.
- Severity and affected component.
- File or code area, avoiding absolute machine paths in public output.
- Data class involved, such as token, PII, card data, auth bypass, or injection.
- Exploitability signal and whether the finding appears actionable.
- Minimal fix and validation evidence.

If the finding looks like a false positive or accepted risk, state the evidence
briefly and avoid changing code solely to satisfy noise.

## PR and Issue Wording

- Only mention ZeroPath in PRs, issues, or comments when the work is actually
  related to ZeroPath or the draft already references a ZeroPath finding.
- Use wording like: `Addresses ZeroPath finding: https://zeropath.com/app/issues/<uuid>`.
- Do not say ZeroPath confirmed a finding is resolved unless that was verified
  through the CLI or another explicit ZeroPath result supplied by the user.
- If the code was changed but ZeroPath has not re-scanned yet, say that the
  change addresses the finding pattern and is awaiting ZeroPath re-scan.
