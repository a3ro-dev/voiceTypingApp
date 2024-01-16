from flask import Flask, request, redirect
from werkzeug.serving import make_server

class VoiceTypingAppServer:
    def __init__(self):
        self.app = Flask(__name__)
        self.server = None

        @self.app.route('/send_message', methods=['POST'])
        def send_message():
            message = request.form.get('message')
            device_name = request.form.get('device_name')
            print(f"Received message from {device_name}: {message}")
            return redirect("http://example.com", code=302)

    def run(self):
        self.server = make_server('localhost', 3000, self.app)
        self.server.serve_forever()

    def stop(self):
        if self.server is not None:
            self.server.shutdown()