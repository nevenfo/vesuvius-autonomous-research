# Weekly VESUVIUS watch, launched by the scheduled task Windows "VesuviusResearchWatch".
# No commit: report + state written to watch/, analysed in the next Claude Code session.
$ErrorActionPreference = "Continue"
$Repo = Split-Path -Parent $PSScriptRoot
$Py   = Join-Path $env:USERPROFILE "vesuvius-work\.venv\Scripts\python.exe"
$LogDir = Join-Path $env:USERPROFILE "vesuvius-work\logs"
New-Item -ItemType Directory -Force $LogDir | Out-Null
$Log = Join-Path $LogDir "watch.log"
$env:PYTHONPATH = Join-Path $Repo "src"
$env:PYTHONIOENCODING = "utf-8"
Add-Content $Log "[$(Get-Date -Format s)] start"
if (-not (Test-Path (Join-Path $Repo "src\vesres\watch.py"))) { Add-Content $Log "[$(Get-Date -Format s)] depot inaccessible (NAS/SMB) - exit 2"; exit 2 }
& $Py -m vesres.watch --root $Repo 2>&1 | ForEach-Object { "$_" } | Out-File -Append -Encoding utf8 $Log
$rc = $LASTEXITCODE
Add-Content $Log "[$(Get-Date -Format s)] exit $rc"
exit $rc
