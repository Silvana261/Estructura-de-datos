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


# E1: INSERCIÓN
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


# ------------------------------------------------------------ E2: BÚSQUEDA POR ID
def experimento_2_busqueda(w):
    """Tiempo de M búsquedas por ID (todas de IDs existentes) sobre la estructura ya construida."""

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

    def buscar_lista(lista, ids):
        for i in ids:
            Lista.buscar_en_lista(lista, i)

    def buscar_abb(arbol, ids):
        for i in ids:
            arbol.buscarABB(i)

    def buscar_bmas(arbol, ids):
        for i in ids:
            arbol.buscarBMas(i)

    estructuras = {"lista": (construir_lista, buscar_lista),
                   "abb": (construir_abb, buscar_abb),
                   "bmas": (construir_bmas, buscar_bmas)}

    for orden in ORDENES:
        for n in TAMANOS:
            for rep in range(1, REPETICIONES + 1):
                estudiantes = generar_estudiantes(n, orden)
                ids = generar_busquedas(estudiantes, NUM_BUSQUEDAS_INDIVDUALES)     # mismas búsquedas para las 3 estructuras

                for estr, (construir, buscar) in estructuras.items():
                    objeto = construir(estudiantes)         # La construcción queda FUERA del cronómetro

                    # Solo se cronometran las M búsquedas
                    tiempo, _ = medir(buscar, objeto, ids)
                    w.writerow(["E2", estr, orden, n, NUM_BUSQUEDAS_INDIVDUALES, rep, tiempo, altura_de(estr, objeto)])

            print(f"[E2] orden={orden:9} N={n:6} listo ({REPETICIONES} repeticiones)")


# ------------------------------------------------------------ E3: LISTADO ASCENDENTE
def experimento_3_listado(w):
    """Tiempo de producir en memoria la secuencia ordenada de los N estudiantes (sin imprimir)."""

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

    def listar_lista(lista):
        return Lista.listar_en_orden(lista)     # copia y ordena con sort

    def listar_abb(arbol):
        return arbol.listarEnOrden()            # recorrido en orden

    def listar_bmas(arbol):
        return arbol.listarTodos()              # recorrido de las hojas enlazadas

    estructuras = {"lista": (construir_lista, listar_lista),
                   "abb": (construir_abb, listar_abb),
                   "bmas": (construir_bmas, listar_bmas)}

    for orden in ORDENES:
        for n in TAMANOS:
            for rep in range(1, REPETICIONES + 1):
                estudiantes = generar_estudiantes(n, orden)

                for estr, (construir, listar) in estructuras.items():
                    objeto = construir(estudiantes)         # fuera del cronómetro

                    tiempo, _ = medir(listar, objeto)
                    w.writerow(["E3", estr, orden, n, "", rep, tiempo, altura_de(estr, objeto)])

            print(f"[E3] orden={orden:9} N={n:6} listo ({REPETICIONES} repeticiones)")


# ------------------------------------------------------------ E5: BÚSQUEDA POR RANGO
def experimento_5_rango(w):
    """Tiempo de Q búsquedas por rango [a, b], cada una devolviendo K estudiantes.
    Solo se usan tamaños N >= K, porque un rango de K estudiantes no cabe en menos."""

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

    def rangos_lista(lista, rangos):
        for a, b in rangos:
            Lista.buscar_rango(lista, a, b)

    def rangos_abb(arbol, rangos):
        for a, b in rangos:
            arbol.buscar_rango(a, b)

    def rangos_bmas(arbol, rangos):
        for a, b in rangos:
            arbol.buscar_rango(a, b)

    estructuras = {"lista": (construir_lista, rangos_lista),
                   "abb": (construir_abb, rangos_abb),
                   "bmas": (construir_bmas, rangos_bmas)}

    # Si decides usar solo inserción aleatoria en E5, cambia ORDENES por ["aleatorio"]
    for orden in ORDENES:
        for n in TAMANOS:
            if n < TAMANO_RANGO:
                continue
            for rep in range(1, REPETICIONES + 1):
                estudiantes = generar_estudiantes(n, orden)
                rangos = generar_rangos(n, NUMERO_DE_RANGOS, TAMANO_RANGO)    # mismos rangos para las 3 estructuras

                for estr, (construir, buscar_rangos) in estructuras.items():
                    objeto = construir(estudiantes)         # fuera del cronómetro

                    tiempo, _ = medir(buscar_rangos, objeto, rangos)
                    w.writerow(["E5", estr, orden, n, NUMERO_DE_RANGOS, TAMANO_RANGO, rep, tiempo, altura_de(estr, objeto)])

            print(f"[E5] orden={orden:9} N={n:6} listo ({REPETICIONES} repeticiones)")


# ------------------------------------------------------------ PRINCIPAL
def correr(nombre, funcion, columnas):
    """Abre el CSV propio del experimento, escribe el encabezado y ejecuta el experimento."""
    os.makedirs("datos", exist_ok=True)
    archivo = f"datos/{nombre}.csv"
    with open(archivo, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(columnas)
        funcion(w)
    print(f"Datos crudos guardados en {archivo}\n")


def main():
    # Para correr solo algunos experimentos, comenta las líneas que no quieras.
    correr("e1_insercion", experimento_1_insercion, COLUMNAS)
    correr("e2_busqueda", experimento_2_busqueda, COLUMNAS)
    correr("e3_listado", experimento_3_listado, COLUMNAS)
    correr("e5_rango", experimento_5_rango, COLUMNAS_RANGO)


if __name__ == "__main__":
    main()