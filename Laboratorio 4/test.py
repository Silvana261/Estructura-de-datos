import os
import matplotlib.pyplot as plt 
import random 
import Quadtree

# 1. PRUEBAS PARA VERIFICAR QUE LOS RESULTADOS CON FUERZA BRUTA COINCIDAN CON LOS DEL QUADTREE
def prueba_coincidir():

    TAMANO = 20000  # Tamaño de la ciudad de prueba
    RADIO = 500     # Radio para probar la búsqueda por Radio

    # Primero se generan los datos, serán 10000 puntos, con una dispersión de 1500 metros (desviación estandar)
    puntos = Quadtree.generar_puntos_realistas(10000, ancho_ciudad = TAMANO, largo_ciudad = TAMANO, dispersion_barrio= 1500)

    # Se prueba la construcción del Quadtree
    raiz = Quadtree.Nodo_Quadtree(0,0, TAMANO, TAMANO)  # La raíz tendrá coordenadas (0,0) y será un cuadrado ya que el tamaño es igual en el eje x y en el y 
    puntos_insertados = 0                               # Contador para los puntos 

    for x, y in puntos:                # Ciclo que recorre cada punto generado anteriormente
        if raiz.insertar_punto(x,y):   # Se llama al método del Quadtree para insertar puntos
            puntos_insertados += 1     # Se incrementa el contador si la inserción fue exitosa

    print(f"\nCantidad de puntos en la lista: {len(puntos)}")          # Se muestra la cantidad de puntos generados e insertados
    print(f"\nCantidad de puntos en el QuadTree: {puntos_insertados}")

    if len(puntos) == puntos_insertados:               # Se comprueba que sea la misma cantidad los puntos de la lista que los del árbol
        print("\nTodos los puntos se insertaron")
    else:
        print("\nHay puntos que no se insertaron")

    # Se comparan los resultados con el árbol y con fuerza bruta en la búsqueda de radio
    for i in range(100):                       # Se generan 100  búsquedas de puntos a un radio

        centro_x = random.uniform(0, TAMANO)   # Se genera aleatoriamente los puntos sobre los que se va a hacer la búsqueda, delimitados por las dimensiones de la ciudad
        centro_y = random.uniform(0, TAMANO)    

        # Se realiza la búsqueda en el árbol y con fuerza bruta
        resultado_arbol = sorted(raiz.consultar_en_radio(centro_x, centro_y, RADIO))        # Las listas que retornan las dos funciones se ordenan para poder comparar
        resultado_bruta = sorted(Quadtree.busqueda_radio_fuerza_bruta(puntos, centro_x, centro_y, RADIO))
        assert resultado_arbol == resultado_bruta, f" Difieren en el punto ({centro_x}, {centro_y})"   # Con assert se verifica que los dos resultados coincidan, si no se muestra el punto del problema
    print("\nLas 100 consultas coinciden con fuerza bruta y el árbol")

    # Ahora comparar si coinciden los resultados en la búsqueda del vecino más cercano
    for i in range(100):                        # Se hacen 100 búsquedas del vecino más cercano

        consulta_x = random.uniform(0, TAMANO)    # Sobre puntos generados aleatoriamente dentro las dimensiones del cuadrante
        consulta_y = random.uniform(0, TAMANO)

        # Se realiza la búsqueda del vecino más cercano con fuerza bruta y en el árbol 
        resultado_arbol = raiz.vecino_mas_cercano(consulta_x, consulta_y)                                
        resultado_bruta = Quadtree.vecino_mas_cercano_fuerza_bruta(puntos, consulta_x, consulta_y)
        assert resultado_arbol == resultado_bruta, f"En el resultado difieren en ({consulta_x},{consulta_y})"  # Con assert se verifica que los dos resultados coincidan, si no se muestra el punto del problema

    print("\nLas 100 búsquedas coinciden con fuerza bruta y el árbol")

# 2. PRUEBAS UNITARIAS QUADTREE

PUNTOS_PEQUENOS = [(1, 1), (6, 2), (2, 3), (3, 1), (5, 5),(7, 6), (8, 2), (4, 7), (1, 8), (9, 9)]  # Puntos para las pruebas unitarias

