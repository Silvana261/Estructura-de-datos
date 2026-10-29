import os
import time
import random
import numpy as np
import matplotlib.pyplot as plt
import Quadtree
 
TAMANO = 20000                  # ciudad de 20000 x 20000 metros
RADIO = 500                     # metros
DISPERSION = 1500               # metros (desviación estándar de los barrios)
TAMANOS = [10, 20, 50, 100, 200, 500, 1000, 2000, 5000, 10000, 20000]   # valores de N
CONSULTAS = 200                 # consultas por cada N (se promedia)
REPETICIONES = 5                # repeticiones de la construcción (inserción)
REP_PROFUNDIDAD = 5             # veces que se generan datos nuevos para medir profundidad
 
 
# ---------- FUNCIONES AUXILIARES ----------
 
def generar(tipo, cantidad):
    if tipo == "uniforme":
        return Quadtree.generar_puntos_uniformes(cantidad, ancho_ciudad=TAMANO, largo_ciudad=TAMANO)
    return Quadtree.generar_puntos_realistas(cantidad, ancho_ciudad=TAMANO, largo_ciudad=TAMANO,
                                             dispersion_barrio=DISPERSION)
 
def profundidad(nodo):          # Profundidad máxima del árbol (la raíz sola tiene profundidad 0)
    if nodo.es_hoja:
        return 0
    mayor = 0
    for hijo in nodo.hijos:
        p = profundidad(hijo)
        if p > mayor:
            mayor = p
    return 1 + mayor
 
def construir_arbol(puntos):    # Devuelve (árbol, tiempo en segundos)
    inicio = time.perf_counter()
    raiz = Quadtree.Nodo_Quadtree(0, 0, TAMANO, TAMANO)
    for x, y in puntos:
        raiz.insertar_punto(x, y)
    return raiz, time.perf_counter() - inicio
 
def construir_lista(puntos):    # Fuerza bruta: "insertar" es agregar a una lista
    inicio = time.perf_counter()
    lista = []
    for x, y in puntos:
        lista.append((x, y))
    return lista, time.perf_counter() - inicio
 
def medir_construccion(funcion, puntos):    # Devuelve (estructura, media, desviación) entre repeticiones
    tiempos = []
    for i in range(REPETICIONES):
        estructura, tiempo = funcion(puntos)
        tiempos.append(tiempo)
    return estructura, np.mean(tiempos), np.std(tiempos)
 
def medir_consultas(funcion, consultas):    # Devuelve (media, desviación) entre consultas
    tiempos = []
    for cx, cy in consultas:
        inicio = time.perf_counter()
        funcion(cx, cy)
        tiempos.append(time.perf_counter() - inicio)
    return np.mean(tiempos), np.std(tiempos)
 
def medias(lista):              # De una lista de (media, desviación) saca las medias
    return [par[0] for par in lista]
 
def desviaciones(lista):        # ... y las desviaciones
    return [par[1] for par in lista]
 
def pendiente(ns, tiempos):     # Pendiente de la recta en escala log-log (ajuste sobre las medias)
    logs_n = [np.log10(n) for n in ns]
    logs_t = [np.log10(t) for t in tiempos]
    return np.polyfit(logs_n, logs_t, 1)[0]
 
def cruce(ns, t_arbol, t_bruta):
    # Menor N de la lista desde el cual el árbol es más rápido en ese N y en TODOS los mayores
    resultado = None
    for i in range(len(ns) - 1, -1, -1):        # se recorre de mayor a menor
        if t_arbol[i] < t_bruta[i]:
            resultado = ns[i]
        else:
            break
    return resultado
 
def texto_cruce(valor):
    if valor is None:
        return "el quadtree no es más rápido en ningún N probado"
    return f"N = {valor}"
 
def barras_error(medias_, desvs):
    # En escala log no puede haber barras que lleguen a 0 o negativo: se limita la inferior
    inferior = [min(d, m * 0.99) for m, d in zip(medias_, desvs)]
    return [inferior, desvs]
 
