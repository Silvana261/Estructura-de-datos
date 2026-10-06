import random

ID_INICIO = 1000    # primer ID posible; los IDs van de ID_INICIO a ID_INICIO + n - 1

NOMBRES = ["Ana", "Carlos", "María", "Juan", "Laura", "Pedro", "Sofía", "Daniel",
           "Valentina", "Andrés", "Camila", "Sebastián", "Natalia", "David", "Paula", "Mateo"]


class Estudiante:    # Define la clase que representa a un estudiante.
    def __init__(self, id, nombre, edad, promedio):
        self.id = id
        self.nombre = nombre
        self.edad = edad
        self.promedio = promedio


def generar_estudiantes(n, orden="aleatorio"):
    """n estudiantes con IDs únicos de ID_INICIO a ID_INICIO + n - 1.
    orden = 'aleatorio' -> IDs mezclados; 'ordenado' -> IDs crecientes.
    La lista devuelta está en el orden en que se van a insertar."""
    ids = random.sample(range(ID_INICIO, ID_INICIO + n), n)   # IDs únicos, mezclados
    if orden == "ordenado":
        ids.sort()                                            # de menor a mayor
    estudiantes = []
    for i in ids:
        estudiantes.append(Estudiante(i, random.choice(NOMBRES),
                                      random.randint(18, 50),
                                      round(random.uniform(0.0, 10), 2)))
    return estudiantes


def generar_busquedas(estudiantes, m):
    """m IDs elegidos al azar (con reemplazo) entre los estudiantes que sí existen."""
    ids_a_buscar = []
    for _ in range(m):
        ids_a_buscar.append(random.choice(estudiantes).id)
    return ids_a_buscar


def generar_rangos(n, q, k):
    """q rangos (a, b) de exactamente k IDs. Como los IDs son consecutivos,
    el rango [a, a + k - 1] siempre contiene k estudiantes. Requiere n >= k."""
    rangos = []
    for _ in range(q):
        a = random.randint(ID_INICIO, ID_INICIO + n - k)
        rangos.append((a, a + k - 1))
    return rangos


# ------------------------------------------------------------ PRUEBA RÁPIDA
if __name__ == "__main__":
    est = generar_estudiantes(100, "ordenado")
    print("ordenado:", est[0].id, "...", est[-1].id, "| n =", len(est))   # 1000 ... 1099 | n = 100
    est = generar_estudiantes(100, "aleatorio")
    print("aleatorio, IDs únicos:", len({e.id for e in est}) == 100)
    print("búsquedas:", len(generar_busquedas(est, 1000)))                # 1000
    rangos = generar_rangos(100, 5, 10)
    print("rangos:", rangos)                                              # cada uno con b - a = 9