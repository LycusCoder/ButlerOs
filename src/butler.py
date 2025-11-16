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
        self.current_dashboard = None
        self.current_sidebar = None
        self.current_overlay = None
        self.listener_thread = None
        self.tray_thread = None
        self.root = None
        self.sidebar_state = "closed"  # closed, animating_in, open, animating_out
        
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

    def toggle_dashboard(self):
        """Toggle dashboard visibility"""
        print("Toggle dashboard...")
        try:
            if self.current_dashboard is None or not self.current_dashboard.winfo_exists():
                # Import here to avoid circular dependency
                from dashboard_window import DashboardWindow
                self.current_dashboard = DashboardWindow(self.root)
                print("Dashboard dibuka!")
            else:
                # If exists, close it
                self.current_dashboard.destroy()
                self.current_dashboard = None
                print("Dashboard ditutup!")
        except Exception as e:
            print(f"Error toggle dashboard: {e}")

    def toggle_sidebar(self):
        """Toggle sidebar with animation"""
        if self.sidebar_state in ("animating_in", "animating_out"):
            return
        
        if self.sidebar_state == "closed":
            self.show_sidebar()
        else:
            self.hide_sidebar()
    
    def show_sidebar(self):
        """Show sidebar with slide-in animation"""
        if self.sidebar_state != "closed":
            return
        
        print("[BUTLER] Opening sidebar...")
        self.sidebar_state = "animating_in"
        
        try:
            # Create overlay
            self.create_overlay()
            
            # Create sidebar
            from sidebar_window import SidebarWindow
            self.current_sidebar = SidebarWindow(self.root, on_close_callback=self.hide_sidebar)
            
            # Slide in
            self.current_sidebar.slide_in(duration_ms=300)
            
            self.sidebar_state = "open"
        except Exception as e:
            print(f"[BUTLER] Error showing sidebar: {e}")
            self.sidebar_state = "closed"
    
    def hide_sidebar(self):
        """Hide sidebar with slide-out animation"""
        if self.sidebar_state != "open":
            return
        
        print("[BUTLER] Closing sidebar...")
        self.sidebar_state = "animating_out"
        
        try:
            if self.current_sidebar and self.current_sidebar.winfo_exists():
                self.current_sidebar.slide_out(duration_ms=300)
                # Delay destroy to allow animation to complete
                self.root.after(300, self.destroy_sidebar)
            
            if self.current_overlay and self.current_overlay.winfo_exists():
                self.current_overlay.destroy()
                self.current_overlay = None
            
            self.sidebar_state = "closed"
        except Exception as e:
            print(f"[BUTLER] Error hiding sidebar: {e}")
            self.sidebar_state = "closed"
    
    def destroy_sidebar(self):
        """Destroy sidebar after animation"""
        try:
            if self.current_sidebar and self.current_sidebar.winfo_exists():
                self.current_sidebar.destroy()
                self.current_sidebar = None
        except Exception as e:
            print(f"[BUTLER] Error destroying sidebar: {e}")
    
    def create_overlay(self):
        """Create dimming overlay"""
        try:
            self.current_overlay = ctk.CTkToplevel(self.root)
            self.current_overlay.attributes("-topmost", True)
            
            screen_width = self.root.winfo_screenwidth()
            screen_height = self.root.winfo_screenheight()
            
            self.current_overlay.geometry(f"{screen_width}x{screen_height}+0+0")
            self.current_overlay.configure(fg_color=("#000000", "#000000"))
            self.current_overlay.attributes("-alpha", 0.3)
            
            # Click overlay to close
            self.current_overlay.bind("<Button-1>", lambda e: self.toggle_sidebar())
            self.current_overlay.bind("<Escape>", lambda e: self.toggle_sidebar())
            
            print("[BUTLER] Overlay created")
        except Exception as e:
            print(f"[BUTLER] Error creating overlay: {e}")

    def start_listener(self):
        hotkey = self.load_hotkey()
        print(f"[LISTENER] Hotkey untuk menu: {hotkey}")
        keyboard.add_hotkey(hotkey, self.show_quick_menu)
        keyboard.add_hotkey("win+s", self.toggle_sidebar)
        print("[LISTENER] Hotkey Win+S untuk sidebar aktif!")
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