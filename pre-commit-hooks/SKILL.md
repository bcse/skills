---
name: pre-commit-hooks
description: Use when a repository needs a version-controlled git pre-commit hook for local quality gates, especially Python, JavaScript/TypeScript, Rust, or mixed-language projects, or when asked to enforce checks before commits.
---

# Setting Up Pre-Commit Hooks

## Overview

Install a **version-controlled** git `pre-commit` hook that runs the repo's normal quality gates before each commit. Keep the hook in `.githooks/` and point Git at it with `core.hooksPath`; never hand-copy scripts into `.git/hooks/`.

## When To Use

- A repo needs local checks before commit: format, lint, type-check, test, build.
- A user asks to "add a pre-commit hook", "set up git hooks", or "enforce checks on commit".
- A polyglot repo needs one hook that coordinates multiple toolchains.

Do not use this when the repo already uses the `pre-commit` framework (`.pre-commit-config.yaml`); extend that config instead.

## Quick Start

1. Inspect the repo for existing hooks/config:
   - `git config --local --get core.hooksPath`
   - `.pre-commit-config.yaml`, `.githooks/`, `.git/hooks/pre-commit`
2. Choose reference files for the repo's languages:
   - Python: `references/python.md`
   - JavaScript/TypeScript: `references/javascript.md`
   - Rust: `references/rust.md`
3. Copy the relevant language example from `assets/` into `.githooks/pre-commit`.
4. For mixed-language repos, merge the needed language examples into one hook.
5. Adapt checks to commands the repo already uses.
6. Enable and verify:

```sh
chmod +x .githooks/pre-commit
git config --local core.hooksPath .githooks
.githooks/pre-commit
```

Document the same setup commands in README/AGENTS so contributors can enable the hook after cloning.

## Templates

| Language | Example |
|----------|---------|
| Python | `assets/pre-commit-python` |
| JavaScript/TypeScript | `assets/pre-commit-javascript` |
| Rust | `assets/pre-commit-rust` |

## Core Rules

- Use POSIX `sh`; avoid bashisms unless the repo already requires Bash.
- If `core.hooksPath` is already set to another path, do not overwrite silently.
- Keep only commands the repo can run today. Fix only failures introduced by this setup or already within the requested scope. Report unrelated existing failures and defer any affected new strict gate; do not disable or weaken existing gates.
- Do not auto-detect tools and silently skip missing ones. A hook should fail when a selected gate cannot run.
- Prefer check-only formatters when available. If using mutating commands (`cargo fmt`, `npm run format`, `ruff format`), keep a before/after `git diff` guard and abort if files changed.
- Do not run dependency-upgrade commands in a hook: no `npm audit fix`, `cargo update`, `uv lock --upgrade`, or similar. Put dependency updates in explicit commits/PRs.
- Keep expensive checks in CI or pre-push when they make normal commits painful.

## Common Mistakes

- Copying to `.git/hooks/pre-commit`: untracked, per-clone, and easy to drift.
- Adding every possible language command instead of the repo's actual commands.
- Writing an auto-detect hook that passes when expected tools are missing.
- Running auto-fixers without detecting rewritten files.
- Adding `npm audit fix` or package upgrades to pre-commit.
- Making the hook pass only on your machine because it depends on global tools not in project docs.
