import threading
from server import VoiceTypingAppServer
import tkinter as tk

def start_server():
    server = VoiceTypingAppServer()
    threading.Thread(target=server.run).start()

root = tk.Tk()
start_button = tk.Button(root, text="Start Server", command=start_server)
start_button.pack()
root.mainloop()