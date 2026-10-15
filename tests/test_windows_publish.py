"""No remote writes: validate publisher identities, safety checks and cancellation."""
import importlib.util
import json
from pathlib import Path
from unittest.mock import Mock
import pytest

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('win_publisher',ROOT/'scripts'/'publish_github.py')
pub=importlib.util.module_from_spec(spec);spec.loader.exec_module(pub)


def test_noreply_identity_avoids_personal_email():
    login,email=pub.commit_identity({'login':'example-owner','id':123,'email':'private@example.invalid'},'example-owner')
    assert (login,email)==('example-owner','123+example-owner@users.noreply.github.com')


def test_wrong_github_account_rejected():
    with pytest.raises(ValueError,match='not the requested owner'):
        pub.commit_identity({'login':'wrong-owner','id':1},'example-owner')


@pytest.mark.parametrize('data',[{}, {'login':'invalid user','id':1}, {'login':'valid','id':False}, {'login':'valid','id':0}])
def test_invalid_profile_rejected(data):
    with pytest.raises(ValueError):pub.commit_identity(data,None)


def test_existing_repo_never_overwritten(tmp_path):
    (tmp_path/'.git').mkdir()
    with pytest.raises(ValueError,match='fresh extracted folder'):pub.require_fresh_folder(tmp_path)


def test_parent_git_repo_rejected(tmp_path):
    (tmp_path/'.git').mkdir();child=tmp_path/'child';child.mkdir()
    with pytest.raises(ValueError):pub.require_fresh_folder(child)


def test_git_environment_override_rejected(tmp_path,monkeypatch):
    monkeypatch.setenv('GIT_INDEX_FILE','elsewhere')
    with pytest.raises(ValueError,match='Clear custom'):pub.require_fresh_folder(tmp_path)


def test_check_only_never_touches_github(monkeypatch):
    runner=Mock(side_effect=AssertionError('network/git forbidden'))
    monkeypatch.setattr(pub,'run',runner)
    assert pub.main(['--check-only'])==0
    runner.assert_not_called()


def test_confirmation_cancels_before_init(monkeypatch):
    monkeypatch.setattr(pub,'require_fresh_folder',lambda _:None)
    monkeypatch.setattr(pub.shutil,'which',lambda _: '/synthetic/exe')
    runner=Mock(side_effect=[Mock(stdout=json.dumps({'login':'example-owner','id':1})),Mock(stdout='[[]]')])
    monkeypatch.setattr(pub,'run',runner)
    monkeypatch.setattr('builtins.input',lambda _: 'CANCEL')
    assert pub.main(['--owner','example-owner'])==0
    assert len(runner.call_args_list)==2
    assert all(c.args[0]=='gh' for c in runner.call_args_list)


def test_existing_remote_aborts_before_local_git(monkeypatch):
    monkeypatch.setattr(pub,'require_fresh_folder',lambda _:None)
    monkeypatch.setattr(pub.shutil,'which',lambda _: '/synthetic/exe')
    runner=Mock(side_effect=[Mock(stdout=json.dumps({'login':'example-owner','id':1})),
      Mock(stdout=json.dumps([[{'full_name':'example-owner/'+pub.REPO_NAME}]]))])
    monkeypatch.setattr(pub,'run',runner)
    with pytest.raises(ValueError,match='already exists'):pub.main([])
    assert len(runner.call_args_list)==2


def test_publisher_success_with_local_git_and_fake_github(tmp_path,monkeypatch):
    """Exercise real staging/commit, but stub every gh call so no repo is created."""
    import shutil
    import subprocess
    clean=tmp_path/'clean source'
    clean.mkdir()
    for name in pub.checker.public_files(ROOT):
        target=clean/name; target.parent.mkdir(parents=True,exist_ok=True)
        shutil.copyfile(ROOT/name,target)
    monkeypatch.setattr(pub,'ROOT',clean)
    original=pub.run
    gh_calls=[]
    def fake_run(*argv,**kw):
        if argv[0]!='gh': return original(*argv,**kw)
        gh_calls.append(argv)
        if argv[-1]=='user': return subprocess.CompletedProcess(argv,0,json.dumps({'login':'example-owner','id':123}), '')
        if argv[-1] == 'repos/example-owner/' + pub.REPO_NAME:
            return subprocess.CompletedProcess(argv, 0, json.dumps({'full_name':'example-owner/' + pub.REPO_NAME, 'has_issues':True, 'default_branch':'main'}), '')
        if 'user/repos?affiliation=owner&per_page=100' in argv:
            return subprocess.CompletedProcess(argv,0,'[[]]','')
        return subprocess.CompletedProcess(argv,0,'synthetic gh success','')
    monkeypatch.setattr(pub,'run',fake_run)
    which=shutil.which
    monkeypatch.setattr(pub.shutil,'which',lambda n: 'synthetic-gh' if n=='gh' else which(n))
    monkeypatch.setattr('builtins.input',lambda _: 'CREATE example-owner/'+pub.REPO_NAME+' PRIVATE')
    # Even a preexisting environment identity must not leak into the new commit.
    monkeypatch.setenv('GIT_AUTHOR_EMAIL','private@example.invalid')
    monkeypatch.setenv('GIT_COMMITTER_EMAIL','private@example.invalid')
    assert pub.main(['--owner','example-owner','--private'])==0
    commit=original('git','log','-1','--format=%ae|%ce').stdout.strip()
    assert commit=='123+example-owner@users.noreply.github.com|123+example-owner@users.noreply.github.com'
    create=[call for call in gh_calls if call[1:3]==('repo','create')]
    assert len(create)==1 and '--private' in create[0] and '--push' in create[0]
    assert not pub.checker.inspect_index(clean,pub.checker.public_files(clean))


def test_repository_setup_explicitly_enables_issues(monkeypatch):
    target = 'example-owner/' + pub.REPO_NAME
    runner = Mock(side_effect=[Mock(stdout=''), Mock(stdout=json.dumps({'full_name':target,'has_issues':True,'default_branch':'main'}))])
    monkeypatch.setattr(pub, 'run', runner)
    details = pub.configure_repository(target)
    assert details['has_issues'] is True
    edit = runner.call_args_list[0].args
    assert edit[:4] == ('gh', 'repo', 'edit', target)
    assert '--enable-issues' in edit
    assert '--default-branch' in edit and 'main' in edit
    assert all('issue' != c.args[1] for c in runner.call_args_list)


@pytest.mark.parametrize('payload', [
    {'full_name':'example-owner/'+pub.REPO_NAME,'has_issues':False,'default_branch':'main'},
    {'full_name':'someone/other','has_issues':True,'default_branch':'main'},
    {'full_name':'example-owner/'+pub.REPO_NAME,'has_issues':True,'default_branch':'other'},
])
def test_repository_setup_does_not_claim_unverified_success(monkeypatch, payload):
    runner = Mock(side_effect=[Mock(stdout=''), Mock(stdout=json.dumps(payload))])
    monkeypatch.setattr(pub, 'run', runner)
    with pytest.raises(ValueError, match='not confirmed'):
        pub.configure_repository('example-owner/'+pub.REPO_NAME)
