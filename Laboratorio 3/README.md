# Laboratorio 3: Sistema de Administración de Estudiantes

## 1. Problema y objetivo

### Problema
Una institución educativa necesita administrar la información de sus estudiantes. Cada
registro contiene ID (matrícula única), nombre, edad y promedio. El sistema debe permitir:

1. Buscar un estudiante por su ID.
2. Insertar un nuevo estudiante.
3. Listar todos los estudiantes en orden ascendente de ID.

Además de estas tres operaciones se evaluó la búsqueda por rango de IDs.
### Objetivo
Estudiar experimentalmente cómo la estrategia de almacenamiento y búsqueda afecta el tiempo
de ejecución a medida que aumenta el tamaño de los datos (N). Se comparan tres estructuras:
**lista**, **árbol ABB** y **árbol B+**, y se contrastan los resultados
con la complejidad teórica. Las conclusiones se sustentan en mediciones y análisis estadístico.

## 2. Estructuras de datos y algoritmos
Las tres estructuras guardan objetos `Estudiante` con los campos `id` (único), `nombre`, `edad`
y `promedio`. El ID es la clave de búsqueda y de orden.

### 2.1 Lista (`Lista.py`)

Una lista de Python (arreglo dinámico) sin ningún orden especial: los estudiantes quedan en el
orden en que se insertan.

- **O(1) — Insertar:** `append` al final de la lista.
- **O(N) — Buscar por ID:** recorrido secuencial comparando el ID de cada estudiante; se detiene
  al encontrarlo.
- **O(N log N) — Listar en orden:** copia de la lista y `sort` por ID (Timsort). Si la lista ya
  está ordenada, Timsort lo detecta y el costo baja a ≈O(N).
- **O(N) — Rango [a, b]:** recorre **toda** la lista y recoge los estudiantes con a ≤ ID ≤ b.

### 2.2 Árbol binario de búsqueda, ABB (`ArbolABB.py`)

Cada nodo guarda un estudiante y apunta a un hijo izquierdo (IDs menores) y a uno derecho (IDs
mayores o iguales), así que su forma depende del orden de inserción. Todas
las operaciones son iterativas (sin recursión). Ya que python tiene un límite de recursión.

- **Insertar:** baja desde la raíz comparando IDs hasta encontrar un hijo vacío.
  - IDs aleatorios: O(log N)
  - IDs ascendentes: O(N)
- **Buscar por ID:** baja comparando, hacia la izquierda o la derecha.
  - IDs aleatorios: O(log N)
  - IDs ascendentes: O(N)
- **Listar en orden:** recorrido inorden.
  - Cualquier orden de entrada: O(N)
- **Rango [a, b]:** recorrido con poda; baja a la izquierda solo si ID > a y a la derecha solo
  si ID < b.
  - IDs aleatorios: O(log N + K), con K = número de estudiantes en el rango
  - IDs ascendentes: O(N)
- **Altura:** recorrido por niveles (la raíz es el nivel 1). Cuesta O(N) calcularla.
  - IDs aleatorios: O(log N)
  - IDs ascendentes: O(N)

### 2.3 Árbol B+ (`ArbolBMas.py`)

Árbol balanceado donde **todos los estudiantes están en las hojas**, y los nodos internos solo
guardan claves que orientan la búsqueda. Las hojas están enlazadas entre sí (`siguiente`), lo
que permite recorrerlas en orden sin volver a subir al árbol. También se hizo de manera iterativa.
- **Grado = 50:** cada nodo admite hasta 50 claves.
- **Inserción:** se baja a la hoja correspondiente guardando los nodos internos recorridos, se
  inserta el ID en su posición ordenada y se rechaza si ya existe. Si la hoja supera 50 claves,
  se divide en dos (25 y 26) y la primera clave de la hoja derecha sube al padre. Si un nodo
  interno supera 50 claves, se divide y la clave central sube. Si
  se divide la raíz, el árbol crece un nivel; así todas las hojas siempre quedan a la misma
  altura.
- **Búsqueda dentro de un nodo:** es **lineal**, tanto en los
  nodos internos como en la hoja. El costo por nivel es proporcional al grado g (≤ 50).
  
Las operaciones, con g = 50 como constante:

- **O(log N) — Insertar:** descenso, inserción ordenada en la hoja y posibles
  divisiones.
