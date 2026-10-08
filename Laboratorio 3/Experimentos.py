import csv
import gc
import os
import time

import Lista
from ArbolABB import ABB
from ArbolBMas import ArbolBMas
from GenerarDatos import generar_estudiantes, generar_busquedas, generar_rangos

# Parámetros
NUM_BUSQUEDAS_INDIVDUALES = 1000        # número de búsquedas por ID en cada medición  (M)
NUMERO_DE_RANGOS = 1000                    # número de rangos por medición en la búqueda por rangos (Q)
TAMANO_RANGO = 100         # Número de estudiantes que devuelve cada búsqueda por rango (K)

TAMANOS = [10, 25, 50, 100, 500, 1000, 5000, 10000, 20000]   # número de estudiantes con los que corre el experimento
REPETICIONES = 13                                           # Número de repeticiones por experimento

ORDENES = ["aleatorio", "ordenado"]   # El orden en el que pueden estar insertados los daatos

# Columnas de las tablas de los resultados crudos CSV
COLUMNAS = ["experimento", "estructura", "orden", "N", "M", "rep", "tiempo_s", "altura"] # N: número de estudiantes en esa corrida. M:Número de busquedas.rep: número de repeticiones
COLUMNAS_RANGO = ["experimento", "estructura", "orden", "N", "Q", "K", "rep", "tiempo_s", "altura"]    # K: número de estudiantes en el rango 


# CRONÓMETRO
def medir(funcion, *args):   # Recibe una función y una cantidad variable de argumentos que serán enviados a esa función.

    gc.collect()       # Ejecuta el recolector de basura para liberar objetos que ya no se están utilizando antes de comenzar la medición.
    gc.disable()       # Desactiva temporalmente el recolector de basura para evitar que interfiera con la medición del tiempo de ejecución.
    try:               
        t0 = time.perf_counter()     # Guarda el tiempo exacto justo antes de ejecutar la función.
        resultado = funcion(*args)   # Ejecuta la función recibida utilizando los argumentos enviados.
        t1 = time.perf_counter()     # Guarda el tiempo justo después de terminar la ejecución de la función
    finally:
        gc.enable()     # Vuelve a activar el recolector de basura después de realizar la medición
    return t1 - t0, resultado  # Calcula el tiempo que tardó la función (tiempo final - tiempo inicial) y devuelve tanto el tiempo de ejecución como el resultado obtenido.


def altura_de(estr, objeto):   # Función para calcular la altura del árbol que se reciba en objeto
    return objeto.altura() if estr in ("abb", "bmas") else ""     # se retorna la altura del árbol ya sea ABB o B+ llamando sus métodos


#  ------------------ E1: INSERCIÓN ------------------
def experimento_1_insercion(w):       # 'w' se utiliza para escribir los resultados en un archivo CSV.
    """Tiempo de insertar N estudiantes, con IDs aleatorios y en orden creciente."""

    # Se hacen funciones auxiliares para insertar los mismos estudiantes en cada una de las estructuras, creando las estructuras y llamando sus respectivos métodos
    def insertar_lista(estudiantes):  
        lista = []
        for e in estudiantes:
            Lista.insertar_en_lista(lista, e)
        return lista

    def insertar_abb(estudiantes):
        arbol = ABB()
        for e in estudiantes:
            arbol.insertarABB(e)
        return arbol

    def insertar_bmas(estudiantes):
        arbol = ArbolBMas()
        for e in estudiantes:
            arbol.insertarBMas(e)
        return arbol
    # Crea un diccionario que relaciona el nombre de cada estructura con la función encargada de realizar sus inserciones.  Esto permite ejecutar las tres estructuras mediante un mismo ciclo.
    estructuras = {"lista": insertar_lista, "abb": insertar_abb, "bmas": insertar_bmas}

    for orden in ORDENES:        # Recorre los diferentes órdenes en los que se pueden generar los estudiantes
        for n in TAMANOS:        # Recorre los diferentes tamaños de datos que se pueden probar.
            for rep in range(1, REPETICIONES + 1):  # Se repite el experimento con el mismo tamaño y orden de inserción 20 veces
                
                estudiantes = generar_estudiantes(n, orden)      # Genera una nueva colección de N estudiantes.  # Los datos son los mismos que se utilizarán para probar todas las estructuras

                for estr, insertar in estructuras.items():     # Recorre cada estructura y obtiene su función de inserción.
                    
                    tiempo, objeto = medir(insertar, estudiantes)  # Ejecuta la función de inserción y mide únicamente el tiempo que tarda en insertar esos estudiantes
                    w.writerow(["E1", estr, orden, n, "", rep, tiempo, altura_de(estr, objeto)])   # Escribe el CSV con el resultado por filas

            print(f"[E1] orden={orden:9} N={n:6} listo ({REPETICIONES} repeticiones)")


