# Python Pre-Commit Checks

Use this reference when a repo has `pyproject.toml`, `uv.lock`, `requirements.txt`, `setup.cfg`, or Python tests.

## Command Selection

| Need | Prefer | Alternatives |
|------|--------|--------------|
| Lint | `ruff check` | project-specific lint script |
| Format check | `ruff format --check` | `ruff format` with diff guard |
| Type check | existing checker | `ty check`, `mypy .`, or `pyright` |
| Tests with uv | `uv run pytest` | `uv run python -m pytest` |
| Tests without uv | `pytest` | `python -m pytest` |

Use exactly one type checker unless the repo already runs more than one. Prefer the existing checker. For a new strict gate, fix only setup-related or otherwise in-scope issues; report unrelated existing failures and defer the new gate without disabling or weakening existing gates.

## Detection

- `uv.lock` or `[tool.uv]`: use `uv run ...`.
- `[tool.ruff]` or `ruff` dependency: use Ruff lines.
- `mypy`, `pyright`, or `ty` in config/dependencies: use that existing checker.
- Existing Make/Nox/Tox scripts: prefer the repo's documented command if it wraps the same gates.

## Common Mistakes

- Assuming every Python repo uses `uv`.
- Running `ruff format` without a before/after diff guard.
- Adding strict type checking before the project is clean.
- Running dependency updates (`uv lock --upgrade`, `pip-compile --upgrade`) in pre-commit.
