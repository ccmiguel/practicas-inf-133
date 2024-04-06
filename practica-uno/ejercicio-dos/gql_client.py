import requests

# Definir la URL del servidor GraphQL
url = 'http://localhost:8000/graphql'

# Definir la consulta GraphQL para listar todas las plantas
query_lista = """
{
    plantas {
        id
        nombre_comun
        especie
        edad_meses
        altura_cm
        tiene_frutos
    }
}
"""

# Definir la consulta GraphQL para buscar plantas por especie
query_buscar_por_especie = """
query BuscarPlantasPorEspecie($especie: String!) {
    plantasPorEspecie(especie: $especie) {
        id
        nombre_comun
        especie
        edad_meses
        altura_cm
        tiene_frutos
    }
}
"""

# Definir la consulta GraphQL para buscar plantas que tienen frutos
query_buscar_con_frutos = """
{
    plantasConFrutos {
        id
        nombre_comun
        especie
        edad_meses
        altura_cm
        tiene_frutos
    }
}
"""

# Definir la consulta GraphQL para crear una nueva planta
query_crear = """
mutation {
    crearPlanta(nombreComun: "Orquídea", especie: "Orchidaceae", edadMeses: 12, alturaCm: 25, tieneFrutos: false) {
        planta {
            id
            nombre_comun
            especie
            edad_meses
            altura_cm
            tiene_frutos
        }
    }
}
"""

# Definir la consulta GraphQL para actualizar la información de una planta
query_actualizar = """
mutation {
    actualizarPlanta(id: 1, nombreComun: "Cactus", especie: "Cactaceae", edadMeses: 18, alturaCm: 30, tieneFrutos: true) {
        planta {
            id
            nombre_comun
            especie
            edad_meses
            altura_cm
            tiene_frutos
        }
    }
}
"""

# Definir la consulta GraphQL para eliminar una planta
query_eliminar = """
mutation {
    eliminarPlanta(id: 2) {
        planta {
            id
            nombre_comun
            especie
            edad_meses
            altura_cm
            tiene_frutos
        }
    }
}
"""

# Realizar solicitudes POST al servidor GraphQL
response = requests.post(url, json={'query': query_lista})
print("Listar todas las plantas:")
print(response.text)

response = requests.post(url, json={'query': query_buscar_por_especie, 'variables': {'especie': 'Cactaceae'}})
print("\nBuscar plantas por especie (Cactaceae):")
print(response.text)

response = requests.post(url, json={'query': query_buscar_con_frutos})
print("\nBuscar plantas que tienen frutos:")
print(response.text)

response = requests.post(url, json={'query': query_crear})
print("\nCrear una nueva planta:")
print(response.text)

response = requests.post(url, json={'query': query_actualizar})
print("\nActualizar la información de una planta:")
print(response.text)

response = requests.post(url, json={'query': query_eliminar})
print("\nEliminar una planta:")
print(response.text)
