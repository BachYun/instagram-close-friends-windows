# Known issues, limits and validation gaps

This page distinguishes observed development failures from design limits and work not
yet validated. It is not a claim that these are all bugs in the current Windows build.

| Topic | Classification | What is established | Appropriate action |
|---|---|---|---|
| Native Windows execution | Validation pending | Current package has not been executed on a native Windows build host | Run the included Windows CI and manual smoke test; record results |
| Windows on ARM / virtual machines | Not validated | Local Linux tests and x64 CI configuration do not establish ARM/VM compatibility | Identify architecture and VM in issue reports; do not label it supported without evidence |
| Help command in earlier Windows package | Fixed in `0.1.0b2` | An unescaped `%LOCALAPPDATA%` help string triggered argparse formatting failure | This release escapes the literal percent signs and tests `--help` |
| Instagram loading/error page | Observed in earlier development | Automatic post-click reloads previously encountered `Something went wrong` | This edition never auto-reloads; stop on error, review uncertain state manually |
| Rate limits, CAPTCHA, login approvals | External restrictions | The helper cannot establish a universally safe action rate or solve platform restrictions | Stop, complete legitimate manual verification, no automated retries or identity rotation |
| English Bloks UI only | Layout limitation | Selectors and icons are based on the observed English Close Friends layout | Changed/unknown layouts stop; report minimal sanitized UI details |
| On-screen selection versus saved selection | Deliberate semantics | A changed icon is not independent proof of saved membership | Verify pending selections after the prompted manual full refresh |
| Follower totals and renames | Snapshot limitation | CSVs are not automatically synchronized to live follower counts | Import a complete current export; review renamed/reassigned/unavailable accounts |
| Open CSV in Excel | Windows file behavior | An open report can prevent atomic replacement | Close the report and retry the offline task; do not repeat a live click |
| Old scripts, two computers | Coordination limitation | Current locks coordinate participating local processes, not every tool/device | Stop other bots/computers; one account run at a time |
| Account identity | Explicit user declaration | Local binding does not prove which account is open in Chrome | Confirm the account visually before every run; never switch it mid-run |
| Source upload versus Actions result | Separate outcomes | A pushed repository does not prove hosted jobs started or passed | Inspect Actions annotations and steps; do not mark CI green without a successful run |
| Public Issues privacy | User reporting risk | Templates cannot automatically sanitize posted logs or attachments | Follow the privacy checklist before posting |

Use the [reporting guide](ISSUES.md) for a new Windows report. A fresh native Windows
failure should be accompanied by its exact build and short redacted error, not replaced
with a guessed cause. No known Instagram-side error is an instruction to bypass controls.
