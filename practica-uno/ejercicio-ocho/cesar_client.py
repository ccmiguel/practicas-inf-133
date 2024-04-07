import requests
import json

url = "http://localhost:8000/messages"

# Crear un mensaje
data = {"content": "Hola, mundo!"}
response = requests.post(url, json=data)
print(response.text)

# Listar todos los mensajes
response = requests.get(url)
print(response.text)

# Buscar mensaje por ID
response = requests.get(url + "/1")
print(response.text)

# Actualizar contenido de un mensaje
data = {"content": "Hola, Mundo! Este es un mensaje actualizado."}
response = requests.put(url + "/1", json=data)
print(response.text)

# Eliminar un mensaje
response = requests.delete(url + "/1")
print(response.text)
