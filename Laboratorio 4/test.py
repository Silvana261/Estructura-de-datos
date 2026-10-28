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



    print(f"Puntos generados: {len(puntos)}")          # Se muestra la cantidad de puntos generados e insertados

    print(f"Puntos insertados: {puntos_insertados}")



    if len(puntos) == puntos_insertados:               # Se comprueba que sea la misma cantidad los puntos de la lista que los del árbol

        print("Todos los puntos se insertaron")

    else:

        print("Hay puntos que no se insertaron")



    # Se comparan los resultados con el árbol y con fuerza bruta en la búsqueda de radio



    for i in range(100):                       # Se generan 100  búsquedas de puntos a un radio

        centro_x = random.uniform(0, TAMANO)   # Se genera aleatoriamente los puntos sobre los que se va a hacer la búsqueda, delimitados por las dimensiones de la ciudad

        centro_y = random.uniform(0, TAMANO)    

        # Se realiza la búsqueda en el árbol y con fuerza bruta

        resultado_arbol = sorted(raiz.consultar_en_radio(centro_x, centro_y, RADIO))        # Las listas que retornan las dos funciones se ordenan para poder comparar

        resultado_bruta = sorted(Quadtree.busqueda_radio_fuerza_bruta(puntos, centro_x, centro_y, RADIO))



        assert resultado_arbol == resultado_bruta, f" Difieren en el punto ({centro_x}, {centro_y})"   # Con assert se verifica que los dos resultados coincidan, si no se muestra el punto del problema



    print("Las 100 consultas coinciden")



    # Ahora comparar si coinciden los resultados en la búsqueda del vecino más cercano



    for i in range(100):                        # Se hacen 100 búsquedas del vecino más cercano

        centro_x = random.uniform(0, TAMANO)    # Sobre puntos generados aleatoriamente dentro las dimensiones del cuadrante

        centro_y = random.uniform(0, TAMANO)

        # Se realiza la búsqueda del vecino más cercano con fuerza bruta y en el árbol 

        resultado_arbol = raiz.vecino_mas_cercano(centro_x, centro_y)                                

        resultado_bruta = Quadtree.vecino_mas_cercano_fuerza_bruta(puntos, centro_x, centro_y)



        assert resultado_arbol == resultado_bruta, f"En el resultado difieren en ({centro_x},{centro_y})"  # Con assert se verifica que los dos resultados coincidan, si no se muestra el punto del problema



    print("Las 100 búsquedas coinciden")



# 2. PRUEBAS UNITARIAS QUADTREE



# Inserción

def prueba_inserción():
    quadtree = Quadtree.Nodo_Quadtree(0, 0, 10, 10)

    # Se insertan 10 puntos dentro de la ciudad
    for punto in PUNTOS_PEQUENOS:
        assert quadtree.insertar_punto(*punto) == True

    # Pruebas de puntos fuera del árbol y de duplicados
    assert quadtree.insertar_punto(11, 11) == False  # Fuera del árbol
    assert quadtree.insertar_punto(12, 4) == False   # Fuera del eje x
    assert quadtree.insertar_punto(6, 11) == False   # Fuera del eje y
    assert quadtree.insertar_punto(1, 1) == False    # Duplicado

    print("\\nTodas las pruebas de inserción pasaron")
    return quadtree


# Búsqueda por radio (con el mismo árbol de la prueba anterior)
def prueba_radio():
    quadtree = prueba_inserción()

    assert quadtree.consultar_en_radio(1, 1, 1) == [(1, 1)]
    assert sorted(quadtree.consultar_en_radio(2, 2, 2)) == [(1, 1), (2, 3), (3, 1)]
    assert sorted(quadtree.consultar_en_radio(5, 5, 3)) == [(4, 7), (5, 5), (7, 6)]
    assert quadtree.consultar_en_radio(5, 1, 0.5) == []

    print("\\nTodas las pruebas de búsqueda a un radio fueron exitosas")


def prueba_vecino():
    quadtree = prueba_inserción()

    # De la lista que devuelve este método en la posición 0, está el punto
    assert quadtree.vecino_mas_cercano(6, 3)[0] == (6, 2)
    assert quadtree.vecino_mas_cercano(0, 0)[0] == (1, 1)

    print("\\nPrueba del vecino más cercano exitosa")


def pruebas_unitarias():
    while True:
        op = input("\\n Escoger la prueba unitaria a realizar:\\n 1. Probar inserciones.\\n 2. Probar búsqueda por radio.\\n 3. El vecino más cercano.\\n 4. Salir\\n")
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



