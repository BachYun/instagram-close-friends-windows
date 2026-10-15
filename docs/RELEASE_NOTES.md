# Windows Only — v0.1.0-beta.2

Source package for `BachYun/instagram-close-friends-windows`. Includes native Windows
locks, Chrome launcher, PowerShell setup, CSV history and separate manual-refresh audits.
No automatic reloads, theme changes, credential capture, private-API login or restriction retries.

This publication update adds Windows-specific naming, full documentation, bug/setup/feature
issue forms and an owner-run publisher that enables the Issues tab. It fixes a prior
argparse `--help` percent-formatting error. See CHANGELOG.md and docs/BUILD_VALIDATION.md.

**Validation:** build-host tests are not native Windows or live Instagram tests. Run the
included Windows CI and manual smoke test before changing this experimental designation.
Windows ARM/VM compatibility is not established. Do not advertise guaranteed bulk additions.

The package contains source and synthetic examples only. Real CSVs, profiles, session data,
passwords and exports stay local. No hosted repository or release is implied by this file.
