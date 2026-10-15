#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-3.0-only
"""Create a NEW GitHub repository from this clean package using authenticated gh.

Run on the owner's Mac or Windows PC. Refuses existing .git histories, parent
repositories, existing remote repos, and unexpected public files. Never force-pushes,
never rewrites other repositories, and never reads GitHub tokens itself.
"""
from __future__ import annotations
import argparse
import ast
import importlib.util
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
REPO_NAME = "instagram-close-friends-windows"
SPEC = importlib.util.spec_from_file_location("publication_check", ROOT / "scripts" / "check_publish.py")
checker = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(checker)


def run(*arguments: str, check: bool = True) -> subprocess.CompletedProcess:
    env = os.environ.copy()
    env["GH_HOST"] = "github.com"
    return subprocess.run(list(arguments), cwd=ROOT, text=True, encoding="utf-8",
                          errors="replace", capture_output=True, check=check, env=env)


def require_fresh_folder(root: Path) -> None:
    if any((folder / ".git").exists() for folder in [root, *root.parents]):
        raise ValueError("This publisher only accepts a fresh extracted folder outside any existing Git repository. No remote writes made. Do not delete an existing repository to bypass this check.")
    if os.environ.get("GIT_DIR") or os.environ.get("GIT_WORK_TREE") or os.environ.get("GIT_INDEX_FILE"):
        raise ValueError("Clear custom GIT_DIR/GIT_WORK_TREE/GIT_INDEX_FILE settings before using the publisher.")


def commit_identity(profile: dict, owner: str | None) -> tuple[str, str]:
    login, user_id = profile.get("login"), profile.get("id")
    if not isinstance(login, str) or not re.fullmatch(r"[A-Za-z0-9-]{1,39}", login):
        raise ValueError("Could not validate the authenticated GitHub username.")
    if not isinstance(user_id, int) or isinstance(user_id, bool) or user_id <= 0:
        raise ValueError("Could not validate the authenticated GitHub user ID.")
    if owner and login.lower() != owner.lower():
        raise ValueError(f"gh is signed in as {login}, not the requested owner. Switch gh accounts before publishing.")
    return login, f"{user_id}+{login}@users.noreply.github.com"



def configure_repository(target: str) -> dict:
    """Only call for the NEW repository just created by this invocation.

    Makes the Issues tab explicit and checks the returned repository settings.
    This does not create any issues or publish any account data.
    """
    run("gh", "repo", "edit", target,
        "--enable-issues", "--enable-wiki=false", "--default-branch", "main",
        "--add-topic", "windows", "--add-topic", "python",
        "--add-topic", "playwright", "--add-topic", "instagram",
        "--add-topic", "close-friends")
    details = json.loads(run("gh", "api", "--hostname", "github.com", f"repos/{target}").stdout)
    if (not isinstance(details, dict)
            or details.get("full_name", "").lower() != target.lower()
            or details.get("has_issues") is not True
            or details.get("default_branch") != "main"):
        raise ValueError("Source upload completed, but repository/Issues settings were not confirmed. Inspect the newly created repository; do not create a duplicate.")
    return details

