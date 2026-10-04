import gc
import random
import time

from ArbolABB import ABB
from ArbolBMas import ArbolBMas
import Lista


class Estudiante:
    def __init__(self, id, nombre, edad, promedio):
        self.id = id
        self.nombre = nombre
        self.edad = edad
        self.promedio = promedio


NOMBRES = ["Ana", "Carlos", "María", "Juan", "Laura", "Pedro", "Sofía", "Daniel",
           "Valentina", "Andrés", "Camila", "Sebastián", "Natalia", "David", "Paula", "Mateo"]


# ---------------------------------------------------------------- 1. DATOS
def generar_estudiantes(n, orden="aleatorio"):
    """Genera n estudiantes con IDs únicos.
    Los IDs se muestrean de un rango 10 veces mayor que n (así hay IDs libres
    que sirven como 'inexistentes' en las búsquedas fallidas).
    orden = 'aleatorio' -> IDs mezclados; 'ordenado' -> IDs crecientes."""
    ids = random.sample(range(1, 10 * n + 1), n)   # sin repetición
    if orden == "ordenado":
        ids.sort()
    return [Estudiante(i, random.choice(NOMBRES), random.randint(18, 50),
                       round(random.uniform(0.0, 10), 2)) for i in ids]


def generar_busquedas(estudiantes, m, existentes=True):
    """m IDs de búsqueda al azar (con reemplazo).
    existentes=True  -> IDs que sí están en la estructura.
    existentes=False -> IDs que NO están (peor caso de la lista)."""
    if existentes:
        return [random.choice(estudiantes).id for _ in range(m)]
    usados = {e.id for e in estudiantes}
    n = len(estudiantes)
    inexistentes = []
    while len(inexistentes) < m:
        candidato = random.randint(1, 10 * n)
        if candidato not in usados:
            inexistentes.append(candidato)
    return inexistentes


# ------------------------------------------------------------ 2. CRONÓMETRO
def medir(funcion, *args):
    """Ejecuta funcion(*args) y devuelve (nanosegundos, resultado).
    El GC se apaga solo durante la medición; antes se hace un collect()."""
    gc.collect()
    gc.disable()
    try:
        t0 = time.perf_counter_ns()
        resultado = funcion(*args)
        t1 = time.perf_counter_ns()
    finally:
        gc.enable()
    return t1 - t0, resultado


# --------------------------------------------------------- 3. CONSTRUCCIÓN
def insertar_todos(estructura, estudiantes):
    """Inserta todos los estudiantes en la estructura indicada
    ('lista', 'abb' o 'bmas'). Es lo que se cronometra en E1."""
    if estructura == "lista":
        lista = []
        for e in estudiantes:
            Lista.insertar_en_lista(lista, e)
        return lista
    if estructura == "abb":
        arbol = ABB()
        for e in estudiantes:
            arbol.insertarABB(e)
        return arbol
    if estructura == "bmas":
        arbol = ArbolBMas()
        for e in estudiantes:
            arbol.insertarBMas(e)
        return arbol
    raise ValueError(f"Estructura desconocida: {estructura}")


def buscar_todos(estructura, objeto, ids):
    """Busca cada ID de la lista 'ids'. Es lo que se cronometra en E2."""
    if estructura == "lista":
        for i in ids:
            Lista.buscar_en_lista(objeto, i)
    elif estructura == "abb":
        for i in ids:
            objeto.buscarABB(i)
    elif estructura == "bmas":
        for i in ids:
            objeto.buscarBMas(i)


def listar(estructura, objeto):
    """Produce la secuencia ordenada en memoria (sin imprimir). Es E3."""
    if estructura == "lista":
        return Lista.listar_en_orden(objeto)
    if estructura == "abb":
        return objeto.listarEnOrden()
    if estructura == "bmas":
        return objeto.listarTodos()

# ------------------------------------------------------------ PRUEBA RÁPIDA
if __name__ == "__main__":
    for orden in ("aleatorio", "ordenado"):
        est = generar_estudiantes(1000, orden)
        ids = generar_busquedas(est, 100)
        for estr in ("lista", "abb", "bmas"):
            t_ins, obj = medir(insertar_todos, estr, est)
            t_bus, _ = medir(buscar_todos, estr, obj, ids)
            t_lis, res = medir(listar, estr, obj)
            ordenado_ok = all(res[k].id < res[k + 1].id for k in range(len(res) - 1))
            h = obj.altura() if estr in ("abb", "bmas") else "-"
            print(f"{orden:9} {estr:5} ins={t_ins/1e6:8.2f}ms bus={t_bus/1e6:8.2f}ms "
                  f"lis={t_lis/1e6:7.2f}ms altura={h} listado_ordenado={ordenado_ok} n={len(res)}")