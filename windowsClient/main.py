import threading
import tkinter as tk
from server import VoiceTypingAppServer
from PIL import Image
import pystray

server = None
server_thread = None

def toggle_server():
    global server
    global server_thread
    if server is None:
        server = VoiceTypingAppServer()
        server_thread = threading.Thread(target=server.run)
        server_thread.start()
    else:
        server.stop()  # You need to implement this method in your server class
        server_thread.join() # type: ignore
        server = None
        server_thread = None

def create_icon(image_path):
    image = Image.open(image_path)
    icon = pystray.Icon("name", image, "My System Tray Icon", menu=pystray.Menu(pystray.MenuItem("Quit", lambda: icon.stop())))
    icon.run()

def on_close():
    root.withdraw()
    create_icon('windowsClient/voice-control.ico')  # Replace with the path to your icon file

root = tk.Tk()
root.title("VoiceTypingWindowsClient")
root.geometry("500x500")
# root.iconbitmap('voice-control.ico')

toggle_button = tk.Checkbutton(root, text="Toggle Server", command=toggle_server, width=100, height=100)
toggle_button.pack()

root.protocol("WM_DELETE_WINDOW", on_close)
root.mainloop()