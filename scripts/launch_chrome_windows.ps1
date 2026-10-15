# SPDX-License-Identifier: GPL-3.0-only
[CmdletBinding()]
param([string]$ProfilePath, [string]$ChromePath,
      [ValidateRange(1024,65535)][int]$Port = 9222, [switch]$DryRun)
Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent $PSScriptRoot
$python = Join-Path $root '.venv\Scripts\python.exe'
if (-not (Test-Path -LiteralPath $python)) { throw 'Run scripts\setup_windows.ps1 first.' }
$arguments = @('--port', "$Port")
if ($ProfilePath) { $arguments += @('--profile', $ProfilePath) }
if ($ChromePath) { $arguments += @('--chrome', $ChromePath) }
if ($DryRun) { $arguments += '--dry-run' }
& $python (Join-Path $PSScriptRoot 'launch_chrome_windows.py') @arguments
exit $LASTEXITCODE
