import tkinter as tk
from tkinter import ttk
from ttkthemes import ThemedTk
import threading
import speech_recognition as sr
import pyttsx3
import pyautogui as pyg
from audioplayer import AudioPlayer as adp
import pyperclip

class VoiceTypingApp:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.engine = pyttsx3.init()
        self.is_listening = False
        self.root = ThemedTk(theme="arc")  # Using a theme for better appearance
        self.root.title("Voice Typing App")
        self.root.geometry("300x200")
        self.create_widgets()

    def create_widgets(self):
        self.start_button = ttk.Button(self.root, text="Start", command=self.start_listening)
        self.start_button.pack()
        self.stop_button = ttk.Button(self.root, text="Stop", command=self.stop_listening)
        self.stop_button.pack()

    def start_listening(self):
        self.is_listening = True
        threading.Thread(target=self.listen_loop).start()
        adp('windowsClient/audio/ting.mp3').play(block=True)

    def stop_listening(self):
        self.is_listening = False
        self.engine.say('Listening Paused.')
        self.engine.runAndWait()

    def listen_loop(self):
        while self.is_listening:
            try:
                with self.microphone as source:
                    audio = self.recognizer.listen(source)
                    text = self.recognizer.recognize(audio)
                    cmd = str(text).lower()
                    if cmd == "exit":
                        break
                    elif cmd in ["pause", "stop"]:
                        self.stop_listening()
                    elif cmd in ["new line", "next line"]:
                        pyg.press('enter')
                    else:
                        pyperclip.copy(text)  # Copy the text to the clipboard
                        pyg.hotkey('ctrl', 'v')  # Paste the text
                        print(text) 
            except Exception as e:
                self.engine.say(f"I didn't understand that due to {e}")
                self.engine.runAndWait()

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = VoiceTypingApp()
    app.run()