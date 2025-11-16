# Lycus Butler App

Aplikasi sistem tray yang powerful dan modern untuk quick access ke aplikasi favorit lo. Built dengan Python, customtkinter, dan pystray.

## 🎯 Features

- ✅ **System Tray Integration** - Aplikasi berjalan di background dengan icon di system tray
- ✅ **Hotkey Listener** - Tekan `Ctrl+Alt+M` untuk buka quick menu
- ✅ **Dynamic Quick Menu** - Popup menu yang di-generate otomatis dari config.json
- ✅ **Settings GUI** - Edit, tambah, atau hapus aplikasi tanpa edit file manual
- ✅ **Butler Dashboard (HUD)** - Widget proaktif dengan system monitor, notes, dan todo list
- ✅ **System Monitor** - Real-time CPU, RAM, dan top processes monitoring
- ✅ **Quick Notes** - Auto-save notepad untuk catatan cepat
- ✅ **Todo List with Time Tracking** - Task management dengan start time dan deadline
- ✅ **Dark/Light Mode** - Toggle theme sesuai preferensi
- ✅ **Responsive & Draggable** - Window bisa di-resize, drag, minimize, maximize, dan fullscreen
- ✅ **Configurable** - Semua setting disimpan di `config.json`

## 📦 Tech Stack

- **Python 3.11+**
- **customtkinter** - Modern GUI library
- **keyboard** - Hotkey listener
- **pystray** - System tray icon
- **pillow** - Image processing
- **psutil** - System monitoring (CPU, RAM, processes)

## 🏗️ Project Structure

```
lycus-butler-app/
├── src/
│   ├── butler.py              # Main app - entry point
│   ├── dashboard_window.py    # Butler Dashboard (HUD) GUI
│   ├── quick_menu.py          # Dynamic popup menu GUI
│   ├── settings_window.py     # Settings window GUI
│   ├── assets/
│   │   ├── ico/
│   │   │   └── butler.ico     # Tray icon
│   │   └── png/
│   ├── utils/
│   │   ├── __init__.py
│   │   └── system_tray.py     # System tray handler
│   └── config/
│       ├── __init__.py
│       ├── config.json        # App configuration
│       ├── todos.json         # Todo list data
│       └── notes.txt          # Quick notes data
├── requirements.txt
├── README.md
└── .github/
    └── agents/
        └── Lycus.agent.md     # Agent instructions
```

## ⚙️ Installation

### 1. Clone Repository
```bash
git clone https://github.com/LycusCoder/ButlerOs.git
cd lycus-butler-app
```

### 2. Create Virtual Environment (Optional but recommended)
```bash
python -m venv .venv
# On Windows:
.venv\Scripts\activate
# On macOS/Linux:
source .venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

## 🚀 Usage

### Jalankan Aplikasi
```bash
cd src
python butler.py
```

Aplikasi akan:
1. Minimize ke system tray
2. Listener aktif dengan hotkey `Ctrl+Alt+M`

### Hotkeys

| Hotkey | Action |
|--------|--------|
| `Ctrl+Alt+M` | Buka Quick Menu Popup |
| `Esc` | Close Quick Menu (atau klik di luar) |

### System Tray Menu

Klik kanan icon di system tray:
- **Toggle Dashboard** - Buka/tutup Butler Dashboard (HUD)
- **Settings** - Buka settings window untuk manage apps
- **Exit** - Keluar aplikasi

### Butler Dashboard Features

**System Monitor (Task Manager Style):**
- Real-time CPU usage dengan progress bar
- Real-time RAM usage dengan progress bar
- Top 3 processes yang paling banyak makan RAM
- Update interval: 1 detik (efficient monitoring)

**Quick Notes:**
- Auto-save notepad
- Setiap keystroke otomatis tersimpan
- File location: `src/config/notes.txt`

**Todo List:**
- Task management dengan time tracking
- Field: Task name, Start time, Deadline
- Checkbox untuk mark sebagai done
- Delete button per task
- Format JSON: `src/config/todos.json`

**Window Controls:**
- 🌙/☀️ Toggle Dark/Light mode
- Minimize, Maximize, Fullscreen support
- Draggable dari title bar
- Resizable window
- Always on top (optional)

## 🔧 Configuration

File `src/config/config.json`:

```json
{
  "hotkey": "ctrl+alt+m",
  "quick_apps": [
    {
      "name": "Buka Chrome",
      "path": "chrome"
    },
    {
      "name": "Folder Proyek",
      "path": "explorer D:\\Projects"
    },
    {
      "name": "VS Code",
      "path": "code"
    }
  ]
}
```

### Menambah Aplikasi

**Via Settings GUI (Recommended):**
1. Klik Settings di tray
2. Isi "Nama Tombol" dan "Perintah/Path"
3. Klik "Add New App"

**Via Manual Edit config.json:**
Tambah object baru ke array `quick_apps` dengan `name` dan `path`.

### Managing Todos

**Via Dashboard GUI (Recommended):**
1. Buka Dashboard dari tray menu
2. Klik "+ Add Task" di section Todo List
3. Isi task name, start time, dan deadline
4. Klik "Save Task"

**Via Manual Edit todos.json:**
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

## 🛠️ Architecture

### butler.py (Main App)
- Initialize GUI root window (hidden)
- Start hotkey listener di thread terpisah
- Start system tray di thread terpisah
- Main thread handle tkinter event loop

### quick_menu.py (Quick Menu)
- CTkToplevel window yang auto-generated dari config
- Auto-close ketika klik tombol atau klik di luar
- Non-blocking - listener tetap aktif

### settings_window.py (Settings)
- Add/Edit/Delete apps
- Save changes ke config.json
- Scrollable list dengan delete button per item

### system_tray.py (System Tray Handler)
- Icon management
- Menu items (Settings, Exit)
- Icon path dari `assets/ico/butler.ico`

## 📝 Notes

- **Run as Admin** jika hotkey gak jalan (Windows limitation)
- **Icon file** (`butler.ico`) harus ada di `src/assets/ico/`
- **Threading** - Listener dan Tray berjalan async, gak block GUI

## 🤝 Contributing

Contributions welcome! Feel free untuk:
- Report issues
- Suggest features
- Submit pull requests

## 📄 License

MIT License - feel free to use for personal or commercial projects

---

**Made with ❤️ by Lycus**
