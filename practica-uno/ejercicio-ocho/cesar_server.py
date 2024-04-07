from http.server import HTTPServer, BaseHTTPRequestHandler
import json

class Message:
    def __init__(self, id, content):
        self.id = id
        self.content = content
        self.encrypted_content = self.encrypt(content)

    def encrypt(self, content):
        encrypted_content = ""
        for char in content:
            if char.isalpha():
                shifted_char = chr((ord(char) - ord('a') + 3) % 26 + ord('a'))
                encrypted_content += shifted_char
            else:
                encrypted_content += char
        return encrypted_content

class MessageService:
    messages = {}

    @staticmethod
    def create_message(content):
        message_id = len(MessageService.messages) + 1
        message = Message(message_id, content)
        MessageService.messages[message_id] = message
        return message

    @staticmethod
    def list_messages():
        return [vars(message) for message in MessageService.messages.values()]

    @staticmethod
    def find_message_by_id(message_id):
        if message_id in MessageService.messages:
            return vars(MessageService.messages[message_id])
        else:
            return None

    @staticmethod
    def update_message(message_id, content):
        if message_id in MessageService.messages:
            MessageService.messages[message_id].content = content
            MessageService.messages[message_id].encrypted_content = MessageService.messages[message_id].encrypt(content)
            return vars(MessageService.messages[message_id])
        else:
            return None

    @staticmethod
    def delete_message(message_id):
        if message_id in MessageService.messages:
            del MessageService.messages[message_id]
            return True
        else:
            return False

class HTTPResponseHandler:
    @staticmethod
    def handle_response(handler, status, data):
        handler.send_response(status)
        handler.send_header("Content-type", "application/json")
        handler.end_headers()
        handler.wfile.write(json.dumps(data).encode("utf-8"))

    @staticmethod
    def handle_reader(handler):
        content_length = int(handler.headers["Content-Length"])
        post_data = handler.rfile.read(content_length)
        return json.loads(post_data.decode("utf-8"))

class MessageRequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        if self.path == "/messages":
            data = HTTPResponseHandler.handle_reader(self)
            content = data.get("content")
            message = MessageService.create_message(content)
            HTTPResponseHandler.handle_response(self, 201, vars(message))
        else:
            HTTPResponseHandler.handle_response(self, 404, {"message": "Ruta no encontrada"})

    def do_GET(self):
        if self.path == "/messages":
            messages = MessageService.list_messages()
            HTTPResponseHandler.handle_response(self, 200, messages)
        elif self.path.startswith("/messages/"):
            message_id = int(self.path.split("/")[-1])
            message = MessageService.find_message_by_id(message_id)
            if message:
                HTTPResponseHandler.handle_response(self, 200, message)
            else:
                HTTPResponseHandler.handle_response(self, 404, {"message": "Mensaje no encontrado"})
        else:
            HTTPResponseHandler.handle_response(self, 404, {"message": "Ruta no encontrada"})

    def do_PUT(self):
        if self.path.startswith("/messages/"):
            message_id = int(self.path.split("/")[-1])
            data = HTTPResponseHandler.handle_reader(self)
            content = data.get("content")
            updated_message = MessageService.update_message(message_id, content)
            if updated_message:
                HTTPResponseHandler.handle_response(self, 200, updated_message)
            else:
                HTTPResponseHandler.handle_response(self, 404, {"message": "Mensaje no encontrado"})
        else:
            HTTPResponseHandler.handle_response(self, 404, {"message": "Ruta no encontrada"})

    def do_DELETE(self):
        if self.path.startswith("/messages/"):
            message_id = int(self.path.split("/")[-1])
            if MessageService.delete_message(message_id):
                HTTPResponseHandler.handle_response(self, 200, {"mensaje": "Mensaje eliminado"})
            else:
                HTTPResponseHandler.handle_response(self, 404, {"message": "Mensaje no encontrado"})
        else:
            HTTPResponseHandler.handle_response(self, 404, {"message": "Ruta no encontrada"})

def run_server(port=8000):
    try:
        server_address = ("", port)
        httpd = HTTPServer(server_address, MessageRequestHandler)
        print(f"Iniciando servidor web en http://localhost:{port}/")
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("Apagando servidor web")
        httpd.socket.close()

if __name__ == "__main__":
    run_server()
