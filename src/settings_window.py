import customtkinter as ctk
import json
import os
from tkinter import messagebox

class SettingsWindow(ctk.CTkToplevel):
    def __init__(self):
        super().__init__()
        
        self.title("Butler Settings")
        self.geometry("500x600")
        self.attributes("-topmost", True)
        self.config_file = os.path.join(os.path.dirname(__file__), "config", "config.json")
        
        # --- Panel Kiri (List Aplikasi) ---
        self.left_frame = ctk.CTkFrame(self, width=200)
        self.left_frame.pack(side="left", fill="y", padx=10, pady=10)
        
        self.label_list = ctk.CTkLabel(self.left_frame, text="Quick Apps", font=ctk.CTkFont(size=16))
        self.label_list.pack(pady=10)
        
        self.scroll_frame = ctk.CTkScrollableFrame(self.left_frame, width=180)
        self.scroll_frame.pack(fill="both", expand=True)

        # --- Panel Kanan (Form Edit/Tambah) ---
        self.right_frame = ctk.CTkFrame(self)
        self.right_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)
        
        self.label_form = ctk.CTkLabel(self.right_frame, text="Add/Edit App", font=ctk.CTkFont(size=16))
        self.label_form.pack(pady=10)
        
        self.entry_name = ctk.CTkEntry(self.right_frame, placeholder_text="Nama Tombol")
        self.entry_name.pack(pady=10, padx=10, fill="x")
        
        self.entry_path = ctk.CTkEntry(self.right_frame, placeholder_text="Perintah/Path")
        self.entry_path.pack(pady=10, padx=10, fill="x")
        
        self.btn_add = ctk.CTkButton(self.right_frame, text="Add New App", command=self.add_app)
        self.btn_add.pack(pady=20, padx=10, fill="x")
        
        self.load_config()

    def load_config(self):
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()
            
        try:
            with open(self.config_file, "r") as f:
                self.config = json.load(f)
            self.apps = self.config.get("quick_apps", [])
        except FileNotFoundError:
            self.config = {"quick_apps": []}
            self.apps = []
        
        for i, app in enumerate(self.apps):
            frame = ctk.CTkFrame(self.scroll_frame)
            label = ctk.CTkLabel(frame, text=app['name'], width=100)
            label.pack(side="left", padx=5)
            
            btn_del = ctk.CTkButton(
                frame, 
                text="X", 
                command=lambda index=i: self.delete_app(index),
                width=30, fg_color="red"
            )
            btn_del.pack(side="right")
            
            frame.pack(fill="x", pady=5)
            
    def save_config(self):
        with open(self.config_file, "w") as f:
            json.dump(self.config, f, indent=2)
        self.load_config()

    def add_app(self):
        name = self.entry_name.get()
        path = self.entry_path.get()
        
        if not name or not path:
            messagebox.showerror("Error", "Nama dan Path tidak boleh kosong!")
            return
            
        new_app = {"name": name, "path": path}
        self.config["quick_apps"].append(new_app)
        
        self.save_config()
        
        self.entry_name.delete(0, "end")
        self.entry_path.delete(0, "end")

    def delete_app(self, index):
        try:
            self.config["quick_apps"].pop(index)
            self.save_config()
        except IndexError:
            pass