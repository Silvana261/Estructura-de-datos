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

**Con el fin de analizar el comportamiento del Quadtree y resolver la pregunta del problema, se obtuvo la siguiente visualización:**


### Inserción
<img width="1200" height="1200" alt="image" src="https://github.com/user-attachments/assets/72d81389-4c07-410c-a308-3ebdbe56428e" />

> [!NOTE]
> Aquí se puede ver una ciudad de 40.000 X 40.000 metros, con 10.000 puntos de entrega, donde se   concentran más en en unos puntos que en otros con la distribución realista.

### Búsqueda por radio
<img width="1040" height="1137" alt="image" src="https://github.com/user-attachments/assets/0471620b-a3c1-4a83-9bc3-f479cb606b8e" />
```
Se generó una búsqueda aleatoria para buscar los puntos a un radio de 500 metros.
Entonces desde el punto `(14191.9, 8701.51)` a un radio de 500 metros están los puntos de   entrega: `(13934.8, 8964.2)`, `(14291.4, 8502.5)`, `(14378.5, 8267.2)`, `(14490.6, 8672.1)`, `(14552.7, 8601.5)` 
```

### Vecino más cercano 
<img width="1200" height="1200" alt="image" src="https://github.com/user-attachments/assets/d83353fd-0fe8-4a77-ac8f-d663642ff140" />

> Y se generó un punto aleatorio de consulta para el vecino más cercano.
  Entonces el punto de entrega más cercano desde el punto `(21337.75, 35693.37)` es el `(21209.17, 35738.52)` a una distancia de **136.28** metros.



## 4.  `analisis.py`

En este archivo se realizan 4 experimentos para comparar el rendimiento del Quadtree y la lista, a medida que aumenta el número de puntos. Además se hicieron funciones auxiliares para llamar a las funciones y métodos que generan los puntos, para calcular la profundidad del árbol, para llamar los métodos para construir el árbol, medir el tiempo y calcular desde que tamaño es mejor el Quadtree.


### Parámetros:

* **TAMANO (N)** = 40.000. Largo y ancho de la ciudad
* **RADIO** = 500 m. Radio para todas las búsquedas por radio
* **DISPERSION** = 1.500 m. Desviación estándar de cada barrio para la generación de datos realistas
* **TAMANOS** = [10, 20, 50, 100, 200, 500, 1000, 2000, 5000, 10000, 20000,40000]. Los distintos tamaños de puntos
* **CONSULTAS** = 200. Consultas por cada tamaño de TAMANOS
* **REPETICIONES** = 50. Número de repeticiones de la construcción y medición de profundidad

### Cómo se mide el tiempo

Se usa `time.perf_counter()`, que es el reloj de mayor resolución disponible en Python.

### `EXPERIMENTO 1: Profundidad del Quadtree`

Para cada tamaño N se construyen árboles con puntos generados de forma uniforme y con puntos generados de forma realista (con barrios). En cada árbol se calcula la profundidad máxima, es decir, la cantidad de niveles de la rama más larga. Este proceso se repite 50 veces por cada N, generando puntos nuevos en cada repetición, y se calculan el promedio y la desviación estándar de la profundidad. Los resultados se grafican en función de N, con el valor promedio escrito sobre cada punto y las barras de error con ± 1 desviación estándar.

<img width="1145" height="884" alt="97825f5b-877f-487f-a5f1-491199ef9442" src="https://github.com/user-attachments/assets/4bc2b0ad-554f-4bbd-846b-047998b6e6e0" />

### Interpretación:

Con la distribución uniforme se generan árboles menos profundos que con la realista, porque la concentración de puntos en los barrios obliga a subdividir más veces para dejar un punto por hoja. 

La profundidad promedio de un Quadtre es **log2(N)**, lo que representa una pendiente aproximadamente de **3.32**. Las pendientes medidas fueron 3,30 (uniforme) y 3,31 (realista), prácticamente iguales a la teórica.

### Gráficos 