# Inserción
def prueba_inserción():
    quadtree = Quadtree.Nodo_Quadtree(0, 0, 10, 10)  # Se hace un Quadtree de 10 metros de largo y ancho

    for x, y in PUNTOS_PEQUENOS:    # Se insertan 10 puntos dentro de la ciudad
        assert quadtree.insertar_punto(x,y) == True  # Con assert se verifica que todas las inserciones pasen

    # Pruebas de puntos fuera del árbol y de duplicados
    assert quadtree.insertar_punto(11, 11) == False  # Fuera del árbol
    assert quadtree.insertar_punto(12, 4) == False   # Fuera del eje x
    assert quadtree.insertar_punto(6, 11) == False   # Fuera del eje y
    assert quadtree.insertar_punto(1, 1) == False    # Duplicado

    print("\nTodas las pruebas de inserción pasaron")
    return quadtree  # Se retorna el árbol para las demás pruebas unitarias

# Búsqueda por radio (con el mismo árbol de la prueba anterior)
def prueba_radio():
    quadtree = prueba_inserción()  # Se reutiliza la prueba anterior

    assert quadtree.consultar_en_radio(6, 3, 2) == [(6, 2)]  # En cada consulta al radio, se verifica que coincidan los puntos que retorna la función con los que debería ser 
    assert sorted(quadtree.consultar_en_radio(2, 2, 2)) == [(1, 1), (2, 3), (3, 1)]
    assert sorted(quadtree.consultar_en_radio(5, 5, 3)) == [(4, 7), (5, 5), (7, 6)]
    assert quadtree.consultar_en_radio(5, 1, 0.5) == []

    print("\nTodas las pruebas de búsqueda a un radio fueron exitosas")
    
# Vecino más cercano (con el mismo árbol de la prueba anterior)
def prueba_vecino():
    quadtree = prueba_inserción()
    # De la lista que devuelve este método en la posición 0, está el punto
    assert quadtree.vecino_mas_cercano(6, 3)[0] == (6, 2)
    assert quadtree.vecino_mas_cercano(0, 0)[0] == (1, 1)

    print("\nPrueba del vecino más cercano exitosa")

# Función para escoger la prueba unitaria a realizar 
def pruebas_unitarias():
    while True:
        op = input("\n Escoger la prueba unitaria a realizar:\n 1. Probar inserciones.\n 2. Probar búsqueda por radio.\n 3. El vecino más cercano.\n 4. Salir\n")
        match op:
            case "1":
                prueba_inserción()
            case "2":
                prueba_radio()
            case "3":
                prueba_vecino()
            case "4":
                break
            case _:
                print("Opción inválida")


# FUNCIONES PARA VISUALIZAR EL ARBOL

def tamano_punto(puntos):   # Si hay pocos puntos, se ven más grandes
    if len(puntos) < 100:
        return 30
    else:
        return 3 

def dibujar_cuadrantes(nodo, eje):   # Dibuja el cuadro de cada hoja

    if nodo.es_hoja:
        rectangulo = plt.Rectangle((nodo.coordenada_x, nodo.coordenada_y), nodo.longitud_horizontal, nodo.longitud_vertical, fill = False, edgecolor = "black", linewidth=0.5)
        eje.add_patch(rectangulo)
    else:
        for hijo in nodo.hijos:
            dibujar_cuadrantes(hijo, eje)


def graficar_arbol(raiz, puntos, nombre_archivo, titulo="", color_puntos="red"):

    figura, eje = plt.subplots(figsize=(8, 8))
    
    dibujar_cuadrantes(raiz, eje)

    xs = [p[0] for p in puntos]
    ys = [p[1] for p in puntos]

    eje.scatter(xs, ys, color=color_puntos, s=tamano_punto(puntos))

    eje.set_title(titulo)
    eje.set_xlabel(f"Dimensiones de la ciudad: {raiz.longitud_horizontal} x {raiz.longitud_vertical} m | Cantidad de puntos: {len(puntos)}")

    plt.savefig(nombre_archivo, dpi=150)
    plt.close()

