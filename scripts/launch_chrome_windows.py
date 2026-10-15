#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-3.0-only
"""Launch installed Chrome with a dedicated Windows profile and loopback CDP.

No browser automation, login, credentials, session export, stealth flags, or reloads.
Use --dry-run to inspect the exact argument list without launching anything.
"""
from __future__ import annotations
import argparse
import os
from pathlib import Path
import socket
import subprocess
import sys
from typing import Mapping

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from cf_platform import configure_console, default_data_root

URL = "https://www.instagram.com/accounts/close_friends/"


def chrome_candidates(env: Mapping[str, str]) -> list[Path]:
    paths = []
    for key in ("ProgramFiles", "ProgramFiles(x86)", "LOCALAPPDATA"):
        if env.get(key):
            paths.append(Path(env[key]) / "Google" / "Chrome" / "Application" / "chrome.exe")
    return paths


def find_chrome(explicit: Path | None, env: Mapping[str, str]) -> Path:
    choices = [explicit.expanduser()] if explicit is not None else chrome_candidates(env)
    for path in choices:
        if path.is_file() and path.name.lower() == "chrome.exe":
            return path.resolve()
    raise ValueError("Google Chrome was not found. Install Chrome, or pass --chrome with its full chrome.exe path.")


def check_profile(profile: Path, env: Mapping[str, str]) -> Path:
    profile = profile.expanduser().resolve()
    if str(profile).startswith("\\\\"):
        raise ValueError("Use a local dedicated profile, not a network share.")
    if profile.is_file():
        raise ValueError("The profile path is a file, not a folder.")
    # Refuse the ordinary Chrome root and all profiles inside it (Default/Profile 1/etc.).
    local = Path(env.get("LOCALAPPDATA", str(Path.home() / "AppData" / "Local")))
    ordinary = (local / "Google" / "Chrome" / "User Data").resolve()
    if profile == ordinary or ordinary in profile.parents:
        raise ValueError("Do not use your ordinary Chrome User Data/Default profile. Use a separate helper profile.")
    return profile


def build_command(chrome: Path, profile: Path, port: int) -> list[str]:
    if not 1024 <= port <= 65535:
        raise ValueError("Choose a debugging port from 1024 to 65535.")
    return [str(chrome), f"--remote-debugging-port={port}",
            "--remote-debugging-address=127.0.0.1", f"--user-data-dir={profile}",
            "--no-first-run", "--no-default-browser-check", URL]


def is_listening(port: int) -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.settimeout(0.5)
        return sock.connect_ex(("127.0.0.1", port)) == 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--chrome", type=Path)
    parser.add_argument("--profile", type=Path,
                        default=default_data_root(windows=True) / "chrome-profile")
    parser.add_argument("--port", type=int, default=9222)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args(argv)
    if sys.platform != "win32":
        parser.error("This launcher is for native Windows. It does not launch Chrome on macOS/Linux.")
    chrome = find_chrome(args.chrome, os.environ)
    profile = check_profile(args.profile, os.environ)
    command = build_command(chrome, profile, args.port)
    if args.dry_run:
        print("DRY RUN: no profile created, no browser launched.")
        print(subprocess.list2cmdline(command))
        return 0
    if is_listening(args.port):
        raise ValueError(f"Port {args.port} is already in use. Keep your existing dedicated Chrome, or investigate manually; no process was stopped.")
    profile.mkdir(parents=True, exist_ok=True)
    child = subprocess.Popen(command, close_fds=True)
    print(f"Chrome launch requested (process {child.pid}).")
    print(f"Dedicated profile: {profile}")
    print(f"Local debugging: http://127.0.0.1:{args.port}")
    print("Sign in manually on Instagram. Keep exactly ONE Close Friends tab open.")
    print("Keep this profile private. Do not expose/forward the debugging port.")
    print("Close this dedicated Chrome when finished. No login has been performed by this launcher.")
    return 0


if __name__ == "__main__":
    configure_console()
    try:
        raise SystemExit(main())
    except (ValueError, OSError) as exc:
        print(f"LAUNCH ERROR: {exc}", file=sys.stderr)
        raise SystemExit(1)
