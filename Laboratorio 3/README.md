# Laboratorio 3: Sistema de Administración de Estudiantes

## 1. Problema y objetivo

### Problema
Una institución educativa necesita administrar la información de sus estudiantes. Cada
registro contiene ID (matrícula única), nombre, edad y promedio. El sistema debe permitir:

1. Buscar un estudiante por su ID.
2. Insertar un nuevo estudiante.
3. Listar todos los estudiantes en orden ascendente de ID.

Además de estas tres operaciones se evaluó la búsqueda por rango de IDs.

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


