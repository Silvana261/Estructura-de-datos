import os
import time
import random
import numpy as np
import matplotlib.pyplot as plt
import Quadtree

TAMANO = 40000                  # ciudad de 20000 x 20000 metros
RADIO = 500                     # Las búsquedas por radio serán de 500 metros
DISPERSION = 1500               # metros (desviación estándar de los barrios)
TAMANOS = [10, 20, 50, 100, 200, 500, 1000, 2000, 5000, 10000, 20000,40000]   # valores de N (número de puntos)
CONSULTAS = 200                 # consultas por cada N (se promedia)
REPETICIONES = 50               # Número de repeticiones de cada experimento

#  FUNCIONES AUXILIARES 

# FUNCIÓN PARA GENERAR LOS DATOS
def generar(tipo, cantidad):  # Función para generar los puntos tanto uniformes como realistas con los barrios
    if tipo == "uniforme":
        return Quadtree.generar_puntos_uniformes(cantidad, ancho_ciudad=TAMANO, largo_ciudad=TAMANO)
    return Quadtree.generar_puntos_realistas(cantidad, ancho_ciudad=TAMANO, largo_ciudad=TAMANO, dispersion_barrio=DISPERSION)


# FUNCIÓN PARA CALCULAR LA PROFUNDIDAD DEL ÁRBOL
def profundidad(nodo):          # Profundidad máxima del árbol (la raíz sola tiene profundidad 0)
    if nodo.es_hoja:            # Si un nodo es hoja, no tiene hijos, entonces su profundidad es cero 
        return 0
    mayor = 0                   # Guarda la profundidad más alta que encuentre entre los hijos
    for hijo in nodo.hijos:     # Recorre los 4 hijos del nodo actual
        p = profundidad(hijo)   # Llama recursivamente la función para calcular la profundidad de cada hijo
        if p > mayor:           # Actualiza la variable si la profundidad devuelta por el hijo es mayor a la actual
            mayor = p
    return 1 + mayor            # Al irse devolviendo sumará uno por cada hijo hasta llegar al padre 


# FUNCIONES PARA CONSTRUIR LAS DOS ESTRUCTURAS
def construir_arbol(puntos):        # Toma el tiempo de construcción del árbol
    inicio = time.perf_counter()    # Se inicia el contador de tiempo
    raiz = Quadtree.Nodo_Quadtree(0, 0, TAMANO, TAMANO)    # Se construye el árbol
    for x, y in puntos:              # Se inserta cada punto en el árbol
        raiz.insertar_punto(x, y)
    return raiz, time.perf_counter() - inicio     # Retorna el árbol y el tiempo

def construir_lista(puntos):    # Fuerza bruta: "insertar" es agregar a una lista
    inicio = time.perf_counter()   # Se inicia el contador de tiempo
    lista = []                     # Se inicializa la estructura 
    for x, y in puntos:            # Se inserta cada punto
        lista.append((x, y))       
    return lista, time.perf_counter() - inicio   # Retorna la lista y el tiempo


# FUNCIONES PARA MEDIR LOS TIEMPOS
def medir_construccion(funcion, puntos):    # Toma alguna de las dos funciones anteriores para construir la estructura tantas veces
    tiempos = []                                  # Lista donde se almacenarán los tiempos 
    for i in range(REPETICIONES):                 # Se repite el experimento tantas repeticiones se hayan definido
        estructura, tiempo = funcion(puntos)      
        tiempos.append(tiempo)                    # El tiempo devuelto se agrega a la lista
    return estructura, np.mean(tiempos), np.std(tiempos)     # Retorna la estructura, el promedio del tiempo de las repeticiones y la desviación estándar 

def medir_consultas(funcion, consultas):    # Función para medir el tiempo de la consulta (radio o vecino)
    tiempos = []                      # lista donde se alamcenarán los tiempos
    for cx, cy in consultas:          # Por cada consulta
        inicio = time.perf_counter()  # Se incia el contador de tiempo
        funcion(cx, cy)               # Se llama a la función 
        tiempos.append(time.perf_counter() - inicio)     # Se agrega el tiempo a la lista
    return np.mean(tiempos), np.std(tiempos)             # Se retorna el tiempo promedio de esas consultas y la desviación estandar

# FUNCIONES PARA SACAR LAS ESTADÍSTICAS
def medias(lista):              # De una lista de (media, desviación) saca las medias
    return [par[0] for par in lista]

def desviaciones(lista):        # ... y las desviaciones
    return [par[1] for par in lista]

def pendiente(tamanos_n, tiempos):     # Pendiente de la recta en escala log-log (ajuste sobre las medias)
    logs_n = [np.log10(n) for n in tamanos_n]
    logs_t = [np.log10(t) for t in tiempos]
    return np.polyfit(logs_n, logs_t, 1)[0]  # Calcula la pendiente logarítmica con polyfit

