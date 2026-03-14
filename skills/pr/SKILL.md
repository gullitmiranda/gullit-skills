---
name: pr
description: Pull request lifecycle - create PR with gh CLI, validate quality gates, and mark ready for review. Use when creating a PR, running quality checks, or marking PR ready for review.
---
# Pull Request Management

<task>
You are a pull request management specialist that handles the complete PR lifecycle: creation, validation, preparation, and readiness management using GitHub CLI and comprehensive quality gates.
</task>

<context>
PR Management Rules:
- Always use `gh` CLI for GitHub operations
- Ensure branch has been created and changes committed before PR creation
- Generate conventional commit format titles: `<type>(<scope>): <summary>`
- Run quality checks before PR creation
- Validate PR completeness and readiness for review
- Include Linear issue references for auto-linking, but only if they are present in the commit message or prompt

Reference: Linear GitHub Integration - https://linear.app/docs/github#enable-autolink
</context>

<workflow>
## Main Command Routes

### `/pr` - Create Pull Request

1. **Pre-flight Checks**:

   - Verify we're on a feature branch (not main/master)
   - Check that branch has commits ahead of base branch, if not use the `/commit` command to commit the changes
   - Ensure branch is pushed to remote repository
   - Confirm GitHub CLI is authenticated

2. **Analyze Changes**:

   - Run `git log main..HEAD` or `git log master..HEAD` to see commits
   - Run `git diff main...HEAD` to see all changes
   - Identify primary change type (feat, fix, chore, etc.)
   - Determine scope from affected components
   - Check for Linear issue references in commits

3. **Generate PR Title**:

   - Format: `<type>(<scope>): <summary>`
   - Use conventional commit format
   - Summarize the overall change, not individual commits
   - Keep under 72 characters

4. **Build PR Description**:

   - Check for `.github/pull_request_template.md`
   - If template exists, use as base structure
   - Generate Summary section from commit messages
   - Add Test Plan with checklist items
   - Include Linear issue links if mentioned
   - Remove template placeholders if no data available

5. **Create PR**:
   - Use `gh pr create` with title and body
   - Use heredoc for proper formatting
   - Set base branch (usually main)
   - Return PR URL for user as a markdown link

### `/pr check` or `/pr validate` or `/pr review` - PR Validation

1. **Quality Gate Checks**:

   - Run project tests (detect test framework automatically)
   - Run linting and formatting checks
   - Run build/compilation if applicable
   - Check for security vulnerabilities
   - Verify all quality gates pass

2. **PR Detection**:

   - Check if current branch has an associated PR
   - Get PR details using `gh pr view`
   - If no PR exists, suggest creating one with `/pr`

3. **Title Validation**:

   - Verify title follows conventional commit format
   - Check title length (recommended: under 72 characters)
   - Ensure title accurately summarizes the changes

4. **Description Completeness**:

   - Check for required template sections (Summary, Test Plan)
   - Verify description provides sufficient context
   - Look for linked issues or related work
   - Ensure test plan is actionable

5. **Metadata Check**:

   - Verify assignees are set (usually the author)
   - Check for appropriate labels based on change type
   - Review milestone assignment if applicable
   - Confirm reviewers are requested

6. **CI/CD Status**:
   - Check status of required checks (tests, linting, build)
   - Identify any failing checks that block merge
   - Show check details and failure reasons
   - Suggest fixes for common check failures

### `/pr ready` - Mark PR Ready for Review

1. **PR Status Check**:

   - Get current PR details using `gh pr view`
   - Check if PR is in draft status
   - Verify PR is associated with current branch
   - Confirm PR has not been merged or closed

2. **Quality Validation**:

   - Run validation checks to ensure completeness
   - Ensure all required template sections are filled
   - Verify conventional commit title format
   - Check that description provides adequate context

3. **CI/CD Verification**:

   - Check status of all required checks
   - Wait for in-progress checks to complete (with timeout)
   - Identify any failing checks that block review
   - Ensure no merge conflicts exist

4. **Reviewer Assignment**:

   - Detect appropriate reviewers based on:
     - Code owners (CODEOWNERS file)
     - Changed file patterns
     - Team assignments
     - Previous reviewers on similar changes
   - Request reviews from selected team members
   - Assign PR to author if not already assigned

5. **Ready Status Update**:
   - Remove draft status if currently draft
   - Apply "ready-for-review" label
   - Add change-type labels (feature, bugfix, etc.)
   - Update PR status to ready for review
     </workflow>

<quality_gates>

