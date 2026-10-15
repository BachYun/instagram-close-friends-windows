# Operational limits

This is an unofficial local interface helper, not an Instagram API, service or CAPTCHA
solution. There is no guaranteed action rate, compatibility promise or protection from
account restrictions. Do not bypass authentication, solve challenges programmatically,
rotate proxies/devices, or schedule repeated retries of blocked actions.

## Account and state

Manually verify the signed-in account before each run. `--account` binds a local data
folder to a user-declared name; it is not automatic identity detection. Keep one Close
Friends tab open in the dedicated Chrome instance. Do not change accounts or manually
toggle selections while a run is executing. Username snapshots may be stale or reassigned.

An on-screen checkmark is not proof of persistence. Intent is saved before each click;
uncertain actions are held for read-only verification after a manual full refresh. A
freshly observed selected state is still only an observation at that time, not a
permanent membership guarantee. Do not delete history to make an uncertain click retry.

## Windows storage and browser

Use separate local data folders for separate accounts, outside the Git checkout. The
default is under Local AppData. Files inherit Windows ACLs; chmod/umask does not guarantee
privacy on Windows. Avoid shared/network/OneDrive/Dropbox folders for active histories.

The launcher refuses the ordinary Chrome data root and uses a dedicated profile. No
passwords or session cookies are transferred from an existing browser. Loopback CDP
still gives local software control of the browser; do not expose or tunnel it. Close
the dedicated Chrome when finished and keep other Instagram automation disabled.

The file locks guard cooperating local helper processes only, not other machines, old
scripts, extensions or a malicious local user. Lock files deliberately remain after exit.
Never delete them while another process may be using them.

## Error handling and limits

Unknown checkbox/layout, page errors, authentication redirects and detected HTTP errors
stop rather than trigger another click or automatic reload. The helper caps source scans
at 100, audits at 20 and clicks at 10, with default search pacing of 30 seconds. These are
software limits, not Instagram-approved safe amounts. Manual refresh is explicitly
requested only for verification; cancel it if the page fails to load.

Publication and synthetic tests make no account changes. Do not add Instagram secrets
or real account data to automated CI. The exact Windows/Instagram combination requires
manual validation before claiming support beyond the implemented code path.
