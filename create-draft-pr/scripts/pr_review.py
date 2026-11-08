#!/usr/bin/env python3
"""Helpers for the PR review routine. Needs `gh` logged in; run it from a clone of the PR's repository.

  pr_review.py wait   <PR> [--minutes N]                        print new comments until every check on the head is done
  pr_review.py read   <PR> [--review-id ID]                     print every new comment in full, or one review
  pr_review.py verify <PR> --body-file FILE [--base origin/main] check the published PR body against the file
  pr_review.py reply  <PR> <COMMENT_ID> <FILE> [--dry-run]       reply inside a review thread

Why a script: the review APIs have traps that cost rounds. A comment is new when someone other than you posted it
after the head commit's committer date; your own thread replies appear as COMMENTED reviews, so your login is
skipped. Comments come from three endpoints: reviews, inline review comments, and PR timeline comments. A later round often has no
inline comments, and its findings sit in the review body under "Additional findings" (Copilot: "Suppressed").
Findings in those sections count. `closingIssuesReferences` shows a new `Fixes #N` about ten seconds after a body edit.

`wait` polls the head commit's check runs rather than `actions/runs`: check runs cover every Actions job and any
app-posted check. It ends when they are all complete on two polls in a row, since a hook can post just after its
check ends.
"""

from __future__ import annotations

import argparse
import difflib
import json
import re
import subprocess
import sys
import time


def gh(*args: str) -> str:
    result = subprocess.run(["gh", *args], capture_output=True, text=True)
    if result.returncode != 0:
        sys.exit(f"gh {' '.join(args[:2])} failed: {result.stderr.strip()}")
    return result.stdout


def api_list(path: str, items: str = ".[]") -> list[dict]:
    """Every item of a paginated list endpoint. `--jq` prints one JSON object per line."""
    out = gh("api", path, "--paginate", "--jq", items)
    return [json.loads(line) for line in out.splitlines() if line.strip()]


def repo_name(explicit: str | None) -> str:
    return explicit or gh("repo", "view", "--json", "nameWithOwner", "--jq", ".nameWithOwner").strip()


def pr_info(repo: str, pr: str, *fields: str) -> dict:
    return json.loads(gh("pr", "view", pr, "-R", repo, "--json", ",".join(fields)))


def head_and_since(repo: str, pr: str) -> tuple[str, str]:
    """The head SHA and its committer date: comments after that date are new."""
    info = pr_info(repo, pr, "headRefOid", "commits")
    head = info["headRefOid"]
    return head, next(c["committedDate"] for c in info["commits"] if c["oid"] == head)


def new_comments(repo: str, pr: str, since: str, me: str) -> list[dict]:
    """Reviews, inline comments, and timeline comments by others since `since`, oldest first. Pending reviews are skipped."""
    found = [
        {"kind": "review", "id": r["id"], "user": r["user"]["login"], "at": r["submitted_at"], "body": r.get("body") or "",
         "where": f"{r['state']} on {r['commit_id'][:8]}"}
        for r in api_list(f"repos/{repo}/pulls/{pr}/reviews")
        if r.get("submitted_at")
    ]
    found += [
        {"kind": "inline" if c.get("in_reply_to_id") is None else "inline reply", "id": c["id"], "user": c["user"]["login"],
         "at": c["created_at"], "body": c["body"], "where": f"{c['path']}:{c.get('line')} in review {c['pull_request_review_id']}"}
        for c in api_list(f"repos/{repo}/pulls/{pr}/comments")
    ]
    found += [
        {"kind": "comment", "id": c["id"], "user": c["user"]["login"], "at": c["created_at"], "body": c["body"], "where": "timeline"}
        for c in api_list(f"repos/{repo}/issues/{pr}/comments")
    ]
    # GitHub timestamps share one ISO format, so they compare as strings.
    return sorted((c for c in found if c["user"] != me and c["at"] >= since), key=lambda c: c["at"])


