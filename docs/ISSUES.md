# Issues and support — Windows only

The issue tracker for this project is [https://github.com/BachYun/instagram-close-friends-windows/issues](https://github.com/BachYun/instagram-close-friends-windows/issues).
It becomes available when the owner publishes this repository with Issues enabled.
The publisher sets and verifies that setting; it does not create support tickets itself.

## Choose a form

**Windows bug report** is for behavior that differs from the documented code behavior.
**Windows setup help** is for Python, PowerShell, installation, Chrome or CSV questions.
**Windows feature request** is for an improvement within the existing privacy and
verification safeguards. All three forms live in `.github/ISSUE_TEMPLATE/` on `main`.

Read [KNOWN_ISSUES.md](KNOWN_ISSUES.md) and [TROUBLESHOOTING.md](TROUBLESHOOTING.md) first.
Search existing open and closed issues for the exact short error message. If you find an
existing report, add non-sensitive new evidence there instead of creating a duplicate.

## Useful diagnostic details

Include the helper's `--version`, Python's `--version`, the Windows build from `winver`,
CPU/OS architecture (x64 or ARM64), Chrome's version, and whether Windows is virtualized.
State the exact stage: installation, status/import, Chrome launch, CDP attachment, search,
click, manual-refresh audit, or GitHub publication. Give minimal steps and expected/actual
results. Replace account names and private folder components with placeholders.

A useful error excerpt is the printed phase/category and a few surrounding lines, not a
whole terminal history. Do not rerun actions against a restricted account to obtain extra
evidence. Saying that no native Windows test has been run is valid and useful.

## Never post these

Do not attach actual followers/history/reports, whole Instagram exports, Chrome profile
folders, passwords, 2FA codes, Authy seeds or QR codes, cookies, session IDs, authorization
headers, raw HTTP responses, HAR files, debug-port tunnels, private keys, or API tokens.
Review screenshots for avatars, account details, browser tabs, addresses and notifications.
If sensitive information was posted, remove it and follow the affected provider's credential
revocation process; deleting a post alone may not invalidate a leaked credential.

For security concerns use [SECURITY.md](../SECURITY.md). If GitHub offers a private
**Report a vulnerability** action, use it. Otherwise request a private channel without
posting the sensitive proof publicly. No email address is invented in this package.

## How maintainers can triage

Confirm release and environment, then try to reproduce with synthetic/local data first.
Classify the problem as installation, UI-layout change, tracking semantics, platform lock,
CSV/import, or repository/CI. The default GitHub `bug`, `question`, and `enhancement`
labels are used by the forms. A failing hosted runner before any test steps is not the
same as a failing test assertion. Preserve exact failure evidence before changing code.

Native Windows validation is an open **validation gap**, not an established code failure.
A platform rate limit or CAPTCHA is not a request to bypass security controls. There is
no promised response time, no paid support service, and no guarantee of completion for
unavailable or renamed followers.

## If the Issues tab or forms are missing

The owner can run:

```text
gh repo edit BachYun/instagram-close-friends-windows --enable-issues
```

Confirm the templates were pushed to `main` and `main` is the default branch. YAML forms
and their config belong in `.github/ISSUE_TEMPLATE`, not under `docs` alone. In a private
repository, only authorized collaborators can view or report issues. Templates become
visible through **Issues -> New issue**. [GitHub template documentation](https://docs.github.com/en/communities/using-templates-to-encourage-useful-issues-and-pull-requests/configuring-issue-templates-for-your-repository).
