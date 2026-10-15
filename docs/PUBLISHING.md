# Publish the Windows-only repository

**Intended repository:** `BachYun/instagram-close-friends-windows`  
**Display title:** Instagram Close Friends — Windows Only  
**Package:** `0.1.0b2` / `v0.1.0-beta.2`

A Windows PC or virtual machine is not needed to publish this code. The publisher runs
on your Mac with Python, Git and GitHub CLI. Running the Instagram helper on Windows is
a separate operation. The package itself does not mean a remote repository exists.

## Prerequisites

Use Python 3.12+ and installed `git` and `gh`. Your existing Mac Python/GitHub setup can
be used; Playwright does not need to be installed just to upload. On a Mac where GitHub
CLI is missing, install it through your existing Homebrew installation with `brew install gh`.
Do not install a new VM for this task.

Authenticate locally if needed, using the browser sign-in flow rather than pasting tokens:

```text
gh auth login --hostname github.com --git-protocol https --web --scopes workflow
gh auth setup-git --hostname github.com
gh auth status
```

The workflow scope can be needed when an OAuth/PAT-based login uploads `.github/workflows`.
Follow account/organization policies; this is not a reason to bypass their controls.

## Publish from the Mac — one command block

Save `instagram-close-friends-windows-v0.1.0-beta.2.zip` to Downloads. Review its source.
The extraction folder must be new and outside any other Git repository. Then run:

```bash
cd "$HOME" &&
unzip -n "$HOME/Downloads/instagram-close-friends-windows-v0.1.0-beta.2.zip" &&
cd "$HOME/instagram-close-friends-windows" &&
python3.12 scripts/publish_github.py --check-only &&
python3.12 scripts/publish_github.py --owner BachYun --public
```

The command uses `&&` so later steps do not run if an earlier step fails. Do not paste
a filename with `(1)` unless that is the file you actually downloaded; move/rename the
reviewed archive to the exact shown name or adjust the path. Do not mix this package
with the previous `instagram-close-friends-playwright-windows` directory.

**`--public` publishes the source to everyone.** At the confirmation prompt, type:

```text
CREATE BachYun/instagram-close-friends-windows PUBLIC
```

Default publication is private when no visibility flag is supplied. The command above
chooses public deliberately. For private publication, pass `--private` and use the displayed
PRIVATE confirmation. Private visibility is not a reason to upload account secrets.

## What the publisher does

1. Reads the public-file manifest, checks intended source bytes, and parses Python files.
2. Confirms a fresh folder, an authenticated personal GitHub account and an unused repo name.
3. Shows the owner, name, visibility and requested confirmation before any Git writes.
4. Initializes a new `main` history. It does not copy history from your Mac repository.
5. Uses the authenticated user's ID-based GitHub noreply commit address and sets explicit
   author/committer identity, avoiding a personal-email environment override.
6. Stages only manifest files and checks the staged contents before committing/pushing.
7. Creates and pushes the new repository through `gh repo create`.
8. Enables Issues, disables the wiki, sets `main` as default and adds Windows/Python/Playwright
   topics. It reads back the repository settings to verify the name/default/Issues flag.
9. Prints repository and Issues URLs. It does not create any issue tickets or release tags.

The check is limited defense in depth, not a complete security audit. Inspect the source;
actual followers, progress logs, passwords, browser profiles and exports must stay outside.
The tool never force-pushes, rewrites another repo, stops an unrelated process or uploads
runtime files. GitHub operations use your local CLI credentials, which it does not print.

## Confirm the remote result

After `UPLOADED AND ISSUES ENABLED`:

```text
gh repo view BachYun/instagram-close-friends-windows --web
```

In GitHub, check **Code** for README/docs, **Issues -> New issue** for the three forms,
and **Actions -> Windows tests** for the CI result. A source upload is not a passing
Windows test. A runner `startup_failure` without executed steps is not a Python assertion
failure; read the workflow's annotations before guessing its cause. CI uses synthetic data.

## From Windows PowerShell

Extract into a new source folder and open PowerShell there. Run separately:

```powershell
py -3.12 scripts\publish_github.py --check-only
py -3.12 scripts\publish_github.py --owner BachYun --public
```

Use the displayed typed confirmation. Virtual-environment activation is not required.
Do not put your Instagram password or authentication code in any publishing command.

## If publishing is interrupted

A failed push can still leave a local commit or a created remote. A settings failure after
`SOURCE UPLOADED` means the code may already be uploaded even if the script exits nonzero.
**Do not delete `.git`, create duplicates, force-push or blindly rerun the initial publisher.**

Inspect:

```text
git status
git remote -v
gh repo view BachYun/instagram-close-friends-windows
```

If `origin` is that exact intended new repo and the local main commit is the clean package,
finish a missing push with `git push -u origin main`. If the remote has commits you did not
expect, stop and review them rather than overwriting. If only Issues setup failed, enable
it explicitly after confirming this is the new Windows repository:

```text
gh repo edit BachYun/instagram-close-friends-windows --enable-issues --default-branch main
gh api repos/BachYun/instagram-close-friends-windows --jq .has_issues
```

The last command should print `true`. Check **Issues -> New issue** for the forms. See
[ISSUES.md](ISSUES.md) if templates are not visible. An existing remote name is never
silently treated as permission to overwrite it.

## Optional prerelease after review

Only after the exact uploaded build has the desired test evidence, create its beta tag
and release using the reviewed notes:

```text
gh release create v0.1.0-beta.2 --repo BachYun/instagram-close-friends-windows --prerelease --title "Windows Only v0.1.0-beta.2" --notes-file docs/RELEASE_NOTES.md
```

This is not run automatically. Keep native Windows and live Instagram validation claims
accurate. Do not change a failing workflow into a fake passing badge or hide skipped tests.

## Official references

- [Create/push a repository](https://cli.github.com/manual/gh_repo_create)
- [Enable Issues and edit repository settings](https://cli.github.com/manual/gh_repo_edit)
- [GitHub issue forms](https://docs.github.com/en/communities/using-templates-to-encourage-useful-issues-and-pull-requests/syntax-for-issue-forms)
- [GitHub commit email privacy](https://docs.github.com/en/account-and-profile/how-tos/email-preferences/setting-your-commit-email-address)