def describe(c: dict) -> str:
    return f"{c['kind']} {c['id']} by {c['user']} at {c['at']} | {c['where']}"


def cmd_wait(args: argparse.Namespace) -> int:
    """Exit 0: every check complete on two polls in a row. 3: timed out."""
    repo = repo_name(args.repo)
    head, since = head_and_since(repo, args.pr)
    me = gh("api", "user", "--jq", ".login").strip()
    print(f"watching {head[:8]}: comments by others since {since}, until every check completes; every {args.interval}s for up to {args.minutes} minutes", flush=True)
    started = time.time()
    seen: set[tuple[str, int]] = set()
    settled = 0  # consecutive polls with every check complete
    while True:
        waited = int(time.time() - started)
        comments = new_comments(repo, args.pr, since, me)
        for c in comments:
            if (c["kind"], c["id"]) not in seen:
                seen.add((c["kind"], c["id"]))
                print(f"  + {describe(c)}", flush=True)
        checks = api_list(f"repos/{repo}/commits/{head}/check-runs", ".check_runs[]")
        pending = [c["name"] for c in checks if c["status"] != "completed"]
        print(
            f"[{waited // 60}m{waited % 60:02d}s] new comments {len(comments)} | checks complete {len(checks) - len(pending)}/{len(checks)}"
            + (f" | pending: {', '.join(pending)}" if pending else ""),
            flush=True,
        )
        settled = settled + 1 if checks and not pending else 0
        if settled == 2 or waited >= args.minutes * 60:
            break
        time.sleep(args.interval)
    for c in checks:
        print(f"  check {c['name']}: {c['conclusion'] or c['status']}")
    reviews = sum(c["kind"] == "review" for c in comments)
    if settled == 2:
        print(f"CHECKS DONE on {head[:8]}: {len(comments)} new comments, {reviews} of them reviews")
        return 0
    print(f"TIMED OUT after {args.minutes} minutes on {head[:8]}: {len(comments)} new comments, {len(pending)} checks pending")
    return 3


def readable(body: str) -> str:
    """The review body as plain text: icons shortened, summaries as headings, details tags removed."""
    text = re.sub(r"<picture>.*?</picture>", "[icon]", body, flags=re.S)
    text = text.split("<summary><strong>What changed in this PR</strong>")[0]
    text = re.sub(r"<summary>(.*?)</summary>", lambda m: "\n### " + re.sub(r"</?strong>", "", m.group(1)).strip(), text, flags=re.S)
    text = re.sub(r"</?details[^>]*>|</?strong>|<!--.*?-->", "", text, flags=re.S)
    return re.sub(r"\n{3,}", "\n\n", text).strip()


def cmd_read(args: argparse.Namespace) -> int:
    repo = repo_name(args.repo)
    head, since = head_and_since(repo, args.pr)
    if args.review_id:
        review = json.loads(gh("api", f"repos/{repo}/pulls/{args.pr}/reviews/{args.review_id}"))
        print(f"review {review['id']} by {review['user']['login']} | {review['state']} | commit {review['commit_id'][:8]} | head {head[:8]}\n")
        print(readable(review.get("body") or ""))
        comments = [
            c
            for c in api_list(f"repos/{repo}/pulls/{args.pr}/comments")
            if c["pull_request_review_id"] == review["id"] and c.get("in_reply_to_id") is None
        ]
        print(f"\n=== root inline comments of this review: {len(comments)}")
        for c in comments:
            print(f"\n##### comment {c['id']} | {c['path']}:{c.get('line')}\n{c['body']}")
        return 0
    me = gh("api", "user", "--jq", ".login").strip()
    comments = new_comments(repo, args.pr, since, me)
    print(f"head {head[:8]} committed {since} | new comments by others: {len(comments)}")
    for c in comments:
        print(f"\n##### {describe(c)}\n{readable(c['body']) if c['kind'] == 'review' else c['body']}")
    return 0 if comments else 3