def barras_error(medias_, desvs):
    # En escala log no puede haber barras que lleguen a 0 o negativo: se limita la inferior
    inferior = [min(d, m * 0.99) for m, d in zip(medias_, desvs)]
    return [inferior, desvs]


# FUNCIÓN PARA CALCULAR DESDE QUE N ES MEJOR QUADTREE
def cruce(tamanos_n, t_arbol, t_bruta):
    # Menor N de la lista desde el cual el árbol es más rápido en ese N y en TODOS los mayores
    resultado = None
    for i in range(len(tamanos_n) - 1, -1, -1):    # se recorre de mayor a menor los tamaños de N
        if t_arbol[i] < t_bruta[i]:         # Si el tiempo para ese N fue menor en el árbol 
            resultado = tamanos_n[i]               #  Se actualiza la variable con el valor de N
        else:
            break
    if resultado is None:
        return None, "nunca gana en los N probados" # Si resultado nunca tomo un valor, el Quadtree no fue más rápido
    return resultado, "punto exacto de la lista" # Como es de adelante hacia atrás, al final queda el primer N en el que el Quadtree fue más rápido
  

#  GRÁFICAS 

def graficar_loglog(tamanos_n, bruta, arbol, titulo, ylabel, archivo):
    m_bruta = pendiente(tamanos_n, medias(bruta))
    m_arbol = pendiente(tamanos_n, medias(arbol))

    figura, eje = plt.subplots(figsize=(8, 6))
    eje.errorbar(tamanos_n, medias(bruta), yerr=barras_error(medias(bruta), desviaciones(bruta)),
                 fmt="o-", color="#5355F4", capsize=3, label=f"Fuerza bruta (pendiente = {m_bruta:.2f})")
    eje.errorbar(tamanos_n, medias(arbol), yerr=barras_error(medias(arbol), desviaciones(arbol)),
                 fmt="s-", color="#F354E0", capsize=3, label=f"Quadtree (pendiente = {m_arbol:.2f})")
    eje.set_xscale("log")
    eje.set_yscale("log")

    n_cruce_val, mensaje = cruce(tamanos_n, medias(arbol), medias(bruta))
    
    if n_cruce_val is not None:
        eje.axvline(n_cruce_val, color="green", linestyle="--",
                    label=f"El quadtree gana desde N ≈ {n_cruce_val}")
    
    eje.set_title(titulo)
    eje.set_xlabel("Cantidad de puntos N (escala logarítmica)")
    eje.set_ylabel(ylabel + " (escala logarítmica)")
    eje.grid(True, which="both", alpha=0.3)
    eje.legend()
    
    plt.savefig(archivo, dpi=150, bbox_inches="tight")
    plt.close()
    return m_bruta, m_arbol

def graficar_profundidad(tamanos_n, uniforme, realista, archivo):
    # uniforme y realista son listas de (media, desviación)
    figura, eje = plt.subplots(figsize=(9, 6))
    eje.errorbar(tamanos_n, medias(uniforme), yerr=desviaciones(uniforme), fmt="o-", color="green",
                 capsize=3, label="Uniforme")
    eje.errorbar(tamanos_n, medias(realista), yerr=desviaciones(realista), fmt="s-", color="purple",
                 capsize=3, label="Realista (barrios)")
    eje.set_xscale("log")

    # Valor medio escrito sobre cada punto
    for n, (m, d) in zip(tamanos_n, uniforme):
        eje.annotate(f"{m:.1f}", (n, m), textcoords="offset points", xytext=(0, -14),
                     ha="center", fontsize=8, color="green")
    for n, (m, d) in zip(tamanos_n, realista):
        eje.annotate(f"{m:.1f}", (n, m), textcoords="offset points", xytext=(0, 8),
                     ha="center", fontsize=8, color="purple")

    eje.set_title("Profundidad del quadtree según la distribución")
    eje.set_xlabel("Cantidad de puntos N (escala logarítmica)")
    eje.set_ylabel("Profundidad máxima del árbol")
    eje.grid(True, which="both", alpha=0.3)
    eje.legend()
    eje.text(0.5, -0.18, f"Media de {REPETICIONES} repeticiones, barras: ± 1 desviación estándar",
             transform=eje.transAxes, ha="center", fontsize=8)

    plt.savefig(archivo, dpi=150, bbox_inches="tight")
    plt.close()


# EXPERIMENTO 1: PROFUNDIDAD 

