---
name: create-draft-pr
description: Create a draft PR. Run bounded automated review rounds only when the user explicitly requests the PR review routine or asks to take a PR through automated review.
---

# PR Routine

For a request to create a PR, complete section 1 and return its URL. Do not wait for reviews unless the user explicitly requests the review routine.

For an explicitly requested routine, inspect the current PR or create a draft if needed, wait for the designated reviewer's completed review of the current head, validate its findings, and fix authorized in-scope defects. Push fixes and reply to review threads only within the user's authorization. Continue until a completed review has no new findings or the agreed limit is reached.

Unless the user supplies other limits, allow at most 3 completed review rounds and 30 minutes of total review waiting across the routine. State these defaults when starting; do not pause to ask about optional overrides. Stop starting new rounds at the limit, finish any in-progress local correction safely, and report unreviewed changes or unresolved findings without calling the loop clean.

Steps 3 and 6 are where this goes wrong in practice — the comments are not where they look like they should be, and replies land in the wrong place. Those sections are the reason this skill exists.

## 1. Open the draft PR

Before creating, confirm the branch is pushed, in sync, and carries only commits that belong to this PR:

```bash
git rev-list --left-right --count @{u}...HEAD    # want "0  0"
git log --oneline <base>..HEAD                   # every line must belong here
```

If unrelated commits are present, report them. Move or rewrite commits only when changing the branch history is already authorized.

Use `$write-pr` for the title and body, then:

```bash
gh pr create --draft --base master --head "$(git branch --show-current)" \
  --title "fix(scope): Imperative summary" --body-file pr-body.md
```

Return the draft PR URL once created. Continue below only for an explicitly requested automated review routine; first verify that the designated reviewer is available and review has been requested or configured for this PR.

## 2. Wait for the review

Use the environment's supported asynchronous wait or background execution tools, with short bounded polls when needed. Do not assume a particular `run_in_background` parameter exists. Count all waiting against the routine's remaining time budget.

Resolve `REPO`, `PR`, the current `HEAD_SHA`, and `REVIEWER` from the target PR and the designated reviewer. Inspect submitted reviews, not just new inline comments:

```bash
gh api "repos/$REPO/pulls/$PR/reviews" --paginate \
  --jq '.[] | {id, reviewer: .user.login, commit_id, state, submitted_at}'
```

A completed round requires a previously unprocessed, submitted review by `REVIEWER` whose `commit_id` equals the current head SHA and whose state is `COMMENTED`, `APPROVED`, or `CHANGES_REQUESTED`. Zero inline comments can still be a completed review. Record processed review and comment IDs in the task state.

Re-read the PR head before accepting completion; a review for an older head does not establish coverage of the new one. After a push, verify that a new review is actually scheduled or request one if authorized. If the reviewer is unavailable, no review is scheduled, the API fails persistently, or the time budget expires, report the pending state and end this invocation. Do not treat missing comments or an API error as a clean review, and do not create a monitor unless requested.

## 3. Read the findings

**`gh pr view --json comments` returns `[]` for review comments.** It reads the issue-comment timeline; Copilot's findings are pull-request *review* comments and live on a different endpoint. Looking only there reads as "no feedback" when there are findings waiting.

Two surfaces, both worth reading:

```bash
# The overview Copilot posts (file table, what it reviewed, how many comments).
# Splitting on "<details>" drops the suppressed-comments block — see below.
gh pr view "$PR" --json reviews \
  --jq '.reviews[] | {author: .author.login, state, body: (.body | split("<details>")[0])}'

# The actual findings
gh api "repos/$REPO/pulls/$PR/comments" --paginate \
  --jq '.[] | {id, pull_request_review_id, user: .user.login, path, line, in_reply_to_id, body}'
```

- Select comments belonging to the completed review via `pull_request_review_id` and the designated reviewer. Root findings have `in_reply_to_id: null`; filter out replies and already handled comment IDs.
- **Do not truncate this output.** No `| head`, and skip any wrapper that caps stdout: comment bodies get cut mid-sentence and you act on half a finding. Pull one body in full with
  `gh api "repos/$REPO/pulls/comments/$ID" --jq '.body'`.
- Record handled comment IDs alongside processed review IDs in the task state; new comment arrival alone does not establish that a review is complete.

**Ignore suppressed comments.** Copilot's review body often ends with a collapsed `<details><summary>Suppressed comments (N)</summary>` block, typically labelled "Previously missed — in code that hasn't changed since the last review". Those are not input to this loop. Copilot withheld them itself, they carry no comment id and so have no thread to answer in, and they target code the round did not touch — so working them turns a converging loop into an open-ended audit of the entire diff, growing the change set every round and delaying the human review the routine exists to reach. Do not fix them, do not reply to them, do not count them as findings.

