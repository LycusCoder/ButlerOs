# 📝 Changelog - Butler App

## [v2.0.0] - Butler Dashboard Release 🎉

### 🎯 Major Features Added

#### 1. Butler Dashboard (HUD)
**File:** `src/dashboard_window.py` (NEW)

Proactive widget dengan fitur lengkap:
- **System Monitor:**
  - Real-time CPU usage (%)
  - Real-time RAM usage (%)
  - Top 3 memory-consuming processes
  - Update interval: 1 second (Task Manager style)
  - Visual progress bars untuk CPU & RAM

- **Quick Notes:**
  - Auto-save notepad
  - Keystroke-level auto-saving
  - Persisted to `src/config/notes.txt`
  - Save status indicator

- **Todo List with Time Tracking:**
  - Task name
  - Start time (YYYY-MM-DD HH:MM)
  - Deadline (YYYY-MM-DD HH:MM)
  - Completion checkbox
  - Delete functionality
  - Persisted to `src/config/todos.json`

- **Window Features:**
  - Custom title bar (frameless design)
  - Drag to move
  - Minimize button
  - Maximize/Fullscreen toggle
  - Close button
  - Dark/Light mode toggle (☀️/🌙)
  - Resizable window
  - Always on top (configurable)
  - Centered on first launch

- **Design:**
  - Modern AtlasOS-inspired UI
  - Minimalist aesthetic
  - Smooth transitions
  - Responsive layout
  - Scrollable content area

#### 2. System Tray Enhancement
**File:** `src/utils/system_tray.py` (UPDATED)

- Added "Toggle Dashboard" menu item
- Opens/closes dashboard on click
- Integrated with main app state

#### 3. Main App Integration
**File:** `src/butler.py` (UPDATED)

- Added dashboard state management
- `toggle_dashboard()` method
- Handles dashboard lifecycle
- Prevents duplicate instances

#### 4. Configuration Files
**Files:** (NEW)
- `src/config/todos.json` - Todo list storage
- `src/config/notes.txt` - Quick notes storage

Sample data included for immediate testing.

#### 5. Testing & Documentation
**Files:** (NEW)
- `test_dashboard.py` - Standalone dashboard test
- `SETUP_GUIDE.md` - Comprehensive setup & usage guide
- `CHANGELOG.md` - This file

**Files:** (UPDATED)
- `README.md` - Updated with all new features
- `requirements.txt` - Added `psutil` dependency

---

## [v1.0.0] - Initial Release

### Features
- System tray integration
- Hotkey listener (`Ctrl+Alt+M`)
- Quick menu popup
- Settings window
- Dynamic app configuration
- Dark mode UI

### Files
- `src/butler.py`
- `src/quick_menu.py`
- `src/settings_window.py`
- `src/utils/system_tray.py`
- `src/config/config.json`

---

## 📊 Statistics

### Code Changes (v1.0.0 → v2.0.0)
- **New Files:** 5
  - dashboard_window.py (~420 lines)
  - todos.json
  - notes.txt
  - test_dashboard.py
  - SETUP_GUIDE.md
  
- **Modified Files:** 3
  - butler.py (+20 lines)
  - system_tray.py (+10 lines)
  - README.md (+80 lines)

- **New Dependencies:** 1
  - psutil (system monitoring)

### Features Count
- **v1.0.0:** 6 features
- **v2.0.0:** 15+ features
- **Growth:** 250% feature increase

---

## 🔮 Roadmap (Future Versions)

### v2.1.0 (Planned)
- Command Palette with search
- Keyboard shortcuts for dashboard
- Customizable update intervals

### v2.2.0 (Planned)
- Plugin system architecture
- Custom themes support
- Export/import todos

### v3.0.0 (Planned)
- Cloud sync for notes & todos
- Multi-monitor support
- Advanced system stats (disk, network, temp)
- Widget customization

---

## 🐛 Bug Fixes

### v2.0.0
- None (initial dashboard release)

---

## ⚠️ Breaking Changes

### v2.0.0
- None (backward compatible)
- All v1.0.0 features retained

---

## 🙏 Credits

- **Original Concept:** Lycus
- **Implementation:** Lycus Agent
- **Inspired by:** AtlasOS, Spotlight (macOS), PowerToys Run (Windows)

---

**Last Updated:** 2025-01-15
