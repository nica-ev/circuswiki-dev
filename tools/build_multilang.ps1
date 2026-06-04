$ErrorActionPreference = "Stop"

$Root = Resolve-Path (Join-Path $PSScriptRoot "..")
$Site = Join-Path $Root "site"

Push-Location $Root
try {
    python tools/stage_multilang.py

    if (Test-Path $Site) {
        Remove-Item -LiteralPath $Site -Recurse -Force
    }

    zensical build
    zensical build -f zensical.en.toml
}
finally {
    Pop-Location
}
