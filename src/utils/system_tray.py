from pystray import Icon, MenuItem, Menu
from PIL import Image
import threading
import sys
import os

class SystemTray:
    def __init__(self, app):
        self.app = app
        
        # Load icon dari assets
        icon_path = os.path.join(os.path.dirname(__file__), "..", "assets", "ico", "butler.ico")
        self.image = Image.open(icon_path)
        
        self.icon = Icon(
            "Lycus Butler",
            self.image,
            "Lycus Butler",
            menu=Menu(
                MenuItem("Toggle Dashboard", self.toggle_dashboard),
                MenuItem("Settings", self.open_settings),
                MenuItem("Exit", self.exit_app)
            )
        )

    def start(self):
        self.icon.run(setup=self.setup)

    def setup(self, icon):
        icon.visible = True
        print("System Tray aktif!")

    def toggle_dashboard(self, icon):
        """Toggle dashboard visibility"""
        print("Toggle dashboard...")
        if hasattr(self.app, 'toggle_dashboard'):
            self.app.toggle_dashboard()

    def open_settings(self, icon):
        print("Membuka settings...")
        from settings_window import SettingsWindow
        settings = SettingsWindow()

    def exit_app(self, icon):
        print("Keluar dari aplikasi...")
        icon.stop()
        sys.exit()