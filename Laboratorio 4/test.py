import random 
import Quadtree
from Quadtree import busqueda_radio_fuerza_bruta, vecino_mas_cercano_fuerza_bruta, Nodo_Quadtree, generar_puntos_realistas

# 1. PRUEBAS PARA VERIFICAR QUE LOS RESULTADOS CON FUERZA BRUTA COINCIDAN CON LOS DEL QUADTREE

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
def prueba_inserción(Quadtree = Nodo_Quadtree(0,0,8,8)):
    assert Quadtree.insertar_punto(1, 1) == True       #  Dentro del rango
    assert Quadtree.insertar_punto(6, 2) == True       #  Dentro del rango
    assert Quadtree.insertar_punto(2, 3) == True       #  Dentro del rango
    assert Quadtree.insertar_punto(3, 1) == True       #  Dentro del rango
    assert Quadtree.insertar_punto(9, 9) == False      #  Fuera del árbol
    assert Quadtree.insertar_punto(10, 4) == False     #  Fuera del árbol (por el eje x)
    assert Quadtree.insertar_punto(6, 9) == False      #  Fuera del árbol (por el eje y)
    assert Quadtree.insertar_punto(1, 1) == False      #  duplicado
 
    print(" \nTodas las pruebas de inserción pasaron")
    return Quadtree

# Búsqueda por rango  ( Con el mismo árbol de la prueba anterior) 
def prueba_rango():
    Quadtree = prueba_inserción()  # Puntos en el árbol: (1, 1), (6, 2), (2, 3), (3, 1)
    
    assert Quadtree.consultar_en_radio(1,1,1) == [(1,1)]  # A un radio de un metro solo está el punto (1,1)
    assert sorted(Quadtree.consultar_en_radio(2, 2, 2)) == [(1,1), (2,3),(3,1)]   # El punto (2,2) a un radio de 2: (1, 1) está a distancia ~1.41 (entra), (3, 1) está a distancia ~1.41 (entra), (2, 3) está a distancia 1.0 (entra), (6, 2) está a distancia 4.0 (Queda fuera)
    assert sorted(Quadtree.consultar_en_radio(3, 2, 5)) == [(1, 1), (2, 3), (3, 1), (6, 2)] # El punto (3,2) a un radio de 5: abarca todos los puntos
    assert Quadtree.consultar_en_radio(7, 7, 1) == []  # El punto (7,7) a un radio de 1 no hay puntos en ese radio
    vacio = Nodo_Quadtree(0, 0, 5, 5)
    assert vacio.consultar_rango(0, 0, 8, 8) == []  # Se prueba con un árbol vacío
    print("\n Todas las pruebas de búsqueda a un radio fueron exitosas")

def prueba_vecino():
    Quadtree = prueba_inserción()   # Puntos en el árbol: (1, 1), (6, 2), (2, 3), (3, 1)
    # De la lista que devuelve este método en la posición 0, está el punto
    assert raiz.vecino_mas_cercano(6, 3)[0] == (6, 2)   # El más cercano a (6,3) es (6,2)
    assert raiz.vecino_mas_cercano(0, 0)[0] == (1, 1)   # El más cercano a (0,0) es (1,1)
    vacio = Nodo_Quadtree(0, 0, 3, 3)
    assert vacio.vecino_mas_cercano(4, 4)[0] is None  # Se prueba con un árbol vacío
    
prueba_inserción()
prueba_rango()
prueba_vecino()
    