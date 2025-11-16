import customtkinter as ctk
import json
import os
import subprocess

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class QuickMenu(ctk.CTkToplevel):
    def __init__(self, root):
        super().__init__(root)
        
        self.title("Quick Menu")
        self.attributes("-topmost", True)
        self.attributes("-toolwindow", True)
        # Jangan pake grab_set(), bikin blocking
        # self.grab_set()
        self.focus()
        
        # Baca config
        config_path = os.path.join(os.path.dirname(__file__), "config", "config.json")
        try:
            with open(config_path, "r") as f:
                config = json.load(f)
            app_list = config.get("quick_apps", [])
        except FileNotFoundError:
            app_list = []
        
        # Hitung tinggi jendela
        window_height = (len(app_list) * 50) + 40
        self.geometry(f"300x{window_height}")
        
        # Bikin tombol dinamis
        if not app_list:
            label = ctk.CTkLabel(self, text="Belum ada app di config.json")
            label.pack(pady=20, padx=20)
        else:
            for app in app_list:
                btn = ctk.CTkButton(
                    self, 
                    text=app["name"], 
                    command=lambda p=app["path"]: self.run_command(p)
                )
                btn.pack(pady=8, padx=20, fill="x")

        # Auto-close kalo klik di luar
        self.bind("<FocusOut>", self.on_focus_out)
        # Close juga kalo tekan Escape
        self.bind("<Escape>", lambda e: self.destroy())

    def run_command(self, command):
        print(f"Menjalankan: {command}")
        try:
            subprocess.Popen(command, shell=True)
        except Exception as e:
            print(f"Error: {e}")
        self.destroy()

    def on_focus_out(self, event):
        # Delay sedikit supaya user bisa lihat
        self.after(100, self.destroy)