# ----------- E2: BÚSQUEDA POR ID -------------
def experimento_2_busqueda(w):
    """Tiempo de M búsquedas a IDs aleatorios existentes sobre la estructura ya construida."""
    # Se construyen funciones auxiliares para construir cada estructura y para llamar el respectivo método de búsqueda
    def construir_lista(estudiantes):
        lista = []
        for e in estudiantes:
            Lista.insertar_en_lista(lista, e)
        return lista

    def construir_abb(estudiantes):
        arbol = ABB()
        for e in estudiantes:
            arbol.insertarABB(e)
        return arbol

    def construir_bmas(estudiantes):
        arbol = ArbolBMas()
        for e in estudiantes:
            arbol.insertarBMas(e)
        return arbol

    def buscar_lista(lista, ids):    # Funciones auxiliares para llamar cada método de búsqueda, pasandole a cada una la estructura y los ids a buscar
        for i in ids:
            Lista.buscar_en_lista(lista, i)

    def buscar_abb(arbol, ids):
        for i in ids:
            arbol.buscarABB(i)

    def buscar_bmas(arbol, ids):
        for i in ids:
            arbol.buscarBMas(i)
    # Diccionario que relaciona cada estructura con la función que permite construirla y la función que permite realizar las búsquedas
    estructuras = {"lista": (construir_lista, buscar_lista), "abb": (construir_abb, buscar_abb), "bmas": (construir_bmas, buscar_bmas)}

    for orden in ORDENES:     # Se recorren los diferentes órdenes en los que se pueden generar los estudiantes
        for n in TAMANOS:     # Se repite el experimento con los diferentes tamaños de estudiantes
            for rep in range(1, REPETICIONES + 1):           # Se repite 20 veces cada experimento con los mismos n estudiantes y el mismo orden
                estudiantes = generar_estudiantes(n, orden)  # Se generan los n estudiantes utilizando el orden actual
                ids_a_buscar = generar_busquedas(estudiantes, NUM_BUSQUEDAS_INDIVDUALES)     # Se generan los M = 1000 ids a buscar con la función generar busquedas dentro de los estudiantes generados

                for estr, (construir, buscar) in estructuras.items():
                    objeto = construir(estudiantes)                      # Se construye cada estructura con los mismos estudiantes y el tiempo que tarda en construirse no se incluye en el experimento

                    tiempo, _ = medir(buscar, objeto, ids_a_buscar)      # Se mide el tiempo de realizar las M búsquedas con cada objeto
                                                                         # como no se necesita los estudiantes que retornan las funciones, se guardan en _
                                                                         
                    # Se guardan en el archivo del eperimento 2, donde cada columna describe la estructura, orden, número de estudiantes, número de búsquedas, repeticiones, tiempo del exp, y la altura del árbol                                                  
                    w.writerow(["E2", estr, orden, n, NUM_BUSQUEDAS_INDIVDUALES, rep, tiempo, altura_de(estr, objeto)])

            print(f"[E2] orden={orden:9} N={n:6} listo ({REPETICIONES} repeticiones)")   # Se va mostrando el progreso 


# ------------ E3: LISTADO ASCENDENTE   -------------
def experimento_3_listado(w):
    """Tiempo de producir en memoria la secuencia ordenada de los N estudiantes (sin imprimir)."""

    # Se construyen funciones auxiliares para construir cada estructura e insertar los estudiantes llamando sus métodos
    def construir_lista(estudiantes):
        lista = []
        for e in estudiantes:
            Lista.insertar_en_lista(lista, e) 
        return lista

    def construir_abb(estudiantes):
        arbol = ABB()
        for e in estudiantes:
            arbol.insertarABB(e)
        return arbol

    def construir_bmas(estudiantes):
        arbol = ArbolBMas()
        for e in estudiantes:
            arbol.insertarBMas(e)
        return arbol

    # Se hacen funciones auxiliares para llamar cada método que lista los estudiantes en orden de cada estructura
    def listar_lista(lista):
        return Lista.listar_en_orden(lista)     # copia y ordena con sort

    def listar_abb(arbol):
        return arbol.listarEnOrden()            # recorrido en orden

    def listar_bmas(arbol):
        return arbol.listarTodos()              # recorrido de las hojas enlazadas

    # Se hace un diccionario que relaciona cada estructura con su función para construirla y listar los elementos
    estructuras = {"lista": (construir_lista, listar_lista), "abb": (construir_abb, listar_abb),  "bmas": (construir_bmas, listar_bmas)}

    for orden in ORDENES:    # Se recorren los diferentes órdenes en los que se pueden generar los estudiantes
        for n in TAMANOS:    # Se repite el experimento con los diferentes tamaños de estudiantes
            for rep in range(1, REPETICIONES + 1):             # Se repite 20 veces cada experimento con los mismos n estudiantes y el mismo orden
                estudiantes = generar_estudiantes(n, orden)    # Se generan los estudiantes en el orden correspondiente

                for estr, (construir, listar) in estructuras.items():     # Probamos el listado en cada una de las estructuras recorriendo el diccionario 
                    objeto = construir(estudiantes)         # Construimos cada estructura con los mismo estudiantes, se hace fuera del cronómetro porque no hace parte del experimento

                    tiempo, _ = medir(listar, objeto)       # Se mide el tiempo en el que cada estructura lista los n estudiantes, pasandole la funcion y el parámetro que es el objeto                    
                    
                    # Se guarda el resultado en el archivo del experimento 3, donde las columnas son la estructura, el orden de los datos, número de estudiantes, "" porque no hay búsquedas en este experimento, las repeticiones, tiempo y altura de la estructura
                    w.writerow(["E3", estr, orden, n, "", rep, tiempo, altura_de(estr, objeto)])

            print(f"[E3] orden={orden:9} N={n:6} listo ({REPETICIONES} repeticiones)")   # Se muestra el progreso cada ciclo completado


