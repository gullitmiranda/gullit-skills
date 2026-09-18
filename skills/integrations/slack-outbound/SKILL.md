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
- Prefer `slack_send_message_draft` over send. Send only with explicit user
  confirmation of the final text and destination.
- Apply `publish-safe-links` and `data-boundary` before any draft or send.
- Keep formatting guidance in the Cursor Slack plugin `slack-messaging` skill;
  this skill owns audience and grounding.
- Never write GitHub PRs or issues as `#123` or `repo#123`. Include the title
  and the full `https://github.com/<owner>/<repo>/pull/<n>` (or `/issues/<n>`)
  URL. Slack's GitHub app rewrites a raw GitHub URL into `#123`; wrap that
  full URL in inline code so the URL stays visible. Naming the repo in the
  sentence does not replace the URL.

## Procedure

1. **Destination.** Identify where it posts and whether it is a new top-level
   message or a thread reply.
2. **Ground.** Read recent destination context. Note what the audience already
   knows and what is still private to this chat.
3. **Audience rewrite.** Lead with the point. Include: who/what, why it
   matters here, next step or ask, and clickable public links. Match channel
   tone from the recent messages, not from this conversation.
4. **Ship posture.** Show the draft (or create a Slack draft). Wait for
   confirmation before sending. After send, return the message permalink when
   available.
