# Contributing

This is a Windows-focused derivative. Keep attribution and GPLv3 notices intact. Work
on a feature branch after publication; do not modify the original Mac repository when
contributing to this Windows edition.

Use Python 3.12/3.13 and run the Windows commands in `docs/TESTING.md`. Tests must use
synthetic data and local browser fixtures; do not add Instagram credentials, real
followers, profiles, raw API payloads or automation against third-party accounts to CI.

Maintain the safeguards: explicit account confirmation, intent-before-click logging,
no automatic reload/theme override, separate manual-refresh verification, nonblocking
workspace/endpoint locks, bounded actions and no retry around restrictions.

New public source files must be added explicitly to `PUBLIC_FILES.txt`. Run
`scripts/check_publish.py` and inspect the staged diff before pushing. The manifest is
not a comprehensive security scan. Report actual validation scope; mocked Windows APIs
are not native Windows test results.

## Windows issue forms

Use [the Issues guide](docs/ISSUES.md) for bugs, setup help and feature requests. Keep
forms and known limitations consistent with the actual release. Add a regression test
for code fixes; never require live Instagram credentials in CI. `PUBLIC_FILES.txt` must
include new source/docs/tests, but must never contain personal runtime data.