def configurar_ejes(eje, raiz, centro_x, centro_y, zoom):   # Define qué parte del mapa se ve

    if zoom is not None:

        eje.set_xlim(centro_x - zoom, centro_x + zoom)

        eje.set_ylim(centro_y - zoom, centro_y + zoom)

    elif raiz is not None:

        eje.set_xlim(raiz.coordenada_x, raiz.coordenada_x + raiz.longitud_horizontal)

        eje.set_ylim(raiz.coordenada_y, raiz.coordenada_y + raiz.longitud_vertical)

    eje.set_aspect("equal")



def graficar_arbol(raiz, puntos, nombre_archivo, titulo="", color_puntos="red"):

    figura, eje = plt.subplots(figsize=(8, 8))



    dibujar_cuadrantes(raiz, eje)



    xs = [p[0] for p in puntos]

    ys = [p[1] for p in puntos]

    eje.scatter(xs, ys, color=color_puntos, s=tamano_punto(puntos))



    configurar_ejes(eje, raiz, None, None, None)

    eje.set_title(titulo)
    eje.set_xlabel(f"Dimensiones de la ciudad: {raiz.longitud_horizontal} x {raiz.longitud_vertical} m | Cantidad de puntos: {len(puntos)}")

    plt.savefig(nombre_archivo, dpi=150)

    plt.close()



def graficar_radio(puntos, centro_x, centro_y, radio, encontrados, nombre_archivo,titulo="", raiz=None, zoom=None):

    figura, eje = plt.subplots(figsize=(8, 8))



    if raiz is not None:

        dibujar_cuadrantes(raiz, eje)



    xs = [p[0] for p in puntos]

    ys = [p[1] for p in puntos]

    eje.scatter(xs, ys, color="lightgray", s=tamano_punto(puntos), label="Puntos")



    if len(encontrados) > 0:

        xs_enc = [p[0] for p in encontrados]

        ys_enc = [p[1] for p in encontrados]

        eje.scatter(xs_enc, ys_enc, color="red", s=tamano_punto(puntos) * 3,label="Dentro del radio (" + str(len(encontrados)) + ")")

    circulo = plt.Circle((centro_x, centro_y), radio, fill=False, color="blue")

    eje.add_patch(circulo)

    eje.scatter([centro_x], [centro_y], color="blue", marker="x", label="Consulta")



    configurar_ejes(eje, raiz, centro_x, centro_y, zoom)

    eje.set_title(titulo)
    if raiz is not None:
        eje.set_xlabel(f"Dimensiones de la ciudad: {raiz.longitud_horizontal} x {raiz.longitud_vertical} m | Cantidad de puntos: {len(puntos)}")
    else:
        eje.set_xlabel(f"Cantidad de puntos: {len(puntos)}")

    if len(puntos) <= 20:
        texto_resultados = "Resultados: " + str(encontrados)
        eje.text(0.02, 0.98, texto_resultados, transform=eje.transAxes,
                 verticalalignment="top", fontsize=9,
                 bbox=dict(boxstyle="round", facecolor="white", alpha=0.85))

    eje.legend()

    plt.savefig(nombre_archivo, dpi=150)

    plt.close()

def graficar_vecino(puntos, x_consulta, y_consulta, vecino, nombre_archivo,titulo="", raiz=None, zoom=None):

    figura, eje = plt.subplots(figsize=(8, 8))



    if raiz is not None:

        dibujar_cuadrantes(raiz, eje)



    xs = [p[0] for p in puntos]

    ys = [p[1] for p in puntos]

    eje.scatter(xs, ys, color="lightgray", s=tamano_punto(puntos), label="Puntos")



    eje.scatter([x_consulta], [y_consulta], color="blue", marker="x", label="Consulta")  

    if vecino is not None:

        eje.scatter([vecino[0]], [vecino[1]], color="red", s=tamano_punto(puntos) * 3,

                    label="Vecino más cercano")

        eje.plot([x_consulta, vecino[0]], [y_consulta, vecino[1]], color="red", linestyle="--")



    configurar_ejes(eje, raiz, x_consulta, y_consulta, zoom)

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

    eje.legend()

    plt.savefig(nombre_archivo, dpi=150)

    plt.close()



# GRÁFICAS PEQUEÑAS (las de las pruebas unitarias)



PUNTOS_PEQUENOS = [
    (1, 1), (6, 2), (2, 3), (3, 1), (5, 5),
    (7, 6), (8, 2), (4, 7), (1, 8), (9, 9)
]



