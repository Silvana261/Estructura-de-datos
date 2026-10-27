import random 
import Quadtree
from Quadtree import busqueda_radio_fuerza_bruta, vecino_mas_cercano_fuerza_bruta, Nodo_Quadtree, generar_puntos_realistas

TAMANO = 20000
RADIO = 500

# Primero se generan los datos
puntos = Quadtree.generar_puntos_realistas(10000, ancho_ciudad = TAMANO, largo_ciudad = TAMANO, dispersion_barrio= 1500)

# Se prueba la construcción del Quadtree
raiz = Quadtree.Nodo_Quadtree(0,0, TAMANO, TAMANO)
puntos_insertados = 0

for x, y in puntos:
    if raiz.insertar_punto(x,y):
        puntos_insertados += 1
        
print(f"Puntos generados: {len(puntos)}")
print(f"Puntos insertados: {puntos_insertados}")

if len(puntos) == puntos_insertados:
    print("Todos los puntos se insertaron")
else:
    print("Hay puntos que no se insertaron")

# Se comparan los resultados con el árbol y con fuerza bruta en la búsqueda a un radio

for i in range(100):
    centro_x = random.uniform(0, TAMANO)
    centro_y = random.uniform(0, TAMANO)
    
    resultado_arbol = sorted(raiz.consultar_en_radio(centro_x, centro_y, RADIO))
    resultado_bruta = sorted(Quadtree.busqueda_radio_fuerza_bruta(puntos, centro_x, centro_y, RADIO))
    
    assert resultado_arbol == resultado_bruta, f"Radio: difieren en ({centro_x}, {centro_y})"

print(" Las 100 consultas coinciden")

# Ahora comparar si coinciden los resultados en la búsqueda del vecino más cercano

for i in range(100):
    centro_x = random.uniform(0, TAMANO)
    centro_y = random.uniform(0, TAMANO)
    
    resultado_arbol = raiz.vecino_mas_cercano(centro_x, centro_y)
    resultado_bruta = Quadtree.vecino_mas_cercano_fuerza_bruta(puntos, centro_x, centro_y)
    
    assert resultado_arbol == resultado_bruta, f"En el resultado difieren en ({centro_x},{centro_y})"    
print(" Las 100 búsquedas coinciden")