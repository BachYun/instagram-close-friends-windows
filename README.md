# Instagram Close Friends — Windows Only

**Repository: `BachYun/instagram-close-friends-windows`**

[Setup](#quick-start-on-windows) · [Commands](docs/COMMANDS.md) · [Reports](#reports) ·
[Issues](#issues) · [Known issues](docs/KNOWN_ISSUES.md) · [Security](SECURITY.md)

**A Windows-only distribution of the local Playwright Close Friends helper.**
Compare your follower CSV with the visible Instagram Close Friends interface, approve
limited additions, and separately verify the results after a manual refresh.

**Version:** `0.1.0b2` / `v0.1.0-beta.2` · **Target:** Windows 11+ · **Python:** 3.12 / 3.13

**Release status: experimental. Native Windows validation is pending.** Windows x64 is
this edition's test target. Windows on ARM (including a Mac virtual machine) is not
validated by this build; report architecture and virtualization details in Issues.
macOS/Linux are not the end-user runtime support scope of this repository. The small
POSIX fallback exists for development and publishing; the Mac project stays separate.

> Windows-specific code and CI configuration are included. The package was tested on a Linux
> build host; native Windows CI and a Windows/Instagram manual test must still be run.
> Do not interpret a successful source upload, synthetic test, or checkmark as proof of
> live compatibility. This is not affiliated with Instagram or Meta.

This is a separate source project, derived from
[`BachYun/instagram-close-friends-playwright`](https://github.com/BachYun/instagram-close-friends-playwright)
at commit `69d249754bf4c932d2163f6b62ce12b046ad2f4b`. It does not modify that repository.

## What is different in this Windows edition?

- Native nonblocking `msvcrt` file locks replace the Windows-incompatible `fcntl` path.
  Locks coordinate the account data folder and Chrome debugging port.
- Windows data defaults to `%LOCALAPPDATA%\InstagramCloseFriendsWindows`.
- PowerShell setup and Chrome launcher, with an equivalent direct Python launcher.
- Detects ordinary system/user Chrome installations and preserves spaces in file paths.
- Refuses the ordinary Chrome profile; uses a dedicated profile and localhost debugging.
- Windows CI includes real process-lock tests, PowerShell syntax checks and a local DOM fixture.
- Source-only GitHub publisher works on the owner's Mac or Windows PC and uses a
  GitHub `noreply` commit identity. No personal email is copied from the original history.

The same safeguards remain: **no automatic reloads, no theme changes, no password/2FA
handling, no direct Instagram API client, no CAPTCHA bypass, no deletion mode, no
unattended retry loop.** Manual login and any legitimate verification stay in Chrome.

## Requirements

Use Windows 11 or newer with Python 3.12 or 3.13 and Google Chrome installed. Git is
needed for cloning/development; GitHub CLI is only needed by the repository publisher.
Windows 10 is not a claimed support target; consult current Playwright requirements.
The POSIX fallback permits offline development/publication on a Mac or Linux machine,
but the supplied Chrome launcher is Windows-only.

Official references:
[Python downloads](https://www.python.org/downloads/windows/),
[Playwright requirements](https://playwright.dev/python/docs/intro),
[Chrome debugging profiles](https://developer.chrome.com/blog/remote-debugging-port).

## Quick start on Windows

### 1. Get the source and install dependencies

Extract this project's ZIP into a folder outside your private account-data folder. After
publication, Git users can instead clone it:

```powershell
git clone https://github.com/BachYun/instagram-close-friends-windows.git
Set-Location instagram-close-friends-windows
```

Open **PowerShell** in the source folder. Use the commands below one at a time; stop on
any nonzero result. This is a Python source project, not a standalone `.exe` or a Chrome
extension. Windows does not have to be installed on the computer used only to publish it.

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe close_friends_csv.py --version
```

Use `py -3.13` instead when that is the installed version. Stop if any command fails.
There is no need to activate the virtual environment or change execution policy.
No administrator rights are needed. Do not copy a Mac `.venv` to Windows.

An optional setup script does the same with explicit exit-code checks:

```powershell
.\scripts\setup_windows.ps1
```

If downloaded PowerShell scripts are blocked, review them first and unblock those
specific files using `Unblock-File`; do not disable a corporate policy or use a global
execution-policy bypass. The direct Python commands above also work without PS scripts.
See [troubleshooting](docs/TROUBLESHOOTING.md).

### 2. Keep your account files outside the repository

```powershell
$Data = Join-Path $env:LOCALAPPDATA 'InstagramCloseFriendsWindows'
New-Item -ItemType Directory -Force -Path $Data | Out-Null
```

Copy **your real** `followers.csv` into that data folder with File Explorer. The first
column is usernames; a `username` header is optional. The included example CSV is fake
and must never be used for live account additions.

To resume existing work, also copy the latest `close_friends_progress.csv` and, when
present, `.close_friends_account.json` from your old workspace. Preserve the originals.
Do **not** copy browser profiles, cookies, `.env`, virtual environments, or raw logs into
this source repository. Stop the old helper before migrating; never run both machines
against the account at the same time. See [migration](docs/MIGRATION.md).

Windows file permissions inherit from your local user folder; Unix `chmod`/`umask` are
not a substitute for a Windows ACL. Avoid shared, network-mounted or cloud-synced folders.

### 3. Launch Chrome with a separate profile

```powershell
.\.venv\Scripts\python.exe scripts\launch_chrome_windows.py
```

Or use the PowerShell wrapper:

```powershell
.\scripts\launch_chrome_windows.ps1
```

The default browser profile is `%LOCALAPPDATA%\InstagramCloseFriendsWindows\chrome-profile`.
This is **not** your ordinary Chrome profile; its existing Instagram login is not copied.
Log in normally on the genuine Instagram website and complete any legitimate two-factor
verification. Keep exactly **one** Close Friends tab open in the launched Chrome.
Stop if Instagram displays a challenge loop, restriction or error.

If port 9222 is already in use, the launcher stops. Keep an existing dedicated Chrome
window when it is already the intended one; do not start duplicate browsers or kill
unrelated processes. Do not tunnel/expose the debugging port. Close this dedicated
Chrome when finished: localhost debugging grants browser control, not just read access.

Custom executable/profile and inspection-only launch:

```powershell
.\.venv\Scripts\python.exe scripts\launch_chrome_windows.py --chrome 'C:\Program Files\Google\Chrome\Application\chrome.exe' --profile 'C:\Users\YOUR_USER\Private Data\CF Chrome' --dry-run
```

Replace the example path with a real private path. `--dry-run` does not create a profile
or launch a process. This launcher never changes Instagram settings.

### 4. Check saved progress offline

```powershell
.\.venv\Scripts\python.exe close_friends_csv.py --data-dir $Data --status
```

No browser connection is made. Counts describe the imported follower snapshot and local
observations, **not** a live whole-account count.

### 5. Preview one or a few usernames

Replace `YOUR_USERNAME` with the Instagram account you are logged into, without `@`:

```powershell
.\.venv\Scripts\python.exe close_friends_csv.py --data-dir $Data --account YOUR_USERNAME --start 1 --limit 3
```

The account declaration binds this private workspace to that username. It does not
independently detect who is logged in; visually confirm the account before each run.
Preview reads the visible interface and generates website search requests, but never
clicks a selection circle. Do not switch accounts or interact with the tab mid-run.

### 6. Approve one test addition

```powershell
.\.venv\Scripts\python.exe close_friends_csv.py --data-dir $Data --account YOUR_USERNAME --apply --start 1 --limit 20 --max-adds 1
```

Type `ADD 1 TO YOUR_USERNAME`, substituting the actual account name. The helper skips
historically selected accounts and uncertain prior clicks. It attempts at most one click
and logs intent before clicking. The new checkmark is **pending verification**, not saved
membership proof. Unknown states and detected errors stop the run without a second click.

### 7. Verify pending selections after a manual refresh

```powershell
.\.venv\Scripts\python.exe close_friends_csv.py --data-dir $Data --account YOUR_USERNAME --verify-pending --limit 20
```

When prompted, press **Ctrl+R once in the connected Chrome tab**, wait for a healthy
Close Friends page and type `REFRESHED YOUR_USERNAME`. Do not toggle circles during this
check. The helper verifies that the document changed and reads selection states without
clicking. A successful check is a timestamped UI observation, not a permanent guarantee.

To audit one specific name already in your follower CSV:

```powershell
.\.venv\Scripts\python.exe close_friends_csv.py --data-dir $Data --account YOUR_USERNAME --verify-live --username EXACT_FOLLOWER_USERNAME
```

## Further additions and new followers

After reviewing the prior batch and checking normal manual use:

```powershell
.\.venv\Scripts\python.exe close_friends_csv.py --data-dir $Data --account YOUR_USERNAME --apply --start 21 --limit 20 --max-adds 3
```

Use the report's position column to choose a range. `--limit` is source positions scanned,
including skips, not number of additions. The helper caps a scan at 100 names, an audit
at 20, and click attempts at 10. Default pacing is 30 seconds between searches. None of
these are Instagram-approved or guaranteed safe limits. There is no automatic batch loop.

To update the follower snapshot, import a **complete all-time export for the same account**:

```powershell
.\.venv\Scripts\python.exe close_friends_csv.py --data-dir $Data --import-export 'C:\Users\YOUR_USER\Downloads\YOUR_REAL_EXPORT.zip' --status
```

Use the actual ZIP path. Review counts and confirm `IMPORT N` as shown. The old CSV is
backed up and progress preserved. An archive's account owner is not detected for you.
Absent usernames may mean rename/export differences, not necessarily an unfollow. The
helper never removes anyone from Close Friends. Positions can change after import.

## Command reference and resuming

Every flag, its default, confirmation phrase and side effect is documented in
[COMMANDS.md](docs/COMMANDS.md). Read [STATUSES.md](docs/STATUSES.md) before interpreting
counts or resuming a run. Run `--verify-pending` before a further addition batch when
uncertain clicks exist. Never reset the history simply to force another click.

The source CSV, not Instagram's profile counter, determines which accounts are scanned.
A report of 685 names still means 685 even if the live profile now has more followers.
Import a new complete snapshot to include new usernames. A normal exit is not a claim
that every follower has been added.

## Reports

| File in the private data folder | Meaning |
|---|---|
| `close_friends_progress.csv` | Append-only history; preserve this |
| `close_friends_status.csv` | Every snapshot username, position and latest meaningful status |
| `close_friends_selected.csv` | Historically recorded selections and evidence time |
| `close_friends_pending.csv` | Still unconfirmed, including unresolved states |
| `close_friends_awaiting_verification.csv` | Uncertain clicks that need an audit |
| `close_friends_errors.csv` | Sanitized error category and phase |
| `close_friends_new_since_export.csv` | Names not in the earlier snapshot |
| `close_friends_no_longer_following.csv` | Legacy name: absent from the new export, not proof of unfollowing |

```powershell
Invoke-Item (Join-Path $Data 'close_friends_status.csv')
```

Definitions: [statuses](docs/STATUSES.md). An exit code of zero does not mean all followers
were added. Do not immediately restart after restrictions or failed verification.

## Testing and publication

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements-dev.txt
.\.venv\Scripts\python.exe -m pytest -q -m 'not browser'
.\.venv\Scripts\python.exe scripts\check_publish.py
```

The GitHub Actions workflow targets native Windows, with an additional Linux regression
job. Tests use synthetic files and a locally intercepted DOM fixture, never Instagram
credentials. See [test scope](docs/TESTING.md), [executed build checks](docs/BUILD_VALIDATION.md), [security](SECURITY.md) and
[publishing from Mac or Windows](docs/PUBLISHING.md). Preserve the beta label until the
exact release passes native Windows tests and a manual Instagram test.

The first-publication helper creates **a new repository only**, using your authenticated
GitHub CLI. It refuses existing local Git histories or a remote repo of that name, defaults
to private, sets an ID-based GitHub `noreply` identity and stages only the reviewed manifest.
It never rewrites or force-pushes the Mac/Linux repository. The checker is limited, not a
complete security audit or history scrubber.

## Issues

Use the **[GitHub Issues tab](https://github.com/BachYun/instagram-close-friends-windows/issues)** for this Windows repository.
The publisher explicitly enables it; the source folder also contains the issue forms.
Links become available after this repository is created under the displayed owner/name.

| What you need | Where to start |
|---|---|
| Reproducible bug | [Windows bug report](https://github.com/BachYun/instagram-close-friends-windows/issues/new?template=bug_report.yml) |
| Installation, PowerShell, or Chrome help | [Windows setup help](https://github.com/BachYun/instagram-close-friends-windows/issues/new?template=setup_help.yml) |
| Improvement to the Windows tool | [Feature request](https://github.com/BachYun/instagram-close-friends-windows/issues/new?template=feature_request.yml) |
| A known limitation or validation gap | [Known issues and limits](docs/KNOWN_ISSUES.md) |
| Private/security-sensitive concern | Read [SECURITY.md](SECURITY.md); do not post secrets in an issue |

Before reporting, search existing issues and read [Windows troubleshooting](docs/TROUBLESHOOTING.md).
Include the helper version, Windows version/build, x64/ARM64 architecture, Python and
Chrome versions, whether you use a VM, the failing command with private values replaced,
expected/actual behavior, and a short **reviewed and redacted** error excerpt. The forms
ask for these details and include a privacy checklist.

**Never attach** real follower/progress CSVs, full Instagram exports, browser profiles,
passwords, Authy codes or seeds, cookies, session IDs, full network traces, or tokens.
A publisher/test success is not evidence of a healthy live Instagram account. Do not
make repeated account requests solely to fill out a bug report. [Full reporting guide](docs/ISSUES.md).

No live issues are automatically opened by the publisher, and no fixes are promised for
Instagram enforcement or challenge handling. Do not request CAPTCHA bypass, proxy rotation,
rate-limit evasion, or removal of the existing confirmation and verification safeguards.

## License and provenance

GPL-3.0-only. Original notices and license are preserved in [NOTICE.md](NOTICE.md) and
[LICENSE](LICENSE). Dependency licenses remain separate. No brand assets are included.
The Windows work is a port, not a claim of exclusive authorship of inherited material.
