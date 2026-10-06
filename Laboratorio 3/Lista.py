# MÉTODO DE LISTA 

def buscar_en_lista(estudiantes, id_buscado):    # Recibe la lista de estudiantes y el id a buscar
    for estudiante in estudiantes:               # Se compara el id de cada estudiante en orden con el buscado hasta encontrarlo
        if estudiante.id == id_buscado:          # Se retorna el estudiante con el id correspondiente al buscado
            return estudiante
    return None

def insertar_en_lista(estudiantes, nuevo_estudiante):    # Recibe la lista de estudiantes y el nuevo a insertar
    estudiantes.append(nuevo_estudiante)                 # Se inserta con el método append, que lo pone al final de la lista


def listar_en_orden(estudiantes):                       # Recibe la lista de estudiantes (inicialmente desordenada)
    estudiantes_ordenados = estudiantes.copy()           # Hace una copia de la lista original para no modificarla
    estudiantes_ordenados.sort(key=lambda estudiante: estudiante.id)  # Se ordena por ID usando sort()
    return estudiantes_ordenados                          # Retorna la lista ya ordenada

def buscar_rango(estudiantes, inicio, fin):   # Función para buscar por rangos en una vista
    resultados = []                           #  Inicializa una lista donde se guardaran los estudiantes buscados

    for estudiante in estudiantes:            # Recorre cada estudiante, y si el Id está en el rango se inserta en resultado
        if inicio <= estudiante.id <= fin:
            resultados.append(estudiante)

    return resultados