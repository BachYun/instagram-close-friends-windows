"""Parse PowerShell sources on native Windows CI; never execute the launch/setup scripts."""
import os
from pathlib import Path
import shutil
import subprocess
import pytest


def test_powershell_sources_parse():
    executable=shutil.which('pwsh') or shutil.which('powershell')
    if not executable:
        if os.getenv('CF_REQUIRE_NATIVE_WINDOWS')=='1':pytest.fail('PowerShell must be installed on Windows CI')
        pytest.skip('PowerShell is not installed on this test host')
    root=Path(__file__).resolve().parents[1]
    program=r'''$ErrorActionPreference='Stop'
$root=$env:CF_PS_PARSE_ROOT
$files=Get-ChildItem -LiteralPath (Join-Path $root 'scripts') -Filter '*.ps1'
foreach($file in $files) {
  $tokens=$null; $errors=$null
  [void][System.Management.Automation.Language.Parser]::ParseFile($file.FullName,[ref]$tokens,[ref]$errors)
  if($errors.Count -gt 0) { $errors | ForEach-Object { Write-Output $_.Message }; exit 1 }
}
Write-Output 'PowerShell source parsing passed.'
'''
    env=os.environ.copy();env['CF_PS_PARSE_ROOT']=str(root)
    result=subprocess.run([executable,'-NoProfile','-NonInteractive','-Command',program],
                          capture_output=True,text=True,env=env,timeout=25)
    assert result.returncode==0,result.stdout+result.stderr
