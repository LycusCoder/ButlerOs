import sys
import os
import winreg

"""
Remove startup entry created by register_startup.py
Usage:
    python unregister_startup.py [app-name]
"""

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
    name = sys.argv[1] if len(sys.argv) > 1 else "LycusButler"
    unregister(name)