Only the inline comments from the `pulls/$PR/comments` endpoint drive steps 4 through 7. If a suppressed item names something you believe is a genuine defect, that is separate work: finish the loop first, then raise it on its own.

Also check whether tests actually run on this PR:

```bash
gh pr view "$PR" --json statusCheckRollup --jq '[.statusCheckRollup[] | {name, conclusion}]'
```

If no test job appears, say so when you report — a green PR page is not a green suite, and your local run is the only evidence there is.

## 4. Validate before fixing

Load `$receiving-code-review` and follow it. The short version: verify each claim against the code before touching anything, and push back with reasoning when it does not hold.

Copilot is right often enough to take seriously and wrong often enough that you must check. From one real run of this loop, three findings:

| Finding | Verdict |
|---|---|
| A captured local went stale after an in-place refresh | Real bug, and worse than described — the staleness outlived the retry |
| An error payload reached API consumers via a store the raise site never mentions | Real, and the most severe of the three — and it only appeared in **round 2** |
| An un-awaited cancelled task "keeps this test flaky" | Cause did not hold — but a genuine unrelated defect sat on the same line |

Three lessons in that table:

- **Findings can arrive in later rounds.** After pushing a fix, seek review of the new head within the remaining round and waiting budgets.
- **A wrong reason can still point at a bad line.** When you refute the stated cause, read the line anyway before moving on.
- **Claims about reachability deserve a probe, not reasoning.** Trace the path and run something.

When authorized to reply, explain refuted claims in-thread with evidence. Fix defects covered by the finding or necessary to complete the request; report unrelated nearby defects separately. Do not implement a change whose justification you know to be wrong.

## 5. Fix in cohesive commits

One commit per finding or per coherent group — never one squashed catch-all. The reviewer needs to see which change answers which comment, and a bad call has to be revertible on its own.

Run checks that demonstrate the fix and the project's required checks. Add regression coverage when it meaningfully distinguishes the defect from corrected behavior. Revert and reapply a fix to test the test only when its ability to detect the defect remains uncertain. Run the full suite when required by the project or justified by the change's risk; otherwise use affected tests. Report the checks actually performed and their results.

## 6. Push and reply

Reply **in the thread**, not as a top-level PR comment — a top-level reply orphans the discussion from the line it is about:

```bash
gh api "repos/$REPO/pulls/$PR/comments/$COMMENT_ID/replies" -F body=@reply.txt
```

`-F`, not `-f`. With `-f` the comment body posts as the literal string `@reply.txt`. See `$gh-api-file-body-flag`.

A good reply names the commit SHA, states what was verified and how, and is explicit when you disagreed. Include the evidence — the failing assertion, the probe output — rather than claiming the check happened.

Update the PR body in the same pass when the change set moved:

```bash
gh pr edit "$PR" --body-file pr-body.md
```

## 7. Loop

After a fix is pushed, return to section 2 only within the remaining budget and when another review is scheduled or can be requested within authorization.

End cleanly only after reading a completed review of the current head with no new root-level inline findings and no unresolved requested changes from the routine. A completed review containing only suppressed comments may end the loop if there are no unresolved requested changes; never classify a `CHANGES_REQUESTED` review as clean solely because it has no inline comments. If all findings were refuted with evidence and no code changed, report that disposition and stop without manufacturing a push or another round.

At the round or waiting limit, return the current PR URL, reviewed and current SHAs, remaining findings, and whether the latest changes still await review. Do not extend the budget automatically or label that state clean.

When the loop is done, report: rounds run, findings per round, which you accepted and which you refuted and why, the verification evidence, and whether CI ran tests.

**Leave the PR in draft.** Do not run `gh pr ready`. Inviting human reviewers is the author's call — they may want another look at the diff, a live test run, or a decision on something you escalated before anyone is notified. Report the actual outcome: clean, findings refuted, pending review, or budget reached. Only a clean outcome supports saying the review loop is complete.

## Guardrails

- Every fix is scoped to the finding. A review comment is not license to refactor.
- Only inline review comments are findings. Suppressed comments are out of scope for the loop.
- Never widen a client-facing surface to satisfy an observability request — check where an error message or payload actually travels before enriching it.
- Do not add unrelated commits during the loop. Report any that appear; move or rewrite them only within existing authorization to change branch history.
- Never report the loop as clean on a round you did not actually read.
