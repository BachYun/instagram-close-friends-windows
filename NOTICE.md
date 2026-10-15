# License and provenance notice

This publication is distributed under **GNU GPL version 3 only**, SPDX identifier
`GPL-3.0-only`. The complete license text is in `LICENSE`. The license's own Free Software
Foundation notice is retained unchanged. Project contributions remain with their
respective authors/rightsholders; no exclusive authorship claim is made here.

## Development history

The development workflow began by evaluating:

- Project: `tuliosousapro/Instagram-Close-Friends-BOT`
- Repository: https://github.com/tuliosousapro/Instagram-Close-Friends-BOT
- Reviewed branch: `feature/basic-configs`
- License reviewed: GNU General Public License version 3
- License source: https://github.com/tuliosousapro/Instagram-Close-Friends-BOT/blob/feature/basic-configs/LICENSE

The code packaged here is a refinement of the subsequently supplied local, no-reload
Playwright helper. It is not a vendored copy of the upstream instagrapi client, and does
not include its session file, credentials, configuration, or dependency stack. The GPLv3
publication choice retains conservative license continuity with the project's ancestry.
Do not remove applicable notices or relicense inherited third-party material without
reviewing its terms.

## Modifications in this distribution

The supplied no-reload helper was modified for this initial beta publication: generic
account configuration, separate private workspaces, strict input validation, history
binding, improved DOM row discovery, stricter browser endpoints, broader offline tests,
publication safeguards and documentation. The earlier development version labels are not
a history of public releases for this repository.

Python dependencies are installed separately and retain their own licenses. This notice
does not relicense Playwright, Chrome, Python, Instagram content or any other third-party
work. No endorsement by the original project author, Meta, Instagram or Playwright is
implied. No Instagram or third-party brand assets are shipped.

## Windows derivative — 2026-10-15

This separate distribution, `instagram-close-friends-windows`, is derived from:

- Repository: https://github.com/BachYun/instagram-close-friends-playwright
- Commit: `69d249754bf4c932d2163f6b62ce12b046ad2f4b`
- Original source tree: `688773144eec28819b5be3b84005e5b120c286b9`

The input archive was verified to match that Git tree before changes. This Windows port
adds native Windows locks, platform paths, launcher/setup scripts, additional synthetic
and native-CI tests, publisher tooling and Windows documentation. It removes the Windows
platform refusal and the Mac launcher from this distribution. Original source, test and
license notices remain attributed to their respective contributors. The original Git
history and personal commit email are not copied into the new repository.

Native Windows and live Instagram execution have not been verified on the build host.
The complete original GPLv3 license text is retained unchanged; this notice does not
relicense inherited material or any separately installed dependencies.

## Windows-only publication refinement — 2026-10-15

The `0.1.0b2` source package uses the Windows-specific repository name
`instagram-close-friends-windows`, adds issue forms and detailed reporting/command docs,
explicitly enables and verifies GitHub Issues during owner-run publication, and fixes an
argparse percent-formatting failure in the earlier Windows help command. These changes
do not establish native Windows or live Instagram validation. License text is unchanged.
