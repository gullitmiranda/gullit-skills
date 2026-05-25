---
name: workflow
description: Language, terminal, workspace, branch, commit, PR, planning, and documentation workflow rules. Use when writing in English, committing, creating PRs, or creating plans in .cursor/plans/.
---

# Workflow Rules

## Language

- By default always write documentation, comments, code, commit messages, and pull request titles/descriptions in English
- Use English for all technical communication including:
  - Code comments and documentation
  - Commit messages and commit descriptions
  - Pull request titles and descriptions
  - Technical documentation and README files
  - API documentation and code examples

## Integrated Terminal

- Prefer terminal commands over GUI operations when possible

## Temporary Files Management

- When creating temporary files, use temporary directories (`./tmp` or system tmp)
- Never commit temporary files to version control

## Workspace & Multi-Repository Rules

### Workspace Structure Awareness

- Always check current working directory and understand repository boundaries
- Never assume single git repository when working in multi-repo workspace
- Always verify which repository operations are targeting before execution

### Multi-Repository Handling

- When working with staged changes, identify which specific repository they belong to
- Navigate to correct repository directory before running git operations
- Treat each repository as separate entity with its own git state

## Branch Management

- Create feature branches from main/master
- Use descriptive branch names
- Keep branches focused on single features
- Delete merged branches

## Commit Workflow

- When committing from an AI agent in a repo with Trunk hooks, run the final `git commit` with stdin closed by appending `</dev/null` so the hook cannot hang waiting for EOF
- If Trunk hook execution still appears stuck with closed stdin, or reports daemon/GRPC errors, use `trunk daemon shutdown` only as fallback recovery before retrying
- Only commit when explicitly requested
- Never commit unstaged changes without explicit request
- Never commit directly to main/master branch
- Make small, focused commits
- Use conventional commit format
- Include meaningful commit messages
- Reference issues when applicable: GitHub Issues by default; Linear only when explicitly referenced in the prompt or commits

## PR Workflow

- Create PRs for all main branch changes
- Use descriptive PR titles
- Include comprehensive descriptions
- Request appropriate reviewers

## Planning Workflow

### Plan Creation Guidelines

- Create plans in `.cursor/plans/` directory
- Use clear, actionable task breakdown
- Include dependencies and prerequisites
- Format as markdown with clear sections
- **NEVER include timelines or schedules**
- **NEVER generate cronograms or time estimates**
- Focus on what needs to be done, not when

### Plan Structure

- ## Objective
- ## Tasks
- ## Dependencies
- ## Acceptance Criteria
- ## Notes

### Plan Files

- Save in `.cursor/plans/` with `.plan.md` extension so plans match the standard format (e.g. `descriptive-name.plan.md`).
- Use the same task/todo structure as native Cursor plans so plans stay consistent whether created in plan mode or in chat.
- **NEVER commit files under `.cursor/plans/`** — they are local-only and gitignored; committing them is a hard error that breaks the user's setup.

## Documentation Standards

### Content Guidelines

- Clear and concise explanations
- Practical examples and use cases
- Consistent formatting and structure
- Regular updates and maintenance
- Avoid redundant information
- Avoid overly complex explanations
- In documentation, prefer linking to the GitHub repository URL instead of just mentioning the repo name

### ZeroPath References

- Apply the `zeropath` skill whenever the task or draft mentions ZeroPath,
  `zeropath`, ZeroPath findings, or URLs under `https://zeropath.com/`.
- When referencing ZeroPath findings in chat replies, documents, plans, PR
  bodies, issue bodies, or comments, always include the full URL as visible
  text. Format: `https://zeropath.com/app/issues/<uuid>`.
- Do not replace known ZeroPath finding URLs with UUID-only references, shortened
  links, hidden markdown labels, or vague labels like `ZeroPath 6.3`.
- Do not add ZeroPath information to unrelated PRs or documents. These rules
  apply only when ZeroPath is already part of the task, draft, commits, or
  linked evidence.
