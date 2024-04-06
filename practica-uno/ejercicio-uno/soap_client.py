from zeep import Client

# Crear un cliente SOAP
client = Client('http://localhost:8000')

# Solicitar al usuario que ingrese dos números enteros
x = int(input("Ingrese el primer número entero: "))
y = int(input("Ingrese el segundo número entero: "))

# Llamar a las funciones del servicio SOAP con los valores ingresados
result1 = client.service.SumaDosNumeros(x=x, y=y)
result2 = client.service.RestaDosNumeros(x=x, y=y)
result3 = client.service.MultiplicaDosNumeros(x=x, y=y)
result4 = client.service.DivideDosNumeros(x=x, y=y)

# Imprimir los resultados
print(f"La suma de {x} y {y} es: {result1}")
print(f"La resta de {x} y {y} es: {result2}")
print(f"La multiplicación de {x} y {y} es: {result3}")
print(f"La división de {x} y {y} es: {result4}")