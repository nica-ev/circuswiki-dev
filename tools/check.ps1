param(
    # Include the full multilingual Zensical build. This is slower but closest to deployment.
    [switch]$FullBuild,

    # Skip staging when only fast Python checks are needed.
    [switch]$NoStage
)

$ErrorActionPreference = "Stop"

$Root = Resolve-Path (Join-Path $PSScriptRoot "..")
Push-Location $Root
try {
    Write-Host "== Python syntax =="
    python -m compileall tools

    Write-Host "== Language registry =="
    python -m tools.core.languages

    Write-Host "== Unit tests =="
    python -m unittest discover tools/tests

    if (-not $NoStage) {
        Write-Host "== Multilingual staging =="
        python tools/stage_multilang.py
    }

    if ($FullBuild) {
        Write-Host "== Full multilingual build =="
        powershell -ExecutionPolicy Bypass -File tools/build_multilang.ps1
    }
}
finally {
    Pop-Location
}
