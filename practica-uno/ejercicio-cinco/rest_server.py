from http.server import HTTPServer, BaseHTTPRequestHandler
import json
from urllib.parse import urlparse, parse_qs

class Animal:
    def __init__(self, id, nombre, especie, genero, edad, peso):
        self.id = id
        self.nombre = nombre
        self.especie = especie
        self.genero = genero
        self.edad = edad
        self.peso = peso

class AnimalService:
    animals = [
        Animal(1, "Elefante", "Paquidermo", "Masculino", 3, 160),
        Animal(2, "Jaguar", "Felino", "Femenino", 6, 190)
    ]

    @staticmethod
    def create_animal(data):
        id = len(AnimalService.animals) + 1
        animal = Animal(
            id,
            data.get("nombre"),
            data.get("especie"),
            data.get("genero"),
            data.get("edad"),
            data.get("peso")
        )
        AnimalService.animals.append(animal)
        return animal

    @staticmethod
    def list_animals():
        return [vars(animal) for animal in AnimalService.animals]

    @staticmethod
    def find_animals_by_species(especie):
        return [vars(animal) for animal in AnimalService.animals if animal.especie == especie]

    @staticmethod
    def find_animals_by_gender(genero):
        return [vars(animal) for animal in AnimalService.animals if animal.genero == genero]

    @staticmethod
    def update_animal(id, data):
        for animal in AnimalService.animals:
            if animal.id == id:
                for key, value in data.items():
                    setattr(animal, key, value)
                return vars(animal)
        return None

    @staticmethod
    def delete_animal(id):
        for animal in AnimalService.animals:
            if animal.id == id:
                AnimalService.animals.remove(animal)
                return True
        return False

class HTTPResponseHandler:
    @staticmethod
    def handle_response(handler, status, data):
        handler.send_response(status)
        handler.send_header("Content-type", "application/json")
        handler.end_headers()
        handler.wfile.write(json.dumps(data).encode("utf-8"))

class RESTRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urlparse(self.path)
        query_params = parse_qs(parsed_path.query)

        if parsed_path.path == "/animales":
            if "especie" in query_params:
                especie = query_params["especie"][0]
                animals = AnimalService.find_animals_by_species(especie)
                HTTPResponseHandler.handle_response(self, 200, animals)
            elif "genero" in query_params:
                genero = query_params["genero"][0]
                animals = AnimalService.find_animals_by_gender(genero)
                HTTPResponseHandler.handle_response(self, 200, animals)
            else:
                animals = AnimalService.list_animals()
                HTTPResponseHandler.handle_response(self, 200, animals)
        else:
            HTTPResponseHandler.handle_response(self, 404, {"Error": "Ruta no existente"})

    def do_POST(self):
        if self.path == "/animales":
            content_length = int(self.headers["Content-Length"])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode("utf-8"))

            animal = AnimalService.create_animal(data)

            HTTPResponseHandler.handle_response(self, 201, vars(animal))
        else:
            HTTPResponseHandler.handle_response(self, 404, {"Error": "Ruta no existente"})

    def do_PUT(self):
        if self.path.startswith("/animales/"):
            id = int(self.path.split("/")[-1])
            content_length = int(self.headers["Content-Length"])
            put_data = self.rfile.read(content_length)
            data = json.loads(put_data.decode("utf-8"))

            animal = AnimalService.update_animal(id, data)
            if animal:
                HTTPResponseHandler.handle_response(self, 200, animal)
            else:
                HTTPResponseHandler.handle_response(self, 404, {"Error": "Animal no encontrado"})
        else:
            HTTPResponseHandler.handle_response(self, 404, {"Error": "Ruta no existente"})

    def do_DELETE(self):
        if self.path.startswith("/animales/"):
            id = int(self.path.split("/")[-1])
            if AnimalService.delete_animal(id):
                HTTPResponseHandler.handle_response(self, 200, {"mensaje": "Animal eliminado"})
            else:
                HTTPResponseHandler.handle_response(self, 404, {"Error": "Animal no encontrado"})
        else:
            HTTPResponseHandler.handle_response(self, 404, {"Error": "Ruta no existente"})

def run_server(port=8000):
    try:
        server_address = ("", port)
        httpd = HTTPServer(server_address, RESTRequestHandler)
        print(f"Iniciando servidor web en http://localhost:{port}/")
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("Apagando servidor web")
        httpd.socket.close()

if __name__ == "__main__":
    run_server()