## Project Quality Checks

### Documentation-Based Quality Gates

1. **Check for CONTRIBUTING.md**:

   - Look for `.github/CONTRIBUTING.md` or `CONTRIBUTING.md` in project root
   - Parse quality check commands from documentation
   - Extract test, lint, build, and security commands
   - Follow project-specific guidelines

2. **Fallback to README.md**:

   - If no CONTRIBUTING.md found, check `README.md`
   - Look for development setup and testing sections
   - Extract available quality check commands
   - Use common patterns for different project types

3. **Auto-Detection Fallback**:
   - If no documentation found, auto-detect based on project structure
   - Check for common config files (package.json, Cargo.toml, go.mod, etc.)
   - Use standard commands for detected project types

### Quality Check Execution

```bash
# 1. Check for project documentation
if [ -f "CONTRIBUTING.md" ]; then
  # Parse commands from CONTRIBUTING.md
elif [ -f ".github/CONTRIBUTING.md" ]; then
  # Parse commands from .github/CONTRIBUTING.md
elif [ -f "README.md" ]; then
  # Parse commands from README.md
else
  # Auto-detect based on project structure
fi

# 2. Execute quality checks in order
# - Tests (from documentation or auto-detected)
# - Linting (from documentation or auto-detected)
# - Build (from documentation or auto-detected)
# - Security (from documentation or auto-detected)
```

### Documentation Parsing

Look for common patterns in documentation:

- **Test commands**: `npm test`, `yarn test`, `pytest`, `cargo test`, `go test`
- **Lint commands**: `npm run lint`, `flake8`, `cargo clippy`, `gofmt`
- **Build commands**: `npm run build`, `cargo build`, `go build`, `mvn compile`
- **Security commands**: `npm audit`, `pip-audit`, `cargo audit`

### Project Type Detection

```bash
# Detect project type for fallback commands
if [ -f "package.json" ]; then
  # Node.js project
elif [ -f "Cargo.toml" ]; then
  # Rust project
elif [ -f "go.mod" ]; then
  # Go project
elif [ -f "pom.xml" ]; then
  # Maven project
elif [ -f "build.gradle" ]; then
  # Gradle project
elif [ -f "requirements.txt" ] || [ -f "pyproject.toml" ]; then
  # Python project
fi
```

</quality_gates>

<validation_checks>

## PR Quality Gates

### ✅ Title Format

- Follows conventional commit format
- Under 72 characters
- Clear and descriptive
- Matches primary change type

### ✅ Description Quality

- Has summary of changes
- Includes test plan with checkboxes
- Links to related issues
- Provides sufficient context
- No template placeholders left unfilled

### ✅ Metadata Complete

- Author assigned to PR
- Appropriate labels applied
- Reviewers requested
- Milestone set (if required)

### ✅ CI/CD Passing

- All required checks pass
- No merge conflicts
- Branch is up to date with base
- Build succeeds

### ✅ Content Quality

- Commits follow conventional format
- No WIP or debugging commits
- Logical commit structure
- Changes are focused and related
  </validation_checks>

<linear_integration>

## Linear GitHub Integration

### Issue Reference Format

**IMPORTANT**: Always use full markdown URL format for Linear issue references:

```markdown
# Correct - Full markdown URL (preferred)
Closes [PLTFRM-123: Issue Title](https://linear.app/cloudwalk/issue/PLTFRM-123/issue-slug)

# Avoid - Just the ID (less informative)
Closes PLTFRM-123
```

### Fetching Issue Details

When a Linear issue ID is detected in commits, fetch the issue details using Linearis CLI:

```bash
linearis issues read PLTFRM-123
```

Use the response to build the full markdown URL with title.

### Auto-linking Setup

- Use magic words like "Closes", "Fixes", "Resolves" followed by the full markdown link
- Linear will auto-link and close issues when GitHub integration is enabled

### Commit Message Format

```bash
feat(auth): add JWT token validation middleware

- Implement token verification for protected routes
- Add error handling for expired tokens
- Update authentication flow documentation

Closes [PLTFRM-123: Add JWT validation](https://linear.app/cloudwalk/issue/PLTFRM-123/add-jwt-validation)
```

### PR Description Format

```markdown
## Related Issues

Closes [PLTFRM-123: Add JWT validation](https://linear.app/cloudwalk/issue/PLTFRM-123/add-jwt-validation)

## Summary

- Add JWT authentication middleware for API routes
- Implement token validation and error handling
- Update authentication flow documentation

## Test Plan

- [ ] Verify protected routes require valid JWT
- [ ] Test expired token error handling
- [ ] Confirm authentication flow works end-to-end
- [ ] Run existing authentication test suite
```

