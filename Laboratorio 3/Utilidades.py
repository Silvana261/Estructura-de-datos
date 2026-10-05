import gc         # Importa el módulo garbage collector (recolector de basura).
import random
import time
from ArbolABB import ABB
from ArbolBMas import ArbolBMas
import Lista

class Estudiante:    # Define la clase que representa a un estudiante.
    def __init__(self, id, nombre, edad, promedio):
        self.id = id
        self.nombre = nombre
        self.edad = edad
        self.promedio = promedio

# Lista de nombres que pueden asignarse aleatoriamente a los estudiantes.
NOMBRES = ["Ana", "Carlos", "María", "Juan", "Laura", "Pedro", "Sofía", "Daniel","Valentina", "Andrés", "Camila", "Sebastián", "Natalia", "David", "Paula", "Mateo"]


# 1. DATOS
def generar_estudiantes(n, orden="aleatorio"):      # n indica cuántos estudiantes se quieren generar.  Y el orden significa si los IDs van a estar aleatorios u ordenados
    
    ids = random.sample(range(1000, 1000 + n), n)   # Genera n IDs únicos desde entre 1000 y 1000 + n -1. random.sample los genera sin repetir aleatoriamente
    if orden == "ordenado":       # Comprueba si se pidió que los estudiantes estén ordenados.
        ids.sort()                # Ordena los IDs de menor a mayor.
    estudiantes = []
    for i in ids:
        estudiantes.append(Estudiante(i, random.choice(NOMBRES), random.randint(18, 50), round(random.uniform(0.0, 10), 2) ))
        
    return estudiantes  # Se generan los estudiantes y se retorna la lista, ya sea con los IDs ordenados o aleatorios.


def generar_busquedas(estudiantes, m):      # Función para generar los m IDs que se van a buscar
    ids_a_buscar = []
    for i in estudiantes:
        ids_a_buscar.append(random.choice(estudiantes).id)  # Selecciona aleatoriamente IDs de los estudiantes a buscar
    return ids_a_buscar  


# 2. CRONÓMETRO
def medir(funcion, *args):     # función para medir cuánto tarda otra función.
                               # Ejecuta funcion(*args) y devuelve (segundos, resultado de la función ejecutada)
    gc.collect()     # Limpia objetos que ya no se están utilizando en memoria
    gc.disable()     # Desactiva temporalmente el recolector de basura. Esto evita que interfiera con la medición

    try:     # Intenta ejecutar la medición.
        
        t0 = time.perf_counter()    # Guarda el tiempo inicial en segundos

        resultado = funcion(*args)  # Ejecuta la función que se recibe cómo parámetro y *args permite enviarle los parámetros

        t1 = time.perf_counter()    # Guarda el tiempo final en segundos
    finally:     # Se vuelve a activar el recolector de basura al terminar el try siempre
        gc.enable()
    return t1 - t0, resultado     # Devuelve el tiempo en segundos y el resultado


# 3. FUNCIONES PARA FACILITAR LA CONSTRUCCIÓN EN TODAS LAS ESTRUCTURAS

def insertar_todos(estructura, estudiantes):    # Inserta todos los estudiantes en la estructura indicada
    
    if estructura == "lista":     # Si la estructura es una lista
        lista = []
        
        for e in estudiantes:   
            Lista.insertar_en_lista(lista, e)    # Inserta cada estudiante

        return lista   # Devuelve la lista con todos los estudiantes

    if estructura == "abb":    # Si la estructura es un ABB
        arbol = ABB()          # Crea un árbol binario de búsqueda vacío.      

        for e in estudiantes:  # Inserta cada estudiante con el método de ABB
            arbol.insertarABB(e)

        return arbol

    if estructura == "bmas":    # Si la estructura es un árbol B+
        arbol = ArbolBMas()     # Crea un B+ vacío

        for e in estudiantes:   # Inserta cada estudiante
            arbol.insertarBMas(e)

        return arbol    # Retorna el B+

    # Si se escribe una estructura que no existe
    raise ValueError(f"Estructura desconocida: {estructura}")


def buscar_para_todas_las_estructuras(estructura, objeto, ids):     # Función para realizar varias búsquedas
 # estructura es el tipo de estructura (lista, ABB, B+).objeto es la lista o árbol existente sobre el que se va a buscar y los ids que se van a buscar
    
    if estructura == "lista":   # Si es una lista, se busca cada id con la función definida para buscar en lista
        for i in ids:
            Lista.buscar_en_lista(objeto, i)

    elif estructura == "abb":   # Si es un ABB, se busca cada id con el método del ABB
        for i in ids:
            objeto.buscarABB(i)

    elif estructura == "bmas":   # Si es un árbol B+, se busca cada id con el método del B+
        for i in ids:
            objeto.buscarBMas(i)


def listar(estructura, objeto):     # Función para obtener todos los elementos ordenados, pero solo en memoria

    if estructura == "lista":   # Si es una lista
        return Lista.listar_en_orden(objeto)    # Si es una lista

    if estructura == "abb":     # Si es un ABB
        return objeto.listarEnOrden()           # Realiza el recorrido en orden del ABB.

    if estructura == "bmas":    # Si es un árbol B+
        return objeto.listarTodos()             # Obtiene todos los elementos del árbol B+ en orden.

# ------------------------------------------------------------ PRUEBA RÁPIDA
if __name__ == "__main__":
    for orden in ("aleatorio", "ordenado"):
        est = generar_estudiantes(1000, orden)
        ids = generar_busquedas(est, 100)
        for estr in ("lista", "abb", "bmas"):
            t_ins, obj = medir(insertar_todos, estr, est)
            t_bus, _ = medir(buscar_para_todas_las_estructuras, estr, obj, ids)
            t_lis, res = medir(listar, estr, obj)
            ordenado_ok = all(res[k].id < res[k + 1].id for k in range(len(res) - 1))
            h = obj.altura() if estr in ("abb", "bmas") else "-"
            print(f"{orden:9} {estr:5} ins={t_ins/1e6:8.2f}ms bus={t_bus/1e6:8.2f}ms "
                  f"lis={t_lis/1e6:7.2f}ms altura={h} listado_ordenado={ordenado_ok} n={len(res)}")