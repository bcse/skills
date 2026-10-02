---
name: write-pr
description: Write clear pull request titles and descriptions with visual explanations. Use when creating a PR, drafting PR content, or when the user asks to write/improve a PR description.
---

# Writing Pull Requests

Help reviewers understand the problem, the resulting behavior, and the evidence supporting the change. Describe the final patch for someone who has not seen the authoring conversation. Prefer diagrams or images when they explain the change more clearly than prose. Use short captions and keep text for facts the visual cannot show.

Before drafting, inspect the current diff against the intended base, the repository's PR template, and available test results. Use supplied artifacts when repository access is unavailable, and state material evidence gaps. Reconcile the title and body with the final scope after revisions.

## Reader and language

Read and apply $writing-for-human before drafting. The reader is a reviewer who needs to understand the change and verify its evidence. Adapt its reader guidance to that task: problem, resulting behavior, key changes, and validation. Use the repository's PR template instead of its README route.

Write the title, body, and visual labels in [ASD-STE100 Simplified Technical English, Issue 9](https://www.asd-ste100.org/assets/files/ASD-STE100_ISSUE9.pdf). Apply its dictionary and writing rules in addition to the reader guidance:

- Use approved words with their approved meanings, parts of speech, and forms. Verify uncertain words in the STE dictionary.
- Use established software terms as technical nouns or technical verbs only when the standard permits them. Use one term for each concept.
- Use a maximum of 25 words per descriptive sentence and 20 words per instruction. Give each instruction one action.
- Prefer active voice and simple verb forms. Put conditions before instructions. Keep each paragraph about one topic.
- Preserve facts, conditions, risks, and uncertainty when you simplify sentences.

Keep code, commands, paths, identifiers, quoted output, and required template text exact. Use STE for the surrounding explanation. Do not claim verified STE compliance without a review against the standard and dictionary. If these sources are unavailable, state the verification limit outside the PR draft.

## PR Title

Use Conventional Commits format:

```
<type>(<scope>): <description>
```

### Types

| Type       | Use for                                    |
|------------|--------------------------------------------|
| `feat`     | New feature                                |
| `fix`      | Bug fix                                    |
| `docs`     | Documentation only                         |
| `refactor` | Code restructure (no behavior change)      |
| `perf`     | Performance improvement                    |
| `test`     | Adding or fixing tests                     |
| `chore`    | Maintenance, dependencies, configs         |
| `build`    | Build system changes                       |
| `ci`       | CI/CD configuration                        |

### Scope

Optional noun in parentheses describing the affected area: `fix(auth):`, `feat(api):`, `docs(readme):`

### Description Rules

- Use imperative mood: "Add" not "Added" or "Adds"
- Start with capital letter
- No period at end
- Keep under 50 characters when possible

### Examples

```
feat(auth): Add OAuth2 login support
fix(api): Handle null response in user endpoint
docs: Update installation instructions
refactor(db): Simplify query builder logic
feat!: Remove deprecated v1 API endpoints
```

Use `!` before `:` to indicate breaking changes.

## PR Body Template

Follow the repository's template when present. Otherwise, adapt this template to the change. A small fix may need only a summary and validation. Use diagrams, images, or other review aids within Changes to explain behavior and help reviewers navigate the diff. Omit unused sections and checklists.

```markdown
## Summary

<What this PR does and why. Link related issues.>

Fixes #123

## Changes

<A diagram, image, or diff sketch with a short caption, when useful>

- <Specific change 1>
- <Specific change 2>

## Testing

<Commands actually run, observed results, and relevant limits>

<Separate any suggested manual verification from completed checks>

## Checklist

- [ ] Tests added/updated
- [ ] Documentation updated (if needed)
- [ ] Breaking changes noted (if any)
```

## Writing Guidelines

### Summary Section

Lead with the concrete problem and resulting behavior. Include a trigger and before/after example when that makes the change easier to assess.

- Be specific—avoid vague phrases like "improve performance" or "enhance UX"
- Link related issues using keywords: `Fixes #123`, `Closes #456`, `Related to #789`
- Don't assume readers will read linked issues—include essential context

### Changes Section

Show concrete behavior and design choices that help reviewers assess the patch. Prefer a diagram or image to a long explanation of flows, relationships, states, or UI changes. For a change spanning several files, name the entry point and key files or symbols in a useful reading order. Include technical details when they explain a tradeoff, dependency, or risk.

**Good:**
- Add rate limiting to API endpoints
- Update error messages to include request ID

**Avoid:**
- Changed line 42 in auth.js
- Refactored some code

### Review aids

Give reviewers a compact visual explanation they can check against the code when it makes the change easier to understand. Choose the smallest useful view. A straightforward patch may need only a sentence; a complex patch may benefit from several views when each answers a different question.

Read [Review aids](references/review-aids.md) when selecting a visual or preparing an attachment. Use the diagram or image format that best explains the change; Mermaid is one option. GitHub also supports file attachments. Keep the explanation readable within the PR, and verify each view against the final patch.

### Testing Section

Report validation that actually happened. Name the command, tested behavior, and observed result; include the revision or environment when it affects reproducibility. Link relevant test cases, CI runs, or captured output when available. Keep excerpts short and preserve the assertion or failure reason that matters.

Separate completed checks from suggested verification. State relevant checks not run and material limits, such as mocked dependencies or untested concurrency. If no results are available, say so instead of turning proposed commands into passing evidence.

#### TDD evidence

When test-driven development was used and its sequence is supported by execution records, include a compact account in Testing:

| Stage | Evidence to include |
|-------|---------------------|
| Red | The test and command run before implementation, plus the observed failure showing the missing behavior. An unrelated setup failure does not establish this. |
| Green | The same test passing after the implementation, with the command and observed result. |
| Refactor, if performed | What was simplified and which checks passed afterward. |

Include broader regression checks separately, with their actual scope and results. Passing tests alone do not establish TDD. If tests were added after implementation, describe them as regression coverage. Replaying a test against the old code afterward can demonstrate the regression, but does not prove the test was written first. If a TDD claim is requested but the sequence is unknown, state that it is unverified and report the evidence available. Do not invent earlier failures, refactoring steps, logs, or test counts.

### Breaking Changes

If the PR introduces breaking changes, add a section:

```markdown
## Breaking Changes

- `oldMethod()` removed—use `newMethod()` instead
- Config option `foo` renamed to `bar`
```

## Checklist Usage

- Mark items with `[x]` only when actually completed
- Remove items that don't apply, or mark as N/A
- Common items: tests, docs, migrations, changelog

## Quick Reference

| Do | Don't |
|----|-------|
| Use imperative mood | Use past tense |
| Link issues explicitly | Assume context |
| List specific changes | Be vague |
| Provide test steps | Say "tested locally" |
| Note breaking changes | Hide API changes |
