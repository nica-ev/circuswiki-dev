$ErrorActionPreference = "Stop"

$Root = Resolve-Path (Join-Path $PSScriptRoot "..")
Push-Location $Root
try {
    python tools/dev_console/server.py
}
finally {
    Pop-Location
}
