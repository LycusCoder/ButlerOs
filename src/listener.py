import keyboard
import os
import threading

def show_menu():
    print("Hotkey detected! Opening menu...")
    os.system("start python quick_menu.py") 

def start_listener():
    print("Listener active. Press 'Ctrl + Alt + M' to open the menu.")
    print("Press 'Esc' to exit the listener.")
    keyboard.add_hotkey("ctrl+alt+m", show_menu)
    keyboard.wait("esc", suppress=True) 
    print("Listener stopped.")

if __name__ == "__main__":
    listener_thread = threading.Thread(target=start_listener)
    listener_thread.start()