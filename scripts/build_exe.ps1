# PowerShell build script for Lycus Butler
# Usage: Open PowerShell in repo root and run:
#   .\scripts\build_exe.ps1

$projectRoot = Split-Path -Parent $MyInvocation.MyCommand.Definition
Set-Location $projectRoot

# Clean previous builds
if (Test-Path dist) { Remove-Item -Recurse -Force dist }
if (Test-Path build) { Remove-Item -Recurse -Force build }
if (Test-Path "LycusButler.spec") { Remove-Item -Force "LycusButler.spec" }

# PyInstaller command - adjust paths if needed
$iconPath = Join-Path $projectRoot "src\assets\ico\butler.ico"
$entry = Join-Path $projectRoot "src\butler.py"

# Include the whole assets folder (CustomTkinter might need runtime assets)
$addData = "src\assets;assets"

# Run PyInstaller
pyinstaller --noconfirm --clean --onefile --windowed --add-data "$addData" --icon "$iconPath" --name "LycusButler" "$entry"

if ($LASTEXITCODE -ne 0) {
    Write-Error "PyInstaller failed with exit code $LASTEXITCODE"
    exit $LASTEXITCODE
}

Write-Host "Build complete. EXE located at: dist\LycusButler.exe" -ForegroundColor Green
