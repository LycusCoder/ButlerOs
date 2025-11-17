# ⚡ Butler Dashboard - Quick Reference

## 🔥 Shortcuts & Hotkeys

| Action | Shortcut |
|--------|----------|
| Open Quick Menu | `Ctrl + Alt + M` |
| Toggle Dashboard | Klik kanan tray → "Toggle Dashboard" |
| Close Dashboard | `Esc` atau klik `✕` |
| Toggle Theme | Klik `☀️` / `🌙` di title bar |

---

## 📋 Common Tasks

### Start Butler App
```bash
cd src
python butler.py
```

### Open Dashboard
1. Klik kanan icon di system tray
2. Pilih "Toggle Dashboard"

### Add New Todo
1. Buka Dashboard
2. Klik `+ Add Task`
3. Fill form:
   - Task: "Nama task"
   - Start: "2025-01-15 10:00"
   - Deadline: "2025-01-20 18:00"
4. Klik "Save Task"

### Quick Notes
- Langsung ketik di Dashboard
- Auto-save otomatis
- File: `src/config/notes.txt`

### Add Quick App
1. Klik kanan tray → "Settings"
2. Isi nama & path/command
3. Klik "Add New App"

---

## 📂 File Locations

```
src/config/
├── config.json       # Quick apps configuration
├── todos.json        # Todo list data
└── notes.txt         # Quick notes data
```

---

## 🎨 Dashboard Sections

### 1. System Monitor
- **CPU Usage:** Realtime percentage + progress bar
- **RAM Usage:** Realtime percentage + progress bar
- **Top Processes:** 3 apps dengan RAM usage tertinggi
- **Update:** Setiap 1 detik

### 2. Quick Notes
- **Auto-save:** Setiap keystroke
- **Location:** `src/config/notes.txt`
- **Indicator:** "Auto-saved" status

### 3. Todo List
- **Fields:** Task name, Start time, Deadline
- **Actions:** Check/uncheck, Delete
- **Storage:** `src/config/todos.json`

---

## 🔧 Quick Config

### Change Dashboard Size
**File:** `src/dashboard_window.py` (Line ~13-16)
```python
width = 800   # Default
height = 600  # Default
```

### Change Update Interval
**File:** `src/dashboard_window.py` (Line ~415)
```python
self.after(1000, self.update_system_stats)  # 1 second
```

### Change Hotkey
**File:** `src/config/config.json`
```json
{
  "hotkey": "ctrl+alt+m"
}
```

---

## 🐛 Quick Fixes

| Problem | Solution |
|---------|----------|
| Hotkey tidak work | Run as Administrator (Windows) |
| Icon tidak muncul | Check system tray settings |
| Dashboard blank | Install: `pip install psutil` |
| Tkinter error | Install: `sudo apt-get install python3-tk` (Linux) |

---

## 📦 Dependencies

```bash
pip install customtkinter keyboard pystray pillow psutil
```

---

## 🎯 Todo JSON Format

```json
{
  "todos": [
    {
      "task": "Task name",
      "done": false,
      "start_time": "2025-01-15 10:00",
      "deadline": "2025-01-20 18:00"
    }
  ]
}
```

---

## 🚀 Pro Tips

1. **Drag Dashboard:** Klik title bar, drag anywhere
2. **Fullscreen Mode:** Klik `□` button untuk maximize
3. **Multi-line Notes:** Press Enter di Quick Notes
4. **Quick Access:** Pin Butler to startup untuk auto-run
5. **Backup:** Copy `src/config/` folder untuk backup data

---

## 📱 System Requirements

- **OS:** Windows 10+, Linux (Ubuntu/Debian), macOS
- **Python:** 3.11+
- **RAM:** 100MB minimum
- **Dependencies:** customtkinter, keyboard, pystray, pillow, psutil

---

## 🔗 Useful Commands

```bash
# Install dependencies
pip install -r requirements.txt

# Run main app
cd src && python butler.py

# Test dashboard only
python test_dashboard.py

# Check Python version
python --version
```

---

## ⚙️ Feature Status

| Feature | Status |
|---------|--------|
| System Tray | ✅ |
| Hotkey Listener | ✅ |
| Quick Menu | ✅ |
| Settings GUI | ✅ |
| Dashboard | ✅ |
| System Monitor | ✅ |
| Quick Notes | ✅ |
| Todo List | ✅ |
| Dark/Light Mode | ✅ |
| Command Palette | 🔜 Coming Soon |
| Plugin System | 🔜 Coming Soon |

---

**Quick Start:** Run `python src/butler.py` → Klik kanan tray → Toggle Dashboard!

🎉 Enjoy Butler Dashboard!
