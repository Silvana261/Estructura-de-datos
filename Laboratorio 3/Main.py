import random
import time
from ArbolABB import ABB
import Lista
from ArbolBMas import ArbolBMas

class Estudiante:   # Clase que representa a un estudiante con su información
    
    def __init__(self, id, nombre, edad, promedio):
        self.id = id
        self.nombre = nombre
        self.edad = edad
        self.promedio = promedio
    
    
def generar_estudiantes(cantidad):    # Función para generar los estudiantes
    
    estudiantes = []
    nombres = ["Ana","Carlos","María","Juan","Laura","Pedro","Sofía","Daniel","Valentina","Andrés","Camila","Sebastián","Natalia","David","Paula","Mateo"]

    ids = list(range(1001,11001))  # Se crean 10000 ids diferentes
    
    random.shuffle(ids)            # Mezclamos los ids aleatoriamente, de forma que estén en un orden aleatorio
    
    for i in range(cantidad):
        
        estudiante = Estudiante(id = ids[i], nombre = random.choice(nombres),  edad = random.randint(18,50), promedio = round(random.uniform(0.0, 10), 2)) # Unimorm genera un decimal aleatorio y round lo redondea a dos decimales
        
        estudiantes.append(estudiante)
    return estudiantes




estudiantes = generar_estudiantes(10000)      # Generamos los 10.000 estudiantes una sola vez
ids_buscar = random.sample([estudiante.id for estudiante in estudiantes], 100) # Elegimos los mismos 100 IDs para ambos experimentos

# Dos órdenes de inserción
ordenes = {
    "Experimento 1 - Aleatorio": estudiantes.copy(),
    "Experimento 2 - Ordenado": sorted(
        estudiantes, key=lambda estudiante: estudiante.id
    )
}

def probar_estructuras(nombre, datos):
    print("\n" + "=" * 55)
    print(nombre)
    print("=" * 55)

    # LISTA
    lista = []
    inicio = time.perf_counter()
    for estudiante in datos:
        Lista.insertar_en_lista(lista, estudiante)
    tiempo_insertar = time.perf_counter() - inicio

    inicio = time.perf_counter()
    for id_buscado in ids_buscar:
        Lista.buscar_en_lista(lista, id_buscado)
    tiempo_buscar = time.perf_counter() - inicio

    print("LISTA")
    print(f"Inserción: {tiempo_insertar:.6f} segundos")
    print(f"Búsqueda de 100 IDs: {tiempo_buscar:.6f} segundos")

    # ABB
    abb = ABB()
    inicio = time.perf_counter()
    for estudiante in datos:
        abb.insertarABB(estudiante)
    tiempo_insertar = time.perf_counter() - inicio

    inicio = time.perf_counter()
    for id_buscado in ids_buscar:
        abb.buscarABB(id_buscado)
    tiempo_buscar = time.perf_counter() - inicio

    print("\nABB")
    print(f"Inserción: {tiempo_insertar:.6f} segundos")
    print(f"Búsqueda de 100 IDs: {tiempo_buscar:.6f} segundos")

    # ÁRBOL B+
    bmas = ArbolBMas(grado=50)
    inicio = time.perf_counter()
    for estudiante in datos:
        bmas.insertarBMas(estudiante)
    tiempo_insertar = time.perf_counter() - inicio

    inicio = time.perf_counter()
    for id_buscado in ids_buscar:
        bmas.buscarBMas(id_buscado)
    tiempo_buscar = time.perf_counter() - inicio

    print("\nÁRBOL B+")
    print(f"Inserción: {tiempo_insertar:.6f} segundos")
    print(f"Búsqueda de 100 IDs: {tiempo_buscar:.6f} segundos")


for nombre, datos in ordenes.items():
    probar_estructuras(nombre, datos)