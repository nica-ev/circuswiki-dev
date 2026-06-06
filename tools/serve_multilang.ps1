param(
    # Address to bind the preview server to. Use 0.0.0.0 for local-network testing.
    [string]$HostAddress = "127.0.0.1",

    # Local port for the preview server.
    [int]$Port = 8000,

    # Skip rebuilding and serve the existing site/ output.
    [switch]$NoBuild
)

$ErrorActionPreference = "Stop"

$Root = Resolve-Path (Join-Path $PSScriptRoot "..")
Push-Location $Root
try {
    if (-not $NoBuild) {
        powershell -ExecutionPolicy Bypass -File tools/build_multilang.ps1
    }

    python tools/serve_multilang_site.py --host $HostAddress --port $Port
}
finally {
    Pop-Location
}