- **O(log N) — Buscar por ID:** descenso por los nodos internos y búsqueda
  lineal en la hoja.
- **O(N) — Listar en orden:** se baja a la hoja más a la izquierda y se recorre la cadena de
  hojas enlazadas.
- **O(log N + K) — Rango [a, b]:** se baja a la hoja donde empieza el
  rango y se recorren las hojas enlazadas hasta pasar b.
- **O(log_g N) — Altura:** se baja por el primer hijo hasta una hoja (una hoja sola cuenta como
  nivel 1).

### 2.4  `GenerarDatos.py`

Todo se genera con el módulo `random` de Python, **fuera del cronómetro**: el
tiempo de generar los datos nunca entra en las mediciones.

* #### Clase Estudiante:
Define lo que representa un estudiante; cada uno tiene su id, nombre, edad y promedio. El id será la clave de búsqueda en los experimentos

* #### Generar_estudiantes:
Es una función que genera los estudiantes. Recibe como parámetros `n` estudiantes a generar y el `orden` que puede ser `aleatorio` u `ordenado`.
Aquí se generar los ids aleatoriamente desde 1000 hasta 1000 + n estudiantes. Luego según el parámetro de orden se ordenan crecientemente con sort(), sino, se dejan tal y como se generan.
Finalmente, se generan los n estudiantes asignandole a cada uno un ID y escogiendo un nombre, edad y promedio aleatorio (los nombres se escogen aleatoriamente de una lista definida). Y la lista se devuelve en el orden a insertar

* #### generar_busquedas:
Esta función escoge `m` ids aleatorios de la lista de estudiantes ya existente, y devuelve la lista de los ids a buscar en el experimento de búsquedas aleatorias.

* #### generar_rangos:
Esta función genera `Q` rangos de búsqueda cada uno con la misma cantidad `K` de estudiantes. 
Para generar los rangos, lo hace escogiendo aleatoriamente el ID de inicio verificando que no se se pase del límite número de estudiantes - `K` para que sea un rango válido


## 3. Diseño experimental (`experimentos.py`)

### 3.1 Metodología de los experimentos
En todos los experimentos se busca evaluar y comparar el rendimiento de las estructuras de datos (Lista, ABB y árbol B+) al variar el número de estudiantes (N) y el orden de inserción. Para que la comparación sea válida, se mantienen constantes los demás parámetros de cada experimento, como la cantidad de búsquedas o consultas realizadas y el tamaño de los rangos consultados. Para cada combinación de (N) y orden de inserción se realizan 20 repeticiones, con el fin de obtener resultados más representativos y reducir la influencia de variaciones puntuales en los tiempos de ejecución. La función de cada experimento se describe a continuación:

*  ###  E1  (`experimento_1_insercion`)
Se insertan N estudiantes, uno por uno, en cada estructura inicialmente vacía. La inserción se
hace con IDs aleatorios y con IDs en orden ascendente, para comparar el rendimiento de cada
estructura al cambiar el orden de inserción. Se cronometra el tiempo de insertar los N
estudiantes completos. Se realizan 20 repeticiones por cada combinación de `N` y orden de inserción.

* ### E2 (`experimento_2_busqueda`)
Sobre cada estructura ya construida con `N` estudiantes, se buscan `M = 1000` ids escogidos con la función `generar_busquedas`. Este experimento se hace tanto en la estructura construida con inserción aleatoria y en orden. Se evalúa cómo varía el rendimiento de las búsquedas al aumentar (N) y el orden de inserción, manteniendo constante la cantidad de búsquedas. Se cronometra únicamente el tiempo total de las (M) búsquedas; el tiempo de construcción de la estructura no se incluye. Se realizan 20 repeticiones por cada combinación de (N) y orden de inserción. 

* ### E3 (`experimento_3_listado`)
Sobre cada estructura ya construida con (N) estudiantes, se obtiene la secuencia completa de estudiantes ordenada por ID, tanto para estructuras construidas con IDs aleatorios como con IDs en orden ascendente. Se quiere evaluar cómo influye el orden de inserción y el aumento de `N` en el rendimiento del listado ordenado. Se cronometra únicamente la operación de listado; el tiempo de construcción de la estructura no se incluye. Se realizan 20 repeticiones por cada combinación de (N) y orden de inserción.