def graficas_pequenas():

    arbol = prueba_inserción()    # árbol con los 4 puntos



    graficar_arbol(arbol, PUNTOS_PEQUENOS, "graficas/arbol_pequeno.png", "Quadtree con 4 puntos")

    encontrados = arbol.consultar_en_radio(1, 1, 1)

    graficar_radio(PUNTOS_PEQUENOS, 1, 1, 1, encontrados, "graficas/radio_pequeno_p1.png", "Centro (1,1), radio 1", raiz=arbol)

    encontrados = arbol.consultar_en_radio(2, 2, 2)

    graficar_radio(PUNTOS_PEQUENOS, 2, 2, 2, encontrados, "graficas/radio_pequeno_p2.png", "Centro (2,2), radio 2", raiz=arbol)

    encontrados = arbol.consultar_en_radio(3, 2, 5)

    graficar_radio(PUNTOS_PEQUENOS, 3, 2, 5, encontrados, "graficas/radio_pequeno_p3.png", "Centro (3,2), radio 5", raiz=arbol)

    encontrados = arbol.consultar_en_radio(7, 7, 1)

    graficar_radio(PUNTOS_PEQUENOS, 7, 7, 1, encontrados, "graficas/radio_pequeno_p4.png", "Centro (7,7), radio 1", raiz=arbol)



    vecino = arbol.vecino_mas_cercano(6, 3)

    graficar_vecino(PUNTOS_PEQUENOS, 6, 3, vecino[0], "graficas/vecino_pequeno_p1.png", "Vecino de (6,3)", raiz=arbol)

    vecino = arbol.vecino_mas_cercano(0,0)

    graficar_vecino(PUNTOS_PEQUENOS, 0, 0, vecino[0], "graficas/vecino_pequeno_p2.png", "Vecino de (0,0)", raiz=arbol)



# GRÁFICAS GRANDES (ciudad de 40000 x 40000 m y 10000 puntos)
def graficas_grandes():

    tamano = 40000

    puntos = Quadtree.generar_puntos_realistas(10000, ancho_ciudad=tamano, largo_ciudad=tamano,
                                               dispersion_barrio=2500)

    raiz = Quadtree.Nodo_Quadtree(0, 0, tamano, tamano)

    for x, y in puntos:
        raiz.insertar_punto(x, y)

    # Inserción realista de los 10000 puntos, sin usar rojo.
    graficar_arbol(raiz, puntos, "graficas/insercion_realista.png",
                   "Inserción realista de 10000 puntos", color_puntos="steelblue")

    # Búsqueda por radio en una ubicación aleatoria.
    centro_x = random.uniform(0, tamano)
    centro_y = random.uniform(0, tamano)
    radio = 12000
    encontrados = raiz.consultar_en_radio(centro_x, centro_y, radio)

    graficar_radio(puntos, centro_x, centro_y, radio, encontrados,
                   "graficas/busqueda_radio.png",
                   "Búsqueda por radio de 500 m (consulta aleatoria)", raiz=raiz)

    # Vecino más cercano desde una ubicación aleatoria.
    x_consulta = random.uniform(0, tamano)
    y_consulta = random.uniform(0, tamano)
    vecino = raiz.vecino_mas_cercano(x_consulta, y_consulta)

    graficar_vecino(puntos, x_consulta, y_consulta, vecino[0],
                    "graficas/vecino_mas_cercano.png",
                    "Vecino más cercano (consulta aleatoria)", raiz=raiz)

    # Conservar también las dos gráficas originales de inserción con 400 puntos.
    tamano_muestra = 20000
    for nombre, generador in [("uniforme", Quadtree.generar_puntos_uniformes),
                              ("realista", Quadtree.generar_puntos_realistas)]:
        muestra = generador(400, ancho_ciudad=tamano_muestra, largo_ciudad=tamano_muestra)
        arbol_muestra = Quadtree.Nodo_Quadtree(0, 0, tamano_muestra, tamano_muestra)
        for x, y in muestra:
            arbol_muestra.insertar_punto(x, y)
        graficar_arbol(arbol_muestra, muestra, "graficas/arbol_" + nombre + ".png",
                       "Quadtree con 400 puntos (" + nombre + ")")

if __name__ == "__main__":

    os.makedirs("graficas", exist_ok=True)



    prueba_coincidir()

    pruebas_unitarias()

    graficas_pequenas()

    graficas_grandes()
