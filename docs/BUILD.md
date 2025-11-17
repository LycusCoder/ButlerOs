# Build & Auto-start Guide (Windows)

This document explains how to build a single EXE for Lycus Butler and configure it to auto-start on Windows.

IMPORTANT: Run the commands locally on your machine. Building an exe requires PyInstaller and access to your Python environment.

## Prerequisites
- Windows 10/11
- Python 3.8+ (3.11 recommended)
- Virtual environment activated (recommended)
- Install dependencies:

```powershell
pip install -r requirements.txt
pip install pyinstaller
```

Note: `keyboard` library may require elevating privileges to capture global hotkeys. If you rely on global hotkeys, run the exe as normal user; if you get permission errors, try running once as Administrator.

## Build EXE (one-file)
From repo root, run (PowerShell):

```powershell
# Option A: run helper script
.\scripts\build_exe.ps1

# Option B: run pyinstaller manually
pyinstaller --noconfirm --clean --onefile --windowed --add-data "src\assets;assets" --icon "src\assets\ico\butler.ico" --name "LycusButler" src\butler.py
```

Output: `dist\LycusButler.exe`

## Register EXE to Auto-Start (per-user)
You can add a Run registry entry under the current user (HKCU) so the exe auto-starts when you log in.

```powershell
# Example (PowerShell):
python .\scripts\register_startup.py "C:\full\path\to\dist\LycusButler.exe" "LycusButler"

# To remove:
python .\scripts\unregister_startup.py "LycusButler"
```

Or use the convenience wrapper to build and register in one step:

```powershell
# Build and register
.\scripts\build_and_register.ps1 -RegisterStartup
```

## Notes & Troubleshooting
- If hotkeys don't work, make sure the `keyboard` library has the privilege it needs. For some global hotkeys, you might need to run the app with elevated permissions.
- Avoid assigning `Win+S` or other reserved Windows shortcuts. Configure hotkeys in `src/config/config.json`.
- If PyInstaller fails to bundle assets, check `--add-data` path formatting on Windows: "src\assets;assets"
- For a GUI app, `--windowed` prevents a console window. Remove it while debugging to see console logs.

## Signing & Distribution (Optional)
- For production distribution, consider code-signing the EXE (recommended to avoid SmartScreen warnings).
- For an installer, consider Inno Setup or NSIS.

## Final checks
- After building and registering, log out and log back in to confirm the app starts automatically.
- Check Windows Task Manager → Startup tab to see the entry.

