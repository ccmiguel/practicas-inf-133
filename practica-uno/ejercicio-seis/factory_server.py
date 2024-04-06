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

class Mammal(Animal):
    def __init__(self, id, nombre, genero, edad, peso, gestation_period):
        super().__init__(id, nombre, "Mamífero", genero, edad, peso)
        self.gestation_period = gestation_period

class Bird(Animal):
    def __init__(self, id, nombre, genero, edad, peso, wingspan):
        super().__init__(id, nombre, "Ave", genero, edad, peso)
        self.wingspan = wingspan

class Reptile(Animal):
    def __init__(self, id, nombre, genero, edad, peso, scale_type):
        super().__init__(id, nombre, "Reptil", genero, edad, peso)
        self.scale_type = scale_type

class Amphibian(Animal):
    def __init__(self, id, nombre, genero, edad, peso, skin_type):
        super().__init__(id, nombre, "Anfibio", genero, edad, peso)
        self.skin_type = skin_type

class Fish(Animal):
    def __init__(self, id, nombre, genero, edad, peso, habitat):
        super().__init__(id, nombre, "Pez", genero, edad, peso)
        self.habitat = habitat

class AnimalFactory:
    @staticmethod
    def create_animal(animal_type, id, nombre, genero, edad, peso, **kwargs):
        if animal_type == "Mammal":
            return Mammal(id, nombre, genero, edad, peso, kwargs.get("gestation_period"))
        elif animal_type == "Bird":
            return Bird(id, nombre, genero, edad, peso, kwargs.get("wingspan"))
        elif animal_type == "Reptile":
            return Reptile(id, nombre, genero, edad, peso, kwargs.get("scale_type"))
        elif animal_type == "Amphibian":
            return Amphibian(id, nombre, genero, edad, peso, kwargs.get("skin_type"))
        elif animal_type == "Fish":
            return Fish(id, nombre, genero, edad, peso, kwargs.get("habitat"))
        else:
            raise ValueError("Tipo de animal no válido")

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




class ZooRequestHandler(BaseHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        self.animal_factory = AnimalFactory()
        super().__init__(*args, **kwargs)

    def do_POST(self):
        if self.path == "/animals":
            data = HTTPResponseHandler.handle_reader(self)
            animal_type = data.get("animal_type")
            del data["animal_type"]  # Eliminar animal_type de data
            animal = self.create_animal(animal_type, **data)
            if animal:
                HTTPResponseHandler.handle_response(self, 201, vars(animal))
            else:
                HTTPResponseHandler.handle_response(self, 400, {"message": "Tipo de animal no válido"})
        else:
            HTTPResponseHandler.handle_response(self, 404, {"message": "Ruta no encontrada"})

    def create_animal(self, animal_type, **kwargs):
        id = 1  # O puedes encontrar el último ID de alguna manera
        return self.animal_factory.create_animal(animal_type, id, **kwargs)

def run_server(port=8000):
    try:
        server_address = ("", port)
        httpd = HTTPServer(server_address, ZooRequestHandler)
        print(f"Iniciando servidor web en http://localhost:{port}/")
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("Apagando servidor web")
        httpd.socket.close()

if __name__ == "__main__":
    run_server()