* ### E4 (`altura`)
No tiene una función propia, sino que la gráfica sale a partir de el CSV de `E1`
En este experimento se calcula la altura del árbol ABB y B+ para cada tamaño de estudiantes N y orden de inserción. Esto permite analizar cómo varía la altura de los árboles al aumentar `N` y  cómo influye el orden de inserción. 

* ### E5 (`experimento_5_rango`)
Sobre cada estructura ya construida, se ejecutan búsquedas para `Q = 1000` rangos, generados con la función `generar_rangos`. Se hace para los números de estudiantes mayores a 100 ya que cada rango devuelve ` K = 100` estudiantes y también se hace para cada orden de inserción. Se cronometra el tiempo total de las Q búsquedas.

Cada repetición del experimento se guarda en una fila de un CSV individual para cada experimento (excepto el 4).
  
## 3.2 Método de medición (`medir`)
Para medir los tiempos de ejecución se utiliza la función medir(), que emplea time.perf_counter() por su precisión para medir intervalos de tiempo cortos. Antes de cada medición, se ejecuta gc.collect() para liberar objetos que ya no se utilizan y se desactiva temporalmente el recolector de basura mediante gc.disable(), evitando que sus pausas interfieran con el tiempo registrado. Al finalizar, el recolector se vuelve a activar mediante gc.enable(), incluso si ocurre un error durante la ejecución.

Dentro de esta, se pone la función y se le pasan los argumentos necesarios de las que se quieran ejecutar puntualmente para medir sólo lo necesario de cada experimento.


## 3.3 Parámetros del experimento

- #### `NUM_BUSQUEDAS_INDIVIDUALES = 1000 (M)`:
  Se realizan 1.000 búsquedas por medición para obtener un tiempo más representativo del rendimiento de cada estructura y reducir la influencia de pequeñas variaciones en búsquedas individuales.
- #### `NUMERO_DE_RANGOS = 1000 (Q)`:
  Se ejecutan 1.000 consultas por rango para evaluar el rendimiento de esta operación sobre un conjunto suficiente de consultas y facilitar la comparación entre estructuras.
- #### `TAMANO_RANGO = 100 (K)`:
  Cada consulta devuelve exactamente 100 estudiantes para que todas las estructuras procesen la misma cantidad de resultados por consulta. Así, las diferencias de tiempo se relacionan principalmente con la forma en que cada estructura busca y recorre los datos, y no con que una tenga que devolver más estudiantes que otra.
- #### `TAMANOS = [10, 25, 50, 100, 300, 1000, 2000, 5000, 10000, 20000, 30000]`:
  Se utilizan tamaños crecientes para observar cómo cambia el rendimiento a medida que aumenta la cantidad de estudiantes. Incluir conjuntos pequeños y grandes permite identificar diferencias entre las estructuras que podrían no ser evidentes al evaluar un único tamaño, así como estudiar sus tendencias de crecimiento.
- #### `REPETICIONES = 20`:
  Se realizan 20 repeticiones por cada combinación de tamaño (N) y orden de inserción porque los tiempos pueden variar entre ejecuciones debido a factores externos, como la actividad del sistema operativo. Las repeticiones permiten calcular promedios, lo que ayuda a distinguir tendencias consistentes de resultados aislados.
- #### `ORDENES = ["aleatorio", "ordenado"]`:
  Se utilizan estos dos órdenes para estudiar cómo afecta la secuencia de inserción al rendimiento de cada estructura.

## 4. Estadísticas

## `Graficar.py`

Aquí se convierte los resultados crudos de los experimentos (archivos CSV) en las gráficas. No corre ningún experimento: solo lee los CSV que ya existen. Hace lo siguiente:

1. Lee los CSV de `datos/`.
2. Agrupa las repeticiones por combinación de **estructura, orden y N**.
3. Calcula el **promedio** y la **desviación estándar** de cada combinación.
4. Calcula la **pendiente log-log** de cada curva.
5. Dibuja una gráfica por experimento y una de la altura de los árboles, y las guarda en
   `graficas/`.

## Entradas y salidas

**Entradas** (generadas por el script de experimentos):

| Archivo | Experimento |
|---|---|
| `datos/e1_insercion.csv` | E1: inserción |
| `datos/e2_busqueda.csv` | E2: búsqueda por ID |
| `datos/e3_listado.csv` | E3: listado ascendente |
| `datos/e5_rango.csv` | E5: búsqueda por rango |

**Salidas** (carpeta `graficas/`):

