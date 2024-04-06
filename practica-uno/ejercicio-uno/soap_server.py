from http.server import HTTPServer
from pysimplesoap.server import SoapDispatcher, SOAPHandler

# Define la función del servicio

def SumaDosNumeros(x, y):
    return x + y 

def RestaDosNumeros(x, y):
    return x - y 

def MultiplicaDosNumeros(x, y):
    return x * y 

def DivideDosNumeros(x, y):
    if y == 0:
        return "Error: No se puede dividir por cero."
    return x / y 

# Creamos la ruta del servidor SOAP
dispatcher = SoapDispatcher(
    "ejemplo-soap-server",
    location="http://localhost:8000/",
    action="http://localhost:8000/",
    namespace="http://localhost:8000/",
    trace=True,
    ns=True,
)

# Registramos el servicio

dispatcher.register_function(
    "SumaDosNumeros",
    SumaDosNumeros,
    returns={"resultado": int},
    args={"x": int, "y": int}
)

dispatcher.register_function(
    "RestaDosNumeros",
    RestaDosNumeros,
    returns={"resultado": int},
    args={"x": int, "y": int}
)

dispatcher.register_function(
    "MultiplicaDosNumeros",
    MultiplicaDosNumeros,
    returns={"resultado": int},
    args={"x": int, "y": int}
)

dispatcher.register_function(
    "DivideDosNumeros",
    DivideDosNumeros,
    returns={"resultado": int},
    args={"x": int, "y": int}
)

# Iniciamos el servidor HTTP
server = HTTPServer(("0.0.0.0", 8000), SOAPHandler)
server.dispatcher = dispatcher
print("Servidor SOAP iniciado en http://localhost:8000/")
server.serve_forever()
