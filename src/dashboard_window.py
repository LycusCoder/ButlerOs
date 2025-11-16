import customtkinter as ctk
import psutil
import json
import os
from datetime import datetime
from tkinter import messagebox

class DashboardWindow(ctk.CTkToplevel):
    def __init__(self, root):
        super().__init__(root)
        
        # Window Configuration
        self.title("Butler Dashboard")
        self.geometry("800x600")
        
        # Center window on screen
        self.update_idletasks()
        width = 800
        height = 600
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f'{width}x{height}+{x}+{y}')
        
        # Window attributes
        self.attributes("-topmost", True)
        self.minsize(600, 400)
        
        # State variables
        self.is_dark_mode = True
        self.monitoring_active = True
        self.config_dir = os.path.join(os.path.dirname(__file__), "config")
        self.notes_file = os.path.join(self.config_dir, "notes.txt")
        self.todos_file = os.path.join(self.config_dir, "todos.json")
        
        # Create UI
        self.create_custom_titlebar()
        self.create_main_content()
        
        # Start monitoring loop
        self.update_system_stats()
        
        # Bind close event
        self.protocol("WM_DELETE_WINDOW", self.on_close)
        
    def create_custom_titlebar(self):
        """Custom title bar with controls"""
        self.titlebar = ctk.CTkFrame(self, height=40, corner_radius=0)
        self.titlebar.pack(fill="x", side="top")
        
        # Title
        self.title_label = ctk.CTkLabel(
            self.titlebar, 
            text="🤖 Butler Dashboard", 
            font=ctk.CTkFont(size=14, weight="bold")
        )
        self.title_label.pack(side="left", padx=15)
        
        # Theme toggle button
        self.theme_btn = ctk.CTkButton(
            self.titlebar,
            text="☀️",
            width=40,
            command=self.toggle_theme,
            fg_color="transparent",
            hover_color=("#E0E0E0", "#2B2B2B")
        )
        self.theme_btn.pack(side="right", padx=5)
        
        # Close button
        self.close_btn = ctk.CTkButton(
            self.titlebar,
            text="✕",
            width=40,
            command=self.on_close,
            fg_color="transparent",
            hover_color=("#FF5555", "#FF5555")
        )
        self.close_btn.pack(side="right", padx=5)
        
        # Maximize button
        self.max_btn = ctk.CTkButton(
            self.titlebar,
            text="□",
            width=40,
            command=self.toggle_fullscreen,
            fg_color="transparent",
            hover_color=("#E0E0E0", "#2B2B2B")
        )
        self.max_btn.pack(side="right", padx=5)
        
        # Minimize button
        self.min_btn = ctk.CTkButton(
            self.titlebar,
            text="─",
            width=40,
            command=self.minimize_window,
            fg_color="transparent",
            hover_color=("#E0E0E0", "#2B2B2B")
        )
        self.min_btn.pack(side="right", padx=5)
        
        # Make titlebar draggable
        self.titlebar.bind("<Button-1>", self.start_drag)
        self.titlebar.bind("<B1-Motion>", self.do_drag)
        self.title_label.bind("<Button-1>", self.start_drag)
        self.title_label.bind("<B1-Motion>", self.do_drag)
        
    def start_drag(self, event):
        self.x = event.x
        self.y = event.y
        
    def do_drag(self, event):
        deltax = event.x - self.x
        deltay = event.y - self.y
        x = self.winfo_x() + deltax
        y = self.winfo_y() + deltay
        self.geometry(f"+{x}+{y}")
        
    def toggle_fullscreen(self):
        if self.attributes("-fullscreen"):
            self.attributes("-fullscreen", False)
            self.max_btn.configure(text="□")
        else:
            self.attributes("-fullscreen", True)
            self.max_btn.configure(text="❐")
            
    def minimize_window(self):
        self.iconify()
        
    def toggle_theme(self):
        self.is_dark_mode = not self.is_dark_mode
        if self.is_dark_mode:
            ctk.set_appearance_mode("dark")
            self.theme_btn.configure(text="☀️")
        else:
            ctk.set_appearance_mode("light")
            self.theme_btn.configure(text="🌙")
            
    def create_main_content(self):
        """Create main dashboard content"""
        # Main container with padding
        self.main_container = ctk.CTkFrame(self, corner_radius=0)
        self.main_container.pack(fill="both", expand=True, padx=0, pady=0)
        
        # Create scrollable frame
        self.scroll_frame = ctk.CTkScrollableFrame(self.main_container)
        self.scroll_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # System Monitor Section
        self.create_system_monitor()
        
        # Quick Notes Section
        self.create_quick_notes()
        
        # Todo List Section
        self.create_todo_list()
        
    def create_system_monitor(self):
        """System monitoring section with CPU, RAM, and processes"""
        monitor_frame = ctk.CTkFrame(self.scroll_frame, corner_radius=10)
        monitor_frame.pack(fill="x", pady=(0, 20))
        
        # Header
        header = ctk.CTkLabel(
            monitor_frame, 
            text="⚡ System Monitor", 
            font=ctk.CTkFont(size=16, weight="bold")
        )
        header.pack(anchor="w", padx=20, pady=(15, 10))
        
        # Stats container
        stats_container = ctk.CTkFrame(monitor_frame, fg_color="transparent")
        stats_container.pack(fill="x", padx=20, pady=(0, 15))
        
        # CPU Usage
        cpu_frame = ctk.CTkFrame(stats_container, corner_radius=8)
        cpu_frame.pack(side="left", fill="both", expand=True, padx=(0, 10))
        
        ctk.CTkLabel(
            cpu_frame, 
            text="CPU Usage", 
            font=ctk.CTkFont(size=12)
        ).pack(pady=(10, 5))
        
        self.cpu_label = ctk.CTkLabel(
            cpu_frame, 
            text="0%", 
            font=ctk.CTkFont(size=24, weight="bold")
        )
        self.cpu_label.pack(pady=(0, 10))
        
        self.cpu_bar = ctk.CTkProgressBar(cpu_frame, width=200)
        self.cpu_bar.pack(pady=(0, 10), padx=15)
        self.cpu_bar.set(0)
        
        # RAM Usage
        ram_frame = ctk.CTkFrame(stats_container, corner_radius=8)
        ram_frame.pack(side="left", fill="both", expand=True)
        
        ctk.CTkLabel(
            ram_frame, 
            text="RAM Usage", 
            font=ctk.CTkFont(size=12)
        ).pack(pady=(10, 5))
        
        self.ram_label = ctk.CTkLabel(
            ram_frame, 
            text="0%", 
            font=ctk.CTkFont(size=24, weight="bold")
        )
        self.ram_label.pack(pady=(0, 10))
        
        self.ram_bar = ctk.CTkProgressBar(ram_frame, width=200)
        self.ram_bar.pack(pady=(0, 10), padx=15)
        self.ram_bar.set(0)
        
        # Top Processes
        process_frame = ctk.CTkFrame(monitor_frame, corner_radius=8, fg_color="transparent")
        process_frame.pack(fill="x", padx=20, pady=(0, 15))
        
        ctk.CTkLabel(
            process_frame, 
            text="Top 3 Processes (RAM)", 
            font=ctk.CTkFont(size=12, weight="bold")
        ).pack(anchor="w", pady=(5, 10))
        
        self.process_labels = []
        for i in range(3):
            label = ctk.CTkLabel(
                process_frame, 
                text=f"{i+1}. Loading...", 
                font=ctk.CTkFont(size=11),
                anchor="w"
            )
            label.pack(anchor="w", pady=2)
            self.process_labels.append(label)
            
    def create_quick_notes(self):
        """Quick notes section with auto-save"""
        notes_frame = ctk.CTkFrame(self.scroll_frame, corner_radius=10)
        notes_frame.pack(fill="both", expand=True, pady=(0, 20))
        
        # Header
        header_container = ctk.CTkFrame(notes_frame, fg_color="transparent")
        header_container.pack(fill="x", padx=20, pady=(15, 10))
        
        header = ctk.CTkLabel(
            header_container, 
            text="📝 Quick Notes", 
            font=ctk.CTkFont(size=16, weight="bold")
        )
        header.pack(side="left")
        
        save_status = ctk.CTkLabel(
            header_container, 
            text="Auto-saved", 
            font=ctk.CTkFont(size=10),
            text_color="gray"
        )
        save_status.pack(side="right")
        self.save_status_label = save_status
        
        # Notes textbox
        self.notes_textbox = ctk.CTkTextbox(
            notes_frame, 
            height=150,
            corner_radius=8,
            font=ctk.CTkFont(size=12)
        )
        self.notes_textbox.pack(fill="both", expand=True, padx=20, pady=(0, 15))
        
        # Load existing notes
        self.load_notes()
        
        # Auto-save on text change
        self.notes_textbox.bind("<KeyRelease>", self.auto_save_notes)
        
    def create_todo_list(self):
        """Todo list section with time tracking"""
        todo_frame = ctk.CTkFrame(self.scroll_frame, corner_radius=10)
        todo_frame.pack(fill="both", expand=True, pady=(0, 20))
        
        # Header with Add button
        header_container = ctk.CTkFrame(todo_frame, fg_color="transparent")
        header_container.pack(fill="x", padx=20, pady=(15, 10))
        
        header = ctk.CTkLabel(
            header_container, 
            text="✅ Todo List", 
            font=ctk.CTkFont(size=16, weight="bold")
        )
        header.pack(side="left")
        
        add_btn = ctk.CTkButton(
            header_container,
            text="+ Add Task",
            width=100,
            height=28,
            command=self.add_todo_dialog,
            corner_radius=6
        )
        add_btn.pack(side="right")
        
        # Todo list container
        self.todo_container = ctk.CTkFrame(todo_frame, fg_color="transparent")
        self.todo_container.pack(fill="both", expand=True, padx=20, pady=(0, 15))
        
        # Load todos
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
            print(f"Error loading notes: {e}")
            
    def auto_save_notes(self, event=None):
        """Auto-save notes to file"""
        try:
            notes = self.notes_textbox.get("1.0", "end-1c")
            os.makedirs(self.config_dir, exist_ok=True)
            with open(self.notes_file, "w", encoding="utf-8") as f:
                f.write(notes)
            self.save_status_label.configure(text="✓ Auto-saved")
            self.after(2000, lambda: self.save_status_label.configure(text="Auto-saved"))
        except Exception as e:
            print(f"Error saving notes: {e}")
            
    def load_todos(self):
        """Load todos from JSON file"""
        try:
            if os.path.exists(self.todos_file):
                with open(self.todos_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                self.todos = data.get("todos", [])
            else:
                self.todos = []
        except Exception as e:
            print(f"Error loading todos: {e}")
            self.todos = []
            
        self.render_todos()
        
    def save_todos(self):
        """Save todos to JSON file"""
        try:
            os.makedirs(self.config_dir, exist_ok=True)
            with open(self.todos_file, "w", encoding="utf-8") as f:
                json.dump({"todos": self.todos}, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error saving todos: {e}")
            
    def render_todos(self):
        """Render todo list items"""
        # Clear existing todos
        for widget in self.todo_container.winfo_children():
            widget.destroy()
            
        if not self.todos:
            empty_label = ctk.CTkLabel(
                self.todo_container,
                text="No tasks yet. Click '+ Add Task' to create one!",
                font=ctk.CTkFont(size=12),
                text_color="gray"
            )
            empty_label.pack(pady=20)
            return
            
        # Render each todo
        for i, todo in enumerate(self.todos):
            todo_item = ctk.CTkFrame(self.todo_container, corner_radius=8)
            todo_item.pack(fill="x", pady=5)
            
            # Checkbox
            checkbox = ctk.CTkCheckBox(
                todo_item,
                text="",
                width=20,
                command=lambda idx=i: self.toggle_todo(idx)
            )
            checkbox.pack(side="left", padx=(10, 5), pady=10)
            if todo.get("done", False):
                checkbox.select()
                
            # Task info container
            info_frame = ctk.CTkFrame(todo_item, fg_color="transparent")
            info_frame.pack(side="left", fill="x", expand=True, pady=10)
            
            # Task name
            task_label = ctk.CTkLabel(
                info_frame,
                text=todo.get("task", "Untitled"),
                font=ctk.CTkFont(size=13, weight="bold" if not todo.get("done") else "normal"),
                anchor="w"
            )
            task_label.pack(anchor="w", fill="x")
            
            # Time info
            start_time = todo.get("start_time", "N/A")
            deadline = todo.get("deadline", "N/A")
            time_text = f"Start: {start_time} | Deadline: {deadline}"
            
            time_label = ctk.CTkLabel(
                info_frame,
                text=time_text,
                font=ctk.CTkFont(size=10),
                text_color="gray",
                anchor="w"
            )
            time_label.pack(anchor="w")
            
            # Delete button
            delete_btn = ctk.CTkButton(
                todo_item,
                text="🗑️",
                width=40,
                height=35,
                command=lambda idx=i: self.delete_todo(idx),
                fg_color="transparent",
                hover_color=("#FF5555", "#8B0000")
            )
            delete_btn.pack(side="right", padx=10)
            
    def toggle_todo(self, index):
        """Toggle todo completion status"""
        if 0 <= index < len(self.todos):
            self.todos[index]["done"] = not self.todos[index].get("done", False)
            self.save_todos()
            self.render_todos()
            
    def delete_todo(self, index):
        """Delete a todo item"""
        if 0 <= index < len(self.todos):
            self.todos.pop(index)
            self.save_todos()
            self.render_todos()
            
    def add_todo_dialog(self):
        """Show dialog to add new todo"""
        dialog = ctk.CTkToplevel(self)
        dialog.title("Add New Task")
        dialog.geometry("400x300")
        dialog.attributes("-topmost", True)
        dialog.transient(self)
        dialog.grab_set()
        
        # Center dialog
        dialog.update_idletasks()
        x = self.winfo_x() + (self.winfo_width() // 2) - 200
        y = self.winfo_y() + (self.winfo_height() // 2) - 150
        dialog.geometry(f"+{x}+{y}")
        
        # Task name
        ctk.CTkLabel(dialog, text="Task Name:", font=ctk.CTkFont(size=12)).pack(pady=(20, 5), padx=20, anchor="w")
        task_entry = ctk.CTkEntry(dialog, placeholder_text="Enter task name")
        task_entry.pack(fill="x", padx=20, pady=(0, 15))
        
        # Start time
        ctk.CTkLabel(dialog, text="Start Time:", font=ctk.CTkFont(size=12)).pack(pady=(0, 5), padx=20, anchor="w")
        start_entry = ctk.CTkEntry(dialog, placeholder_text="YYYY-MM-DD HH:MM")
        start_entry.pack(fill="x", padx=20, pady=(0, 15))
        start_entry.insert(0, datetime.now().strftime("%Y-%m-%d %H:%M"))
        
        # Deadline
        ctk.CTkLabel(dialog, text="Deadline:", font=ctk.CTkFont(size=12)).pack(pady=(0, 5), padx=20, anchor="w")
        deadline_entry = ctk.CTkEntry(dialog, placeholder_text="YYYY-MM-DD HH:MM")
        deadline_entry.pack(fill="x", padx=20, pady=(0, 20))
        
        def save_todo():
            task = task_entry.get().strip()
            start = start_entry.get().strip()
            deadline = deadline_entry.get().strip()
            
            if not task:
                messagebox.showerror("Error", "Task name cannot be empty!")
                return
                
            new_todo = {
                "task": task,
                "done": False,
                "start_time": start,
                "deadline": deadline
            }
            
            self.todos.append(new_todo)
            self.save_todos()
            self.render_todos()
            dialog.destroy()
            
        # Save button
        save_btn = ctk.CTkButton(
            dialog,
            text="Save Task",
            command=save_todo,
            corner_radius=6
        )
        save_btn.pack(pady=10)
        
    def update_system_stats(self):
        """Update system statistics (CPU, RAM, processes)"""
        if not self.monitoring_active:
            return
            
        try:
            # CPU Usage
            cpu_percent = psutil.cpu_percent(interval=0.1)
            self.cpu_label.configure(text=f"{cpu_percent:.1f}%")
            self.cpu_bar.set(cpu_percent / 100)
            
            # RAM Usage
            ram = psutil.virtual_memory()
            ram_percent = ram.percent
            self.ram_label.configure(text=f"{ram_percent:.1f}%")
            self.ram_bar.set(ram_percent / 100)
            
            # Top 3 processes by memory
            processes = []
            for proc in psutil.process_iter(['name', 'memory_percent']):
                try:
                    processes.append({
                        'name': proc.info['name'],
                        'memory': proc.info['memory_percent']
                    })
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    pass
                    
            # Sort by memory and get top 3
            processes.sort(key=lambda x: x['memory'], reverse=True)
            top_3 = processes[:3]
            
            for i, proc in enumerate(top_3):
                if i < len(self.process_labels):
                    self.process_labels[i].configure(
                        text=f"{i+1}. {proc['name'][:30]} - {proc['memory']:.1f}%"
                    )
                    
        except Exception as e:
            print(f"Error updating stats: {e}")
            
        # Schedule next update (Task Manager style - 1 second)
        self.after(1000, self.update_system_stats)
        
    def on_close(self):
        """Handle window close event"""
        self.monitoring_active = False
        self.destroy()
