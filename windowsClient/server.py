from flask import Flask, redirect, request
from flask_socketio import SocketIO
import pyautogui

class VoiceTypingAppServer:
    def __init__(self):
        self.app = Flask(__name__)
        self.socketio = SocketIO(self.app)

        @self.app.route('/send_message', methods=['POST'])
        def send_message():
            message = request.form.get('message')
            device_name = request.form.get('device_name')
            print(f"Received message from {device_name}: {message}")
            if message is not None:
                pyautogui.write(str(message)) # Type out the message
            return redirect("https://github.com/a3ro-dev/voiceTypingApp", code=302)

        @self.socketio.on('message')
        def handle_message(data):
            print('received message: ' + data)

    def run(self):
        self.socketio.run(self.app, host='0.0.0.0', port=3000, use_reloader=False, log_output=True)
