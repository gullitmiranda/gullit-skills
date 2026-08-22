---
name: data-boundary
description: >-
  ALWAYS use before writing, editing, committing, or pushing in any personal or
  public repository. Prevent employer, client, or private identifiers from
  leaking outside their authorized context.
---

# Data Boundary Guard

## Rules

- Fail closed when in doubt.
- Prefer omission over speculative sanitization.
- Keep reusable behavior separate from context-specific configuration.
- Do not assume that public availability makes copying or republishing authorized.

## Purpose

Keep information in the context where it is authorized to exist. Classify the destination before writing and fail closed when ownership, privacy, or publication scope is unclear.

## Context Classification

Classify the destination as one of:

- `work`: organization-controlled repository or workspace.
- `private-personal`: private repository or local archive controlled by the user.
- `public-personal`: public repository, package, documentation, issue, pull request, or other externally readable content.

Do not infer that private personal storage is authorized merely because it is private. Ownership, policy, license, and confidentiality still apply.

## Blocked Content for Public Personal Contexts

Never publish the following in a public personal repository or message:

- Secrets, tokens, credentials, certificates, or private keys.
- Customer, employee, account, payment, or personal data.
- Internal domains, hostnames, network details, project identifiers, or infrastructure names.
- Organization names, repository owners, team names, issue prefixes, or service names that identify a current employer or private client.
- Proprietary source code, operational procedures, vulnerability details, scanner output, or incident evidence.
- Absolute machine paths, private workspace links, or private repository URLs.

Use generic placeholders such as `<company>`, `<org>`, `<work>`, or `<repo>` when an example is useful.

## Procedure

Before writing or publishing:

1. Identify the destination context and intended audience.
2. Check ownership, authorization, license, confidentiality, and publication scope.
3. Scan the content for secrets, private data, identifiers, paths, URLs, and context-specific details.
4. Generalize or remove information that is not required for the reusable behavior.
5. Stop and ask when the boundary or authorization is ambiguous.

Before writing, committing, or pushing to a public personal repository:

- Classify the destination. Research notes, operating cards, and "temporary" docs are not exceptions.
- Inspect the staged diff.
- Run the machine forbidden-pattern scan (`personal-publish-guard`). Treat a miss, skip, or `--no-verify` as a failed publish, not a warning.
- Confirm that examples are generic and portable (`<company>`, `<org>`, `<work>`, `<repo>`).
- Confirm that no private source, logs, prompts, tool arguments, or credentials are included.
- If the scan is missing or the boundary is ambiguous, stop. Do not publish and "generalize later."

## Private Personal Archives

A private personal archive may contain transferable notes or workflows only when their retention is authorized and they contain no secrets or restricted data. Keep work-specific mappings, defaults, and sensitive operational details in a separate private configuration or organization-controlled repository.

