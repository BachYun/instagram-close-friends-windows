# Windows troubleshooting

## `py` is not recognized

Install Python 3.12 or 3.13 for Windows and reopen PowerShell. Confirm `py -3.12 --version`
(or `py -3.13 --version`). Commands are PowerShell syntax, not Command Prompt or Bash.

## A command failed but the next command ran

Windows PowerShell 5.1 does not support Bash `&&`. The README lists separate commands;
stop on the first failure. The optional `scripts\setup_windows.ps1` checks native exit
codes explicitly. Run Python directly using `.\.venv\Scripts\python.exe`; activation is
not necessary. Do not copy a Mac/Linux virtual environment.

## PowerShell script is blocked

Read the downloaded script first. To remove the download mark from only the reviewed
files, use `Unblock-File .\scripts\setup_windows.ps1` and/or
`Unblock-File .\scripts\launch_chrome_windows.ps1`. Do not bypass organization policy or
set global execution policy to Unrestricted. The direct Python commands in the README
avoid needing a PowerShell script at all. No administrator rights are required.

## Chrome was not found or a path contains spaces

The launcher checks Chrome in Program Files, Program Files (x86), and Local AppData.
Use `--chrome 'C:\full path\chrome.exe'` for a custom installation. Arguments are passed
as a list, not a shell command string. Use `--dry-run` to inspect before launching.

## Port 9222 is already used

The launcher will not reuse a random process, start a second debugging Chrome, or kill
anything. Keep the already-running dedicated helper Chrome if that is the intended
session; otherwise inspect manually. A custom port must match `--cdp-url` in the helper.
Never expose/tunnel a browser debug endpoint off the machine.

## Cannot write/replace a CSV

Close Excel or another program that has the report/snapshot file open, then rerun the
OFFLINE status check. Windows may deny atomic replacement of a file held by another
program. Do not interpret a file permission error as lost Instagram progress or retry a
live click. Use a local private directory, not a shared/network/cloud-sync workspace.

## Another run holds a lock

Stop the other helper normally. Locks release when its process exits. Do not delete lock
files while a process may still be running; files remain on disk intentionally to keep
all processes coordinating on the same object. Old scripts and other computers do not
share this protection.

## `Something went wrong`, CAPTCHA, or `rate_limited`

Stop the helper and inspect Instagram manually. The Windows version does not reload,
rotate identities, solve CAPTCHAs, clear sessions, or retry restrictions. No fixed delay
is a guaranteed cooldown. An on-screen click may have succeeded even if a later read
failed, which is why uncertain state stays queued until manual-refresh verification.

## Pending, unconfirmed, or apparently incomplete results

`--status` is offline historical reporting. `--verify-pending` audits only its pending/
uncertain queue, after you refresh manually and confirm the account. `--verify-live`
checks a chosen range or `--username`; it is not a whole-account API audit. A normal exit
is not proof the full follower snapshot was completed. See STATUSES.md.

## New followers do not appear

The tool does not scrape a new follower list automatically. Import a complete updated
official follower export for the SAME account, or provide your own complete CSV. Do not
replace an existing log with an old report; retain the append-only history.

## GitHub upload fails or Actions never start

Publication is a separate workflow from Instagram automation. See PUBLISHING.md for
authentication, staged-file checks and interrupted first-upload recovery. Read workflow
annotations before changing tested Python code in response to a runner startup error.
