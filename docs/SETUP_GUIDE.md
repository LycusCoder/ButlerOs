# 🚀 Butler Dashboard - Setup Guide

## ✨ Fitur Baru yang Sudah Diimplementasikan

### 1. **Butler Dashboard (HUD)** 🖥️
Widget proaktif semi-permanen dengan:
- **System Monitor realtime** (CPU, RAM, top 3 processes)
- **Quick Notes** dengan auto-save
- **Todo List** dengan time tracking (start time + deadline)
- **Dark/Light Mode** toggle
- **Draggable, Resizable, Fullscreen** support

### 2. **Modern UI/UX** 🎨
- Custom title bar dengan window controls
- AtlasOS-inspired minimalist design
- Smooth animations dan transitions
- Responsive layout

### 3. **Smart Features** 🧠
- Update interval Task Manager style (1 detik)
- Auto-save notes pada setiap keystroke
- Todo completion tracking
- Top processes monitoring

---

## 📋 Prerequisites

### Windows
```bash
# Python 3.11+ required
python --version

# Install dependencies
pip install -r requirements.txt
```

### Linux/macOS
```bash
# Python 3.11+ required
python3 --version

# Install Tkinter (jika belum ada)
# Ubuntu/Debian:
sudo apt-get install python3-tk

# macOS (via Homebrew):
brew install python-tk

# Install dependencies
pip install -r requirements.txt
```

---

## 🏃 Cara Menjalankan

### Method 1: Via Main App (Recommended)

```bash
cd src
python butler.py
```

Aplikasi akan:
1. ✅ Berjalan di background (system tray)
2. ✅ Hotkey `Ctrl+Alt+M` aktif untuk quick menu
3. ✅ Klik kanan tray icon → "Toggle Dashboard" untuk buka dashboard

### Method 2: Test Dashboard Standalone

```bash
python test_dashboard.py
```

Ini akan langsung buka dashboard tanpa tray icon, cocok untuk testing.

---

## 🎯 Cara Menggunakan Dashboard

### 1. **Buka Dashboard**
- Klik kanan icon Butler di system tray
- Pilih "Toggle Dashboard"
- Dashboard akan muncul di tengah screen

### 2. **Window Controls**
- **Drag:** Klik dan drag title bar untuk pindah posisi
- **Minimize:** Klik tombol `─`
- **Maximize/Fullscreen:** Klik tombol `□` (toggle)
- **Theme Toggle:** Klik `☀️` atau `🌙` untuk ganti mode
- **Close:** Klik `✕`

### 3. **System Monitor**
Monitoring realtime:
- CPU Usage dengan progress bar
- RAM Usage dengan progress bar
- Top 3 processes yang paling banyak makan RAM
- Update setiap 1 detik (efficient)

### 4. **Quick Notes**
- Langsung ketik di textbox
- Auto-save pada setiap keystroke
- Tersimpan di: `src/config/notes.txt`
- Status "Auto-saved" muncul setiap kali save

### 5. **Todo List**
**Menambah Task:**
1. Klik tombol `+ Add Task`
2. Isi:
   - Task Name (wajib)
   - Start Time (format: `YYYY-MM-DD HH:MM`)
   - Deadline (format: `YYYY-MM-DD HH:MM`)
3. Klik "Save Task"

**Manage Tasks:**
- ✅ **Check/Uncheck:** Klik checkbox untuk mark as done
- 🗑️ **Delete:** Klik tombol sampah untuk hapus task

**Data Location:** `src/config/todos.json`

---

## 📁 File Structure

```
/app/
├── src/
│   ├── butler.py              # Main entry point
│   ├── dashboard_window.py    # Dashboard GUI (NEW!)
│   ├── quick_menu.py          # Hotkey popup menu
│   ├── settings_window.py     # Settings GUI
│   ├── utils/
│   │   └── system_tray.py     # System tray handler (UPDATED)
│   └── config/
│       ├── config.json        # Quick apps config
│       ├── todos.json         # Todo list data (NEW!)
│       └── notes.txt          # Quick notes data (NEW!)
├── requirements.txt           # Python dependencies (UPDATED)
├── test_dashboard.py          # Standalone dashboard test (NEW!)
└── README.md                  # Main documentation (UPDATED)
```

---

## 🔧 Troubleshooting

### Issue: Hotkey tidak berfungsi
**Solution:** 
- Windows: Run sebagai Administrator
- Linux: Pastikan user punya permission untuk keyboard event

### Issue: Icon tidak muncul di system tray
**Solution:**
- Pastikan file `src/assets/ico/butler.ico` ada
- Check system tray settings (Windows: bisa tersembunyi)

### Issue: Dashboard tidak muncul
**Solution:**
```bash
# Test standalone
python test_dashboard.py

# Jika error tentang Tkinter:
# Ubuntu/Debian:
sudo apt-get install python3-tk
```

### Issue: System monitor tidak update
**Solution:**
- Pastikan `psutil` terinstall: `pip install psutil`
- Check console untuk error messages

---

## 🎨 Customization

### Mengubah Update Interval
Edit `dashboard_window.py`, line ~415:
```python
# Default: 1000ms (1 detik)
self.after(1000, self.update_system_stats)

# Contoh: 2 detik
self.after(2000, self.update_system_stats)
```

### Mengubah Ukuran Dashboard Default
Edit `dashboard_window.py`, line ~13-16:
```python
width = 800   # Ubah sesuai keinginan
height = 600  # Ubah sesuai keinginan
```

### Mengubah Format Todos
Edit `src/config/todos.json`:
```json
{
  "todos": [
    {
      "task": "Nama task",
      "done": false,
      "start_time": "2025-01-15 10:00",
      "deadline": "2025-01-20 18:00"
    }
  ]
}
```

---

## 🚦 Status Implementasi

### ✅ Phase 1: Butler Dashboard - COMPLETE
- [x] Dashboard window dengan custom title bar
- [x] System monitor (CPU, RAM, processes)
- [x] Quick notes dengan auto-save
- [x] Todo list dengan time tracking
- [x] Dark/Light mode toggle
- [x] Draggable, resizable, fullscreen
- [x] System tray integration
- [x] Modern AtlasOS-inspired design

### 🔮 Future Enhancements (Phase 2 & 3)
- [ ] Command Palette (upgrade quick_menu.py dengan search bar)
- [ ] Plugin System (extensible architecture)
- [ ] Customizable themes
- [ ] More system stats (disk, network, temperature)
- [ ] Cloud sync untuk notes & todos

---

## 🤝 Support

Untuk questions atau issues:
1. Check troubleshooting section di atas
2. Review README.md untuk detailed documentation
3. Check console output untuk error messages

---

**Made with ❤️ by Lycus & Lycus**

Selamat mencoba Butler Dashboard! 🎉
