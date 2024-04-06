from http.server import HTTPServer, BaseHTTPRequestHandler
import json

from urllib.parse import urlparse, parse_qs

pacientes = [
    {
        "CI": "1234567",
        "nombre": "María",
        "apellido": "López",
        "edad": 30,
        "género": "Femenino",
        "diagnóstico": "Hipertensión",
        "doctor": "Dr. García"
    },
]


class PacientesService:
    @staticmethod
    def find_paciente(ci):
        return next(
            (paciente for paciente in pacientes if paciente["CI"] == ci),
            None,
        )

    @staticmethod
    def add_paciente(data):
        pacientes.append(data)
        return pacientes

    @staticmethod
    def update_paciente(ci, data):
        paciente = PacientesService.find_paciente(ci)
        if paciente:
            paciente.update(data)
            return pacientes
        else:
            return None

    @staticmethod
    def delete_paciente(ci):
        for i, paciente in enumerate(pacientes):
            if paciente["CI"] == ci:
                pacientes.pop(i)
                return pacientes
        return None


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

        if parsed_path.path == "/pacientes":
            if "diagnóstico" in query_params:
                diagnostico = query_params["diagnóstico"][0]
                pacientes_filtrados = [
                    paciente for paciente in pacientes if paciente["diagnóstico"] == diagnostico
                ]
                if pacientes_filtrados:
                    HTTPResponseHandler.handle_response(
                        self, 200, pacientes_filtrados
                    )
                else:
                    HTTPResponseHandler.handle_response(self, 204, [])
            elif "doctor" in query_params:
                doctor = query_params["doctor"][0]
                pacientes_doctor = [
                    paciente for paciente in pacientes if paciente["doctor"] == doctor
                ]
                if pacientes_doctor:
                    HTTPResponseHandler.handle_response(
                        self, 200, pacientes_doctor
                    )
                else:
                    HTTPResponseHandler.handle_response(self, 204, [])
            elif "CI" in query_params:
                ci = query_params["CI"][0]
                paciente = PacientesService.find_paciente(ci)
                if paciente:
                    HTTPResponseHandler.handle_response(self, 200, [paciente])
                else:
                    HTTPResponseHandler.handle_response(self, 204, [])
            else:
                HTTPResponseHandler.handle_response(self, 200, pacientes)
        else:
            HTTPResponseHandler.handle_response(
                self, 404, {"Error": "Ruta no existente"}
            )

    def do_POST(self):
        if self.path == "/pacientes":
            data = self.read_data()
            pacientes = PacientesService.add_paciente(data)
            HTTPResponseHandler.handle_response(self, 201, {"mensaje": "Paciente creado"})
        else:
            HTTPResponseHandler.handle_response(
                self, 404, {"Error": "Ruta no existente"}
            )

    def do_PUT(self):
        if self.path.startswith("/pacientes/"):
            ci = self.path.split("/")[-1]
            data = self.read_data()
            pacientes = PacientesService.update_paciente(ci, data)
            if pacientes:
                HTTPResponseHandler.handle_response(self, 200, pacientes)
            else:
                HTTPResponseHandler.handle_response(
                    self, 404, {"Error": "Paciente no encontrado"}
                )
        else:
            HTTPResponseHandler.handle_response(
                self, 404, {"Error": "Ruta no existente"}
            )

    def do_DELETE(self):
        if self.path.startswith("/pacientes/"):
            ci = self.path.split("/")[-1]
            pacientes = PacientesService.delete_paciente(ci)
            if pacientes:
                HTTPResponseHandler.handle_response(self, 200, pacientes)
            else:
                HTTPResponseHandler.handle_response(
                    self, 404, {"Error": "Paciente no encontrado"}
                )
        else:
            HTTPResponseHandler.handle_response(
                self, 404, {"Error": "Ruta no existente"}
            )

    def read_data(self):
        content_length = int(self.headers["Content-Length"])
        data = self.rfile.read(content_length)
        data = json.loads(data.decode("utf-8"))
        return data


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