- `E1_Inserción.png`
- `E2_Búsqueda_por_ID.png`
- `E3_Listado_ascendente.png`
- `E5_Búsqueda_por_rango.png`
- `altura_vs_N.png`

## Cómo se calcula cada cosa

### Promedio y desviación estándar
Para cada combinación (estructura, orden, N) se toman **todas** las repeticiones y se calcula su
promedio y su desviación estándar. En las gráficas, el punto es el promedio y las barras
y la franja sombreada son ±1 desviación estándar. 
La desviación estándar permite visualizar la variabilidad experimental, que puede deberse a la carga de la máquina o a la planificación de procesos del sistema operativo.

### Valores atípicos
**No se descarta ninguna repetición.** Para cada combinación se aplica la regla de Tukey: una
repetición se *marca* como atípica si queda fuera de `[Q1 − 1.5·IQR, Q3 + 1.5·IQR]`, donde Q1 y
Q3 son el primer y el tercer cuartil e IQR = Q3 − Q1. Solo se cuenta cuántas hay y se imprime en
consola, para poder reportarlo. Las repeticiones marcadas se mantienen en el promedio y la
desviación. Porque puede que sean atípicos por interferencias del sistema o no, entonces se mantienen para mantener la objetividad. Además comprobé que las pendientes no cambian de forma relevante con o sin ellos.

### Pendiente log-log
Es la pendiente de la recta que mejor ajusta `log10(promedio)` contra `log10(N)`, calculada con
`numpy.polyfit`. Si el tiempo sigue `T ≈ c · N^k`, la pendiente estima el exponente `k`
Lo que ayuda a verificar si se cumple con la complejidad teórica o no.

| Complejidad teórica | Comportamiento aproximado | Pendiente esperada |
|---|---|---|
| O(1) | Constante | 0 |
| O(log N) | Logarítmico | Tiende a 0 |
| O(N) | Lineal | 1 |
| O(N log N) | Lineal-logarítmico | ≈ 1.1  |
| O(N²) | Cuadrático | 2 |

- **Ventana del ajuste:** solo se usan los puntos con `N ≥ 1000` (constante `N_MIN_AJUSTE`). Con N
  pequeño el tiempo es de microsegundos y lo dominan costos fijos (llamadas, cronómetro, ruido),
  no el algoritmo. Todos los puntos se dibujan igual en la gráfica. Solo se usa así para el cálculo de la pendiente.
- La pendiente describe **cómo crece** el tiempo con N, no cuál estructura es más rápida. Eso lo
  indica la altura de la curva.

### Altura de los árboles
Para el archivo del experimento E1 se promedia la altura de todas las repeticiones para cada `N` en cada orden de inserción. La lista no aparece, porque no tiene altura.

## Cómo leer las gráficas

- Cada figura tiene **dos paneles**: IDs en orden aleatorio (izquierda) e IDs en orden
  ascendente (derecha).
- Cada panel tiene una curva por estructura: **Lista** (rosa), **ABB** (morado) y **B+** (verde).
- Los dos ejes están en **escala logarítmica**, siempre.
- El eje Y está en **segundos**, salvo en la gráfica de altura, donde son **niveles del árbol**.
- La leyenda muestra la pendiente de cada curva. El título de la leyenda recuerda que se calcula
  con `N ≥ 1000`.

## Funciones de Gráficas

- `cargar_datos`: lee los CSV que existan y los une en una sola tabla.
- `contar_atipicos`: cuenta las repeticiones de una combinación marcadas por la regla de Tukey.
- `agrupar`: calcula promedio, desviación y número de repeticiones por combinación, e imprime
  cuántas repeticiones se marcaron como atípicas.
- `agrupar_altura`: calcula promedio y desviación de la altura de los árboles.
- `calcular_pendiente`: regresión log-log con los puntos de `N ≥ N_MIN_AJUSTE`.
- `graficar_subplot`: dibuja un panel (un orden) con las curvas de las estructuras.
- `hacer_figura`: arma la figura de dos paneles y la guarda como imagen.
- `main`: encadena todo: carga, agrupa, grafica cada experimento y la altura.

## Análisis de los resultados
### E1: Inserción
<img width="2100" height="900" alt="image" src="https://github.com/user-attachments/assets/975c18b4-3523-4eda-bb97-cd47060ddca7" />

