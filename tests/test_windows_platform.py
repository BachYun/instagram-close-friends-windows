"""Synthetic Windows backend tests plus real local-process lock tests on the host OS."""
import errno
import io
import os
from pathlib import Path
import subprocess
import sys
from types import SimpleNamespace
from unittest.mock import Mock, call

import pytest
import cf_platform as platform
from test_helper import m, project

ROOT = Path(__file__).resolve().parents[1]


def test_windows_data_uses_localappdata(tmp_path):
    assert platform.default_data_root(windows=True, environ={'LOCALAPPDATA':str(tmp_path)}) == tmp_path/'InstagramCloseFriendsWindows'


def test_windows_data_fallback(tmp_path, monkeypatch):
    monkeypatch.setattr(platform.Path, 'home', lambda: tmp_path)
    assert platform.default_data_root(windows=True, environ={}) == tmp_path/'AppData'/'Local'/'InstagramCloseFriendsWindows'


def test_unix_development_fallback(tmp_path, monkeypatch):
    monkeypatch.setattr(platform.Path, 'home', lambda: tmp_path)
    assert platform.default_data_root(windows=False, environ={}) == tmp_path/'.local'/'share'/platform.PROJECT


def test_shared_windows_port_lock_root(tmp_path, monkeypatch):
    monkeypatch.setenv('LOCALAPPDATA', str(tmp_path))
    monkeypatch.setattr(platform, 'is_windows', lambda: True)
    assert platform.endpoint_lock_root() == tmp_path/'InstagramCloseFriendsWindows'/'locks'


def test_data_override_preserved(tmp_path, monkeypatch):
    monkeypatch.setenv('CLOSE_FRIENDS_DATA_DIR', str(tmp_path/'Private Data'))
    assert m.default_data_dir() == tmp_path/'Private Data'


def test_msvcrt_lock_uses_same_byte_nonblocking(monkeypatch):
    crt = SimpleNamespace(locking=Mock(), LK_NBLCK=2, LK_UNLCK=0)
    monkeypatch.setitem(sys.modules,'msvcrt',crt)
    handle = Mock(); handle.fileno.return_value=15
    platform.acquire_lock(handle, windows=True)
    platform.release_lock(handle, windows=True)
    assert handle.seek.call_args_list == [call(0),call(0)]
    assert crt.locking.call_args_list == [call(15,2,1),call(15,0,1)]
    handle.write.assert_not_called()


def test_msvcrt_conflict_not_retried(monkeypatch):
    crt=SimpleNamespace(locking=Mock(side_effect=OSError(errno.EACCES,'locked')), LK_NBLCK=2)
    monkeypatch.setitem(sys.modules,'msvcrt',crt)
    with pytest.raises(OSError): platform.acquire_lock(Mock(), windows=True)
    crt.locking.assert_called_once()


def test_lock_failure_never_unlocks_unowned_region(tmp_path, monkeypatch):
    monkeypatch.setattr(platform,'acquire_lock',Mock(side_effect=OSError(errno.EACCES,'busy')))
    release=Mock(); monkeypatch.setattr(platform,'release_lock',release)
    with pytest.raises(ValueError,match='busy file'):
        with platform.file_lock(tmp_path/'x.lock','busy file'): pass
    release.assert_not_called()
    assert (tmp_path/'x.lock').read_bytes()==b''


def test_noncontention_error_not_mislabeled(tmp_path, monkeypatch):
    monkeypatch.setattr(platform,'acquire_lock',Mock(side_effect=OSError(errno.EIO,'io failure')))
    with pytest.raises(OSError):
        with platform.file_lock(tmp_path/'x.lock','busy file'): pass


def test_lock_released_on_exception(tmp_path):
    path=tmp_path/'empty.lock'
    with pytest.raises(RuntimeError):
        with platform.file_lock(path,'busy'): raise RuntimeError('synthetic')
    with platform.file_lock(path,'busy'): pass
    assert path.exists()  # never unlink the coordination inode/file


def run_child(code, path):
    return subprocess.run([sys.executable,'-c',code,str(ROOT),str(path)],
                          capture_output=True,text=True,timeout=15)


def test_native_process_exclusion_then_release(tmp_path):
    path=tmp_path/'folder with spaces'; path.mkdir()
    lock=path/'x.lock'
    child='''import sys
sys.path.insert(0,sys.argv[1])
from pathlib import Path
from cf_platform import file_lock
try:
    with file_lock(Path(sys.argv[2]), 'busy'): pass
except ValueError:
    sys.exit(23)
'''
    with platform.file_lock(lock,'busy'):
        result=run_child(child,lock)
        assert result.returncode==23, result.stderr
    result=run_child(child,lock)
    assert result.returncode==0, result.stderr


def test_native_process_exit_releases_lock(tmp_path):
    lock=tmp_path/'x.lock'
    child='''import os,sys
sys.path.insert(0,sys.argv[1])
from pathlib import Path
from cf_platform import file_lock
with file_lock(Path(sys.argv[2]), 'busy'):
    os._exit(0)
'''
    result=run_child(child,lock)
    assert result.returncode==0,result.stderr
    with platform.file_lock(lock,'busy'): pass


def test_console_output_redirect_does_not_crash(monkeypatch):
    raw=io.BytesIO()
    output=io.TextIOWrapper(raw,encoding='cp1252')
    monkeypatch.setattr(platform,'is_windows',lambda:True)
    monkeypatch.setattr(platform.sys,'stdout',output)
    monkeypatch.setattr(platform.sys,'stderr',output)
    platform.configure_console()
    output.write('\u2713'); output.flush()
    assert raw.getvalue()==b'\\u2713'


def test_windows_platform_not_rejected_before_status(project,monkeypatch):
    # Real lock backend is exercised above/on native CI. Here validate CLI gating only.
    import contextlib
    monkeypatch.setattr(m.sys,'platform','win32')
    monkeypatch.setattr(m,'run_lock',contextlib.nullcontext)
    assert m.main(['--status'])==0


def test_ci_requires_native_windows_when_requested():
    if os.getenv('CF_REQUIRE_NATIVE_WINDOWS')=='1':
        assert sys.platform=='win32'
