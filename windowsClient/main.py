import threading
import tkinter as tk
from server import VoiceTypingAppServer
from PIL import Image
import pystray

server = None
server_thread = None
icon = None
device_name_label = None
connection_status_canvas = None

def toggle_server(icon, item):
    global server
    global server_thread
    if server is None:
        server = VoiceTypingAppServer()
        server_thread = threading.Thread(target=server.run)
        server_thread.start()
        if item is not None:
            item.text = "Turn server off"
    else:
        server.stop()  # You need to implement this method in your server class
        server_thread.join() # type: ignore
        server = None
        server_thread = None
        if item is not None:
            item.text = "Turn server on"

device_name_label = None  # Initialize the device_name_label variable

connection_status_canvas = None  # Initialize the connection_status_canvas variable

def update_device_name(device_name):
    device_name_label.config(text=f"Device name: {device_name}")

def update_connection_status(is_connected):
    global connection_status_canvas  # Add global keyword to access the global variable
    color = "green" if is_connected else "red"
    connection_status_canvas.config(bg=color)

def create_icon(image_path):
    global icon
    image = Image.open(image_path)
    menu_item = pystray.MenuItem("Turn server on", toggle_server)
    icon = pystray.Icon("name", image, "My System Tray Icon", menu=pystray.Menu(menu_item, pystray.MenuItem("Quit", lambda icon, item: icon.stop())))
    icon.run()

def on_close():
    root.withdraw()
    create_icon('windowsClient/voice-control.ico')  # Replace with the path to your icon file

root = tk.Tk()
root.title("VoiceTypingWindowsClient")
root.geometry("500x500")
# root.iconbitmap('voice-control.ico')

toggle_button = tk.Checkbutton(root, text="Toggle Server", command=lambda: toggle_server(None, None), width=100, height=100)
toggle_button.pack()

device_name_label = tk.Label(root, text="Device name: ")
device_name_label.pack()

connection_status_canvas = tk.Canvas(root, width=500, height=20, bg="red")
connection_status_canvas.pack(fill=tk.X)

root.protocol("WM_DELETE_WINDOW", on_close)
root.mainloop()