from flask import Flask, request, redirect

class VoiceTypingAppServer:
    def __init__(self):
        self.app = Flask(__name__)

        @self.app.route('/send_message', methods=['POST'])
        def send_message():
            message = request.form.get('message')
            # Here you would send the message to your Flutter app
            # This could be done in a variety of ways, such as through a WebSocket connection,
            # by updating a database that your Flutter app is listening to, etc.
            
            # Redirect to a specific URL
            return redirect("http://example.com", code=302)

    def run(self):
        self.app.run(port=3000)

if __name__ == '__main__':
    server = VoiceTypingAppServer()
    server.run()