def n_cruce(ns, bruta, arbol):
    # Estima el N donde el quadtree empieza a ganar (y a seguir ganando).
    # Devuelve (valor, nota). bruta y arbol son listas de (media, desviación).
    factor = [bruta[i][0] / arbol[i][0] for i in range(len(ns))]
 
    i = len(ns) - 1
    if factor[i] < 1:
        return None, "nunca gana en los N probados"
 
    while i >= 0 and factor[i] >= 1:      # se retrocede mientras el árbol siga ganando
        i -= 1
 
    if i < 0:
        return ns[0], "gana desde el menor N probado (el cruce está por debajo)"
 
    # El cruce está entre ns[i] (pierde) y ns[i+1] (gana): se interpola en escala log-log
    x1, x2 = np.log10(ns[i]), np.log10(ns[i + 1])
    y1, y2 = np.log10(factor[i]), np.log10(factor[i + 1])
    x_cruce = x1 + (0 - y1) * (x2 - x1) / (y2 - y1)
    return 10 ** x_cruce, "estimado por interpolación"
 
 
# ---------- GRÁFICAS ----------
 
def graficar_loglog(ns, bruta, arbol, titulo, ylabel, archivo):
    # bruta y arbol son listas de (media, desviación)
    m_bruta = pendiente(ns, medias(bruta))
    m_arbol = pendiente(ns, medias(arbol))
 
    figura, eje = plt.subplots(figsize=(8, 6))
    eje.errorbar(ns, medias(bruta), yerr=barras_error(medias(bruta), desviaciones(bruta)),
                 fmt="o-", color="red", capsize=3,
                 label=f"Fuerza bruta (pendiente = {m_bruta:.2f})")
    eje.errorbar(ns, medias(arbol), yerr=barras_error(medias(arbol), desviaciones(arbol)),
                 fmt="s-", color="blue", capsize=3,
                 label=f"Quadtree (pendiente = {m_arbol:.2f})")
    eje.set_xscale("log")
    eje.set_yscale("log")
 
    # Línea vertical donde el quadtree empieza a ganar
    n_est, nota = n_cruce(ns, bruta, arbol)
    if n_est is not None and n_est > ns[0]:
        eje.axvline(n_est, color="green", linestyle="--",
                    label=f"El quadtree gana desde N ≈ {n_est:.0f}")
 
    eje.set_title(titulo)
    eje.set_xlabel("Cantidad de puntos N (escala logarítmica)")
    eje.set_ylabel(ylabel + " (escala logarítmica)")
    eje.grid(True, which="both", alpha=0.3)
    eje.legend()
    eje.text(0.5, -0.18, "Barras de error: ± 1 desviación estándar", transform=eje.transAxes,
             ha="center", fontsize=8)
 
    plt.savefig(archivo, dpi=150, bbox_inches="tight")
    plt.close()
    return m_bruta, m_arbol
 
def graficar_profundidad(ns, uniforme, realista, archivo):
    # uniforme y realista son listas de (media, desviación)
    figura, eje = plt.subplots(figsize=(9, 6))
    eje.errorbar(ns, medias(uniforme), yerr=desviaciones(uniforme), fmt="o-", color="green",
                 capsize=3, label="Uniforme")
    eje.errorbar(ns, medias(realista), yerr=desviaciones(realista), fmt="s-", color="purple",
                 capsize=3, label="Realista (barrios)")
    eje.set_xscale("log")
 
    # Valor medio escrito sobre cada punto
    for n, (m, d) in zip(ns, uniforme):
        eje.annotate(f"{m:.1f}", (n, m), textcoords="offset points", xytext=(0, -14),
                     ha="center", fontsize=8, color="green")
    for n, (m, d) in zip(ns, realista):
        eje.annotate(f"{m:.1f}", (n, m), textcoords="offset points", xytext=(0, 8),
                     ha="center", fontsize=8, color="purple")
 
    eje.set_title("Profundidad del quadtree según la distribución")
    eje.set_xlabel("Cantidad de puntos N (escala logarítmica)")
    eje.set_ylabel("Profundidad máxima del árbol")
    eje.grid(True, which="both", alpha=0.3)
    eje.legend()
    eje.text(0.5, -0.18, f"Media de {REP_PROFUNDIDAD} repeticiones, barras: ± 1 desviación estándar",
             transform=eje.transAxes, ha="center", fontsize=8)
 
    plt.savefig(archivo, dpi=150, bbox_inches="tight")
    plt.close()
 