def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--owner", help="Refuse to publish unless gh is signed in as this personal account.")
    visibility = parser.add_mutually_exclusive_group()
    visibility.add_argument("--private", action="store_true", help="Default: create a private repo for validation.")
    visibility.add_argument("--public", action="store_true", help="Publish the clean source publicly.")
    parser.add_argument("--check-only", action="store_true", help="Offline package review; no GitHub access or writes.")
    args = parser.parse_args(argv)
    names = checker.public_files(ROOT)
    issues = checker.inspect_tree(ROOT, names)
    for name in names:
        if name.endswith(".py"):
            ast.parse((ROOT / name).read_text(encoding="utf-8"), filename=name)
    if issues:
        raise ValueError("Public-file check failed:\n" + "\n".join(issues))
    print(f"SOURCE CHECK PASSED: {len(names)} intended public files.")
    print("This limited check is not a complete secret/security audit. Review the source yourself.")
    if args.check_only:
        print("CHECK ONLY: no GitHub access, repository creation or push.")
        return 0
    require_fresh_folder(ROOT)
    for name in ("git", "gh"):
        if not shutil.which(name):
            raise ValueError(f"{name} is not installed. Install it and reopen your terminal.")
    profile = json.loads(run("gh", "api", "--hostname", "github.com", "user").stdout)
    owner, email = commit_identity(profile, args.owner)
    target = f"{owner}/{REPO_NAME}"
    # An authenticated repository-list read avoids mistaking an HTTP error for nonexistence.
    listed = json.loads(run("gh", "api", "--hostname", "github.com", "--paginate", "--slurp",
                            "user/repos?affiliation=owner&per_page=100").stdout)
    repos = [repo for page in listed for repo in page]
    if any(repo.get("full_name", "").lower() == target.lower() for repo in repos):
        raise ValueError(f"{target} already exists. This publisher will not overwrite it.")
    visibility_word = "PUBLIC" if args.public else "PRIVATE"
    phrase = f"CREATE {target} {visibility_word}"
    print(f"\nCreate NEW {visibility_word.lower()} repository: {target}")
    print("Commit author uses your GitHub ID-based noreply address, not your personal email.")
    print("Only intended source files will be staged; personal account data is not part of this package.")
    print("The new repository will have Issues enabled, with bug/setup/feature forms.")
    if args.public:
        print("PUBLIC means anyone can view and copy the published source files.")
    if input(f"Type {phrase}: ").strip() != phrase:
        print("Cancelled. No repository created.")
        return 0
    run("git", "init", "-b", "main")
    run("git", "config", "user.name", owner)
    run("git", "config", "user.email", email)
    run("git", "config", "core.autocrlf", "false")
    # No dependence on a user's unavailable GPG signing key for this initial commit.
    run("git", "config", "commit.gpgsign", "false")
    run("git", "add", "--", *names)
    staged_issues = checker.inspect_index(ROOT, names)
    if staged_issues:
        raise ValueError("Staged-file review failed; no commit/push performed:\n" + "\n".join(staged_issues))
    print(run("git", "diff", "--cached", "--stat").stdout)
    # Explicit author/committer prevent inherited personal-email environment variables.
    commit_env = os.environ.copy()
    commit_env.update(GIT_AUTHOR_NAME=owner, GIT_COMMITTER_NAME=owner,
                      GIT_AUTHOR_EMAIL=email, GIT_COMMITTER_EMAIL=email)
    subprocess.run(["git", "commit", "-m", "Initial Windows beta: native locks, Windows launcher and offline tests"],
                   cwd=ROOT, env=commit_env, check=True)
    run("gh", "auth", "setup-git", "--hostname", "github.com")
    # A failure here may still leave a newly created remote; never force or silently retry.
    created = run("gh", "repo", "create", target, "--public" if args.public else "--private",
                  "--source", str(ROOT), "--remote", "origin", "--push", "--disable-wiki",
                  "--description", "Windows-only beta: Instagram Close Friends CSV helper with manual login, separate verification, and issue-report forms.")
    print(created.stdout)
    print(f"SOURCE UPLOADED: https://github.com/{target}")
    configure_repository(target)
    print(f"UPLOADED AND ISSUES ENABLED: https://github.com/{target}")
    print(f"Issues: https://github.com/{target}/issues")
    print("Bug report, setup-help and feature-request forms are included on main.")
    print("Review Actions > Windows tests. Native Windows/live Instagram validation is not implied by upload.")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (ValueError, OSError, SyntaxError, json.JSONDecodeError, EOFError) as exc:
        print(f"PUBLISH ERROR: {exc}", file=sys.stderr)
        raise SystemExit(1)
    except subprocess.CalledProcessError as exc:
        print("PUBLISH STOPPED: a Git/GitHub command failed. No force-push or automatic retry was performed.", file=sys.stderr)
        print((exc.stderr or str(exc)).strip(), file=sys.stderr)
        print("Review gh auth status and the target repo before retrying. See docs/PUBLISHING.md for partial-upload recovery.", file=sys.stderr)
        raise SystemExit(1)
