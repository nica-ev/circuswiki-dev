$ErrorActionPreference = "Stop"

$Root = Resolve-Path (Join-Path $PSScriptRoot "..")
$Site = Join-Path $Root "site"

Push-Location $Root
try {
    python tools/configure_site_base.py
    python tools/stage_multilang.py

    if (Test-Path $Site) {
        Remove-Item -LiteralPath $Site -Recurse -Force
    }

    zensical build
    zensical build -f zensical.en.toml
    zensical build -f zensical.pl.toml
}
finally {
    Pop-Location
}