El panel izquierdo usa IDs en orden aleatorio y el derecho IDs en orden ascendente. Cada panel tiene una curva por estructura.

**En la inserción en orden aleatorio, se puede observar que:**

- La pendiente de la lista es **1.01** (esperado 1). Cada inserción es un `append`, que cuesta O(1), pero aquí se insertan N estudiantes, así que el tiempo total sí crece con N: si se duplica N, se duplica el tiempo. Por eso la pendiente es cercana de 1 y no 0 y tiene un comportamiento lineal.

- La pendiente del ABB es **1.22** (esperado ≈ 1.1) Cada inserción en este árbol es O(log(N)) y con N inserciones, el total es O(Nlog(N)). Por lo que el valor obtenido se aproxima a lo esperado en en el comportamiento.
  
- La pendiente obtenida en el B+ es **1.15** (esperada ≈ 1.1) Al igual al anterior se espera una complejidad O(Nlog(N)) y la pendiente obtenida se aproxima a la esperada.

En cuanto a eficiencia, al insertar los IDs aleatoriamente la estructura más rápida (con la curva más baja) es la **Lista** porque se hace solo con append. El árbol **ABB** es un poco más rápido que el **B+** porque el B+ trabaja más en cada inserción, ya que busca dentro del nodo, y cuando lo inserta y enlaza con los demás estudiantes y a veces debe dividir las hojas.

**En la inserción en orden, se puede observar que:**

- La pendiente de la lista es **1** que es igual al esperado para que la complejidad sea compatible con la lineal O(N). Aquí también se hace la misma operación de la inserción en orden aleatorio, la diferencia de pendientes pudo haber ocurrido por ruido experimental, pero la diferencia no es significativa en la complejidad algorítmica.
  
- La pendiente en el ABB es **2.09** (esperada 2). Aquí se espera que la complejidad sea cuadrática porque al insertar en orden el árbol se degenera y termina como una lista enlazada y cada inserción tiene que recorrer todo lo que ya hay.
  
- La pendiente en el B+ es **1.20** (esperada 1.1) aquí se esperaba también una complejidad de O(Nlog(N)) porque el orden de entrada no degrada la estructura porque cuando un nodo se llena, se divide y el árbol crece hacia arriba y gracias a eso suele tener entre 3 a 4 niveles; además, el grado de los nodos es de 50 para que no se tenga que dividir tanto los nodos, lo que evita que el árbol crezca como lista como el ABB.

En cuanto a eficiencia, la lista sigue siendo la más eficiente, ya que es la estructura más simple y barata para insertar, pero en este caso, el árbol **B+** es más eficiente que el árbol **ABB** porque este se vuelve cuadrático y mientras crezca N se vuelve más lento, en cambio el B+ no es muy afectado por el orden de inserción.

En conclusión, insertar en una lista es lo más barato.

### E2: Búsqueda por ID
<img width="2100" height="900" alt="image" src="https://github.com/user-attachments/assets/76a0e312-88a9-455a-9a8c-fd7e0e146bff" />

El panel izquierdo usa IDs en orden aleatorio y el derecho IDs en orden ascendente. Cada panel tiene una curva por estructura.

**En la búsqueda con IDs con inserción aleatoria, se puede observar que:**

- La pendiente de la lista es **1.08** (esperada  1). Para encontrar un estudiante la lista lo busca uno por uno desde el inicio, cada búsqueda cuesta O(N) entonces todas las M búsquedas cuestan **O(M*N)**. Como M es fijo, el tiempo crece al mismo ritmo que N y es lineal. La pendiente encontrada estuvo aproximada la complejidad real.
  
- La pendiente del ABB es **0.23** (esperada ≈ 0.1 a 0.14). Cada búsqueda cuesta O(log(N)). al ser **M** búsquedas, termina siendo O(Mlog(N)) pero como M es constante, se puede ignorar y el costo sigue siendo logarítmico. El valor de la pendiente queda por encima de lo esperado porque en el último punto crece más rápido de lo normal.
  
- La pendiente del B+ es **0.16** ( esperada ≈ 0.1 a 0.14). También cuesta O(log(N)) como el árbol anterior y la pendiente obtenida se acerca a lo esperado.

En cuanto a la eficiencia, con IDs aleatorios las dos estructuras en árbol son mucho más rápidas que la lista cuando N crece. El **ABB** es la estructura más rápida y el **B+** un poco menos rápido. Aunque los dos tienen el mismo costo computacional, el B+ trabaja más en cada búsqueda porque recorre las claves de cada nodo linealmente para encontrar la rama por la que debe bajar. 


