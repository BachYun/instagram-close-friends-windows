# SPDX-License-Identifier: GPL-3.0-only
# Windows PowerShell 5.1+ / PowerShell 7. No Administrator rights needed.
[CmdletBinding()]
param([ValidateSet('3.12','3.13')][string]$PythonVersion = '3.12', [switch]$Dev)
Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'
if ($env:OS -ne 'Windows_NT') { throw 'This setup script requires Windows.' }
$root = Split-Path -Parent $PSScriptRoot
$venv = Join-Path $root '.venv'
$python = Join-Path $venv 'Scripts\python.exe'
if ((Test-Path -LiteralPath $venv) -and -not (Test-Path -LiteralPath $python)) {
    throw 'A non-Windows or incomplete .venv exists. Use a fresh extracted folder; no files were deleted.'
}
if (-not (Test-Path -LiteralPath $python)) {
    if (-not (Get-Command py -ErrorAction SilentlyContinue)) {
        throw 'Python launcher not found. Install Python 3.12 or 3.13 for Windows, then reopen PowerShell.'
    }
    & py "-$PythonVersion" -m venv $venv
    if ($LASTEXITCODE -ne 0) { throw 'Creating the Python environment failed.' }
}
& $python -c 'import sys; assert sys.version_info >= (3, 12), "Python 3.12+ required"'
if ($LASTEXITCODE -ne 0) { throw 'The existing Python environment is too old.' }
$requirements = if ($Dev) { 'requirements-dev.txt' } else { 'requirements.txt' }
& $python -m pip install -r (Join-Path $root $requirements)
if ($LASTEXITCODE -ne 0) { throw 'Dependency installation failed; do not continue.' }
& $python (Join-Path $root 'close_friends_csv.py') --version
if ($LASTEXITCODE -ne 0) { throw 'Version check failed.' }
Write-Host 'Setup complete. No Instagram login or actions performed.'
