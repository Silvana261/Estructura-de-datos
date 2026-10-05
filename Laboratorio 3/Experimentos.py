import csv
import os

from Utilidades import generar_estudiantes, insertar_en_todas_las_estructuras, medir

# ------------------------------------------------------------ PARÁMETROS
PRUEBA = True   # True = corrida corta para verificar que todo funciona.
                # Cambiar a False para el experimento real.

if PRUEBA:
    TAMANOS = [10, 100, 1000]
    REPS_NORMAL, REPS_PEQUENO = 3, 3
else:
    TAMANOS = [10, 25, 50, 100, 500, 1000, 5000, 10000, 20000]
    REPS_NORMAL, REPS_PEQUENO = 20, 30     # 30 repeticiones si N <= 50

ESTRUCTURAS = ["lista", "abb", "bmas"]
ORDENES = ["aleatorio", "ordenado"]
ARCHIVO = "datos/resultados_prueba.csv" if PRUEBA else "datos/resultados_crudos.csv"

COLUMNAS = ["experimento", "estructura", "orden", "N", "M", "rep", "tiempo_s", "altura"]


def repeticiones(n):
    return REPS_PEQUENO if n <= 50 else REPS_NORMAL


# ------------------------------------------------------------ E1: INSERCIÓN
def experimento_1_insercion(w):
    """Mide cuánto tarda insertar N estudiantes en cada estructura,
    con IDs en orden aleatorio y en orden creciente."""
    for orden in ORDENES:
        for n in TAMANOS:
            for rep in range(1, repeticiones(n) + 1):

                # Datos nuevos en cada repetición (sin seed).
                # Los mismos datos para las 3 estructuras dentro de la repetición.
                estudiantes = generar_estudiantes(n, orden)

                for estr in ESTRUCTURAS:
                    # Solo se cronometra la inserción de los N estudiantes
                    tiempo, objeto = medir(insertar_en_todas_las_estructuras, estr, estudiantes)

                    # La altura se calcula DESPUÉS de medir (fuera del cronómetro)
                    altura = objeto.altura() if estr in ("abb", "bmas") else ""

                    w.writerow(["E1", estr, orden, n, "", rep, tiempo, altura])

            print(f"[E1] orden={orden:9} N={n:6} listo ({repeticiones(n)} repeticiones)")


# ------------------------------------------------------------ PRINCIPAL
def main():
    os.makedirs("datos", exist_ok=True)
    with open(ARCHIVO, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(COLUMNAS)

        experimento_1_insercion(w)
        # experimento_2_busqueda(w)   <- se agrega después
        # experimento_3_listado(w)    <- se agrega después

    print(f"\nDatos crudos guardados en {ARCHIVO}")


if __name__ == "__main__":
    main()