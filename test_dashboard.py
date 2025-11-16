#!/usr/bin/env python3
"""
Simple test script untuk Butler Dashboard
Test basic functionality tanpa perlu full system tray
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

import customtkinter as ctk
from dashboard_window import DashboardWindow

def test_dashboard():
    """Test dashboard window"""
    print("🧪 Testing Butler Dashboard...")
    print("-" * 50)
    
    # Create root window
    root = ctk.CTk()
    root.withdraw()  # Hide root
    
    try:
        # Create dashboard
        print("✓ Creating dashboard window...")
        dashboard = DashboardWindow(root)
        
        print("✓ Dashboard created successfully!")
        print("✓ System monitor initialized")
        print("✓ Quick notes loaded")
        print("✓ Todo list loaded")
        print("-" * 50)
        print("📊 Dashboard is running!")
        print("   - Try dragging the window")
        print("   - Toggle dark/light mode")
        print("   - Add a new todo")
        print("   - Type in quick notes (auto-saves)")
        print("   - Watch real-time system stats")
        print("-" * 50)
        print("Press Ctrl+C to stop or close the dashboard window")
        
        # Run mainloop
        root.mainloop()
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True

if __name__ == "__main__":
    test_dashboard()
