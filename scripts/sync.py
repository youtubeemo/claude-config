#!/usr/bin/env python3
"""Create reviewable PRs for managed Claude instructions; never merge or run production."""
import base64
import json
import os
from pathlib import Path
import re
import sys
import urllib.error
import urllib.parse
import urllib.request

OWNER = "youtubeemo"
REPOS = ("gta-shorts-germany", "storyhouse-originals", "cartoon-story-universe",
         "dschungel-freunde", "gta-shorts-website")
BRANCH = "automation/claude-config-sync"
ROOT = Path(__file__).resolve().parents[1]
TOKEN = os.getenv("SYNC_TOKEN", "")
DRY_RUN = os.getenv("DRY_RUN", "false").lower() == "true"
SPECS = (
    ("CLAUDE.md", "skill-config", ROOT / "managed/skill-config.md"),
    ("AGENTS.md", "agent-rules", ROOT / "managed/agent-rules.md"),
)

def api(method, path, payload=None):
    url = "https://api.github.com" + path
    data = None if payload is None else json.dumps(payload).encode()
    request = urllib.request.Request(
        url, data=data, method=method,
        headers={"Authorization": "Bearer " + TOKEN,
                 "Accept": "application/vnd.github+json",
                 "X-GitHub-Api-Version": "2022-11-28",
                 "User-Agent": "claude-config-sync",
                 "Content-Type": "application/json"})
    with urllib.request.urlopen(request, timeout=30) as response:
        return json.load(response)

def file_at(repo, path, ref):
    escaped = urllib.parse.quote(path, safe="/")
    item = api("GET", f"/repos/{OWNER}/{repo}/contents/{escaped}?ref={urllib.parse.quote(ref, safe='')}")
    return base64.b64decode(item["content"]).decode(), item["sha"]

def update_block(text, label, new_text):
    start = f"<!-- {label}:start v1.0.0"
    end = f"<!-- {label}:end -->"
    # Preserve original start marker and everything outside the managed region.
    pattern = re.compile(r"(" + re.escape(start) + r"[^\n]*\n)(.*?)(" + re.escape(end) + r")", re.S)
    if len(pattern.findall(text)) != 1:
        raise ValueError(f"Expected exactly one managed block: {label}")
    return pattern.sub(lambda m: m.group(1) + new_text.rstrip() + "\n" + m.group(3), text)

def run(repo):
    default = api("GET", f"/repos/{OWNER}/{repo}")["default_branch"]
    edits = []
    for path, label, source in SPECS:
        current, _ = file_at(repo, path, default)
        updated = update_block(current, label, source.read_text())
        if current != updated:
            edits.append((path, updated))
    if not edits:
        print(f"{repo}: already synchronized")
        return
    if DRY_RUN:
        print(f"{repo}: would update {', '.join(p for p, _ in edits)}")
        return
    base_sha = api("GET", f"/repos/{OWNER}/{repo}/git/ref/heads/{default}")["object"]["sha"]
    try:
        api("POST", f"/repos/{OWNER}/{repo}/git/refs",
            {"ref": "refs/heads/" + BRANCH, "sha": base_sha})
    except urllib.error.HTTPError as exc:
        if exc.code != 422:
            raise
        # Do not overwrite a branch or modify an existing open PR.
        print(f"{repo}: sync branch exists; review existing PR first")
        return
    for path, content in edits:
        # New branch initially points to default; fetch the SHA from that branch.
        _, sha = file_at(repo, path, BRANCH)
        api("PUT", f"/repos/{OWNER}/{repo}/contents/{path}",
            {"message": "Sync managed Claude instructions", "branch": BRANCH,
             "sha": sha, "content": base64.b64encode(content.encode()).decode()})
    pr = api("POST", f"/repos/{OWNER}/{repo}/pulls",
             {"title": "Sync central Claude instructions",
              "head": BRANCH, "base": default,
              "body": "Only managed blocks in CLAUDE.md and AGENTS.md. No production code, workflows, secrets, or plugin settings changed."})
    print(f"{repo}: {pr['html_url']}")

def main():
    if not TOKEN:
        print("SYNC_TOKEN is missing; no remote changes made.", file=sys.stderr)
        sys.exit(2)
    failures = 0
    for repo in REPOS:
        try:
            run(repo)
        except Exception as exc:
            failures += 1
            print(f"{repo}: ERROR {exc}", file=sys.stderr)
    sys.exit(1 if failures else 0)

if __name__ == "__main__":
    main()
