# SPDX-License-Identifier: GPL-3.0-only
"""Platform paths and nonblocking locks. Never delete lock files on release.

Windows locks one byte at offset zero, including on an empty file. Microsoft CRT
permits locking beyond EOF. No initialization write can race with another holder.
POSIX uses flock. These coordinate local processes, not other computers/old bots.
"""
from __future__ import annotations

from contextlib import contextmanager
import errno
import os
from pathlib import Path
import sys
from typing import BinaryIO, Iterator, Mapping

WINDOWS_APP = "InstagramCloseFriendsWindows"
LOCK_NAMESPACE = "instagram-close-friends-playwright"
PROJECT = "instagram-close-friends-windows"


def is_windows() -> bool:
    return sys.platform == "win32"


def default_data_root(*, windows: bool | None = None,
                      environ: Mapping[str, str] | None = None) -> Path:
    env = os.environ if environ is None else environ
    if windows is None:
        windows = is_windows()
    if windows:
        base = Path(env["LOCALAPPDATA"]) if env.get("LOCALAPPDATA") else Path.home() / "AppData" / "Local"
        return base / WINDOWS_APP
    return Path.home() / ".local" / "share" / PROJECT


def endpoint_lock_root() -> Path:
    if is_windows():
        return default_data_root() / "locks"
    # Share the original helper's endpoint namespace when using the POSIX fallback.
    return Path.home() / ".cache" / LOCK_NAMESPACE / "locks"


def acquire_lock(handle: BinaryIO, *, windows: bool | None = None) -> None:
    if windows is None:
        windows = is_windows()
    if windows:
        import msvcrt
        handle.seek(0)
        msvcrt.locking(handle.fileno(), msvcrt.LK_NBLCK, 1)
    else:
        import fcntl
        fcntl.flock(handle.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)


def release_lock(handle: BinaryIO, *, windows: bool | None = None) -> None:
    if windows is None:
        windows = is_windows()
    if windows:
        import msvcrt
        handle.seek(0)
        msvcrt.locking(handle.fileno(), msvcrt.LK_UNLCK, 1)
    else:
        import fcntl
        fcntl.flock(handle.fileno(), fcntl.LOCK_UN)


@contextmanager
def file_lock(path: Path, message: str) -> Iterator[None]:
    path = Path(path)
    if path.is_symlink():
        raise ValueError("Refusing a symlinked lock file.")
    flags = os.O_RDWR | os.O_CREAT | getattr(os, "O_BINARY", 0) | getattr(os, "O_NOFOLLOW", 0)
    fd = os.open(path, flags, 0o600)
    with os.fdopen(fd, "r+b", buffering=0) as handle:
        try:
            acquire_lock(handle)
        except OSError as exc:
            if exc.errno in {errno.EACCES, errno.EAGAIN, errno.EDEADLK}:
                raise ValueError(message) from exc
            raise
        try:
            yield
        finally:
            release_lock(handle)
    # Do not unlink: waiting/contending processes must keep using the same file.


def configure_console() -> None:
    if is_windows():
        for stream in (sys.stdout, sys.stderr):
            if hasattr(stream, "reconfigure"):
                # Preserve console encoding; avoid exceptions when output is redirected.
                stream.reconfigure(errors="backslashreplace")
