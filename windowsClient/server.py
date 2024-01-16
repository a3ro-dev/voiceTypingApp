from flask import Flask, request, redirect
from werkzeug.serving import make_server
import pyautogui

class VoiceTypingAppServer:
    def __init__(self):
        self.app = Flask(__name__)
        self.server = None

        @self.app.route('/send_message', methods=['POST'])
        def send_message():
            message = request.form.get('message')
            device_name = request.form.get('device_name')
            print(f"Received message from {device_name}: {message}")
            pyautogui.write(message)  # type: ignore # Type out the message
            return redirect("https://github.com/a3ro-dev/voiceTypingApp", code=302)

    def run(self):
        self.server = make_server('localhost', 3000, self.app)
        self.server.serve_forever()

    def stop(self):
        if self.server is not None:
            self.server.shutdown()