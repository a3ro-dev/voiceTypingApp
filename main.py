import tkinter as tk
from tkinter import ttk
from ttkthemes import ThemedTk
import speech_recognition as sr
import pyttsx3
import pyautogui as pyg
from audioplayer import AudioPlayer as adp
import pyperclip
import threading

class VoiceTypingApp:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.engine = pyttsx3.init()
        self.is_listening = False
        self.root = ThemedTk(theme="yaru")  # Using the yaru' theme
        self.root.title("Voice Typing App")
        self.root.geometry("300x150")
        self.create_widgets()

    def create_widgets(self):
        frame = ttk.Frame(self.root)
        frame.pack(pady=20)

        self.settings_button = ttk.Button(frame, text="⚙️", command=self.open_settings)
        self.settings_button.grid(row=0, column=0)

        self.mic_button = ttk.Button(frame, text="🎙️", command=self.toggle_listening)
        self.mic_button.grid(row=0, column=1, padx=(10, 0))

        self.close_button = ttk.Button(frame, text="X", command=self.root.quit)
        self.close_button.grid(row=0, column=2)

        self.listening_label = ttk.Label(self.root, text="Listening...")
        self.listening_label.pack()

    def open_settings(self):
        # Create a new window
        self.settings_window = tk.Toplevel(self.root)
        self.settings_window.title("Settings")

        # Add a label
        label = tk.Label(self.settings_window, text="Theme")
        label.pack(side="left", padx=(10, 10))

        # Add a dark/light mode switch
        self.theme_var = tk.StringVar(value="light")
        self.dark_mode_button = tk.Radiobutton(self.settings_window, text="Dark Mode", variable=self.theme_var, value="dark", command=self.switch_theme)
        self.dark_mode_button.pack(side="left")

        self.light_mode_button = tk.Radiobutton(self.settings_window, text="Light Mode", variable=self.theme_var, value="light", command=self.switch_theme)
        self.light_mode_button.pack(side="left")

    def switch_theme(self):
        if self.theme_var.get() == "dark":
            self.root.configure(background='black')
            self.root.tk_setPalette(background='black', foreground='white')
        else:
            self.root.configure(background='white')
            self.root.tk_setPalette(background='white', foreground='black')

    def toggle_listening(self):
        if self.is_listening:
            self.stop_listening()
        else:
            self.start_listening()

    def start_listening(self):
        if not self.is_listening:
            self.is_listening = True
            self.listening_thread = threading.Thread(target=self.listen_loop)  # Create a new thread for listening
            self.listening_thread.start()  # Start the listening thread
            adp('./audio/ting.mp3').play(block=True)
            self.listening_label.config(text="Listening...")

    def stop_listening(self):
        if self.is_listening:
            self.is_listening = False
            self.listening_thread.join()  # Wait for the listening thread to finish
            self.engine.say('Listening Paused.')
            self.engine.runAndWait()
            self.listening_label.config(text="Not Listening...")

    def listen_loop(self):
        special_commands = {"exit", "pause", "stop", "new line", "next line"}
        while self.is_listening:
            try:
                with self.microphone as source:
                    audio = self.recognizer.listen(source)
                    text = self.recognizer.recognize(audio)  # synthesize the text from the audio
                    cmd = str(text).lower()
                    if cmd in special_commands:
                        if cmd == "exit":
                            self.is_listening = False  # Ensure the loop can exit
                        elif cmd in {"pause", "stop"}:
                            self.stop_listening()
                        elif cmd in {"new line", "next line"}:
                            pyg.press('enter')
                    else:
                        pyperclip.copy(cmd)  # Copy the text to the clipboard
                        pyg.hotkey('ctrl', 'v')  # Paste the text
                        print(cmd)
            except Exception as e:
                self.engine.say(f"I didn't understand that due to {e}")
                self.engine.runAndWait()
                if not self.is_listening:
                    break  # Exit the loop if stop_listening was called

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = VoiceTypingApp()
    app.run()