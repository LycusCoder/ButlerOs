# --- Dependency Installation ---
Write-Host "⚙️ Installing/updating dependencies from requirements.txt..."
$pipPath = Join-Path $PSScriptRoot ".venv\scripts\pip.exe"
& $pipPath install -r (Join-Path $PSScriptRoot "requirements.txt")

# --- Application Launch ---
Write-Host "🚀 Launching Lycus Butler app silently..."

# Construct the absolute path to the WINDOWLESS python executable
$pythonwPath = Join-Path $PSScriptRoot ".venv\scripts\pythonw.exe"

# Launch the application silently using pythonw.exe
Start-Process -FilePath $pythonwPath -ArgumentList ".\src\butler.py" -WorkingDirectory $PSScriptRoot

Write-Host "✅ Lycus Butler app started in the background."