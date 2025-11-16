import threading
import keyboard
import json
import os
import sys
import customtkinter as ctk
from quick_menu import QuickMenu
from utils.system_tray import SystemTray

class ButlerApp:
    def __init__(self):
        self.current_quick_menu = None
        self.current_settings = None
        self.listener_thread = None
        self.tray_thread = None
        self.root = None
        
    def load_hotkey(self):
        config_path = os.path.join(os.path.dirname(__file__), "config", "config.json")
        try:
            with open(config_path, "r") as f:
                config = json.load(f)
            return config.get("hotkey", "ctrl+alt+m")
        except FileNotFoundError:
            return "ctrl+alt+m"

    def show_quick_menu(self):
        print("Hotkey terdeteksi! Membuka menu...")
        try:
            # Jangan blok, buka di thread terpisah
            if self.current_quick_menu is None or not self.current_quick_menu.winfo_exists():
                self.current_quick_menu = QuickMenu(self.root)
        except Exception as e:
            print(f"Error membuka menu: {e}")

    def start_listener(self):
        hotkey = self.load_hotkey()
        print(f"Listener aktif. Hotkey: {hotkey}")
        keyboard.add_hotkey(hotkey, self.show_quick_menu)
        keyboard.wait()

    def start_tray(self):
        tray = SystemTray(self)
        tray.start()

    def run(self):
        print("🚀 Lycus Butler App sedang berjalan...")
        
        # Bikin root window (hidden)
        self.root = ctk.CTk()
        self.root.withdraw()  # Hide it
        self.root.attributes("-topmost", False)
        
        # Start listener di thread terpisah
        self.listener_thread = threading.Thread(target=self.start_listener, daemon=True)
        self.listener_thread.start()
        
        # Start tray di thread terpisah juga
        self.tray_thread = threading.Thread(target=self.start_tray, daemon=True)
        self.tray_thread.start()
        
        # Jalankan root mainloop di thread utama
        # Ini biar GUI bisa responsif
        self.root.mainloop()

if __name__ == "__main__":
    app = ButlerApp()
    app.run()