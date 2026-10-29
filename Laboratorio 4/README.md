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
* `verificar_si_contiene_punto`:
  Verifica si un punto a insertar cae dentro del nodo. Se valida entonces que la coordenada del punto x a insertar esté entre el inicio del nodo (coordenada x) y el final ( coordenada x + longitud horizontal). Asimismo, con el eje y.
  
* `subdividir_nodo`:
  Se encarga de dividir a un nodo en 4, convirtiendolo en un nodo interno, cada uno con la mitad del ancho y largo del padre.
  Crea 4 nodos del mismo tipo Quadtree:
  * hijo_Noreste: arriba a la derecha
  * hijo_Noroeste: arriba a la izquierda
  * hijo_Sureste: abajo a la derecha
  * hijo_Suroeste: abajo a la izquierda
 Y se guardan en una lista en ese mismo orden

* `indice_hijo`:
  determina a cuál de los 4 hijos pertenece un punto. Compara sus coordenadas con el centro del nodo (derecha o izquierda, arriba o abajo) y devuelve el índice del cuadrante correspondiente (0 = NE, 1 = NO, 2 = SE, 3 = SO), que coincide con el orden de la lista hijos. Se usa al insertar un punto y al buscar el vecino más cercano.

* `insertar_punto`:
  inserta un punto en el nodo o en alguno de sus descendientes. Primero verifica que el punto caiga dentro de la región del nodo (con la función auxiliar); si no, devuelve False. Si el nodo es una hoja:
  
  Si está vacía, guarda el punto y devuelve True.
  Si ya tiene un punto idéntico, no lo inserta (duplicado) y devuelve False.
  Si tiene otro punto distinto, se subdivide el nodo con subdividir_nodo, se reubica el punto antiguo en el hijo que le corresponde (con indice_hijo) y luego se continúa para insertar el punto nuevo.
  
  Si el nodo ya es interno, calcula con indice_hijo a cuál hijo pertenece el punto y llama recursivamente a insertar_punto en ese hijo. Devuelve el resultado de esa inserción.

* `verificar_si_se_cruza`:
  Función auxiliar que comprueba si el rango rectangular buscado (x_min, y_min, x_max, y_max) se solapa con la región que cubre el nodo. Lo hace eje por eje: en cada uno, el inicio del nodo debe ser menor que el fin de la consulta, y el inicio de la consulta menor que el fin del nodo. Devuelve True solo si hay solape en X y en Y a la vez. Se usa en consultar_rango para podar: si no se cruzan, se descarta el nodo y todo su subárbol sin revisar ninguno de sus puntos.

* `consultar_rango`:
  Sirve para encontrar los puntos dentro de un rango específico ( un rectángulo ). Primero se verifica si las dimensiones del rectángulo del rango se cruza con el nodo, con la función anterior, si no es así, se descarta todo ese sub árbol. Si se cruzan, Se llama recursivamente la función para recorrer los hijos de los nodos hasta llegar a las hojas y devolver los puntos obtenidos en una lista.

* `consultar_en_radio`:
  Para encontrar los puntos en un radio, se calcula las coordenadas del rectángulo mínimo que contiene al círculo de la consulta, luego con la función (`consultar_rango`) se sacan los puntos candidatos. Luego, se calcula la distancia euclidiana de los puntos candidatos y el punto de la consulta, la cual debe ser menor o igual al radio para estar adentro, y estos serían los puntos rsultantes.


* `distancia_minima_a_cuadro`:
  
  
  
