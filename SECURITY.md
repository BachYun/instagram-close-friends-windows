# Security

Do not put passwords, Authy/2FA codes or seeds, cookies, tokens, Chrome profiles, Instagram
export archives, actual follower CSVs, progress histories or raw response bodies in this
repository, an issue, CI, or release asset. Default storage is a private local Windows
user folder outside the source checkout. File ACLs must be reviewed separately; Unix
file modes do not provide Windows ACL isolation.

CDP controls the browser. Keep the dedicated profile private, bind only to loopback,
never forward the port and close that Chrome instance when finished. The helper does not
read/export login secrets. Complete any Instagram verification yourself in the official
interface; stop on restrictions, CAPTCHA loops or page errors.

Locks coordinate local cooperating helper processes only. They do not stop other browser
extensions, old script versions, malware or another computer using the same account.
Avoid shared/network/cloud-sync workspaces and simultaneous runs on different computers.

The publication checker uses an allowlist and limited secret patterns, not a complete
audit. It does not inspect arbitrary history or revoke credentials. If sensitive material
was exposed, revoke the affected credential/session through its provider and arrange
appropriate repository cleanup. Do not repost the secret in a public report.

For a vulnerability, use GitHub private vulnerability reporting when enabled. If it is
not enabled, ask the maintainer for a private channel without including exploit secrets
or account data. Only share minimal sanitized reproduction details.
