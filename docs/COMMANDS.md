# Windows command reference

Run in PowerShell from the source folder. Examples call the virtual environment's Python
explicitly; activation is not required. Replace UPPERCASE placeholders. Commands that
contact the website may still be rejected by Instagram; none is restriction-free.

Set these variables for one PowerShell session:

```powershell
$Python = '.\.venv\Scripts\python.exe'
$Data = Join-Path $env:LOCALAPPDATA 'InstagramCloseFriendsWindows'
$Account = 'YOUR_USERNAME'
```

`$Account` is a username, never a password. Use a different private data folder and Chrome
profile for each account. After opening a new PowerShell window, set the variables again.

## Commands and side effects

| Task | Example | Side effects |
|---|---|---|
| Version | `& $Python close_friends_csv.py --version` | Prints version only |
| Help | `& $Python close_friends_csv.py --help` | Prints options only |
| Offline status | `& $Python close_friends_csv.py --data-dir $Data --status` | Reads snapshot/history and writes derived CSV reports; no browser connection |
| Import full export | `& $Python close_friends_csv.py --data-dir $Data --import-export 'C:\Exports\YOUR_EXPORT.zip' --status` | Prompts, backs up and replaces follower snapshot; no Instagram requests |
| Preview | `& $Python close_friends_csv.py --data-dir $Data --account $Account --start 1 --limit 3` | Searches the website, writes preview log entries; no membership clicks |
| One addition | `& $Python close_friends_csv.py --data-dir $Data --account $Account --apply --start 1 --limit 20 --max-adds 1` | Requests approval; attempts at most one eligible click; logs pending evidence |
| Pending audit | `& $Python close_friends_csv.py --data-dir $Data --account $Account --verify-pending --limit 20` | Requires manual refresh and confirmation; reads website and appends observations, no clicks |
| One-name audit | `& $Python close_friends_csv.py --data-dir $Data --account $Account --verify-live --username EXACT_FOLLOWER_USERNAME` | Same audit, for an exact name already in the CSV |

The `C:\Exports` example must be replaced by the real ZIP path.

## Every helper flag

| Option | Default / accepted values | Meaning |
|---|---|---|
| `--version` | No value | Print this release's version and exit |
| `--help` | No value | Show CLI usage and exit |
| `--data-dir PATH` | Windows Local AppData directory, or `CLOSE_FRIENDS_DATA_DIR` | Private data workspace |
| `--account NAME` | Existing local binding, otherwise required for first browser run | Your declaration of the connected account; not automatic login identification |
| `--cdp-url URL` | `http://127.0.0.1:9222` | Loopback Chrome debugging endpoint only |
| `--status` | Off | Offline derived reports; cannot be combined with browser modes |
| `--import-export ZIP` | Off | Import after counts/confirmation, then return without browser actions |
| `--verify-live` | Off | Read current state after an explicitly requested manual refresh |
| `--verify-pending` | Off | Audit uncertain/pending queue, not every unconfirmed follower |
| `--apply` | Off | Enable limited, confirmed-by-user addition attempts |
| `--username NAME` | Off | One exact CSV name; overrides positional selection; not valid with `--verify-pending` |
| `--start N` | 1; positive | CSV position, except pending mode uses its filtered queue position |
| `--limit N` | 5; 1–100 | Positions scanned, including skips; audits capped at 20 except a single-name audit |
| `--max-adds N` | 3; 1–10 | Maximum click attempts, not a number of successful saved additions |
| `--delay-seconds N` | 30; finite 10–3600 | Minimum time between searches; a software guardrail, not an Instagram limit |
| `--no-dark` | Compatibility flag | Accepted but unnecessary: the helper never changes the theme |

`--apply`, `--verify-live` and `--verify-pending` are mutually exclusive.
Never put passwords, Authy seeds/codes, cookies, or access tokens in command arguments.

## Confirmation phrases

An addition asks for `ADD N TO your_username`, with the actual displayed N/account.
An audit asks for `REFRESHED your_username` after the script has started waiting and you
have refreshed the connected tab once with **Ctrl+R**. A refresh before the prompt does
not satisfy the new-document check. An import asks for `IMPORT N` using the parsed count.
Anything else cancels. Run the saved `.py` file, not a Python heredoc or a piped script.

## Launcher flags

```powershell
& $Python scripts\launch_chrome_windows.py --help
```

`--chrome PATH` specifies an installed `chrome.exe`; `--profile PATH` specifies a private
dedicated profile; `--port N` chooses a port from 1024 to 65535; `--dry-run` prints the
argument list without creating a profile or launching Chrome. The default port is 9222.
A custom port must also appear in the helper's `--cdp-url`. Never expose or tunnel it.

## Normal endings, errors and reports

Exit 0 means the selected task ended normally, not that all followers were added. An
addition may end because its click budget was reached, all candidates were skipped, or
no candidates existed. Exit 2 indicates a browser/operation error or CLI validation error;
other errors may exit 1, and an outer Ctrl+C interruption may exit 130. Read the message,
not just the exit code. Preserve history; do not change results to force new clicks.

Open reports only when the helper is not writing them. Close Excel/Numbers equivalents
before regenerating reports; Windows can refuse replacement of files that are held open.

See [STATUSES.md](STATUSES.md) for all history states and the filtered queue semantics.
