# Review Completion Manifest

`pr-delivery` builds this small JSON value after every reviewer for a fixed PR
head has returned. Keep it in the parent workflow state and pass its serialized
contents to `pr-babysit` in the handoff capsule. Do not publish it in PR
content or treat it as a substitute for the reviewer's actual result.

```json
{
  "pr_url": "<pr-url>",
  "expected_head_sha": "<head-sha>",
  "reviewed_head_sha": "<head-sha>",
  "completion": "complete",
  "sessions": [
    {
      "id": "<runtime-session-id>",
      "kind": "initial|delta",
      "status": "reviewed",
      "reviewed_head_sha": "<head-sha>"
    }
  ]
}
```

The parent may set `completion` to `complete` only when the manifest contains
at least one session and every listed session has `status: reviewed` with a
terminal successful result for the exact `reviewed_head_sha`. A reviewer
failure, timeout, malformed result, SHA mismatch, or pending user decision must
prevent manifest creation and stop the delivery flow.

`pr-babysit` validates the serialized manifest: its PR URL and both SHAs must
match its arguments, completion must be `complete`, the session list must be
non-empty, and every session must be terminal, `reviewed`, and pinned to the
requested SHA before it watches or changes the PR.
