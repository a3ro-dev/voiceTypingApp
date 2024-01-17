import time
import pyautogui
import tkinter as tk
import tkinter.messagebox
from threading import Thread
import subprocess

class App:
    def __init__(self, root):
        self.root = root
        self.file_path = 'vivo 1904/Internal storage/documents/voicetypingdata//voicetypingdata.txt'
        self.is_paused = False
        self.start_button = tk.Button(root, text="Start", command=self.start_typing)
        self.start_button.pack()
        self.pause_button = tk.Button(root, text="Pause", command=self.pause_typing)
        self.pause_button.pack()

    def start_typing(self):
        def check_device_connected():
            try:
                result = subprocess.run(['adb', 'devices'], capture_output=True, text=True)
                lines = result.stdout.splitlines()
                if len(lines) > 2:
                    return lines[1].split('\t')[0]
                else:
                    return None
            except FileNotFoundError:
                tkinter.messagebox.showerror("Error", "ADB not found. Please install ADB and add it to your system's PATH.")
                self.root.quit()

        device_name = check_device_connected()
        if device_name:
            self.typing_thread = Thread(target=self.type_words_from_file)
            self.typing_thread.start()
            self.start_button.config(text=f"Connected to {device_name}", state="disabled")
        else:
            tkinter.messagebox.showerror("Error", "No device found")
            self.root.quit()

    def pause_typing(self):
        self.is_paused = not self.is_paused
        self.pause_button.config(text="Resume" if self.is_paused else "Pause")

    def type_words_from_file(self):
        try:
            with open(self.file_path, 'r') as file:
                lines = file.readlines()

            for line in lines:
                while self.is_paused:
                    time.sleep(1)
                word = line.split(': ')[1].strip()
                pyautogui.write(word)
                pyautogui.press('space')
                time.sleep(1)
        except FileNotFoundError:
            tkinter.messagebox.showerror("Error", f"File not found: {self.file_path}")

def check_device_connected(self):
    try:
        result = subprocess.run(['adb', 'devices'], capture_output=True, text=True)
        lines = result.stdout.splitlines()
        if len(lines) > 2:
            return lines[1].split('\t')[0]
        else:
            return None
    except FileNotFoundError:
        tkinter.messagebox.showerror("Error", "ADB not found. Please install ADB and add it to your system's PATH.")
        self.root.quit()

root = tk.Tk()
app = App(root)
root.mainloop()