def graficar_aceleracion(ns, series, archivo):
    # series: lista de (nombre, bruta, arbol, color)
    figura, eje = plt.subplots(figsize=(9, 6))
 
    for nombre, bruta, arbol, color in series:
        factor = [bruta[i][0] / arbol[i][0] for i in range(len(ns))]
        eje.plot(ns, factor, "o-", color=color, label=nombre)
 
        n_est, nota = n_cruce(ns, bruta, arbol)
        if n_est is not None and n_est > ns[0]:
            eje.axvline(n_est, color=color, linestyle="--", alpha=0.7)
            eje.annotate(f"N ≈ {n_est:.0f}", (n_est, 1), textcoords="offset points",
                         xytext=(5, 10), color=color, fontsize=9, rotation=90)
 
    eje.axhline(1, color="black", linewidth=1.5)          # línea de empate
 
    eje.set_xscale("log")
    eje.set_yscale("log")
    limite_inferior, limite_superior = eje.get_ylim()
    eje.axhspan(1, max(limite_superior, 10), color="green", alpha=0.08)
    eje.axhspan(min(limite_inferior, 0.1), 1, color="red", alpha=0.08)
    eje.set_ylim(limite_inferior, limite_superior)
 
    eje.text(0.02, 0.95, "Zona verde: el quadtree es más rápido", transform=eje.transAxes,
             color="green", fontsize=9, va="top")
    eje.text(0.02, 0.05, "Zona roja: la fuerza bruta es más rápida", transform=eje.transAxes,
             color="red", fontsize=9, va="bottom")
 
    eje.set_title("¿Desde qué N es mejor el quadtree?")
    eje.set_xlabel("Cantidad de puntos N (escala logarítmica)")
    eje.set_ylabel("Factor de aceleración = t fuerza bruta / t quadtree")
    eje.grid(True, which="both", alpha=0.3)
    eje.legend(loc="center left")
 
    plt.savefig(archivo, dpi=150, bbox_inches="tight")
    plt.close()
 
 
# ---------- EXPERIMENTO 1: PROFUNDIDAD ----------
 
def experimento_profundidad():
    print("\nEXPERIMENTO 1: profundidad (uniforme vs realista)")
    resultado_uniforme = []
    resultado_realista = []
 
    for n in TAMANOS:
        profs_u = []
        profs_r = []
        for i in range(REP_PROFUNDIDAD):          # datos nuevos en cada repetición
            arbol_u, t = construir_arbol(generar("uniforme", n))
            arbol_r, t = construir_arbol(generar("realista", n))
            profs_u.append(profundidad(arbol_u))
            profs_r.append(profundidad(arbol_r))
 
        resultado_uniforme.append((np.mean(profs_u), np.std(profs_u)))
        resultado_realista.append((np.mean(profs_r), np.std(profs_r)))
        print(f"N = {n:6d} | uniforme: {resultado_uniforme[-1][0]:5.1f} ± {resultado_uniforme[-1][1]:.2f}"
              f" | realista: {resultado_realista[-1][0]:5.1f} ± {resultado_realista[-1][1]:.2f}")
 
    graficar_profundidad(TAMANOS, resultado_uniforme, resultado_realista,
                         "graficas/analisis_profundidad.png")
 
 
# ---------- EXPERIMENTOS 2, 3 y 4: RENDIMIENTO ----------
 
def imprimir_tabla(nombre, bruta, arbol):
    print(f"\n{nombre}")
    print(f"{'N':>7} | {'bruta (us)':>20} | {'quadtree (us)':>20} | {'bruta/quadtree':>14}")
    for i in range(len(TAMANOS)):
        factor = bruta[i][0] / arbol[i][0]
        print(f"{TAMANOS[i]:7d} | {bruta[i][0]*1e6:10.1f} ± {bruta[i][1]*1e6:7.1f}"
              f" | {arbol[i][0]*1e6:10.1f} ± {arbol[i][1]*1e6:7.1f} | {factor:14.2f}")
 
