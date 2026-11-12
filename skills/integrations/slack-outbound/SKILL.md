---
name: slack-outbound
description: >-
  Compose, draft, or send Slack messages for a destination audience. Use when
  preparing, drafting, or posting Slack messages, replies, announcements, or PR
  review requests — including when using Slack MCP send/draft tools.
---

# Slack Outbound

Write for the people who will read the message in Slack, not for this chat.

## Hard Rules

- Resolve the destination first: channel, DM, or thread (URL, name, or ID).
- Before drafting, read destination context when tools allow: thread parent +
  replies, or recent channel messages. If tools are unavailable, ask for the
  URL/paste or state that the draft is ungrounded.
- Never assume chat-only shared context. Ban: "as we discussed", "the PR",
  "the fix", "the issue" without a public referent (link, ID, or one-line
  restatement a stranger in that channel would understand).
- Print the exact message text in chat before calling any Slack write tool, so
  the wording and destination are reviewable as a preview instead of as raw tool
  input. Print, then proceed in the same turn: do not end the turn waiting for
  approval. Still prefer `slack_send_message_draft` over a direct send, since
  the Slack draft is the review gate.
- Apply `publish-safe-links` and `data-boundary` before any draft or send.
- Keep formatting guidance in the Cursor Slack plugin `slack-messaging` skill;
  this skill owns audience and grounding.
- Never write GitHub PRs or issues as `#123` or `repo#123`. Include the title
  and the full `https://github.com/<owner>/<repo>/pull/<n>` (or `/issues/<n>`)
  URL. Naming the repo in the sentence does not replace the URL. Do not wrap
  the URL in inline code or otherwise obscure it.
- Deliver the chat preview and any draft as raw Slack mrkdwn inside a fenced code block so copy/paste works as a snippet: plain *bold* bullets, raw URLs, never rendered chat markdown or [text](url) syntax.
- Default to short. If the message fits in one or two lines, it must not become
  a paragraph; length needs a reason the reader can act on.

## PR Review Requests

A review request is a ping, not a report. The PR title and description already
carry scope, and the thread already carries the previous context; restating
them turns the channel into a newsletter.

- Default shape: one line of what changed plus the ask, then the full PR URL.

```
Fixes stale restart-panel data on the runners dashboard — review?
https://github.com/<owner>/<repo>/pull/<n>
```

- Do not restate the PR body: scope, rollout steps, deployment flow, checklists,
  or "closing the loop on the previous PR". One line of explanation is usually
  more than enough.
- Reply in the existing thread when one covers the same change; never re-explain
  what that thread already says.
- Elaborate only when the request needs it — the user asked for detail, or
  omitting a fact would mislead the reviewer (non-obvious risk, rollback or
  sequencing caveat, a decision they must make). Even then, pick one: a short
  line inside the request itself, or a follow-up reply in the request's thread.

## Procedure

1. **Destination.** Identify where it posts and whether it is a new top-level
   message or a thread reply.
2. **Ground.** Read recent destination context. Note what the audience already
   knows and what is still private to this chat.
3. **Audience rewrite.** Lead with the point. Include: who/what, why it
   matters here, next step or ask, and clickable public links. Match channel
   tone from the recent messages, not from this conversation.
4. **Ship posture.** Print the exact message, then call the tool in the same
   turn — `slack_send_message_draft` by default, a direct send only when the user
   asked to send as-is. Do not stop the turn to wait for approval. After send,
   return the message permalink when available.

## Permalinks

A Slack permalink already identifies the destination; parse it instead of
searching by name, which fails for private channels, DMs, and lists the search
index does not cover.

- `.../archives/<channel_id>/p<ts>` gives the channel ID plus `thread_ts`
  (dot before the last six digits: `p1794343236340939` becomes
  `1794343236.340939`).
- `.../lists/<team_id>/<list_id>` gives the list ID directly.
