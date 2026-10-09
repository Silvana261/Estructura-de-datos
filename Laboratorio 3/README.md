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
**lista**, **árbol binario de búsqueda (ABB)** y **árbol B+**, y se contrastan los resultados
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
las operaciones son iterativas (con pila o ciclo, sin recursión). Ya que python tiene un límite de recursión.

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
  - IDs ascendentes: N

### 2.3 Árbol B+ (`ArbolBMas.py`)

Árbol balanceado donde **todos los estudiantes están en las hojas**, y los nodos internos solo
guardan claves que orientan la búsqueda. Las hojas están enlazadas entre sí (`siguiente`), lo
que permite recorrerlas en orden sin volver a subir al árbol.
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

### 2.3  GenerarDatos.py

Todo se genera con el módulo `random` de Python, **fuera del cronómetro**: el
tiempo de generar los datos nunca entra en las mediciones.

#### Clase Estudiante:
Define lo que representa un estudiante; cada uno tiene su id, nombre, edad y promedio. El id será la clave de búsqueda en los experimentos

#### Generar_estudiantes:
Es una función que genera los estudiantes. Recibe como parámetros `n` estudiantes a generar y el `orden` que puede ser `aleatorio` u `ordenado`.
Aquí se generar los ids aleatoriamente desde 1000 hasta 1000 + n estudiantes. Luego según el parámetro de orden se ordenan crecientemente con sort(), sino, se dejan tal y como se generan.
Finalmente, se generan los n estudiantes asignandole a cada uno un ID y escogiendo un nombre, edad y promedio aleatorio (los nombres se escogen aleatoriamente de una lista definida). Y la lista se devuelve en el orden a insertar

#### generar_busquedas:
Esta función escoge `m` ids aleatorios de la lista de estudiantes ya existente, y devuelve la lista de los ids a buscar en el experimento de búsquedas aleatorias.

#### generar_rangos:
Esta función genera `Q` rangos de búsqueda cada uno con la misma cantidad `K` de estudiantes. 
Para generar los rangos, lo hace escogiendo aleatoriamente el ID de inicio verificando que no se se pase del límite número de estudiantes - `K` para que sea un rango válido



## 3. Diseño experimental (`experimentos.py`)

Este archivo contiene el cronómetro común a todos los experimentos y los parámetros que
controlan cómo se corren. Las funciones `experimento_1_insercion`, `experimento_2_busqueda`,
`experimento_3_listado` y `experimento_5_rango` reutilizan ambos.

### 3.1 Función `medir`

- **`gc.collect()` antes de medir:** fuerza una recolección de basura completa justo antes de
  arrancar el cronómetro. Así se "limpia" cualquier objeto pendiente de liberar que se haya
  acumulado en la repetición anterior, y se reduce la probabilidad de que el recolector decida
  dispararse por sí solo durante la medición siguiente.
- **`gc.disable()` durante la medición:** el recolector de basura de Python puede activarse en
  cualquier momento, incluso a mitad de la función que se está cronometrando, y añadir una pausa
  impredecible al tiempo medido. Desactivarlo elimina esa fuente de ruido del sistema, para que
  el tiempo reportado refleje el trabajo real del algoritmo y no una interrupción externa.
- **`time.perf_counter()`:** se usa en vez de `time.time()` porque es un reloj de alta resolución
  pensado específicamente para medir intervalos cortos de tiempo, no afectado por ajustes del
  reloj del sistema (como la sincronización horaria).
- **Qué queda fuera del cronómetro:** solo se mide `funcion(*args)`. La generación de los
  estudiantes, de los IDs a buscar y de los rangos, así como la construcción de la estructura en
  los experimentos 2 y 5, ocurre *antes* de llamar a `medir`, para que el tiempo reportado
  corresponda únicamente a la operación que se quiere estudiar (inserción, búsqueda, listado o
  rango), y no a la preparación de los datos. 

### 3.2 Parámetros del experimento

- **`NUM_BUSQUEDAS_INDIVDUALES` (M = 1000)** y **`NUMERO_DE_RANGOS` (Q = 1000):** una sola
  búsqueda o un solo rango tarda microsegundos, un tiempo demasiado pequeño para medirse con
  precisión y fácilmente dominado por el overhead fijo de Python. Agrupar M búsquedas (o Q
  rangos) dentro de un mismo bloque cronometrado amortigua ese overhead entre muchas operaciones
  y lleva el tiempo total de la corrida a un rango donde el reloj del sistema puede medirlo con
  confianza.
- **`TAMANO_RANGO` (K = 100):** se mantiene **constante** en todos los N para aislar el efecto
  que se quiere estudiar. El costo teórico de una consulta de rango tiene la forma
  O(costo_de_llegar + K): si K variara junto con N, el tiempo medido mezclaría dos efectos
  distintos —cuánto cuesta ubicar el inicio del rango, y cuánto cuesta recorrer los resultados—
  y no se podría atribuir un cambio en el tiempo a uno u otro. Con K fijo, el término K es
  idéntico en cada medición, así que cualquier diferencia observada al variar N proviene
  exclusivamente del costo de localizar el inicio del rango, que es lo que distingue a las tres
  estructuras entre sí.
  