def experimento_profundidad():   # Función para construir varios árboles con distintos tamaños de N para promediar su profundidad
    print("\nEXPERIMENTO 1: profundidad (uniforme vs realista)")
    resultado_uniforme = []  # Se inicializan las listas donde se guardarán los resultados
    resultado_realista = []

    for n in TAMANOS:   # Se varia la cantidad de puntos en cada experimento
        profudindad_uniforme = []        # Se inicializa las listas donde se guardará la profundidad de los árboles construidos con el mismo n
        profundidad_realista = []   
        for i in range(REPETICIONES):    # Para cada N, se repite una cantidad de veces
            arbol_uniforme, tiempo = construir_arbol(generar("uniforme", n))     # Se construye y toma el tiempo del árbol con datos aleatorios y realistas 
            arbol_realista, tiempo = construir_arbol(generar("realista", n))    
            profudindad_uniforme.append(profundidad(arbol_uniforme))             # Se calcula la profundidad del árbol y se agrega a la lista
            profundidad_realista.append(profundidad(arbol_realista))

        resultado_uniforme.append((np.mean(profudindad_uniforme), np.std(profudindad_uniforme)))   # Al final de las repeticiones, se promedia las profundidades y se saca la desviación estándar
        resultado_realista.append((np.mean(profundidad_realista), np.std(profundidad_realista)))   
        print(f"N = {n:6d} | uniforme: {resultado_uniforme[-1][0]:5.1f} ± {resultado_uniforme[-1][1]:.2f}"
              f" | realista: {resultado_realista[-1][0]:5.1f} ± {resultado_realista[-1][1]:.2f}")

    graficar_profundidad(TAMANOS, resultado_uniforme, resultado_realista,  # Se llama la función para graficar 
                         "graficas/analisis_profundidad.png")


#  EXPERIMENTOS 2, 3 y 4: RENDIMIENTO 

def experimento_rendimiento():
    print("\nEXPERIMENTOS 2, 3 y 4: fuerza bruta vs quadtree (distribución realista)")

    insercion_bruta, insercion_arbol = [], []  # Se inicializa las listas donde se alamacenarán los resultados con árbol y fuerza bruta
    rad_bruta, rad_arbol = [], []
    vec_bruta, vec_arbol = [], []

    for n in TAMANOS:   # Se experimenta con los N número de puntos
        puntos = generar("realista", n)   # Se generan los puntos con distribución realista

        # Inserción
        lista, promedio, desviacion = medir_construccion(construir_lista, puntos)   # Se llama a la función que con la cantidad de puntos que se le pasa, la cual construirá la estructura y duvuelve el promedio y la desviación de las repeticiones
        insercion_bruta.append((promedio, desviacion))  # Se inserta en la lista el promedio y desviación como resultado de ese tamaño de N
        arbol, promedio, desviacion = medir_construccion(construir_arbol, puntos)   # Se hace lo mismo con el árbol
        insercion_arbol.append((promedio, desviacion))

        # Mismas consultas para los dos métodos
        consultas = [(random.uniform(0, TAMANO), random.uniform(0, TAMANO)) for i in range(CONSULTAS)]  # Se hace una lista con las coordenadas de las consultas 

        # BÚSQUEDA POR RADIO:
        # Función auxiliar para llamar a la función de búsqueda por radio de fuerza bruta
        def radio_bruta(cx, cy):
            return Quadtree.busqueda_radio_fuerza_bruta(lista, cx, cy, RADIO)
        rad_bruta.append(medir_consultas(radio_bruta, consultas)) # Luego llama a la función auxiliar para que retorne el promedio y la desviación de las repeticiones para esa búsqueda por radio
        # Función auxiliar para la búsqueda por radio usando el Quadtree
        def radio_arbol(cx, cy): 
            return arbol.consultar_en_radio(cx, cy, RADIO)
        rad_arbol.append(medir_consultas(radio_arbol, consultas))  # Llama a la misma función auxiliar pero con el árbol

        # VECINO MÁS CERCANO:
        # Función auxiliar para buscar el vecino más cercano mediante fuerza bruta
        def vecino_bruta(cx, cy):
            return Quadtree.vecino_mas_cercano_fuerza_bruta(lista, cx, cy)
        vec_bruta.append(medir_consultas(vecino_bruta, consultas))
        # Función auxiliar para buscar el vecino más cercano usando el Quadtree
        def vecino_arbol(cx, cy):
            return arbol.vecino_mas_cercano(cx, cy)
        vec_arbol.append(medir_consultas(vecino_arbol, consultas))
        print(f"N = {n} listo")


    # Gráficas log-log con pendientes, barras de error y línea del cruce
    m1 = graficar_loglog(TAMANOS, insercion_bruta, insercion_arbol, "Inserción de N puntos",
                         "Tiempo total (s)", "graficas/analisis_insercion.png")
    m2 = graficar_loglog(TAMANOS, rad_bruta, rad_arbol, f"Búsqueda por radio ({RADIO} m)",
                         "Tiempo por consulta (s)", "graficas/analisis_radio.png")
    m3 = graficar_loglog(TAMANOS, vec_bruta, vec_arbol, "Vecino más cercano",
                         "Tiempo por consulta (s)", "graficas/analisis_vecino.png")


if __name__ == "__main__":
                
    os.makedirs("graficas", exist_ok=True)
    experimento_profundidad()
    experimento_rendimiento()
    print("\nListo. Gráficas guardadas en graficas/")