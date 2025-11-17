import sys
import os
import winreg

"""
Register the given exe path to current user's Run key so it starts on login.
Usage:
    python register_startup.py "C:\path\to\LycusButler.exe"

Requires Windows.
This writes to HKCU\Software\Microsoft\Windows\CurrentVersion\Run
"""

def register(app_name: str, exe_path: str):
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                             r"Software\Microsoft\Windows\CurrentVersion\Run",
                             0, winreg.KEY_SET_VALUE)
        # Ensure path quoted
        value = f'"{exe_path}"'
        winreg.SetValueEx(key, app_name, 0, winreg.REG_SZ, value)
        winreg.CloseKey(key)
        print(f"Registered {app_name} to run at login: {exe_path}")
    except Exception as e:
        print(f"Error registering startup: {e}")


def unregister(app_name: str):
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                             r"Software\Microsoft\Windows\CurrentVersion\Run",
                             0, winreg.KEY_ALL_ACCESS)
        winreg.DeleteValue(key, app_name)
        winreg.CloseKey(key)
        print(f"Removed {app_name} from startup")
    except FileNotFoundError:
        print(f"{app_name} not found in startup entries")
    except Exception as e:
        print(f"Error unregistering startup: {e}")


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python register_startup.py <path-to-exe> [app-name]")
        sys.exit(1)
    exe = sys.argv[1]
    name = sys.argv[2] if len(sys.argv) > 2 else "LycusButler"
    exe = os.path.abspath(exe)
    register(name, exe)
