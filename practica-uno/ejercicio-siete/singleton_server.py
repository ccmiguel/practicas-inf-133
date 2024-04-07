from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import random

class Game:
    _instance = None

    def __new__(cls):
        if not cls._instance:
            cls._instance = super().__new__(cls)
            cls._instance.games = {}
        return cls._instance

    def create_game(self, player_element):
        game_id = len(self.games) + 1
        server_element = random.choice(["piedra", "papel", "tijera"])
        result = self.calculate_result(player_element, server_element)
        game_data = {
            "id": game_id,
            "player_element": player_element,
            "server_element": server_element,
            "result": result
        }
        self.games[game_id] = game_data
        return game_data

    def calculate_result(self, player_element, server_element):
        if player_element == server_element:
            return "empató"
        elif (player_element == "piedra" and server_element == "tijera") or \
             (player_element == "tijera" and server_element == "papel") or \
             (player_element == "papel" and server_element == "piedra"):
            return "ganó"
        else:
            return "perdió"

class GameRequestHandler(BaseHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        self.game_instance = Game()
        super().__init__(*args, **kwargs)

    def do_POST(self):
        if self.path == "/games":
            content_length = int(self.headers["Content-Length"])
            post_data = self.rfile.read(content_length)
            player_element = json.loads(post_data.decode("utf-8"))["element"]
            game = self.game_instance.create_game(player_element)
            self.send_response(201)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(game).encode("utf-8"))
        else:
            self.send_response(404)
            self.end_headers()

    def do_GET(self):
        if self.path == "/games":
            games = list(self.game_instance.games.values())
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(games).encode("utf-8"))
        elif self.path.startswith("/games?resultado="):
            result_filter = self.path.split("=")[1]
            games = [game for game in self.game_instance.games.values() if game["result"] == result_filter]
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(games).encode("utf-8"))
        else:
            self.send_response(404)
            self.end_headers()

def run_server(port=8000):
    try:
        server_address = ("", port)
        httpd = HTTPServer(server_address, GameRequestHandler)
        print(f"Iniciando servidor web en http://localhost:{port}/")
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("Apagando servidor web")
        httpd.socket.close()

if __name__ == "__main__":
    run_server()