**En la búsqueda con IDs con inserción en orden ascendente, se puede observar que:**

- La pendiente de la lista es **1.04** (esperada 1). Es el mismo algoritmo que en aleatorio, y
  el orden en que se insertaron los estudiantes no cambia el recorrido, así que su
  comportamiento es lineal.
  
-  La pendiente del ABB es **1.04** (esperada 1). Como con IDs ascendentes el árbol queda como una lista enlazada y buscar un estudiante obliga a recorrer  la cadena, así que la búsqueda deja de ser O(log N) y pasa a ser O(N). La pendiente pasó de 0.23 en aleatorio a 1.04 en ascendente.

- La pendiente del B+ es **0.13** (esperada ≈ 0.1 a 0.14). Es casi igual que en aleatorio: como
  el B+ se mantiene balanceado, el orden de inserción no le afecta.

En cuanto a eficiencia, con IDs ascendentes el **B+** es claramente el mejor.  El **ABB** pasa a ser el peor, incluso más lento que la lista. Aunque ambos son lineales, recorrer nodos enlazados por punteros cuesta más que recorrer un arreglo.

En conclusión, la lista es la peor en cuanto a tiempo para realizar las búsquedas. Los árboles solo son mejores si no se degeneran. Además, el ABB es la mejor opción para buscar, pero solo con IDs en orden aleatorio al insertarlos porque si se insertan en orden, se vuelve peor que la lista. Y por último, el B+ es el más estable, ya que la curva no cambia casi nada con el orden y el tiempo de respuesta es muy bueno.


### 6.3 E3: Listado ascendente

<img width="2100" height="900" alt="image" src="https://github.com/user-attachments/assets/6a9f9def-321e-4b7a-9f14-1af37835ce0e" />

El panel izquierdo usa IDs en orden aleatorio y el derecho IDs en orden ascendente. Cada panel tiene una curva por estructura.

**En el listado con IDs en orden aleatorio, se puede observar que:**

- La pendiente de la lista es **1.16** (esperada 1.1). Para listar, la lista se ordena primero con `sort()` y con datos desordenados cuesta 0(Nlog(N)). Por eso es la pendiente más alta.

-  La pendiente del ABB es **1.08** (esperada  1). El árbol El árbol ya guarda los estudiantes en orden, por lo que solo hay que recorrer los N nodos, lo que cuesta O(N)

-  La pendiente del B+ es **1.08** (esperada 1). También recorre los N estudiantes una vez, por
  las hojas enlazadas, y cuesta O(N).

En cuanto a la eficiencia, con IDs aleatorios la estructura más rápida es el **B+**, seguida del **ABB** y luego la **Lista** que es la más lenta porque es la única que tiene que ordenar. El B+ es más rápido que el ABB porque los estudiantes están enlazados y puede saltar entre ellos, mientras que el ABB tiene que subir y bajar varias veces entre nodos.

**En el listado con IDs en orden ascendente, se puede observar que:**

- La pendiente de la lista es **1.04** (esperada 1). Aquí los estudiantes ya están ordenados y sort() de python lo detecta, así que el costo baja a ser lineal.
  
- La pendiente del ABB es **0.95** ( esperada 1). El árbol está degenerado pero para listar todos los estudiantes no necesita buscar, solo recorrer los N nodos, así que sigue siendo lineal su costo.
  
- La pendiente del B+ es **0.93** (esperada 1). Realiza el mismo proceso de recorrer las hojas por lo que debería seguir siendo lineal.

En cuanto a eficiencia, con IDs ascendentes el **B+** sigue siendo el más rápido, pero el ABB pasa a ser el más lento, porque recorrer una lista enlazada cuesta más que retornar una lista que ya estaba ordenada.

En conclusión, el costo para listar en orden todos los elementos en los árboles es lineal, sin importar el orden de inserción, porque solo se recorren todos los estudiantes. La lista en cambio, si cuesta más por tener que ordenarla en caso de que los IDs estén desordenados.  
El B+ es el más rápido en cualquier orden. Con IDs ordenados, el ABB pasa a ser más lento que una lista ya ordenada aunque sigue siendo lineal.
Las pendientes obtenidas están cerca de 1, que era lo esperado.



  

  

