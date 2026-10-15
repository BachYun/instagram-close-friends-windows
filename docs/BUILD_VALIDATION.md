# Build validation — Windows Only 0.1.0b2

Date: 2026-10-15. This is a source-package validation record, not a GitHub Actions result.

## Source and changes

Based on the previously supplied Windows port archive, which was derived from
`BachYun/instagram-close-friends-playwright` commit
`69d249754bf4c932d2163f6b62ce12b046ad2f4b`.
The current package renames the Windows repository, adds issue forms/reporting docs,
adds explicit Issues enablement/read-back to the owner-run publisher, and fixes the
argparse literal-percent help error. The original GPL license file is unchanged.

## Executed for this package

Host: Linux x86_64; Python 3.13.5; pytest 9.0.2; Playwright 1.57.0; PyYAML 6.0.3.
The DOM fixture used locally installed `/usr/bin/chromium` with network requests
fulfilled/aborted locally. No Instagram login or network request was made by those tests.

- Full suite: **137 passed, 1 skipped**.
- The one skip requires PowerShell; PowerShell is not installed on this Linux host.
- The known `--help` failure is fixed and covered by a subprocess regression test.
- Both synthetic DOM tests passed, including alternate account-row wrappers.
- Source manifest/publication checks passed: **49 intended public files**.
- Python source compilation passed.
- All issue forms parsed and their required structure/dropdown string types were checked.
- Local Markdown file links were checked for existence.
- The publisher success path uses real local Git but stubs EVERY GitHub CLI request.
- Publisher tests verified explicit Issues enablement and refusal to claim success when
  the returned repository name, Issues flag or default branch is wrong.
- No actual remote repository, Issues setting, ticket, tag or release was created by tests.

## Not established

Native Windows process locking, PowerShell execution, installed Windows Chrome launch,
Windows ARM64/VM compatibility, and live Instagram behavior remain unverified by this build.
Mocked Windows API tests and Linux process-lock tests do not prove native Windows success.
The included native Windows GitHub Actions workflow still needs a successful observed run.
Source publication also does not establish that GitHub will start a hosted runner.

No actual followers, progress files, credentials, browser profiles, ZIP account exports,
virtual environments or previous Git history are included in the publication archive.
The manifest/credential-pattern checker is limited defense in depth, not a full audit.
