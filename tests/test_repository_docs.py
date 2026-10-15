"""Offline publication regressions. No GitHub or Instagram requests."""
import re
import subprocess
import sys
from pathlib import Path
from urllib.parse import urlsplit

import pytest
import yaml

ROOT = Path(__file__).resolve().parents[1]


def test_main_help_handles_windows_environment_literal():
    proc = subprocess.run([sys.executable, str(ROOT / 'close_friends_csv.py'), '--help'],
                          capture_output=True, text=True, encoding='utf-8')
    assert proc.returncode == 0, proc.stderr
    assert '%LOCALAPPDATA%' in proc.stdout
    assert '--verify-pending' in proc.stdout


@pytest.mark.parametrize('script', ['launch_chrome_windows.py', 'publish_github.py'])
def test_auxiliary_help_is_offline(script):
    proc = subprocess.run([sys.executable, str(ROOT / 'scripts' / script), '--help'],
                          capture_output=True, text=True, encoding='utf-8')
    assert proc.returncode == 0, proc.stderr


@pytest.mark.parametrize('filename', ['bug_report.yml', 'setup_help.yml', 'feature_request.yml'])
def test_issue_forms_structure(filename):
    data = yaml.safe_load((ROOT / '.github' / 'ISSUE_TEMPLATE' / filename).read_text(encoding="utf-8"))
    assert len(data['name']) >= 3 and data['description']
    assert data['title'].startswith('[Windows')
    assert data['labels']
    ids = set()
    for item in data['body']:
        assert item['type'] in {'markdown', 'input', 'textarea', 'dropdown', 'checkboxes'}
        assert 'attributes' in item
        if item['type'] != 'markdown':
            assert item['id'] not in ids
            ids.add(item['id'])
            assert item['attributes']['label']
        if item['type'] == 'dropdown':
            assert all(isinstance(value, str) and value for value in item['attributes']['options'])
    assert any(item['type'] == 'checkboxes' for item in data['body'])


def test_issue_configuration_links_are_windows_specific():
    cfg = yaml.safe_load((ROOT / '.github' / 'ISSUE_TEMPLATE' / 'config.yml').read_text(encoding="utf-8"))
    assert cfg['blank_issues_enabled'] is False
    for link in cfg['contact_links']:
        url = urlsplit(link['url'])
        assert url.scheme == 'https' and url.netloc == 'github.com'
        assert url.path.startswith('/BachYun/instagram-close-friends-windows/')


def test_readme_is_windows_only_and_has_issues_section():
    text = (ROOT / 'README.md').read_text(encoding="utf-8")
    assert text.startswith('# Instagram Close Friends — Windows Only')
    assert '\n## Issues\n' in text
    assert 'Native Windows validation is pending' in text
    assert 'bug_report.yml' in text and 'setup_help.yml' in text and 'feature_request.yml' in text


def test_relative_markdown_file_links_exist():
    # Ignore command text and URL anchors; check ordinary inline local file links.
    for path in [ROOT / 'README.md', *list((ROOT / 'docs').glob('*.md'))]:
        for link in re.findall(r'\]\(([^\s)]+)\)', path.read_text(encoding="utf-8")):
            if link.startswith(('https:', 'http:', '#', 'mailto:')):
                continue
            filepart = link.split('#')[0]
            if filepart:
                assert (path.parent / filepart).exists(), (path.name, link)
