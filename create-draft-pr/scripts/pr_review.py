#!/usr/bin/env python3
"""Helpers for the PR review routine. Needs `gh` logged in; run it from a clone of the PR's repository.

  pr_review.py wait   <PR> [--reviewer LOGIN] [--minutes N]     wait for a completed review of the current head
  pr_review.py read   <PR> [--review-id ID] [--reviewer LOGIN]  print one review in full, with its inline comments
  pr_review.py verify <PR> --body-file FILE [--base origin/main] check the published PR body against the file
  pr_review.py reply  <PR> <COMMENT_ID> <FILE> [--dry-run]       reply inside a review thread

Why a script: the review APIs have traps that cost rounds. Your own thread replies appear as COMMENTED reviews under
your login on the same commit, so reviews are selected by reviewer login and commit. A later round often has no
inline comments, and its findings sit in the review body under "Previously missed" or "Suppressed". Findings in
those sections count. `closingIssuesReferences` shows a new `Fixes #N` about ten seconds after a body edit.
"""

import argparse
import difflib
import json
import re
import subprocess
import sys
import time

BOT = "copilot-pull-request-reviewer[bot]"
DONE = {"COMMENTED", "APPROVED", "CHANGES_REQUESTED"}


def gh(*args: str) -> str:
    result = subprocess.run(["gh", *args], capture_output=True, text=True)
    if result.returncode != 0:
        sys.exit(f"gh {' '.join(args[:2])} failed: {result.stderr.strip()}")
    return result.stdout


def api_list(path: str) -> list[dict]:
    """Every item of a paginated list endpoint. `--jq .[]` prints one JSON object per line."""
    out = gh("api", path, "--paginate", "--jq", ".[]")
    return [json.loads(line) for line in out.splitlines() if line.strip()]


def repo_name(explicit: str | None) -> str:
    return explicit or gh("repo", "view", "--json", "nameWithOwner", "--jq", ".nameWithOwner").strip()


def pr_info(pr: str, *fields: str) -> dict:
    return json.loads(gh("pr", "view", pr, "--json", ",".join(fields)))


def completed_reviews(repo: str, pr: str, reviewer: str, commit: str | None) -> list[dict]:
    reviews = api_list(f"repos/{repo}/pulls/{pr}/reviews")
    return [
        r
        for r in reviews
        if r["user"]["login"] == reviewer and r["state"] in DONE and (commit is None or r["commit_id"] == commit)
    ]


def cmd_wait(args: argparse.Namespace) -> int:
    repo = repo_name(args.repo)
    head = pr_info(args.pr, "headRefOid")["headRefOid"]
    print(f"waiting for {args.reviewer} on {head[:8]} (up to {args.minutes} minutes)", flush=True)
    started = time.time()
    while time.time() - started < args.minutes * 60:
        found = completed_reviews(repo, args.pr, args.reviewer, head)
        if found:
            r = found[-1]
            waited = int(time.time() - started)
            print(
                f"COMPLETED review_id={r['id']} state={r['state']} commit={head[:8]} "
                f"submitted_at={r['submitted_at']} waited={waited // 60}m{waited % 60:02d}s"
            )
            return 0
        time.sleep(args.interval)
    print(f"NO COMPLETED REVIEW of {head[:8]} within {args.minutes} minutes")
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
    head = pr_info(args.pr, "headRefOid")["headRefOid"]
    if args.review_id:
        review = json.loads(gh("api", f"repos/{repo}/pulls/{args.pr}/reviews/{args.review_id}"))
    else:
        found = completed_reviews(repo, args.pr, args.reviewer, head)
        if not found:
            print(f"No completed review by {args.reviewer} of the current head {head[:8]}.")
            return 3
        review = found[-1]
    print(f"review {review['id']} | {review['state']} | commit {review['commit_id'][:8]} | submitted {review['submitted_at']}")
    print(f"current head: {head[:8]} ({'this review covers it' if review['commit_id'] == head else 'THIS REVIEW IS OF AN OLDER HEAD'})\n")
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


def cmd_verify(args: argparse.Namespace) -> int:
    repo = repo_name(args.repo)
    info = pr_info(args.pr, "body", "title", "isDraft", "headRefOid", "closingIssuesReferences")
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
    wait.add_argument("--reviewer", default=BOT)
    wait.add_argument("--minutes", type=int, default=25)
    wait.add_argument("--interval", type=int, default=30)
    read = sub.add_parser("read")
    read.add_argument("pr")
    read.add_argument("--review-id")
    read.add_argument("--reviewer", default=BOT)
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