def graficar_radio(puntos, centro_x, centro_y, radio, encontrados, nombre_archivo,
                   titulo="", raiz=None, unidad="m"):
    figura, eje = plt.subplots(figsize=(8, 8))
    if raiz is not None:
        dibujar_cuadrantes(raiz, eje)
    xs = [p[0] for p in puntos]
    ys = [p[1] for p in puntos]

    eje.scatter(xs, ys, color="lightgray", s=tamano_punto(puntos), label="Puntos")

    if len(encontrados) > 0:

        xs_enc = [p[0] for p in encontrados]
        ys_enc = [p[1] for p in encontrados]

        eje.scatter(xs_enc, ys_enc, color="red", s=tamano_punto(puntos) * 3,
                    label="Dentro del radio (" + str(len(encontrados)) + ")")

    circulo = plt.Circle((centro_x, centro_y), radio, fill=False, color="blue")

    eje.add_patch(circulo)
    eje.scatter([centro_x], [centro_y], color="blue", marker="x", label="Consulta")

    eje.set_title(titulo)

    # Información debajo de la gráfica
    if raiz is not None:
        info = (f"Dimensiones de la ciudad: {raiz.longitud_horizontal} x {raiz.longitud_vertical} {unidad} | "
                f"Cantidad de puntos: {len(puntos)}")
    else:
        info = f"Cantidad de puntos: {len(puntos)}"

    info += f"\nConsulta: ({centro_x:g}, {centro_y:g}) | Radio: {radio:g} {unidad}"
    info += f"\nPuntos dentro del radio: {len(encontrados)}"

    # Coordenadas de los puntos encontrados (máximo 10, de 3 en 3 por línea)
    maximo = 10
    if len(encontrados) > 0:
        ordenados = sorted(encontrados)[:maximo]
        for i in range(0, len(ordenados), 3):
            grupo = ordenados[i:i + 3]
            info += "\n" + "   ".join(f"({x:.1f}, {y:.1f})" for x, y in grupo)
        if len(encontrados) > maximo:
            info += f"\n... y {len(encontrados) - maximo} más"

    eje.set_xlabel(info, fontsize=9)

    eje.legend()
    plt.savefig(nombre_archivo, dpi=150, bbox_inches="tight")
    plt.close()
    
def graficar_vecino(puntos, x_consulta, y_consulta, vecino, nombre_archivo,titulo="", raiz=None):

    figura, eje = plt.subplots(figsize=(8, 8))
    
    if raiz is not None:
        dibujar_cuadrantes(raiz, eje)

    xs = [p[0] for p in puntos]
    ys = [p[1] for p in puntos]

    eje.scatter(xs, ys, color="lightgray", s=tamano_punto(puntos), label="Puntos")
    eje.scatter([x_consulta], [y_consulta], color="blue", marker="x", label="Consulta")  

    if vecino is not None:
        eje.scatter([vecino[0]], [vecino[1]], color="magenta", s=tamano_punto(puntos) * 3, label="Vecino más cercano")
        eje.plot([x_consulta, vecino[0]], [y_consulta, vecino[1]], color="red", linestyle="--")

    eje.set_title(titulo)
    if raiz is not None:
        eje.set_xlabel(f"Dimensiones de la ciudad: {raiz.longitud_horizontal} x {raiz.longitud_vertical} m | Cantidad de puntos: {len(puntos)}")
    else:
        eje.set_xlabel(f"Cantidad de puntos: {len(puntos)}")

    # Mostrar siempre el punto de consulta y el resultado, incluso con muchos puntos.
    texto_consulta = f"Punto de consulta: ({x_consulta:.2f}, {y_consulta:.2f})"
    texto_vecino = f"Vecino más cercano: {vecino}"
    eje.text(0.02, 0.98, texto_consulta + "\n" + texto_vecino,
             transform=eje.transAxes, verticalalignment="top", fontsize=9,
             bbox=dict(boxstyle="round", facecolor="white", alpha=0.85))

    eje.legend(loc = "upper right")
    plt.savefig(nombre_archivo, dpi=150)
    plt.close()


# GRÁFICAS PEQUEÑAS (las de las pruebas unitarias)

