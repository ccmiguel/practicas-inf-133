import requests

# URL del servidor RESTful
url = "http://localhost:8000/"

# Obtener todos los pacientes
ruta_get_pacientes = url + "pacientes"
get_pacientes_response = requests.get(ruta_get_pacientes)
print("Lista de todos los pacientes:")
print(get_pacientes_response.text)

# Agregar un nuevo paciente
ruta_post_paciente = url + "pacientes"
nuevo_paciente = {
    "CI": "1234566",
    "nombre": "Juan",
    "apellido": "Ramirez",
    "edad": 35,
    "género": "Masculino",
    "diagnóstico": "Diabetes",
    "doctor": "Dr. Ramos",
}
post_paciente_response = requests.post(ruta_post_paciente, json=nuevo_paciente)
print("\nRespuesta al agregar un nuevo paciente:")
print(post_paciente_response.text)


# Obtener paciente por CI
ci_paciente = "1234567"
ruta_get_paciente_ci = url + f"pacientes?CI={ci_paciente}"
get_paciente_ci_response = requests.get(ruta_get_paciente_ci)
print(f"\nPaciente con CI {ci_paciente}:")
print(get_paciente_ci_response.text)

# Filtrar pacientes por diagnóstico
diagnostico = "Diabetes"
ruta_get_pacientes_diagnostico = url + f"pacientes?diagnóstico={diagnostico}"
get_pacientes_diagnostico_response = requests.get(ruta_get_pacientes_diagnostico)
print(f"\nPacientes con diagnóstico de {diagnostico}:")
print(get_pacientes_diagnostico_response.text)

# Filtrar pacientes por doctor
doctor = "Dr. García"
ruta_get_pacientes_doctor = url + f"pacientes?doctor={doctor}"
get_pacientes_doctor_response = requests.get(ruta_get_pacientes_doctor)
print(f"\nPacientes atendidos por el doctor {doctor}:")
print(get_pacientes_doctor_response.text)


# Actualizar información de un paciente
ci_paciente_actualizar = "1234567"
ruta_put_paciente = url + f"pacientes/{ci_paciente_actualizar}"
datos_actualizados = {
    "edad": 35,
    "diagnóstico": "Diabetes",
}
put_paciente_response = requests.put(ruta_put_paciente, json=datos_actualizados)
print("\nRespuesta al actualizar la información de un paciente:")
print(put_paciente_response.text)

# Eliminar un paciente
ruta_delete_paciente = url + f"pacientes/{ci_paciente_actualizar}"
delete_paciente_response = requests.delete(ruta_delete_paciente)
print("\nRespuesta al eliminar un paciente:")
print(delete_paciente_response.text)
