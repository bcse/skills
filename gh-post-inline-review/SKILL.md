---
name: gh-post-inline-review
description: "Format supplied code-review findings as priority-badged inline GitHub comments and post them together as one commit-anchored pull request review with the gh CLI. Use after findings have already been produced and the task is to normalize their GitHub locations, build the review payload, or publish the findings to a PR."
---

# Post Inline GitHub Review

Format and publish findings that were produced elsewhere. Do not perform a code review, discover new findings, judge their validity, change their priority, or rewrite their substance.

## Input Contract

Require the caller to name the reviewing model, then require each supplied
finding to provide:

- `priority`: `P0`, `P1`, `P2`, or `P3`
- `title`: displayed after the priority badge
- `body`: posted verbatim except for trimming surrounding whitespace
- `path`: repository-relative file path
- `line`: final line of the GitHub diff anchor
- optional `start_line`: first line of a multiline anchor
- optional `side`: `RIGHT` by default; use `LEFT` for deleted lines

Preserve the supplied finding order and content. If a required field or valid diff location is missing, report exactly what is needed; do not infer content, severity, or an anchor.

## Payload Format

Create `review.json` with this shape:

```json
{
  "commit_id": "40-character pull request head SHA",
  "model": "name of the model that produced the findings",
  "findings": [
    {
      "priority": "P2",
      "title": "Gate the option on the actual request route",
      "body": "When ... Please ...",
      "path": "relative/path/to/file.rs",
      "line": 42,
      "start_line": 39,
      "side": "RIGHT"
    }
  ]
}
```

Apply these formatting rules:

- Preserve the finding array order.
- Preserve `priority`, `title`, and `body`; trim only surrounding whitespace.
- Supply `model` as the name of whichever model actually produced the findings,
  resolved at run time rather than copied from an example. It is required, and
  the script refuses to render a review without it.
- Accept priorities `P0`, `P1`, `P2`, and `P3` for badge formatting.
- Use a repository-relative `path` with `/` separators.
- Use `RIGHT` for added or contextual lines and `LEFT` for deleted lines.
- Omit `start_line` for a single-line comment.
- Require `start_line < line` for a multiline comment.
- Require at least one finding.

Render the review body as:

```markdown
### Code Review

**Reviewed commit:** 0123456789

🤖 Generated with <model name>
```

Render each inline comment as a badge and a title, with no category prefix:

```markdown
**<sub><sub>![P2 Badge](https://img.shields.io/badge/P2-yellow?style=flat)</sub></sub>  Gate the option on the actual request route**

When ... Please ...
```

Use badge colors `red` for P0/P1, `yellow` for P2, and `blue` for P3.

Never wrap a commit SHA in backticks anywhere in the review body or a finding
body. GitHub auto-links a bare 7-40 character hex SHA to its commit page; code
formatting suppresses that and leaves the reader grey text to copy by hand.
Separate consecutive SHAs with commas rather than slashes so the linkifier sees
clean word boundaries.

```markdown
after the fixes in eae67b92, bac8a00f, and 2d26170a     <- linked
after the fixes in `eae67b92`/`bac8a00f`/`2d26170a`     <- dead text
```

## Format and Post

1. Identify the target repository and pull request.
2. Resolve the PR's full current head SHA:

   ```bash
   gh pr view <number-or-url> --json headRefOid --jq .headRefOid
   ```

3. Validate only posting metadata: repository-relative paths, positive line numbers, `LEFT`/`RIGHT` sides, and multiline range order. Confirm each anchor belongs to the PR diff without evaluating the finding itself.
4. Create `review.json` using the supplied findings unchanged and the resolved SHA.
5. Resolve `<skill-dir>` to the directory containing this `SKILL.md`, then render the GitHub API payload:

   ```bash
   python3 <skill-dir>/scripts/format_inline_review.py review.json > review-payload.json
   ```

6. Inspect the payload to confirm the finding count, order, text, paths, lines, sides, and commit SHA match the supplied input.
7. Re-read the PR head SHA immediately before posting. If it changed, verify that each supplied anchor still refers to the same unchanged code in the new diff, without re-evaluating or changing the finding. If that is established, update `commit_id` in `review.json`, regenerate the payload for the new head SHA, and repeat step 6. Request updated anchors only when it cannot be established.
8. Post only when the user has explicitly asked to publish, submit, or leave the findings:

   ```bash
   gh api repos/<owner>/<repo>/pulls/<number>/reviews --method POST --input review-payload.json
   ```

9. Return the posted review URL, reviewed commit, and number of inline findings. If publishing was not requested, return the rendered draft without posting.

Do not create a no-findings review; this skill requires at least one supplied finding.
