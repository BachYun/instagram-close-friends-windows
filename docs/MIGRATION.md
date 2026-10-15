# Move the workflow to Windows without losing progress

The Windows repository is separate from the original Mac/Linux repository. It retains
the three-column history format: `timestamp,username,result`.

1. Stop the Mac helper and any extension working on the same account.
2. Preserve a private backup of `followers.csv` and `close_friends_progress.csv`.
3. Install this Windows edition in a new source folder and create its Python environment.
4. Create `%LOCALAPPDATA%\InstagramCloseFriendsWindows` (or a separate local data folder
   for each account). Copy those two CSV files there. Copy `.close_friends_account.json`
   too when present and it belongs to the same account. Do not merge mismatched histories.
5. Run `--status` before connecting to Chrome. This reads/derives reports without changing
   input follower/history files or accessing Instagram.
6. Launch a new dedicated Windows Chrome profile and authenticate manually with your
   ordinary credentials and two-factor app. Never migrate cookies, passwords or a Chrome
   profile from the Mac through this repository.
7. Use `--verify-pending` to audit uncertain clicks before attempting new additions.

For a custom data folder:

```powershell
$Data = 'C:\Users\YOUR_USER\Private Data\Close Friends'
.\.venv\Scripts\python.exe close_friends_csv.py --data-dir $Data --account YOUR_USERNAME --status
```

Replace examples with actual paths/account names. Existing `--no-dark` remains accepted
for compatibility, but no version of this Windows edition changes the theme. The old
bulk command `--limit 685` is intentionally not accepted: scans cap at 100 positions and
audits at 20. `--max-adds` caps click attempts, not verified saved additions.

Use the exact **latest private log** when migrating. Reports are derived snapshots, not
substitutes for history. Do not copy them back over newer logs on the Mac. The file locks
coordinate processes on one machine only; they do not coordinate two computers or older
scripts that ignore locks. Do not share the live workspace via OneDrive/Dropbox/SMB.

Names and follower counts can change. Import a complete new follower export to identify
additional usernames; a profile's numeric follower count alone cannot update a CSV.
The import leaves history intact and creates an old-snapshot backup after confirmation.
