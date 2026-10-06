import csv
import gc
import os
import time

import Lista
from ArbolABB import ABB
from ArbolBMas import ArbolBMas
from GenerarDatos import generar_estudiantes, generar_busquedas, generar_rangos

# ------------------------------------------------------------ PARÁMETROS
PRUEBA = True   # True = corrida corta para verificar que todo funciona.
                # Cambiar a False para el experimento real.

M = 1000        # número de búsquedas por ID en cada medición (E2)
Q = 1000        # número de rangos por medición (E5)
K = 100         # cantidad de estudiantes que devuelve cada rango (E5)

if PRUEBA:
    TAMANOS = [10, 100, 1000]
    REPETICIONES = 3
else:
    TAMANOS = [10, 25, 50, 100, 500, 1000, 5000, 10000, 20000]
    REPETICIONES = 20      # número fijo de repeticiones para todos los N

ORDENES = ["aleatorio", "ordenado"]

COLUMNAS = ["experimento", "estructura", "orden", "N", "M", "rep", "tiempo_s", "altura"]
COLUMNAS_RANGO = ["experimento", "estructura", "orden", "N", "Q", "K", "rep", "tiempo_s", "altura"]


# ------------------------------------------------------------ CRONÓMETRO
def medir(funcion, *args):
    """Ejecuta funcion(*args) y devuelve (segundos, resultado). GC apagado durante la medición."""
    gc.collect()
    gc.disable()
    try:
        t0 = time.perf_counter()
        resultado = funcion(*args)
        t1 = time.perf_counter()
    finally:
        gc.enable()
    return t1 - t0, resultado


def altura_de(estr, objeto):
    """La altura se calcula DESPUÉS de medir (fuera del cronómetro). La lista no tiene."""
    return objeto.altura() if estr in ("abb", "bmas") else ""


# ------------------------------------------------------------ E1: INSERCIÓN
def experimento_1_insercion(w):
    """Tiempo de insertar N estudiantes, con IDs aleatorios y en orden creciente."""

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

    estructuras = {"lista": insertar_lista, "abb": insertar_abb, "bmas": insertar_bmas}

    for orden in ORDENES:
        for n in TAMANOS:
            for rep in range(1, REPETICIONES + 1):
                # Datos nuevos en cada repetición (sin seed); los mismos para las 3 estructuras
                estudiantes = generar_estudiantes(n, orden)

                for estr, insertar in estructuras.items():
                    # Solo se cronometra la inserción de los N estudiantes
                    tiempo, objeto = medir(insertar, estudiantes)
                    w.writerow(["E1", estr, orden, n, "", rep, tiempo, altura_de(estr, objeto)])

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
                ids = generar_busquedas(estudiantes, M)     # mismas búsquedas para las 3 estructuras

                for estr, (construir, buscar) in estructuras.items():
                    objeto = construir(estudiantes)         # La construcción queda FUERA del cronómetro

                    # Solo se cronometran las M búsquedas
                    tiempo, _ = medir(buscar, objeto, ids)
                    w.writerow(["E2", estr, orden, n, M, rep, tiempo, altura_de(estr, objeto)])

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
            if n < K:
                continue
            for rep in range(1, REPETICIONES + 1):
                estudiantes = generar_estudiantes(n, orden)
                rangos = generar_rangos(n, Q, K)    # mismos rangos para las 3 estructuras

                for estr, (construir, buscar_rangos) in estructuras.items():
                    objeto = construir(estudiantes)         # fuera del cronómetro

                    tiempo, _ = medir(buscar_rangos, objeto, rangos)
                    w.writerow(["E5", estr, orden, n, Q, K, rep, tiempo, altura_de(estr, objeto)])

            print(f"[E5] orden={orden:9} N={n:6} listo ({REPETICIONES} repeticiones)")


# ------------------------------------------------------------ PRINCIPAL
def correr(nombre, funcion, columnas):
    """Abre el CSV propio del experimento, escribe el encabezado y ejecuta el experimento."""
    os.makedirs("datos", exist_ok=True)
    archivo = f"datos/{nombre}_prueba.csv" if PRUEBA else f"datos/{nombre}.csv"
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