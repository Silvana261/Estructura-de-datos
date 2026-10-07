import random

ID_INICIO = 1000    # primer ID posible; los IDs van de ID_INICIO a ID_INICIO + n - 1

NOMBRES = ["Ana", "Carlos", "María", "Juan", "Laura", "Pedro", "Sofía", "Daniel",                 # Lista de nombres posibles para generar los estudiantes
           "Valentina", "Andrés", "Camila", "Sebastián", "Natalia", "David", "Paula", "Mateo"]


class Estudiante:    # Define la clase que representa a un estudiante.
    def __init__(self, id, nombre, edad, promedio):
        self.id = id
        self.nombre = nombre
        self.edad = edad
        self.promedio = promedio


def generar_estudiantes(n, orden="aleatorio"):      # Función para generar los estudiantes, recibe n: cantidad de estudiantes y el orden: si van a ser aleatorios u ordenados por ID
    """n estudiantes con IDs únicos de ID_INICIO a ID_INICIO + n - 1.
    orden = 'aleatorio' -> IDs mezclados; 'ordenado' -> IDs crecientes.
    La lista devuelta está en el orden en que se van a insertar."""
    ids = random.sample(range(1000, 1000 + n), n)   #  Se generan aleatoriamente los ids únicos de manera aleatoria
    if orden == "ordenado":       # Si los estudiantes se van a generar en orden
        ids.sort()                # Se ordenan los ids de manera ascendente   
    estudiantes = []
    for i in ids:    # Se crea cada estudiante, asignandole un id, escogiendo un nombre aleatorio, una edad aleatoria entre 18 y 50, y un promedio aleatorio
        estudiantes.append(Estudiante(i, random.choice(NOMBRES), random.randint(18, 50), round(random.uniform(0.0, 5.0), 2)))
    return estudiantes


def generar_busquedas(estudiantes, m):    # Función para escoger los m ids existentes a buscar

    ids_a_buscar = []
    for _ in range(m):     
        ids_a_buscar.append(random.choice(estudiantes).id)    # Se escogen aleatoriamente los estudiantes y se devuelve una lista de los ids a buscar
    return ids_a_buscar


def generar_rangos(n, q, k):     # Función para generar los rangos de búsquedas. n: cantidad total de estudiantes, q: número de consultas, k cantidad de estudiantes en el rango

    rangos = []
    for _ in range(q):  
        a = random.randint(ID_INICIO, ID_INICIO + n - k)  # Se escoge el id de inicio de forma aleatoria entre los posibles, restandole k para que no se salga del rango
        rangos.append((a, a + k - 1))   # Calcula el id de fin del rango sumandoles k-1 al id del inicio
    return rangos   # Retorna los rangos


# ------------------------------------------------------------ PRUEBA RÁPIDA
if __name__ == "__main__":
    est = generar_estudiantes(100, "ordenado")
    print("ordenado:", est[0].id, "...", est[-1].id, "| n =", len(est))   # 1000 ... 1099 | n = 100
    est = generar_estudiantes(100, "aleatorio")
    print("aleatorio, IDs únicos:", len({e.id for e in est}) == 100)
    print("búsquedas:", len(generar_busquedas(est, 1000)))                # 1000
    rangos = generar_rangos(100, 5, 10)
    print("rangos:", rangos)                                              # cada uno con b - a = 9