def graficas_pequenas():

    arbol = prueba_inserción()    # árbol con los 10 puntos de prueba

    graficar_arbol(arbol, PUNTOS_PEQUENOS, "graficas/prueba_insercion.png", "Quadtree con 10 puntos")

    encontrados = arbol.consultar_en_radio(6, 3, 2)
    graficar_radio(PUNTOS_PEQUENOS, 6, 3, 2, encontrados, "graficas/radio_pequeno_p1.png", "Centro (6,3), radio 2", raiz=arbol)

    encontrados = arbol.consultar_en_radio(2, 2, 2)
    graficar_radio(PUNTOS_PEQUENOS, 2, 2, 2, encontrados, "graficas/radio_pequeno_p2.png", "Centro (2,2), radio 2", raiz=arbol)

    encontrados = arbol.consultar_en_radio(3, 2, 5)
    graficar_radio(PUNTOS_PEQUENOS, 3, 2, 5, encontrados, "graficas/radio_pequeno_p3.png", "Centro (3,2), radio 5", raiz=arbol)

    vecino = arbol.vecino_mas_cercano(6, 3)
    graficar_vecino(PUNTOS_PEQUENOS, 6, 3, vecino[0], "graficas/vecino_pequeno_p1.png", "Vecino de (6,3)", raiz=arbol)

    vecino = arbol.vecino_mas_cercano(0,0)
    graficar_vecino(PUNTOS_PEQUENOS, 0, 0, vecino[0], "graficas/vecino_pequeno_p2.png", "Vecino de (0,0)", raiz=arbol)


# GRÁFICAS GRANDES (ciudad de 40000 x 40000 m y 10000 puntos) y para una muestra de 400 puntos
def graficas_grandes():

    tamano = 40000

    puntos = Quadtree.generar_puntos_realistas(10000, ancho_ciudad=tamano, largo_ciudad=tamano, dispersion_barrio=2500)  # La desviación estándar será de 2500
    raiz = Quadtree.Nodo_Quadtree(0, 0, tamano, tamano)

    for x, y in puntos:
        raiz.insertar_punto(x, y)

    # Inserción realista de los 10000 puntos, sin usar rojo.
    graficar_arbol(raiz, puntos, "graficas/insercion_ciudad.png",
                   "Inserción realista de 10000 puntos", color_puntos="steelblue")

    # Búsqueda por radio en una ubicación aleatoria.
    centro_x = random.uniform(0, tamano)
    centro_y = random.uniform(0, tamano)
    radio = 500  # Búsqueda a un radio de 500 metros
    encontrados = raiz.consultar_en_radio(centro_x, centro_y, radio)  # Se llama al método que devuelve la lista de los puntos dentro el radio

    graficar_radio(puntos, centro_x, centro_y, radio, encontrados,
                   "graficas/busqueda_radio.png",
                   "Búsqueda por radio de 500 m (consulta aleatoria)", raiz=raiz)

    # Vecino más cercano desde una ubicación aleatoria.
    x_consulta = random.uniform(0, tamano)
    y_consulta = random.uniform(0, tamano)
    vecino = raiz.vecino_mas_cercano(x_consulta, y_consulta) # Se llama al método que busca al vecino más cercano

    graficar_vecino(puntos, x_consulta, y_consulta, vecino[0],
                    "graficas/vecino_mas_cercano.png",
                    "Vecino más cercano (consulta aleatoria)", raiz=raiz)

    # Se hace también un árbol más pequeño con 400 puntos, para visualizar mejor el QuadTree
    tamano_muestra = 20000  # Será una ciudad de 20000 x 20000 metros
    for nombre, generador_de_puntos in [("uniforme", Quadtree.generar_puntos_uniformes),
                              ("realista", Quadtree.generar_puntos_realistas)]:   # Se generan con datos uniformes y con datos realistas para comparar 
        muestra = generador_de_puntos(400, ancho_ciudad=tamano_muestra, largo_ciudad=tamano_muestra)
        arbol_muestra = Quadtree.Nodo_Quadtree(0, 0, tamano_muestra, tamano_muestra)
        for x, y in muestra:
            arbol_muestra.insertar_punto(x, y)
        graficar_arbol(arbol_muestra, muestra, "graficas/arbol_" + nombre + ".png",
                       "Quadtree con 400 puntos (" + nombre + ")")

# Se llaman a todas las pruebas
if __name__ == "__main__":
    os.makedirs("graficas", exist_ok=True)

    prueba_coincidir()
    pruebas_unitarias()
    graficas_pequenas()
    graficas_grandes()