def cmd_verify(args: argparse.Namespace) -> int:
    repo = repo_name(args.repo)
    info = pr_info(repo, args.pr, "body", "title", "isDraft", "headRefOid", "closingIssuesReferences")
    wanted = open(args.body_file).read().rstrip("\n")
    live = info["body"].rstrip("\n")
    problems = []
    if live != wanted:
        problems.append("the published body differs from the file")
        diff = difflib.unified_diff(wanted.splitlines(), live.splitlines(), "file", "published", lineterm="", n=0)
        print("\n".join(list(diff)[:20]))
    print(f"title: {info['title']}")
    print(f"draft: {info['isDraft']} | head: {info['headRefOid'][:8]} | closing issues: {[i['number'] for i in info['closingIssuesReferences']]}")
    backticked = re.findall(r"`[0-9a-f]{7,40}`", live)
    print(f"commit hashes in backticks (they must be bare to autolink): {len(backticked)}")
    if backticked:
        problems.append("backticked commit hashes")
    # The PR's own head decides the range, so a commit that exists only locally is not flagged.
    head = info["headRefOid"]
    local = subprocess.run(["git", "cat-file", "-e", f"{head}^{{commit}}"], capture_output=True).returncode == 0
    span = f"{args.base}..{head if local else 'HEAD'}"
    log = subprocess.run(["git", "log", "--format=%h", span], capture_output=True, text=True)
    if log.returncode == 0 and log.stdout.split():
        commits = log.stdout.split()
        missing = [c for c in commits if c not in live]
        print(f"commits in {args.base}..{head[:8] if local else 'HEAD'}: {len(commits)} | not mentioned in the body: {missing}")
        if missing:
            problems.append("commits missing from the body")
    html = gh("api", f"repos/{repo}/pulls/{args.pr}", "-H", "Accept: application/vnd.github.html+json", "--jq", ".body_html")
    links = set(re.findall(r'href="[^"]*/commit/([0-9a-f]{40})"', html))
    print(f"rendered: {len(links)} unique commit links | {html.count('<details')} details | {html.count('<table')} tables | {len(re.findall(r'lang=.mermaid.', html))} mermaid blocks")
    print("OK" if not problems else "PROBLEMS: " + "; ".join(problems))
    return 0 if not problems else 1


def cmd_reply(args: argparse.Namespace) -> int:
    repo = repo_name(args.repo)
    text = open(args.file).read()
    if args.dry_run:
        print(f"would reply to comment {args.comment_id} on PR {args.pr}:\n{text[:300]}")
        return 0
    # -F reads the file. With -f the body would be the literal text "@file".
    out = gh("api", f"repos/{repo}/pulls/{args.pr}/comments/{args.comment_id}/replies", "-F", f"body=@{args.file}")
    reply = json.loads(out)
    print(f"reply {reply['id']} in thread of {reply['in_reply_to_id']}: {reply['body'][:60]!r}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--repo", help="owner/name; default: the repository of the current directory")
    sub = parser.add_subparsers(dest="command", required=True)
    wait = sub.add_parser("wait")
    wait.add_argument("pr")
    wait.add_argument("--minutes", type=int, default=60)
    wait.add_argument("--interval", type=int, default=60)
    read = sub.add_parser("read")
    read.add_argument("pr")
    read.add_argument("--review-id")
    verify = sub.add_parser("verify")
    verify.add_argument("pr")
    verify.add_argument("--body-file", required=True)
    verify.add_argument("--base", default="origin/main")
    reply = sub.add_parser("reply")
    reply.add_argument("pr")
    reply.add_argument("comment_id")
    reply.add_argument("file")
    reply.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    return {"wait": cmd_wait, "read": cmd_read, "verify": cmd_verify, "reply": cmd_reply}[args.command](args)


if __name__ == "__main__":
    sys.exit(main())
