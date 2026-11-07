---
name: slack-outbound
description: >-
  Compose, draft, or send Slack messages for a destination audience. Use when
  preparing, drafting, or posting Slack messages, replies, or announcements —
  including when using Slack MCP send/draft tools.
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
