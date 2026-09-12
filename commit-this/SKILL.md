---
name: commit-this
description: Use when the user asks agent to create a git commit, draft or modify a commit message, commit staged or current changes, or amend a commit. Triggers include "commit this", "make a commit", and "git commit".
allowed-tools: Bash(git add:*), Bash(git status:*), Bash(git diff:*), Bash(git commit:*)
---

# Create Commit

Create one focused commit, or draft/update a commit message.

## Workflow

1. Inspect `git status` and the relevant diff.
2. If only drafting a message, do not stage or commit.
3. If committing, preserve the requested scope:
   - use already-staged changes unless told to stage more
   - otherwise stage only files clearly related to the request
4. Read [commit-message.md](references/commit-message.md), then draft or amend the message.
5. Run `git commit -m` when a commit is requested.
6. Report the commit hash and subject, or return only the drafted message.

## Guardrails

**IMPORTANT:** Preserve the user's intended commit scope.

- Never include unrelated changes, generated noise, secrets, credentials, or local-only files.
- Avoid `git add .` unless the user explicitly asks to commit everything.
- When other changes are present, stage only authorized changes that can be clearly identified. Ask only when the intended commit scope cannot be safely separated.
- If hooks fail, report the output and fix only intended-scope issues.

## Examples

- Message only: "draft a commit message" -> inspect the provided or staged diff, read [commit-message.md](references/commit-message.md), and return only the message.
- Commit: "commit this" -> inspect status and diff, stage only intended files if needed, read [commit-message.md](references/commit-message.md), commit, then report the hash and subject.
