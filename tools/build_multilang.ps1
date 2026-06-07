$ErrorActionPreference = "Stop"

$Root = Resolve-Path (Join-Path $PSScriptRoot "..")
$Site = Join-Path $Root "site"
$LanguageRegistry = Join-Path $Root "tools\config\languages.json"

Push-Location $Root
try {
    $Languages = (Get-Content -LiteralPath $LanguageRegistry -Raw | ConvertFrom-Json).languages

    python tools/configure_site_base.py
    python tools/stage_multilang.py

    if (Test-Path $Site) {
        Remove-Item -LiteralPath $Site -Recurse -Force
    }

    foreach ($Language in $Languages) {
        if ($Language.root) {
            zensical build
        }
        else {
            zensical build -f $Language.zensical
        }
    }

    python tools/augment_sitemaps.py
}
finally {
    Pop-Location
}
