---
name: quality
description: Code quality, commit standards, quality gates, PR standards, documentation, performance, security, and output character hygiene (gremlin characters). Use when writing code, committing, creating PRs, generating any text, or when the user runs /gremlin-clean.
---

# Quality Rules

**MANDATORY — Output hygiene:** Never use gremlin/invisible characters in any generated text. Use only standard space (U+0020) and normal line breaks (LF/CRLF). No zero-width (U+200B, U+200D, U+200C), no non-breaking space (U+00A0) unless required, no control or separator characters (U+2028, U+2029). Rewrite pasted content as clean text instead of copying raw.

## Code Quality

### Commit Standards

- Use conventional commit format: `<type>(<scope>): <description>`
- Types: feat, fix, chore, docs, style, refactor, test
- Present tense, imperative mood
- **Always write commit messages in English**
- Include Linear issue references when applicable
- Keep descriptions concise but descriptive

### Code Style

- Follow project-specific linting rules
- Maintain consistent code style across the project
- Use meaningful variable and function names
- Include proper error handling
- Write clear, self-documenting code
- Add comments for complex logic

### Lint and format fix workflow (Trunk)

When fixing lint, format, or style issues in a project that uses Trunk:

1. **First:** Run `trunk check --fix` to auto-fix everything Trunk can fix.
2. **Then:** Address any remaining issues manually (what Trunk reports but could not auto-fix).
3. Re-run `trunk check` (or `trunk check --fix`) to confirm all issues are resolved.

Do not manually fix what Trunk can fix; let Trunk do it first, then the agent resolves the rest.

### Code Organization

- Keep functions small and focused
- Use appropriate design patterns
- Maintain clear separation of concerns
- Follow DRY (Don't Repeat Yourself) principles
- Organize imports and dependencies properly

## Quality Gates

### Pre-commit Checks

- All tests must pass before committing
- Linting must pass without errors
- Build must succeed
- Security scans must pass
- No sensitive data in commits

### Pre-PR Checks

- All quality gates must pass
- Code review requirements met
- Documentation updated
- Tests cover new functionality
- Performance impact assessed

### Pull Request Standards

- **Always write PR titles and descriptions in English**
- Use descriptive and clear PR titles
- Include comprehensive descriptions with context
- Reference Linear issues when applicable
- Follow conventional commit format for PR titles
- When referencing PRs or issues, always use full GitHub URLs (e.g., `https://github.com/org/repo/pull/123`), never shorthand like `repo #123` or `repo#number`

### Testing Requirements

- All commands must be testable
- Include edge case testing
- Verify safety mechanisms work
- Test error handling paths
- Maintain test coverage standards

## Documentation Quality

### Content Standards

- Clear and concise explanations
- Practical examples and use cases
- Consistent formatting and structure
- Regular updates and maintenance
- Avoid redundant information
- Avoid overly complex explanations

### Structure Requirements

- Use proper markdown formatting
- Include table of contents for long documents
- Add code examples with syntax highlighting
- Include troubleshooting sections
- Provide clear navigation

### Maintenance

- Keep documentation up to date
- Review and update regularly
- Remove outdated information
- Add new features to documentation
- Solicit feedback from users

## Performance Quality

### Efficiency Standards

- Optimize for performance when possible
- Avoid unnecessary operations
- Use appropriate data structures
- Monitor resource usage
- Profile critical paths

### Scalability Considerations

- Design for growth
- Consider multi-repository scenarios
- Plan for increased usage
- Optimize for large codebases
- Handle edge cases gracefully

## Security Quality

### Data Protection

- Never commit sensitive information
- Use environment variables for secrets
- Validate all inputs
- Sanitize user data
- Follow security best practices

### Access Control

- Implement proper authentication
- Use least privilege principle
- Audit access patterns
- Monitor for suspicious activity
- Regular security reviews

## Integration Quality

### API Design

- Use consistent naming conventions
- Provide clear error messages
- Include proper status codes
- Document all endpoints
- Version APIs appropriately

### External Services

- Handle service failures gracefully
- Implement proper retry logic
- Monitor external dependencies
- Provide fallback mechanisms
- Log integration issues

## Monitoring and Observability

### Logging Standards

- Use appropriate log levels
- Include relevant context
- Avoid logging sensitive data
- Structure logs for analysis
- Implement log rotation

### Metrics and Monitoring

- Track key performance indicators
- Monitor error rates
- Set up alerts for critical issues
- Regular health checks
- Performance monitoring

---

## Output / Character Hygiene (Gremlin Characters)

**Known Cursor/LLM issue:** Models sometimes emit invisible Unicode despite instructions. See `docs/gremlin-characters-cursor-llm.md` for references and full list.

The AI must ensure that all generated text—including code, comments, documentation, and user-facing messages—is free from "gremlin characters" (invisible or problematic Unicode). These cause rendering issues, lint errors (e.g. `no-irregular-whitespace`), and parsing errors.

### Prohibited Characters

Use only **U+0020** (space) and **LF/CRLF**. Avoid:

- **Zero-width**: U+200B (ZWSP), U+200C (ZWNJ), U+200D (ZWJ), U+2060 (word joiner), U+2063 (invisible separator)
- **Non-breaking / other spaces**: U+00A0 (NBSP), U+1680 (Ogham), U+180E (Mongolian vowel separator), U+2000–U+200A (en/em quad, figure space, thin space, etc.), U+202F (narrow NBSP), U+205F (medium math space), U+3000 (ideographic space), U+FEFF (BOM)
- **Line/paragraph**: U+2028 (line separator), U+2029 (paragraph separator)
- **Other**: U+00AD (soft hyphen), control characters (U+0000–U+001F, U+007F), directional formatting

### /gremlin-clean

When the user runs `/gremlin-clean`, follow **`commands/gremlin-clean.md`**: run `~/.cursor/scripts/strip-gremlins.py` on the target file(s) and report. Command is defined in `commands/` so it appears in the / menu. The script automatically skips binary files (`.db`, `.sqlite`, images, archives, fonts, compiled files, etc.).

### AI Enforcement

- Use only standard space (U+0020) and normal line breaks (LF/CRLF) in generated content.
- Do not insert zero-width or other invisible characters.
- When pasting or referencing external text, prefer rewriting as clean ASCII/Unicode rather than copying raw content that may contain gremlins.
- Prefer clear, readable text composed of standard visible characters only.