<img width="1200" height="1200" alt="223b614e-98a1-4c98-95c6-9d765a9e0fcd" src="https://github.com/user-attachments/assets/a48f816b-f034-489f-b022-4ca25ff00d96" />


<img width="1200" height="1200" alt="42548015-5f0d-460b-926a-f99d0c4924be" src="https://github.com/user-attachments/assets/4774fb34-ccdb-48be-965e-c44efac8e984" />

### `EXPERIMENTO 2: INSERCIÓN`

Para cada tamaño de N se generan puntos con distribución realista una sola vez, y con esos mismos puntos se construyen las dos estructuras. Cada construcción se repite 50 veces, se mide el tiempo y se calcula el promedio y desviación estándar de las repeticiones. 

<img width="1053" height="825" alt="image" src="https://github.com/user-attachments/assets/61b0dc9e-a6a7-436d-91e7-051f4cf4591e" />


### Interpretación:

En cuanto a la inserción, el quadtree es más lento que la lista en todos los N probados. La lista es mucho más eficiente a la hora de insertar.

La pendiente fue **1.06** para la lista lo cual coincide con la teoría donde se espera una pendiente aproximadamente de **1**, ya que tiene un costo **O(N). 

Y la pendiente para el quadtree fue de **1.14** lo cual coincide con la teoría donde se espera una pendiente aproximadamente de **1.1** para que sea **O(NlogN)**.


### `EXPERIMENTO 3: RADIO`

Para cada tamaño de N se generan puntos con distribución realista una sola vez, y con ellos se construyen las dos estructuras. Luego, se generan 200 puntos de consulta y se buscan los puntos a un radio de 500 metros. Finalmente, se calcula el promedio y la desviación estándar de las 200 consultas de cada N.
<img width="1053" height="825" alt="image" src="https://github.com/user-attachments/assets/18c96a68-60f9-4c37-a56a-afb7ba840a18" />


### Interpretación:


En la búsqueda por radio, el más eficiente fue el quadtree.
La fuerza bruta tiene una pendiente de **0.99** como se espera de un costo **O(N)**, porque recorre todos los puntos.  El quadtree obtuvo una pendiente de **0.38**,  que es cerca de lo que se esperaba para un costo de **O(log(N))**.

En este caso, a partir de N = 20 puntos, el Quadtree es más rápido de que la lista. Y antes eran casi igual de rápidos.

Una posible causa de las desviaciones gigantes, es que como las consultas son puntos aleatorios, puede que hayan caído algunos en zonas muy pobladas, por lo que los puntos dentro del radio aumentaban mucho respecto a los que cayeron en puntos aislados.


### `EXPERIMENTO 4: VECINO MÁS CERCANO`

Para cada tamaño de N se usan los mismos puntos y las mismas estructuras del experimento anterior. Se utilizan los mismos 200 puntos de consultas aleatorias y en cada una se busca el vecino más cercano. Luego se promedia el tiempo que se demoraron las 200 consultas en cada N y se saca la desviación estándar 


<img width="1053" height="823" alt="image" src="https://github.com/user-attachments/assets/7ab90fb8-67d9-461e-b85b-01149830f56a" />


### Interpretación:

En la búsqueda del vecino más cercano, al principio es más eficiente la lista para tamaños de N menores a 100 (pequeños), y partir de ahí el más eficiente es el quadtree, y la lista crece de manera lineal.

La fuerza bruta tiene una pendiente log-log de **0.99**, como se espera de un costo **O(N)**, porque calcula la distancia a todos los puntos en cada consulta. 

La pendiente del quadtree fue de **0.13**  que concuerda con el costo computacional de **O(log(N))**

































### Limitaciones

- Los tiempos dependen de la máquina y de Python (intérprete), por lo que importa la **tendencia** y las pendientes, no los valores absolutos.
- En el quadtree el costo de una consulta depende de la **densidad local**, por eso la desviación entre consultas es grande: una consulta en un barrio denso devuelve muchos puntos, y una en una zona vacía casi ninguno.
- La inserción en la lista (`append`) es casi gratuita, así que el quadtree no puede ganar ese experimento. Su costo de construcción se compensa en las consultas.


