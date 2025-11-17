# Build exe then optionally register it to run on login
# Usage:
#   Open PowerShell as Administrator (not required for HKCU Run)
#   .\scripts\build_and_register.ps1 -RegisterStartup

param(
    [switch] $RegisterStartup
)

$projectRoot = Split-Path -Parent $MyInvocation.MyCommand.Definition
Set-Location $projectRoot

# Build
Write-Host "Building LycusButler.exe..."
.
\scripts\build_exe.ps1

$exePath = Join-Path $projectRoot "dist\LycusButler.exe"
if (!(Test-Path $exePath)) {
    Write-Error "Exe not found at $exePath. Build failed or dist not present."
    exit 1
}

if ($RegisterStartup) {
    Write-Host "Registering startup entry..."
    python .\scripts\register_startup.py "$exePath" "LycusButler"
    Write-Host "Registered startup."
} else {
    Write-Host "Build complete. To register startup run:"
    Write-Host "python .\scripts\register_startup.py \"$exePath\" LycusButler"
}
