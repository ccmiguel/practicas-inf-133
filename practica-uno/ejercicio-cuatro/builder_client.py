import requests
import json

url = "http://localhost:8000/paciente"
headers = {'Content-type': 'application/json'}

mi_paciente = {
    "CI": "1234567",
    "nombre": "María",
    "apellido": "López",
    "edad": 30,
    "genero": "Femenino",
    "diagnostico": "Hipertensión",
    "doctor": "Dr. García"
}
response = requests.post(url, json=mi_paciente, headers=headers)
print(response.json())
