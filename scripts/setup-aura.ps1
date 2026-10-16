param([switch]$IncludeSample)
$ErrorActionPreference = 'Stop'
$stationRoot = Split-Path -Parent $PSScriptRoot
Set-Location -LiteralPath $stationRoot
if (-not (Test-Path -LiteralPath '.venv\Scripts\python.exe')) {
    python -m venv .venv
    if ($LASTEXITCODE -ne 0) { throw 'Could not create Python environment' }
}
& .\.venv\Scripts\python.exe -m pip install torch==2.5.1 torchvision==0.20.1 --index-url https://download.pytorch.org/whl/cpu
if ($LASTEXITCODE -ne 0) { throw 'CPU PyTorch installation failed' }
& .\.venv\Scripts\python.exe -m pip install -r requirements-ai.txt
if ($LASTEXITCODE -ne 0) { throw 'AI dependency installation failed' }
$assetArguments = @('scripts/setup_aura.py', '--model', 'both')
if ($IncludeSample) { $assetArguments += '--sample' }
& .\.venv\Scripts\python.exe @assetArguments
if ($LASTEXITCODE -ne 0) { throw 'AI asset verification failed' }
Write-Host 'AI ready. Start scripts/start.ps1, then use Test AI on your video.'
