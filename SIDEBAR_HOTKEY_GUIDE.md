# 🎯 Butler Sidebar - Hotkey Customization Guide

## Overview
Butler Sidebar sekarang fully customizable! Trigger sidebar dengan hotkey pilihan lo, bukan cuma default.

## Default Hotkeys

| Fungsi | Hotkey | File |
|--------|--------|------|
| 🔍 Quick Menu (Search) | `Ctrl+Alt+M` | `config.json` |
| 📋 Sidebar Toggle | `Ctrl+Alt+S` | `config.json` |

## Customize Hotkey

### Step 1: Buka `config.json`
```bash
src/config/config.json
```

### Step 2: Edit Hotkey
Cari section ini:
```json
{
  "hotkey": "ctrl+alt+m",
  "sidebar_hotkey": "ctrl+alt+s",
  "quick_apps": [...]
}
```

### Step 3: Pilih Hotkey Baru

#### Hotkey Format
```
modifier1+modifier2+key
```

#### Modifiers
- `ctrl` - Control
- `alt` - Alt
- `shift` - Shift
- `win` - Windows Key

#### Key Examples
```
# Single letter
"a", "b", "c" ... "z"

# Numbers
"0", "1", "2" ... "9"

# Special keys
"f1", "f2" ... "f12"  (function keys)
"enter"               (Enter)
"space"               (Space bar)
"esc"                 (Escape)
"tab"                 (Tab)
"delete"
"backspace"
"up", "down", "left", "right"  (Arrow keys)
```

### Contoh Konfigurasi

#### Option 1: Simple (Recommended)
```json
{
  "hotkey": "ctrl+alt+m",
  "sidebar_hotkey": "ctrl+alt+s",
  ...
}
```

#### Option 2: Windows Key Combo
```json
{
  "hotkey": "win+e",
  "sidebar_hotkey": "win+shift+s",
  ...
}
```

#### Option 3: Shift+Alt Combo
```json
{
  "hotkey": "shift+alt+a",
  "sidebar_hotkey": "shift+alt+s",
  ...
}
```

#### Option 4: Function Keys
```json
{
  "hotkey": "f1",
  "sidebar_hotkey": "f2",
  ...
}
```

#### Option 5: Indonesian Preference
```json
{
  "hotkey": "ctrl+alt+p",
  "sidebar_hotkey": "ctrl+alt+d",
  ...
}
```

## Step 4: Restart App
Simpan config.json, terus restart Butler:

```bash
# Kill app
Stop-Process -Name "python" -ErrorAction SilentlyContinue

# Restart
python src/butler.py
```

## Verify Hotkey

Cek logs saat startup:
```
[LISTENER] Hotkey untuk menu: ctrl+alt+m
[LISTENER] Hotkey untuk sidebar: ctrl+alt+s
[LISTENER] Semua hotkey aktif!
```

## Troubleshooting

### Hotkey gak Registered
**Problem**: Hotkey sudah di-config tapi gak jalan
**Solution**:
1. Pastikan syntax benar (lowercase semua)
2. Jangan pakai spasi: `ctrl + alt + m` ❌ → `ctrl+alt+m` ✅
3. Check apakah hotkey conflict dengan Windows atau aplikasi lain

### Hotkey Conflict
**Problem**: Hotkey lo conflict dengan shortcut Windows atau aplikasi lain
**Solution**: Pilih hotkey yang tidak dipakai
- `Win+S` - Reserved Windows (Search)
- `Win+V` - Reserved Windows (Clipboard)
- `Win+E` - Reserved Windows (Explorer)
- Cek task manager atau Google untuk conflict check

### App Crash saat Startup
**Problem**: Hotkey syntax error menyebabkan app crash
**Solution**:
1. Cek JSON syntax: gunakan https://jsonlint.com/
2. Pastikan format valid:
```json
{
  "hotkey": "ctrl+alt+m",
  "sidebar_hotkey": "ctrl+alt+s",
  ...
}
```

## Pro Tips

### Quick Menu vs Sidebar
- **Quick Menu** (Ctrl+Alt+M) = Search & launch apps
- **Sidebar** (Ctrl+Alt+S) = System monitor + notes + todos

### Optimal Combinations
```json
// If using lots of shortcuts
{
  "hotkey": "alt+space",
  "sidebar_hotkey": "alt+s"
}

// If gaming (avoid Ctrl+Alt conflict)
{
  "hotkey": "f1",
  "sidebar_hotkey": "f2"
}

// Minimalist
{
  "hotkey": "shift+space",
  "sidebar_hotkey": "shift+s"
}
```

### Windows Hotkey Reference
Common Windows hotkeys to avoid:
- `Win+D` - Show desktop
- `Win+I` - Settings
- `Win+E` - File Explorer
- `Win+V` - Clipboard
- `Win+Shift+S` - Screenshot
- `Alt+Tab` - Switch window
- `Alt+F4` - Close window

## Architecture

### How It Works
1. `butler.py` reads hotkeys dari `config.json`
2. `listener.py` (dalam background thread) register hotkeys menggunakan `keyboard` library
3. Saat hotkey dipencet, callback function di-trigger
4. App opens sidebar atau quick menu

### File Structure
```
src/
  butler.py           # Main app + hotkey registration
  config/
    config.json       # Hotkey config (EDIT HERE!)
  utils/
    system_tray.py    # Alternative trigger via tray menu
```

## Config Reference

```json
{
  "hotkey": "ctrl+alt+m",           // Quick Menu hotkey
  "sidebar_hotkey": "ctrl+alt+s",   // Sidebar hotkey
  "quick_apps": [                    // Apps list
    {
      "name": "VS Code",
      "path": "code"
    },
    ...
  ]
}
```

## Advanced: System Tray Alternative

Gak mau pakai hotkey? Bisa trigger dari system tray:
1. Right-click tray icon (butler.ico)
2. Click "Toggle Sidebar"
3. Click "Toggle Dashboard" (kalau masih ada)

## Questions?

Kalau ada issue dengan hotkey:
1. Check logs di console
2. Verify syntax di config.json
3. Test hotkey combination di PowerShell:
```powershell
# Install keyboard library test
pip show keyboard
```

---

**Updated**: Phase 3 - Sidebar Optimization
**Last tested on**: Windows 11, Python 3.11, CustomTkinter 5.2.2
