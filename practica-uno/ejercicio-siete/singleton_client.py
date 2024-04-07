import requests
import json

url = "http://localhost:8000/"

# Crear una partida
data = {"element": "piedra"}
response = requests.post(url + "games", json=data)
print(response.text)

# Listar todas las partidas
response = requests.get(url + "games")
print(response.text)

# Listar partidas con resultado "ganó"
response = requests.get(url + "games?resultado=ganó")
print(response.text)
