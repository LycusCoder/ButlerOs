# Lycus Butler App

Aplikasi sistem tray yang powerful dan modern untuk quick access ke aplikasi favorit lo. Built dengan Python, customtkinter, dan pystray.

## 🎯 Features

- ✅ **System Tray Integration** - Aplikasi berjalan di background dengan icon di system tray
- ✅ **Hotkey Listener** - Tekan `Ctrl+Alt+M` untuk buka quick menu
- ✅ **Dynamic Quick Menu** - Popup menu yang di-generate otomatis dari config.json
- ✅ **Settings GUI** - Edit, tambah, atau hapus aplikasi tanpa edit file manual
- ✅ **Dark Mode** - GUI modern dengan dark theme
- ✅ **Configurable** - Semua setting disimpan di `config.json`

## 📦 Tech Stack

- **Python 3.11+**
- **customtkinter** - Modern GUI library
- **keyboard** - Hotkey listener
- **pystray** - System tray icon
- **pillow** - Image processing

## 🏗️ Project Structure

```
lycus-butler-app/
├── src/
│   ├── butler.py              # Main app - entry point
│   ├── quick_menu.py          # Dynamic popup menu GUI
│   ├── settings_window.py      # Settings window GUI
│   ├── assets/
│   │   ├── ico/
│   │   │   └── butler.ico      # Tray icon
│   │   └── png/
│   ├── utils/
│   │   ├── __init__.py
│   │   └── system_tray.py      # System tray handler
│   └── config/
│       ├── __init__.py
│       └── config.json         # App configuration
├── requirements.txt
├── README.md
└── .github/
    └── agents/
        └── Lycus.agent.md      # Agent instructions
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
- **Settings** - Buka settings window untuk manage apps
- **Exit** - Keluar aplikasi

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
