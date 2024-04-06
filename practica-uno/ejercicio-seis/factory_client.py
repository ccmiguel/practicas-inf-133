import requests
import json

url = "http://localhost:8000/animals"
headers = {"Content-Type": "application/json"}

# Crear un mamífero
data = {
    "animal_type": "Mammal",
    "nombre": "Elefante",
    "genero": "Masculino",
    "edad": 10,
    "peso": 4000,
    "gestation_period": 22
}

response = requests.post(url, json=data, headers=headers)
print(response.text)

# Crear un ave
data = {
    "animal_type": "Bird",
    "nombre": "Águila",
    "genero": "Femenino",
    "edad": 5,
    "peso": 6,
    "wingspan": 2
}

response = requests.post(url, json=data, headers=headers)
print(response.text)

# Crear un reptil
data = {
    "animal_type": "Reptile",
    "nombre": "Cocodrilo",
    "genero": "Masculino",
    "edad": 15,
    "peso": 500,
    "scale_type": "Escamoso"
}

response = requests.post(url, json=data, headers=headers)
print(response.text)

# Crear un anfibio
data = {
    "animal_type": "Amphibian",
    "nombre": "Rana",
    "genero": "Femenino",
    "edad": 2,
    "peso": 0.1,
    "skin_type": "Húmeda"
}

response = requests.post(url, json=data, headers=headers)
print(response.text)

# Crear un pez
data = {
    "animal_type": "Fish",
    "nombre": "Salmón",
    "genero": "Masculino",
    "edad": 3,
    "peso": 5,
    "habitat": "Agua dulce"
}

response = requests.post(url, json=data, headers=headers)
print(response.text)
