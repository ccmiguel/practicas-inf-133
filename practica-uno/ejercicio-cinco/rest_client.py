import requests
import json

url = "http://localhost:8000/animales"
headers = {'Content-type': 'application/json'}

# Crear un animal
nuevo_animal = {
    "nombre": "León",
    "especie": "Panthera leo",
    "genero": "Masculino",
    "edad": 5,
    "peso": 180
}
response = requests.post(url, json=nuevo_animal, headers=headers)
print("Respuesta al agregar un nuevo animal:")
print(response.json())

# Listar todos los animales
response = requests.get(url)
print("\nLista de todos los animales:")
print(response.json())

# Buscar animales por especie
especie = "Panthera leo"
url_especie = f"{url}?especie={especie}"
response = requests.get(url_especie)
print(f"\nAnimales de la especie {especie}:")
print(response.json())

# Buscar animales por género
genero = "Masculino"
url_genero = f"{url}?genero={genero}"
response = requests.get(url_genero)
print(f"\nAnimales de género {genero}:")
print(response.json())

# Actualizar información de un animal
id_animal = 1
url_actualizar = f"{url}/{id_animal}"
datos_actualizados = {
    "edad": 6,
    "peso": 190
}
response = requests.put(url_actualizar, json=datos_actualizados, headers=headers)
print("\nRespuesta al actualizar la información de un animal:")
print(response.json())

# Eliminar un animal
id_animal_eliminar = 1
url_eliminar = f"{url}/{id_animal_eliminar}"
response = requests.delete(url_eliminar)
print("\nRespuesta al eliminar un animal:")
print(response.json())