# ------------- E5: BÚSQUEDA POR RANGO ----------------
def experimento_5_rango(w):
    """Tiempo de Q búsquedas por rango [a, b], cada una devolviendo K estudiantes.
    Solo se usan tamaños N >= K, porque un rango de K estudiantes no cabe en menos."""

    # Funciones auxiliares para construir cada estructura 
    def construir_lista(estudiantes):
        lista = []
        for e in estudiantes:
            Lista.insertar_en_lista(lista, e)
        return lista

    def construir_abb(estudiantes):
        arbol = ABB()
        for e in estudiantes:
            arbol.insertarABB(e)
        return arbol

    def construir_bmas(estudiantes):
        arbol = ArbolBMas()
        for e in estudiantes:
            arbol.insertarBMas(e)
        return arbol
    # Funciones auxiliares para realizar las búsquedas por rango, llamando al método de cada estructura
    # Para cada estructura se hace un ciclo para buscar cada rango que será generado por otra función
    def rangos_lista(lista, rangos):
        for a, b in rangos:
            Lista.buscar_rango(lista, a, b)

    def rangos_abb(arbol, rangos):
        for a, b in rangos:
            arbol.buscar_rango(a, b)

    def rangos_bmas(arbol, rangos):
        for a, b in rangos:
            arbol.buscar_rango(a, b)
    # Diccionario donde para cada estructura se guarda la función auxiliar para construir la estructura y buscar por rangos
    estructuras = {"lista": (construir_lista, rangos_lista),"abb": (construir_abb, rangos_abb), "bmas": (construir_bmas, rangos_bmas)}

    for orden in ORDENES:          # Se hace el experimento de búsqueda por rangos insertando los estudiantes en orden y en desorden 
        for n in TAMANOS:          # Se prueban también todos los tamaños de estudiantes
            if n < TAMANO_RANGO:   # Se verifica que el rango de estudiantes (100) sea menor que el número de estudiantes total para que sea posible buscarlos. 
                continue           # Si n es menor, se prueba con con otro tamaño
            for rep in range(1, REPETICIONES + 1):            # Para cada combinación se hace 15 repeticiones
                estudiantes = generar_estudiantes(n, orden)   # Se generan los estudiantes según el orden 
                rangos = generar_rangos(n, NUMERO_DE_RANGOS, TAMANO_RANGO)    # Se generan 1000 rangos de 100 estudiantes, que serán los mismos para las 3 estructuras para que sea justo

                for estr, (construir, buscar_rangos) in estructuras.items():  
                    objeto = construir(estudiantes)                    # Construye las estructuras fuera del croónometro, ya que se mide únicamente el tiempo de búsqueda
                    tiempo, _ = medir(buscar_rangos, objeto, rangos)   # Se mide el tiempo en el que la estructura correspondiente realiza la búsqueda de todos los rangos
                    # Se escribe el resultado directamente en el CSV del experimento #5
                    w.writerow(["E5", estr, orden, n, NUMERO_DE_RANGOS, TAMANO_RANGO, rep, tiempo, altura_de(estr, objeto)])

            print(f"[E5] orden={orden:9} N={n:6} listo ({REPETICIONES} repeticiones)")


# --------------- PRINCIPAL ---------------
def correr(nombre, funcion, columnas):
    """Abre el CSV propio del experimento, escribe el encabezado y ejecuta el experimento."""
    os.makedirs("datos", exist_ok=True)      # Crea la carpeta "datos" si todavía no existe.
    archivo = f"datos/{nombre}.csv"          # Construye la ruta del archivo utilizando el nombre recibido.
    with open(archivo, "w", newline="", encoding="utf-8") as f:       # Abre el archivo en modo escritura ("w")
        w = csv.writer(f)       
        w.writerow(columnas)        # Escribe la primera fila del CSV, que contiene los nombres de las columnas
        funcion(w)                  # La función del experimento será la encargada de realizar las pruebas
    print(f"Datos crudos guardados en {archivo}\n")


def main():
    """ Función principal del programa. Ejecuta todos los experimentos definidos y guarda cada uno en su propio archivo CSV."""
    correr("e1_insercion", experimento_1_insercion, COLUMNAS)
    correr("e2_busqueda", experimento_2_busqueda, COLUMNAS)
    correr("e3_listado", experimento_3_listado, COLUMNAS)
    correr("e5_rango", experimento_5_rango, COLUMNAS_RANGO)     # Se utiliza COLUMNAS_RANGO porque este experimento tiene información adicional relacionada con los rangos.


if __name__ == "__main__":      # Punto de entrada del programa
    main()