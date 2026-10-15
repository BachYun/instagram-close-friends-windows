"""Launcher planning tests. Never start a real Chrome process or sign into Instagram."""
import importlib.util
from pathlib import Path
from unittest.mock import Mock
import subprocess
import pytest

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('win_launcher',ROOT/'scripts'/'launch_chrome_windows.py')
launcher=importlib.util.module_from_spec(spec);spec.loader.exec_module(launcher)


def test_candidates_cover_machine_and_user_installs(tmp_path):
    values={key:str(tmp_path/key) for key in ['ProgramFiles','ProgramFiles(x86)','LOCALAPPDATA']}
    candidates=launcher.chrome_candidates(values)
    assert len(candidates)==3
    assert all(p.name=='chrome.exe' for p in candidates)


def test_explicit_binary_overrides_candidates(tmp_path):
    exe=tmp_path/'Browser Folder'/'chrome.exe';exe.parent.mkdir();exe.write_text('synthetic')
    assert launcher.find_chrome(exe,{})==exe


def test_missing_chrome_actionable():
    with pytest.raises(ValueError,match='Chrome was not found'):launcher.find_chrome(None,{})


@pytest.mark.parametrize('suffix',['','Default','Profile 1'])
def test_ordinary_profile_refused(tmp_path,suffix):
    profile=tmp_path/'Google'/'Chrome'/'User Data'/suffix
    with pytest.raises(ValueError,match='ordinary Chrome'):
        launcher.check_profile(profile,{'LOCALAPPDATA':str(tmp_path)})


def test_profile_as_file_refused(tmp_path):
    p=tmp_path/'a';p.write_text('not a folder')
    with pytest.raises(ValueError,match='is a file'):launcher.check_profile(p,{'LOCALAPPDATA':str(tmp_path)})


def test_command_preserves_spaces_and_loopback(tmp_path):
    exe=tmp_path/'Program Files'/'chrome.exe';profile=tmp_path/'Private Data'/'chrome-profile'
    args=launcher.build_command(exe,profile,9222)
    assert args[0]==str(exe)
    assert f'--user-data-dir={profile}' in args
    assert '--remote-debugging-address=127.0.0.1' in args
    assert not any('disable-blink' in x or 'no-sandbox' in x for x in args)
    assert '"' in subprocess.list2cmdline(args)


@pytest.mark.parametrize('port',[0,80,65536])
def test_bad_port_rejected(port,tmp_path):
    with pytest.raises(ValueError):launcher.build_command(tmp_path/'chrome.exe',tmp_path,port)


def test_dry_run_no_launch_or_profile_creation(tmp_path,monkeypatch):
    exe=tmp_path/'chrome.exe';exe.write_text('synthetic')
    profile=tmp_path/'new profile'
    monkeypatch.setattr(launcher.sys,'platform','win32')
    launch=Mock(side_effect=AssertionError('no process'))
    monkeypatch.setattr(launcher.subprocess,'Popen',launch)
    probe=Mock(side_effect=AssertionError('no socket'))
    monkeypatch.setattr(launcher,'is_listening',probe)
    assert launcher.main(['--chrome',str(exe),'--profile',str(profile),'--dry-run'])==0
    assert not profile.exists()
    launch.assert_not_called();probe.assert_not_called()


def test_existing_port_not_reused_or_killed(tmp_path,monkeypatch):
    exe=tmp_path/'chrome.exe';exe.write_text('synthetic')
    monkeypatch.setattr(launcher.sys,'platform','win32')
    monkeypatch.setattr(launcher,'is_listening',lambda _:True)
    launch=Mock();monkeypatch.setattr(launcher.subprocess,'Popen',launch)
    with pytest.raises(ValueError,match='already in use'):
        launcher.main(['--chrome',str(exe),'--profile',str(tmp_path/'new profile')])
    launch.assert_not_called()


def test_launch_passes_argument_array_not_shell_string(tmp_path,monkeypatch):
    exe=tmp_path/'chrome.exe';exe.write_text('synthetic')
    profile=tmp_path/'new profile'
    monkeypatch.setattr(launcher.sys,'platform','win32')
    monkeypatch.setattr(launcher,'is_listening',lambda _:False)
    launch=Mock(return_value=Mock(pid=123));monkeypatch.setattr(launcher.subprocess,'Popen',launch)
    assert launcher.main(['--chrome',str(exe),'--profile',str(profile)])==0
    args,kwargs=launch.call_args
    assert isinstance(args[0],list)
    assert kwargs=={'close_fds':True}
    assert profile.is_dir()
