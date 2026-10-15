# Test scope and honest compatibility status

## What this Windows edition adds

Native nonblocking `msvcrt.locking` on Windows, a POSIX fallback for development, Windows
private paths, safe launcher argument construction, Windows PowerShell wrappers, a
source-only GitHub publisher, and native-Windows CI jobs.

The build host used for this package is **Linux**, not Windows. See the delivered build
report for executed results. Tests with a mocked msvcrt module check the API contract and
code path, but are NOT a substitute for a real Windows filesystem/process test.
PowerShell parsing is skipped only when PowerShell is absent on the build host; it is
required in the Windows CI job. Two inherited symlink tests may skip on a Windows
machine without Developer Mode/symlink privilege; the skip is explicitly reported.

No automated test authenticates with Instagram, exports cookies, uses real followers or
adds anyone to a real Close Friends list. DOM tests serve synthetic content in memory and
intercept/abort all browser requests. Native Windows/live Instagram compatibility remains
unverified until the corresponding runs are actually observed to succeed.

## Windows local tests

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements-dev.txt
.\.venv\Scripts\python.exe -m pytest -q -m 'not browser'
.\.venv\Scripts\python.exe scripts\check_publish.py
```

For the isolated DOM tests:

```powershell
.\.venv\Scripts\python.exe -m playwright install chromium
$env:CF_RUN_BROWSER_TESTS = '1'
.\.venv\Scripts\python.exe -m pytest -q
```

The automated helper itself attaches to installed Chrome and does not require this
Chromium download. It is needed only by the synthetic DOM tests.

## Native Windows CI

`.github/workflows/windows-tests.yml` runs on `windows-latest` for Python 3.12 and 3.13,
and includes a Linux regression job. Windows jobs execute native byte-range locks,
cross-process exclusion and lock-release-on-exit tests, atomic CSV replacement and log
compatibility tests, PowerShell parsing and intercepted-browser fixtures. Permissions
are read-only, action versions pinned, and no Instagram secrets are required.

If jobs fail before steps/runner assignment, inspect Actions annotations; that is not a
passing or failing Python test result. The presence of a workflow file proves only that
coverage is configured, not that GitHub has run or passed it.

## Manual acceptance test for the exact Windows build

Use a normal, healthy account session. Run one preview, one explicitly approved addition,
and a separate manual-refresh verification. Confirm no second click/removal occurs for
an existing selection and that an interrupted click is still held for verification.
Confirm a blocked/error page stops the helper. Do not deliberately trigger rate limits
or repeatedly solve challenges for testing.

A healthy synthetic run cannot guarantee Instagram will accept automation. Keep the
beta status and document only actual observations, including OS, Python, Chrome version,
date and interface locale; never include credentials or session state in an issue.
