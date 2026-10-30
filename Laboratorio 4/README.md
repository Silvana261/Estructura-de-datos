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

- ### Nodo_Quadtree:
  Esta clase define a un nodo del árbol y los métodos para realizar las consultas, Los nodos en sí son cuadrantes del árbol, solo que unos guardan puntos (cuando son hojas) y señalan a sus 4  hijos cuando se dividen. Las coordenadas y dimensiones de los nodos están en metros 
  
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
  Calcula la distancia entre un punto y el lado más cercano a este, para la búsqueda del vecino más cercano.

* `vecino_mas_cercano`:
  Busca el punto más cercano a una ubicación dada. Mantiene una lista mejor = [punto, distancia] compartida entre todas las llamadas recursivas, que al inicio está vacía. En cada nodo, si ya existe un mejor punto, calcula con distancia_minima_a_cuadro la distancia mínima de la consulta a ese nodo; si no mejora la mejor distancia, descarta el nodo y todo su subárbol. Si el nodo es una hoja con un punto, calcula la distancia euclidiana y, si es menor que la mejor, actualiza mejor. Si es un nodo interno, visita primero el hijo donde cae la consulta (con indice_hijo) y luego los otros tres, que casi siempre se descartan por la poda. Al terminar, devuelve [punto, distancia] con el vecino más cercano.

- ### Fuerza bruta:
  Se trabaja con una lista. Para buscar los puntos dentro de un radio, se recorre toda la lista calculando la distancia euclidiana entre el punto y el de la consulta. Y para el vecino más cercano, también recorre todos los puntos hasta encontrar la menor distancia.

- ### Funciones para generar puntos:

  
  * `generar_puntos_uniformes`:
    Se generan las coordenadas de los puntos aleatoriamente, todos tienen las misma probabilidad de caer en cualquier lado del quadtree

  
   * `generar_puntos_realistas`:
     Los puntos aleatorios se generan con distribución gaussiana (`random.gauss`), de modo que los puntos tienen 70% de probabilidad de caer alrededor de unos barrios predefinidos:  *barrios = [(8000, 8000), (32000, 8000), (20000, 20000), (32000, 32000)]*
     Ya que en la vida real, la distribución de los lugares no suele ser uniforme, sino que suelen estar más concentrados en unos lados.
  
## 3. Test `test.py`
En este archivo se hicieron las pruebas para verificar el funcionamiento del Quadtree y las funciones para generar las gráficas del árbol.

- ### **`prueba_coincidir`**:
  Esta es una función que se realizó para verificar que los resultados fueran iguales con fuerza bruta y el Quadtree.
  
  Se hizo un Quadtree de **20000 x20000** y se estableció un radio de **500**.
  Se generaron los puntos y se insertaron en el árbol con un contador por cada punto insertado, y se verificó que el número de puntos generados coincidiera con los del contador.
  
  <img width="497" height="125" alt="image" src="https://github.com/user-attachments/assets/b6159a4f-a46d-4356-9a33-82fc03e1ee41" />

  Luego, se realizan 100 búsquedas de radio, con puntos de consulta aleatorios. Se realiza tanto en el árbol como con fuerza bruta. Se comparan los resultados de las dos listas que retorna cada estructura y si son iguales, pasa la prueba.

  
    <img width="635" height="43" alt="image" src="https://github.com/user-attachments/assets/ffa69be7-66e9-4b7d-a0f6-3a2a06a8262a" />

  Finalmente, se hace la búsqueda del vecino más cercano a 100 puntos de consulta con las dos estructuras. Y si coinciden en cada búsqueda, pasa la prueba.

    <img width="537" height="45" alt="image" src="https://github.com/user-attachments/assets/ff1cb075-b731-45dc-b4ab-42a27850c839" />


