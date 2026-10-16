param([string]$Config = "")
$ErrorActionPreference = "Stop"
$stationRoot = Split-Path -Parent $PSScriptRoot
Set-Location -LiteralPath $stationRoot
if (-not (Test-Path -LiteralPath ".venv\Scripts\python.exe")) {
    python -m venv .venv
    if ($LASTEXITCODE -ne 0) { throw "Could not create Python environment" }
    & .\.venv\Scripts\python.exe -m pip install -r requirements.txt
    if ($LASTEXITCODE -ne 0) { throw "Dependency installation failed" }
}
if ($Config) { $env:GS_CONFIG = (Resolve-Path -LiteralPath $Config).Path }
Write-Host "Aero Ground Station: http://127.0.0.1:8000"
& .\.venv\Scripts\python.exe -m uvicorn groundstation.main:app --host 127.0.0.1 --port 8000
