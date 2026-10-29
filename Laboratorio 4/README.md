# Laboratorio 4: Quadtree VS Fuerza Bruta

## Problema y objetivos:

Se tiene coordenadas de entrega (x,y) de 10.000 puntos de entrega por lo que se necesita implementar un sistema que permita encontrar el punto más cercano a otro o buscar los puntos a un radio de distancia.

### Objetivo:
- Implementar la estructura de árbol Quadtree, el cual permitirá responder a las necesidades del sistema de entregas.
- Comparar el rendimiento del Quadtree con la fuerza bruta (lista)
- Visualizar el árbol y los puntos de las consultas

## 2. Estructuras de datos y algoritmos

### `Quadtree.py`
Aquí se implementó el Quadtree para dos dimensiones, las funciones para la fuerza bruta y para generar los datos.

- **Nodo_Quadtree**:
  Esta clase define a un nodo del árbol y los métodos para realizar las consultas, Los nodos en sí son cuadrantes del árbol, solo que unos guardan puntos (cuando son hojas) y señalan a sus 4  hijos cuando se dividen.
  
  Un `nodo` tiene:
  * Coordenada x
  * Coordenada y
  * Longitud vertical
  * Longitud horizontal
  * punto: Cada nodo tiene la capacidad de tener un punto
  * hijos: los cuatro nodos a los que apunta cuando se divide. Los hijos se identifican como: hijo_Noreste, hijo_Noroeste, hijo_Sureste e hijo_Suroeste.
  * Y una variable booleana que indíca si el nodo es una hoja o no (self.es_hoja)

La clase tiene los siguientes métodos:
* 
