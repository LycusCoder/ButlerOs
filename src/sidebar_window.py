import customtkinter as ctk
import psutil
import json
import os
from datetime import datetime
from tkinter import messagebox

class SidebarWindow(ctk.CTkToplevel):
    """Modern Sidebar Widget Center - slide-in from right side"""
    
    def __init__(self, root, on_close_callback=None):
        super().__init__(root)
        
        # Store callback
        self.on_close_callback = on_close_callback
        
        # Window Configuration
        self.title("Butler Sidebar")
        self.attributes("-alpha", 1.0)
        
        # Get screen dimensions
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        
        sidebar_width = 400
        
        # Start from off-screen (right side)
        self.geometry(f"{sidebar_width}x{screen_height}+{screen_width}+0")
        
        # Window attributes
        self.attributes("-topmost", True)
        self.attributes("-toolwindow", False)
        
        # Make window visible
        self.deiconify()
        
        # State variables
        self.is_dark_mode = True
        self.monitoring_active = True
        self.is_animating = False
        self.is_visible = False
        self.config_dir = os.path.join(os.path.dirname(__file__), "config")
        self.notes_file = os.path.join(self.config_dir, "notes.txt")
        self.todos_file = os.path.join(self.config_dir, "todos.json")
        
        self.sidebar_width = sidebar_width
        self.screen_width = screen_width
        self.screen_height = screen_height
        
        # Create UI
        self.create_custom_titlebar()
        self.create_main_content()
        
        # Start monitoring loop
        self.update_system_stats()
        
        # Bind close event
        self.protocol("WM_DELETE_WINDOW", self.on_close)
        
        # Bind Esc to close sidebar
        self.bind("<Escape>", lambda e: self.on_close())
        
        # Close when clicking title bar close button
        self.bind("<Button-1>", self.on_click_handler)
        
    def create_custom_titlebar(self):
        """Custom title bar with controls"""
        self.titlebar = ctk.CTkFrame(self, height=40, corner_radius=0, fg_color="#1a1a1a")
        self.titlebar.pack(fill="x", side="top")
        self.titlebar.pack_propagate(False)
        
        # Title
        self.title_label = ctk.CTkLabel(
            self.titlebar, 
            text="Butler Sidebar",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        self.title_label.pack(side="left", padx=15, pady=10)
        
        # Theme toggle
        self.theme_btn = ctk.CTkButton(
            self.titlebar,
            text="☀️",
            width=40,
            command=self.toggle_theme,
            fg_color="transparent",
            hover_color=("#E0E0E0", "#2B2B2B")
        )
        self.theme_btn.pack(side="right", padx=5, pady=5)
        
        # Close button
        self.close_btn = ctk.CTkButton(
            self.titlebar,
            text="✕",
            width=40,
            command=self.on_close,
            fg_color="transparent",
            hover_color=("#FF5555", "#FF5555")
        )
        self.close_btn.pack(side="right", padx=5, pady=5)
        
    def toggle_theme(self):
        self.is_dark_mode = not self.is_dark_mode
        if self.is_dark_mode:
            ctk.set_appearance_mode("dark")
            self.theme_btn.configure(text="☀️")
        else:
            ctk.set_appearance_mode("light")
            self.theme_btn.configure(text="🌙")
            
    def create_main_content(self):
        """Create main sidebar content"""
        # Main container
        self.main_container = ctk.CTkFrame(self, corner_radius=0)
        self.main_container.pack(fill="both", expand=True, padx=0, pady=0)
        
        # Create scrollable frame
        self.scroll_frame = ctk.CTkScrollableFrame(self.main_container)
        self.scroll_frame.pack(fill="both", expand=True, padx=15, pady=15)
        
        # System Monitor Section
        self.create_system_monitor()
        
        # Quick Notes Section
        self.create_quick_notes()
        
        # Todo List Section
        self.create_todo_list()
        
    def create_system_monitor(self):
        """System monitoring section"""
        monitor_frame = ctk.CTkFrame(self.scroll_frame, corner_radius=10)
        monitor_frame.pack(fill="x", pady=(0, 15))
        
        # Header
        header = ctk.CTkLabel(
            monitor_frame, 
            text="System Monitor",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        header.pack(anchor="w", padx=15, pady=(15, 10))
        
        # CPU Usage
        cpu_frame = ctk.CTkFrame(monitor_frame, corner_radius=8)
        cpu_frame.pack(side="left", fill="both", expand=True, padx=(15, 7), pady=(0, 10))
        
        ctk.CTkLabel(cpu_frame, text="CPU", font=ctk.CTkFont(size=11)).pack(pady=(8, 3))
        self.cpu_label = ctk.CTkLabel(cpu_frame, text="0%", font=ctk.CTkFont(size=18, weight="bold"))
        self.cpu_label.pack(pady=(0, 8))
        self.cpu_bar = ctk.CTkProgressBar(cpu_frame, width=150)
        self.cpu_bar.pack(pady=(0, 8), padx=10)
        self.cpu_bar.set(0)
        
        # RAM Usage
        ram_frame = ctk.CTkFrame(monitor_frame, corner_radius=8)
        ram_frame.pack(side="left", fill="both", expand=True, padx=(7, 15), pady=(0, 10))
        
        ctk.CTkLabel(ram_frame, text="RAM", font=ctk.CTkFont(size=11)).pack(pady=(8, 3))
        self.ram_label = ctk.CTkLabel(ram_frame, text="0%", font=ctk.CTkFont(size=18, weight="bold"))
        self.ram_label.pack(pady=(0, 8))
        self.ram_bar = ctk.CTkProgressBar(ram_frame, width=150)
        self.ram_bar.pack(pady=(0, 8), padx=10)
        self.ram_bar.set(0)
        
        # Top processes
        proc_label = ctk.CTkLabel(
            monitor_frame,
            text="Top Processes",
            font=ctk.CTkFont(size=10, weight="bold"),
            text_color="gray"
        )
        proc_label.pack(anchor="w", padx=15, pady=(10, 5))
        
        self.process_frame = ctk.CTkFrame(monitor_frame, fg_color="transparent")
        self.process_frame.pack(fill="x", padx=15, pady=(0, 15))
        
        self.update_processes()
        
    def create_quick_notes(self):
        """Quick notes section"""
        notes_frame = ctk.CTkFrame(self.scroll_frame, corner_radius=10)
        notes_frame.pack(fill="both", expand=True, pady=(0, 15))
        
        # Header
        header_container = ctk.CTkFrame(notes_frame, fg_color="transparent")
        header_container.pack(fill="x", padx=15, pady=(15, 10))
        
        header = ctk.CTkLabel(
            header_container, 
            text="Quick Notes",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        header.pack(side="left")
        
        self.save_status_label = ctk.CTkLabel(
            header_container,
            text="Auto-saved",
            font=ctk.CTkFont(size=9),
            text_color="gray"
        )
        self.save_status_label.pack(side="right")
        
        # Notes textbox
        self.notes_textbox = ctk.CTkTextbox(
            notes_frame,
            height=100,
            corner_radius=8,
            font=ctk.CTkFont(size=11)
        )
        self.notes_textbox.pack(fill="both", expand=True, padx=15, pady=(0, 15))
        
        self.load_notes()
        self.notes_textbox.bind("<KeyRelease>", self.auto_save_notes)
        
    def create_todo_list(self):
        """Todo list section"""
        todo_frame = ctk.CTkFrame(self.scroll_frame, corner_radius=10)
        todo_frame.pack(fill="both", expand=True, pady=(0, 15))
        
        # Header with Add button
        header_container = ctk.CTkFrame(todo_frame, fg_color="transparent")
        header_container.pack(fill="x", padx=15, pady=(15, 10))
        
        header = ctk.CTkLabel(
            header_container,
            text="Todo List",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        header.pack(side="left")
        
        add_btn = ctk.CTkButton(
            header_container,
            text="+ Add",
            width=60,
            height=25,
            command=self.add_todo_dialog,
            corner_radius=6,
            font=ctk.CTkFont(size=10)
        )
        add_btn.pack(side="right")
        
        # Todo list container
        self.todo_container = ctk.CTkFrame(todo_frame, fg_color="transparent")
        self.todo_container.pack(fill="both", expand=True, padx=15, pady=(0, 15))
        
        self.load_todos()
        
    def load_notes(self):
        """Load notes from file"""
        try:
            if os.path.exists(self.notes_file):
                with open(self.notes_file, "r", encoding="utf-8") as f:
                    notes = f.read()
                self.notes_textbox.delete("1.0", "end")
                self.notes_textbox.insert("1.0", notes)
        except Exception as e:
            print(f"[SIDEBAR] Error loading notes: {e}")
            
    def auto_save_notes(self, event=None):
        """Auto-save notes"""
        try:
            notes = self.notes_textbox.get("1.0", "end-1c")
            os.makedirs(self.config_dir, exist_ok=True)
            with open(self.notes_file, "w", encoding="utf-8") as f:
                f.write(notes)
            self.save_status_label.configure(text="✓ Saved")
            self.after(1500, lambda: self.save_status_label.configure(text="Auto-saved"))
        except Exception as e:
            print(f"[SIDEBAR] Error saving notes: {e}")
            
    def load_todos(self):
        """Load todos from JSON"""
        try:
            if os.path.exists(self.todos_file):
                with open(self.todos_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                self.todos = data.get("todos", [])
            else:
                self.todos = []
        except Exception as e:
            print(f"[SIDEBAR] Error loading todos: {e}")
            self.todos = []
        self.render_todos()
        
    def save_todos(self):
        """Save todos to JSON"""
        try:
            os.makedirs(self.config_dir, exist_ok=True)
            with open(self.todos_file, "w", encoding="utf-8") as f:
                json.dump({"todos": self.todos}, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"[SIDEBAR] Error saving todos: {e}")
            
    def render_todos(self):
        """Render todo list"""
        for widget in self.todo_container.winfo_children():
            widget.destroy()
            
        if not self.todos:
            empty_label = ctk.CTkLabel(
                self.todo_container,
                text="No tasks. Click + Add!",
                font=ctk.CTkFont(size=11),
                text_color="gray"
            )
            empty_label.pack(pady=10)
            return
            
        for i, todo in enumerate(self.todos):
            todo_item = ctk.CTkFrame(self.todo_container, corner_radius=6)
            todo_item.pack(fill="x", pady=3)
            
            checkbox = ctk.CTkCheckBox(
                todo_item,
                text="",
                width=20,
                command=lambda idx=i: self.toggle_todo(idx)
            )
            checkbox.pack(side="left", padx=(5, 8), pady=5)
            if todo.get("done", False):
                checkbox.select()
                
            info_frame = ctk.CTkFrame(todo_item, fg_color="transparent")
            info_frame.pack(side="left", fill="x", expand=True, pady=5)
            
            task_label = ctk.CTkLabel(
                info_frame,
                text=todo.get("task", "Untitled"),
                font=ctk.CTkFont(size=11, weight="bold" if not todo.get("done") else "normal"),
                anchor="w"
            )
            task_label.pack(anchor="w", fill="x")
            
            time_text = f"{todo.get('deadline', 'No deadline')}"
            time_label = ctk.CTkLabel(
                info_frame,
                text=time_text,
                font=ctk.CTkFont(size=9),
                text_color="gray",
                anchor="w"
            )
            time_label.pack(anchor="w", fill="x")
            
            delete_btn = ctk.CTkButton(
                todo_item,
                text="X",
                width=25,
                height=25,
                command=lambda idx=i: self.delete_todo(idx),
                fg_color="transparent",
                hover_color=("#FF5555", "#8B0000"),
                font=ctk.CTkFont(size=9)
            )
            delete_btn.pack(side="right", padx=3)
            
    def toggle_todo(self, index):
        """Toggle todo status"""
        if 0 <= index < len(self.todos):
            self.todos[index]["done"] = not self.todos[index].get("done", False)
            self.save_todos()
            self.render_todos()
            
    def delete_todo(self, index):
        """Delete todo"""
        if 0 <= index < len(self.todos):
            self.todos.pop(index)
            self.save_todos()
            self.render_todos()
            
    def add_todo_dialog(self):
        """Add todo dialog"""
        dialog = ctk.CTkToplevel(self)
        dialog.title("Add Task")
        dialog.geometry("350x220")
        dialog.attributes("-topmost", True)
        dialog.transient(self)
        dialog.grab_set()
        
        # Center dialog
        dialog.update_idletasks()
        x = self.winfo_x() + (self.sidebar_width // 2) - 175
        y = self.winfo_y() + 200
        dialog.geometry(f"+{x}+{y}")
        
        ctk.CTkLabel(dialog, text="Task:", font=ctk.CTkFont(size=11)).pack(pady=(15, 5), padx=15, anchor="w")
        task_entry = ctk.CTkEntry(dialog, placeholder_text="What to do?")
        task_entry.pack(fill="x", padx=15, pady=(0, 10))
        
        ctk.CTkLabel(dialog, text="Deadline:", font=ctk.CTkFont(size=11)).pack(pady=(0, 5), padx=15, anchor="w")
        deadline_entry = ctk.CTkEntry(dialog, placeholder_text="YYYY-MM-DD HH:MM")
        deadline_entry.pack(fill="x", padx=15, pady=(0, 15))
        deadline_entry.insert(0, datetime.now().strftime("%Y-%m-%d %H:%M"))
        
        def save():
            task = task_entry.get().strip()
            deadline = deadline_entry.get().strip()
            if not task:
                messagebox.showerror("Error", "Task name required!")
                return
            self.todos.append({"task": task, "done": False, "deadline": deadline})
            self.save_todos()
            self.render_todos()
            dialog.destroy()
            
        ctk.CTkButton(dialog, text="Save Task", command=save, corner_radius=6).pack(pady=10)
        
    def update_system_stats(self):
        """Update system stats"""
        if not self.monitoring_active:
            return
        try:
            cpu = psutil.cpu_percent(interval=0.05)
            self.cpu_label.configure(text=f"{cpu:.0f}%")
            self.cpu_bar.set(cpu / 100)
            
            ram = psutil.virtual_memory()
            self.ram_label.configure(text=f"{ram.percent:.0f}%")
            self.ram_bar.set(ram.percent / 100)
            
            self.update_processes()
        except Exception as e:
            print(f"[SIDEBAR] Error updating stats: {e}")
        self.after(1000, self.update_system_stats)
    
    def update_processes(self):
        """Update top processes list"""
        try:
            for widget in self.process_frame.winfo_children():
                widget.destroy()
            
            processes = []
            for proc in psutil.process_iter(['pid', 'name', 'memory_percent']):
                try:
                    processes.append((proc.info['name'], proc.info['memory_percent']))
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    pass
            
            top_procs = sorted(processes, key=lambda x: x[1], reverse=True)[:3]
            
            for name, mem in top_procs:
                proc_item = ctk.CTkFrame(self.process_frame, corner_radius=4, fg_color="transparent")
                proc_item.pack(fill="x", pady=1)
                
                name_label = ctk.CTkLabel(
                    proc_item,
                    text=f"{name[:25]}",
                    font=ctk.CTkFont(size=9),
                    anchor="w"
                )
                name_label.pack(side="left", fill="x", expand=True)
                
                mem_label = ctk.CTkLabel(
                    proc_item,
                    text=f"{mem:.1f}%",
                    font=ctk.CTkFont(size=9),
                    text_color="gray"
                )
                mem_label.pack(side="right")
        except Exception as e:
            print(f"[SIDEBAR] Error updating processes: {e}")
        
    def on_click_handler(self, event):
        """Handle clicks"""
        pass
        
    def on_close(self):
        """Handle close"""
        self.monitoring_active = False
        print("[SIDEBAR] Closing sidebar...")
        if self.on_close_callback:
            self.on_close_callback()
        try:
            self.destroy()
        except Exception:
            pass
        
    def slide_in(self, duration_ms=300):
        """Animate slide in from right - optimized for smooth motion"""
        if self.is_animating or self.is_visible:
            print(f"[SIDEBAR] Cannot slide in - is_animating={self.is_animating}, is_visible={self.is_visible}")
            return
        self.is_animating = True
        self.is_visible = True
        print(f"[SIDEBAR] Starting slide-in animation (duration={duration_ms}ms)")
        
        steps = 40  # More steps = smoother animation
        step_duration = max(10, duration_ms // steps)  # Min 10ms between frames
        target_x = self.screen_width - self.sidebar_width
        current_x = self.screen_width
        step = (target_x - current_x) / steps
        frame_count = 0
        
        def animate():
            nonlocal current_x, frame_count
            current_x += step
            frame_count += 1
            
            if frame_count < steps:
                self.geometry(f"{self.sidebar_width}x{self.screen_height}+{int(current_x)}+0")
                self.after(step_duration, animate)
            else:
                # Final position
                self.geometry(f"{self.sidebar_width}x{self.screen_height}+{target_x}+0")
                self.is_animating = False
                print("[SIDEBAR] Slide-in animation complete!")
                
        animate()
        
    def slide_out(self, duration_ms=300):
        """Animate slide out to right - optimized for smooth motion"""
        if self.is_animating or not self.is_visible:
            return
        self.is_animating = True
        self.is_visible = False
        
        steps = 40  # More steps = smoother animation
        step_duration = max(10, duration_ms // steps)  # Min 10ms between frames
        target_x = self.screen_width
        current_x = self.screen_width - self.sidebar_width
        step = (target_x - current_x) / steps
        frame_count = 0
        
        def animate():
            nonlocal current_x, frame_count
            current_x += step
            frame_count += 1
            
            if frame_count < steps:
                self.geometry(f"{self.sidebar_width}x{self.screen_height}+{int(current_x)}+0")
                self.after(step_duration, animate)
            else:
                self.geometry(f"{self.sidebar_width}x{self.screen_height}+{target_x}+0")
                self.is_animating = False
                
        animate()
