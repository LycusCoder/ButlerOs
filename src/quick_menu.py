import customtkinter as ctk
import json
import os
import subprocess

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class CommandPalette(ctk.CTkToplevel):
    def __init__(self, root):
        super().__init__(root)
        
        # Window configuration
        self.title("Command Palette")
        self.geometry("600x400")
        self.attributes("-topmost", True)
        self.attributes("-toolwindow", True)
        self.resizable(False, False)
        self.focus()
        
        # State management
        self.all_apps = []
        self.filtered_apps = []
        self.selected_index = 0
        self.result_widgets = []
        
        # Load config
        self.load_config()
        
        # Build UI
        self.setup_ui()
        
        # Setup keyboard bindings
        self.setup_bindings()
        
        # Initial display
        self.filter_commands()
        
    def load_config(self):
        """Load apps from config.json"""
        config_path = os.path.join(os.path.dirname(__file__), "config", "config.json")
        try:
            with open(config_path, "r") as f:
                config = json.load(f)
            self.all_apps = config.get("quick_apps", [])
        except FileNotFoundError:
            self.all_apps = []
    
    def get_app_icon(self, app_name, app_path):
        """Auto-detect emoji icon based on app name/path"""
        name_lower = app_name.lower()
        path_lower = app_path.lower()
        
        # Browser icons
        if any(x in name_lower or x in path_lower for x in ["chrome", "browser", "firefox", "edge"]):
            return "🌐"
        # Code editors
        elif any(x in name_lower or x in path_lower for x in ["vscode", "code", "vs code", "sublime", "atom", "editor"]):
            return "💻"
        # File explorers
        elif any(x in name_lower or x in path_lower for x in ["explorer", "folder", "file", "finder"]):
            return "📁"
        # Terminal/Command
        elif any(x in name_lower or x in path_lower for x in ["cmd", "terminal", "powershell", "bash", "shell"]):
            return "⚡"
        # Music/Media
        elif any(x in name_lower or x in path_lower for x in ["spotify", "music", "media", "vlc", "player"]):
            return "🎵"
        # Communication
        elif any(x in name_lower or x in path_lower for x in ["discord", "slack", "teams", "zoom", "chat"]):
            return "💬"
        # Default
        else:
            return "🚀"
    
    def setup_ui(self):
        """Build the UI components"""
        # Main container with padding
        main_container = ctk.CTkFrame(self, fg_color="transparent")
        main_container.pack(fill="both", expand=True, padx=20, pady=20)
        
        # === TOP SECTION: Search Bar ===
        search_container = ctk.CTkFrame(main_container, fg_color="transparent")
        search_container.pack(fill="x", pady=(0, 15))
        
        # Search icon/label
        search_icon = ctk.CTkLabel(
            search_container, 
            text="🔍", 
            font=("Segoe UI Emoji", 20)
        )
        search_icon.pack(side="left", padx=(0, 10))
        
        # Search entry
        self.search_entry = ctk.CTkEntry(
            search_container,
            placeholder_text="Ketik untuk mencari aplikasi...",
            height=45,
            font=("Segoe UI", 16),
            border_width=2,
            corner_radius=10
        )
        self.search_entry.pack(side="left", fill="x", expand=True)
        self.search_entry.focus()
        
        # === MIDDLE SECTION: Results Container ===
        # Result count label
        self.result_count_label = ctk.CTkLabel(
            main_container,
            text="",
            font=("Segoe UI", 11),
            text_color="#888888"
        )
        self.result_count_label.pack(anchor="w", pady=(0, 8))
        
        # Scrollable results frame
        self.results_frame = ctk.CTkScrollableFrame(
            main_container,
            fg_color="#1a1a1a",
            corner_radius=10,
            scrollbar_button_color="#3d3d3d",
            scrollbar_button_hover_color="#4d4d4d"
        )
        self.results_frame.pack(fill="both", expand=True, pady=(0, 10))
        
        # === BOTTOM SECTION: Keyboard Hints ===
        hints_frame = ctk.CTkFrame(main_container, fg_color="transparent")
        hints_frame.pack(fill="x")
        
        hints_text = "↑↓ Navigate  •  ↵ Execute  •  Esc Close"
        hints_label = ctk.CTkLabel(
            hints_frame,
            text=hints_text,
            font=("Segoe UI", 10),
            text_color="#666666"
        )
        hints_label.pack()
    
    def setup_bindings(self):
        """Setup keyboard event bindings"""
        # Search input triggers filtering
        self.search_entry.bind("<KeyRelease>", lambda e: self.filter_commands())
        
        # Enter to execute selected
        self.search_entry.bind("<Return>", lambda e: self.execute_selected())
        
        # Arrow keys for navigation
        self.search_entry.bind("<Down>", lambda e: self.navigate_down())
        self.search_entry.bind("<Up>", lambda e: self.navigate_up())
        
        # Escape to close
        self.bind("<Escape>", lambda e: self.destroy())
        
        # Auto-close on focus out
        self.bind("<FocusOut>", self.on_focus_out)
    
    def filter_commands(self):
        """Filter apps based on search input"""
        query = self.search_entry.get().strip().lower()
        
        if not query:
            # Show all apps if search is empty
            self.filtered_apps = self.all_apps.copy()
        else:
            # Filter by name (case-insensitive, partial match)
            self.filtered_apps = [
                app for app in self.all_apps
                if query in app["name"].lower()
            ]
        
        # Reset selection to first item
        self.selected_index = 0
        
        # Update display
        self.update_results_display()
    
    def update_results_display(self):
        """Re-render the filtered results"""
        # Clear existing widgets
        for widget in self.result_widgets:
            widget.destroy()
        self.result_widgets.clear()
        
        # Update result count
        count = len(self.filtered_apps)
        if count == 0:
            self.result_count_label.configure(text="❌ Tidak ada hasil")
        elif count == 1:
            self.result_count_label.configure(text="✓ 1 hasil ditemukan")
        else:
            self.result_count_label.configure(text=f"✓ {count} hasil ditemukan")
        
        # Display results or empty state
        if not self.filtered_apps:
            self.show_empty_state()
        else:
            for idx, app in enumerate(self.filtered_apps):
                self.create_result_item(idx, app)
    
    def show_empty_state(self):
        """Show friendly empty state"""
        empty_frame = ctk.CTkFrame(self.results_frame, fg_color="transparent")
        empty_frame.pack(fill="both", expand=True, pady=50)
        
        empty_label = ctk.CTkLabel(
            empty_frame,
            text="🔍 Tidak ada aplikasi yang cocok\nCoba kata kunci lain",
            font=("Segoe UI", 14),
            text_color="#666666",
            justify="center"
        )
        empty_label.pack()
        
        self.result_widgets.append(empty_frame)
    
    def create_result_item(self, idx, app):
        """Create a single result item widget"""
        is_selected = (idx == self.selected_index)
        
        # Result item frame
        item_frame = ctk.CTkFrame(
            self.results_frame,
            fg_color="#2d2d2d" if is_selected else "transparent",
            corner_radius=8,
            border_width=2 if is_selected else 0,
            border_color="#1f6feb" if is_selected else "transparent",
            cursor="hand2"
        )
        item_frame.pack(fill="x", pady=4, padx=2)
        
        # Content container
        content_frame = ctk.CTkFrame(item_frame, fg_color="transparent")
        content_frame.pack(fill="x", padx=15, pady=12)
        
        # Icon
        icon = self.get_app_icon(app["name"], app["path"])
        icon_label = ctk.CTkLabel(
            content_frame,
            text=icon,
            font=("Segoe UI Emoji", 24),
            width=40
        )
        icon_label.pack(side="left", padx=(0, 15))
        
        # Text container
        text_container = ctk.CTkFrame(content_frame, fg_color="transparent")
        text_container.pack(side="left", fill="x", expand=True)
        
        # App name
        name_label = ctk.CTkLabel(
            text_container,
            text=app["name"],
            font=("Segoe UI", 14, "bold"),
            anchor="w",
            text_color="#ffffff" if is_selected else "#e0e0e0"
        )
        name_label.pack(anchor="w")
        
        # App path (subtle)
        path_label = ctk.CTkLabel(
            text_container,
            text=app["path"],
            font=("Segoe UI", 10),
            anchor="w",
            text_color="#888888"
        )
        path_label.pack(anchor="w")
        
        # Hover effects
        def on_enter(e):
            if idx != self.selected_index:
                item_frame.configure(fg_color="#252525")
        
        def on_leave(e):
            if idx != self.selected_index:
                item_frame.configure(fg_color="transparent")
        
        def on_click(e):
            self.selected_index = idx
            self.execute_selected()
        
        # Bind hover and click events
        for widget in [item_frame, content_frame, icon_label, text_container, name_label, path_label]:
            widget.bind("<Enter>", on_enter)
            widget.bind("<Leave>", on_leave)
            widget.bind("<Button-1>", on_click)
        
        self.result_widgets.append(item_frame)
    
    def navigate_down(self):
        """Navigate to next result"""
        if self.filtered_apps and self.selected_index < len(self.filtered_apps) - 1:
            self.selected_index += 1
            self.update_results_display()
            # Scroll to selected item
            self.scroll_to_selected()
    
    def navigate_up(self):
        """Navigate to previous result"""
        if self.filtered_apps and self.selected_index > 0:
            self.selected_index -= 1
            self.update_results_display()
            # Scroll to selected item
            self.scroll_to_selected()
    
    def scroll_to_selected(self):
        """Auto-scroll to keep selected item visible"""
        if 0 <= self.selected_index < len(self.result_widgets):
            selected_widget = self.result_widgets[self.selected_index]
            # Force the scrollable frame to show the selected widget
            self.results_frame._parent_canvas.yview_moveto(
                self.selected_index / max(len(self.filtered_apps), 1)
            )
    
    def execute_selected(self):
        """Execute the selected command"""
        if not self.filtered_apps:
            return
        
        if 0 <= self.selected_index < len(self.filtered_apps):
            app = self.filtered_apps[self.selected_index]
            self.run_command(app["path"], app["name"])
    
    def run_command(self, command, name):
        """Execute the command and close palette"""
        print(f"🚀 Menjalankan: {name} → {command}")
        try:
            subprocess.Popen(command, shell=True)
            print(f"✅ Berhasil menjalankan: {name}")
        except Exception as e:
            print(f"❌ Error menjalankan {name}: {e}")
        
        # Close the palette
        self.destroy()
    
    def on_focus_out(self, event):
        """Auto-close when focus is lost"""
        # Delay slightly to allow button clicks
        self.after(100, self.destroy)


# Backward compatibility: alias old class name
QuickMenu = CommandPalette