- ### Pruebas unitarias:

  Se hicieron funciones auxiliares para hacer pruebas específicas:
  Usan un quadtree pequeño de **10 × 10 metros** con 10 puntos de entrega, para poder verificar a mano cada resultado esperado:
  
  `PUNTOS_PEQUENOS = [(1, 1), (6, 2), (2, 3), (3, 1), (5, 5),(7, 6), (8, 2), (4, 7), (1, 8), (9, 9)]`

  Cada prueba se verificó con `assert`, con el cual, si el resultado no coincide, el programa para e indica en donde ocurrió el error.

  * ### **prueba_insercion**:
    
    En esta prueba se insertan todos los puntos de la lista, los cuales deben ser exitosa su inserción. También se verificó que la inserción de los siguientes puntos fuera falsa:
    
    * El punto `(11,11)` no entra porque está por fuera
    * El punto `(12,4)` no entra porque está por fuera por el eje X
    * El punto `(6,11)` no entra porque está por fuera por el eje Y
    * El punto `(1,1)`  es un duplicado.

   **Resultado en consola**     
    <img width="459" height="201" alt="image" src="https://github.com/user-attachments/assets/1ef3fa4d-1172-4488-8582-ffe1a16e56b9" />

    **Gráfico del árbol**
    <img width="1200" height="1200" alt="image" src="https://github.com/user-attachments/assets/6ad1e5a9-6792-4f45-b822-997a34195252" />
    

  * ### **prueba_radio**:
    
    Se utiliza el mismo árbol producido anteriormente.
    Igualmente, se verificó con `assert` los resultados y de manera visual
    
    <img width="569" height="277" alt="image" src="https://github.com/user-attachments/assets/ce6a94da-25eb-4052-bbc6-c7c7a9faa700" />

    * ### Los puntos a un radio de 2 metros del punto `(6,3)` es `(6,2)`

    <img width="1001" height="1114" alt="image" src="https://github.com/user-attachments/assets/4b86a096-bae0-46b3-8e8d-134db836a113" />
  
    * ### Los puntos a un radio de 2 metros del punto `(2,2)` son `(1,1)`, `(2,3)`, `(3,1)`

    <img width="1001" height="1114" alt="image" src="https://github.com/user-attachments/assets/e56931d5-7cb0-43ed-9dc3-28ba37864e37" />

    * ### Los puntos a un radio de 4 metros del punto `(3,2)` son  `(4,7)`, `(5,5)`, `(7,6)`, (5, 5), (6, 2)
  
    <img width="1005" height="1136" alt="image" src="https://github.com/user-attachments/assets/c7207c9d-2d6e-424a-b172-6176b9e67c96" />

    *  ### Y no hay puntos a un radio de 0.5 metros del punto `(5,1)`
      
    <img width="1001" height="1092" alt="image" src="https://github.com/user-attachments/assets/9b449b93-7d64-4b07-ac9c-49a788791874" />


  * ### **prueba_vecino**:
 
    
    Se realiza con el mismo árbol para los siguientes puntos:
 
    
     <img width="417" height="272" alt="image" src="https://github.com/user-attachments/assets/10c198ff-3e7b-44b1-93ad-eea717672a37" />

    
    * ### El vecino más cercano de `(6,3)` es  `(6,2)`.   La distancia es un metro
      <img width="1200" height="1200" alt="image" src="https://github.com/user-attachments/assets/dd79c6cd-ce7a-4b8a-a88c-9a0e827f4e1a" />
    
 
      
    * ### El vecino más cercano de `(0,0)` es `(1,1)`. La distancia es 1.41 metros
 
      <img width="1200" height="1200" alt="image" src="https://github.com/user-attachments/assets/2ff4e8a9-a75d-4da9-a068-4ca86725c0c4" />
      

      
    * ### El vecino más cercano de `(5.6,9)` es  `(4,7)`. La distancia es 2.56 metros
   
      <img width="1200" height="1200" alt="image" src="https://github.com/user-attachments/assets/afb64d31-c780-440e-a29b-698fe69d79e3" />

    