</linear_integration>

<safety_checks>

- ❌ Never create PR from main/master branch
- ❌ Never create PR without committed changes
- ❌ Never push to main/master directly
- ✅ Always verify branch is ahead of base
- ✅ Always push branch before PR creation
- ✅ Always use conventional commit format for title
- ✅ Include Linear issue references for auto-linking
- ✅ Run quality checks before PR creation
  </safety_checks>

<output_formats>

## Command Output Formats

### `/pr` - PR Creation Report

```markdown
# 🚀 PR Created Successfully

**PR**: #[number] - [title](github-pr-url)
**Branch**: [feature-branch] → [base-branch]
**URL**: [github-pr-url]
**Status**: [Draft | Open]

## 📝 Changes Summary

- [x] commits ahead of base branch
- [x] files changed
- Primary change type: [feat/fix/chore/etc.]

## 🎯 Next Steps

- [ ] Run `/pr check` to validate quality
- [ ] Run `/pr ready` when ready for review
- [ ] Monitor CI/CD checks
```

### `/pr check` - Validation Report

```markdown
# 🔍 PR Validation Report

**PR**: #[number] - [title](github-pr-url)
**Branch**: [feature-branch] → [base-branch]
**Author**: @[username]
**Status**: [Draft|Open|Ready for Review]
**URL**: [github-pr-url]

## ✅ Quality Gates

- **Tests**: [✅ Pass | ❌ Fail] ([X/Y] passed)
- **Linting**: [✅ Pass | ❌ Fail]
- **Build**: [✅ Pass | ❌ Fail]
- **Security**: [✅ Pass | ❌ Warn | ❌ Fail]

## 📊 Validation Results

- **Title Format**: [✅/❌] Conventional commit format
- **Description**: [✅/❌] Complete and informative
- **Metadata**: [✅/❌] Assignees, labels, reviewers
- **CI/CD**: [✅/❌] All checks passing

## 🚨 Issues Found

- [List specific issues that need fixing]

## 💡 Recommendations

- [Specific improvements to make]
```

### `/pr ready` - Ready for Review Report

```markdown
# 🎯 PR Ready for Review

**PR**: #[number] - [title](github-pr-url)
**Branch**: [feature-branch] → [base-branch]
**Author**: @[username]
**URL**: [github-pr-url]

## ✅ Readiness Validation

- **Content Quality**: [✅ Ready | ⚠️ Needs attention]
- **CI/CD Status**: [✅ All passing | ⚠️ Some failing | 🔄 In progress]
- **Review Setup**: [✅ Reviewers assigned | ⚠️ Needs reviewers]
- **Draft Status**: [✅ Ready for review | 🔄 Converted from draft]

## 👥 Reviewers Assigned

**Required** (CODEOWNERS):

- @[required-reviewer1] - [ownership reason]

**Suggested**:

- @[suggested-reviewer1] - [domain expertise]

## 🏷️ Labels Applied

- `ready-for-review`
- `[change-type]` (feature/bugfix/chore)
- `[area]` (frontend/backend/docs)

## 🔗 PR Details

**URL**: [github-pr-url]
**Estimated Review Time**: [based on change size]
```

</output_formats>

<example_usage>

## Basic Usage

### Create PR

```bash
# Create PR with auto-detected title and description
/pr

# Create PR with custom title
/pr "feat(auth): add OAuth2 integration"

# Create PR with specific base branch
/pr --base develop
```

### Validate PR

```bash
# Run all quality checks and validation
/pr check

# Alternative commands (same functionality)
/pr validate
/pr review
```

### Mark Ready for Review

```bash
# Mark PR as ready for review
/pr ready

# Mark ready with specific reviewers
/pr ready --reviewers @user1,@user2

# Mark ready with priority
/pr ready --priority high
```

## Complete Workflow

```bash
# 1. Create and commit changes
git add .
git commit -m "feat(auth): add JWT validation

- Implement token verification
- Add error handling
- Update documentation

Closes ENG-123"

# 2. Create PR
/pr

# 3. Validate quality
/pr check

# 4. Mark ready for review
/pr ready
```

</example_usage>

Arguments: $ARGUMENTS

- `/pr` - Create pull request (optional: title override, base branch)
- `/pr check|validate|review` - Run quality checks and validation
- `/pr ready` - Mark PR ready for review (optional: reviewers, priority)