def experimento_rendimiento():
    print("\nEXPERIMENTOS 2, 3 y 4: fuerza bruta vs quadtree (distribución realista)")
 
    ins_bruta, ins_arbol = [], []
    rad_bruta, rad_arbol = [], []
    vec_bruta, vec_arbol = [], []
 
    for n in TAMANOS:
        puntos = generar("realista", n)
 
        # Inserción
        lista, m, d = medir_construccion(construir_lista, puntos)
        ins_bruta.append((m, d))
        arbol, m, d = medir_construccion(construir_arbol, puntos)
        ins_arbol.append((m, d))
 
        # Mismas consultas para los dos métodos
        consultas = [(random.uniform(0, TAMANO), random.uniform(0, TAMANO)) for i in range(CONSULTAS)]
 
        # Búsqueda por radio
        rad_bruta.append(medir_consultas(
            lambda cx, cy: Quadtree.busqueda_radio_fuerza_bruta(lista, cx, cy, RADIO), consultas))
        rad_arbol.append(medir_consultas(
            lambda cx, cy: arbol.consultar_en_radio(cx, cy, RADIO), consultas))
 
        # Vecino más cercano
        vec_bruta.append(medir_consultas(
            lambda cx, cy: Quadtree.vecino_mas_cercano_fuerza_bruta(lista, cx, cy), consultas))
        vec_arbol.append(medir_consultas(
            lambda cx, cy: arbol.vecino_mas_cercano(cx, cy), consultas))
 
        print(f"N = {n} listo")
 
    # Tablas con media ± desviación y factor de aceleración
    imprimir_tabla("INSERCIÓN (tiempo total)", ins_bruta, ins_arbol)
    imprimir_tabla("BÚSQUEDA POR RADIO (tiempo por consulta)", rad_bruta, rad_arbol)
    imprimir_tabla("VECINO MÁS CERCANO (tiempo por consulta)", vec_bruta, vec_arbol)
 
    # Gráficas log-log con pendientes, barras de error y línea del cruce
    m1 = graficar_loglog(TAMANOS, ins_bruta, ins_arbol, "Inserción de N puntos",
                         "Tiempo total (s)", "graficas/analisis_insercion.png")
    m2 = graficar_loglog(TAMANOS, rad_bruta, rad_arbol, f"Búsqueda por radio ({RADIO} m)",
                         "Tiempo por consulta (s)", "graficas/analisis_radio.png")
    m3 = graficar_loglog(TAMANOS, vec_bruta, vec_arbol, "Vecino más cercano",
                         "Tiempo por consulta (s)", "graficas/analisis_vecino.png")
 
    # Gráfica del factor de aceleración (para ver el cruce)
    graficar_aceleracion(TAMANOS, [
        ("Inserción", ins_bruta, ins_arbol, "gray"),
        ("Búsqueda por radio", rad_bruta, rad_arbol, "blue"),
        ("Vecino más cercano", vec_bruta, vec_arbol, "orange"),
    ], "graficas/analisis_aceleracion.png")
 
    print("\nPENDIENTES (log-log):")
    print(f"Inserción      | bruta: {m1[0]:.2f} | quadtree: {m1[1]:.2f}")
    print(f"Radio          | bruta: {m2[0]:.2f} | quadtree: {m2[1]:.2f}")
    print(f"Vecino cercano | bruta: {m3[0]:.2f} | quadtree: {m3[1]:.2f}")
 
    print("\n¿DESDE QUÉ N GANA EL QUADTREE? (primer N de la lista, en ese N y en todos los mayores)")
    print("Inserción      :", texto_cruce(cruce(TAMANOS, medias(ins_arbol), medias(ins_bruta))))
    print("Radio          :", texto_cruce(cruce(TAMANOS, medias(rad_arbol), medias(rad_bruta))))
    print("Vecino cercano :", texto_cruce(cruce(TAMANOS, medias(vec_arbol), medias(vec_bruta))))
 
    print("\nN ESTIMADO DEL CRUCE (interpolado):")
    for nombre, b, a in [("Inserción", ins_bruta, ins_arbol),
                         ("Radio", rad_bruta, rad_arbol),
                         ("Vecino cercano", vec_bruta, vec_arbol)]:
        n_est, nota = n_cruce(TAMANOS, b, a)
        if n_est is None:
            print(f"{nombre:15}: {nota}")
        else:
            print(f"{nombre:15}: N ≈ {n_est:.0f} ({nota})")
 
    # ¿Cuántas consultas compensan el costo de construir el árbol? (con el N más grande)
    print(f"\nCONSULTAS NECESARIAS PARA COMPENSAR LA CONSTRUCCIÓN (N = {TAMANOS[-1]}):")
    costo_extra = ins_arbol[-1][0] - ins_bruta[-1][0]
    ahorro_radio = rad_bruta[-1][0] - rad_arbol[-1][0]
    ahorro_vecino = vec_bruta[-1][0] - vec_arbol[-1][0]
    if ahorro_radio > 0:
        print(f"Radio          : {costo_extra / ahorro_radio:.0f} consultas")
    if ahorro_vecino > 0:
        print(f"Vecino cercano : {costo_extra / ahorro_vecino:.0f} consultas")
 
 
if __name__ == "__main__":
    random.seed(1)                      # resultados repetibles
    os.makedirs("graficas", exist_ok=True)
    experimento_profundidad()
    experimento_rendimiento()
    print("\nListo. Gráficas guardadas en graficas/")
 